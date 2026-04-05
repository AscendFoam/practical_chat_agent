from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from practical_chat_agent.connectors.desktop.base import DesktopConnector
from practical_chat_agent.connectors.desktop.pywinauto_support import prepare_pywinauto
from practical_chat_agent.connectors.desktop.screen_capture import capture_screen_region_png, save_png_bytes
from practical_chat_agent.connectors.desktop.windows_api import (
    get_foreground_window_handle,
    list_child_windows,
    list_visible_windows,
)
from practical_chat_agent.core.enums import Platform
from practical_chat_agent.core.models import DesktopCapturedMessage, DesktopScanResult, OcrDocumentResult, OcrTextBlock
from practical_chat_agent.services.ocr import GlmOcrService


@dataclass(slots=True)
class OcrLine:
    text: str
    label: str | None
    bbox: list[float]
    left: float
    top: float
    right: float
    bottom: float
    width: float
    height: float
    center_x: float
    side: str
    timestamp_text: str | None


class WeChatDesktopConnector(DesktopConnector):
    connector_name = "wechat_desktop"

    def __init__(
        self,
        *,
        ocr_service: GlmOcrService | None = None,
        capture_debug_dir: str | Path | None = None,
    ) -> None:
        self.ocr_service = ocr_service
        self.capture_debug_dir = Path(capture_debug_dir or ".cache/desktop_captures")

    def scan_current_conversation(
        self,
        *,
        account_id: str,
        conversation_hint: str | None = None,
        force_ocr: bool = False,
        save_capture: bool = False,
    ) -> DesktopScanResult:
        if sys.platform != "win32":
            return DesktopScanResult(
                connector_name=self.connector_name,
                platform=Platform.WECHAT,
                account_id=account_id,
                conversation_hint=conversation_hint,
                notes=["Desktop scanning is currently implemented for Windows only."],
            )

        candidates = self._find_candidate_windows(
            visible_windows=list_visible_windows(),
            conversation_hint=conversation_hint,
        )
        if not candidates:
            return DesktopScanResult(
                connector_name=self.connector_name,
                platform=Platform.WECHAT,
                account_id=account_id,
                conversation_hint=conversation_hint,
                notes=[
                    "No WeChat desktop window was detected.",
                    "Make sure the WeChat client is running and its main window is visible.",
                ],
            )

        window = candidates[0]
        child_windows = list_child_windows(int(window["hwnd"]), max_depth=3)
        foreground_hwnd = get_foreground_window_handle()
        notes = [
            f"Detected WeChat candidate window: title='{window['title']}' process='{window['process_name']}'.",
            f"Window handle={window['hwnd']} pid={window['process_id']} class='{window['class_name']}' rect={window['rect']}.",
        ]
        if foreground_hwnd is not None:
            notes.append(f"Current foreground window handle is {foreground_hwnd}.")
        if force_ocr:
            notes.append("Force OCR is enabled, so accessible-text extraction will be skipped.")
        if save_capture:
            notes.append("Save capture is enabled, so OCR screenshots will be persisted.")
        if child_windows:
            notes.append(
                "Child window tree: "
                + "; ".join(
                    f"hwnd={child['hwnd']} class='{child['class_name']}' pid={child['process_id']} visible={child['visible']}"
                    for child in child_windows[:4]
                ),
            )

        messages, extra_notes = self._extract_messages(
            account_id=account_id,
            window=window,
            child_windows=child_windows,
            foreground_hwnd=foreground_hwnd,
            force_ocr=force_ocr,
            save_capture=save_capture,
        )
        notes.extend(extra_notes)
        return DesktopScanResult(
            connector_name=self.connector_name,
            platform=Platform.WECHAT,
            account_id=account_id,
            conversation_hint=conversation_hint,
            messages=messages,
            notes=notes,
        )

    @staticmethod
    def _find_candidate_windows(
        *,
        visible_windows: list[dict[str, object]],
        conversation_hint: str | None,
    ) -> list[dict[str, object]]:
        hint = (conversation_hint or "").casefold()

        def matches(window: dict[str, object]) -> bool:
            title = str(window.get("title") or "")
            process_name = str(window.get("process_name") or "")
            lowered_title = title.casefold()
            lowered_process = process_name.casefold()
            return (
                "wechat" in lowered_process
                or "weixin" in lowered_process
                or "wechat" in lowered_title
                or "\u5fae\u4fe1" in title
            )

        candidates = [window for window in visible_windows if matches(window)]
        if hint:
            hinted = [window for window in candidates if hint in str(window.get("title") or "").casefold()]
            if hinted:
                return hinted
        return candidates

    def _extract_messages(
        self,
        *,
        account_id: str,
        window: dict[str, object],
        child_windows: list[dict[str, object]],
        foreground_hwnd: int | None,
        force_ocr: bool,
        save_capture: bool,
    ) -> tuple[list[DesktopCapturedMessage], list[str]]:
        notes: list[str] = []
        if not force_ocr:
            Desktop, bootstrap_notes = prepare_pywinauto()
            notes.extend(bootstrap_notes)
            if Desktop is not None:
                messages, accessible_notes = self._extract_accessible_messages(
                    window=window,
                    child_windows=child_windows,
                    Desktop=Desktop,
                )
                notes.extend(accessible_notes)
                if messages:
                    return messages, notes
        else:
            notes.append("Accessible-text extraction was skipped because force_ocr=True.")

        ocr_messages, ocr_notes = self._extract_messages_via_ocr(
            account_id=account_id,
            window=window,
            child_windows=child_windows,
            foreground_hwnd=foreground_hwnd,
            save_capture=save_capture,
        )
        notes.extend(ocr_notes)
        return ocr_messages, notes

    def _extract_accessible_messages(
        self,
        *,
        window: dict[str, object],
        child_windows: list[dict[str, object]],
        Desktop: Any,
    ) -> tuple[list[DesktopCapturedMessage], list[str]]:
        notes: list[str] = []
        handles = [int(window["hwnd"])] + [int(child["hwnd"]) for child in child_windows]
        candidates: list[dict[str, Any]] = []
        counts = {"uia": 0, "win32": 0}
        for hwnd in handles:
            for backend in ("uia", "win32"):
                extracted, note = self._read_text_candidates(Desktop=Desktop, hwnd=hwnd, backend=backend)
                candidates.extend(extracted)
                counts[backend] += len(extracted)
                if note:
                    notes.append(note)

        filtered = self._filter_accessible_candidates(candidates=candidates, root_window=window)
        if filtered:
            notes.append(
                f"Collected {len(filtered)} visible message candidates from pywinauto texts (uia={counts['uia']}, win32={counts['win32']}).",
            )
        elif candidates:
            notes.append(
                "pywinauto connected, but only chrome-level text was accessible. The current WeChat build exposes very little standard UIA text.",
            )
        else:
            notes.append(
                "pywinauto connected, but no non-empty accessible texts were exposed by the current window tree. Falling back to OCR.",
            )

        return [
            DesktopCapturedMessage(
                sender_name=item["sender_name"],
                text=item["message_text"],
                display_time=item.get("display_time"),
                bubble_side=item.get("bubble_side"),
                bubble_type=item.get("bubble_type"),
                quoted_text=item.get("quoted_text"),
                quoted_sender_name=item.get("quoted_sender_name"),
                raw=item["raw"],
            )
            for item in filtered
        ], notes

    def _extract_messages_via_ocr(
        self,
        *,
        account_id: str,
        window: dict[str, object],
        child_windows: list[dict[str, object]],
        foreground_hwnd: int | None,
        save_capture: bool,
    ) -> tuple[list[DesktopCapturedMessage], list[str]]:
        notes: list[str] = []
        if self.ocr_service is None:
            return [], ["OCR fallback is not configured for this desktop connector."]

        reason = self.ocr_service.availability_reason()
        if reason is not None:
            return [], [f"OCR fallback is unavailable because {reason}."]

        valid_handles = {int(window["hwnd"])} | {int(child["hwnd"]) for child in child_windows}
        if foreground_hwnd is None:
            return [], ["OCR fallback was skipped because Windows did not report a foreground window."]
        if foreground_hwnd not in valid_handles:
            return [], [
                "OCR fallback was skipped because the detected WeChat window is not the current foreground window. Bring the target chat to the front and rerun.",
            ]

        chat_rect = self._estimate_chat_history_rect(window)
        notes.append(f"OCR fallback will capture the estimated chat history region: {chat_rect}.")
        try:
            screenshot_bytes = capture_screen_region_png(chat_rect)
        except Exception as exc:  # noqa: BLE001
            return [], [f"OCR fallback could not capture the visible chat region: {exc}"]

        capture_path: Path | None = None
        if save_capture:
            capture_path = self._save_capture_artifact(account_id=account_id, window=window, png_bytes=screenshot_bytes)
            notes.append(f"OCR fallback saved a debug capture to '{capture_path}'.")

        try:
            ocr_result = self.ocr_service.recognize_image(
                image_bytes=screenshot_bytes,
                mime_type="image/png",
                user_id=account_id,
            )
        except Exception as exc:  # noqa: BLE001
            return [], [f"GLM OCR request failed: {exc}"]

        parsed, sensitive_count, timeline_count = self._parse_ocr_messages(ocr_result)
        if sensitive_count:
            notes.append(f"OCR parsing suppressed {sensitive_count} lines that looked like secrets or credentials.")
        if timeline_count:
            notes.append(f"OCR parsing recognized {timeline_count} timeline markers or timestamp separators.")
        if not parsed:
            notes.append("GLM OCR completed, but no chat-like message bubbles were extracted from the screenshot.")
            return [], notes

        notes.append(f"GLM OCR extracted {len(parsed)} structured message bubbles from the visible chat screenshot.")
        return [
            DesktopCapturedMessage(
                sender_name=item["sender_name"],
                text=item["message_text"],
                display_time=item.get("display_time"),
                bubble_side=item.get("bubble_side"),
                bubble_type=item.get("bubble_type"),
                quoted_text=item.get("quoted_text"),
                quoted_sender_name=item.get("quoted_sender_name"),
                raw={
                    "source": "wechat_desktop_ocr",
                    "provider": ocr_result.provider,
                    "model": ocr_result.model,
                    "bbox": item["bbox"],
                    "label": item["label"],
                    "raw_text": item["raw_text"],
                    "line_count": item["line_count"],
                    **({"debug_capture_path": str(capture_path)} if capture_path is not None else {}),
                },
            )
            for item in parsed
        ], notes

    def _read_text_candidates(
        self,
        *,
        Desktop: Any,
        hwnd: int,
        backend: str,
    ) -> tuple[list[dict[str, Any]], str | None]:
        try:
            wrapper = Desktop(backend=backend).window(handle=hwnd).wrapper_object()
        except Exception as exc:  # noqa: BLE001
            return [], f"{backend} backend could not connect to hwnd={hwnd}: {exc}"

        controls: list[Any] = [wrapper]
        descendant_error: str | None = None
        try:
            controls.extend(wrapper.descendants())
        except Exception as exc:  # noqa: BLE001
            descendant_error = str(exc)
            try:
                controls.extend(wrapper.children())
            except Exception:  # noqa: BLE001
                pass

        extracted: list[dict[str, Any]] = []
        for control in controls:
            text = self._safe_window_text(control)
            if not text:
                continue
            extracted.append(
                {
                    "text": text,
                    "backend": backend,
                    "hwnd": hwnd,
                    "control_type": self._safe_control_attr(control, "control_type"),
                    "class_name": self._safe_control_attr(control, "class_name"),
                    "rect": self._safe_rectangle(control),
                },
            )

        note = None
        if descendant_error is not None and extracted:
            note = f"{backend} backend had limited tree access for hwnd={hwnd}: {descendant_error}"
        elif descendant_error is not None:
            note = f"{backend} backend could only inspect the top-level wrapper for hwnd={hwnd}: {descendant_error}"
        return extracted, note

    def _filter_accessible_candidates(
        self,
        *,
        candidates: list[dict[str, Any]],
        root_window: dict[str, object],
    ) -> list[dict[str, Any]]:
        rect = dict(root_window.get("rect") or {})
        left = int(rect.get("left", 0))
        top = int(rect.get("top", 0))
        right = int(rect.get("right", 0))
        bottom = int(rect.get("bottom", 0))
        width = max(right - left, 1)
        height = max(bottom - top, 1)
        min_chat_left = left + int(width * 0.18)
        min_chat_top = top + int(height * 0.08)
        max_chat_bottom = bottom - int(height * 0.16)
        ignored = {
            "",
            "weixin",
            "\u5fae\u4fe1",
            "\u641c\u7d22".casefold(),
            "\u804a\u5929\u4fe1\u606f".casefold(),
        }

        results: list[dict[str, Any]] = []
        seen: set[tuple[str, tuple[int, int, int, int] | None]] = set()
        for item in candidates:
            text = self._normalize_text(item.get("text"))
            if not text or text.casefold() in ignored or self._looks_like_timestamp(text):
                continue
            bounds = item.get("rect")
            box = self._rect_to_tuple(bounds)
            if box is not None:
                center_x = (box[0] + box[2]) / 2
                center_y = (box[1] + box[3]) / 2
                if center_x < min_chat_left or center_y < min_chat_top or center_y > max_chat_bottom:
                    continue
            key = (text, box)
            if key in seen:
                continue
            seen.add(key)
            sender_name, message_text = self._split_sender_prefix(text)
            bubble_side = None
            if box is not None:
                bubble_side = "right" if (box[0] + box[2]) / 2 >= left + width * 0.60 else "left"
            results.append(
                {
                    "sort_key": (box[1] if box else 0, box[0] if box else 0, text),
                    "sender_name": sender_name,
                    "message_text": message_text,
                    "display_time": None,
                    "bubble_side": bubble_side,
                    "bubble_type": "outgoing" if bubble_side == "right" else ("incoming" if bubble_side == "left" else None),
                    "quoted_text": None,
                    "quoted_sender_name": None,
                    "raw": {
                        "source": "wechat_desktop_accessible_text",
                        "backend": item.get("backend"),
                        "window_handle": item.get("hwnd"),
                        "control_type": item.get("control_type"),
                        "class_name": item.get("class_name"),
                        "bounds": bounds,
                        "raw_text": text,
                    },
                },
            )
        results.sort(key=lambda item: item["sort_key"])
        return results[:50]

    def _parse_ocr_messages(self, ocr_result: OcrDocumentResult) -> tuple[list[dict[str, Any]], int, int]:
        lines = self._prepare_ocr_lines(ocr_result.blocks)
        if not lines:
            return [], 0, 0

        results: list[dict[str, Any]] = []
        sensitive_count = 0
        timeline_count = 0
        current_time: str | None = None
        sender_hint: str | None = None
        recent_left_sender: str | None = None

        index = 0
        while index < len(lines):
            line = lines[index]
            if line.side == "center":
                if line.timestamp_text is not None:
                    current_time = line.timestamp_text
                    sender_hint = None
                    recent_left_sender = None
                    timeline_count += 1
                else:
                    system_kind = self._classify_system_message(line.text)
                    if system_kind is not None and not self._looks_sensitive(line.text):
                        results.append(
                            {
                                "sort_key": (line.top, line.left, line.text),
                                "sender_name": None,
                                "message_text": line.text,
                                "display_time": current_time,
                                "bubble_side": "center",
                                "bubble_type": system_kind,
                                "quoted_text": None,
                                "quoted_sender_name": None,
                                "bbox": line.bbox,
                                "label": line.label,
                                "raw_text": line.text,
                                "line_count": 1,
                            },
                        )
                index += 1
                continue

            next_line = lines[index + 1] if index + 1 < len(lines) else None
            if sender_hint is None and self._looks_like_sender_header(line=line, next_line=next_line):
                sender_hint = line.text
                recent_left_sender = line.text
                index += 1
                continue

            if self._looks_sensitive(line.text):
                sensitive_count += 1
                index += 1
                continue

            bubble_side = line.side
            bubble_type = "outgoing" if bubble_side == "right" else "incoming"
            sender_name = None
            if bubble_side == "left":
                sender_name = sender_hint or recent_left_sender
                recent_left_sender = sender_name
            else:
                sender_hint = None

            merged_texts = [line.text]
            merged_bbox = list(line.bbox)
            consumed = 1
            gap_limit = max(18.0, line.height * 1.4)
            while index + consumed < len(lines):
                candidate = lines[index + consumed]
                if candidate.side != bubble_side or candidate.side == "center":
                    break
                future = lines[index + consumed + 1] if index + consumed + 1 < len(lines) else None
                if (
                    sender_hint is None
                    and candidate.top - merged_bbox[3] >= max(10.0, line.height * 0.45)
                    and self._looks_like_sender_header(line=candidate, next_line=future)
                ):
                    break
                if candidate.top - merged_bbox[3] > gap_limit:
                    break
                if self._looks_sensitive(candidate.text):
                    sensitive_count += 1
                    consumed += 1
                    continue
                merged_texts.append(candidate.text)
                merged_bbox = self._merge_bbox(merged_bbox, candidate.bbox)
                consumed += 1

            message_text = "\n".join(merged_texts).strip()
            if message_text:
                quoted_text, quoted_sender_name, cleaned_text = self._extract_reply_quote(
                    merged_texts=merged_texts,
                    bubble_side=bubble_side,
                )
                final_text = cleaned_text or message_text
                classified_bubble_type = bubble_type
                if self._looks_like_recall_message(final_text):
                    classified_bubble_type = "recall_notice"
                elif quoted_text is not None:
                    classified_bubble_type = "incoming_reply" if bubble_side == "left" else "outgoing_reply"
                results.append(
                    {
                        "sort_key": (merged_bbox[1], merged_bbox[0], final_text),
                        "sender_name": sender_name,
                        "message_text": final_text,
                        "display_time": current_time,
                        "bubble_side": bubble_side,
                        "bubble_type": classified_bubble_type,
                        "quoted_text": quoted_text,
                        "quoted_sender_name": quoted_sender_name,
                        "bbox": merged_bbox,
                        "label": line.label,
                        "raw_text": message_text,
                        "line_count": len(merged_texts),
                    },
                )
            index += consumed

        results.sort(key=lambda item: item["sort_key"])
        return results[:50], sensitive_count, timeline_count

    def _prepare_ocr_lines(self, blocks: list[OcrTextBlock]) -> list[OcrLine]:
        prepared: list[tuple[str, list[float], str | None]] = []
        for block in blocks:
            text = self._normalize_text(block.text)
            if text and len(block.bbox) >= 4:
                prepared.append((text, [float(value) for value in block.bbox[:4]], block.label))
        if not prepared:
            return []

        image_width = max(bbox[2] for _, bbox, _ in prepared)
        results: list[OcrLine] = []
        for text, bbox, label in prepared:
            left, top, right, bottom = bbox
            width = max(right - left, 1.0)
            center_x = left + width / 2
            timestamp = self._extract_timestamp(text)
            if timestamp is not None:
                side = "center"
            elif abs(center_x - image_width / 2) <= image_width * 0.12 and width <= image_width * 0.55:
                side = "center"
            elif center_x >= image_width * 0.62:
                side = "right"
            else:
                side = "left"
            results.append(
                OcrLine(
                    text=text,
                    label=label,
                    bbox=bbox,
                    left=left,
                    top=top,
                    right=right,
                    bottom=bottom,
                    width=width,
                    height=max(bottom - top, 1.0),
                    center_x=center_x,
                    side=side,
                    timestamp_text=timestamp,
                ),
            )
        results.sort(key=lambda item: (item.top, item.left, item.text))
        return results

    def _looks_like_sender_header(self, *, line: OcrLine, next_line: OcrLine | None) -> bool:
        if line.side != "left" or line.timestamp_text is not None or len(line.text) > 24:
            return False
        if re.search(r"https?://|www\.|[@#:/\\]", line.text):
            return False
        if self._looks_sensitive(line.text):
            return False
        if next_line is None or next_line.side != "left":
            return False
        if next_line.top - line.bottom > max(28.0, line.height * 2.2):
            return False
        if next_line.width < line.width * 0.8 and len(next_line.text) <= len(line.text):
            return False
        return True

    def _extract_reply_quote(
        self,
        *,
        merged_texts: list[str],
        bubble_side: str,
    ) -> tuple[str | None, str | None, str | None]:
        if len(merged_texts) < 2:
            return None, None, None

        if len(merged_texts) >= 3:
            quote_lines = merged_texts[:-1]
            reply_line = merged_texts[-1].strip()
            if sum(len(line) for line in quote_lines) <= 72 and reply_line:
                quoted_sender_name = None
                quoted_text = "\n".join(quote_lines).strip()
                if ": " in quote_lines[0] or "\uff1a" in quote_lines[0]:
                    quoted_sender_name, first_quote = self._split_sender_prefix(quote_lines[0])
                    quoted_text = "\n".join([first_quote, *quote_lines[1:]]).strip()
                return quoted_text or None, quoted_sender_name, reply_line

        if len(merged_texts) == 2 and bubble_side == "right":
            first_line, second_line = merged_texts
            if len(first_line) <= 24 and len(second_line) >= max(2, len(first_line)):
                return first_line.strip() or None, None, second_line.strip() or None

        return None, None, None

    @staticmethod
    def _looks_like_recall_message(text: str) -> bool:
        lowered = text.casefold()
        return "\u64a4\u56de\u4e86\u4e00\u6761\u6d88\u606f" in text or "recalled a message" in lowered

    def _classify_system_message(self, text: str) -> str | None:
        if not text.strip():
            return None
        if self._looks_like_recall_message(text):
            return "system_recall"
        lowered = text.casefold()
        if any(
            marker in text
            for marker in (
                "\u4ee5\u4e0b\u662f\u65b0\u6d88\u606f",
                "\u4ee5\u4e0a\u4e3a\u5386\u53f2\u6d88\u606f",
                "\u52a0\u5165\u4e86\u7fa4\u804a",
                "\u79fb\u51fa\u4e86\u7fa4\u804a",
                "\u7fa4\u516c\u544a",
            )
        ):
            return "system_notice"
        if "joined the group" in lowered or "left the group" in lowered or "invited" in lowered:
            return "system_notice"
        return None

    def _estimate_chat_history_rect(self, window: dict[str, object]) -> dict[str, int]:
        rect = dict(window.get("rect") or {})
        left = int(rect.get("left", 0))
        top = int(rect.get("top", 0))
        right = int(rect.get("right", 0))
        bottom = int(rect.get("bottom", 0))
        width = max(right - left, 1)
        height = max(bottom - top, 1)
        return {
            "left": left + int(width * 0.26),
            "top": top + int(height * 0.10),
            "right": right - int(width * 0.02),
            "bottom": bottom - int(height * 0.23),
        }

    def _save_capture_artifact(self, *, account_id: str, window: dict[str, object], png_bytes: bytes) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_account_id = re.sub(r"[^A-Za-z0-9_-]+", "_", account_id).strip("_") or "desktop"
        output_path = self.capture_debug_dir / self.connector_name / safe_account_id / f"{timestamp}_hwnd_{int(window.get('hwnd') or 0)}.png"
        return save_png_bytes(png_bytes=png_bytes, output_path=output_path)

    @staticmethod
    def _merge_bbox(first: list[float], second: list[float]) -> list[float]:
        return [min(first[0], second[0]), min(first[1], second[1]), max(first[2], second[2]), max(first[3], second[3])]

    @staticmethod
    def _safe_window_text(control: Any) -> str:
        try:
            return WeChatDesktopConnector._normalize_text(control.window_text())
        except Exception:  # noqa: BLE001
            return ""

    @staticmethod
    def _safe_control_attr(control: Any, attr: str) -> str | None:
        try:
            element_info = getattr(control, "element_info", None)
            value = getattr(element_info, attr, None)
            return None if value is None else str(value)
        except Exception:  # noqa: BLE001
            return None

    @staticmethod
    def _safe_rectangle(control: Any) -> dict[str, int] | None:
        try:
            rect = control.rectangle()
        except Exception:  # noqa: BLE001
            return None
        return {"left": int(rect.left), "top": int(rect.top), "right": int(rect.right), "bottom": int(rect.bottom)}

    @staticmethod
    def _rect_to_tuple(rect: Any) -> tuple[int, int, int, int] | None:
        if not isinstance(rect, dict):
            return None
        try:
            return (int(rect["left"]), int(rect["top"]), int(rect["right"]), int(rect["bottom"]))
        except Exception:  # noqa: BLE001
            return None

    @staticmethod
    def _normalize_text(value: Any) -> str:
        return re.sub(r"\s+", " ", str(value or "").replace("\r", " ").replace("\n", " ")).strip()

    @staticmethod
    def _split_sender_prefix(text: str) -> tuple[str | None, str]:
        for separator in (": ", "\uff1a"):
            if separator in text:
                sender_name, message_text = text.split(separator, 1)
                if 0 < len(sender_name) <= 20:
                    return sender_name.strip(), message_text.strip()
        return None, text

    @staticmethod
    def _extract_timestamp(text: str) -> str | None:
        normalized = text.strip()
        patterns = (
            r"\d{1,2}:\d{2}",
            r"\d{4}[-/]\d{1,2}[-/]\d{1,2}",
            r"(?:\u6628\u5929|\u4eca\u5929|\u661f\u671f[\u4e00-\u65e5])\s+\d{1,2}:\d{2}",
            r"\d{1,2}\u6708\d{1,2}\u65e5\s+\d{1,2}:\d{2}",
        )
        return normalized if any(re.fullmatch(pattern, normalized) for pattern in patterns) else None

    def _looks_like_timestamp(self, text: str) -> bool:
        return self._extract_timestamp(text) is not None

    @staticmethod
    def _looks_sensitive(text: str) -> bool:
        lowered = text.casefold()
        if any(keyword in lowered for keyword in ("password", "passwd", "api_key", "apikey", "secret", "token")):
            return True
        if re.search(r"\bsk-[A-Za-z0-9_-]{10,}\b", text):
            return True
        if re.search(r"[A-Za-z0-9]{20,}\.[A-Za-z0-9_-]{6,}", text):
            return True
        return False
