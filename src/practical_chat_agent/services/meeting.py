from __future__ import annotations

from pathlib import Path

from practical_chat_agent.connectors.meeting.base import MeetingConnector
from practical_chat_agent.core.bus import InMemoryEventBus
from practical_chat_agent.core.events import RuntimeEvent
from practical_chat_agent.core.models import MeetingLivePreview


class MeetingMonitorService:
    """Coordinates meeting connectors and emits lightweight runtime events."""

    def __init__(
        self,
        *,
        connectors: dict[str, MeetingConnector],
        event_bus: InMemoryEventBus | None = None,
    ) -> None:
        self.connectors = connectors
        self.event_bus = event_bus

    def preview(
        self,
        *,
        connector_name: str,
        account_id: str,
        meeting_hint: str | None = None,
        sample_audio_path: Path | None = None,
        capture_seconds: float | None = None,
        chunk_seconds: float | None = None,
        save_capture: bool = False,
        speaker_name: str | None = None,
    ) -> MeetingLivePreview:
        connector = self.connectors.get(connector_name)
        if connector is None:
            raise ValueError(f"Unknown meeting connector: {connector_name}")

        result = connector.preview_live_session(
            account_id=account_id,
            meeting_hint=meeting_hint,
            sample_audio_path=sample_audio_path,
            capture_seconds=capture_seconds,
            chunk_seconds=chunk_seconds,
            save_capture=save_capture,
            speaker_name=speaker_name,
        )

        if self.event_bus is not None:
            self.event_bus.publish(
                RuntimeEvent(
                    topic="meeting.preview.completed",
                    payload={
                        "connector_name": result.connector_name,
                        "platform": result.platform.value,
                        "account_id": result.account_id,
                        "segment_count": len(result.segments),
                    },
                ),
            )

        return result
