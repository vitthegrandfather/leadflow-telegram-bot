from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.customer import (
    back_to_menu_keyboard,
    category_keyboard,
    confirmation_keyboard,
    contact_keyboard,
    edit_field_keyboard,
    main_menu_keyboard,
)
from app.services.lead_service import DuplicateLeadError, LeadDraft, LeadService
from app.services.notification_service import notify_admins
from app.services.validation import (
    ValidationError,
    normalize_phone,
    parse_category,
    parse_contact_method,
    validate_description,
    validate_name,
)
from app.states.lead_form import LeadForm
from app.utils.formatting import format_lead_brief, html_text

router = Router(name="customer")

WELCOME = (
    "LeadFlow is a request desk for a small service studio. "
    "Send a structured brief and the team will follow up using the contact method you prefer."
)
ABOUT = (
    "This is a personal portfolio demonstration of a Telegram lead bot with a lightweight "
    "CRM workflow. It is not a live client product and does not represent paid client work."
)
ASK_NAME = "What is your full name?"
ASK_PHONE = "What is the best phone number to reach you?"
ASK_CATEGORY = "Which service are you looking for?"
ASK_DESCRIPTION = "Briefly describe the project. A few sentences is enough."
ASK_CONTACT = "How should we contact you?"
NEED_TEXT = "Please send that as text."


def _summary(data: dict) -> str:
    return (
        "Please confirm this request:\n"
        f"Name: {html_text(data.get('full_name', ''))}\n"
        f"Phone: {html_text(data.get('phone', ''))}\n"
        f"Service: {html_text(data.get('category_label', ''))}\n"
        f"Contact: {html_text(data.get('contact_label', ''))}\n"
        f"Brief: {html_text(data.get('description', ''))}"
    )


async def _safe_edit(callback: CallbackQuery, text: str, markup=None) -> None:
    await callback.answer()
    if callback.message:
        await callback.message.edit_text(text, reply_markup=markup)
    elif callback.from_user:
        await callback.bot.send_message(callback.from_user.id, text, reply_markup=markup)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(WELCOME, reply_markup=main_menu_keyboard())


