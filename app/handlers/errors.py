from __future__ import annotations

import logging

from aiogram import Dispatcher
from aiogram.exceptions import TelegramAPIError
from aiogram.types import ErrorEvent

from app.services.auth_service import UnauthorizedAdminError
from app.services.lead_service import LeadNotFoundError
from app.services.validation import ValidationError

logger = logging.getLogger(__name__)

USER_ERROR = "Something went wrong on my side. Please try again in a moment."


def register_error_handlers(dp: Dispatcher) -> None:
    @dp.error()
    async def on_error(event: ErrorEvent) -> bool:
        err = event.exception
        if isinstance(err, UnauthorizedAdminError):
            update = event.update
            if update.callback_query:
                await update.callback_query.answer(str(err), show_alert=True)
            elif update.message:
                await update.message.answer(str(err))
            return True
        if isinstance(err, (ValidationError, LeadNotFoundError)):
            update = event.update
            text = str(err)
            if update.callback_query:
                await update.callback_query.answer(text, show_alert=True)
            elif update.message:
                await update.message.answer(text)
            return True

        logger.exception("Unhandled bot error", exc_info=err)
        update = event.update
        try:
            if update.callback_query:
                await update.callback_query.answer(USER_ERROR, show_alert=True)
            elif update.message:
                await update.message.answer(USER_ERROR)
        except TelegramAPIError:
            logger.exception("Failed to send error message to user")
        return True
