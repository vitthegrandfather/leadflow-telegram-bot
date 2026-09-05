from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers import customer
from app.models.enums import LeadStatus
from app.services.lead_service import LeadService
from app.states.lead_form import LeadForm
from tests.conftest import TEST_USER_ID


class FakeState:
    def __init__(self) -> None:
        self.data: dict[str, object] = {}
        self.state = None

    async def clear(self) -> None:
        self.data.clear()
        self.state = None

    async def set_state(self, state) -> None:
        self.state = state

    async def update_data(self, **values):
        self.data.update(values)
        return dict(self.data)

    async def get_data(self):
        return dict(self.data)


def message(text: str) -> AsyncMock:
    item = AsyncMock()
    item.text = text
    item.answer = AsyncMock()
    return item


def callback(data: str) -> AsyncMock:
    item = AsyncMock()
    item.data = data
    item.from_user.id = TEST_USER_ID
    item.from_user.username = "demo_user"
    item.answer = AsyncMock()
    item.message.edit_text = AsyncMock()
    return item


@pytest.mark.asyncio
async def test_complete_customer_intake_flow(
    monkeypatch: pytest.MonkeyPatch,
    lead_service: LeadService,
    session: AsyncSession,
) -> None:
    state = FakeState()

    await customer.capture_name(message("Maya Chen"), state)  # type: ignore[arg-type]
    assert state.state == LeadForm.phone

    await customer.capture_phone(message("+1 (415) 555-0114"), state)  # type: ignore[arg-type]
    assert state.state == LeadForm.category

    category = callback("c:cat:telegram_bot")
    await customer.capture_category(category, state)  # type: ignore[arg-type]
    assert state.state == LeadForm.description

    await customer.capture_description(
        message("Build a Telegram assistant for incoming service requests."),
        state,  # type: ignore[arg-type]
    )
    assert state.state == LeadForm.contact_method

    contact = callback("c:cm:telegram")
    await customer.capture_contact(contact, state)  # type: ignore[arg-type]
    assert state.state == LeadForm.confirm

    notify_admins = AsyncMock()
    monkeypatch.setattr(customer, "notify_admins", notify_admins)
    confirmation = callback("c:ok")
    await customer.confirm_lead(
        confirmation,
        state,  # type: ignore[arg-type]
        lead_service,
        session,
    )

    leads = await lead_service.list_for_user(TEST_USER_ID)
    assert len(leads) == 1
    assert leads[0].status is LeadStatus.NEW
    assert leads[0].phone == "+14155550114"
    assert state.state is None
    assert state.data == {}
    notify_admins.assert_awaited_once()
    confirmation.message.edit_text.assert_awaited_once()