@router.message(Command("cancel"))
@router.callback_query(F.data == "c:x")
async def cancel_flow(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text = "Request cancelled. You can start again from the menu whenever you like."
    if isinstance(event, CallbackQuery):
        await _safe_edit(event, text, main_menu_keyboard())
        return
    await event.answer(text, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "m:h")
async def menu_home(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await _safe_edit(callback, WELCOME, main_menu_keyboard())


@router.callback_query(F.data == "m:a")
async def menu_about(callback: CallbackQuery) -> None:
    await _safe_edit(callback, ABOUT, back_to_menu_keyboard())


@router.callback_query(F.data == "m:s")
async def menu_submit(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(LeadForm.full_name)
    await _safe_edit(callback, ASK_NAME)


@router.callback_query(F.data == "m:r")
async def menu_requests(
    callback: CallbackQuery,
    lead_service: LeadService,
) -> None:
    user = callback.from_user
    if user is None:
        await callback.answer("This action is no longer available.", show_alert=True)
        return
    leads = await lead_service.list_for_user(user.id)
    if not leads:
        text = "You have not submitted a request yet."
    else:
        lines = [format_lead_brief(lead) for lead in leads[:20]]
        text = "Your requests:\n\n" + "\n".join(lines)
    await _safe_edit(callback, text, back_to_menu_keyboard())


@router.message(LeadForm.full_name)
async def capture_name(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(NEED_TEXT)
        return
    try:
        name = validate_name(message.text)
    except ValidationError as exc:
        await message.answer(str(exc))
        return
    data = await state.update_data(full_name=name)
    if data.get("phone") and data.get("description") and data.get("contact_method"):
        await state.set_state(LeadForm.confirm)
        await message.answer(_summary(data), reply_markup=confirmation_keyboard())
        return
    await state.set_state(LeadForm.phone)
    await message.answer(ASK_PHONE)


@router.message(LeadForm.phone)
async def capture_phone(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(NEED_TEXT)
        return
    try:
        phone = normalize_phone(message.text)
    except ValidationError as exc:
        await message.answer(str(exc))
        return
    data = await state.update_data(phone=phone)
    if data.get("service_category"):
        await state.set_state(LeadForm.confirm)
        await message.answer(_summary(data), reply_markup=confirmation_keyboard())
        return
    await state.set_state(LeadForm.category)
    await message.answer(ASK_CATEGORY, reply_markup=category_keyboard())


@router.callback_query(LeadForm.category, F.data.startswith("c:cat:"))
async def capture_category(callback: CallbackQuery, state: FSMContext) -> None:
    value = (callback.data or "").split(":")[-1]
    try:
        category = parse_category(value)
    except ValidationError as exc:
        await callback.answer(str(exc), show_alert=True)
        return
    data = await state.update_data(
        service_category=category.value,
        category_label=category.label,
    )
    if data.get("description"):
        await state.set_state(LeadForm.confirm)
        await _safe_edit(callback, _summary(data), confirmation_keyboard())
        return
    await state.set_state(LeadForm.description)
    await _safe_edit(callback, ASK_DESCRIPTION)


@router.message(LeadForm.description)
async def capture_description(message: Message, state: FSMContext) -> None:
    if not message.text:
        await message.answer(NEED_TEXT)
        return
    try:
        description = validate_description(message.text)
    except ValidationError as exc:
        await message.answer(str(exc))
        return
    data = await state.update_data(description=description)
    if data.get("preferred_contact_method"):
        await state.set_state(LeadForm.confirm)
        await message.answer(_summary(data), reply_markup=confirmation_keyboard())
        return
    await state.set_state(LeadForm.contact_method)
    await message.answer(ASK_CONTACT, reply_markup=contact_keyboard())


@router.callback_query(LeadForm.contact_method, F.data.startswith("c:cm:"))
async def capture_contact(callback: CallbackQuery, state: FSMContext) -> None:
    value = (callback.data or "").split(":")[-1]
    try:
        method = parse_contact_method(value)
    except ValidationError as exc:
        await callback.answer(str(exc), show_alert=True)
        return
    data = await state.update_data(
        preferred_contact_method=method.value,
        contact_label=method.label,
    )
    await state.set_state(LeadForm.confirm)
    await _safe_edit(callback, _summary(data), confirmation_keyboard())


@router.callback_query(LeadForm.confirm, F.data == "c:ed")
async def edit_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await _safe_edit(callback, "Which field should I change?", edit_field_keyboard())


@router.callback_query(LeadForm.confirm, F.data.startswith("c:e:"))
@router.callback_query(F.data.startswith("c:e:"))
async def edit_field(callback: CallbackQuery, state: FSMContext) -> None:
    field = (callback.data or "").split(":")[-1]
    if field == "name":
        await state.set_state(LeadForm.full_name)
        await _safe_edit(callback, ASK_NAME)
    elif field == "phone":
        await state.set_state(LeadForm.phone)
        await _safe_edit(callback, ASK_PHONE)
    elif field == "cat":
        await state.set_state(LeadForm.category)
        await _safe_edit(callback, ASK_CATEGORY, category_keyboard())
    elif field == "desc":
        await state.set_state(LeadForm.description)
        await _safe_edit(callback, ASK_DESCRIPTION)
    elif field == "cm":
        await state.set_state(LeadForm.contact_method)
        await _safe_edit(callback, ASK_CONTACT, contact_keyboard())
    else:
        await callback.answer("This action is no longer available.", show_alert=True)


@router.callback_query(LeadForm.confirm, F.data == "c:ok")
async def confirm_lead(
    callback: CallbackQuery,
    state: FSMContext,
    lead_service: LeadService,
    session: AsyncSession,
) -> None:
    user = callback.from_user
    if user is None:
        await callback.answer("This action is no longer available.", show_alert=True)
        return
    data = await state.get_data()
    required = (
        "full_name",
        "phone",
        "service_category",
        "description",
        "preferred_contact_method",
    )
    if any(not data.get(key) for key in required):
        await callback.answer("Please complete every field first.", show_alert=True)
        return
    draft = LeadDraft(
        full_name=data["full_name"],
        phone=data["phone"],
        service_category=parse_category(data["service_category"]),
        description=data["description"],
        preferred_contact_method=parse_contact_method(data["preferred_contact_method"]),
    )
    try:
        lead = await lead_service.create_lead(
            telegram_user_id=user.id,
            username=user.username,
            draft=draft,
        )
    except DuplicateLeadError as exc:
        await state.clear()
        await _safe_edit(
            callback,
            (
                f"A matching request is already in the queue as "
                f"<b>{html_text(exc.lead.public_id)}</b>. I did not create a duplicate."
            ),
            main_menu_keyboard(),
        )
        return
    await session.commit()
    await notify_admins(callback.bot, lead)
    await state.clear()
    await _safe_edit(
        callback,
        (
            f"Request <b>{html_text(lead.public_id)}</b> is in the queue. "
            "An administrator will review it shortly."
        ),
        main_menu_keyboard(),
    )


@router.callback_query()
async def unknown_callback(callback: CallbackQuery) -> None:
    await callback.answer("This action is no longer available.", show_alert=True)
