from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    APP_NAME: str = Field(...)
    APP_VERSION: str = Field(...)

    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/jarvis.log"

    DEFAULT_LLM: str = "ollama"
    OLLAMA_URL: str = "http://localhost:11434"

    WAKE_WORD: str = "Jarvis"
    SLEEP_TIMEOUT: int = 300

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()