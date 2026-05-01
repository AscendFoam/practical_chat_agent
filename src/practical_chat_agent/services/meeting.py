from __future__ import annotations

from pathlib import Path
from typing import Iterable

from practical_chat_agent.connectors.meeting.base import MeetingConnector
from practical_chat_agent.core.bus import InMemoryEventBus
from practical_chat_agent.core.enums import ChannelType, ContentType, Direction, MeetingAudioSource, SourceType
from practical_chat_agent.core.events import RuntimeEvent
from practical_chat_agent.core.models import (
    AgentTurnResult,
    InboundEvent,
    MeetingLivePreview,
    MeetingSegmentRecord,
    MeetingSessionRecord,
    MeetingTranscriptSegment,
    utc_now,
)
from practical_chat_agent.runtime.agent_runtime import AgentRuntime
from practical_chat_agent.services.meeting_assistant import MeetingAssistantService
from practical_chat_agent.storage.repositories.base import MeetingRepository


class MeetingMonitorService:
    """Coordinates meeting connectors and emits lightweight runtime events."""

    def __init__(
        self,
        *,
        connectors: dict[str, MeetingConnector],
        runtime: AgentRuntime | None = None,
        event_bus: InMemoryEventBus | None = None,
        meeting_repository: MeetingRepository | None = None,
        assistant_service: MeetingAssistantService | None = None,
    ) -> None:
        self.connectors = connectors
        self.runtime = runtime
        self.event_bus = event_bus
        self.meeting_repository = meeting_repository
        self.assistant_service = assistant_service

    def preview(
        self,
        *,
        connector_name: str,
        account_id: str,
        meeting_hint: str | None = None,
        sample_audio_path: Path | None = None,
        agent_id: str | None = None,
        audio_source: MeetingAudioSource = MeetingAudioSource.LOOPBACK,
        capture_seconds: float | None = None,
        chunk_seconds: float | None = None,
        save_capture: bool = False,
        device_name: str | None = None,
    ) -> MeetingLivePreview:
        connector = self.connectors.get(connector_name)
        if connector is None:
            raise ValueError(f"Unknown meeting connector: {connector_name}")

        result = connector.preview_live_session(
            account_id=account_id,
            meeting_hint=meeting_hint,
            sample_audio_path=sample_audio_path,
            audio_source=audio_source,
            capture_seconds=capture_seconds,
            chunk_seconds=chunk_seconds,
            save_capture=save_capture,
            device_name=device_name,
        )
        self._persist_meeting_preview(
            connector_name=connector_name,
            preview=result,
        )
        runtime_turns = self._dispatch_capture_chunks_to_runtime(
            connector_name=connector_name,
            preview=result,
            agent_id=agent_id,
        )
        result.runtime_agent_id = agent_id
        result.runtime_turns = runtime_turns

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

    def _persist_meeting_preview(
        self,
        *,
        connector_name: str,
        preview: MeetingLivePreview,
    ) -> None:
        if self.meeting_repository is None:
            return

        meeting_key = preview.meeting_title or preview.account_id
        channel_id = f"meeting::{preview.platform.value}::{meeting_key}"
        existing_session = self.meeting_repository.get_session_by_key(
            channel_id=channel_id,
            meeting_key=meeting_key,
        )
        now = utc_now()
        session_record = MeetingSessionRecord(
            session_id=existing_session.session_id if existing_session is not None else MeetingSessionRecord(
                connector_name=connector_name,
                platform=preview.platform,
                account_id=preview.account_id,
                meeting_key=meeting_key,
                channel_id=channel_id,
            ).session_id,
            connector_name=connector_name,
            platform=preview.platform,
            account_id=preview.account_id,
            meeting_key=meeting_key,
            meeting_title=preview.meeting_title,
            channel_id=channel_id,
            audio_source=preview.audio_source,
            capture_backend=preview.capture_backend,
            capture_device_name=preview.capture_device_name,
            transcription_backend=preview.transcription_backend,
            detected_window=preview.detected_window,
            notes=preview.notes[-20:],
            latest_summary=existing_session.latest_summary if existing_session is not None else None,
            latest_key_points=existing_session.latest_key_points if existing_session is not None else [],
            latest_action_items=existing_session.latest_action_items if existing_session is not None else [],
            latest_follow_up_questions=existing_session.latest_follow_up_questions if existing_session is not None else [],
            last_segment_at=existing_session.last_segment_at if existing_session is not None else None,
            created_at=existing_session.created_at if existing_session is not None else now,
            updated_at=now,
        )

        persisted_session = self.meeting_repository.upsert_session(session_record)
        preview.meeting_session_id = persisted_session.session_id

        segment_records = self._build_segment_records(
            connector_name=connector_name,
            preview=preview,
            session_id=persisted_session.session_id,
        )
        if segment_records:
            self.meeting_repository.add_segments(segment_records)
            latest_segment_time = max(
                (
                    segment.started_at
                    or segment.ended_at
                    or segment.created_at
                    for segment in segment_records
                ),
                default=now,
            )
            persisted_session.last_segment_at = latest_segment_time

        recent_segments = self.meeting_repository.list_recent_segments(
            session_id=persisted_session.session_id,
            limit=self._summary_segment_limit(),
        )
        summary_advice = self._build_summary_advice(
            meeting_title=preview.meeting_title,
            recent_segments=recent_segments,
        )
        persisted_session.latest_summary = summary_advice.summary
        persisted_session.latest_key_points = summary_advice.key_points
        persisted_session.latest_action_items = summary_advice.action_items
        persisted_session.latest_follow_up_questions = summary_advice.follow_up_questions
        persisted_session.updated_at = now
        persisted_session = self.meeting_repository.upsert_session(persisted_session)

        preview.rolling_summary = persisted_session.latest_summary
        preview.rolling_key_points = persisted_session.latest_key_points
        preview.rolling_action_items = persisted_session.latest_action_items
        preview.rolling_follow_up_questions = persisted_session.latest_follow_up_questions

        preview.notes.append(
            f"Meeting session '{persisted_session.session_id}' persisted with {len(segment_records)} new segment(s).",
        )

    def _build_summary_advice(
        self,
        *,
        meeting_title: str | None,
        recent_segments: Iterable[MeetingSegmentRecord],
    ):
        transcript_segments = [
            MeetingTranscriptSegment(
                speaker_name=segment.speaker_name,
                text=segment.text,
                display_time=segment.display_time,
                started_at=segment.started_at,
                ended_at=segment.ended_at,
                raw=segment.raw,
            )
            for segment in recent_segments
            if segment.text.strip()
        ]
        if self.assistant_service is not None:
            return self.assistant_service.build_summary_advice(
                meeting_title=meeting_title,
                transcript_segments=transcript_segments,
            )
        return MeetingAssistantService(
            api_key=None,
            base_url=None,
            model=None,
            enabled=False,
        ).build_summary_advice(
            meeting_title=meeting_title,
            transcript_segments=transcript_segments,
        )

    @staticmethod
    def _summary_segment_limit() -> int:
        return 12

    @staticmethod
    def _build_segment_records(
        *,
        connector_name: str,
        preview: MeetingLivePreview,
        session_id: str,
    ) -> list[MeetingSegmentRecord]:
        chunk_by_index = {chunk.chunk_index: chunk for chunk in preview.capture_chunks}
        records: list[MeetingSegmentRecord] = []
        for segment in preview.segments:
            raw = dict(segment.raw)
            chunk_index_raw = raw.get("chunk_index")
            chunk_index = int(chunk_index_raw) if isinstance(chunk_index_raw, int | float) else None
            matched_chunk = chunk_by_index.get(chunk_index) if chunk_index is not None else None
            records.append(
                MeetingSegmentRecord(
                    session_id=session_id,
                    connector_name=connector_name,
                    platform=preview.platform,
                    account_id=preview.account_id,
                    chunk_index=chunk_index,
                    speaker_name=segment.speaker_name,
                    display_time=segment.display_time,
                    text=segment.text,
                    started_at=segment.started_at,
                    ended_at=segment.ended_at,
                    audio_source=preview.audio_source,
                    capture_device_name=preview.capture_device_name or (matched_chunk.device_name if matched_chunk else None),
                    saved_path=matched_chunk.saved_path if matched_chunk is not None else None,
                    raw=raw,
                ),
            )
        return records

    def _dispatch_capture_chunks_to_runtime(
        self,
        *,
        connector_name: str,
        preview: MeetingLivePreview,
        agent_id: str | None,
    ) -> list[AgentTurnResult]:
        if self.runtime is None or not agent_id:
            if agent_id and self.runtime is None:
                preview.notes.append("Runtime agent dispatch was requested, but no runtime is configured.")
            return []

        runtime_turns: list[AgentTurnResult] = []
        for chunk in preview.capture_chunks:
            text = (chunk.transcription_text or "").strip()
            if not text:
                continue

            event = self._build_meeting_inbound_event(
                connector_name=connector_name,
                preview=preview,
                chunk=chunk,
                text=text,
            )
            turn = self.runtime.handle_inbound_event(agent_id=agent_id, event=event)
            runtime_turns.append(turn)
            preview.notes.append(
                f"Runtime dispatched meeting chunk {chunk.chunk_index:02d} to agent '{agent_id}' as event '{event.event_id}'.",
            )
            if self.event_bus is not None:
                self.event_bus.publish(
                    RuntimeEvent(
                        topic="meeting.segment.ingested",
                        payload={
                            "connector_name": connector_name,
                            "agent_id": agent_id,
                            "event_id": event.event_id,
                            "channel_id": event.channel_id,
                            "chunk_index": chunk.chunk_index,
                        },
                    ),
                )
        return runtime_turns

    @staticmethod
    def _build_meeting_inbound_event(
        *,
        connector_name: str,
        preview: MeetingLivePreview,
        chunk: object,
        text: str,
    ) -> InboundEvent:
        meeting_key = preview.meeting_title or preview.account_id
        channel_id = f"meeting::{preview.platform.value}::{meeting_key}"
        actor_id = f"{preview.audio_source.value}:{preview.capture_device_name or chunk.device_name}" if preview.audio_source else (preview.capture_device_name or chunk.device_name)
        return InboundEvent(
            event_id=f"meeting_{preview.account_id}_{chunk.chunk_index:02d}_{int(chunk.started_offset_seconds * 1000)}",
            source_type=SourceType.MEETING_SEGMENT,
            platform=preview.platform,
            channel_id=channel_id,
            channel_type=ChannelType.MEETING,
            account_id=preview.account_id,
            actor_id=actor_id,
            actor_name="self" if preview.audio_source == MeetingAudioSource.MICROPHONE else None,
            direction=Direction.INBOUND,
            content_type=ContentType.TEXT,
            text=text,
            attachments=[
                {
                    "type": "meeting_capture_chunk",
                    "connector_name": connector_name,
                    "audio_source": chunk.audio_source.value,
                    "device_name": chunk.device_name,
                    "saved_path": chunk.saved_path,
                    "display_time": chunk.display_time,
                },
            ],
            raw={
                "connector_name": connector_name,
                "meeting_title": preview.meeting_title,
                "audio_source": chunk.audio_source.value,
                "capture_device_name": chunk.device_name,
                "capture_backend": preview.capture_backend,
                "transcription_backend": preview.transcription_backend,
                "chunk": chunk.model_dump(mode="json"),
            },
        )
