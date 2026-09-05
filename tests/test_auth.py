import pytest

from app.services.auth_service import UnauthorizedAdminError, is_admin, require_admin
from tests.conftest import TEST_ADMIN_ID, TEST_USER_ID


def test_is_admin_true() -> None:
    assert is_admin(TEST_ADMIN_ID, [TEST_ADMIN_ID])


def test_unauthorized_admin_access() -> None:
    assert is_admin(TEST_USER_ID, [TEST_ADMIN_ID]) is False
    assert is_admin(None, [TEST_ADMIN_ID]) is False
    with pytest.raises(UnauthorizedAdminError):
        require_admin(TEST_USER_ID, [TEST_ADMIN_ID])
