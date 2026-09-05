from __future__ import annotations

import secrets
from datetime import datetime, timezone

PUBLIC_ID_PATTERN = r"^LF-\d{6}-[0-9A-F]{4}$"


def generate_public_id(when: datetime | None = None) -> str:
    stamp = (when or datetime.now(timezone.utc)).strftime("%y%m%d")
    suffix = secrets.token_hex(2).upper()
    return f"LF-{stamp}-{suffix}"
