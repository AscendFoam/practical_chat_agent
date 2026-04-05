from __future__ import annotations

import re
from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: str = Field(default="dev", validation_alias=AliasChoices("APP_ENV"))
    app_name: str = Field(default="practical-chat-agent", validation_alias=AliasChoices("APP_NAME"))

    mysql_host: str = Field(default="127.0.0.1", validation_alias=AliasChoices("MYSQL_HOST"))
    mysql_port: int = Field(default=3306, validation_alias=AliasChoices("MYSQL_PORT"))
    mysql_user: str = Field(default="root", validation_alias=AliasChoices("MYSQL_USER"))
    mysql_password: str = Field(default="", validation_alias=AliasChoices("MYSQL_PASSWORD"))
    mysql_database: str = Field(
        default="practical_chat_agent",
        validation_alias=AliasChoices("MYSQL_DATABASE"),
    )
    mysql_echo: bool = Field(default=False, validation_alias=AliasChoices("MYSQL_ECHO"))

    openai_api_key: str | None = Field(default=None, validation_alias=AliasChoices("OPENAI_API_KEY"))
    openai_base_url: str | None = Field(default=None, validation_alias=AliasChoices("OPENAI_BASE_URL"))
    glm_ocr_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("GLM_OCR_API_KEY", "ZHIPUAI_API_KEY", "ZAI_API_KEY"),
    )
    glm_ocr_model: str = Field(default="glm-ocr", validation_alias=AliasChoices("GLM_OCR_MODEL"))
    desktop_ocr_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("DESKTOP_OCR_ENABLED"),
    )
    desktop_ocr_timeout_seconds: float = Field(
        default=30.0,
        validation_alias=AliasChoices("DESKTOP_OCR_TIMEOUT_SECONDS"),
    )
    desktop_capture_debug_dir: str = Field(
        default=".cache/desktop_captures",
        validation_alias=AliasChoices("DESKTOP_CAPTURE_DEBUG_DIR"),
    )
    meeting_transcribe_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "MEETING_TRANSCRIBE_API_KEY",
            "GLM_OCR_API_KEY",
            "ZHIPUAI_API_KEY",
            "ZAI_API_KEY",
        ),
    )
    meeting_transcribe_model: str | None = Field(
        default="glm-asr-2512",
        validation_alias=AliasChoices("MEETING_TRANSCRIBE_MODEL"),
    )
    meeting_transcribe_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("MEETING_TRANSCRIBE_ENABLED"),
    )
    meeting_transcribe_timeout_seconds: float = Field(
        default=30.0,
        validation_alias=AliasChoices("MEETING_TRANSCRIBE_TIMEOUT_SECONDS"),
    )
    meeting_capture_debug_dir: str = Field(
        default=".cache/meeting_captures",
        validation_alias=AliasChoices("MEETING_CAPTURE_DEBUG_DIR"),
    )
    meeting_loopback_sample_rate: int = Field(
        default=16000,
        validation_alias=AliasChoices("MEETING_LOOPBACK_SAMPLE_RATE"),
    )
    meeting_loopback_default_capture_seconds: float = Field(
        default=6.0,
        validation_alias=AliasChoices("MEETING_LOOPBACK_DEFAULT_CAPTURE_SECONDS"),
    )
    meeting_loopback_default_chunk_seconds: float = Field(
        default=5.0,
        validation_alias=AliasChoices("MEETING_LOOPBACK_DEFAULT_CHUNK_SECONDS"),
    )
    meeting_loopback_preferred_speaker_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MEETING_LOOPBACK_PREFERRED_SPEAKER_NAME"),
    )

    @property
    def sqlalchemy_server_uri(self) -> str:
        return (
            f"mysql+pymysql://{quote_plus(self.mysql_user)}:{quote_plus(self.mysql_password)}"
            f"@{self.mysql_host}:{self.mysql_port}/mysql?charset=utf8mb4"
        )

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            f"mysql+pymysql://{quote_plus(self.mysql_user)}:{quote_plus(self.mysql_password)}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
        )

    def validated_database_name(self) -> str:
        if not re.fullmatch(r"[A-Za-z0-9_]+", self.mysql_database):
            raise ValueError(
                "MYSQL_DATABASE must contain only letters, numbers, and underscores.",
            )
        return self.mysql_database


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
