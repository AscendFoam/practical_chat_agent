from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field, replace
from datetime import datetime
from threading import Event
from time import monotonic
from typing import Callable

from practical_chat_agent.core.enums import MeetingAudioSource
from practical_chat_agent.core.models import (
    MeetingCaptureChunkDebug,
    MeetingLivePreview,
    MeetingTranscriptSegment,
)
from practical_chat_agent.services.meeting import MeetingMonitorService


@dataclass(slots=True)
class MeetingLiveLoopRequest:
    connector_name: str
    account_id: str
    meeting_hint: str | None = None
    agent_id: str | None = None
    audio_source: MeetingAudioSource = MeetingAudioSource.LOOPBACK
    capture_seconds: float | None = None
    chunk_seconds: float | None = None
    save_capture: bool = False
    device_name: str | None = None
    cooldown_seconds: float = 0.25


@dataclass(slots=True)
class MeetingLiveLoopUpdate:
    iteration: int
    status: str
    request: MeetingLiveLoopRequest
    preview: MeetingLivePreview | None = None
    new_segments: list[MeetingTranscriptSegment] = field(default_factory=list)
    latest_chunk: MeetingCaptureChunkDebug | None = None
    message: str = ""
    error: str | None = None
    emitted_at: datetime = field(default_factory=datetime.now)


class MeetingLiveLoopService:
    """Run the existing meeting preview flow in a continuous loop for live captions."""

    def __init__(self, *, meeting_service: MeetingMonitorService) -> None:
        self.meeting_service = meeting_service

    def run_once(
        self,
        *,
        request: MeetingLiveLoopRequest,
        iteration: int = 1,
        seen_signatures: set[str] | None = None,
        seen_order: deque[str] | None = None,
    ) -> MeetingLiveLoopUpdate:
        resolved_request = self._normalize_request(request)
        preview = self.meeting_service.preview(
            connector_name=resolved_request.connector_name,
            account_id=resolved_request.account_id,
            meeting_hint=resolved_request.meeting_hint,
            agent_id=resolved_request.agent_id,
            audio_source=resolved_request.audio_source,
            capture_seconds=resolved_request.capture_seconds,
            chunk_seconds=resolved_request.chunk_seconds,
            save_capture=resolved_request.save_capture,
            device_name=resolved_request.device_name,
        )
        new_segments = self._collect_new_segments(
            preview=preview,
            seen_signatures=seen_signatures,
            seen_order=seen_order,
        )
        latest_chunk = preview.capture_chunks[-1] if preview.capture_chunks else None
        return MeetingLiveLoopUpdate(
            iteration=iteration,
            status=self._resolve_status(preview=preview, new_segments=new_segments),
            request=resolved_request,
            preview=preview,
            new_segments=new_segments,
            latest_chunk=latest_chunk,
            message=self._build_message(preview=preview, new_segments=new_segments, latest_chunk=latest_chunk),
        )

    def run_forever(
        self,
        *,
        request: MeetingLiveLoopRequest,
        on_update: Callable[[MeetingLiveLoopUpdate], None],
        stop_event: Event,
        signature_cache_size: int = 256,
    ) -> None:
        seen_signatures: set[str] = set()
        seen_order: deque[str] = deque(maxlen=max(int(signature_cache_size), 32))
        resolved_request = self._normalize_request(request)
        iteration = 0

        while not stop_event.is_set():
            iteration += 1
            started_at = monotonic()
            try:
                update = self.run_once(
                    request=resolved_request,
                    iteration=iteration,
                    seen_signatures=seen_signatures,
                    seen_order=seen_order,
                )
            except Exception as exc:  # noqa: BLE001
                update = MeetingLiveLoopUpdate(
                    iteration=iteration,
                    status="error",
                    request=resolved_request,
                    message=f"Live transcription loop failed: {exc}",
                    error=str(exc),
                )

            on_update(update)
            elapsed_seconds = monotonic() - started_at
            wait_seconds = max(float(resolved_request.cooldown_seconds) - elapsed_seconds, 0.0)
            if stop_event.wait(wait_seconds):
                break

        on_update(
            MeetingLiveLoopUpdate(
                iteration=iteration,
                status="stopped",
                request=resolved_request,
                message="Live caption loop stopped.",
            ),
        )

    @staticmethod
    def _normalize_request(request: MeetingLiveLoopRequest) -> MeetingLiveLoopRequest:
        resolved_chunk_seconds = max(float(request.chunk_seconds or 2.0), 0.5)
        resolved_capture_seconds = max(float(request.capture_seconds or resolved_chunk_seconds), resolved_chunk_seconds)
        return replace(
            request,
            chunk_seconds=resolved_chunk_seconds,
            capture_seconds=resolved_capture_seconds,
            cooldown_seconds=max(float(request.cooldown_seconds), 0.0),
        )

    @staticmethod
    def _collect_new_segments(
        *,
        preview: MeetingLivePreview,
        seen_signatures: set[str] | None,
        seen_order: deque[str] | None,
    ) -> list[MeetingTranscriptSegment]:
        if seen_signatures is None or seen_order is None:
            return [segment for segment in preview.segments if segment.text.strip()]

        new_segments: list[MeetingTranscriptSegment] = []
        for segment in preview.segments:
            text = segment.text.strip()
            if not text:
                continue
            signature = MeetingLiveLoopService._segment_signature(segment=segment)
            if signature in seen_signatures:
                continue
            if len(seen_order) == seen_order.maxlen:
                evicted = seen_order.popleft()
                seen_signatures.discard(evicted)
            seen_order.append(signature)
            seen_signatures.add(signature)
            new_segments.append(segment)
        return new_segments

    @staticmethod
    def _segment_signature(*, segment: MeetingTranscriptSegment) -> str:
        started_at = segment.started_at.isoformat() if segment.started_at is not None else ""
        return "|".join(
            [
                started_at,
                segment.display_time or "",
                segment.speaker_name or "",
                segment.text.strip(),
            ],
        )

    @staticmethod
    def _resolve_status(
        *,
        preview: MeetingLivePreview,
        new_segments: list[MeetingTranscriptSegment],
    ) -> str:
        if new_segments:
            return "transcribed"
        if not preview.detected_window:
            return "waiting_window"
        if preview.capture_chunks and all(chunk.is_silent for chunk in preview.capture_chunks):
            return "silence"
        if preview.capture_chunks:
            return "listening"
        return "idle"

    @staticmethod
    def _build_message(
        *,
        preview: MeetingLivePreview,
        new_segments: list[MeetingTranscriptSegment],
        latest_chunk: MeetingCaptureChunkDebug | None,
    ) -> str:
        if new_segments:
            joined = " / ".join(segment.text.strip() for segment in new_segments[:2])
            return f"Received {len(new_segments)} subtitle line(s): {joined[:120]}"
        if latest_chunk is not None:
            if latest_chunk.is_silent:
                return (
                    f"Listening... latest chunk looks silent "
                    f"(rms={latest_chunk.rms:.6f}, duration={latest_chunk.duration_seconds:.2f}s)."
                )
            return (
                "Listening... "
                f"rms={latest_chunk.rms:.6f}, retry={latest_chunk.transcription_retry_count}, "
                f"status={latest_chunk.transcription_status or 'pending'}."
            )
        if preview.notes:
            return preview.notes[-1]
        return "Waiting for meeting audio."
