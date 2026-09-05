from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    bot_token: str = ""
    admin_ids: str = ""
    database_url: str = "sqlite+aiosqlite:///./data/leadflow.db"
    log_level: str = "INFO"
    duplicate_window_seconds: int = Field(default=600, ge=0)

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.upper()

    @property
    def admin_id_set(self) -> frozenset[int]:
        ids: list[int] = []
        for chunk in self.admin_ids.split(","):
            item = chunk.strip()
            if not item:
                continue
            ids.append(int(item))
        return frozenset(ids)


@lru_cache
def get_settings() -> Settings:
    return Settings()
