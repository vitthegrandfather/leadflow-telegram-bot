from __future__ import annotations

import asyncio
import logging

from app.bot import create_bot, create_dispatcher
from app.config import get_settings
from app.database.session import ensure_sqlite_dir, init_db
from app.logging import setup_logging

logger = logging.getLogger(__name__)


def _require_runtime_settings() -> None:
    settings = get_settings()
    if not settings.bot_token.strip():
        raise SystemExit(
            "BOT_TOKEN is required. Copy .env.example to .env and add a BotFather token."
        )
    try:
        admin_ids = settings.admin_id_set
    except ValueError as exc:
        raise SystemExit("ADMIN_IDS must be a comma-separated list of integers.") from exc
    if not admin_ids:
        raise SystemExit("ADMIN_IDS must contain at least one Telegram user ID.")


async def run() -> None:
    settings = get_settings()
    session_factory = await init_db(settings)
    bot = create_bot(settings)
    dp = create_dispatcher(session_factory)
    logger.info("LeadFlow Bot starting")
    await dp.start_polling(bot)


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)
    _require_runtime_settings()
    ensure_sqlite_dir(settings.database_url)
    asyncio.run(run())


if __name__ == "__main__":
    main()
