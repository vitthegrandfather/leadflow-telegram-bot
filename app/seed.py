from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from app.config import get_settings
from app.database.session import ensure_sqlite_dir, init_db, run_migrations
from app.logging import setup_logging
from app.models.enums import ContactMethod, LeadStatus, ServiceCategory
from app.repositories.lead_repository import LeadRepository

SAMPLES = [
    {
        "telegram_user_id": 900000001,
        "username": "maya.studio",
        "full_name": "Maya Chen",
        "phone": "+14155550114",
        "service_category": ServiceCategory.WEBSITE_DEVELOPMENT,
        "description": (
            "Need a marketing site for a ceramics studio with a simple enquiry form "
            "and a gallery of recent work."
        ),
        "preferred_contact_method": ContactMethod.EMAIL,
        "status": LeadStatus.NEW,
        "admin_note": None,
        "days_ago": 7,
    },
    {
        "telegram_user_id": 900000002,
        "username": "omar.h",
        "full_name": "Omar Haddad",
        "phone": "+971501234567",
        "service_category": ServiceCategory.TELEGRAM_BOT,
        "description": (
            "Booking bot for a two-chair barbershop. Customers pick a slot, staff confirm, "
            "and we send a reminder."
        ),
        "preferred_contact_method": ContactMethod.TELEGRAM,
        "status": LeadStatus.IN_PROGRESS,
        "admin_note": "Waiting on opening hours and public holidays list.",
        "days_ago": 6,
    },
    {
        "telegram_user_id": 900000003,
        "username": "e.volkova",
        "full_name": "Elena Volkova",
        "phone": "+491701112233",
        "service_category": ServiceCategory.API_INTEGRATION,
        "description": (
            "Connect Stripe invoices to our internal Notion tracker so finance stops "
            "copying numbers by hand."
        ),
        "preferred_contact_method": ContactMethod.EMAIL,
        "status": LeadStatus.COMPLETED,
        "admin_note": "Shipped webhook + Notion database mapping on 1 Sep.",
        "days_ago": 5,
    },
    {
        "telegram_user_id": 900000004,
        "username": "jonasberg",
        "full_name": "Jonas Berg",
        "phone": "+46701234567",
        "service_category": ServiceCategory.BUSINESS_AUTOMATION,
        "description": (
            "Weekly CSV of new signups emailed to operations, with a Slack ping when volume spikes."
        ),
        "preferred_contact_method": ContactMethod.PHONE,
        "status": LeadStatus.CANCELLED,
        "admin_note": "Client postponed until Q4. Keep the brief on file.",
        "days_ago": 5,
    },
    {
        "telegram_user_id": 900000005,
        "username": "priya.nair",
        "full_name": "Priya Nair",
        "phone": "+919820011223",
        "service_category": ServiceCategory.WEBSITE_DEVELOPMENT,
        "description": (
            "Rebuild the clinic landing page. Need appointment CTA, doctor bios, "
            "and multilingual EN/HI copy slots."
        ),
        "preferred_contact_method": ContactMethod.WHATSAPP,
        "status": LeadStatus.IN_PROGRESS,
        "admin_note": "Design draft sent. Awaiting logo files.",
        "days_ago": 4,
    },
    {
        "telegram_user_id": 900000006,
        "username": "luca.moretti",
        "full_name": "Luca Moretti",
        "phone": "+393471112244",
        "service_category": ServiceCategory.OTHER,
        "description": (
            "Not sure which service we need. We run a small winery and want tasting-room "
            "reservations without a full website rebuild."
        ),
        "preferred_contact_method": ContactMethod.PHONE,
        "status": LeadStatus.NEW,
        "admin_note": None,
        "days_ago": 3,
    },
    {
        "telegram_user_id": 900000007,
        "username": "hannah.cole",
        "full_name": "Hannah Cole",
        "phone": "+447700900123",
        "service_category": ServiceCategory.TELEGRAM_BOT,
        "description": (
            "Support bot that answers FAQs for an online course and hands off to a human "
            "after two failed replies."
        ),
        "preferred_contact_method": ContactMethod.TELEGRAM,
        "status": LeadStatus.COMPLETED,
        "admin_note": "FAQ set v2 approved. Bot handed over.",
        "days_ago": 2,
    },
    {
        "telegram_user_id": 900000008,
        "username": "wei.zhang",
        "full_name": "Wei Zhang",
        "phone": "+8613800138000",
        "service_category": ServiceCategory.API_INTEGRATION,
        "description": (
            "Sync inventory from our warehouse API into Shopify, including low-stock alerts "
            "to the ops chat."
        ),
        "preferred_contact_method": ContactMethod.EMAIL,
        "status": LeadStatus.NEW,
        "admin_note": None,
        "days_ago": 1,
    },
    {
        "telegram_user_id": 900000009,
        "username": "sofia.alvarez",
        "full_name": "Sofia Alvarez",
        "phone": "+34600111222",
        "service_category": ServiceCategory.BUSINESS_AUTOMATION,
        "description": (
            "Onboarding checklist for new contractors: collect documents, send a welcome pack, "
            "notify legal."
        ),
        "preferred_contact_method": ContactMethod.WHATSAPP,
        "status": LeadStatus.IN_PROGRESS,
        "admin_note": "Need document list from legal before workflow mapping.",
        "days_ago": 0,
    },
]


async def seed() -> None:
    settings = get_settings()
    factory = await init_db(settings)
    async with factory() as session:
        repo = LeadRepository(session)
        existing = await repo.count_all()
        if existing >= 8:
            print(f"Database already has {existing} leads. Seed skipped.")
            return
        now = datetime.now(timezone.utc)
        for index, sample in enumerate(SAMPLES, start=1):
            created = now - timedelta(days=int(sample["days_ago"]))
            await repo.create(
                telegram_user_id=int(sample["telegram_user_id"]),
                username=str(sample["username"]),
                full_name=str(sample["full_name"]),
                phone=str(sample["phone"]),
                service_category=sample["service_category"],  # type: ignore[arg-type]
                description=str(sample["description"]),
                preferred_contact_method=sample["preferred_contact_method"],  # type: ignore[arg-type]
                public_id=f"LF-SEED-{index:04d}",
                status=sample["status"],  # type: ignore[arg-type]
                admin_note=sample["admin_note"],  # type: ignore[arg-type]
                created_at=created,
            )
        await session.commit()
        print(f"Inserted {len(SAMPLES)} fictional sample leads.")


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)
    ensure_sqlite_dir(settings.database_url)
    run_migrations(settings.database_url)
    asyncio.run(seed())


if __name__ == "__main__":
    main()
