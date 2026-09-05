from datetime import datetime, timezone

import pytest

from app.models.enums import ContactMethod, LeadStatus, ServiceCategory
from app.services.lead_service import DuplicateLeadError, LeadDraft, LeadService
from tests.conftest import TEST_USER_ID


def _draft(**overrides) -> LeadDraft:
    payload = dict(
        full_name="Maya Chen",
        phone="+14155550114",
        service_category=ServiceCategory.WEBSITE_DEVELOPMENT,
        description="Need a marketing site with an enquiry form.",
        preferred_contact_method=ContactMethod.EMAIL,
    )
    payload.update(overrides)
    return LeadDraft(**payload)


@pytest.mark.asyncio
async def test_lead_creation(lead_service: LeadService) -> None:
    lead = await lead_service.create_lead(
        telegram_user_id=TEST_USER_ID,
        username="maya.studio",
        draft=_draft(),
    )
    assert lead.id is not None
    assert lead.public_id.startswith("LF-")
    assert lead.status is LeadStatus.NEW
    assert lead.full_name == "Maya Chen"
    assert lead.telegram_user_id == TEST_USER_ID
    assert lead.created_at.tzinfo is not None
    assert lead.created_at.utcoffset() is not None


@pytest.mark.asyncio
async def test_status_transition(lead_service: LeadService) -> None:
    lead = await lead_service.create_lead(
        telegram_user_id=TEST_USER_ID,
        username=None,
        draft=_draft(),
    )
    updated, previous, changed = await lead_service.change_status(lead.id, LeadStatus.IN_PROGRESS)
    assert previous is LeadStatus.NEW
    assert changed is True
    assert updated.status is LeadStatus.IN_PROGRESS
    same, _, changed_again = await lead_service.change_status(lead.id, LeadStatus.IN_PROGRESS)
    assert changed_again is False
    assert same.status is LeadStatus.IN_PROGRESS


@pytest.mark.asyncio
async def test_customer_request_retrieval(lead_service: LeadService) -> None:
    await lead_service.create_lead(
        telegram_user_id=TEST_USER_ID,
        username="maya",
        draft=_draft(),
    )
    await lead_service.create_lead(
        telegram_user_id=999,
        username="other",
        draft=_draft(phone="+14155550999", description="A different brief for another customer."),
    )
    mine = await lead_service.list_for_user(TEST_USER_ID)
    assert len(mine) == 1
    assert mine[0].telegram_user_id == TEST_USER_ID


@pytest.mark.asyncio
async def test_duplicate_submission(lead_service: LeadService) -> None:
    first = await lead_service.create_lead(
        telegram_user_id=TEST_USER_ID,
        username="maya",
        draft=_draft(),
    )
    with pytest.raises(DuplicateLeadError) as exc:
        await lead_service.create_lead(
            telegram_user_id=TEST_USER_ID,
            username="maya",
            draft=_draft(),
        )
    assert exc.value.lead.public_id == first.public_id


@pytest.mark.asyncio
async def test_note_replace(lead_service: LeadService) -> None:
    lead = await lead_service.create_lead(
        telegram_user_id=TEST_USER_ID,
        username=None,
        draft=_draft(),
    )
    updated = await lead_service.set_note(lead.id, "  Call after 18:00  ")
    assert updated.admin_note == "Call after 18:00"
    cleared = await lead_service.set_note(lead.id, "   ")
    assert cleared.admin_note is None


def test_public_id_uses_utc_date() -> None:
    stamp = datetime.now(timezone.utc).strftime("%y%m%d")
    assert len(stamp) == 6
