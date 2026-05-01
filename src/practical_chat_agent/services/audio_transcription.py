from __future__ import annotations

from pathlib import Path
from typing import Any


class ZhipuAudioTranscriptionService:
    """Thin wrapper around Zhipu audio transcription for file-based chunk testing."""

    backend_name = "zhipu_audio_transcription"

    def __init__(
        self,
        *,
        api_key: str | None,
        model: str | None,
        timeout_seconds: float = 30.0,
        enabled: bool = False,
        empty_retry_enabled: bool = True,
        empty_retry_prompt: str | None = None,
    ) -> None:
        self.api_key = (api_key or "").strip() or None
        self.model = (model or "").strip() or None
        self.timeout_seconds = timeout_seconds
        self.enabled = enabled
        self.empty_retry_enabled = empty_retry_enabled
        self.empty_retry_prompt = (empty_retry_prompt or "").strip() or None

    def availability_reason(self) -> str | None:
        if not self.enabled:
            return "meeting transcription is disabled by configuration"
        if not self.api_key:
            return "meeting transcription API key is not configured"
        if not self.model:
            return "MEETING_TRANSCRIBE_MODEL is not configured"
        return None

    def transcribe_audio_file(
        self,
        *,
        audio_path: Path,
        user_id: str | None = None,
        prompt: str | None = None,
        hotwords: list[str] | None = None,
    ) -> dict[str, Any]:
        return self.transcribe_audio_bytes(
            filename=audio_path.name,
            audio_bytes=audio_path.read_bytes(),
            mime_type=self._guess_mime_type(audio_path),
            user_id=user_id,
            prompt=prompt,
            hotwords=hotwords,
        )

    def transcribe_audio_bytes(
        self,
        *,
        filename: str,
        audio_bytes: bytes,
        mime_type: str = "application/octet-stream",
        user_id: str | None = None,
        prompt: str | None = None,
        hotwords: list[str] | None = None,
    ) -> dict[str, Any]:
        reason = self.availability_reason()
        if reason is not None:
            raise RuntimeError(reason)

        file_tuple = (filename, audio_bytes, mime_type)
        client = self._create_client()
        response = client.audio.transcriptions.create(
            file=file_tuple,
            model=self.model,
            prompt=prompt,
            hotwords=hotwords,
            user_id=user_id,
            timeout=self.timeout_seconds,
        )

        text = ""
        if getattr(response, "choices", None):
            first_choice = response.choices[0]
            text = str(getattr(getattr(first_choice, "message", None), "content", None) or "").strip()

        return {
            "provider": "zhipu_audio",
            "model": str(getattr(response, "model", None) or self.model),
            "text": text,
            "request_id": getattr(response, "request_id", None),
            "usage": response.usage.model_dump(mode="json") if hasattr(getattr(response, "usage", None), "model_dump") else {},
            "raw": response.model_dump(mode="json") if hasattr(response, "model_dump") else {},
        }

    def _create_client(self) -> Any:
        from zai import ZhipuAiClient

        return ZhipuAiClient(api_key=self.api_key)

    @staticmethod
    def _guess_mime_type(audio_path: Path) -> str:
        suffix = audio_path.suffix.lower()
        if suffix == ".wav":
            return "audio/wav"
        if suffix == ".mp3":
            return "audio/mpeg"
        if suffix == ".m4a":
            return "audio/mp4"
        return "application/octet-stream"
