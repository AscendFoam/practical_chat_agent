from __future__ import annotations

import io
import re
import wave
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class CapturedAudioChunk:
    chunk_index: int
    wav_bytes: bytes
    duration_seconds: float
    started_offset_seconds: float
    speaker_name: str
    sample_rate: int
    channels: int
    rms: float
    saved_path: Path | None = None


class WindowsLoopbackAudioCaptureService:
    """Capture Windows system output audio through WASAPI loopback using soundcard."""

    backend_name = "soundcard_wasapi_loopback"

    def __init__(
        self,
        *,
        sample_rate: int = 16000,
        default_capture_seconds: float = 6.0,
        default_chunk_seconds: float = 5.0,
        preferred_speaker_name: str | None = None,
        debug_dir: str | Path | None = None,
    ) -> None:
        self.sample_rate = sample_rate
        self.default_capture_seconds = default_capture_seconds
        self.default_chunk_seconds = default_chunk_seconds
        self.preferred_speaker_name = preferred_speaker_name
        self.debug_dir = Path(debug_dir or ".cache/meeting_captures")

    def availability_reason(self) -> str | None:
        if self._platform() != "win32":
            return "Windows loopback capture is only supported on Windows"
        try:
            import soundcard  # noqa: F401
            import numpy  # noqa: F401
        except Exception as exc:  # noqa: BLE001
            return f"loopback capture dependencies are unavailable: {exc}"
        return None

    def capture_loopback_chunks(
        self,
        *,
        account_id: str,
        capture_seconds: float | None = None,
        chunk_seconds: float | None = None,
        save_capture: bool = False,
        speaker_name: str | None = None,
    ) -> tuple[list[CapturedAudioChunk], list[str]]:
        reason = self.availability_reason()
        if reason is not None:
            raise RuntimeError(reason)

        import numpy as np
        import soundcard as sc

        resolved_capture_seconds = max(float(capture_seconds or self.default_capture_seconds), 0.25)
        resolved_chunk_seconds = max(float(chunk_seconds or self.default_chunk_seconds), 0.25)
        speaker = self._resolve_speaker(sc=sc, speaker_name=speaker_name)
        microphone = sc.get_microphone(id=str(speaker.id), include_loopback=True)
        if microphone is None:
            raise RuntimeError(f"No loopback microphone was found for speaker '{speaker.name}'.")

        notes = [
            f"Using loopback speaker '{speaker.name}' at {self.sample_rate} Hz.",
            f"Capturing {resolved_capture_seconds:.2f}s of system output audio in {resolved_chunk_seconds:.2f}s chunks.",
        ]

        total_frames = max(int(round(resolved_capture_seconds * self.sample_rate)), 1)
        recorded_chunks: list[Any] = []
        with microphone.recorder(samplerate=self.sample_rate) as recorder:
            remaining = total_frames
            frames_per_pull = max(int(round(min(resolved_chunk_seconds, 1.0) * self.sample_rate)), 1)
            while remaining > 0:
                next_frames = min(frames_per_pull, remaining)
                recorded = recorder.record(numframes=next_frames)
                if len(recorded):
                    recorded_chunks.append(recorded)
                remaining -= next_frames

        if not recorded_chunks:
            return [], notes + ["Loopback capture completed, but no audio frames were returned by the device."]

        audio = np.concatenate(recorded_chunks, axis=0)
        mono = audio if audio.ndim == 1 else audio.mean(axis=1)
        mono = np.clip(mono.astype(np.float32), -1.0, 1.0)

        chunks: list[CapturedAudioChunk] = []
        frames_per_chunk = max(int(round(resolved_chunk_seconds * self.sample_rate)), 1)
        for chunk_index, start in enumerate(range(0, len(mono), frames_per_chunk)):
            frames = mono[start:start + frames_per_chunk]
            if not len(frames):
                continue
            rms = float(np.sqrt(np.mean(np.square(frames), dtype=np.float64)))
            if rms < 0.0015:
                continue
            wav_bytes = self._encode_wav_bytes(frames=frames)
            saved_path = None
            if save_capture:
                saved_path = self._save_chunk(
                    account_id=account_id,
                    chunk_index=chunk_index,
                    wav_bytes=wav_bytes,
                    speaker_name=speaker.name,
                )
            chunks.append(
                CapturedAudioChunk(
                    chunk_index=chunk_index,
                    wav_bytes=wav_bytes,
                    duration_seconds=len(frames) / self.sample_rate,
                    started_offset_seconds=start / self.sample_rate,
                    speaker_name=speaker.name,
                    sample_rate=self.sample_rate,
                    channels=1,
                    rms=rms,
                    saved_path=saved_path,
                ),
            )

        if not chunks:
            return [], notes + ["Loopback capture completed, but every chunk was below the silence threshold."]

        notes.append(f"Loopback capture produced {len(chunks)} non-silent WAV chunk(s).")
        return chunks, notes

    def _resolve_speaker(self, *, sc: Any, speaker_name: str | None) -> Any:
        requested = (speaker_name or self.preferred_speaker_name or "").strip()
        speakers = list(sc.all_speakers())
        if requested:
            lowered = requested.casefold()
            for speaker in speakers:
                if lowered in str(speaker.name).casefold():
                    return speaker
            raise RuntimeError(f"No Windows speaker matched '{requested}'.")
        speaker = sc.default_speaker()
        if speaker is None:
            raise RuntimeError("Windows did not report a default speaker for loopback capture.")
        return speaker

    def _encode_wav_bytes(self, *, frames: Any) -> bytes:
        import numpy as np

        pcm = np.clip(frames * 32767.0, -32768, 32767).astype(np.int16)
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(pcm.tobytes())
        return buffer.getvalue()

    def _save_chunk(
        self,
        *,
        account_id: str,
        chunk_index: int,
        wav_bytes: bytes,
        speaker_name: str,
    ) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_account = re.sub(r"[^A-Za-z0-9_-]+", "_", account_id).strip("_") or "meeting"
        safe_speaker = re.sub(r"[^A-Za-z0-9_-]+", "_", speaker_name).strip("_") or "speaker"
        output_path = self.debug_dir / safe_account / f"{timestamp}_{safe_speaker}_chunk_{chunk_index:02d}.wav"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(wav_bytes)
        return output_path

    @staticmethod
    def _platform() -> str:
        import sys

        return sys.platform
