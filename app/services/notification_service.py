from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import BufferedInputFile

from app.config import Settings, get_settings
from app.keyboards.admin import lead_actions_keyboard
from app.models.enums import LeadStatus
from app.models.lead import Lead
from app.utils.formatting import format_lead_card, html_text

logger = logging.getLogger(__name__)


async def notify_admins(bot: Bot, lead: Lead, settings: Settings | None = None) -> None:
    settings = settings or get_settings()
    text = "New lead received.\n\n" + format_lead_card(lead, include_admin=False)
    markup = lead_actions_keyboard(lead.id)
    for admin_id in settings.admin_id_set:
        try:
            await bot.send_message(
                admin_id,
                text,
                reply_markup=markup,
            )
        except TelegramAPIError:
            logger.exception("Failed to notify administrator", extra={"user_id": admin_id})


async def notify_customer_status_change(
    bot: Bot,
    lead: Lead,
    previous: LeadStatus,
    current: LeadStatus,
) -> None:
    if previous == current:
        return
    text = (
        f"Update on <b>{html_text(lead.public_id)}</b>: "
        f"status is now <b>{html_text(current.label)}</b>."
    )
    try:
        await bot.send_message(lead.telegram_user_id, text)
    except TelegramAPIError:
        logger.exception(
            "Failed to notify customer about status change",
            extra={"user_id": lead.telegram_user_id, "public_id": lead.public_id},
        )


async def send_csv_export(bot: Bot, chat_id: int, payload: bytes) -> None:
    document = BufferedInputFile(payload, filename="leadflow-leads.csv")
    await bot.send_document(chat_id, document, caption="LeadFlow export")
