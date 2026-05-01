from __future__ import annotations

import io
import wave
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from practical_chat_agent.connectors.desktop.windows_api import get_foreground_window_handle, list_visible_windows
from practical_chat_agent.connectors.meeting.base import MeetingConnector
from practical_chat_agent.core.enums import MeetingAudioSource, Platform
from practical_chat_agent.core.models import MeetingCaptureChunkDebug, MeetingLivePreview, MeetingTranscriptSegment
from practical_chat_agent.services.audio_transcription import ZhipuAudioTranscriptionService
from practical_chat_agent.services.meeting_audio_capture import CapturedAudioChunk, WindowsAudioCaptureService


class TencentMeetingDesktopConnector(MeetingConnector):
    connector_name = "tencent_meeting_desktop"

    def __init__(
        self,
        *,
        transcription_service: ZhipuAudioTranscriptionService | None = None,
        audio_capture_service: WindowsAudioCaptureService | None = None,
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
        audio_source: MeetingAudioSource = MeetingAudioSource.LOOPBACK,
        capture_seconds: float | None = None,
        chunk_seconds: float | None = None,
        save_capture: bool = False,
        device_name: str | None = None,
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
                notes.append("Tencent Meeting is currently in the foreground, which is a good baseline for live audio capture.")
            else:
                notes.append("Tencent Meeting is not currently the foreground window.")

        capture_chunks: list[MeetingCaptureChunkDebug] = []
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
            live_segments, live_capture_chunks, live_notes = self._capture_and_transcribe_live_audio(
                account_id=account_id,
                audio_source=audio_source,
                capture_seconds=capture_seconds,
                chunk_seconds=chunk_seconds,
                save_capture=save_capture,
                device_name=device_name,
            )
            notes.extend(live_notes)
            capture_chunks.extend(live_capture_chunks)
            segments.extend(live_segments)

        return MeetingLivePreview(
            connector_name=self.connector_name,
            platform=Platform.TENCENT_MEETING,
            account_id=account_id,
            meeting_title=str(window.get("title") or None) if window is not None else None,
            audio_source=None if sample_audio_path is not None else audio_source,
            capture_backend=self._capture_backend_name(),
            capture_device_name=capture_chunks[0].device_name if capture_chunks else None,
            transcription_backend=self._transcription_backend_name(),
            notes=notes,
            detected_window=window or {},
            capture_chunks=capture_chunks,
            segments=segments,
        )

    def _capture_and_transcribe_live_audio(
        self,
        *,
        account_id: str,
        audio_source: MeetingAudioSource,
        capture_seconds: float | None,
        chunk_seconds: float | None,
        save_capture: bool,
        device_name: str | None,
    ) -> tuple[list[MeetingTranscriptSegment], list[MeetingCaptureChunkDebug], list[str]]:
        notes: list[str] = []
        if self.audio_capture_service is None:
            return [], [], ["No audio capture service is configured for this meeting connector."]

        capture_reason = self.audio_capture_service.availability_reason()
        if capture_reason is not None:
            return [], [], [f"Audio capture is unavailable because {capture_reason}."]

        capture_started_at = datetime.now()
        try:
            captured_chunks, capture_notes = self.audio_capture_service.capture_audio_chunks(
                account_id=account_id,
                audio_source=audio_source,
                capture_seconds=capture_seconds,
                chunk_seconds=chunk_seconds,
                save_capture=save_capture,
                device_name=device_name,
            )
        except Exception as exc:  # noqa: BLE001
            return [], [], [f"Audio capture failed: {exc}"]

        notes.extend(capture_notes)
        chunk_debug = [self._to_chunk_debug(chunk=chunk) for chunk in captured_chunks]
        if not captured_chunks:
            return [], chunk_debug, notes

        if self.transcription_service is None:
            notes.append("Audio capture completed, but no transcription service is configured.")
            self._mark_transcription_unavailable(chunk_debug=chunk_debug, status="skipped_no_transcription_service")
            notes.extend(self._format_chunk_debug_notes(chunk_debug))
            return [], chunk_debug, notes

        transcription_reason = self.transcription_service.availability_reason()
        if transcription_reason is not None:
            notes.append(f"Audio capture completed, but transcription is unavailable because {transcription_reason}.")
            self._mark_transcription_unavailable(chunk_debug=chunk_debug, status="skipped_transcription_unavailable")
            notes.extend(self._format_chunk_debug_notes(chunk_debug))
            return [], chunk_debug, notes

        segments: list[MeetingTranscriptSegment] = []
        previous_success_text: str | None = None
        for chunk, debug_entry in zip(captured_chunks, chunk_debug, strict=True):
            if chunk.is_silent:
                debug_entry.transcription_status = "skipped_silent"
                continue

            filename = f"meeting_chunk_{chunk.chunk_index:02d}.wav"
            try:
                result = self.transcription_service.transcribe_audio_bytes(
                    filename=filename,
                    audio_bytes=chunk.wav_bytes,
                    mime_type="audio/wav",
                    user_id=account_id,
                )
            except Exception as exc:  # noqa: BLE001
                debug_entry.transcription_status = "error"
                debug_entry.transcription_error = str(exc)
                notes.append(f"Chunk {chunk.chunk_index} transcription failed: {exc}")
                continue

            text = str(result.get("text") or "").strip()
            if not text:
                retry_result, retry_notes = self._retry_empty_transcription(
                    chunk=chunk,
                    chunk_index=chunk.chunk_index,
                    captured_chunks=captured_chunks,
                    account_id=account_id,
                    previous_success_text=previous_success_text,
                )
                notes.extend(retry_notes)
                if retry_result is not None:
                    debug_entry.transcription_retry_count = int(retry_result["retry_count"])
                    strategy = retry_result.get("strategy")
                    debug_entry.transcription_retry_strategy = None if strategy is None else str(strategy)
                    retried_result = retry_result.get("result")
                    if retried_result is not None:
                        result = retried_result
                        text = str(result.get("text") or "").strip()
                if not text:
                    debug_entry.transcription_status = "empty"
                    notes.append(f"Chunk {chunk.chunk_index} transcription returned empty text after retry.")
                    continue

            debug_entry.transcription_status = "success"
            debug_entry.transcription_text = text
            previous_success_text = text
            started_at = capture_started_at + timedelta(seconds=chunk.started_offset_seconds)
            ended_at = started_at + timedelta(seconds=chunk.duration_seconds)
            segments.append(
                MeetingTranscriptSegment(
                    speaker_name="self" if audio_source == MeetingAudioSource.MICROPHONE else None,
                    text=text,
                    display_time=debug_entry.display_time,
                    started_at=started_at,
                    ended_at=ended_at,
                    is_final=True,
                    raw={
                        "source": "tencent_meeting_audio_capture",
                        "audio_source": chunk.audio_source.value,
                        "capture_device_name": chunk.device_name,
                        "chunk_index": chunk.chunk_index,
                        "duration_seconds": chunk.duration_seconds,
                        "started_offset_seconds": chunk.started_offset_seconds,
                        "sample_rate": chunk.sample_rate,
                        "channels": chunk.channels,
                        "rms": chunk.rms,
                        "peak": chunk.peak,
                        "compressor_threshold": chunk.compressor_threshold,
                        "compressor_ratio": chunk.compressor_ratio,
                        "limiter_ceiling": chunk.limiter_ceiling,
                        "dc_offset": chunk.dc_offset,
                        "highpass_cutoff_hz": chunk.highpass_cutoff_hz,
                        "trimmed_start_seconds": chunk.trimmed_start_seconds,
                        "trimmed_end_seconds": chunk.trimmed_end_seconds,
                        "silence_threshold": chunk.silence_threshold,
                        "transcription_retry_count": debug_entry.transcription_retry_count,
                        "transcription_retry_strategy": debug_entry.transcription_retry_strategy,
                        "saved_path": str(chunk.saved_path) if chunk.saved_path is not None else None,
                        "provider": result["provider"],
                        "model": result["model"],
                        "request_id": result.get("request_id"),
                        "usage": result.get("usage", {}),
                    },
                ),
            )

        notes.extend(self._format_chunk_debug_notes(chunk_debug))
        if segments:
            notes.append(f"Live {audio_source.value} transcription produced {len(segments)} text segment(s).")
        return segments, chunk_debug, notes

    @staticmethod
    def _mark_transcription_unavailable(
        *,
        chunk_debug: list[MeetingCaptureChunkDebug],
        status: str,
    ) -> None:
        for entry in chunk_debug:
            entry.transcription_status = "skipped_silent" if entry.is_silent else status

    def _to_chunk_debug(self, *, chunk: CapturedAudioChunk) -> MeetingCaptureChunkDebug:
        return MeetingCaptureChunkDebug(
            chunk_index=chunk.chunk_index,
            audio_source=chunk.audio_source,
            device_name=chunk.device_name,
            display_time=self._format_time_range(
                chunk.started_offset_seconds,
                chunk.started_offset_seconds + chunk.duration_seconds,
            ),
            started_offset_seconds=chunk.started_offset_seconds,
            duration_seconds=chunk.duration_seconds,
            sample_rate=chunk.sample_rate,
            channels=chunk.channels,
            rms=chunk.rms,
            peak=chunk.peak,
            applied_gain=chunk.applied_gain,
            normalization_gain=chunk.normalization_gain,
            compressor_threshold=chunk.compressor_threshold,
            compressor_ratio=chunk.compressor_ratio,
            limiter_ceiling=chunk.limiter_ceiling,
            dc_offset=chunk.dc_offset,
            highpass_cutoff_hz=chunk.highpass_cutoff_hz,
            trimmed_start_seconds=chunk.trimmed_start_seconds,
            trimmed_end_seconds=chunk.trimmed_end_seconds,
            silence_threshold=chunk.silence_threshold,
            is_silent=chunk.is_silent,
            wav_size_bytes=chunk.wav_size_bytes,
            saved_path=str(chunk.saved_path) if chunk.saved_path is not None else None,
        )

    def _retry_empty_transcription(
        self,
        *,
        chunk: CapturedAudioChunk,
        chunk_index: int,
        captured_chunks: list[CapturedAudioChunk],
        account_id: str,
        previous_success_text: str | None,
    ) -> tuple[dict[str, Any] | None, list[str]]:
        notes: list[str] = []
        if self.transcription_service is None or not self.transcription_service.empty_retry_enabled:
            return None, notes

        retry_prompt = self._build_retry_prompt(previous_success_text=previous_success_text)
        retry_count = 0
        if retry_prompt:
            retry_count += 1
            try:
                result = self.transcription_service.transcribe_audio_bytes(
                    filename=f"meeting_chunk_{chunk_index:02d}_retry_prompt.wav",
                    audio_bytes=chunk.wav_bytes,
                    mime_type="audio/wav",
                    user_id=account_id,
                    prompt=retry_prompt,
                )
            except Exception as exc:  # noqa: BLE001
                notes.append(f"Chunk {chunk_index} prompt retry failed: {exc}")
            else:
                if str(result.get("text") or "").strip():
                    notes.append(f"Chunk {chunk_index} prompt retry produced text.")
                    return {"result": result, "retry_count": retry_count, "strategy": "prompt_retry"}, notes
                notes.append(f"Chunk {chunk_index} prompt retry still returned empty text.")

        merged_bytes = self._merge_neighbor_wavs(
            chunk_index=chunk_index,
            captured_chunks=captured_chunks,
            neighbor_radius=1,
        )
        if merged_bytes is None:
            return {"result": None, "retry_count": retry_count, "strategy": "prompt_retry_only" if retry_count else None}, notes

        retry_count += 1
        try:
            result = self.transcription_service.transcribe_audio_bytes(
                filename=f"meeting_chunk_{chunk_index:02d}_merged_retry.wav",
                audio_bytes=merged_bytes,
                mime_type="audio/wav",
                user_id=account_id,
                prompt=retry_prompt,
            )
        except Exception as exc:  # noqa: BLE001
            notes.append(f"Chunk {chunk_index} merged retry failed: {exc}")
            return {"result": None, "retry_count": retry_count, "strategy": "merged_neighbor_retry"}, notes

        if str(result.get("text") or "").strip():
            notes.append(f"Chunk {chunk_index} merged retry produced text.")
            return {"result": result, "retry_count": retry_count, "strategy": "merged_neighbor_retry"}, notes

        notes.append(f"Chunk {chunk_index} merged retry still returned empty text.")
        merged_three_bytes = self._merge_neighbor_wavs(
            chunk_index=chunk_index,
            captured_chunks=captured_chunks,
            neighbor_radius=2,
        )
        if merged_three_bytes is None:
            return {"result": None, "retry_count": retry_count, "strategy": "merged_neighbor_retry"}, notes

        retry_count += 1
        try:
            result = self.transcription_service.transcribe_audio_bytes(
                filename=f"meeting_chunk_{chunk_index:02d}_merged3_retry.wav",
                audio_bytes=merged_three_bytes,
                mime_type="audio/wav",
                user_id=account_id,
                prompt=retry_prompt,
            )
        except Exception as exc:  # noqa: BLE001
            notes.append(f"Chunk {chunk_index} merged-3 retry failed: {exc}")
            return {"result": None, "retry_count": retry_count, "strategy": "merged_three_chunk_retry"}, notes

        if str(result.get("text") or "").strip():
            notes.append(f"Chunk {chunk_index} merged-3 retry produced text.")
            return {"result": result, "retry_count": retry_count, "strategy": "merged_three_chunk_retry"}, notes

        notes.append(f"Chunk {chunk_index} merged-3 retry still returned empty text.")
        return {"result": None, "retry_count": retry_count, "strategy": "merged_three_chunk_retry"}, notes

    def _build_retry_prompt(self, *, previous_success_text: str | None) -> str | None:
        base_prompt = self.transcription_service.empty_retry_prompt if self.transcription_service is not None else None
        cleaned_base = str(base_prompt or "").strip()
        cleaned_context = str(previous_success_text or "").strip()
        if cleaned_base and cleaned_context:
            return f"{cleaned_base}\n上一段已识别内容：{cleaned_context}\n请结合上下文继续识别当前语音。"
        if cleaned_context:
            return f"上一段已识别内容：{cleaned_context}\n请结合上下文继续识别当前语音。"
        return cleaned_base or None

    @staticmethod
    def _merge_neighbor_wavs(
        *,
        chunk_index: int,
        captured_chunks: list[CapturedAudioChunk],
        neighbor_radius: int = 1,
    ) -> bytes | None:
        selected = [
            chunk
            for chunk in captured_chunks
            if not chunk.is_silent and abs(chunk.chunk_index - chunk_index) <= neighbor_radius
        ]
        selected.sort(key=lambda item: item.chunk_index)
        if len(selected) < 2:
            return None

        pcm_frames: list[bytes] = []
        sample_rate: int | None = None
        sample_width: int | None = None
        channels: int | None = None
        for chunk in selected:
            with wave.open(io.BytesIO(chunk.wav_bytes), "rb") as wav_file:
                current_rate = wav_file.getframerate()
                current_width = wav_file.getsampwidth()
                current_channels = wav_file.getnchannels()
                if sample_rate is None:
                    sample_rate = current_rate
                    sample_width = current_width
                    channels = current_channels
                if current_rate != sample_rate or current_width != sample_width or current_channels != channels:
                    return None
                pcm_frames.append(wav_file.readframes(wav_file.getnframes()))

        if sample_rate is None or sample_width is None or channels is None:
            return None
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b"".join(pcm_frames))
        return buffer.getvalue()

    @staticmethod
    def _format_chunk_debug_notes(chunk_debug: list[MeetingCaptureChunkDebug]) -> list[str]:
        notes: list[str] = []
        for entry in chunk_debug:
            notes.append(
                "Chunk "
                f"{entry.chunk_index:02d}"
                f" | source={entry.audio_source.value}"
                f" | device='{entry.device_name}'"
                f" | range={entry.display_time or '?'}"
                f" | duration={entry.duration_seconds:.2f}s"
                f" | rms={entry.rms:.6f}"
                f" | peak={(entry.peak if entry.peak is not None else 0.0):.6f}"
                f" | gain={(entry.applied_gain if entry.applied_gain is not None else 1.0):.2f}"
                f" | norm_gain={(entry.normalization_gain if entry.normalization_gain is not None else 1.0):.2f}"
                f" | comp={(entry.compressor_threshold if entry.compressor_threshold is not None else 0.0):.2f}/{(entry.compressor_ratio if entry.compressor_ratio is not None else 1.0):.2f}"
                f" | limiter={(entry.limiter_ceiling if entry.limiter_ceiling is not None else 1.0):.2f}"
                f" | dc={(entry.dc_offset if entry.dc_offset is not None else 0.0):.6f}"
                f" | hp={(entry.highpass_cutoff_hz if entry.highpass_cutoff_hz is not None else 0.0):.1f}Hz"
                f" | trim={entry.trimmed_start_seconds:.2f}s/{entry.trimmed_end_seconds:.2f}s"
                f" | threshold={entry.silence_threshold:.6f}"
                f" | silent={'yes' if entry.is_silent else 'no'}"
                f" | wav_bytes={entry.wav_size_bytes}"
                f" | saved_path={entry.saved_path or '<not saved>'}"
                f" | transcription_status={entry.transcription_status or 'not_attempted'}"
                f" | retry_count={entry.transcription_retry_count}"
                f" | retry_strategy={entry.transcription_retry_strategy or '<none>'}"
                + (f" | transcription_error={entry.transcription_error}" if entry.transcription_error else ""),
            )
        return notes

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
                or "腾讯会议" in title
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
