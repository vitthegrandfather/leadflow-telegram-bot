from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiogram.exceptions import TelegramAPIError
from aiogram.methods import SendMessage

from app.config import Settings
from app.models.enums import ContactMethod, LeadStatus, ServiceCategory
from app.services.notification_service import notify_admins, notify_customer_status_change


def _lead() -> SimpleNamespace:
    return SimpleNamespace(
        id=1,
        public_id="LF-260905-ABCD",
        status=LeadStatus.NEW,
        full_name="Maya Chen",
        phone="+14155550114",
        username="maya",
        telegram_user_id=222222,
        service_category=ServiceCategory.WEBSITE_DEVELOPMENT,
        preferred_contact_method=ContactMethod.EMAIL,
        created_at=datetime(2026, 9, 5, tzinfo=timezone.utc),
        description="Need a marketing site with an enquiry form.",
        admin_note=None,
    )


@pytest.mark.asyncio
async def test_notify_admins_continues_after_failure() -> None:
    bot = AsyncMock()
    bot.send_message = AsyncMock(
        side_effect=[
            TelegramAPIError(method=SendMessage(chat_id=1, text="x"), message="fail"),
            None,
        ]
    )
    settings = Settings(admin_ids="1,2", bot_token="")
    await notify_admins(bot, _lead(), settings=settings)  # type: ignore[arg-type]
    assert bot.send_message.await_count == 2


@pytest.mark.asyncio
async def test_status_notification_skipped_when_unchanged() -> None:
    bot = AsyncMock()
    await notify_customer_status_change(bot, _lead(), LeadStatus.NEW, LeadStatus.NEW)  # type: ignore[arg-type]
    bot.send_message.assert_not_awaited()
