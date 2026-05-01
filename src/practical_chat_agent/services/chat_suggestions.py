from __future__ import annotations

import json
from collections.abc import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from practical_chat_agent.core.enums import ChannelType, SafetyMode
from practical_chat_agent.core.models import AgentProfile, ChatContext, ChatSuggestion, MemoryFact

_CHAT_SUGGESTION_JSON_SCHEMA: dict[str, object] = {
    "name": "chat_suggestion_result",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "should_reply": {"type": "boolean"},
            "summary": {"type": "string"},
            "reply_draft": {"type": "string"},
            "alternatives": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": 3,
            },
            "rationale": {"type": "string"},
            "risk_flags": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": 5,
            },
        },
        "required": [
            "should_reply",
            "summary",
            "reply_draft",
            "alternatives",
            "rationale",
            "risk_flags",
        ],
    },
}


class ChatSuggestionService:
    """Generate a reply suggestion for inbound chat turns."""

    backend_name = "chat_suggestion"

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str | None,
        model: str | None,
        timeout_seconds: float = 20.0,
        enabled: bool = True,
        default_model: str = "deepseek-chat",
    ) -> None:
        self.api_key = (api_key or "").strip() or None
        self.base_url = (base_url or "").strip() or None
        self.model = (model or "").strip() or None
        self.timeout_seconds = max(float(timeout_seconds), 3.0)
        self.enabled = enabled
        self.default_model = default_model

    @property
    def resolved_model(self) -> str:
        return self.model or self.default_model

    def availability_reason(self) -> str | None:
        if not self.enabled:
            return "chat suggestion is disabled by configuration"
        if not self.api_key:
            return "OPENAI_API_KEY is not configured"
        if not self.base_url:
            return "OPENAI_BASE_URL is not configured"
        return None

    def generate(
        self,
        *,
        agent: AgentProfile,
        context: ChatContext,
    ) -> ChatSuggestion:
        remote_reason = self.availability_reason()
        if remote_reason is None:
            try:
                return self._generate_remote(agent=agent, context=context)
            except Exception as exc:  # noqa: BLE001
                fallback = self._generate_fallback(agent=agent, context=context)
                fallback.status = "fallback_after_error"
                fallback.raw["fallback_reason"] = str(exc)
                fallback.raw["resolved_model"] = self.resolved_model
                return fallback

        fallback = self._generate_fallback(agent=agent, context=context)
        fallback.status = "fallback"
        fallback.raw["fallback_reason"] = remote_reason
        fallback.raw["resolved_model"] = self.resolved_model
        return fallback

    def _generate_remote(
        self,
        *,
        agent: AgentProfile,
        context: ChatContext,
    ) -> ChatSuggestion:
        response_format = self._build_response_format()
        payload: dict[str, object] = {
            "model": self.resolved_model,
            "temperature": 0.45,
            "messages": [
                {
                    "role": "system",
                    "content": self._build_system_prompt(agent=agent),
                },
                {
                    "role": "user",
                    "content": self._build_user_prompt(agent=agent, context=context),
                },
            ],
        }
        if response_format is not None:
            payload["response_format"] = response_format

        response = self._post_json(
            url=self._chat_completions_url(),
            payload=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        parsed = self._normalize_response_payload(
            self._parse_json_content(content=self._extract_message_content(response=response)),
        )
        reply_draft = self._clean_string(parsed.get("reply_draft"))
        alternatives = self._coerce_list(parsed.get("alternatives"))
        should_reply = self._coerce_bool(parsed.get("should_reply"))
        if should_reply is None:
            should_reply = bool(reply_draft)
        if should_reply and not reply_draft and alternatives:
            reply_draft = alternatives[0]
            alternatives = alternatives[1:]
        suggestion = ChatSuggestion(
            backend="openai_compatible_chat",
            model=self.resolved_model,
            status="ok",
            should_reply=should_reply,
            summary=self._clean_string(parsed.get("summary")) or context.summary,
            reply_draft=reply_draft,
            alternatives=alternatives,
            rationale=self._clean_string(parsed.get("rationale")),
            risk_flags=self._coerce_list(parsed.get("risk_flags"), limit=5),
            raw={
                "provider_response": response,
                "parsed_response": parsed,
            },
        )
        if suggestion.should_reply and not suggestion.reply_draft:
            raise RuntimeError("chat suggestion model returned should_reply=true but no reply_draft")
        return suggestion

    def _generate_fallback(
        self,
        *,
        agent: AgentProfile,
        context: ChatContext,
    ) -> ChatSuggestion:
        latest_text = (context.latest_message_text or "").strip()
        if not latest_text:
            return ChatSuggestion(
                backend="heuristic_fallback",
                status="no_message",
                should_reply=False,
                summary="No text content was available for suggestion generation.",
                rationale="Inbound event did not contain non-empty text.",
            )

        no_reply_reason = self._infer_no_reply_reason(text=latest_text)
        if no_reply_reason is not None:
            return ChatSuggestion(
                backend="heuristic_fallback",
                status="ok",
                should_reply=False,
                summary="The latest message looks informational and does not need an immediate reply.",
                rationale=no_reply_reason,
                raw={"latest_text": latest_text},
            )

        memory_hint = self._memory_phrase(context.memory_hits)
        reply = self._build_fallback_reply(
            context=context,
            memory_hint=memory_hint,
        )
        alternatives = self._build_alternatives(
            context=context,
            memory_hint=memory_hint,
        )
        risk_flags: list[str] = []
        if agent.safety_mode == SafetyMode.DRAFT_ONLY:
            risk_flags.append("draft_only_mode")
        if context.channel_type == ChannelType.GROUP:
            risk_flags.append("group_context")
        return ChatSuggestion(
            backend="heuristic_fallback",
            model=self.resolved_model,
            status="ok",
            should_reply=True,
            summary=context.summary,
            reply_draft=reply,
            alternatives=alternatives,
            rationale=(
                "Built a reply draft from the latest message, "
                f"{len(context.recent_events)} recent events, and {len(context.memory_hits)} memory hits."
            ),
            risk_flags=risk_flags,
            raw={"memory_hint_used": memory_hint},
        )

    @staticmethod
    def _infer_no_reply_reason(*, text: str) -> str | None:
        normalized = " ".join(text.split()).strip().casefold()
        if not normalized:
            return "The latest message was empty after normalization."
        if normalized in {
            "ok",
            "okay",
            "k",
            "thanks",
            "thank you",
            "\u6536\u5230",
            "\u597d\u7684",
            "\u597d",
            "\u55ef",
            "\u6069",
        }:
            return "Short acknowledgement detected."
        return None

    @staticmethod
    def _memory_phrase(memory_hits: Iterable[MemoryFact]) -> str | None:
        for memory in memory_hits:
            fact = (memory.fact or "").strip()
            if fact:
                return fact
        return None

    @classmethod
    def _build_fallback_reply(
        cls,
        *,
        context: ChatContext,
        memory_hint: str | None,
    ) -> str:
        user_name = context.user_name or context.user_id
        latest_text = (context.latest_message_text or "").strip()
        if cls._contains_cjk(latest_text):
            pieces = [
                f"{user_name}\uff0c\u6211\u770b\u5230\u4f60\u521a\u521a\u8bf4\u201c{latest_text}\u201d\u3002",
                "\u6211\u60f3\u5148\u63a5\u4f4f\u4f60\u8fd9\u4e2a\u8bdd\u9898\uff0c\u518d\u966a\u4f60\u5f80\u4e0b\u804a\u3002",
                "\u5982\u679c\u4f60\u613f\u610f\uff0c\u4e5f\u53ef\u4ee5\u591a\u8bf4\u4e00\u70b9\u4f60\u73b0\u5728\u6700\u5728\u610f\u7684\u90a3\u90e8\u5206\u3002",
            ]
            if memory_hint:
                pieces.insert(
                    1,
                    f"\u6211\u8bb0\u5f97\u4e00\u4ef6\u548c\u4f60\u6709\u5173\u7684\u5c0f\u7ebf\u7d22\uff1a{memory_hint}\u3002",
                )
            return " ".join(pieces)

        pieces = [
            f"Hey {user_name}, I saw your message: \"{latest_text}\".",
            "I want to stay with this topic first instead of jumping too quickly into advice.",
            "If you want, tell me a bit more about the part that matters most right now.",
        ]
        if memory_hint:
            pieces.insert(1, f"I remember one useful detail about you: {memory_hint}.")
        return " ".join(pieces)

    @classmethod
    def _build_alternatives(
        cls,
        *,
        context: ChatContext,
        memory_hint: str | None,
    ) -> list[str]:
        latest_text = (context.latest_message_text or "").strip()
        if cls._contains_cjk(latest_text):
            options = [
                "\u542c\u8d77\u6765\u4f60\u521a\u7ecf\u5386\u4e86\u4e00\u4ef6\u633a\u5177\u4f53\u7684\u4e8b\uff0c\u6211\u60f3\u5148\u542c\u4f60\u628a\u7ec6\u8282\u8bb2\u5b8c\u3002",
                "\u5982\u679c\u4f60\u73b0\u5728\u66f4\u60f3\u8981\u7684\u662f\u5efa\u8bae\uff0c\u6211\u4e5f\u53ef\u4ee5\u5148\u5e2e\u4f60\u4e00\u8d77\u7406\u4e00\u7406\u63a5\u4e0b\u6765\u600e\u4e48\u505a\u3002",
            ]
            if memory_hint:
                options.insert(
                    1,
                    f"\u6211\u4e5f\u8054\u60f3\u5230\u4f60\u4e4b\u524d\u63d0\u8fc7\u7684\u8fd9\u70b9\uff1a{memory_hint}\u3002",
                )
            return options[:2]

        options = [
            "That sounds pretty immediate. I can listen first before jumping into advice.",
            "If you want, I can also help you sort out the next step instead of only reacting.",
        ]
        if memory_hint:
            options.insert(1, f"I also remember this detail about you: {memory_hint}.")
        return options[:2]

    @staticmethod
    def _contains_cjk(text: str) -> bool:
        return any("\u4e00" <= ch <= "\u9fff" for ch in text)

    def _build_system_prompt(self, *, agent: AgentProfile) -> str:
        return (
            "You are a chat suggestion planner for a long-term AI social agent.\n"
            "Your job is to decide whether the agent should reply right now and, if yes, draft one concise reply.\n"
            "Follow these rules:\n"
            "1. Stay aligned with the configured persona, tone, and relationship mode.\n"
            "2. Do not claim to be a specific real human.\n"
            "3. Avoid manipulative, coercive, or unsafe emotional pressure.\n"
            "4. Prefer warm, natural, and context-aware replies over generic compliments.\n"
            "5. Use memory hits only as light context. Do not overstate certainty.\n"
            f"6. Safety mode is `{agent.safety_mode.value}`.\n"
            "7. Return valid JSON only. Do not wrap it in markdown.\n"
            "8. Use this exact object shape and exact key names:\n"
            "{"
            "\"should_reply\": true,"
            "\"summary\": \"short planning summary\","
            "\"reply_draft\": \"one ready-to-send reply\","
            "\"alternatives\": [\"optional alt 1\", \"optional alt 2\"],"
            "\"rationale\": \"why this reply or why no reply\","
            "\"risk_flags\": [\"optional_flag\"]"
            "}.\n"
            "9. If should_reply is true, reply_draft must be a non-empty string.\n"
            "10. If should_reply is false, set reply_draft to an empty string."
        )

    @staticmethod
    def _build_user_prompt(
        *,
        agent: AgentProfile,
        context: ChatContext,
    ) -> str:
        recent_lines = []
        for event in context.recent_events:
            actor = event.actor_name or event.actor_id
            rendered = (event.text or "").strip() or f"<{event.content_type.value}>"
            recent_lines.append(
                f"- [{event.direction.value}] [{event.content_type.value}] {actor}: {rendered}",
            )
        memory_lines = [f"- [{memory.memory_type.value}] {memory.fact}" for memory in context.memory_hits]
        profile_lines: list[str] = []
        if context.memory_profile.preferences:
            profile_lines.append(f"- preferences: {'; '.join(context.memory_profile.preferences[:3])}")
        if context.memory_profile.relationships:
            profile_lines.append(f"- relationships: {'; '.join(context.memory_profile.relationships[:3])}")
        if context.memory_profile.facts:
            profile_lines.append(f"- facts: {'; '.join(context.memory_profile.facts[:3])}")
        if context.memory_profile.reflections:
            profile_lines.append(f"- reflections: {'; '.join(context.memory_profile.reflections[:2])}")
        facet_lines: list[str] = []
        for facet in context.memory_profile.facets[:4]:
            preferred_intents = ", ".join(intent.value for intent in facet.preferred_intents) or "general"
            evidence_preview = "; ".join(facet.evidence_facts[:2]) or "<none>"
            facet_lines.append(
                f"- [{facet.facet_type}] {facet.title}: {facet.summary} "
                f"(confidence={facet.confidence:.2f}; preferred_intents={preferred_intents}; evidence={evidence_preview})",
            )
        return (
            f"Agent display name: {agent.display_name}\n"
            f"Persona type: {agent.persona_type.value}\n"
            f"Relationship mode: {agent.relationship_mode}\n"
            f"Public disclosure: {agent.public_disclosure}\n"
            f"Core traits: {', '.join(agent.core_traits)}\n"
            f"Speech style: {json.dumps(agent.speech_style, ensure_ascii=False)}\n"
            f"Do-not-do rules: {', '.join(agent.do_not_do)}\n"
            f"Platform: {context.platform.value}\n"
            f"Channel type: {context.channel_type.value}\n"
            f"User id: {context.user_id}\n"
            f"User name: {context.user_name or context.user_id}\n"
            f"Detected user intent: {context.intent.value}\n"
            f"Latest message: {context.latest_message_text or ''}\n"
            f"Context summary: {context.summary or ''}\n"
            f"Memory candidate pool size: {context.memory_candidate_count}\n"
            f"User profile summary: {context.memory_profile.summary or '<none>'}\n"
            "Recent events:\n"
            f"{chr(10).join(recent_lines) or '- <none>'}\n"
            "User profile snapshot:\n"
            f"{chr(10).join(profile_lines) or '- <none>'}\n"
            "User profile facets:\n"
            f"{chr(10).join(facet_lines) or '- <none>'}\n"
            "Memory hits:\n"
            f"{chr(10).join(memory_lines) or '- <none>'}\n"
            "Memory retrieval notes:\n"
            f"{chr(10).join(f'- {note}' for note in context.memory_retrieval_notes) or '- <none>'}\n"
            "Please decide whether the agent should reply now and generate a natural draft.\n"
            "Use the profile snapshot as stable background, the profile facets as higher-level person-model hints, "
            "and the memory hits as turn-relevant long-term context.\n"
            "Return JSON only. Use key `reply_draft`, not `draft_reply`."
        )

    def _build_response_format(self) -> dict[str, object] | None:
        if "deepseek" in self.resolved_model.casefold():
            return {"type": "json_object"}
        return {
            "type": "json_schema",
            "json_schema": {
                "name": _CHAT_SUGGESTION_JSON_SCHEMA["name"],
                "strict": True,
                "schema": _CHAT_SUGGESTION_JSON_SCHEMA["schema"],
            },
        }

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
            raise RuntimeError(f"chat suggestion HTTP error {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"chat suggestion request failed: {exc}") from exc

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
                    if isinstance(content, list):
                        text_parts: list[str] = []
                        for item in content:
                            if isinstance(item, str):
                                text_parts.append(item)
                                continue
                            if isinstance(item, dict):
                                text = item.get("text")
                                if isinstance(text, str):
                                    text_parts.append(text)
                        joined = "\n".join(part for part in text_parts if part.strip()).strip()
                        if joined:
                            return joined
        raise RuntimeError("chat suggestion response did not contain a chat message content field")

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
        raise RuntimeError("chat suggestion response was not valid JSON")

    @staticmethod
    def _normalize_response_payload(parsed: dict[str, object]) -> dict[str, object]:
        envelope = parsed
        for key in ("result", "data", "output"):
            nested = envelope.get(key)
            if isinstance(nested, dict):
                envelope = nested
                break

        return {
            "should_reply": envelope.get("should_reply"),
            "summary": ChatSuggestionService._first_non_empty(
                envelope.get("summary"),
                envelope.get("summary_text"),
                envelope.get("plan"),
            ),
            "reply_draft": ChatSuggestionService._first_non_empty(
                envelope.get("reply_draft"),
                envelope.get("draft_reply"),
                envelope.get("suggested_reply"),
                envelope.get("reply"),
                envelope.get("message_text"),
            ),
            "alternatives": envelope.get("alternatives")
            or envelope.get("alternate_replies")
            or envelope.get("reply_options")
            or [],
            "rationale": ChatSuggestionService._first_non_empty(
                envelope.get("rationale"),
                envelope.get("reasoning"),
                envelope.get("why"),
            ),
            "risk_flags": envelope.get("risk_flags")
            or envelope.get("risks")
            or envelope.get("safety_flags")
            or [],
        }

    @staticmethod
    def _clean_string(value: object) -> str | None:
        if not isinstance(value, str):
            return None
        cleaned = " ".join(value.split()).strip()
        return cleaned or None

    @classmethod
    def _first_non_empty(cls, *values: object) -> str | None:
        for value in values:
            cleaned = cls._clean_string(value)
            if cleaned:
                return cleaned
        return None

    @staticmethod
    def _coerce_bool(value: object) -> bool | None:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().casefold()
            if normalized in {"true", "yes", "y", "1"}:
                return True
            if normalized in {"false", "no", "n", "0"}:
                return False
        if isinstance(value, (int, float)):
            return bool(value)
        return None

    @classmethod
    def _coerce_list(cls, value: object, *, limit: int = 3) -> list[str]:
        if isinstance(value, list):
            items = [cls._clean_string(item) for item in value]
            return [item for item in items if item][:limit]
        if isinstance(value, str):
            cleaned = cls._clean_string(value)
            return [cleaned] if cleaned else []
        return []
