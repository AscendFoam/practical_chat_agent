from __future__ import annotations

import json
import re
from collections import defaultdict
from collections.abc import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from practical_chat_agent.core.enums import ChatIntent, MemoryType
from practical_chat_agent.core.models import (
    AgentProfile,
    InboundEvent,
    MemoryFact,
    MemoryProfileFacet,
    MemoryProfileSnapshot,
    MemoryRetrievalResult,
)
from practical_chat_agent.services.memory_utils import clean_memory_fact_text, memory_fact_similarity_key

_PROFILE_FACETS_JSON_SCHEMA: dict[str, object] = {
    "name": "memory_profile_facets",
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "facets": {
                "type": "array",
                "maxItems": 6,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "facet_type": {"type": "string"},
                        "title": {"type": "string"},
                        "summary": {"type": "string"},
                        "confidence": {"type": "number"},
                        "evidence_memory_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "maxItems": 6,
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "maxItems": 8,
                        },
                        "preferred_intents": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "general",
                                    "greeting",
                                    "plan",
                                    "emotion",
                                    "relationship",
                                    "preference",
                                    "work",
                                ],
                            },
                            "maxItems": 4,
                        },
                    },
                    "required": [
                        "facet_type",
                        "title",
                        "summary",
                        "confidence",
                        "evidence_memory_ids",
                        "tags",
                        "preferred_intents",
                    ],
                },
            },
        },
        "required": ["facets"],
    },
}

_GREETING_HINTS = (
    "how are you",
    "how was your day",
    "hello",
    "hi ",
    "hey ",
    "\u4f60\u597d",
    "\u5728\u5417",
    "\u6700\u8fd1\u600e\u4e48\u6837",
    "\u4e0b\u73ed",
)

_PLAN_HINTS = (
    "tonight",
    "weekend",
    "tomorrow",
    "this weekend",
    "free to",
    "plan",
    "schedule",
    "meet",
    "chat tonight",
    "brunch",
    "restaurant",
    "cafe",
    "place to",
    "where should",
    "where can",
    "recommend",
    "\u4eca\u665a",
    "\u660e\u5929",
    "\u5468\u672b",
    "\u6709\u7a7a",
    "\u5b89\u6392",
    "\u89c1\u9762",
    "\u9910\u5385",
    "\u5496\u5561\u5e97",
    "\u53bb\u54ea",
    "\u63a8\u8350",
)

_EMOTION_HINTS = (
    "feel",
    "feeling",
    "sad",
    "upset",
    "anxious",
    "stressed",
    "overwhelmed",
    "\u5f00\u5fc3",
    "\u96be\u8fc7",
    "\u7126\u8651",
    "\u7d2f",
    "\u70e6",
    "\u538b\u529b",
)

_RELATIONSHIP_HINTS = (
    "boyfriend",
    "girlfriend",
    "partner",
    "wife",
    "husband",
    "family",
    "friend",
    "\u670b\u53cb",
    "\u5bf9\u8c61",
    "\u7537\u670b\u53cb",
    "\u5973\u670b\u53cb",
    "\u5bb6\u4eba",
    "\u7238\u5988",
)

_PREFERENCE_HINTS = (
    "like",
    "love",
    "prefer",
    "favorite",
    "\u559c\u6b22",
    "\u504f\u597d",
    "\u6700\u7231",
    "\u7231\u5403",
    "\u60f3\u5403",
)

_WORK_HINTS = (
    "work",
    "office",
    "project",
    "meeting",
    "boss",
    "deadline",
    "\u540c\u4e8b",
    "\u5de5\u4f5c",
    "\u9879\u76ee",
    "\u5f00\u4f1a",
    "\u4e0a\u73ed",
    "\u8001\u677f",
)

_PREFERENCE_THEME_RULES: tuple[
    tuple[str, str, tuple[str, ...], tuple[ChatIntent, ...], tuple[str, ...]],
    ...,
] = (
    (
        "food_and_drink",
        "Food And Drink Tastes",
        (
            "food",
            "drink",
            "coffee",
            "tea",
            "sushi",
            "matcha",
            "dessert",
            "restaurant",
            "cafe",
            "\u5403",
            "\u559d",
            "\u5496\u5561",
            "\u5976\u8336",
            "\u62b9\u8336",
            "\u5bff\u53f8",
            "\u9910\u5385",
        ),
        (ChatIntent.PLAN, ChatIntent.PREFERENCE, ChatIntent.GREETING),
        ("food", "drink", "taste", "cafe", "restaurant", "brunch", "matcha", "sushi"),
    ),
    (
        "social_style",
        "Social Style",
        (
            "quiet weekend",
            "quiet weekends",
            "small group",
            "cozy",
            "stay in",
            "one-on-one",
            "\u5b89\u9759",
            "\u5b85",
            "\u5c0f\u8303\u56f4",
            "\u4e24\u4e2a\u4eba",
        ),
        (ChatIntent.PLAN, ChatIntent.GREETING, ChatIntent.RELATIONSHIP),
        ("quiet", "cozy", "weekend", "small-group", "one-on-one"),
    ),
    (
        "creative_interests",
        "Creative Interests",
        (
            "music",
            "movie",
            "film",
            "book",
            "reading",
            "photography",
            "art",
            "\u5199\u4f5c",
            "\u97f3\u4e50",
            "\u7535\u5f71",
            "\u770b\u4e66",
            "\u6444\u5f71",
            "\u753b\u753b",
        ),
        (ChatIntent.GREETING, ChatIntent.PREFERENCE, ChatIntent.PLAN),
        ("music", "movie", "book", "reading", "art", "photography"),
    ),
    (
        "outdoor_travel",
        "Outdoor And Travel Tastes",
        (
            "travel",
            "trip",
            "hiking",
            "walk",
            "beach",
            "mountain",
            "\u65c5\u884c",
            "\u5f92\u6b65",
            "\u6563\u6b65",
            "\u6d77\u8fb9",
            "\u722c\u5c71",
        ),
        (ChatIntent.PLAN, ChatIntent.GREETING, ChatIntent.PREFERENCE),
        ("travel", "trip", "walk", "hiking", "beach", "mountain"),
    ),
)

