from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject

from app.services.auth_service import is_admin


class AdminCallbackMiddleware(BaseMiddleware):
    """Blocks admin callback prefixes for non-administrators."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, CallbackQuery):
            payload = event.data or ""
            if payload.startswith("a:"):
                user = event.from_user
                if not is_admin(user.id if user else None):
                    await event.answer("This action is limited to administrators.", show_alert=True)
                    return None
        return await handler(event, data)
