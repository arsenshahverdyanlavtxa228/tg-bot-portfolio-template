from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Locale = Literal["ru", "en"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    bot_token: SecretStr = Field(..., description="Telegram bot token from @BotFather")
    admin_id: int = Field(..., description="Telegram user ID of the portfolio owner")

    database_url: str = Field(default="sqlite+aiosqlite:///./data/bot.db")
    media_dir: Path = Field(default=Path("./media"))

    default_locale: Locale = Field(default="ru")
    log_level: str = Field(default="INFO")
    drop_pending_updates: bool = Field(default=False)

    def ensure_dirs(self) -> None:
        self.media_dir.mkdir(parents=True, exist_ok=True)
        if self.database_url.startswith("sqlite"):
            db_path = self.database_url.split("///", 1)[-1]
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)


def load_settings() -> Settings:
    settings = Settings()
    settings.ensure_dirs()
    return settings
