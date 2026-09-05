import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ContactMethod, LeadStatus, ServiceCategory
from app.repositories.lead_repository import LeadRepository


@pytest.mark.asyncio
async def test_repository_create_get_counts(session: AsyncSession) -> None:
    repo = LeadRepository(session)
    lead = await repo.create(
        telegram_user_id=42,
        username="demo",
        full_name="Demo User",
        phone="+14155550100",
        service_category=ServiceCategory.TELEGRAM_BOT,
        description="A booking assistant for a small shop.",
        preferred_contact_method=ContactMethod.TELEGRAM,
    )
    fetched = await repo.get_by_id(lead.id)
    assert fetched is not None
    assert fetched.public_id == lead.public_id
    by_public = await repo.get_by_public_id(lead.public_id)
    assert by_public is not None
    assert await repo.count_all() == 1
    assert await repo.count_by_status(LeadStatus.NEW) == 1
    await repo.update_status(lead, LeadStatus.COMPLETED)
    assert await repo.count_by_status(LeadStatus.COMPLETED) == 1
    recent = await repo.list_recent(limit=5)
    assert recent[0].id == lead.id
