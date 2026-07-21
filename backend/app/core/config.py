"""
=========================================================
JARVIS Configuration Management
=========================================================

This module loads and validates all application settings
from the .env file.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# -------------------------------------------------------
# Project Root (backend/)
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Global application settings.
    """

    # --------------------------------------------------
    # APPLICATION
    # --------------------------------------------------

    APP_NAME: str = Field(...)
    APP_VERSION: str = Field(...)

    DEBUG: bool = Field(default=False)
    API_PREFIX: str = Field(default="/api/v1")

    # --------------------------------------------------
    # SERVER
    # --------------------------------------------------

    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)

    # --------------------------------------------------
    # SECURITY
    # --------------------------------------------------

    SECRET_KEY: str = Field(...)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    # --------------------------------------------------
    # DATABASE
    # --------------------------------------------------

    DATABASE_URL: str = Field(...)

    # --------------------------------------------------
    # LOGGING
    # --------------------------------------------------

    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="logs/jarvis.log")

    # --------------------------------------------------
    # AI
    # --------------------------------------------------

    DEFAULT_LLM: str = Field(default="ollama")
    OLLAMA_URL: str = Field(default="http://localhost:11434")

    # --------------------------------------------------
    # VOICE
    # --------------------------------------------------

    WAKE_WORD: str = Field(default="Jarvis")
    SLEEP_TIMEOUT: int = Field(default=300)

    # --------------------------------------------------
    # Pydantic Configuration
    # --------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns the application settings.
    The settings are cached so the .env file is read only once.
    """
    return Settings()


# Global settings object
settings = get_settings()

SECRET_KEY: str
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60