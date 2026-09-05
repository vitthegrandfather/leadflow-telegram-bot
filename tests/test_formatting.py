from datetime import datetime, timezone
from html import escape
from types import SimpleNamespace

from app.models.enums import ContactMethod, LeadStatus, ServiceCategory
from app.utils.formatting import format_lead_card, html_text


def test_html_escape() -> None:
    raw = "<script>alert(1)</script>"
    escaped = html_text(raw)
    assert escaped == escape(raw, quote=True)
    assert "<script>" not in escaped


def test_format_lead_card_escapes_user_fields() -> None:
    lead = SimpleNamespace(
        public_id="LF-260905-ABCD",
        status=LeadStatus.NEW,
        full_name="<b>Maya</b>",
        phone="+14155550114",
        username="maya&co",
        telegram_user_id=1,
        service_category=ServiceCategory.OTHER,
        preferred_contact_method=ContactMethod.PHONE,
        created_at=datetime(2026, 9, 5, tzinfo=timezone.utc),
        description="Use <html> tags",
        admin_note="Secret <note>",
    )
    card = format_lead_card(lead, include_admin=True)  # type: ignore[arg-type]
    assert "<b>Maya</b>" not in card
    assert escape("<b>Maya</b>", quote=True) in card
    assert escape("maya&co", quote=True) in card
    assert escape("<html>", quote=True) in card
    assert escape("<note>", quote=True) in card
