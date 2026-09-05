from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.handlers import admin
from app.models.enums import ContactMethod, LeadStatus, ServiceCategory
from app.services.lead_service import LeadDraft, LeadService
from tests.conftest import TEST_ADMIN_ID


def admin_callback(data: str) -> AsyncMock:
    item = AsyncMock()
    item.data = data
    item.from_user.id = TEST_ADMIN_ID
    item.answer = AsyncMock()
    item.message.edit_text = AsyncMock()
    return item


@pytest.mark.asyncio
async def test_admin_status_change_notifies_customer(
    monkeypatch: pytest.MonkeyPatch,
    lead_service: LeadService,
) -> None:
    lead = await lead_service.create_lead(
        telegram_user_id=222222,
        username="customer",
        draft=LeadDraft(
            full_name="Maya Chen",
            phone="+14155550114",
            service_category=ServiceCategory.TELEGRAM_BOT,
            description="Build a Telegram assistant for incoming service requests.",
            preferred_contact_method=ContactMethod.TELEGRAM,
        ),
    )
    monkeypatch.setattr(admin, "_is_admin", lambda _user_id: True)
    notify = AsyncMock()
    monkeypatch.setattr(admin, "notify_customer_status_change", notify)
    event = admin_callback(f"a:s:{lead.id}:in_progress")

    await admin.admin_status(event, lead_service)  # type: ignore[arg-type]

    updated = await lead_service.get(lead.id)
    assert updated.status is LeadStatus.IN_PROGRESS
    notify.assert_awaited_once_with(
        event.bot,
        updated,
        LeadStatus.NEW,
        LeadStatus.IN_PROGRESS,
    )
    event.message.edit_text.assert_awaited_once()


@pytest.mark.asyncio
async def test_admin_status_change_denied_for_non_admin(
    monkeypatch: pytest.MonkeyPatch,
    lead_service: LeadService,
) -> None:
    monkeypatch.setattr(admin, "_is_admin", lambda _user_id: False)
    event = admin_callback("a:s:999:completed")

    await admin.admin_status(event, lead_service)  # type: ignore[arg-type]

    event.answer.assert_awaited_once_with("This command is limited to administrators.")
    event.message.edit_text.assert_not_awaited()
