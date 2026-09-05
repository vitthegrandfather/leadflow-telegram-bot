from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import LeadStatus, ServiceCategory
from app.models.lead import Lead
from app.utils.ids import generate_public_id


class LeadRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        telegram_user_id: int,
        username: str | None,
        full_name: str,
        phone: str,
        service_category: ServiceCategory,
        description: str,
        preferred_contact_method,
        public_id: str | None = None,
        status: LeadStatus = LeadStatus.NEW,
        admin_note: str | None = None,
        created_at: datetime | None = None,
    ) -> Lead:
        now = created_at or datetime.now(timezone.utc)
        lead = Lead(
            public_id=public_id or await self.allocate_public_id(),
            telegram_user_id=telegram_user_id,
            username=username,
            full_name=full_name,
            phone=phone,
            service_category=service_category,
            description=description,
            preferred_contact_method=preferred_contact_method,
            status=status,
            admin_note=admin_note,
            created_at=now,
            updated_at=now,
        )
        self.session.add(lead)
        await self.session.flush()
        await self.session.refresh(lead)
        return lead

    async def allocate_public_id(self) -> str:
        for _ in range(8):
            candidate = generate_public_id()
            if await self.get_by_public_id(candidate) is None:
                return candidate
        raise RuntimeError("Could not allocate a unique lead number.")

    async def get_by_id(self, lead_id: int) -> Lead | None:
        return await self.session.get(Lead, lead_id)

    async def get_by_public_id(self, public_id: str) -> Lead | None:
        result = await self.session.execute(select(Lead).where(Lead.public_id == public_id))
        return result.scalar_one_or_none()

    async def list_by_user(self, telegram_user_id: int) -> list[Lead]:
        stmt: Select[tuple[Lead]] = (
            select(Lead)
            .where(Lead.telegram_user_id == telegram_user_id)
            .order_by(Lead.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_recent(self, *, offset: int = 0, limit: int = 5) -> list[Lead]:
        stmt = select(Lead).order_by(Lead.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_all(self) -> list[Lead]:
        stmt = select(Lead).order_by(Lead.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count_all(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(Lead))
        return int(result.scalar_one())

    async def count_by_status(self, status: LeadStatus) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(Lead).where(Lead.status == status)
        )
        return int(result.scalar_one())

    async def find_recent_duplicate(
        self,
        *,
        telegram_user_id: int,
        phone: str,
        service_category: ServiceCategory,
        description: str,
        window_seconds: int,
    ) -> Lead | None:
        cutoff = datetime.now(timezone.utc) - timedelta(seconds=window_seconds)
        stmt = (
            select(Lead)
            .where(
                Lead.telegram_user_id == telegram_user_id,
                Lead.phone == phone,
                Lead.service_category == service_category,
                Lead.description == description,
                Lead.created_at >= cutoff,
            )
            .order_by(Lead.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_status(self, lead: Lead, status: LeadStatus) -> Lead:
        lead.status = status
        lead.updated_at = datetime.now(timezone.utc)
        await self.session.flush()
        await self.session.refresh(lead)
        return lead

    async def update_note(self, lead: Lead, note: str | None) -> Lead:
        lead.admin_note = note
        lead.updated_at = datetime.now(timezone.utc)
        await self.session.flush()
        await self.session.refresh(lead)
        return lead
