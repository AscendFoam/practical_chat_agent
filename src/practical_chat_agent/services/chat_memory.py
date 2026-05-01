from __future__ import annotations

import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from practical_chat_agent.core.enums import MemoryType
from practical_chat_agent.core.models import AgentProfile, ChatContext, ChatMemoryCandidate, InboundEvent, MemoryFact, utc_now
from practical_chat_agent.services.memory_utils import (
    clean_memory_fact_text,
    memory_fact_similarity_key,
    merge_memory_fact_text,
)

_CHAT_MEMORY_JSON_SCHEMA: dict[str, object] = {
    "name": "chat_memory_candidates",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "memories": {
                "type": "array",
                "maxItems": 4,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "memory_type": {
                            "type": "string",
                            "enum": ["preference", "fact", "relationship", "reflection"],
                        },
                        "fact": {"type": "string"},
                        "salience": {"type": "number"},
                        "confidence": {"type": "number"},
                        "merge_with_memory_id": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                        },
                        "rationale": {"type": "string"},
                    },
                    "required": [
                        "memory_type",
                        "fact",
                        "salience",
                        "confidence",
                        "merge_with_memory_id",
                        "rationale",
                    ],
                },
            },
        },
        "required": ["memories"],
    },
}


class ChatMemoryExtractionService:
    """Extract long-term memory candidates from inbound messages."""

    backend_name = "chat_memory"

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
            return "chat memory extraction is disabled by configuration"
        if not self.api_key:
            return "OPENAI_API_KEY is not configured"
        if not self.base_url:
            return "OPENAI_BASE_URL is not configured"
        return None

    def extract(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        context: ChatContext,
    ) -> list[ChatMemoryCandidate]:
        remote_reason = self.availability_reason()
        if remote_reason is None:
            try:
                return self._extract_remote(agent=agent, event=event, context=context)
            except Exception:  # noqa: BLE001
                return self._extract_fallback(agent=agent, event=event, context=context)
        return self._extract_fallback(agent=agent, event=event, context=context)

    def materialize(
        self,
        *,
        candidates: list[ChatMemoryCandidate],
        existing_memories: list[MemoryFact] | None = None,
    ) -> list[MemoryFact]:
        existing_by_id = {memory.memory_id: memory for memory in existing_memories or []}
        existing_by_fact = {
            (memory.user_id, memory.memory_type, memory_fact_similarity_key(memory.fact)): memory
            for memory in existing_memories or []
            if memory.fact.strip()
        }

        facts: list[MemoryFact] = []
        seen: set[tuple[str, str, str]] = set()
        for candidate in candidates:
            normalized_fact = clean_memory_fact_text(candidate.fact)
            if not normalized_fact:
                continue
            fact_key = memory_fact_similarity_key(normalized_fact)
            dedupe_key = (candidate.agent_id, candidate.user_id, f"{candidate.memory_type.value}:{fact_key}")
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)

            target_memory = existing_by_id.get(candidate.merge_with_memory_id or "")
            if target_memory is None:
                target_memory = existing_by_fact.get(
                    (candidate.user_id, candidate.memory_type, fact_key),
                )

            evidence_refs = list(dict.fromkeys((target_memory.evidence_refs if target_memory else []) + candidate.evidence_refs))
            fact_text = normalized_fact
            if target_memory is not None:
                fact_text = merge_memory_fact_text(target_memory.fact, normalized_fact)
            if target_memory is not None:
                facts.append(
                    target_memory.model_copy(
                        update={
                            "memory_type": candidate.memory_type,
                            "fact": fact_text,
                            "salience": max(target_memory.salience, candidate.salience),
                            "confidence": max(target_memory.confidence, candidate.confidence),
                            "evidence_refs": evidence_refs,
                            "updated_at": utc_now(),
                        },
                    ),
                )
                continue
            facts.append(
                MemoryFact(
                    agent_id=candidate.agent_id,
                    user_id=candidate.user_id,
                    memory_type=candidate.memory_type,
                    fact=fact_text,
                    salience=candidate.salience,
                    confidence=candidate.confidence,
                    evidence_refs=evidence_refs,
                ),
            )
        return facts

    def _extract_remote(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        context: ChatContext,
    ) -> list[ChatMemoryCandidate]:
        payload: dict[str, object] = {
            "model": self.resolved_model,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": self._build_system_prompt(),
                },
                {
                    "role": "user",
                    "content": self._build_user_prompt(agent=agent, event=event, context=context),
                },
            ],
        }
        response_format = self._build_response_format()
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
        parsed = self._parse_json_content(content=self._extract_message_content(response=response))
        memories = self._extract_memory_items(parsed=parsed, context=context)

        candidates: list[ChatMemoryCandidate] = []
        for item in memories[:4]:
            fact = self._first_non_empty(
                item.get("fact"),
                item.get("memory"),
                item.get("memory_text"),
                item.get("text"),
            )
            merge_with_memory_id = self._clean_string(
                item.get("merge_with_memory_id") or item.get("merge_with"),
            )
            existing_target = next(
                (memory for memory in context.memory_hits if memory.memory_id == merge_with_memory_id),
                None,
            )
            if not fact and existing_target is not None:
                fact = existing_target.fact
            if not fact:
                continue
            salience_value = item.get("salience") if "salience" in item else item.get("importance")
            confidence_value = item.get("confidence") if "confidence" in item else item.get("certainty")
            candidates.append(
                ChatMemoryCandidate(
                    agent_id=agent.agent_id,
                    user_id=event.actor_id,
                    memory_type=self._parse_memory_type(
                        item.get("memory_type") or item.get("type") or item.get("category"),
                    ),
                    fact=fact,
                    salience=self._coerce_score(
                        salience_value if salience_value is not None else (existing_target.salience if existing_target else None),
                        default=0.65,
                    ),
                    confidence=self._coerce_score(
                        confidence_value if confidence_value is not None else (existing_target.confidence if existing_target else None),
                        default=0.7,
                    ),
                    evidence_refs=[event.event_id],
                    merge_with_memory_id=merge_with_memory_id,
                    rationale=self._first_non_empty(
                        item.get("rationale"),
                        item.get("reasoning"),
                        item.get("why"),
                    ),
                ),
            )
        return candidates

    def _extract_fallback(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        context: ChatContext,
    ) -> list[ChatMemoryCandidate]:
        text = " ".join((event.text or "").split()).strip()
        if not text:
            return []

        existing_by_fact = {
            (memory.memory_type, memory_fact_similarity_key(memory.fact)): memory
            for memory in context.memory_hits
            if memory.fact.strip()
        }
        candidates: list[ChatMemoryCandidate] = []

        rules: list[tuple[str, MemoryType, float, str]] = [
            (r"\bI like\s+(?P<value>.+)", MemoryType.PREFERENCE, 0.72, "User preference: {value}"),
            (r"\bI love\s+(?P<value>.+)", MemoryType.PREFERENCE, 0.72, "User preference: {value}"),
            (r"\bI prefer\s+(?P<value>.+)", MemoryType.PREFERENCE, 0.72, "User preference: {value}"),
            (r"\bmy favorite (?P<value>movie|music|food|drink|game|place|season|color) is (?P<detail>.+)", MemoryType.PREFERENCE, 0.78, "User favorite {value}: {detail}"),
            (r"\bI(?:'m| am) into (?P<value>.+)", MemoryType.PREFERENCE, 0.72, "User interest: {value}"),
            (r"\bI enjoy (?P<value>.+)", MemoryType.PREFERENCE, 0.72, "User preference: {value}"),
            (r"\bmy (?P<value>boyfriend|girlfriend|wife|husband|partner|boss|manager|mother|father|sister|brother)\b", MemoryType.RELATIONSHIP, 0.78, "User relationship detail: {value}"),
            (r"\bI(?:'m| am) close to my (?P<value>.+)", MemoryType.RELATIONSHIP, 0.76, "User close relationship: {value}"),
            (r"\bmy (?P<value>friend|roommate|coworker|colleague) (?P<detail>.+)", MemoryType.RELATIONSHIP, 0.72, "User relationship detail: {value} {detail}"),
            (r"\bI work as (?P<value>.+)", MemoryType.FACT, 0.68, "User fact: works as {value}"),
            (r"\bI am an?\s+(?P<value>.+)", MemoryType.FACT, 0.68, "User fact: is {value}"),
            (r"\bI live in\s+(?P<value>.+)", MemoryType.FACT, 0.68, "User fact: lives in {value}"),
            (r"\bI(?:'m| am) feeling (?P<value>.+)", MemoryType.REFLECTION, 0.82, "User emotional reflection: feeling {value}"),
            (r"\bI feel (?P<value>.+)", MemoryType.REFLECTION, 0.82, "User emotional reflection: feels {value}"),
            (r"\bI(?:'m| am) worried about (?P<value>.+)", MemoryType.REFLECTION, 0.82, "User concern: worried about {value}"),
            (r"\bI(?:'m| am) excited about (?P<value>.+)", MemoryType.REFLECTION, 0.78, "User positive anticipation: excited about {value}"),
            (r"\bI(?:'m| am) stressed(?: about)? (?P<value>.+)", MemoryType.REFLECTION, 0.82, "User stress point: {value}"),
            (r"\bI care a lot about (?P<value>.+)", MemoryType.REFLECTION, 0.76, "User value reflection: cares about {value}"),
            (r"\u6211\u559c\u6b22(?P<value>.+)", MemoryType.PREFERENCE, 0.72, "User preference: {value}"),
            (r"\u6211\u66f4\u559c\u6b22(?P<value>.+)", MemoryType.PREFERENCE, 0.72, "User preference: {value}"),
            (r"\u6211\u6700\u559c\u6b22(?P<value>.+)", MemoryType.PREFERENCE, 0.72, "User preference: {value}"),
            (r"\u6211\u5bf9(?P<value>.+)\u5f88\u611f\u5174\u8da3", MemoryType.PREFERENCE, 0.74, "User interest: {value}"),
            (r"\u6211\u7279\u522b\u559c\u6b22(?P<value>.+)", MemoryType.PREFERENCE, 0.76, "User preference: {value}"),
            (r"\u6211(?:\u7684)?(?P<value>\u7537\u670b\u53cb|\u5973\u670b\u53cb|\u8001\u5a46|\u8001\u516c|\u5bf9\u8c61|\u8001\u677f|\u9886\u5bfc|\u5988\u5988|\u7238\u7238|\u59d0\u59d0|\u54e5\u54e5|\u59b9\u59b9|\u5f1f\u5f1f)", MemoryType.RELATIONSHIP, 0.78, "User relationship detail: {value}"),
            (r"\u6211\u548c(?P<value>.+)\u5173\u7cfb(?P<detail>.+)", MemoryType.RELATIONSHIP, 0.76, "User relationship reflection: {value} {detail}"),
            (r"\u6211\u548c(?P<value>.+)\u5f88\u4eb2\u8fd1", MemoryType.RELATIONSHIP, 0.78, "User close relationship: {value}"),
            (r"\u6211\u5728(?P<value>.+)\u5de5\u4f5c", MemoryType.FACT, 0.68, "User fact: works in {value}"),
            (r"\u6211\u662f(?P<value>.+)", MemoryType.FACT, 0.68, "User fact: is {value}"),
            (r"\u6211\u4f4f\u5728(?P<value>.+)", MemoryType.FACT, 0.68, "User fact: lives in {value}"),
            (r"\u6211\u89c9\u5f97(?P<value>.+)", MemoryType.REFLECTION, 0.76, "User reflection: thinks {value}"),
            (r"\u6211\u73b0\u5728\u611f\u89c9(?P<value>.+)", MemoryType.REFLECTION, 0.82, "User emotional reflection: feels {value}"),
            (r"\u6211\u6709\u70b9(?P<value>\u7d27\u5f20|\u7126\u8651|\u96be\u8fc7|\u5f00\u5fc3|\u7d2f|\u70e6)", MemoryType.REFLECTION, 0.82, "User emotional reflection: feels {value}"),
            (r"\u6211\u62c5\u5fc3(?P<value>.+)", MemoryType.REFLECTION, 0.82, "User concern: worried about {value}"),
            (r"\u6211\u5f88\u671f\u5f85(?P<value>.+)", MemoryType.REFLECTION, 0.76, "User positive anticipation: looking forward to {value}"),
        ]

        for pattern, memory_type, salience, template in rules:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match is None:
                continue
            groups = match.groupdict()
            if "detail" in groups and groups.get("detail") is not None:
                raw_value = template.format(
                    value=" ".join((groups.get("value") or "").split()).strip(" .,!?;:\u3002\uff0c\uff01\uff1f"),
                    detail=" ".join((groups.get("detail") or "").split()).strip(" .,!?;:\u3002\uff0c\uff01\uff1f"),
                )
                fact = raw_value
                existing = existing_by_fact.get((memory_type, memory_fact_similarity_key(fact)))
                candidates.append(
                    ChatMemoryCandidate(
                        agent_id=agent.agent_id,
                        user_id=event.actor_id,
                        memory_type=memory_type,
                        fact=fact,
                        salience=salience,
                        confidence=0.78,
                        evidence_refs=[event.event_id],
                        merge_with_memory_id=existing.memory_id if existing is not None else None,
                        rationale="pattern_match",
                    ),
                )
                continue
            value = " ".join((match.group("value") or "").split()).strip(" .,!?;:\u3002\uff0c\uff01\uff1f")
            if not value:
                continue
            fact = template.format(value=value)
            existing = existing_by_fact.get((memory_type, memory_fact_similarity_key(fact)))
            candidates.append(
                ChatMemoryCandidate(
                    agent_id=agent.agent_id,
                    user_id=event.actor_id,
                    memory_type=memory_type,
                    fact=fact,
                    salience=salience,
                    confidence=0.78,
                    evidence_refs=[event.event_id],
                    merge_with_memory_id=existing.memory_id if existing is not None else None,
                    rationale="pattern_match",
                ),
            )

        if not candidates:
            word_count = len(text.split())
            reflection_fact = self._extract_reflection_fallback(text=text)
            if reflection_fact is not None:
                existing = existing_by_fact.get((MemoryType.REFLECTION, memory_fact_similarity_key(reflection_fact)))
                candidates.append(
                    ChatMemoryCandidate(
                        agent_id=agent.agent_id,
                        user_id=event.actor_id,
                        memory_type=MemoryType.REFLECTION,
                        fact=reflection_fact,
                        salience=0.72,
                        confidence=0.66,
                        evidence_refs=[event.event_id],
                        merge_with_memory_id=existing.memory_id if existing is not None else None,
                        rationale="reflection_fallback",
                    ),
                )
            elif word_count >= 8 and self._looks_durable(text=text):
                compact = text if len(text) <= 140 else f"{text[:137].rstrip()}..."
                fallback_fact = f"User shared: {compact}"
                existing = existing_by_fact.get((MemoryType.FACT, memory_fact_similarity_key(fallback_fact)))
                candidates.append(
                    ChatMemoryCandidate(
                        agent_id=agent.agent_id,
                        user_id=event.actor_id,
                        memory_type=MemoryType.FACT,
                        fact=fallback_fact,
                        salience=0.58,
                        confidence=0.55,
                        evidence_refs=[event.event_id],
                        merge_with_memory_id=existing.memory_id if existing is not None else None,
                        rationale="durable_length_heuristic",
                    ),
                )

        return self._dedupe_candidates(candidates)[:4]

    @staticmethod
    def _looks_durable(*, text: str) -> bool:
        lowered = text.casefold()
        ephemeral_hints = (
            "today",
            "tonight",
            "right now",
            "\u4eca\u5929",
            "\u521a\u521a",
            "\u73b0\u5728",
            "\u9a6c\u4e0a",
        )
        return not any(hint in lowered for hint in ephemeral_hints)

    @staticmethod
    def _extract_reflection_fallback(*, text: str) -> str | None:
        lowered = text.casefold()
        reflection_markers = (
            "i feel",
            "i'm feeling",
            "i am feeling",
            "i'm worried",
            "i am worried",
            "i'm stressed",
            "i am stressed",
            "i care a lot about",
            "\u6211\u89c9\u5f97",
            "\u6211\u611f\u89c9",
            "\u6211\u62c5\u5fc3",
            "\u6211\u6709\u70b9",
            "\u6211\u5f88\u671f\u5f85",
        )
        if any(marker in lowered for marker in reflection_markers):
            compact = text if len(text) <= 140 else f"{text[:137].rstrip()}..."
            return f"User reflection: {compact}"
        return None

    @staticmethod
    def _dedupe_candidates(candidates: list[ChatMemoryCandidate]) -> list[ChatMemoryCandidate]:
        kept: dict[tuple[str, str, str], ChatMemoryCandidate] = {}
        for candidate in candidates:
            fact_key = memory_fact_similarity_key(candidate.fact)
            if not fact_key:
                continue
            key = (candidate.agent_id, candidate.user_id, f"{candidate.memory_type.value}:{fact_key}")
            existing = kept.get(key)
            if existing is None or (candidate.salience, candidate.confidence) > (existing.salience, existing.confidence):
                kept[key] = candidate
        return sorted(
            kept.values(),
            key=lambda candidate: (candidate.salience, candidate.confidence, len(candidate.fact)),
            reverse=True,
        )

    @staticmethod
    def _parse_memory_type(value: object) -> MemoryType:
        if isinstance(value, str):
            normalized = value.strip().casefold()
            mapping = {
                "preference": MemoryType.PREFERENCE,
                "fact": MemoryType.FACT,
                "relationship": MemoryType.RELATIONSHIP,
                "reflection": MemoryType.REFLECTION,
            }
            if normalized in mapping:
                return mapping[normalized]
        return MemoryType.FACT

    @staticmethod
    def _coerce_score(value: object, *, default: float) -> float:
        try:
            return max(0.0, min(float(value), 1.0))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _clean_string(value: object) -> str | None:
        if not isinstance(value, str):
            return None
        cleaned = " ".join(value.split()).strip()
        return cleaned or None

    def _build_system_prompt(self) -> str:
        return (
            "You extract durable memory candidates for a long-term chat agent.\n"
            "Only keep information that is likely useful in future conversations.\n"
            "Prefer stable facts, preferences, relationship details, and meaningful reflections.\n"
            "Preferences include favorites, interests, dislikes, recurring tastes, and activity preferences.\n"
            "Relationship details include partner/family/friend/coworker ties and the tone of those ties.\n"
            "Reflections include stable emotional patterns, concerns, values, goals, and what the user cares about.\n"
            "Avoid short-lived details like one-off timestamps, transient logistics, or exact copy-paste restatements.\n"
            "If a new fact is the same as an existing memory hit, still return one memory item and set merge_with_memory_id to that memory id.\n"
            "Return JSON only. Do not wrap it in markdown.\n"
            "Use this exact top-level shape and exact key names:\n"
            "{"
            "\"memories\": ["
            "{"
            "\"memory_type\": \"preference|fact|relationship|reflection\","
            "\"fact\": \"durable fact text\","
            "\"salience\": 0.0,"
            "\"confidence\": 0.0,"
            "\"merge_with_memory_id\": null,"
            "\"rationale\": \"short reason\""
            "}"
            "]"
            "}.\n"
            "If nothing durable should be stored, return {\"memories\": []}.\n"
            "Do not use alternate top-level keys such as new_memories."
        )

    @staticmethod
    def _build_user_prompt(
        *,
        agent: AgentProfile,
        event: InboundEvent,
        context: ChatContext,
    ) -> str:
        memory_lines = [
            f"- id={memory.memory_id} [{memory.memory_type.value}] {memory.fact}"
            for memory in context.memory_hits
        ]
        profile_lines: list[str] = []
        if context.memory_profile.preferences:
            profile_lines.append(f"- preferences: {'; '.join(context.memory_profile.preferences[:3])}")
        if context.memory_profile.relationships:
            profile_lines.append(f"- relationships: {'; '.join(context.memory_profile.relationships[:3])}")
        if context.memory_profile.reflections:
            profile_lines.append(f"- reflections: {'; '.join(context.memory_profile.reflections[:2])}")
        if context.memory_profile.facts:
            profile_lines.append(f"- facts: {'; '.join(context.memory_profile.facts[:2])}")
        facet_lines: list[str] = []
        for facet in context.memory_profile.facets[:4]:
            preferred_intents = ", ".join(intent.value for intent in facet.preferred_intents) or "general"
            facet_lines.append(
                f"- [{facet.facet_type}] {facet.title}: {facet.summary} "
                f"(confidence={facet.confidence:.2f}; preferred_intents={preferred_intents})",
            )
        return (
            f"Agent display name: {agent.display_name}\n"
            f"Persona type: {agent.persona_type.value}\n"
            f"User id: {event.actor_id}\n"
            f"User name: {event.actor_name or event.actor_id}\n"
            f"Latest inbound message: {event.text or ''}\n"
            f"Context summary: {context.summary or ''}\n"
            f"Current user profile summary: {context.memory_profile.summary or '<none>'}\n"
            "Existing memory hits:\n"
            f"{chr(10).join(memory_lines) or '- <none>'}\n"
            "Current user profile snapshot:\n"
            f"{chr(10).join(profile_lines) or '- <none>'}\n"
            "Current user profile facets:\n"
            f"{chr(10).join(facet_lines) or '- <none>'}\n"
            "Please extract only durable memories from the latest message.\n"
            "Prefer preference / relationship / reflection memories when the user reveals them clearly.\n"
            "Use profile facets as consolidation hints so near-duplicate themes do not become fragmented memories.\n"
            "Return JSON only and use key `memories`."
        )

    def _build_response_format(self) -> dict[str, object] | None:
        if "deepseek" in self.resolved_model.casefold():
            return {"type": "json_object"}
        return {
            "type": "json_schema",
            "json_schema": {
                "name": _CHAT_MEMORY_JSON_SCHEMA["name"],
                "strict": True,
                "schema": _CHAT_MEMORY_JSON_SCHEMA["schema"],
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
            raise RuntimeError(f"chat memory HTTP error {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"chat memory request failed: {exc}") from exc

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
        raise RuntimeError("chat memory response did not contain a chat message content field")

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
        raise RuntimeError("chat memory response was not valid JSON")

    def _extract_memory_items(
        self,
        *,
        parsed: dict[str, object],
        context: ChatContext,
    ) -> list[dict[str, object]]:
        envelope = parsed
        for key in ("result", "data", "output"):
            nested = envelope.get(key)
            if isinstance(nested, dict):
                envelope = nested
                break

        raw_items = envelope.get("memories")
        if not isinstance(raw_items, list):
            raw_items = envelope.get("new_memories")
        if not isinstance(raw_items, list):
            raw_items = envelope.get("memory_candidates")
        if not isinstance(raw_items, list):
            single_item = envelope.get("memory")
            if isinstance(single_item, dict):
                raw_items = [single_item]
            elif any(
                key in envelope
                for key in ("memory_type", "fact", "memory", "memory_text", "text", "merge_with_memory_id")
            ):
                raw_items = [envelope]
            else:
                raw_items = []

        items: list[dict[str, object]] = []
        for item in raw_items:
            if isinstance(item, dict):
                items.append(item)
                continue
            if isinstance(item, str):
                items.append({"fact": item})

        top_level_merge_id = self._clean_string(envelope.get("merge_with_memory_id"))
        if top_level_merge_id and not items:
            existing = next(
                (memory for memory in context.memory_hits if memory.memory_id == top_level_merge_id),
                None,
            )
            if existing is not None:
                items.append(
                    {
                        "memory_type": existing.memory_type.value,
                        "fact": existing.fact,
                        "salience": existing.salience,
                        "confidence": existing.confidence,
                        "merge_with_memory_id": existing.memory_id,
                        "rationale": "duplicate_reference_only",
                    },
                )

        for item in items:
            if "merge_with_memory_id" not in item and top_level_merge_id:
                item["merge_with_memory_id"] = top_level_merge_id
        return items[:4]

    @classmethod
    def _first_non_empty(cls, *values: object) -> str | None:
        for value in values:
            cleaned = cls._clean_string(value)
            if cleaned:
                return cleaned
        return None
