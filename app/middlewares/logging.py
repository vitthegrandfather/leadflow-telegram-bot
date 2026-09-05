from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

logger = logging.getLogger(__name__)


class UpdateLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        extra: dict[str, Any] = {"user_id": getattr(user, "id", None)}
        if isinstance(event, CallbackQuery):
            extra["callback"] = event.data
        elif isinstance(event, Message) and event.text:
            extra["callback"] = event.text.split()[0][:32]
        logger.info("update received", extra=extra)
        return await handler(event, data)