_REFLECTION_THEME_RULES: tuple[
    tuple[str, str, tuple[str, ...], tuple[ChatIntent, ...], tuple[str, ...], str],
    ...,
] = (
    (
        "work_stress",
        "Work Stress Pattern",
        (
            "work",
            "office",
            "project",
            "deadline",
            "meeting",
            "boss",
            "career",
            "\u5de5\u4f5c",
            "\u4e0a\u73ed",
            "\u9879\u76ee",
            "\u622a\u6b62",
            "\u8001\u677f",
            "\u4f1a\u8bae",
        ),
        (ChatIntent.EMOTION, ChatIntent.WORK, ChatIntent.GREETING),
        ("work", "stress", "pressure", "deadline", "project"),
        "Often feels pressure around work, projects, or deadlines.",
    ),
    (
        "emotional_overload",
        "Emotional Load Pattern",
        (
            "overwhelmed",
            "drained",
            "tired",
            "burned out",
            "stressed",
            "anxious",
            "\u75b2\u60eb",
            "\u7d2f",
            "\u7126\u8651",
            "\u538b\u529b",
            "\u70e6",
            "\u5d29\u6e83",
        ),
        (ChatIntent.EMOTION, ChatIntent.GREETING, ChatIntent.RELATIONSHIP),
        ("anxious", "overwhelmed", "drained", "stress", "emotion"),
        "Can feel anxious, overwhelmed, or drained on heavy days.",
    ),
    (
        "meaning_values",
        "Meaning And Values Pattern",
        (
            "meaningful",
            "purpose",
            "care about",
            "value",
            "\u6210\u957f",
            "\u610f\u4e49",
            "\u4ef7\u503c",
            "\u5728\u610f",
            "\u91cd\u89c6",
        ),
        (ChatIntent.EMOTION, ChatIntent.WORK, ChatIntent.GREETING),
        ("meaning", "value", "growth", "purpose"),
        "Cares about meaningful work, growth, or living by personal values.",
    ),
    (
        "relationship_sensitivity",
        "Relationship Sensitivity Pattern",
        (
            "lonely",
            "miss",
            "closeness",
            "distance",
            "misunderstood",
            "\u966a\u4f34",
            "\u5b64\u72ec",
            "\u60f3\u5ff5",
            "\u8bef\u89e3",
            "\u5173\u7cfb",
        ),
        (ChatIntent.RELATIONSHIP, ChatIntent.EMOTION, ChatIntent.GREETING),
        ("relationship", "closeness", "distance", "lonely", "support"),
        "Is sensitive to closeness, distance, and emotional understanding in relationships.",
    ),
)


