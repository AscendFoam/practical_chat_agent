from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from practical_chat_agent.core.enums import MeetingExportTemplate
from practical_chat_agent.core.models import MeetingMinutesDraft, MeetingSegmentRecord, MeetingSessionRecord


@dataclass(slots=True)
class MeetingMinutesContext:
    session_record: MeetingSessionRecord
    segments: list[MeetingSegmentRecord]


class MeetingMinutesService:
    """Build export-ready meeting minutes with optional LLM rewriting."""

    backend_name = "meeting_minutes"

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str | None,
        model: str | None,
        timeout_seconds: float = 30.0,
        enabled: bool = True,
        context_segments: int = 24,
    ) -> None:
        self.api_key = (api_key or "").strip() or None
        self.base_url = (base_url or "").strip() or None
        self.model = (model or "").strip() or None
        self.timeout_seconds = max(float(timeout_seconds), 3.0)
        self.enabled = enabled
        self.context_segments = max(int(context_segments), 6)

    def availability_reason(self) -> str | None:
        if not self.enabled:
            return "meeting minutes rewriter is disabled by configuration"
        if not self.api_key:
            return "OPENAI_API_KEY is not configured"
        if not self.base_url:
            return "OPENAI_BASE_URL is not configured"
        if not self.model:
            return "MEETING_MINUTES_MODEL is not configured"
        return None

    def build_minutes(
        self,
        *,
        session_record: MeetingSessionRecord,
        segments: Iterable[MeetingSegmentRecord],
        template: MeetingExportTemplate,
        fallback_builder,
    ) -> MeetingMinutesDraft:
        context = self._build_context(
            session_record=session_record,
            segments=segments,
        )
        fallback_draft = fallback_builder(
            session_record=context.session_record,
            segments=context.segments,
            template=template,
        )

        remote_reason = self.availability_reason()
        if remote_reason is not None or not context.segments:
            fallback_draft.status = "fallback" if context.segments else "waiting_transcript"
            if remote_reason is not None:
                fallback_draft.raw["fallback_reason"] = remote_reason
            return fallback_draft

        try:
            return self._generate_remote_minutes(
                context=context,
                template=template,
                fallback_draft=fallback_draft,
            )
        except Exception as exc:  # noqa: BLE001
            fallback_draft.status = "fallback_after_error"
            fallback_draft.raw["fallback_reason"] = str(exc)
            return fallback_draft

    def _build_context(
        self,
        *,
        session_record: MeetingSessionRecord,
        segments: Iterable[MeetingSegmentRecord],
    ) -> MeetingMinutesContext:
        filtered_segments = [segment for segment in segments if (segment.text or "").strip()]
        return MeetingMinutesContext(
            session_record=session_record,
            segments=filtered_segments[-self.context_segments :],
        )

    def _generate_remote_minutes(
        self,
        *,
        context: MeetingMinutesContext,
        template: MeetingExportTemplate,
        fallback_draft: MeetingMinutesDraft,
    ) -> MeetingMinutesDraft:
        payload = {
            "model": self.model,
            "temperature": 0.25,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a meticulous executive assistant who rewrites meeting minutes in polished Chinese. "
                        "Return valid JSON only with keys: title, overview, background, conclusions, "
                        "action_items, risks, raw_excerpt_ids. Each list should contain concise, concrete items. "
                        "Do not invent facts beyond the transcript."
                    ),
                },
                {
                    "role": "user",
                    "content": self._build_minutes_prompt(
                        context=context,
                        template=template,
                    ),
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
        return MeetingMinutesDraft(
            template=template,
            backend="openai_compatible_chat",
            model=self.model,
            status="ok",
            title=str(parsed.get("title") or "").strip() or fallback_draft.title,
            overview=str(parsed.get("overview") or "").strip() or fallback_draft.overview,
            background=self._coerce_list(parsed.get("background"), fallback_draft.background),
            conclusions=self._coerce_list(parsed.get("conclusions"), fallback_draft.conclusions),
            action_items=self._coerce_list(parsed.get("action_items"), fallback_draft.action_items),
            risks=self._coerce_list(parsed.get("risks"), fallback_draft.risks),
            raw_excerpt_ids=self._coerce_list(parsed.get("raw_excerpt_ids"), fallback_draft.raw_excerpt_ids),
            raw={"provider_response": response},
        )

    @staticmethod
    def _build_minutes_prompt(
        *,
        context: MeetingMinutesContext,
        template: MeetingExportTemplate,
    ) -> str:
        session = context.session_record
        rendered_lines: list[str] = []
        for segment in context.segments:
            timestamp = segment.display_time or (segment.started_at.isoformat() if segment.started_at else "")
            speaker = f"{segment.speaker_name}: " if segment.speaker_name else ""
            rendered_lines.append(f"[{segment.segment_id}] {timestamp} {speaker}{segment.text.strip()}".strip())

        transcript_text = "\n".join(f"- {line}" for line in rendered_lines)
        return (
            f"Template: {template.value}\n"
            f"Meeting title: {session.meeting_title or session.meeting_key or session.session_id}\n"
            f"Meeting summary hint: {session.latest_summary or ''}\n"
            f"Existing key points: {'; '.join(session.latest_key_points)}\n"
            f"Existing action items: {'; '.join(session.latest_action_items)}\n"
            f"Existing follow-up questions: {'; '.join(session.latest_follow_up_questions)}\n"
            "Rewrite this into polished, human-like formal meeting minutes in Chinese.\n"
            "Use the transcript faithfully and avoid fictional details.\n"
            "Transcript window:\n"
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
            raise RuntimeError(f"minutes HTTP error {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"minutes request failed: {exc}") from exc

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
        raise RuntimeError("minutes response did not contain a chat message content field")

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
        raise RuntimeError("minutes response was not valid JSON")

    @staticmethod
    def _coerce_list(value: object, fallback: list[str]) -> list[str]:
        if isinstance(value, list):
            items = [str(item).strip() for item in value if str(item).strip()]
            return items or fallback
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        return fallback
