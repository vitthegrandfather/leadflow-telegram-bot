"""create leads table

Revision ID: 0001_create_leads
Revises:
Create Date: 2026-09-05
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_create_leads"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "leads",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("public_id", sa.String(length=20), nullable=False),
        sa.Column("telegram_user_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("full_name", sa.String(length=80), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("service_category", sa.String(length=32), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("preferred_contact_method", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("admin_note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("public_id"),
    )
    op.create_index("ix_leads_telegram_user_id", "leads", ["telegram_user_id"])
    op.create_index("ix_leads_status", "leads", ["status"])


def downgrade() -> None:
    op.drop_index("ix_leads_status", table_name="leads")
    op.drop_index("ix_leads_telegram_user_id", table_name="leads")
    op.drop_table("leads")
