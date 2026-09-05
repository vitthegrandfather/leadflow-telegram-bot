from __future__ import annotations

import html
from datetime import datetime

from app.models.lead import Lead


def html_text(value: str | None) -> str:
    return html.escape(value or "", quote=True)


def format_utc(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M UTC")


def format_lead_card(lead: Lead, *, include_admin: bool = False) -> str:
    username = f"@{html_text(lead.username)}" if lead.username else "—"
    lines = [
        f"<b>{html_text(lead.public_id)}</b>",
        f"Status: {html_text(lead.status.label)}",
        f"Name: {html_text(lead.full_name)}",
        f"Phone: {html_text(lead.phone)}",
        f"Telegram: {username} (<code>{lead.telegram_user_id}</code>)",
        f"Service: {html_text(lead.service_category.label)}",
        f"Contact: {html_text(lead.preferred_contact_method.label)}",
        f"Created: {format_utc(lead.created_at)}",
        "",
        html_text(lead.description),
    ]
    if include_admin:
        note = html_text(lead.admin_note) if lead.admin_note else "—"
        lines.extend(["", f"Internal note: {note}"])
    return "\n".join(lines)


def format_lead_brief(lead: Lead) -> str:
    created = lead.created_at.strftime("%Y-%m-%d")
    return (
        f"{html_text(lead.public_id)} · {html_text(lead.service_category.label)} · "
        f"{html_text(lead.status.label)} · {created}"
    )
