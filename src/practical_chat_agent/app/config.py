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
    chat_context_recent_events: int = Field(
        default=8,
        validation_alias=AliasChoices("CHAT_CONTEXT_RECENT_EVENTS"),
    )
    chat_context_memory_hits: int = Field(
        default=8,
        validation_alias=AliasChoices("CHAT_CONTEXT_MEMORY_HITS"),
    )
    chat_suggestion_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("CHAT_SUGGESTION_ENABLED"),
    )
    chat_suggestion_model: str | None = Field(
        default="deepseek-chat",
        validation_alias=AliasChoices("CHAT_SUGGESTION_MODEL", "OPENAI_MODEL"),
    )
    chat_suggestion_timeout_seconds: float = Field(
        default=20.0,
        validation_alias=AliasChoices("CHAT_SUGGESTION_TIMEOUT_SECONDS"),
    )
    chat_memory_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("CHAT_MEMORY_ENABLED"),
    )
    chat_memory_model: str | None = Field(
        default="deepseek-chat",
        validation_alias=AliasChoices("CHAT_MEMORY_MODEL", "OPENAI_MODEL", "CHAT_SUGGESTION_MODEL"),
    )
    chat_memory_timeout_seconds: float = Field(
        default=20.0,
        validation_alias=AliasChoices("CHAT_MEMORY_TIMEOUT_SECONDS"),
    )
    chat_profile_facets_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("CHAT_PROFILE_FACETS_ENABLED"),
    )
    chat_profile_facets_model: str | None = Field(
        default="deepseek-chat",
        validation_alias=AliasChoices(
            "CHAT_PROFILE_FACETS_MODEL",
            "CHAT_MEMORY_MODEL",
            "OPENAI_MODEL",
            "CHAT_SUGGESTION_MODEL",
        ),
    )
    chat_profile_facets_timeout_seconds: float = Field(
        default=20.0,
        validation_alias=AliasChoices("CHAT_PROFILE_FACETS_TIMEOUT_SECONDS"),
    )
    telegram_bot_token: str | None = Field(
        default=None,
        validation_alias=AliasChoices("TELEGRAM_BOT_TOKEN"),
    )
    telegram_delivery_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("TELEGRAM_DELIVERY_ENABLED"),
    )
    telegram_delivery_timeout_seconds: float = Field(
        default=20.0,
        validation_alias=AliasChoices("TELEGRAM_DELIVERY_TIMEOUT_SECONDS"),
    )
    outbound_quiet_hours_start: str | None = Field(
        default="23:00",
        validation_alias=AliasChoices("OUTBOUND_QUIET_HOURS_START"),
    )
    outbound_quiet_hours_end: str | None = Field(
        default="08:00",
        validation_alias=AliasChoices("OUTBOUND_QUIET_HOURS_END"),
    )
    outbound_policy_timezone: str = Field(
        default="Asia/Shanghai",
        validation_alias=AliasChoices("OUTBOUND_POLICY_TIMEZONE"),
    )
    outbound_frequency_limit_count: int = Field(
        default=3,
        validation_alias=AliasChoices("OUTBOUND_FREQUENCY_LIMIT_COUNT"),
    )
    outbound_frequency_limit_window_seconds: int = Field(
        default=600,
        validation_alias=AliasChoices("OUTBOUND_FREQUENCY_LIMIT_WINDOW_SECONDS"),
    )
    outbound_group_chat_draft_only: bool = Field(
        default=True,
        validation_alias=AliasChoices("OUTBOUND_GROUP_CHAT_DRAFT_ONLY"),
    )
    meeting_assistant_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("MEETING_ASSISTANT_ENABLED"),
    )
    meeting_assistant_model: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MEETING_ASSISTANT_MODEL"),
    )
    meeting_assistant_timeout_seconds: float = Field(
        default=20.0,
        validation_alias=AliasChoices("MEETING_ASSISTANT_TIMEOUT_SECONDS"),
    )
    meeting_minutes_rewriter_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("MEETING_MINUTES_REWRITER_ENABLED"),
    )
    meeting_minutes_model: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MEETING_MINUTES_MODEL", "MEETING_ASSISTANT_MODEL"),
    )
    meeting_minutes_timeout_seconds: float = Field(
        default=30.0,
        validation_alias=AliasChoices("MEETING_MINUTES_TIMEOUT_SECONDS"),
    )
    meeting_minutes_context_segments: int = Field(
        default=24,
        validation_alias=AliasChoices("MEETING_MINUTES_CONTEXT_SEGMENTS"),
    )
    meeting_assistant_context_segments: int = Field(
        default=8,
        validation_alias=AliasChoices("MEETING_ASSISTANT_CONTEXT_SEGMENTS"),
    )
    meeting_live_window_alpha: float = Field(
        default=0.92,
        validation_alias=AliasChoices("MEETING_LIVE_WINDOW_ALPHA"),
    )
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
    meeting_transcribe_empty_retry_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices("MEETING_TRANSCRIBE_EMPTY_RETRY_ENABLED"),
    )
    meeting_transcribe_empty_retry_prompt: str = Field(
        default="这是实时会议中文语音转写，请尽量识别口语、短句和不完整句子；如果有犹豫词也尽量保留。",
        validation_alias=AliasChoices("MEETING_TRANSCRIBE_EMPTY_RETRY_PROMPT"),
    )
    meeting_capture_debug_dir: str = Field(
        default=".cache/meeting_captures",
        validation_alias=AliasChoices("MEETING_CAPTURE_DEBUG_DIR"),
    )
    meeting_audio_silence_threshold: float = Field(
        default=0.0015,
        validation_alias=AliasChoices("MEETING_AUDIO_SILENCE_THRESHOLD"),
    )
    meeting_microphone_boost_gain: float = Field(
        default=1.8,
        validation_alias=AliasChoices("MEETING_MICROPHONE_BOOST_GAIN"),
    )
    meeting_microphone_peak_target: float = Field(
        default=0.92,
        validation_alias=AliasChoices("MEETING_MICROPHONE_PEAK_TARGET"),
    )
    meeting_microphone_silence_floor: float = Field(
        default=0.0030,
        validation_alias=AliasChoices("MEETING_MICROPHONE_SILENCE_FLOOR"),
    )
    meeting_microphone_highpass_cutoff_hz: float = Field(
        default=80.0,
        validation_alias=AliasChoices("MEETING_MICROPHONE_HIGHPASS_CUTOFF_HZ"),
    )
    meeting_microphone_trim_padding_seconds: float = Field(
        default=0.12,
        validation_alias=AliasChoices("MEETING_MICROPHONE_TRIM_PADDING_SECONDS"),
    )
    meeting_microphone_compressor_threshold: float = Field(
        default=0.45,
        validation_alias=AliasChoices("MEETING_MICROPHONE_COMPRESSOR_THRESHOLD"),
    )
    meeting_microphone_compressor_ratio: float = Field(
        default=3.0,
        validation_alias=AliasChoices("MEETING_MICROPHONE_COMPRESSOR_RATIO"),
    )
    meeting_microphone_limiter_ceiling: float = Field(
        default=0.96,
        validation_alias=AliasChoices("MEETING_MICROPHONE_LIMITER_CEILING"),
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
    meeting_microphone_preferred_device_name: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MEETING_MICROPHONE_PREFERRED_DEVICE_NAME"),
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
