from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from practical_chat_agent.connectors.meeting.base import MeetingConnector
from practical_chat_agent.connectors.desktop.windows_api import get_foreground_window_handle, list_visible_windows
from practical_chat_agent.core.enums import Platform
from practical_chat_agent.core.models import MeetingLivePreview, MeetingTranscriptSegment
from practical_chat_agent.services.audio_transcription import ZhipuAudioTranscriptionService
from practical_chat_agent.services.meeting_audio_capture import WindowsLoopbackAudioCaptureService


class TencentMeetingDesktopConnector(MeetingConnector):
    connector_name = "tencent_meeting_desktop"

    def __init__(
        self,
        *,
        transcription_service: ZhipuAudioTranscriptionService | None = None,
        audio_capture_service: WindowsLoopbackAudioCaptureService | None = None,
        capture_debug_dir: str | Path | None = None,
    ) -> None:
        self.transcription_service = transcription_service
        self.audio_capture_service = audio_capture_service
        self.capture_debug_dir = Path(capture_debug_dir or ".cache/meeting_captures")

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
        candidates = self._find_candidate_windows(meeting_hint=meeting_hint)
        notes: list[str] = []
        window = candidates[0] if candidates else None
        if window is None:
            notes.extend(
                [
                    "No Tencent Meeting desktop window was detected.",
                    "Make sure Tencent Meeting is running and its main meeting window is visible.",
                ],
            )
        else:
            foreground_hwnd = get_foreground_window_handle()
            notes.append(
                f"Detected Tencent Meeting candidate window: title='{window['title']}' process='{window['process_name']}'.",
            )
            notes.append(
                f"Window handle={window['hwnd']} pid={window['process_id']} class='{window['class_name']}' rect={window['rect']}.",
            )
            if foreground_hwnd is not None:
                notes.append(f"Current foreground window handle is {foreground_hwnd}.")
            if foreground_hwnd == int(window["hwnd"]):
                notes.append("Tencent Meeting is currently in the foreground, which is a good baseline for live loopback capture.")
            else:
                notes.append("Tencent Meeting is not currently the foreground window.")

        segments: list[MeetingTranscriptSegment] = []
        if sample_audio_path is not None:
            if not sample_audio_path.exists():
                notes.append(f"Sample audio file was not found: {sample_audio_path}")
            elif self.transcription_service is None:
                notes.append("No transcription service is configured, so the sample audio file was not processed.")
            else:
                sample_segment, sample_notes = self._transcribe_sample_audio(
                    sample_audio_path=sample_audio_path,
                    account_id=account_id,
                )
                notes.extend(sample_notes)
                if sample_segment is not None:
                    segments.append(sample_segment)
        elif window is not None:
            live_segments, live_notes = self._capture_and_transcribe_live_audio(
                account_id=account_id,
                capture_seconds=capture_seconds,
                chunk_seconds=chunk_seconds,
                save_capture=save_capture,
                speaker_name=speaker_name,
            )
            notes.extend(live_notes)
            segments.extend(live_segments)

        return MeetingLivePreview(
            connector_name=self.connector_name,
            platform=Platform.TENCENT_MEETING,
            account_id=account_id,
            meeting_title=str(window.get("title") or None) if window is not None else None,
            capture_backend=self._capture_backend_name(),
            transcription_backend=self._transcription_backend_name(),
            notes=notes,
            detected_window=window or {},
            segments=segments,
        )

    def _capture_and_transcribe_live_audio(
        self,
        *,
        account_id: str,
        capture_seconds: float | None,
        chunk_seconds: float | None,
        save_capture: bool,
        speaker_name: str | None,
    ) -> tuple[list[MeetingTranscriptSegment], list[str]]:
        notes: list[str] = []
        if self.audio_capture_service is None:
            return [], ["No loopback audio capture service is configured for this meeting connector."]

        capture_reason = self.audio_capture_service.availability_reason()
        if capture_reason is not None:
            return [], [f"Loopback audio capture is unavailable because {capture_reason}."]

        capture_started_at = datetime.now()
        try:
            captured_chunks, capture_notes = self.audio_capture_service.capture_loopback_chunks(
                account_id=account_id,
                capture_seconds=capture_seconds,
                chunk_seconds=chunk_seconds,
                save_capture=save_capture,
                speaker_name=speaker_name,
            )
        except Exception as exc:  # noqa: BLE001
            return [], [f"Loopback audio capture failed: {exc}"]

        notes.extend(capture_notes)
        if not captured_chunks:
            return [], notes

        if self.transcription_service is None:
            notes.append("Audio capture completed, but no transcription service is configured.")
            return [], notes

        transcription_reason = self.transcription_service.availability_reason()
        if transcription_reason is not None:
            notes.append(f"Audio capture completed, but transcription is unavailable because {transcription_reason}.")
            return [], notes

        segments: list[MeetingTranscriptSegment] = []
        for chunk in captured_chunks:
            filename = f"meeting_chunk_{chunk.chunk_index:02d}.wav"
            try:
                result = self.transcription_service.transcribe_audio_bytes(
                    filename=filename,
                    audio_bytes=chunk.wav_bytes,
                    mime_type="audio/wav",
                    user_id=account_id,
                )
            except Exception as exc:  # noqa: BLE001
                notes.append(f"Chunk {chunk.chunk_index} transcription failed: {exc}")
                continue

            text = str(result.get("text") or "").strip()
            if not text:
                notes.append(f"Chunk {chunk.chunk_index} transcription returned empty text.")
                continue

            started_at = capture_started_at + timedelta(seconds=chunk.started_offset_seconds)
            ended_at = started_at + timedelta(seconds=chunk.duration_seconds)
            segments.append(
                MeetingTranscriptSegment(
                    speaker_name=None,
                    text=text,
                    display_time=self._format_time_range(
                        chunk.started_offset_seconds,
                        chunk.started_offset_seconds + chunk.duration_seconds,
                    ),
                    started_at=started_at,
                    ended_at=ended_at,
                    is_final=True,
                    raw={
                        "source": "tencent_meeting_loopback_capture",
                        "chunk_index": chunk.chunk_index,
                        "duration_seconds": chunk.duration_seconds,
                        "started_offset_seconds": chunk.started_offset_seconds,
                        "output_device_name": chunk.speaker_name,
                        "sample_rate": chunk.sample_rate,
                        "channels": chunk.channels,
                        "rms": chunk.rms,
                        "saved_path": str(chunk.saved_path) if chunk.saved_path is not None else None,
                        "provider": result["provider"],
                        "model": result["model"],
                        "request_id": result.get("request_id"),
                        "usage": result.get("usage", {}),
                    },
                ),
            )

        if segments:
            notes.append(f"Live loopback transcription produced {len(segments)} text segment(s).")
        return segments, notes

    def _transcribe_sample_audio(
        self,
        *,
        sample_audio_path: Path,
        account_id: str,
    ) -> tuple[MeetingTranscriptSegment | None, list[str]]:
        notes: list[str] = []
        assert self.transcription_service is not None
        reason = self.transcription_service.availability_reason()
        if reason is not None:
            notes.append(f"Sample audio transcription is unavailable because {reason}.")
            return None, notes

        try:
            result = self.transcription_service.transcribe_audio_file(
                audio_path=sample_audio_path,
                user_id=account_id,
            )
        except Exception as exc:  # noqa: BLE001
            notes.append(f"Sample audio transcription failed: {exc}")
            return None, notes

        notes.append(f"Sample audio transcription completed using model '{result['model']}'.")
        return (
            MeetingTranscriptSegment(
                speaker_name=None,
                text=result["text"],
                display_time=None,
                is_final=True,
                raw={
                    "source": "sample_audio_transcription",
                    "audio_path": str(sample_audio_path),
                    "provider": result["provider"],
                    "model": result["model"],
                    "usage": result.get("usage", {}),
                },
            ),
            notes,
        )

    def _find_candidate_windows(self, *, meeting_hint: str | None) -> list[dict[str, object]]:
        hint = (meeting_hint or "").casefold()

        def matches(window: dict[str, object]) -> bool:
            title = str(window.get("title") or "")
            process_name = str(window.get("process_name") or "")
            lowered_title = title.casefold()
            lowered_process = process_name.casefold()
            return (
                "tencentmeeting" in lowered_process
                or "wemeetapp" in lowered_process
                or "\u817e\u8baf\u4f1a\u8bae" in title
                or "meeting" in lowered_title and "tencent" in lowered_title
            )

        candidates = [window for window in list_visible_windows() if matches(window)]
        if hint:
            hinted = [window for window in candidates if hint in str(window.get("title") or "").casefold()]
            if hinted:
                return hinted
        return candidates

    def _transcription_backend_name(self) -> str | None:
        if self.transcription_service is None:
            return None
        return self.transcription_service.backend_name

    def _capture_backend_name(self) -> str | None:
        if self.audio_capture_service is None:
            return None
        return self.audio_capture_service.backend_name

    @staticmethod
    def _format_time_range(start_seconds: float, end_seconds: float) -> str:
        def fmt(value: float) -> str:
            total_seconds = max(int(round(value)), 0)
            minutes, seconds = divmod(total_seconds, 60)
            return f"{minutes:02d}:{seconds:02d}"

        return f"{fmt(start_seconds)}-{fmt(end_seconds)}"
