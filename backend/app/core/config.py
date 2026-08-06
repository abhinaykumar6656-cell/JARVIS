"""
=========================================================
JARVIS Configuration Management
=========================================================

Loads and validates all application settings from
environment variables.

Supports multiple environments:
- Development
- Testing
- Production

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


# ==========================================================
# Project Root Directory
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]


# ==========================================================
# Settings
# ==========================================================

class Settings(BaseSettings):
    """
    Global application configuration.
    """

    # ======================================================
    # Application
    # ======================================================

    APP_NAME: str = Field(default="JARVIS")

    APP_VERSION: str = Field(default="1.0.0")

    APP_ENV: str = Field(default="development")

    DEBUG: bool = Field(default=True)

    API_PREFIX: str = Field(default="/api/v1")


    # ======================================================
    # Server
    # ======================================================

    HOST: str = Field(default="127.0.0.1")

    PORT: int = Field(default=8000)


    # ======================================================
    # Security
    # ======================================================

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
    )


    # ======================================================
    # Database
    # ======================================================

    DATABASE_URL: str


    # ======================================================
    # Logging
    # ======================================================

    LOG_LEVEL: str = Field(default="INFO")

    LOG_FILE: str = Field(
        default="logs/jarvis.log",
    )


    # ======================================================
    # AI
    # ======================================================

    DEFAULT_LLM: str = Field(
        default="ollama",
    )

    OLLAMA_URL: str = Field(
        default="http://127.0.0.1:11434",
    )

    OLLAMA_MODEL: str = Field(
        default="llama3.2",
    )


    # ======================================================
    # Voice
    # ======================================================

    WAKE_WORD: str = Field(
        default="Jarvis",
    )

    SLEEP_TIMEOUT: int = Field(
        default=300,
    )


    # ======================================================
    # Configuration
    # ======================================================

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# ==========================================================
# Cached Settings
# ==========================================================

@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.
    """

    return Settings()


# ==========================================================
# Global Settings Instance
# ==========================================================

settings = get_settings()