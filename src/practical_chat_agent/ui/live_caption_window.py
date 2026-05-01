from __future__ import annotations

import difflib
import queue
import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from practical_chat_agent.core.enums import MeetingAudioSource, MeetingExportTemplate
from practical_chat_agent.core.models import (
    MeetingAssistantAdvice,
    MeetingCaptureChunkDebug,
    MeetingMinutesRecord,
    MeetingTranscriptSegment,
)
from practical_chat_agent.services.meeting_assistant import MeetingAssistantService
from practical_chat_agent.services.meeting_live_loop import (
    MeetingLiveLoopRequest,
    MeetingLiveLoopService,
    MeetingLiveLoopUpdate,
)
from practical_chat_agent.services.meeting_minutes_export import MeetingMinutesExportResult, MeetingMinutesExportService


@dataclass(slots=True)
class MeetingAssistantUiUpdate:
    status: str
    advice: MeetingAssistantAdvice | None = None
    error: str | None = None
    message: str = ""


@dataclass(slots=True)
class MeetingMinutesUiUpdate:
    status: str
    result: MeetingMinutesExportResult | None = None
    error: str | None = None
    message: str = ""


class MeetingLiveCaptionWindow:
    """Floating caption window with live transcript and AI copilot suggestions."""

    def __init__(
        self,
        *,
        loop_service: MeetingLiveLoopService,
        assistant_service: MeetingAssistantService | None,
        minutes_export_service: MeetingMinutesExportService,
        initial_request: MeetingLiveLoopRequest,
        geometry: str = "1080x720+80+80",
        transcript_limit: int = 120,
        window_alpha: float = 0.92,
        assistant_enabled: bool = True,
    ) -> None:
        self.loop_service = loop_service
        self.assistant_service = assistant_service
        self.minutes_export_service = minutes_export_service
        self.initial_request = initial_request
        self.geometry = geometry
        self.transcript_limit = max(int(transcript_limit), 20)
        self.window_alpha = min(max(float(window_alpha), 0.55), 1.0)
        self.assistant_enabled_default = assistant_enabled
        self._queue: queue.Queue[
            MeetingLiveLoopUpdate | MeetingAssistantUiUpdate | MeetingMinutesUiUpdate
        ] = queue.Queue()
        self._worker_thread: threading.Thread | None = None
        self._assistant_thread: threading.Thread | None = None
        self._stop_event: threading.Event | None = None
        self._transcript_lines: list[str] = []
        self._segment_history: list[MeetingTranscriptSegment] = []
        self._assistant_refresh_pending = False
        self._minutes_thread: threading.Thread | None = None
        self._current_session_id: str | None = None
        self._current_meeting_title = initial_request.meeting_hint or "Tencent Meeting"
        self._default_minutes_export_dir = Path("exports") / "live_window"
        self._minutes_history: list[MeetingMinutesRecord] = []
        self._minutes_history_session_id: str | None = None
        self._minutes_history_window = None
        self._minutes_history_listbox = None
        self._minutes_history_viewer = None
        self._minutes_history_context_var = None
        self._minutes_history_selection_var = None
        self._build_ui()

    def run(self) -> None:
        self.root.after(150, self._drain_updates)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _build_ui(self) -> None:
        try:
            import tkinter as tk
            from tkinter import filedialog, messagebox, scrolledtext, ttk
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Tkinter is unavailable on this system: {exc}") from exc

        self._tk = tk
        self._ttk = ttk
        self._filedialog = filedialog
        self._messagebox = messagebox
        self._scrolledtext = scrolledtext
        self.root = tk.Tk()
        self.root.title("Practical Chat Agent Meeting Copilot")
        self.root.geometry(self.geometry)
        self.root.minsize(860, 560)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", self.window_alpha)
        self.root.configure(bg="#020617")

        self.source_var = tk.StringVar(value=self.initial_request.audio_source.value)
        self.device_name_var = tk.StringVar(value=self.initial_request.device_name or "")
        self.save_capture_var = tk.BooleanVar(value=self.initial_request.save_capture)
        self.assistant_enabled_var = tk.BooleanVar(
            value=bool(self.assistant_enabled_default and self.assistant_service is not None),
        )
        self.status_var = tk.StringVar(value="Ready. Click Start to begin live transcription.")
        self.meeting_var = tk.StringVar(value=self._current_meeting_title)
        self.debug_var = tk.StringVar(value="No chunks yet.")
        self.caption_var = tk.StringVar(value="实时字幕会显示在这里")
        self.assistant_status_var = tk.StringVar(value=self._initial_assistant_status())
        self.assistant_backend_var = tk.StringVar(value=self._assistant_backend_label())
        self.summary_var = tk.StringVar(value="等待实时转写内容进入上下文。")
        self.reply_var = tk.StringVar(value="等出现更明确的讨论点后，我会给出一句可直接开口的话。")
        self.key_points_var = tk.StringVar(value="• 暂无")
        self.follow_up_var = tk.StringVar(value="• 暂无")
        self.action_items_var = tk.StringVar(value="• 暂无")
        self.minutes_status_var = tk.StringVar(value="纪要尚未导出。")
        self.alpha_var = tk.DoubleVar(value=self.window_alpha)
        self.minutes_template_var = tk.StringVar(value=MeetingExportTemplate.STANDARD.value)
        self.minutes_export_dir_var = tk.StringVar(value=str(self._default_minutes_export_dir))

        container = tk.Frame(self.root, bg="#020617", padx=14, pady=14)
        container.pack(fill="both", expand=True)

        header = tk.Frame(container, bg="#0f172a", padx=14, pady=12, highlightbackground="#1e293b", highlightthickness=1)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Meeting Copilot",
            font=("Microsoft YaHei UI", 16, "bold"),
            fg="#f8fafc",
            bg="#0f172a",
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            header,
            text=f"account: {self.initial_request.account_id}",
            font=("Consolas", 10),
            fg="#93c5fd",
            bg="#0f172a",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))
        tk.Label(
            header,
            textvariable=self.meeting_var,
            font=("Microsoft YaHei UI", 10),
            fg="#cbd5e1",
            bg="#0f172a",
        ).grid(row=2, column=0, sticky="w", pady=(4, 0))
        tk.Label(
            header,
            textvariable=self.assistant_backend_var,
            font=("Consolas", 10),
            fg="#86efac",
            bg="#0f172a",
        ).grid(row=0, column=1, sticky="e")
        header.grid_columnconfigure(0, weight=1)

        controls = tk.Frame(container, bg="#020617", pady=10)
        controls.pack(fill="x")

        ttk.Label(controls, text="Source").grid(row=0, column=0, sticky="w")
        self.source_combo = ttk.Combobox(
            controls,
            textvariable=self.source_var,
            values=[item.value for item in MeetingAudioSource],
            width=14,
            state="readonly",
        )
        self.source_combo.grid(row=0, column=1, padx=(6, 12), sticky="w")

        ttk.Label(controls, text="Device").grid(row=0, column=2, sticky="w")
        self.device_entry = ttk.Entry(controls, textvariable=self.device_name_var, width=28)
        self.device_entry.grid(row=0, column=3, padx=(6, 12), sticky="ew")

        self.save_capture_check = ttk.Checkbutton(
            controls,
            text="Save WAV chunks",
            variable=self.save_capture_var,
        )
        self.save_capture_check.grid(row=0, column=4, sticky="w")

        self.assistant_check = ttk.Checkbutton(
            controls,
            text="AI Copilot",
            variable=self.assistant_enabled_var,
        )
        self.assistant_check.grid(row=0, column=5, padx=(12, 0), sticky="w")

        self.start_button = ttk.Button(controls, text="Start", command=self._start_loop)
        self.start_button.grid(row=0, column=6, padx=(12, 6))
        self.stop_button = ttk.Button(controls, text="Stop", command=self._stop_loop, state="disabled")
        self.stop_button.grid(row=0, column=7, padx=(0, 6))
        self.clear_button = ttk.Button(controls, text="Clear", command=self._clear_transcript)
        self.clear_button.grid(row=0, column=8, padx=(0, 6))
        self.refresh_assistant_button = ttk.Button(controls, text="Refresh Advice", command=self._trigger_assistant_refresh)
        self.refresh_assistant_button.grid(row=0, column=9)
        self.export_minutes_button = ttk.Button(controls, text="Export Minutes", command=self._trigger_minutes_export)
        self.export_minutes_button.grid(row=0, column=10, padx=(6, 0))

        ttk.Label(controls, text="Minutes").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.minutes_template_combo = ttk.Combobox(
            controls,
            textvariable=self.minutes_template_var,
            values=[item.value for item in MeetingExportTemplate],
            width=14,
            state="readonly",
        )
        self.minutes_template_combo.grid(row=1, column=1, padx=(6, 12), pady=(10, 0), sticky="w")

        ttk.Label(controls, text="Export Dir").grid(row=1, column=2, sticky="w", pady=(10, 0))
        self.minutes_export_dir_entry = ttk.Entry(controls, textvariable=self.minutes_export_dir_var, width=28)
        self.minutes_export_dir_entry.grid(row=1, column=3, padx=(6, 12), pady=(10, 0), sticky="ew")
        self.minutes_export_dir_button = ttk.Button(controls, text="Browse", command=self._browse_minutes_export_directory)
        self.minutes_export_dir_button.grid(row=1, column=4, pady=(10, 0), sticky="w")
        self.view_latest_minutes_button = ttk.Button(controls, text="Latest Minutes", command=self._open_latest_minutes)
        self.view_latest_minutes_button.grid(row=1, column=5, padx=(12, 6), pady=(10, 0), sticky="w")
        self.diff_previous_minutes_button = ttk.Button(controls, text="Diff Prev", command=self._open_previous_minutes_diff)
        self.diff_previous_minutes_button.grid(row=1, column=6, pady=(10, 0), sticky="w")
        controls.grid_columnconfigure(3, weight=1)
        self._update_minutes_action_state()

        alpha_row = tk.Frame(container, bg="#020617")
        alpha_row.pack(fill="x", pady=(0, 10))
        ttk.Label(alpha_row, text="Opacity").pack(side="left")
        self.alpha_scale = ttk.Scale(
            alpha_row,
            from_=0.55,
            to=1.0,
            variable=self.alpha_var,
            command=self._update_alpha,
        )
        self.alpha_scale.pack(side="left", fill="x", expand=True, padx=(10, 10))
        self.alpha_label = ttk.Label(alpha_row, text=f"{self.window_alpha:.2f}")
        self.alpha_label.pack(side="left")

        caption_frame = tk.Frame(
            container,
            bg="#111827",
            padx=16,
            pady=14,
            highlightbackground="#38bdf8",
            highlightthickness=1,
        )
        caption_frame.pack(fill="x", pady=(0, 10))
        tk.Label(
            caption_frame,
            text="Live Caption Bar",
            font=("Microsoft YaHei UI", 10, "bold"),
            fg="#7dd3fc",
            bg="#111827",
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            caption_frame,
            textvariable=self.caption_var,
            font=("Microsoft YaHei UI", 16, "bold"),
            fg="#f8fafc",
            bg="#111827",
            anchor="w",
            justify="left",
            wraplength=980,
        ).pack(fill="x", pady=(8, 0))

        status_frame = tk.Frame(container, bg="#1e293b", padx=10, pady=10, highlightbackground="#334155", highlightthickness=1)
        status_frame.pack(fill="x", pady=(0, 10))
        tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Microsoft YaHei UI", 10),
            fg="#e2e8f0",
            bg="#1e293b",
            anchor="w",
            justify="left",
        ).pack(fill="x")

        body = tk.PanedWindow(container, orient="horizontal", sashrelief="flat", bg="#020617")
        body.pack(fill="both", expand=True)

        transcript_panel = tk.Frame(body, bg="#020617")
        assistant_panel = tk.Frame(body, bg="#020617")
        body.add(transcript_panel, stretch="always", minsize=420)
        body.add(assistant_panel, stretch="always", minsize=320)

        transcript_card = tk.Frame(
            transcript_panel,
            bg="#020617",
            highlightbackground="#334155",
            highlightthickness=1,
        )
        transcript_card.pack(fill="both", expand=True, padx=(0, 8))
        tk.Label(
            transcript_card,
            text="Transcript Stream",
            font=("Microsoft YaHei UI", 11, "bold"),
            fg="#e2e8f0",
            bg="#020617",
            anchor="w",
            padx=12,
            pady=10,
        ).pack(fill="x")

        transcript_frame = tk.Frame(transcript_card, bg="#020617")
        transcript_frame.pack(fill="both", expand=True)
        self.transcript_text = tk.Text(
            transcript_frame,
            wrap="word",
            bg="#020617",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            relief="flat",
            padx=12,
            pady=12,
            font=("Microsoft YaHei UI", 12),
        )
        self.transcript_text.pack(side="left", fill="both", expand=True)
        self.transcript_text.configure(state="disabled")
        transcript_scrollbar = ttk.Scrollbar(transcript_frame, orient="vertical", command=self.transcript_text.yview)
        transcript_scrollbar.pack(side="right", fill="y")
        self.transcript_text.configure(yscrollcommand=transcript_scrollbar.set)

        assistant_card = tk.Frame(
            assistant_panel,
            bg="#0b1120",
            highlightbackground="#334155",
            highlightthickness=1,
            padx=12,
            pady=12,
        )
        assistant_card.pack(fill="both", expand=True)
        tk.Label(
            assistant_card,
            text="AI Copilot Suggestions",
            font=("Microsoft YaHei UI", 11, "bold"),
            fg="#f8fafc",
            bg="#0b1120",
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            assistant_card,
            textvariable=self.assistant_status_var,
            font=("Consolas", 9),
            fg="#86efac",
            bg="#0b1120",
            anchor="w",
            justify="left",
        ).pack(fill="x", pady=(6, 10))

        self._build_info_block(assistant_card, title="Summary", textvariable=self.summary_var)
        self._build_info_block(assistant_card, title="Suggested Reply", textvariable=self.reply_var)
        self._build_info_block(assistant_card, title="Key Points", textvariable=self.key_points_var)
        self._build_info_block(assistant_card, title="Follow-up Questions", textvariable=self.follow_up_var)
        self._build_info_block(assistant_card, title="Action Items", textvariable=self.action_items_var)
        self._build_info_block(assistant_card, title="Minutes Export", textvariable=self.minutes_status_var)

        footer = tk.Frame(container, bg="#020617", pady=10)
        footer.pack(fill="x")
        tk.Label(
            footer,
            text="Latest chunk debug",
            font=("Microsoft YaHei UI", 10, "bold"),
            fg="#e2e8f0",
            bg="#020617",
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            footer,
            textvariable=self.debug_var,
            font=("Consolas", 9),
            fg="#94a3b8",
            bg="#020617",
            anchor="w",
            justify="left",
        ).pack(fill="x", pady=(4, 0))

    def _build_info_block(self, parent: object, *, title: str, textvariable: object) -> None:
        block = self._tk.Frame(parent, bg="#0b1120", highlightbackground="#1e293b", highlightthickness=1, padx=10, pady=8)
        block.pack(fill="x", pady=(0, 8))
        self._tk.Label(
            block,
            text=title,
            font=("Microsoft YaHei UI", 10, "bold"),
            fg="#7dd3fc",
            bg="#0b1120",
            anchor="w",
        ).pack(fill="x")
        self._tk.Label(
            block,
            textvariable=textvariable,
            font=("Microsoft YaHei UI", 10),
            fg="#e2e8f0",
            bg="#0b1120",
            anchor="w",
            justify="left",
            wraplength=320,
        ).pack(fill="x", pady=(6, 0))

    def _start_loop(self) -> None:
        if self._worker_thread is not None and self._worker_thread.is_alive():
            return

        self._stop_event = threading.Event()
        request = MeetingLiveLoopRequest(
            connector_name=self.initial_request.connector_name,
            account_id=self.initial_request.account_id,
            meeting_hint=self.initial_request.meeting_hint,
            agent_id=self.initial_request.agent_id,
            audio_source=MeetingAudioSource(self.source_var.get()),
            capture_seconds=self.initial_request.capture_seconds,
            chunk_seconds=self.initial_request.chunk_seconds,
            save_capture=bool(self.save_capture_var.get()),
            device_name=(self.device_name_var.get().strip() or None),
            cooldown_seconds=self.initial_request.cooldown_seconds,
        )
        self.status_var.set("Starting live transcription loop...")
        self.assistant_status_var.set("Assistant standing by.")
        self._set_running_state(is_running=True)
        self._worker_thread = threading.Thread(
            target=self.loop_service.run_forever,
            kwargs={
                "request": request,
                "on_update": self._queue.put,
                "stop_event": self._stop_event,
            },
            daemon=True,
        )
        self._worker_thread.start()

    def _stop_loop(self) -> None:
        if self._stop_event is not None:
            self._stop_event.set()
        self.status_var.set("Stopping after the current capture cycle finishes...")

    def _clear_transcript(self) -> None:
        self._transcript_lines.clear()
        self._segment_history.clear()
        self.transcript_text.configure(state="normal")
        self.transcript_text.delete("1.0", "end")
        self.transcript_text.configure(state="disabled")
        self.caption_var.set("实时字幕会显示在这里")
        self.summary_var.set("等待实时转写内容进入上下文。")
        self.reply_var.set("等出现更明确的讨论点后，我会给出一句可直接开口的话。")
        self.key_points_var.set("• 暂无")
        self.follow_up_var.set("• 暂无")
        self.action_items_var.set("• 暂无")
        self.assistant_status_var.set(self._initial_assistant_status())

    def _drain_updates(self) -> None:
        processed_any = False
        while True:
            try:
                update = self._queue.get_nowait()
            except queue.Empty:
                break
            processed_any = True
            self._handle_update(update)

        if processed_any and self._worker_thread is not None and not self._worker_thread.is_alive():
            self._set_running_state(is_running=False)
        self.root.after(150, self._drain_updates)

    def _handle_update(self, update: MeetingLiveLoopUpdate | MeetingAssistantUiUpdate | MeetingMinutesUiUpdate) -> None:
        if isinstance(update, MeetingAssistantUiUpdate):
            self._handle_assistant_update(update)
            return
        if isinstance(update, MeetingMinutesUiUpdate):
            self._handle_minutes_update(update)
            return
        self._handle_loop_update(update)

    def _handle_loop_update(self, update: MeetingLiveLoopUpdate) -> None:
        if update.preview is not None and update.preview.meeting_title:
            self._current_meeting_title = update.preview.meeting_title
            self.meeting_var.set(update.preview.meeting_title)
        if update.preview is not None and update.preview.meeting_session_id:
            if self._current_session_id != update.preview.meeting_session_id:
                self._current_session_id = update.preview.meeting_session_id
                self._minutes_history = []
                self._minutes_history_session_id = None
                self._refresh_minutes_history()
            self.export_minutes_button.configure(state="normal")

        if update.new_segments:
            for segment in update.new_segments:
                self._segment_history.append(segment)
                self._append_segment(segment)
            self._refresh_caption_bar()
            self._trigger_assistant_refresh()

        if update.latest_chunk is not None:
            self.debug_var.set(self._format_chunk_debug(update.latest_chunk))

        prefix = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"[{prefix}] {update.message or update.status}")
        if update.status in {"error", "stopped"}:
            self._set_running_state(is_running=False)
            if update.status == "error":
                self._append_system_line(f"[error] {update.error or update.message}")

    def _handle_assistant_update(self, update: MeetingAssistantUiUpdate) -> None:
        if update.status == "working":
            self.assistant_status_var.set(update.message or "AI 正在分析最近几条转写…")
            return
        if update.status == "error":
            self.assistant_status_var.set(update.error or "AI 分析失败，稍后可以再试。")
            return

        advice = update.advice
        if advice is None:
            return
        backend_detail = advice.backend
        if advice.model:
            backend_detail = f"{backend_detail} / {advice.model}"
        self.assistant_backend_var.set(f"assistant_backend: {backend_detail}")
        self.assistant_status_var.set(update.message or f"建议已更新，status={advice.status}")
        self.summary_var.set(advice.summary or "暂无摘要")
        self.reply_var.set(advice.suggested_reply or "暂无建议")
        self.key_points_var.set(self._format_bullets(advice.key_points))
        self.follow_up_var.set(self._format_bullets(advice.follow_up_questions))
        self.action_items_var.set(self._format_bullets(advice.action_items))
        if self._assistant_refresh_pending:
            self._assistant_refresh_pending = False

    def _handle_minutes_update(self, update: MeetingMinutesUiUpdate) -> None:
        if update.status == "working":
            self.minutes_status_var.set(update.message or "正在生成会议纪要…")
            return
        if update.status == "error":
            self.minutes_status_var.set(update.error or "纪要导出失败。")
            return
        if update.result is None:
            return
        self.minutes_status_var.set(
            update.message
            or (
                f"已导出 {update.result.draft.template.value} 纪要，"
                f"版本={update.result.record.minutes_id}，文件={update.result.output_path.name}"
            ),
        )
        self.minutes_export_dir_var.set(str(update.result.output_path.parent))
        self._refresh_minutes_history(force=True)

    def _append_segment(self, segment: MeetingTranscriptSegment) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        speaker = f"{segment.speaker_name}: " if segment.speaker_name else ""
        prefix = segment.display_time or timestamp
        line = f"[{prefix}] {speaker}{segment.text.strip()}"
        self._append_line(line)

    def _append_system_line(self, text: str) -> None:
        self._append_line(text)

    def _append_line(self, line: str) -> None:
        cleaned = line.strip()
        if not cleaned:
            return
        self._transcript_lines.append(cleaned)
        if len(self._transcript_lines) > self.transcript_limit:
            self._transcript_lines = self._transcript_lines[-self.transcript_limit :]

        self.transcript_text.configure(state="normal")
        self.transcript_text.delete("1.0", "end")
        self.transcript_text.insert("end", "\n\n".join(self._transcript_lines))
        self.transcript_text.see("end")
        self.transcript_text.configure(state="disabled")

    def _refresh_caption_bar(self) -> None:
        if not self._segment_history:
            self.caption_var.set("实时字幕会显示在这里")
            return
        recent_segments = self._segment_history[-2:]
        rendered = []
        for segment in recent_segments:
            speaker = f"{segment.speaker_name}: " if segment.speaker_name else ""
            rendered.append(f"{speaker}{segment.text.strip()}")
        self.caption_var.set("\n".join(rendered))

    def _trigger_assistant_refresh(self) -> None:
        if not self.assistant_enabled_var.get():
            self.assistant_status_var.set("AI Copilot 已关闭。")
            return
        if self.assistant_service is None:
            self.assistant_status_var.set("未配置会议辅助服务。")
            return
        if not self._segment_history:
            self.assistant_status_var.set("等待转写内容后再生成建议。")
            return
        if self._assistant_thread is not None and self._assistant_thread.is_alive():
            self._assistant_refresh_pending = True
            return

        self._assistant_refresh_pending = False
        snapshot = list(self._segment_history[-self.assistant_service.context_segments :])
        meeting_title = self._current_meeting_title
        self._queue.put(MeetingAssistantUiUpdate(status="working", message="AI 正在分析最近几条转写…"))
        self._assistant_thread = threading.Thread(
            target=self._run_assistant_worker,
            kwargs={
                "meeting_title": meeting_title,
                "segments": snapshot,
            },
            daemon=True,
        )
        self._assistant_thread.start()

    def _trigger_minutes_export(self) -> None:
        if self._minutes_thread is not None and self._minutes_thread.is_alive():
            self.minutes_status_var.set("纪要仍在生成中，请稍候。")
            return
        if not self._current_session_id:
            self.minutes_status_var.set("尚未拿到当前会议 session，先开始一次实时转写。")
            return
        self._queue.put(MeetingMinutesUiUpdate(status="working", message="正在生成会议纪要…"))
        self._minutes_thread = threading.Thread(
            target=self._run_minutes_export_worker,
            kwargs={
                "session_id": self._current_session_id,
                "template": self._selected_minutes_template(),
                "output_dir": self._selected_minutes_output_dir(),
            },
            daemon=True,
        )
        self._minutes_thread.start()

    def _run_minutes_export_worker(
        self,
        *,
        session_id: str,
        template: MeetingExportTemplate,
        output_dir: Path,
    ) -> None:
        try:
            session_record = self.minutes_export_service.meeting_repository.get_session(session_id=session_id)
            if session_record is None:
                raise RuntimeError(f"Unknown meeting session: {session_id}")
            segments = self.minutes_export_service.meeting_repository.list_segments(session_id=session_id)
            output_path = output_dir / f"{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            result = self.minutes_export_service.export_minutes(
                session_record=session_record,
                segments=segments,
                template=template,
                output_path=output_path,
            )
        except Exception as exc:  # noqa: BLE001
            self._queue.put(
                MeetingMinutesUiUpdate(
                    status="error",
                    error=str(exc),
                    message="会议纪要导出失败。",
                ),
            )
            return
        self._queue.put(
            MeetingMinutesUiUpdate(
                status="done",
                result=result,
                message=f"纪要已导出到 {result.output_path}",
            ),
        )

    def _run_assistant_worker(
        self,
        *,
        meeting_title: str | None,
        segments: list[MeetingTranscriptSegment],
    ) -> None:
        assert self.assistant_service is not None
        try:
            advice = self.assistant_service.generate_advice(
                meeting_title=meeting_title,
                transcript_segments=segments,
            )
        except Exception as exc:  # noqa: BLE001
            self._queue.put(
                MeetingAssistantUiUpdate(
                    status="error",
                    error=str(exc),
                    message="AI 建议生成失败。",
                ),
            )
            return
        self._queue.put(
            MeetingAssistantUiUpdate(
                status="done",
                advice=advice,
                message=f"建议已更新，来源={advice.backend}",
            ),
        )

    @staticmethod
    def _format_chunk_debug(chunk: MeetingCaptureChunkDebug) -> str:
        return (
            f"chunk={chunk.chunk_index:02d}  "
            f"source={chunk.audio_source.value}  "
            f"rms={chunk.rms:.6f}  "
            f"peak={(chunk.peak if chunk.peak is not None else 0.0):.6f}  "
            f"duration={chunk.duration_seconds:.2f}s  "
            f"silent={'yes' if chunk.is_silent else 'no'}  "
            f"retry={chunk.transcription_retry_count}  "
            f"strategy={chunk.transcription_retry_strategy or '-'}  "
            f"status={chunk.transcription_status or '-'}  "
            f"path={chunk.saved_path or '<not saved>'}"
        )

    @staticmethod
    def _format_bullets(lines: list[str]) -> str:
        cleaned = [line.strip() for line in lines if line.strip()]
        if not cleaned:
            return "• 暂无"
        return "\n".join(f"• {line}" for line in cleaned[:3])

    def _browse_minutes_export_directory(self) -> None:
        selected = self._filedialog.askdirectory(
            parent=self.root,
            mustexist=False,
            initialdir=self.minutes_export_dir_var.get().strip() or str(self._default_minutes_export_dir),
            title="选择会议纪要导出目录",
        )
        if selected:
            self.minutes_export_dir_var.set(selected)

    def _refresh_minutes_history(self, *, force: bool = False) -> None:
        if not self._current_session_id:
            self._minutes_history = []
            self._minutes_history_session_id = None
            self._update_minutes_action_state()
            return
        if (
            self._minutes_history
            and not force
            and self._minutes_history_session_id == self._current_session_id
        ):
            self._update_minutes_action_state()
            return
        try:
            self._minutes_history = self.minutes_export_service.meeting_repository.list_minutes(
                session_id=self._current_session_id,
                limit=10,
            )
            self._minutes_history_session_id = self._current_session_id
        except Exception as exc:  # noqa: BLE001
            self._minutes_history = []
            self._minutes_history_session_id = None
            self.minutes_status_var.set(f"加载纪要历史失败: {exc}")
        self._update_minutes_action_state()

    def _update_minutes_action_state(self) -> None:
        has_session = bool(self._current_session_id)
        latest_state = "normal" if has_session and self._minutes_history else "disabled"
        diff_state = "normal" if has_session and len(self._minutes_history) >= 2 else "disabled"
        self.view_latest_minutes_button.configure(state=latest_state)
        self.diff_previous_minutes_button.configure(state=diff_state)

    def _open_latest_minutes(self) -> None:
        self._refresh_minutes_history(force=True)
        if not self._minutes_history:
            self._messagebox.showinfo("Latest Minutes", "当前会话还没有可查看的纪要版本。", parent=self.root)
            return
        self._open_minutes_history_panel(mode="latest")

    def _open_previous_minutes_diff(self) -> None:
        self._refresh_minutes_history(force=True)
        if len(self._minutes_history) < 2:
            self._messagebox.showinfo("Minutes Diff", "至少需要两个纪要版本才能进行对比。", parent=self.root)
            return
        self._open_minutes_history_panel(mode="diff_latest_two")

    def _render_minutes_record_text(self, record: MeetingMinutesRecord) -> str:
        lines = [
            f"# Minutes Version: {record.title or record.minutes_id}",
            "",
            "## Metadata",
            "",
            f"- Minutes ID: {record.minutes_id}",
            f"- Session ID: {record.session_id}",
            f"- Template: {record.template.value}",
            f"- Backend: {record.backend}",
            f"- Model: {record.model or 'fallback'}",
            f"- Status: {record.status}",
            f"- Output Path: {record.output_path or 'not_saved'}",
            f"- Created At: {record.created_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %z')}",
            "",
            "## Markdown Body",
            "",
            record.markdown_body,
        ]
        return "\n".join(lines)

    def _open_minutes_history_panel(self, *, mode: str = "latest") -> None:
        self._refresh_minutes_history(force=True)
        if not self._minutes_history:
            self._messagebox.showinfo("Minutes History", "当前会话还没有可查看的纪要版本。", parent=self.root)
            return

        if self._minutes_history_window is not None and self._minutes_history_window.winfo_exists():
            window = self._minutes_history_window
            window.deiconify()
            window.lift()
            window.focus_force()
        else:
            window = self._tk.Toplevel(self.root)
            window.title("Meeting Minutes History")
            window.geometry("1240x820+100+100")
            window.minsize(940, 560)
            window.attributes("-topmost", True)
            window.configure(bg="#020617")
            window.protocol("WM_DELETE_WINDOW", self._close_minutes_history_panel)
            self._minutes_history_window = window

            frame = self._tk.Frame(window, bg="#020617", padx=12, pady=12)
            frame.pack(fill="both", expand=True)

            header = self._tk.Frame(frame, bg="#020617")
            header.pack(fill="x", pady=(0, 10))
            self._tk.Label(
                header,
                text="Meeting Minutes History",
                font=("Microsoft YaHei UI", 12, "bold"),
                fg="#e2e8f0",
                bg="#020617",
                anchor="w",
            ).pack(side="left")

            self._minutes_history_context_var = self._tk.StringVar(value="")
            self._minutes_history_selection_var = self._tk.StringVar(value="")
            self._tk.Label(
                header,
                textvariable=self._minutes_history_context_var,
                font=("Consolas", 9),
                fg="#94a3b8",
                bg="#020617",
                anchor="e",
            ).pack(side="right")

            toolbar = self._tk.Frame(frame, bg="#020617")
            toolbar.pack(fill="x", pady=(0, 10))
            self._tk.Button(
                toolbar,
                text="Refresh",
                command=lambda: self._refresh_minutes_history_panel(force=True),
                bg="#1e293b",
                fg="#e2e8f0",
                activebackground="#334155",
                activeforeground="#f8fafc",
                relief="flat",
                padx=10,
                pady=6,
            ).pack(side="left")
            self._tk.Button(
                toolbar,
                text="View Selected",
                command=self._show_selected_minutes_version,
                bg="#0f766e",
                fg="#ecfeff",
                activebackground="#115e59",
                activeforeground="#f0fdfa",
                relief="flat",
                padx=10,
                pady=6,
            ).pack(side="left", padx=(8, 0))
            self._tk.Button(
                toolbar,
                text="Diff Selected",
                command=self._show_selected_minutes_diff,
                bg="#1d4ed8",
                fg="#eff6ff",
                activebackground="#1e40af",
                activeforeground="#dbeafe",
                relief="flat",
                padx=10,
                pady=6,
            ).pack(side="left", padx=(8, 0))
            self._tk.Label(
                toolbar,
                textvariable=self._minutes_history_selection_var,
                font=("Microsoft YaHei UI", 9),
                fg="#cbd5e1",
                bg="#020617",
                anchor="w",
            ).pack(side="left", padx=(12, 0))

            body = self._tk.PanedWindow(frame, orient="horizontal", sashrelief="flat", bg="#020617")
            body.pack(fill="both", expand=True)

            list_card = self._tk.Frame(
                body,
                bg="#0b1120",
                highlightbackground="#334155",
                highlightthickness=1,
                padx=10,
                pady=10,
            )
            body.add(list_card, minsize=280)

            self._tk.Label(
                list_card,
                text="Versions",
                font=("Microsoft YaHei UI", 10, "bold"),
                fg="#7dd3fc",
                bg="#0b1120",
                anchor="w",
            ).pack(fill="x", pady=(0, 8))

            listbox = self._tk.Listbox(
                list_card,
                bg="#020617",
                fg="#f8fafc",
                selectmode="extended",
                exportselection=False,
                activestyle="dotbox",
                relief="flat",
                font=("Consolas", 9),
            )
            listbox.pack(side="left", fill="both", expand=True)
            scrollbar = self._ttk.Scrollbar(list_card, orient="vertical", command=listbox.yview)
            scrollbar.pack(side="right", fill="y")
            listbox.configure(yscrollcommand=scrollbar.set)
            listbox.bind("<<ListboxSelect>>", self._on_minutes_history_selection_change)
            listbox.bind("<Double-Button-1>", lambda _event: self._show_selected_minutes_version())
            self._minutes_history_listbox = listbox

            viewer_card = self._tk.Frame(
                body,
                bg="#0b1120",
                highlightbackground="#334155",
                highlightthickness=1,
                padx=10,
                pady=10,
            )
            body.add(viewer_card, minsize=540)

            self._tk.Label(
                viewer_card,
                text="Preview",
                font=("Microsoft YaHei UI", 10, "bold"),
                fg="#7dd3fc",
                bg="#0b1120",
                anchor="w",
            ).pack(fill="x", pady=(0, 8))

            viewer = self._scrolledtext.ScrolledText(
                viewer_card,
                wrap="word",
                bg="#020617",
                fg="#f8fafc",
                insertbackground="#f8fafc",
                relief="flat",
                padx=12,
                pady=12,
                font=("Consolas", 10),
            )
            viewer.pack(fill="both", expand=True)
            viewer.configure(state="disabled")
            self._minutes_history_viewer = viewer

        self._refresh_minutes_history_panel(force=False)
        if mode == "diff_latest_two":
            self._select_minutes_history_indices([0, 1])
            self._show_selected_minutes_diff()
        else:
            self._select_minutes_history_indices([0])
            self._show_selected_minutes_version()

    def _close_minutes_history_panel(self) -> None:
        if self._minutes_history_window is not None and self._minutes_history_window.winfo_exists():
            self._minutes_history_window.destroy()
        self._minutes_history_window = None
        self._minutes_history_listbox = None
        self._minutes_history_viewer = None
        self._minutes_history_context_var = None
        self._minutes_history_selection_var = None

    def _refresh_minutes_history_panel(self, *, force: bool) -> None:
        self._refresh_minutes_history(force=force)
        if self._minutes_history_window is None or not self._minutes_history_window.winfo_exists():
            return
        if self._minutes_history_context_var is not None:
            count = len(self._minutes_history)
            session_text = self._current_session_id or "unknown"
            self._minutes_history_context_var.set(f"session={session_text}  versions={count}")
        if self._minutes_history_listbox is None:
            return

        selected_ids = self._selected_minutes_ids_from_listbox()
        self._minutes_history_listbox.delete(0, "end")
        for record in self._minutes_history:
            display = self._format_minutes_history_item(record)
            self._minutes_history_listbox.insert("end", display)

        if selected_ids:
            indices = [
                index
                for index, record in enumerate(self._minutes_history)
                if record.minutes_id in selected_ids
            ]
            self._select_minutes_history_indices(indices or [0])
        elif self._minutes_history:
            self._select_minutes_history_indices([0])
        else:
            self._update_minutes_history_selection_label([])
            self._set_minutes_history_viewer_text("当前没有可展示的纪要版本。")

    def _format_minutes_history_item(self, record: MeetingMinutesRecord) -> str:
        created_at = record.created_at.astimezone().strftime("%m-%d %H:%M:%S")
        title = (record.title or record.minutes_id).replace("\n", " ").strip()
        if len(title) > 42:
            title = f"{title[:39].rstrip()}..."
        return f"{created_at} | {record.template.value:<8} | {record.status:<6} | {title}"

    def _select_minutes_history_indices(self, indices: list[int]) -> None:
        if self._minutes_history_listbox is None:
            return
        self._minutes_history_listbox.selection_clear(0, "end")
        valid_indices = [index for index in indices if 0 <= index < len(self._minutes_history)]
        for index in valid_indices:
            self._minutes_history_listbox.selection_set(index)
        if valid_indices:
            self._minutes_history_listbox.see(valid_indices[0])
        self._update_minutes_history_selection_label(valid_indices)

    def _selected_minutes_ids_from_listbox(self) -> list[str]:
        if self._minutes_history_listbox is None:
            return []
        indices = [int(value) for value in self._minutes_history_listbox.curselection()]
        return [
            self._minutes_history[index].minutes_id
            for index in indices
            if 0 <= index < len(self._minutes_history)
        ]

    def _selected_minutes_records(self) -> list[MeetingMinutesRecord]:
        if self._minutes_history_listbox is None:
            return []
        indices = [int(value) for value in self._minutes_history_listbox.curselection()]
        self._update_minutes_history_selection_label(indices)
        return [
            self._minutes_history[index]
            for index in indices
            if 0 <= index < len(self._minutes_history)
        ]

    def _update_minutes_history_selection_label(self, indices: list[int]) -> None:
        if self._minutes_history_selection_var is None:
            return
        if not indices:
            self._minutes_history_selection_var.set("未选择版本")
            return
        records = [
            self._minutes_history[index]
            for index in indices
            if 0 <= index < len(self._minutes_history)
        ]
        if not records:
            self._minutes_history_selection_var.set("未选择版本")
            return
        labels = [record.minutes_id for record in records[:2]]
        suffix = f" (+{len(records) - 2})" if len(records) > 2 else ""
        self._minutes_history_selection_var.set(f"selected={', '.join(labels)}{suffix}")

    def _on_minutes_history_selection_change(self, _event: object = None) -> None:
        records = self._selected_minutes_records()
        if not records:
            self._set_minutes_history_viewer_text("请选择左侧一个或两个纪要版本。")
            return
        if len(records) == 1:
            self._set_minutes_history_viewer_text(self._render_minutes_record_text(records[0]))
            return
        if len(records) > 2:
            preview = self._render_minutes_diff_text(records[:2])
            preview += "\n\n[Info] 当前选中了超过 2 个版本，预览仅展示前两个选中版本的 diff。"
            self._set_minutes_history_viewer_text(preview)
            return
        self._set_minutes_history_viewer_text(self._render_minutes_diff_text(records[:2]))

    def _show_selected_minutes_version(self) -> None:
        records = self._selected_minutes_records()
        if not records:
            self._messagebox.showinfo("Minutes History", "请先选择一个纪要版本。", parent=self._minutes_history_window or self.root)
            return
        self._set_minutes_history_viewer_text(self._render_minutes_record_text(records[0]))

    def _show_selected_minutes_diff(self) -> None:
        records = self._selected_minutes_records()
        if len(records) < 2:
            self._messagebox.showinfo("Minutes History", "请至少选择两个纪要版本进行对比。", parent=self._minutes_history_window or self.root)
            return
        if len(records) > 2:
            self._messagebox.showinfo(
                "Minutes History",
                "当前选中了超过 2 个版本，将使用前两个选中版本进行对比。",
                parent=self._minutes_history_window or self.root,
            )
        self._set_minutes_history_viewer_text(self._render_minutes_diff_text(records[:2]))

    def _render_minutes_diff_text(self, records: list[MeetingMinutesRecord]) -> str:
        left, right = sorted(records[:2], key=lambda item: item.created_at)
        diff_lines = list(
            difflib.unified_diff(
                left.markdown_body.splitlines(),
                right.markdown_body.splitlines(),
                fromfile=f"{left.minutes_id}:{left.template.value}",
                tofile=f"{right.minutes_id}:{right.template.value}",
                lineterm="",
            ),
        )
        if not diff_lines:
            return (
                f"# Minutes Diff\n\n"
                f"- Older: {left.minutes_id}\n"
                f"- Newer: {right.minutes_id}\n\n"
                "No markdown differences."
            )
        header = [
            "# Minutes Diff",
            "",
            f"- Older: {left.minutes_id}",
            f"- Newer: {right.minutes_id}",
            "",
        ]
        return "\n".join(header + diff_lines)

    def _set_minutes_history_viewer_text(self, content: str) -> None:
        if self._minutes_history_viewer is None:
            return
        self._minutes_history_viewer.configure(state="normal")
        self._minutes_history_viewer.delete("1.0", "end")
        self._minutes_history_viewer.insert("1.0", content)
        self._minutes_history_viewer.see("1.0")
        self._minutes_history_viewer.configure(state="disabled")

    def _selected_minutes_template(self) -> MeetingExportTemplate:
        raw_value = self.minutes_template_var.get().strip() or MeetingExportTemplate.STANDARD.value
        try:
            return MeetingExportTemplate(raw_value)
        except ValueError:
            self.minutes_template_var.set(MeetingExportTemplate.STANDARD.value)
            return MeetingExportTemplate.STANDARD

    def _selected_minutes_output_dir(self) -> Path:
        raw_value = self.minutes_export_dir_var.get().strip()
        if not raw_value:
            self.minutes_export_dir_var.set(str(self._default_minutes_export_dir))
            return self._default_minutes_export_dir
        return Path(raw_value)

    def _set_running_state(self, *, is_running: bool) -> None:
        disabled_state = "disabled" if is_running else "normal"
        readonly_state = "disabled" if is_running else "readonly"
        self.start_button.configure(state="disabled" if is_running else "normal")
        self.stop_button.configure(state="normal" if is_running else "disabled")
        self.clear_button.configure(state="disabled" if is_running else "normal")
        self.refresh_assistant_button.configure(state="disabled" if is_running and not self.assistant_enabled_var.get() else "normal")
        self.export_minutes_button.configure(state="normal" if self._current_session_id else "disabled")
        self.source_combo.configure(state=readonly_state)
        self.device_entry.configure(state=disabled_state)
        self.save_capture_check.configure(state=disabled_state)
        self.minutes_template_combo.configure(state="readonly")
        self.minutes_export_dir_entry.configure(state="normal")
        self.minutes_export_dir_button.configure(state="normal")
        self._update_minutes_action_state()

    def _update_alpha(self, _: object = None) -> None:
        value = min(max(float(self.alpha_var.get()), 0.55), 1.0)
        self.root.attributes("-alpha", value)
        self.alpha_label.configure(text=f"{value:.2f}")

    def _initial_assistant_status(self) -> str:
        if self.assistant_service is None:
            return "Assistant unavailable."
        reason = self.assistant_service.availability_reason()
        if reason is None:
            return "Assistant ready."
        return f"Assistant fallback mode: {reason}"

    def _assistant_backend_label(self) -> str:
        if self.assistant_service is None:
            return "assistant_backend: unavailable"
        reason = self.assistant_service.availability_reason()
        if reason is None:
            return f"assistant_backend: openai_compatible / {self.assistant_service.model}"
        return "assistant_backend: heuristic_fallback"

    def _on_close(self) -> None:
        if self._stop_event is not None:
            self._stop_event.set()
        self._close_minutes_history_panel()
        self.root.destroy()
