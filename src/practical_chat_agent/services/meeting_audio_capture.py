from __future__ import annotations

import io
import re
import wave
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from practical_chat_agent.core.enums import MeetingAudioSource


@dataclass(slots=True)
class CapturedAudioChunk:
    chunk_index: int
    audio_source: MeetingAudioSource
    device_name: str
    wav_bytes: bytes
    wav_size_bytes: int
    duration_seconds: float
    started_offset_seconds: float
    sample_rate: int
    channels: int
    rms: float
    peak: float
    applied_gain: float
    normalization_gain: float
    compressor_threshold: float
    compressor_ratio: float
    limiter_ceiling: float
    dc_offset: float
    highpass_cutoff_hz: float
    trimmed_start_seconds: float
    trimmed_end_seconds: float
    silence_threshold: float
    is_silent: bool
    saved_path: Path | None = None


class WindowsAudioCaptureService:
    """Capture Windows loopback or microphone audio through soundcard."""

    backend_name = "soundcard_windows_audio_capture"

    def __init__(
        self,
        *,
        sample_rate: int = 16000,
        default_capture_seconds: float = 6.0,
        default_chunk_seconds: float = 5.0,
        preferred_speaker_name: str | None = None,
        preferred_microphone_name: str | None = None,
        silence_threshold: float = 0.0015,
        microphone_boost_gain: float = 1.8,
        microphone_peak_target: float = 0.92,
        microphone_silence_floor: float = 0.0030,
        microphone_highpass_cutoff_hz: float = 80.0,
        microphone_trim_padding_seconds: float = 0.12,
        microphone_compressor_threshold: float = 0.45,
        microphone_compressor_ratio: float = 3.0,
        microphone_limiter_ceiling: float = 0.96,
        debug_dir: str | Path | None = None,
    ) -> None:
        self.sample_rate = sample_rate
        self.default_capture_seconds = default_capture_seconds
        self.default_chunk_seconds = default_chunk_seconds
        self.preferred_speaker_name = preferred_speaker_name
        self.preferred_microphone_name = preferred_microphone_name
        self.silence_threshold = silence_threshold
        self.microphone_boost_gain = max(float(microphone_boost_gain), 1.0)
        self.microphone_peak_target = min(max(float(microphone_peak_target), 0.1), 0.99)
        self.microphone_silence_floor = max(float(microphone_silence_floor), self.silence_threshold)
        self.microphone_highpass_cutoff_hz = max(float(microphone_highpass_cutoff_hz), 0.0)
        self.microphone_trim_padding_seconds = max(float(microphone_trim_padding_seconds), 0.0)
        self.microphone_compressor_threshold = min(max(float(microphone_compressor_threshold), 0.05), 0.95)
        self.microphone_compressor_ratio = max(float(microphone_compressor_ratio), 1.0)
        self.microphone_limiter_ceiling = min(max(float(microphone_limiter_ceiling), 0.2), 0.99)
        self.debug_dir = Path(debug_dir or ".cache/meeting_captures")

    def availability_reason(self) -> str | None:
        if self._platform() != "win32":
            return "Windows audio capture is only supported on Windows"
        try:
            import soundcard  # noqa: F401
            import numpy  # noqa: F401
        except Exception as exc:  # noqa: BLE001
            return f"audio capture dependencies are unavailable: {exc}"
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
        return self.capture_audio_chunks(
            account_id=account_id,
            audio_source=MeetingAudioSource.LOOPBACK,
            capture_seconds=capture_seconds,
            chunk_seconds=chunk_seconds,
            save_capture=save_capture,
            device_name=speaker_name,
        )

    def capture_microphone_chunks(
        self,
        *,
        account_id: str,
        capture_seconds: float | None = None,
        chunk_seconds: float | None = None,
        save_capture: bool = False,
        microphone_name: str | None = None,
    ) -> tuple[list[CapturedAudioChunk], list[str]]:
        return self.capture_audio_chunks(
            account_id=account_id,
            audio_source=MeetingAudioSource.MICROPHONE,
            capture_seconds=capture_seconds,
            chunk_seconds=chunk_seconds,
            save_capture=save_capture,
            device_name=microphone_name,
        )

    def capture_audio_chunks(
        self,
        *,
        account_id: str,
        audio_source: MeetingAudioSource = MeetingAudioSource.LOOPBACK,
        capture_seconds: float | None = None,
        chunk_seconds: float | None = None,
        save_capture: bool = False,
        device_name: str | None = None,
    ) -> tuple[list[CapturedAudioChunk], list[str]]:
        reason = self.availability_reason()
        if reason is not None:
            raise RuntimeError(reason)

        import numpy as np
        import soundcard as sc

        resolved_capture_seconds = max(float(capture_seconds or self.default_capture_seconds), 0.25)
        resolved_chunk_seconds = max(float(chunk_seconds or self.default_chunk_seconds), 0.25)
        recorder_device, resolved_device_name, capture_label = self._resolve_recorder_device(
            sc=sc,
            audio_source=audio_source,
            device_name=device_name,
        )

        notes = [
            f"Using {audio_source.value} device '{resolved_device_name}' at {self.sample_rate} Hz.",
            f"Capturing {resolved_capture_seconds:.2f}s of {capture_label} in {resolved_chunk_seconds:.2f}s chunks.",
            f"Base silence threshold is set to RMS<{self.silence_threshold:.6f}.",
        ]
        if audio_source == MeetingAudioSource.MICROPHONE:
            notes.append(
                "Microphone enhancement is enabled with "
                f"boost_gain={self.microphone_boost_gain:.2f}, peak_target={self.microphone_peak_target:.2f}, "
                f"silence_floor={self.microphone_silence_floor:.6f}, "
                f"highpass={self.microphone_highpass_cutoff_hz:.1f}Hz, "
                f"trim_padding={self.microphone_trim_padding_seconds:.2f}s, "
                f"compressor={self.microphone_compressor_threshold:.2f}/{self.microphone_compressor_ratio:.2f}, "
                f"limiter={self.microphone_limiter_ceiling:.2f}.",
            )

        total_frames = max(int(round(resolved_capture_seconds * self.sample_rate)), 1)
        recorded_chunks: list[Any] = []
        with recorder_device.recorder(samplerate=self.sample_rate) as recorder:
            remaining = total_frames
            frames_per_pull = max(int(round(min(resolved_chunk_seconds, 1.0) * self.sample_rate)), 1)
            while remaining > 0:
                next_frames = min(frames_per_pull, remaining)
                recorded = recorder.record(numframes=next_frames)
                if len(recorded):
                    recorded_chunks.append(recorded)
                remaining -= next_frames

        if not recorded_chunks:
            return [], notes + ["Audio capture completed, but no audio frames were returned by the device."]

        audio = np.concatenate(recorded_chunks, axis=0)
        channel_count = int(audio.shape[1]) if getattr(audio, "ndim", 1) > 1 else 1
        mono = audio if audio.ndim == 1 else audio.mean(axis=1)
        mono = np.clip(mono.astype(np.float32), -1.0, 1.0)

        chunks: list[CapturedAudioChunk] = []
        frames_per_chunk = max(int(round(resolved_chunk_seconds * self.sample_rate)), 1)
        for chunk_index, start in enumerate(range(0, len(mono), frames_per_chunk)):
            frames = mono[start:start + frames_per_chunk]
            if not len(frames):
                continue

            processed_frames, metrics = self._prepare_chunk_frames(
                frames=frames,
                audio_source=audio_source,
            )
            wav_bytes = self._encode_wav_bytes(frames=processed_frames)
            saved_path = None
            if save_capture:
                saved_path = self._save_chunk(
                    account_id=account_id,
                    audio_source=audio_source,
                    chunk_index=chunk_index,
                    wav_bytes=wav_bytes,
                    device_name=resolved_device_name,
                )

            chunks.append(
                CapturedAudioChunk(
                    chunk_index=chunk_index,
                    audio_source=audio_source,
                    device_name=resolved_device_name,
                    wav_bytes=wav_bytes,
                    wav_size_bytes=len(wav_bytes),
                    duration_seconds=len(processed_frames) / self.sample_rate,
                    started_offset_seconds=start / self.sample_rate + float(metrics["trimmed_start_seconds"]),
                    sample_rate=self.sample_rate,
                    channels=channel_count,
                    rms=metrics["rms"],
                    peak=metrics["peak"],
                    applied_gain=metrics["applied_gain"],
                    normalization_gain=metrics["normalization_gain"],
                    compressor_threshold=metrics["compressor_threshold"],
                    compressor_ratio=metrics["compressor_ratio"],
                    limiter_ceiling=metrics["limiter_ceiling"],
                    dc_offset=metrics["dc_offset"],
                    highpass_cutoff_hz=metrics["highpass_cutoff_hz"],
                    trimmed_start_seconds=metrics["trimmed_start_seconds"],
                    trimmed_end_seconds=metrics["trimmed_end_seconds"],
                    silence_threshold=metrics["silence_threshold"],
                    is_silent=metrics["is_silent"],
                    saved_path=saved_path,
                ),
            )

        if not chunks:
            return [], notes + ["Audio capture completed, but no chunk metadata was produced."]

        non_silent_count = sum(1 for chunk in chunks if not chunk.is_silent)
        silent_count = len(chunks) - non_silent_count
        notes.append(
            f"Audio capture produced {len(chunks)} WAV chunk(s): {non_silent_count} non-silent and {silent_count} below threshold.",
        )
        return chunks, notes

    def _prepare_chunk_frames(
        self,
        *,
        frames: Any,
        audio_source: MeetingAudioSource,
    ) -> tuple[Any, dict[str, float | bool]]:
        import numpy as np

        processed = np.asarray(frames, dtype=np.float32)
        applied_gain = 1.0
        normalization_gain = 1.0
        silence_threshold = self.silence_threshold

        if audio_source == MeetingAudioSource.MICROPHONE:
            dc_offset = float(np.mean(processed)) if len(processed) else 0.0
            processed = processed - dc_offset
            if self.microphone_highpass_cutoff_hz > 0:
                processed = self._highpass_filter(
                    frames=processed,
                    cutoff_hz=self.microphone_highpass_cutoff_hz,
                )
            processed, trimmed_start_seconds, trimmed_end_seconds = self._trim_silence_edges(
                frames=processed,
                threshold=self.microphone_silence_floor,
                padding_seconds=self.microphone_trim_padding_seconds,
            )
            processed = np.clip(processed * self.microphone_boost_gain, -1.0, 1.0)
            applied_gain = self.microphone_boost_gain
            peak = float(np.max(np.abs(processed))) if len(processed) else 0.0
            if peak > 1e-6 and peak < self.microphone_peak_target:
                normalization_gain = min(self.microphone_peak_target / peak, 4.0)
                processed = np.clip(processed * normalization_gain, -1.0, 1.0)
            processed = self._compress_and_limit(frames=processed)
            silence_threshold = max(self.silence_threshold, self.microphone_silence_floor)
        else:
            dc_offset = 0.0
            trimmed_start_seconds = 0.0
            trimmed_end_seconds = 0.0

        rms = float(np.sqrt(np.mean(np.square(processed), dtype=np.float64))) if len(processed) else 0.0
        peak = float(np.max(np.abs(processed))) if len(processed) else 0.0
        is_silent = rms < silence_threshold
        return processed, {
            "rms": rms,
            "peak": peak,
            "applied_gain": applied_gain,
            "normalization_gain": normalization_gain,
            "compressor_threshold": self.microphone_compressor_threshold if audio_source == MeetingAudioSource.MICROPHONE else 0.0,
            "compressor_ratio": self.microphone_compressor_ratio if audio_source == MeetingAudioSource.MICROPHONE else 1.0,
            "limiter_ceiling": self.microphone_limiter_ceiling if audio_source == MeetingAudioSource.MICROPHONE else 1.0,
            "dc_offset": dc_offset,
            "highpass_cutoff_hz": self.microphone_highpass_cutoff_hz if audio_source == MeetingAudioSource.MICROPHONE else 0.0,
            "trimmed_start_seconds": trimmed_start_seconds,
            "trimmed_end_seconds": trimmed_end_seconds,
            "silence_threshold": silence_threshold,
            "is_silent": is_silent,
        }

    def _compress_and_limit(self, *, frames: Any) -> Any:
        import numpy as np

        if not len(frames):
            return frames
        threshold = self.microphone_compressor_threshold
        ratio = self.microphone_compressor_ratio
        limited = np.asarray(frames, dtype=np.float32).copy()
        magnitude = np.abs(limited)
        above = magnitude > threshold
        if np.any(above):
            compressed_magnitude = threshold + (magnitude[above] - threshold) / ratio
            limited[above] = np.sign(limited[above]) * compressed_magnitude
        return np.clip(limited, -self.microphone_limiter_ceiling, self.microphone_limiter_ceiling)

    def _highpass_filter(self, *, frames: Any, cutoff_hz: float) -> Any:
        import numpy as np

        if len(frames) < 2:
            return frames
        rc = 1.0 / (2.0 * np.pi * cutoff_hz)
        dt = 1.0 / float(self.sample_rate)
        alpha = rc / (rc + dt)
        output = np.empty_like(frames, dtype=np.float32)
        output[0] = frames[0]
        for index in range(1, len(frames)):
            output[index] = alpha * (output[index - 1] + frames[index] - frames[index - 1])
        return output

    def _trim_silence_edges(
        self,
        *,
        frames: Any,
        threshold: float,
        padding_seconds: float,
    ) -> tuple[Any, float, float]:
        import numpy as np

        if not len(frames):
            return frames, 0.0, 0.0
        active_indices = np.flatnonzero(np.abs(frames) >= threshold)
        if not len(active_indices):
            return frames, 0.0, 0.0
        padding_frames = int(round(padding_seconds * self.sample_rate))
        start_index = max(int(active_indices[0]) - padding_frames, 0)
        end_index = min(int(active_indices[-1]) + padding_frames + 1, len(frames))
        trimmed_start_seconds = start_index / self.sample_rate
        trimmed_end_seconds = (len(frames) - end_index) / self.sample_rate
        return frames[start_index:end_index], trimmed_start_seconds, trimmed_end_seconds

    def _resolve_recorder_device(
        self,
        *,
        sc: Any,
        audio_source: MeetingAudioSource,
        device_name: str | None,
    ) -> tuple[Any, str, str]:
        if audio_source == MeetingAudioSource.LOOPBACK:
            speaker = self._resolve_speaker(sc=sc, speaker_name=device_name)
            microphone = sc.get_microphone(id=str(speaker.id), include_loopback=True)
            if microphone is None:
                raise RuntimeError(f"No loopback microphone was found for speaker '{speaker.name}'.")
            return microphone, str(speaker.name), "system output audio"

        microphone = self._resolve_microphone(sc=sc, microphone_name=device_name)
        return microphone, str(microphone.name), "microphone input audio"

    def _resolve_speaker(self, *, sc: Any, speaker_name: str | None) -> Any:
        requested = (speaker_name or self.preferred_speaker_name or "").strip()
        speakers = list(sc.all_speakers())
        if requested:
            lowered = requested.casefold()
            for speaker in speakers:
                if lowered in str(speaker.name).casefold():
                    return speaker
            available = ", ".join(str(speaker.name) for speaker in speakers) or "<none>"
            raise RuntimeError(f"No Windows speaker matched '{requested}'. Available speakers: {available}")
        speaker = sc.default_speaker()
        if speaker is None:
            raise RuntimeError("Windows did not report a default speaker for loopback capture.")
        return speaker

    def _resolve_microphone(self, *, sc: Any, microphone_name: str | None) -> Any:
        requested = (microphone_name or self.preferred_microphone_name or "").strip()
        microphones = list(sc.all_microphones())
        if requested:
            lowered = requested.casefold()
            for microphone in microphones:
                if lowered in str(microphone.name).casefold():
                    return microphone
            available = ", ".join(str(microphone.name) for microphone in microphones) or "<none>"
            raise RuntimeError(f"No Windows microphone matched '{requested}'. Available microphones: {available}")
        microphone = sc.default_microphone()
        if microphone is None:
            raise RuntimeError("Windows did not report a default microphone for input capture.")
        return microphone

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
        audio_source: MeetingAudioSource,
        chunk_index: int,
        wav_bytes: bytes,
        device_name: str,
    ) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_account = re.sub(r"[^A-Za-z0-9_-]+", "_", account_id).strip("_") or "meeting"
        safe_source = re.sub(r"[^A-Za-z0-9_-]+", "_", audio_source.value).strip("_") or "audio"
        safe_device = re.sub(r"[^A-Za-z0-9_-]+", "_", device_name).strip("_") or "device"
        output_path = self.debug_dir / safe_account / safe_source / f"{timestamp}_{safe_device}_chunk_{chunk_index:02d}.wav"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(wav_bytes)
        return output_path

    @staticmethod
    def _platform() -> str:
        import sys

        return sys.platform


WindowsLoopbackAudioCaptureService = WindowsAudioCaptureService
