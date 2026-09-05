from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings
from app.database.base import Base
from app.models import lead as _lead_model  # noqa: F401
from app.services.lead_service import LeadService

TEST_ADMIN_ID = 111111
TEST_USER_ID = 222222


@pytest.fixture
def settings() -> Settings:
    return Settings(
        bot_token="",
        admin_ids=str(TEST_ADMIN_ID),
        database_url="sqlite+aiosqlite:///:memory:",
        log_level="WARNING",
        duplicate_window_seconds=600,
    )


@pytest.fixture
async def session(settings: Settings) -> AsyncSession:
    engine = create_async_engine(settings.database_url, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as db_session:
        yield db_session
    await engine.dispose()


@pytest.fixture
def lead_service(session: AsyncSession, settings: Settings) -> LeadService:
    return LeadService(session, settings=settings)
