from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from practical_chat_agent.core.models import MeetingAssistantAdvice, MeetingTranscriptSegment


@dataclass(slots=True)
class MeetingAssistantContext:
    meeting_title: str | None
    transcript_segments: list[MeetingTranscriptSegment]


class MeetingAssistantService:
    """Generate lightweight live meeting assistance from recent transcript context."""

    backend_name = "meeting_assistant"

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str | None,
        model: str | None,
        timeout_seconds: float = 20.0,
        enabled: bool = True,
        context_segments: int = 8,
    ) -> None:
        self.api_key = (api_key or "").strip() or None
        self.base_url = (base_url or "").strip() or None
        self.model = (model or "").strip() or None
        self.timeout_seconds = max(float(timeout_seconds), 3.0)
        self.enabled = enabled
        self.context_segments = max(int(context_segments), 3)

    def availability_reason(self) -> str | None:
        if not self.enabled:
            return "meeting assistant is disabled by configuration"
        if not self.api_key:
            return "OPENAI_API_KEY is not configured"
        if not self.base_url:
            return "OPENAI_BASE_URL is not configured"
        if not self.model:
            return "MEETING_ASSISTANT_MODEL is not configured"
        return None

    def build_summary_advice(
        self,
        *,
        meeting_title: str | None,
        transcript_segments: Iterable[MeetingTranscriptSegment],
    ) -> MeetingAssistantAdvice:
        context = self._build_context(meeting_title=meeting_title, transcript_segments=transcript_segments)
        return self._generate_fallback_advice(context=context)

    def generate_advice(
        self,
        *,
        meeting_title: str | None,
        transcript_segments: Iterable[MeetingTranscriptSegment],
    ) -> MeetingAssistantAdvice:
        context = self._build_context(meeting_title=meeting_title, transcript_segments=transcript_segments)
        if not context.transcript_segments:
            return MeetingAssistantAdvice(
                backend="heuristic_fallback",
                status="waiting_transcript",
                summary="Not enough transcript yet. Keep listening for more meeting context.",
                suggested_reply="Once the discussion becomes clearer, I will suggest a concise response.",
            )

        remote_reason = self.availability_reason()
        if remote_reason is None:
            try:
                return self._generate_remote_advice(context=context)
            except Exception as exc:  # noqa: BLE001
                fallback = self._generate_fallback_advice(context=context)
                fallback.status = "fallback_after_error"
                fallback.raw["fallback_reason"] = str(exc)
                return fallback

        fallback = self._generate_fallback_advice(context=context)
        fallback.status = "fallback"
        fallback.raw["fallback_reason"] = remote_reason
        return fallback

    def _build_context(
        self,
        *,
        meeting_title: str | None,
        transcript_segments: Iterable[MeetingTranscriptSegment],
    ) -> MeetingAssistantContext:
        return MeetingAssistantContext(
            meeting_title=meeting_title,
            transcript_segments=[
                segment
                for segment in transcript_segments
                if (segment.text or "").strip()
            ][-self.context_segments :],
        )

    def _generate_remote_advice(self, *, context: MeetingAssistantContext) -> MeetingAssistantAdvice:
        payload = {
            "model": self.model,
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a concise meeting copilot. "
                        "Return valid JSON with keys: summary, key_points, "
                        "follow_up_questions, suggested_reply, action_items. "
                        "Each list must contain at most 3 items."
                    ),
                },
                {
                    "role": "user",
                    "content": self._build_transcript_prompt(context=context),
                },
            ],
        }
        response = self._post_json(
            url=self._chat_completions_url(),
            payload=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        content = self._extract_message_content(response=response)
        parsed = self._parse_json_content(content=content)
        return MeetingAssistantAdvice(
            backend="openai_compatible_chat",
            model=self.model,
            status="ok",
            summary=str(parsed.get("summary") or "").strip() or "The model did not return a summary.",
            key_points=self._coerce_list(parsed.get("key_points")),
            follow_up_questions=self._coerce_list(parsed.get("follow_up_questions")),
            suggested_reply=str(parsed.get("suggested_reply") or "").strip() or None,
            action_items=self._coerce_list(parsed.get("action_items")),
            raw={"provider_response": response},
        )

    def _generate_fallback_advice(self, *, context: MeetingAssistantContext) -> MeetingAssistantAdvice:
        lines = [segment.text.strip() for segment in context.transcript_segments if segment.text.strip()]
        latest_text = lines[-1] if lines else ""
        recent_lines = lines[-3:]
        joined_recent = "; ".join(recent_lines)

        summary = (
            f"Recent discussion focuses on: {joined_recent[:160]}"
            if joined_recent
            else "There is not enough transcript yet to summarize the meeting."
        )
        key_points = [self._shorten(line) for line in recent_lines]
        follow_up_questions = self._infer_follow_up_questions(lines=lines)
        action_items = self._infer_action_items(lines=lines)
        suggested_reply = self._infer_suggested_reply(latest_text=latest_text, lines=lines)

        return MeetingAssistantAdvice(
            backend="heuristic_fallback",
            model=None,
            status="ok",
            summary=summary,
            key_points=key_points,
            follow_up_questions=follow_up_questions,
            suggested_reply=suggested_reply,
            action_items=action_items,
            raw={
                "meeting_title": context.meeting_title,
                "context_line_count": len(lines),
            },
        )

    @staticmethod
    def _build_transcript_prompt(*, context: MeetingAssistantContext) -> str:
        meeting_title = context.meeting_title or "Unknown meeting"
        rendered_lines = []
        for segment in context.transcript_segments:
            prefix = segment.display_time or ""
            speaker = f"{segment.speaker_name}: " if segment.speaker_name else ""
            rendered_lines.append(f"{prefix} {speaker}{segment.text.strip()}".strip())
        transcript_text = "\n".join(f"- {line}" for line in rendered_lines)
        return (
            f"Meeting title: {meeting_title}\n"
            "Below is the latest transcript window. Produce concise meeting assistance.\n"
            f"{transcript_text}\n"
            "Return JSON only."
        )

    def _chat_completions_url(self) -> str:
        assert self.base_url is not None
        normalized = self.base_url.rstrip("/")
        if normalized.endswith("/chat/completions"):
            return normalized
        return urljoin(f"{normalized}/", "chat/completions")

    def _post_json(
        self,
        *,
        url: str,
        payload: dict[str, object],
        headers: dict[str, str],
    ) -> dict[str, object]:
        request = Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"assistant HTTP error {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"assistant request failed: {exc}") from exc

    @staticmethod
    def _extract_message_content(*, response: dict[str, object]) -> str:
        choices = response.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                message = first.get("message")
                if isinstance(message, dict):
                    content = message.get("content")
                    if isinstance(content, str):
                        return content.strip()
        raise RuntimeError("assistant response did not contain a chat message content field")

    @staticmethod
    def _parse_json_content(*, content: str) -> dict[str, object]:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            parsed = json.loads(cleaned[start : end + 1])
            if isinstance(parsed, dict):
                return parsed
        raise RuntimeError("assistant response was not valid JSON")

    @staticmethod
    def _coerce_list(value: object) -> list[str]:
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()][:3]
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        return []

    @staticmethod
    def _shorten(text: str, limit: int = 64) -> str:
        cleaned = text.strip()
        if len(cleaned) <= limit:
            return cleaned
        return f"{cleaned[:limit - 1]}…"

    @classmethod
    def _infer_follow_up_questions(cls, *, lines: list[str]) -> list[str]:
        joined = "\n".join(lines)
        questions: list[str] = []
        keyword_rules = [
            (
                ("schedule", "timeline", "deadline", "launch", "date", "排期", "上线", "截止"),
                "Should we confirm the timeline, owner, and dependencies before moving on?",
            ),
            (
                ("risk", "issue", "blocker", "problem", "风险", "问题", "阻塞"),
                "What is the biggest risk right now, and do we already have a fallback plan?",
            ),
            (
                ("scope", "design", "requirement", "方案", "需求", "设计"),
                "Do we need to narrow the scope or restate the acceptance criteria?",
            ),
            (
                ("metric", "data", "cost", "指标", "数据", "成本"),
                "Is there a baseline metric or target number we should align on now?",
            ),
        ]
        for keywords, prompt in keyword_rules:
            if any(keyword in joined for keyword in keywords):
                questions.append(prompt)
        if not questions:
            questions.append("Do you want a one-sentence checkpoint summary to realign the room?")
        return questions[:3]

    @classmethod
    def _infer_action_items(cls, *, lines: list[str]) -> list[str]:
        joined = "\n".join(lines)
        items: list[str] = []
        if any(keyword in joined for keyword in ("owner", "follow up", "responsible", "负责人", "跟进")):
            items.append("Confirm the owner for each open task before the meeting ends.")
        if any(keyword in joined for keyword in ("tomorrow", "next week", "deadline", "明天", "下周", "截止")):
            items.append("Write down the next checkpoint or deadline while everyone is aligned.")
        if any(keyword in joined for keyword in ("risk", "issue", "blocker", "风险", "问题", "阻塞", "依赖")):
            items.append("Capture the major risk and dependency items for follow-up.")
        if not items:
            items.append("Separate confirmed decisions from open questions in the meeting notes.")
        return items[:3]

    @classmethod
    def _infer_suggested_reply(cls, *, latest_text: str, lines: list[str]) -> str:
        joined = "\n".join(lines)
        if any(keyword in joined for keyword in ("schedule", "timeline", "deadline", "排期", "上线", "截止")):
            return "I suggest we align the timeline, owner, and dependencies together so execution stays steady."
        if any(keyword in joined for keyword in ("risk", "issue", "blocker", "风险", "问题", "阻塞")):
            return "I suggest we call out the main risk and fallback plan now so everyone can judge the tradeoff clearly."
        if latest_text.endswith(("?", "？")):
            return "Let me restate my understanding first, then I will ask one precise follow-up to avoid misalignment."
        return "I can help close the loop by restating the current decision, open items, and next owner."
