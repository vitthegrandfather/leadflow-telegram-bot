from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import Settings, get_settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def ensure_sqlite_dir(url: str) -> None:
    if "sqlite" not in url:
        return
    prefix = "///"
    if prefix not in url:
        return
    path = url.split(prefix, 1)[1]
    if path in {":memory:", ""}:
        return
    Path(path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


def create_engine(url: str) -> AsyncEngine:
    return create_async_engine(url, echo=False, future=True)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    if _session_factory is None:
        raise RuntimeError("Database is not initialised. Call init_db() first.")
    return _session_factory


def run_migrations(database_url: str | None = None) -> None:
    from alembic.config import Config

    from alembic import command

    cfg = Config("alembic.ini")
    if database_url:
        cfg.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(cfg, "head")


async def init_db(settings: Settings | None = None) -> async_sessionmaker[AsyncSession]:
    global _engine, _session_factory
    settings = settings or get_settings()
    ensure_sqlite_dir(settings.database_url)
    run_migrations(settings.database_url)
    _engine = create_engine(settings.database_url)
    _session_factory = create_session_factory(_engine)
    return _session_factory


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
