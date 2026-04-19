import pytest

from bot.config import Settings


def test_settings_requires_bot_token_and_admin_id(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BOT_TOKEN", raising=False)
    monkeypatch.delenv("ADMIN_ID", raising=False)
    with pytest.raises(Exception):
        Settings(_env_file=None)  # type: ignore[call-arg]


def test_settings_from_env(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setenv("BOT_TOKEN", "123:abc")
    monkeypatch.setenv("ADMIN_ID", "42")
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setenv("MEDIA_DIR", str(tmp_path / "media"))
    monkeypatch.setenv("DEFAULT_LOCALE", "en")

    s = Settings(_env_file=None)  # type: ignore[call-arg]
    assert s.admin_id == 42
    assert s.default_locale == "en"
    assert s.bot_token.get_secret_value() == "123:abc"

    s.ensure_dirs()
    assert (tmp_path / "media").is_dir()
