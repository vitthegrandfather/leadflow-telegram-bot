from __future__ import annotations

from collections.abc import Iterable

from app.config import Settings, get_settings


class UnauthorizedAdminError(PermissionError):
    pass


def is_admin(user_id: int | None, admin_ids: Iterable[int] | None = None) -> bool:
    if user_id is None:
        return False
    allowed = frozenset(admin_ids) if admin_ids is not None else get_settings().admin_id_set
    return user_id in allowed


def require_admin(
    user_id: int | None,
    admin_ids: Iterable[int] | None = None,
    *,
    settings: Settings | None = None,
) -> int:
    allowed = admin_ids
    if allowed is None and settings is not None:
        allowed = settings.admin_id_set
    if not is_admin(user_id, allowed):
        raise UnauthorizedAdminError("This command is limited to administrators.")
    assert user_id is not None
    return user_id
