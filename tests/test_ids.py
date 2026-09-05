import re
from datetime import datetime, timezone

from app.utils.ids import PUBLIC_ID_PATTERN, generate_public_id


def test_public_id_format() -> None:
    public_id = generate_public_id(datetime(2026, 9, 5, tzinfo=timezone.utc))
    assert public_id.startswith("LF-260905-")
    assert re.match(PUBLIC_ID_PATTERN, public_id)
