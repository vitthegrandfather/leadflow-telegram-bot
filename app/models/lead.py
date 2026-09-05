from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import BigInteger, Enum, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.types import UTCDateTime
from app.models.enums import ContactMethod, LeadStatus, ServiceCategory


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _enum_values(enum_cls: type[PyEnum]) -> list[str]:
    return [item.value for item in enum_cls]


class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = (
        Index("ix_leads_telegram_user_id", "telegram_user_id"),
        Index("ix_leads_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    public_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    telegram_user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str | None] = mapped_column(String(64))
    full_name: Mapped[str] = mapped_column(String(80), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    service_category: Mapped[ServiceCategory] = mapped_column(
        Enum(
            ServiceCategory,
            native_enum=False,
            length=32,
            values_callable=_enum_values,
        ),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    preferred_contact_method: Mapped[ContactMethod] = mapped_column(
        Enum(
            ContactMethod,
            native_enum=False,
            length=32,
            values_callable=_enum_values,
        ),
        nullable=False,
    )
    status: Mapped[LeadStatus] = mapped_column(
        Enum(
            LeadStatus,
            native_enum=False,
            length=32,
            values_callable=_enum_values,
        ),
        default=LeadStatus.NEW,
        nullable=False,
    )
    admin_note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )
