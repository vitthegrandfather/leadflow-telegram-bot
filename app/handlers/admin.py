from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.keyboards.admin import admin_home_keyboard, lead_actions_keyboard, lead_list_keyboard
from app.models.enums import LeadStatus
from app.services.auth_service import require_admin
from app.services.export_service import leads_to_csv
from app.services.lead_service import LeadNotFoundError, LeadService
from app.services.notification_service import notify_customer_status_change, send_csv_export
from app.states.admin import AdminNote
from app.utils.formatting import format_lead_brief, format_lead_card, html_text

router = Router(name="admin")

PER_PAGE = 5


def _stats_text(stats: dict[str, int]) -> str:
    return (
        "<b>LeadFlow desk</b>\n\n"
        f"Total: {stats['total']}\n"
        f"New: {stats['new']}\n"
        f"In progress: {stats['in_progress']}\n"
        f"Completed: {stats['completed']}\n"
        f"Cancelled: {stats['cancelled']}"
    )


async def _deny(event: Message | CallbackQuery) -> None:
    text = "This command is limited to administrators."
    if isinstance(event, CallbackQuery):
        await event.answer(text, show_alert=True)
        return
    await event.answer(text)


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext, lead_service: LeadService) -> None:
    user = message.from_user
    if user is None or not _is_admin(user.id):
        await _deny(message)
        return
    await state.clear()
    stats = await lead_service.stats()
    await message.answer(_stats_text(stats), reply_markup=admin_home_keyboard())


def _is_admin(user_id: int) -> bool:
    try:
        require_admin(user_id)
        return True
    except PermissionError:
        return False


@router.callback_query(F.data == "a:h")
async def admin_home(callback: CallbackQuery, lead_service: LeadService) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny(callback)
        return
    stats = await lead_service.stats()
    await callback.answer()
    if callback.message:
        await callback.message.edit_text(_stats_text(stats), reply_markup=admin_home_keyboard())


@router.callback_query(F.data.startswith("a:p:"))
async def admin_page(callback: CallbackQuery, lead_service: LeadService) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny(callback)
        return
    try:
        page = int((callback.data or "a:p:0").split(":")[-1])
    except ValueError:
        await callback.answer("This action is no longer available.", show_alert=True)
        return
    leads, total = await lead_service.recent(page=page, per_page=PER_PAGE)
    if not leads:
        text = "No leads yet."
    else:
        text = "Recent leads:\n\n" + "\n".join(format_lead_brief(lead) for lead in leads)
    await callback.answer()
    if callback.message:
        await callback.message.edit_text(
            text,
            reply_markup=lead_list_keyboard(leads, page=page, total=total, per_page=PER_PAGE),
        )


@router.callback_query(F.data.startswith("a:l:"))
async def admin_lead(callback: CallbackQuery, lead_service: LeadService) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny(callback)
        return
    try:
        lead_id = int((callback.data or "").split(":")[-1])
        lead = await lead_service.get(lead_id)
    except (ValueError, LeadNotFoundError):
        await callback.answer("This lead is no longer available.", show_alert=True)
        return
    await callback.answer()
    if callback.message:
        await callback.message.edit_text(
            format_lead_card(lead, include_admin=True),
            reply_markup=lead_actions_keyboard(lead.id),
        )


@router.callback_query(F.data.startswith("a:s:"))
async def admin_status(callback: CallbackQuery, lead_service: LeadService) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny(callback)
        return
    parts = (callback.data or "").split(":")
    if len(parts) != 4:
        await callback.answer("This action is no longer available.", show_alert=True)
        return
    try:
        lead_id = int(parts[2])
        status = LeadStatus(parts[3])
    except ValueError:
        await callback.answer("This action is no longer available.", show_alert=True)
        return
    lead, previous, changed = await lead_service.change_status(lead_id, status)
    if changed:
        await notify_customer_status_change(callback.bot, lead, previous, lead.status)
        await callback.answer(f"Status set to {lead.status.label}.")
    else:
        await callback.answer("Status is already set.")
    if callback.message:
        await callback.message.edit_text(
            format_lead_card(lead, include_admin=True),
            reply_markup=lead_actions_keyboard(lead.id),
        )


@router.callback_query(F.data.startswith("a:n:"))
async def admin_note_prompt(
    callback: CallbackQuery, state: FSMContext, lead_service: LeadService
) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny(callback)
        return
    try:
        lead_id = int((callback.data or "").split(":")[-1])
        lead = await lead_service.get(lead_id)
    except (ValueError, LeadNotFoundError):
        await callback.answer("This lead is no longer available.", show_alert=True)
        return
    await state.set_state(AdminNote.waiting_text)
    await state.update_data(note_lead_id=lead.id)
    await callback.answer()
    if callback.message:
        await callback.message.answer(
            f"Send an internal note for <b>{html_text(lead.public_id)}</b>. "
            "This replaces any existing note. /cancel to abort."
        )


@router.message(AdminNote.waiting_text)
async def admin_note_capture(
    message: Message,
    state: FSMContext,
    lead_service: LeadService,
) -> None:
    if not message.from_user or not _is_admin(message.from_user.id):
        await _deny(message)
        await state.clear()
        return
    if not message.text:
        await message.answer("Please send the note as text.")
        return
    data = await state.get_data()
    lead_id = data.get("note_lead_id")
    if not isinstance(lead_id, int):
        await state.clear()
        await message.answer("I lost track of that lead. Open it again from the list.")
        return
    lead = await lead_service.set_note(lead_id, message.text)
    await state.clear()
    await message.answer(
        format_lead_card(lead, include_admin=True),
        reply_markup=lead_actions_keyboard(lead.id),
    )


@router.callback_query(F.data == "a:x")
async def admin_export(callback: CallbackQuery, lead_service: LeadService) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny(callback)
        return
    leads = await lead_service.export_rows()
    payload = leads_to_csv(leads)
    await callback.answer("Preparing export.")
    await send_csv_export(callback.bot, callback.from_user.id, payload)