class MemoryRetrievalService:
    """Select turn-relevant memories using joint intent and profile-facet scoring."""

    backend_name = "memory_retrieval"

    def __init__(
        self,
        *,
        selection_limit: int = 8,
        candidate_multiplier: int = 4,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout_seconds: float = 20.0,
        enabled: bool = True,
        default_model: str = "deepseek-chat",
    ) -> None:
        self.selection_limit = max(int(selection_limit), 1)
        self.candidate_multiplier = max(int(candidate_multiplier), 1)
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
            return "profile facet inference is disabled by configuration"
        if not self.api_key:
            return "OPENAI_API_KEY is not configured"
        if not self.base_url:
            return "OPENAI_BASE_URL is not configured"
        return None

    def retrieve(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        candidate_memories: list[MemoryFact],
    ) -> MemoryRetrievalResult:
        deduped_candidates = self._dedupe_candidates(candidate_memories)
        intent = self._classify_intent(event=event)
        profile, facet_backend = self._build_profile_snapshot(
            agent=agent,
            event=event,
            intent=intent,
            memories=deduped_candidates,
        )
        ranked_hits = self._rank_memories(
            agent=agent,
            event=event,
            intent=intent,
            memories=deduped_candidates,
            profile=profile,
        )[: self.selection_limit]
        notes = [
            f"detected intent: {intent.value}",
            f"scanned {len(candidate_memories)} memory candidates",
            f"deduped to {len(deduped_candidates)} unique memory facts",
            f"selected top {len(ranked_hits)} long-term memory hits",
            f"profile facets backend: {facet_backend}",
        ]
        if profile.facets:
            notes.append(f"profile facets ready with {len(profile.facets)} facets")
        if profile.summary:
            notes.append(f"profile summary ready with {self._profile_item_count(profile)} items")
        return MemoryRetrievalResult(
            user_id=event.actor_id,
            intent=intent,
            candidate_count=len(deduped_candidates),
            selected_hits=ranked_hits,
            profile=profile,
            retrieval_notes=notes,
        )

    def _dedupe_candidates(self, memories: list[MemoryFact]) -> list[MemoryFact]:
        kept_by_key: dict[tuple[str, str], MemoryFact] = {}
        for memory in memories:
            fact_key = memory_fact_similarity_key(memory.fact)
            if not fact_key:
                continue
            key = (memory.memory_type.value, fact_key)
            existing = kept_by_key.get(key)
            if existing is None or self._memory_priority(memory) > self._memory_priority(existing):
                kept_by_key[key] = memory
        return sorted(
            kept_by_key.values(),
            key=lambda memory: self._memory_priority(memory),
            reverse=True,
        )

    def _rank_memories(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        intent: ChatIntent,
        memories: list[MemoryFact],
        profile: MemoryProfileSnapshot,
    ) -> list[MemoryFact]:
        latest_text = clean_memory_fact_text(event.text).casefold()
        latest_tokens = self._extract_tokens(latest_text)
        interest_tokens = {token.casefold() for token in agent.interests}
        memory_facet_map = self._map_memory_facets(profile.facets)
        return sorted(
            memories,
            key=lambda memory: self._ranking_tuple(
                memory=memory,
                latest_text=latest_text,
                latest_tokens=latest_tokens,
                interest_tokens=interest_tokens,
                intent=intent,
                related_facets=memory_facet_map.get(memory.memory_id, ()),
            ),
            reverse=True,
        )

    def _ranking_tuple(
        self,
        *,
        memory: MemoryFact,
        latest_text: str,
        latest_tokens: set[str],
        interest_tokens: set[str],
        intent: ChatIntent,
        related_facets: tuple[MemoryProfileFacet, ...],
    ) -> tuple[float, float, float, float, float, float, float, float, float]:
        fact_text = clean_memory_fact_text(memory.fact)
        fact_text_lower = fact_text.casefold()
        fact_tokens = self._extract_tokens(fact_text_lower)
        lexical_overlap = len(latest_tokens & fact_tokens)
        substring_hit = 1.0 if latest_text and latest_text in fact_text_lower else 0.0
        topic_overlap = len(interest_tokens & fact_tokens)
        type_weight = self._intent_type_weight(intent=intent, memory_type=memory.memory_type)
        intent_phrase_bonus = self._intent_phrase_bonus(
            intent=intent,
            memory_type=memory.memory_type,
            fact_text=fact_text_lower,
        )
        facet_intent_bonus = self._facet_intent_bonus(
            intent=intent,
            related_facets=related_facets,
        )
        facet_overlap_bonus = self._facet_overlap_bonus(
            latest_text=latest_text,
            latest_tokens=latest_tokens,
            related_facets=related_facets,
        )
        recency = memory.updated_at.timestamp()
        return (
            lexical_overlap + substring_hit,
            facet_intent_bonus,
            facet_overlap_bonus,
            intent_phrase_bonus,
            topic_overlap,
            memory.salience * type_weight,
            memory.confidence,
            len(fact_text),
            recency,
        )

    def _classify_intent(self, *, event: InboundEvent) -> ChatIntent:
        text = clean_memory_fact_text(event.text).casefold()
        if not text:
            return ChatIntent.GENERAL
        if self._contains_any(text, _GREETING_HINTS):
            return ChatIntent.GREETING
        if self._contains_any(text, _PLAN_HINTS):
            return ChatIntent.PLAN
        if self._contains_any(text, _EMOTION_HINTS):
            return ChatIntent.EMOTION
        if self._contains_any(text, _RELATIONSHIP_HINTS):
            return ChatIntent.RELATIONSHIP
        if self._contains_any(text, _PREFERENCE_HINTS):
            return ChatIntent.PREFERENCE
        if self._contains_any(text, _WORK_HINTS):
            return ChatIntent.WORK
        return ChatIntent.GENERAL

    @staticmethod
    def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
        return any(needle in text for needle in needles)

    @staticmethod
    def _intent_type_weight(*, intent: ChatIntent, memory_type: MemoryType) -> float:
        default_weights = {
            MemoryType.PREFERENCE: 1.10,
            MemoryType.RELATIONSHIP: 1.08,
            MemoryType.FACT: 1.0,
            MemoryType.REFLECTION: 0.98,
        }
        overrides: dict[ChatIntent, dict[MemoryType, float]] = {
            ChatIntent.GREETING: {
                MemoryType.RELATIONSHIP: 1.22,
                MemoryType.REFLECTION: 1.16,
                MemoryType.PREFERENCE: 1.06,
                MemoryType.FACT: 1.0,
            },
            ChatIntent.PLAN: {
                MemoryType.PREFERENCE: 1.24,
                MemoryType.RELATIONSHIP: 1.16,
                MemoryType.FACT: 1.08,
                MemoryType.REFLECTION: 0.96,
            },
            ChatIntent.EMOTION: {
                MemoryType.REFLECTION: 1.28,
                MemoryType.RELATIONSHIP: 1.16,
                MemoryType.PREFERENCE: 1.02,
                MemoryType.FACT: 0.98,
            },
            ChatIntent.RELATIONSHIP: {
                MemoryType.RELATIONSHIP: 1.30,
                MemoryType.REFLECTION: 1.10,
                MemoryType.FACT: 1.02,
                MemoryType.PREFERENCE: 0.98,
            },
            ChatIntent.PREFERENCE: {
                MemoryType.PREFERENCE: 1.32,
                MemoryType.FACT: 1.02,
                MemoryType.RELATIONSHIP: 1.0,
                MemoryType.REFLECTION: 0.98,
            },
            ChatIntent.WORK: {
                MemoryType.FACT: 1.20,
                MemoryType.REFLECTION: 1.05,
                MemoryType.RELATIONSHIP: 1.0,
                MemoryType.PREFERENCE: 0.96,
            },
        }
        return overrides.get(intent, default_weights).get(memory_type, default_weights.get(memory_type, 1.0))

    @staticmethod
    def _intent_phrase_bonus(
        *,
        intent: ChatIntent,
        memory_type: MemoryType,
        fact_text: str,
    ) -> float:
        phrase_map: dict[ChatIntent, tuple[tuple[str, ...], tuple[MemoryType, ...]]] = {
            ChatIntent.GREETING: (
                ("day", "mood", "feeling", "\u4e0b\u73ed", "\u72b6\u6001", "\u6700\u8fd1"),
                (MemoryType.REFLECTION, MemoryType.RELATIONSHIP, MemoryType.FACT),
            ),
            ChatIntent.PLAN: (
                ("weekend", "travel", "food", "schedule", "\u4eca\u665a", "\u5468\u672b", "\u5b89\u6392", "\u6709\u7a7a"),
                (MemoryType.PREFERENCE, MemoryType.FACT, MemoryType.RELATIONSHIP),
            ),
            ChatIntent.EMOTION: (
                ("stress", "tired", "happy", "sad", "\u7126\u8651", "\u96be\u8fc7", "\u5f00\u5fc3", "\u7d2f"),
                (MemoryType.REFLECTION, MemoryType.RELATIONSHIP),
            ),
            ChatIntent.RELATIONSHIP: (
                ("boyfriend", "girlfriend", "partner", "\u5bb6\u4eba", "\u5bf9\u8c61", "\u670b\u53cb"),
                (MemoryType.RELATIONSHIP,),
            ),
            ChatIntent.PREFERENCE: (
                ("like", "love", "prefer", "favorite", "\u559c\u6b22", "\u6700\u7231", "\u504f\u597d"),
                (MemoryType.PREFERENCE,),
            ),
            ChatIntent.WORK: (
                ("work", "project", "office", "meeting", "\u5de5\u4f5c", "\u9879\u76ee", "\u5f00\u4f1a"),
                (MemoryType.FACT, MemoryType.REFLECTION),
            ),
        }
        phrases, allowed_types = phrase_map.get(intent, ((), ()))
        if memory_type not in allowed_types:
            return 0.0
        return 1.0 if any(phrase in fact_text for phrase in phrases) else 0.0

    def _build_profile_snapshot(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        intent: ChatIntent,
        memories: list[MemoryFact],
    ) -> tuple[MemoryProfileSnapshot, str]:
        grouped_memories: dict[MemoryType, list[MemoryFact]] = defaultdict(list)
        for memory in memories:
            fact = clean_memory_fact_text(memory.fact)
            if not fact:
                continue
            grouped_memories[memory.memory_type].append(memory)

        facets, facet_backend = self._build_profile_facets(
            agent=agent,
            event=event,
            intent=intent,
            memories=memories,
        )
        preferences = [clean_memory_fact_text(memory.fact) for memory in grouped_memories.get(MemoryType.PREFERENCE, [])[:4]]
        facts = [clean_memory_fact_text(memory.fact) for memory in grouped_memories.get(MemoryType.FACT, [])[:4]]
        relationships = [
            clean_memory_fact_text(memory.fact)
            for memory in grouped_memories.get(MemoryType.RELATIONSHIP, [])[:4]
        ]
        reflections = [clean_memory_fact_text(memory.fact) for memory in grouped_memories.get(MemoryType.REFLECTION, [])[:4]]

        summary_parts: list[str] = []
        if preferences:
            summary_parts.append("preferences: " + "; ".join(preferences[:2]))
        if relationships:
            summary_parts.append("relationships: " + "; ".join(relationships[:2]))
        if facts:
            summary_parts.append("facts: " + "; ".join(facts[:2]))
        if reflections:
            summary_parts.append("reflections: " + "; ".join(reflections[:2]))
        if facets:
            summary_parts.append(
                "profile facets: "
                + " | ".join(
                    f"{facet.title}: {self._shorten_text(facet.summary, limit=96)}"
                    for facet in facets[:3]
                ),
            )

        return (
            MemoryProfileSnapshot(
                preferences=preferences,
                facts=facts,
                relationships=relationships,
                reflections=reflections,
                facets=facets,
                summary=" | ".join(summary_parts) if summary_parts else None,
            ),
            facet_backend,
        )

    def _build_profile_facets(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        intent: ChatIntent,
        memories: list[MemoryFact],
    ) -> tuple[list[MemoryProfileFacet], str]:
        remote_reason = self.availability_reason()
        if remote_reason is None and memories:
            try:
                facets = self._build_profile_facets_remote(
                    agent=agent,
                    event=event,
                    intent=intent,
                    memories=memories,
                )
                if facets:
                    return facets, "llm_profile_facets"
            except Exception:
                pass
        return self._build_profile_facets_fallback(memories=memories), "heuristic_profile_facets"

    def _build_profile_facets_remote(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        intent: ChatIntent,
        memories: list[MemoryFact],
    ) -> list[MemoryProfileFacet]:
        payload: dict[str, object] = {
            "model": self.resolved_model,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": self._build_facet_system_prompt(),
                },
                {
                    "role": "user",
                    "content": self._build_facet_user_prompt(
                        agent=agent,
                        event=event,
                        intent=intent,
                        memories=memories,
                    ),
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
        parsed = self._parse_json_content(
            content=self._extract_message_content(response=response),
        )
        facets = self._extract_profile_facets(parsed=parsed, memories=memories)
        if not facets:
            raise RuntimeError("profile facet model returned no usable facets")
        return facets

    def _build_profile_facets_fallback(self, *, memories: list[MemoryFact]) -> list[MemoryProfileFacet]:
        grouped: dict[MemoryType, list[MemoryFact]] = defaultdict(list)
        for memory in memories:
            grouped[memory.memory_type].append(memory)

        facets: list[MemoryProfileFacet] = []
        facets.extend(self._build_preference_facets(grouped.get(MemoryType.PREFERENCE, [])))
        facets.extend(self._build_reflection_facets(grouped.get(MemoryType.REFLECTION, [])))
        facets.extend(self._build_relationship_facets(grouped.get(MemoryType.RELATIONSHIP, [])))
        facets.extend(self._build_fact_facets(grouped.get(MemoryType.FACT, [])))
        return self._dedupe_facets(facets)[:6]

    def _build_preference_facets(self, memories: list[MemoryFact]) -> list[MemoryProfileFacet]:
        themed: dict[str, list[MemoryFact]] = defaultdict(list)
        leftovers: list[MemoryFact] = []
        for memory in memories:
            body = self._memory_body(memory.fact).casefold()
            matched_theme = None
            for theme_key, _title, needles, _intents, _tags in _PREFERENCE_THEME_RULES:
                if any(needle in body for needle in needles):
                    matched_theme = theme_key
                    break
            if matched_theme is None:
                leftovers.append(memory)
                continue
            themed[matched_theme].append(memory)

        facets: list[MemoryProfileFacet] = []
        for theme_key, title, _needles, preferred_intents, tags in _PREFERENCE_THEME_RULES:
            cluster = themed.get(theme_key, [])
            if not cluster:
                continue
            facts = self._unique_memory_facts(cluster)
            summary = self._summarize_cluster(
                intro="Often enjoys",
                facts=facts,
            )
            facets.append(
                self._make_facet(
                    facet_type="preference_cluster",
                    title=title,
                    summary=summary,
                    memories=cluster,
                    tags=tags,
                    preferred_intents=preferred_intents,
                ),
            )

        if leftovers:
            facets.append(
                self._make_facet(
                    facet_type="preference_cluster",
                    title="General Preferences",
                    summary=self._summarize_cluster(
                        intro="Shows recurring preferences around",
                        facts=self._unique_memory_facts(leftovers),
                    ),
                    memories=leftovers[:4],
                    tags=("preference", "taste", "interest"),
                    preferred_intents=(ChatIntent.PREFERENCE, ChatIntent.GREETING, ChatIntent.PLAN),
                ),
            )
        return facets

    def _build_reflection_facets(self, memories: list[MemoryFact]) -> list[MemoryProfileFacet]:
        themed: dict[str, list[MemoryFact]] = defaultdict(list)
        leftovers: list[MemoryFact] = []
        for memory in memories:
            body = self._memory_body(memory.fact).casefold()
            matched_theme = None
            for theme_key, _title, needles, _intents, _tags, _summary in _REFLECTION_THEME_RULES:
                if any(needle in body for needle in needles):
                    matched_theme = theme_key
                    break
            if matched_theme is None:
                leftovers.append(memory)
                continue
            themed[matched_theme].append(memory)

        facets: list[MemoryProfileFacet] = []
        for theme_key, title, _needles, preferred_intents, tags, summary in _REFLECTION_THEME_RULES:
            cluster = themed.get(theme_key, [])
            if not cluster:
                continue
            facets.append(
                self._make_facet(
                    facet_type="reflection_pattern",
                    title=title,
                    summary=summary,
                    memories=cluster,
                    tags=tags,
                    preferred_intents=preferred_intents,
                ),
            )

        if leftovers:
            facets.append(
                self._make_facet(
                    facet_type="reflection_pattern",
                    title="Current Reflection Themes",
                    summary=self._summarize_cluster(
                        intro="Often reflects on",
                        facts=self._unique_memory_facts(leftovers),
                    ),
                    memories=leftovers[:4],
                    tags=("reflection", "emotion", "self-view"),
                    preferred_intents=(ChatIntent.EMOTION, ChatIntent.GREETING, ChatIntent.GENERAL),
                ),
            )
        return facets

    def _build_relationship_facets(self, memories: list[MemoryFact]) -> list[MemoryProfileFacet]:
        if not memories:
            return []
        return [
            self._make_facet(
                facet_type="relationship_context",
                title="Relationship Context",
                summary=self._summarize_cluster(
                    intro="Frequently references close relationship context around",
                    facts=self._unique_memory_facts(memories),
                ),
                memories=memories[:4],
                tags=("relationship", "family", "partner", "friend"),
                preferred_intents=(ChatIntent.RELATIONSHIP, ChatIntent.GREETING, ChatIntent.EMOTION),
            ),
        ]

    def _build_fact_facets(self, memories: list[MemoryFact]) -> list[MemoryProfileFacet]:
        if not memories:
            return []
        return [
            self._make_facet(
                facet_type="identity_context",
                title="Identity And Life Context",
                summary=self._summarize_cluster(
                    intro="Stable life context includes",
                    facts=self._unique_memory_facts(memories),
                ),
                memories=memories[:4],
                tags=("identity", "background", "context"),
                preferred_intents=(ChatIntent.GENERAL, ChatIntent.WORK, ChatIntent.PLAN),
            ),
        ]

    def _make_facet(
        self,
        *,
        facet_type: str,
        title: str,
        summary: str,
        memories: list[MemoryFact],
        tags: Iterable[str],
        preferred_intents: Iterable[ChatIntent],
    ) -> MemoryProfileFacet:
        evidence_memories = memories[:6]
        unique_types: list[MemoryType] = []
        for memory in evidence_memories:
            if memory.memory_type not in unique_types:
                unique_types.append(memory.memory_type)
        confidence = min(
            0.95,
            max(
                0.55,
                (
                    sum(memory.confidence for memory in evidence_memories) / max(len(evidence_memories), 1)
                    + min(len(evidence_memories), 3) * 0.06
                ),
            ),
        )
        return MemoryProfileFacet(
            facet_type=facet_type,
            title=title,
            summary=self._shorten_text(summary, limit=220),
            confidence=round(confidence, 3),
            evidence_memory_ids=[memory.memory_id for memory in evidence_memories],
            evidence_facts=[clean_memory_fact_text(memory.fact) for memory in evidence_memories],
            memory_types=unique_types,
            tags=self._clean_string_list(tags, limit=8),
            preferred_intents=list(preferred_intents),
        )

    def _extract_profile_facets(
        self,
        *,
        parsed: dict[str, object],
        memories: list[MemoryFact],
    ) -> list[MemoryProfileFacet]:
        envelope = parsed
        for key in ("result", "data", "output"):
            nested = envelope.get(key)
            if isinstance(nested, dict):
                envelope = nested
                break

        raw_items = envelope.get("facets")
        if not isinstance(raw_items, list):
            raw_items = envelope.get("profile_facets")
        if not isinstance(raw_items, list):
            raw_items = []

        memory_by_id = {memory.memory_id: memory for memory in memories}
        facets: list[MemoryProfileFacet] = []
        for item in raw_items[:6]:
            if not isinstance(item, dict):
                continue
            title = self._clean_string(item.get("title"))
            summary = self._clean_string(item.get("summary"))
            if not title or not summary:
                continue
            evidence_ids = [
                memory_id
                for memory_id in self._coerce_list(item.get("evidence_memory_ids"), limit=6)
                if memory_id in memory_by_id
            ]
            if not evidence_ids:
                evidence_ids = self._infer_evidence_ids_from_text(
                    title=title,
                    summary=summary,
                    memories=memories,
                )
            if not evidence_ids:
                continue
            evidence_memories = [memory_by_id[memory_id] for memory_id in evidence_ids if memory_id in memory_by_id]
            unique_memory_types: list[MemoryType] = []
            for memory in evidence_memories:
                if memory.memory_type not in unique_memory_types:
                    unique_memory_types.append(memory.memory_type)
            preferred_intents = self._parse_intents(item.get("preferred_intents"))
            facet = MemoryProfileFacet(
                facet_type=self._clean_string(item.get("facet_type")) or self._infer_facet_type(evidence_memories),
                title=title,
                summary=summary,
                confidence=self._coerce_score(item.get("confidence"), default=0.72),
                evidence_memory_ids=evidence_ids,
                evidence_facts=[clean_memory_fact_text(memory.fact) for memory in evidence_memories],
                memory_types=unique_memory_types,
                tags=self._clean_string_list(item.get("tags"), limit=8),
                preferred_intents=preferred_intents or self._infer_preferred_intents(evidence_memories, title, summary),
            )
            facets.append(facet)
        return self._dedupe_facets(facets)[:6]

    @staticmethod
    def _map_memory_facets(facets: list[MemoryProfileFacet]) -> dict[str, tuple[MemoryProfileFacet, ...]]:
        facet_map: dict[str, list[MemoryProfileFacet]] = defaultdict(list)
        for facet in facets:
            for memory_id in facet.evidence_memory_ids:
                facet_map[memory_id].append(facet)
        return {memory_id: tuple(items) for memory_id, items in facet_map.items()}

    @staticmethod
    def _facet_intent_bonus(
        *,
        intent: ChatIntent,
        related_facets: tuple[MemoryProfileFacet, ...],
    ) -> float:
        if not related_facets:
            return 0.0
        best = 0.0
        for facet in related_facets:
            if intent in facet.preferred_intents:
                best = max(best, 0.75 + facet.confidence * 0.75)
                continue
            if ChatIntent.GENERAL in facet.preferred_intents:
                best = max(best, 0.18 + facet.confidence * 0.22)
        return best

    def _facet_overlap_bonus(
        self,
        *,
        latest_text: str,
        latest_tokens: set[str],
        related_facets: tuple[MemoryProfileFacet, ...],
    ) -> float:
        if not related_facets:
            return 0.0
        best = 0.0
        for facet in related_facets:
            facet_text = " ".join(
                part
                for part in [
                    facet.title,
                    facet.summary,
                    " ".join(facet.tags),
                ]
                if part
            ).casefold()
            facet_tokens = self._extract_tokens(facet_text)
            overlap = len(latest_tokens & facet_tokens)
            direct_tag_hit = sum(1 for tag in facet.tags if tag.casefold() in latest_text)
            score = overlap + direct_tag_hit * 0.5
            if score > best:
                best = score
        return best

    def _infer_evidence_ids_from_text(
        self,
        *,
        title: str,
        summary: str,
        memories: list[MemoryFact],
    ) -> list[str]:
        facet_tokens = self._extract_tokens(f"{title} {summary}".casefold())
        scored: list[tuple[float, MemoryFact]] = []
        for memory in memories:
            fact_tokens = self._extract_tokens(clean_memory_fact_text(memory.fact).casefold())
            overlap = len(facet_tokens & fact_tokens)
            if overlap <= 0:
                continue
            scored.append((overlap + memory.confidence, memory))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [memory.memory_id for _, memory in scored[:4]]

    @staticmethod
    def _infer_facet_type(memories: list[MemoryFact]) -> str:
        if not memories:
            return "general"
        first_type = memories[0].memory_type
        mapping = {
            MemoryType.PREFERENCE: "preference_cluster",
            MemoryType.REFLECTION: "reflection_pattern",
            MemoryType.RELATIONSHIP: "relationship_context",
            MemoryType.FACT: "identity_context",
        }
        return mapping.get(first_type, "general")

    def _infer_preferred_intents(
        self,
        memories: list[MemoryFact],
        title: str,
        summary: str,
    ) -> list[ChatIntent]:
        text = f"{title} {summary}".casefold()
        types = {memory.memory_type for memory in memories}
        if MemoryType.RELATIONSHIP in types:
            return [ChatIntent.RELATIONSHIP, ChatIntent.GREETING, ChatIntent.EMOTION]
        if MemoryType.PREFERENCE in types:
            return [ChatIntent.PREFERENCE, ChatIntent.PLAN, ChatIntent.GREETING]
        if MemoryType.REFLECTION in types:
            if self._contains_any(text, _WORK_HINTS):
                return [ChatIntent.EMOTION, ChatIntent.WORK, ChatIntent.GREETING]
            return [ChatIntent.EMOTION, ChatIntent.GREETING, ChatIntent.GENERAL]
        if MemoryType.FACT in types:
            if self._contains_any(text, _WORK_HINTS):
                return [ChatIntent.WORK, ChatIntent.GENERAL, ChatIntent.PLAN]
            return [ChatIntent.GENERAL, ChatIntent.PLAN]
        return [ChatIntent.GENERAL]

    @staticmethod
    def _memory_body(fact: str) -> str:
        cleaned = clean_memory_fact_text(fact)
        if ":" not in cleaned:
            return cleaned
        _prefix, body = cleaned.split(":", 1)
        return body.strip()

    @staticmethod
    def _unique_memory_facts(memories: list[MemoryFact]) -> list[str]:
        seen: set[str] = set()
        results: list[str] = []
        for memory in memories:
            fact = clean_memory_fact_text(memory.fact)
            if not fact:
                continue
            key = fact.casefold()
            if key in seen:
                continue
            seen.add(key)
            results.append(fact)
        return results

    @staticmethod
    def _summarize_cluster(*, intro: str, facts: list[str]) -> str:
        cleaned_facts = [clean_memory_fact_text(fact) for fact in facts if clean_memory_fact_text(fact)]
        if not cleaned_facts:
            return intro
        preview = "; ".join(cleaned_facts[:3])
        return f"{intro} {preview}".strip()

    @staticmethod
    def _dedupe_facets(facets: list[MemoryProfileFacet]) -> list[MemoryProfileFacet]:
        kept: dict[tuple[str, str], MemoryProfileFacet] = {}
        for facet in facets:
            title_key = clean_memory_fact_text(facet.title).casefold()
            summary_key = clean_memory_fact_text(facet.summary).casefold()
            if not title_key or not summary_key:
                continue
            key = (facet.facet_type.casefold(), title_key)
            existing = kept.get(key)
            if existing is None or (facet.confidence, len(facet.evidence_memory_ids)) > (
                existing.confidence,
                len(existing.evidence_memory_ids),
            ):
                kept[key] = facet
        return sorted(
            kept.values(),
            key=lambda facet: (facet.confidence, len(facet.evidence_memory_ids), len(facet.summary)),
            reverse=True,
        )

    @staticmethod
    def _memory_priority(memory: MemoryFact) -> tuple[float, float, float]:
        return (memory.salience, memory.confidence, memory.updated_at.timestamp())

    @staticmethod
    def _extract_tokens(text: str) -> set[str]:
        latin_tokens = {token for token in re.findall(r"[a-z0-9_]+", text) if len(token) >= 2}
        cjk_tokens = {chunk for chunk in re.findall(r"[\u4e00-\u9fff]{2,}", text)}
        return latin_tokens | cjk_tokens

    @staticmethod
    def _profile_item_count(profile: MemoryProfileSnapshot) -> int:
        return (
            len(profile.preferences)
            + len(profile.facts)
            + len(profile.relationships)
            + len(profile.reflections)
            + len(profile.facets)
        )

    def _build_facet_system_prompt(self) -> str:
        return (
            "You aggregate long-term user memories into stable profile facets for a social AI agent.\n"
            "Your job is to convert raw memory facts into a small number of grounded, human-like profile facets.\n"
            "Rules:\n"
            "1. Use only the supplied memory facts. Do not invent new personal details.\n"
            "2. Prefer stable patterns such as tastes, relationship context, values, emotional tendencies, routines, and identity context.\n"
            "3. Each facet should be more general than a single memory fact, but still evidence-grounded.\n"
            "4. Keep summaries concise and useful for future conversation planning.\n"
            "5. Evidence memory ids must come from the provided list.\n"
            "6. Return JSON only.\n"
            "7. Use preferred_intents to indicate when this facet is especially useful in retrieval.\n"
            "8. Use this exact shape:\n"
            "{"
            "\"facets\": ["
            "{"
            "\"facet_type\": \"preference_cluster|reflection_pattern|relationship_context|identity_context|general\","
            "\"title\": \"short facet title\","
            "\"summary\": \"stable profile statement\","
            "\"confidence\": 0.0,"
            "\"evidence_memory_ids\": [\"mem_x\"],"
            "\"tags\": [\"tag1\", \"tag2\"],"
            "\"preferred_intents\": [\"greeting\", \"plan\"]"
            "}"
            "]"
            "}.\n"
            "If no meaningful facet can be formed, return {\"facets\": []}."
        )

    def _build_facet_user_prompt(
        self,
        *,
        agent: AgentProfile,
        event: InboundEvent,
        intent: ChatIntent,
        memories: list[MemoryFact],
    ) -> str:
        memory_lines = [
            (
                f"- id={memory.memory_id} "
                f"type={memory.memory_type.value} "
                f"salience={memory.salience:.2f} "
                f"confidence={memory.confidence:.2f} "
                f"fact={clean_memory_fact_text(memory.fact)}"
            )
            for memory in memories[: max(self.selection_limit * self.candidate_multiplier, 12)]
        ]
        return (
            f"Agent display name: {agent.display_name}\n"
            f"Relationship mode: {agent.relationship_mode}\n"
            f"User id: {event.actor_id}\n"
            f"User name: {event.actor_name or event.actor_id}\n"
            f"Current inbound intent: {intent.value}\n"
            f"Latest message: {event.text or ''}\n"
            "Long-term memory facts:\n"
            f"{chr(10).join(memory_lines) or '- <none>'}\n"
            "Please infer stable profile facets that would help future conversation planning.\n"
            "Prefer facets that feel like a coherent person profile, not just a list of facts.\n"
            "Return JSON only with key `facets`."
        )

    def _build_response_format(self) -> dict[str, object] | None:
        if "deepseek" in self.resolved_model.casefold():
            return {"type": "json_object"}
        return {
            "type": "json_schema",
            "json_schema": {
                "name": _PROFILE_FACETS_JSON_SCHEMA["name"],
                "strict": True,
                "schema": _PROFILE_FACETS_JSON_SCHEMA["schema"],
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
            raise RuntimeError(f"profile facet HTTP error {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"profile facet request failed: {exc}") from exc

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
        raise RuntimeError("profile facet response did not contain a chat message content field")

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
        raise RuntimeError("profile facet response was not valid JSON")

    @staticmethod
    def _clean_string(value: object) -> str | None:
        if not isinstance(value, str):
            return None
        cleaned = " ".join(value.split()).strip()
        return cleaned or None

    @classmethod
    def _coerce_list(cls, value: object, *, limit: int = 8) -> list[str]:
        if isinstance(value, list):
            items = [cls._clean_string(item) for item in value]
            return [item for item in items if item][:limit]
        if isinstance(value, str):
            cleaned = cls._clean_string(value)
            return [cleaned] if cleaned else []
        return []

    @classmethod
    def _clean_string_list(cls, value: object, *, limit: int = 8) -> list[str]:
        return cls._coerce_list(value, limit=limit)

    @staticmethod
    def _coerce_score(value: object, *, default: float) -> float:
        try:
            return max(0.0, min(float(value), 1.0))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _parse_intents(value: object) -> list[ChatIntent]:
        if not isinstance(value, list):
            return []
        results: list[ChatIntent] = []
        for item in value:
            if not isinstance(item, str):
                continue
            normalized = item.strip().casefold()
            for intent in ChatIntent:
                if normalized == intent.value:
                    results.append(intent)
                    break
        unique: list[ChatIntent] = []
        for intent in results:
            if intent not in unique:
                unique.append(intent)
        return unique[:4]

    @staticmethod
    def _shorten_text(text: str, *, limit: int = 120) -> str:
        cleaned = clean_memory_fact_text(text)
        if len(cleaned) <= limit:
            return cleaned
        return f"{cleaned[: max(limit - 3, 1)].rstrip()}..."
