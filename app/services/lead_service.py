from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.models.enums import ContactMethod, LeadStatus, ServiceCategory
from app.models.lead import Lead
from app.repositories.lead_repository import LeadRepository


class DuplicateLeadError(Exception):
    def __init__(self, lead: Lead) -> None:
        super().__init__(f"A matching request already exists: {lead.public_id}")
        self.lead = lead


class LeadNotFoundError(LookupError):
    pass


@dataclass(frozen=True)
class LeadDraft:
    full_name: str
    phone: str
    service_category: ServiceCategory
    description: str
    preferred_contact_method: ContactMethod


class LeadService:
    def __init__(self, session: AsyncSession, settings: Settings | None = None) -> None:
        self.session = session
        self.settings = settings or get_settings()
        self.repo = LeadRepository(session)

    async def create_lead(
        self,
        *,
        telegram_user_id: int,
        username: str | None,
        draft: LeadDraft,
    ) -> Lead:
        duplicate = await self.repo.find_recent_duplicate(
            telegram_user_id=telegram_user_id,
            phone=draft.phone,
            service_category=draft.service_category,
            description=draft.description,
            window_seconds=self.settings.duplicate_window_seconds,
        )
        if duplicate is not None:
            raise DuplicateLeadError(duplicate)
        return await self.repo.create(
            telegram_user_id=telegram_user_id,
            username=username,
            full_name=draft.full_name,
            phone=draft.phone,
            service_category=draft.service_category,
            description=draft.description,
            preferred_contact_method=draft.preferred_contact_method,
        )

    async def list_for_user(self, telegram_user_id: int) -> list[Lead]:
        return await self.repo.list_by_user(telegram_user_id)

    async def get(self, lead_id: int) -> Lead:
        lead = await self.repo.get_by_id(lead_id)
        if lead is None:
            raise LeadNotFoundError(f"Lead {lead_id} was not found.")
        return lead

    async def change_status(
        self, lead_id: int, status: LeadStatus
    ) -> tuple[Lead, LeadStatus, bool]:
        lead = await self.get(lead_id)
        previous = lead.status
        if previous == status:
            return lead, previous, False
        updated = await self.repo.update_status(lead, status)
        return updated, previous, True

    async def set_note(self, lead_id: int, note: str) -> Lead:
        lead = await self.get(lead_id)
        cleaned = note.strip() or None
        return await self.repo.update_note(lead, cleaned)

    async def stats(self) -> dict[str, int]:
        return {
            "total": await self.repo.count_all(),
            "new": await self.repo.count_by_status(LeadStatus.NEW),
            "in_progress": await self.repo.count_by_status(LeadStatus.IN_PROGRESS),
            "completed": await self.repo.count_by_status(LeadStatus.COMPLETED),
            "cancelled": await self.repo.count_by_status(LeadStatus.CANCELLED),
        }

    async def recent(self, *, page: int = 0, per_page: int = 5) -> tuple[list[Lead], int]:
        page = max(page, 0)
        total = await self.repo.count_all()
        leads = await self.repo.list_recent(offset=page * per_page, limit=per_page)
        return leads, total

    async def export_rows(self) -> list[Lead]:
        return await self.repo.list_all()
