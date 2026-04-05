from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from practical_chat_agent.core.models import MeetingLivePreview


class MeetingConnector(ABC):
    """Base abstraction for live meeting capture/transcription connectors."""

    connector_name: str

    @abstractmethod
    def preview_live_session(
        self,
        *,
        account_id: str,
        meeting_hint: str | None = None,
        sample_audio_path: Path | None = None,
        capture_seconds: float | None = None,
        chunk_seconds: float | None = None,
        save_capture: bool = False,
        speaker_name: str | None = None,
    ) -> MeetingLivePreview:
        """Inspect the current live meeting state and optionally process sample or captured audio."""
