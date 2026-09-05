from datetime import datetime, timezone
from types import SimpleNamespace

from app.models.enums import ContactMethod, LeadStatus, ServiceCategory
from app.services.export_service import CSV_HEADERS, leads_to_csv


def test_csv_export_headers_and_rows() -> None:
    lead = SimpleNamespace(
        public_id="LF-260905-ABCD",
        created_at=datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc),
        status=LeadStatus.NEW,
        full_name='Maya "Studio" Chen',
        phone="+14155550114",
        username="maya.studio",
        telegram_user_id=900000001,
        service_category=ServiceCategory.WEBSITE_DEVELOPMENT,
        preferred_contact_method=ContactMethod.EMAIL,
        description="Need a site, with commas, please.",
        admin_note=None,
    )
    payload = leads_to_csv([lead])  # type: ignore[list-item]
    text = payload.decode("utf-8-sig")
    first_line = text.splitlines()[0]
    assert first_line.split(",") == CSV_HEADERS
    assert "LF-260905-ABCD" in text
    assert "Website development" in text
    assert '"Maya ""Studio"" Chen"' in text
    assert '"Need a site, with commas, please."' in text
