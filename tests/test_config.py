import pytest

from app.config import Settings
from app.main import _require_runtime_settings


def test_settings_import_without_token() -> None:
    settings = Settings()
    assert settings.bot_token == ""
    assert settings.admin_id_set == frozenset()
    assert "sqlite" in settings.database_url


def test_runtime_requires_admin_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "123456:abcdefghijklmnopqrstuvwxyzABCDEFG")
    monkeypatch.setenv("ADMIN_IDS", "")
    from app.config import get_settings

    get_settings.cache_clear()
    try:
        with pytest.raises(SystemExit, match="at least one Telegram user ID"):
            _require_runtime_settings()
    finally:
        get_settings.cache_clear()
