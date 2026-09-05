from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import Settings
from app.handlers import setup_routers
from app.middlewares.auth import AdminCallbackMiddleware
from app.middlewares.db import DatabaseMiddleware
from app.middlewares.logging import UpdateLoggingMiddleware


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher(session_factory: async_sessionmaker) -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(UpdateLoggingMiddleware())
    dp.update.middleware(DatabaseMiddleware(session_factory))
    dp.callback_query.middleware(AdminCallbackMiddleware())
    setup_routers(dp)
    return dp
