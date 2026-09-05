from __future__ import annotations

import csv
import io
from collections.abc import Iterable

from app.models.lead import Lead

CSV_HEADERS = [
    "public_id",
    "created_at",
    "status",
    "full_name",
    "phone",
    "username",
    "telegram_user_id",
    "category",
    "contact_method",
    "description",
    "admin_note",
]


def leads_to_csv(leads: Iterable[Lead]) -> bytes:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(CSV_HEADERS)
    for lead in leads:
        writer.writerow(
            [
                lead.public_id,
                lead.created_at.isoformat(),
                lead.status.label,
                lead.full_name,
                lead.phone,
                lead.username or "",
                lead.telegram_user_id,
                lead.service_category.label,
                lead.preferred_contact_method.label,
                lead.description,
                lead.admin_note or "",
            ]
        )
    return ("\ufeff" + buffer.getvalue()).encode("utf-8")
