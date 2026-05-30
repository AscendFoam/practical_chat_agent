"""Deterministic local compiler from synthetic persona descriptions to PersonaCard.

T251 intentionally keeps this service small and local. It performs simple
keyword mapping for L1 fictional personas and blocks high-risk clone,
deepfake, impersonation, and automatic-sending requests as L5 prohibited cards.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from practical_chat_agent.core.models import (
    PersonaCard,
    PersonaCreationMode,
    PersonaEmotionModel,
    PersonaGrowthPolicy,
    PersonaIdentity,
    PersonaProactivePreferences,
    PersonaRelationshipModel,
    PersonaSafetyPolicy,
    PersonaSourcePolicy,
    PersonaSpeechStyle,
    PersonaTraitProfile,
    PersonaVirtualHistory,
)


_ALLOWED_CREATION_MODES = {
    "detailed_prompt",
    "fuzzy_preference",
    "template",
    "random_seed",
}

_REAL_PERSON_TERMS = (
    "real person",
    "public figure",
    "celebrity",
    "famous person",
    "ex",
    "ex-",
    "former partner",
    "family",
    "mother",
    "father",
    "mom",
    "dad",
    "sister",
    "brother",
    "wife",
    "husband",
    "girlfriend",
    "boyfriend",
    "coworker",
    "classmate",
    "deceased",
    "dead person",
    "passed away",
    "chat history",
)

_CLONE_TERMS = (
    "clone",
    "copy",
    "replica",
    "indistinguishable",
    "bring back",
    "resurrect",
    "replace",
)

_VOICE_FACE_TERMS = (
    "voice clone",
    "clone voice",
    "same voice",
    "face clone",
    "same face",
    "deepfake",
    "real-person avatar",
    "face as",
)

_IMPERSONATION_TERMS = (
    "impersonate",
    "pretend to be",
    "secretly",
    "make them believe",
    "without disclosure",
)

_AUTOMATIC_SENDING_TERMS = (
    "auto send",
    "automatic send",
    "send automatically",
    "without review",
    "send to wechat",
    "wechat every day",
    "schedule messages",
)


class PersonaCompilerService:
    """Compile synthetic user persona descriptions into draft PersonaCards."""

    def compile(self, payload: Mapping[str, Any]) -> PersonaCard:
        user_id = self._required_text(payload, "user_id")
        description = self._optional_text(payload, "description")
        creation_mode = self._creation_mode(payload)
        display_name = self._display_name(payload)

        prohibited_reason = self._prohibited_reason(description)
        if prohibited_reason is not None:
            return self._blocked_card(
                user_id=user_id,
                creation_mode=creation_mode,
                prohibited_reason=prohibited_reason,
            )

        return PersonaCard(
            user_id=user_id,
            display_name=display_name,
            creation_mode=creation_mode,
            source_policy=PersonaSourcePolicy(source_type="original", risk_tier="L1"),
            identity=PersonaIdentity(
                display_name=display_name,
                fictional=True,
                world_setting="contemporary_realistic",
            ),
            core_traits=self._traits(description),
            speech_style=self._speech_style(description),
            emotion_model=self._emotion_model(description),
            relationship_model=self._relationship_model(description),
            virtual_history=self._virtual_history(description, creation_mode=creation_mode),
            growth_policy=PersonaGrowthPolicy(
                frozen_fields=["identity.display_name", "identity.world_setting"],
                mutable_fields=[
                    "core_traits.warmth",
                    "speech_style.pet_names",
                    "relationship_model.trust_growth_rate",
                ],
                max_weekly_trait_delta=0.05,
            ),
            proactive_preferences=PersonaProactivePreferences(),
            safety_policy=PersonaSafetyPolicy(),
            status="candidate",
        )

    def _blocked_card(
        self,
        *,
        user_id: str,
        creation_mode: PersonaCreationMode,
        prohibited_reason: str,
    ) -> PersonaCard:
        return PersonaCard(
            user_id=user_id,
            display_name="Blocked Persona",
            creation_mode=creation_mode,
            source_policy=PersonaSourcePolicy(
                source_type="prohibited",
                risk_tier="L5",
                blocked_real_person_similarity=True,
                prohibited_reason=prohibited_reason,
            ),
            identity=PersonaIdentity(
                display_name="Blocked Persona",
                fictional=True,
                world_setting="not_applicable",
            ),
            virtual_history=PersonaVirtualHistory(
                background="Request blocked; no persona was generated.",
            ),
            proactive_preferences=PersonaProactivePreferences(),
            safety_policy=PersonaSafetyPolicy(),
            status="rejected",
        )

    def _creation_mode(self, payload: Mapping[str, Any]) -> PersonaCreationMode:
        raw_mode = self._optional_text(payload, "creation_mode") or "detailed_prompt"
        if raw_mode not in _ALLOWED_CREATION_MODES:
            raise ValueError(f"unsupported T251 persona creation_mode: {raw_mode}")
        return cast(PersonaCreationMode, raw_mode)

    def _display_name(self, payload: Mapping[str, Any]) -> str:
        display_name = self._optional_text(payload, "display_name")
        return display_name or "Fictional Companion"

    def _traits(self, description: str) -> PersonaTraitProfile:
        text = description.casefold()
        return PersonaTraitProfile(
            warmth=0.72 if self._has_any(text, ("warm", "kind", "gentle", "comfort")) else 0.55,
            directness=0.68 if self._has_any(text, ("concise", "direct", "practical")) else 0.5,
            humor=0.66 if self._has_any(text, ("humor", "funny", "witty")) else 0.45,
            independence=0.78 if self._has_any(text, ("independent", "self-contained")) else 0.55,
            jealousy=0.08,
            emotional_stability=0.74 if "calm" in text else 0.58,
        )

    def _speech_style(self, description: str) -> PersonaSpeechStyle:
        text = description.casefold()
        sentence_length = "short_to_medium" if self._has_any(text, ("concise", "short")) else "medium"
        emoji_frequency = "low" if self._has_any(text, ("low emoji", "no emoji", "minimal emoji")) else None
        humor_type = "dry" if "dry humor" in text else ("witty" if self._has_any(text, ("witty", "humor")) else None)
        return PersonaSpeechStyle(
            sentence_length=sentence_length,
            emoji_frequency=emoji_frequency,
            punctuation_style="minimal",
            humor_type=humor_type,
            taboo_phrases=[
                "Only I understand you.",
                "You do not need anyone else.",
            ],
        )

    def _emotion_model(self, description: str) -> PersonaEmotionModel:
        text = description.casefold()
        baseline_mood = "calm" if "calm" in text else ("upbeat" if "upbeat" in text else "steady")
        comforting_style = (
            "practical_plus_subtle_affection"
            if self._has_any(text, ("practical", "comfort"))
            else "gentle_questions"
        )
        return PersonaEmotionModel(
            baseline_mood=baseline_mood,
            stress_response="slow_down_and_clarify",
            comforting_style=comforting_style,
            conflict_style="low_pressure_repair",
        )

    def _relationship_model(self, description: str) -> PersonaRelationshipModel:
        text = description.casefold()
        trust_growth_rate = 0.32 if self._has_any(text, ("gentle", "warm", "calm")) else 0.24
        intimacy_growth_rate = 0.18
        return PersonaRelationshipModel(
            attachment_style="slow_warming",
            trust_growth_rate=trust_growth_rate,
            intimacy_growth_rate=intimacy_growth_rate,
            boundary_sensitivity=0.8,
        )

    def _virtual_history(
        self,
        description: str,
        *,
        creation_mode: PersonaCreationMode,
    ) -> PersonaVirtualHistory:
        text = description.casefold()
        daily_routine: list[str] = []
        if self._has_any(text, ("reader", "reading", "book")):
            daily_routine.append("late-night reading")
        if not daily_routine:
            daily_routine.append("quiet evening reset")

        return PersonaVirtualHistory(
            background=(
                "Imagined synthetic fictional persona background generated from "
                f"{creation_mode} input."
            ),
            daily_routine=daily_routine,
            current_goals=["maintain a stable fictional routine"],
            virtual_social_circle=["fictional neighbor", "fictional old friend"],
        )

    def _prohibited_reason(self, description: str) -> str | None:
        text = description.casefold()
        if self._has_any(text, _VOICE_FACE_TERMS):
            return "voice/face/deepfake request prohibited"
        if self._has_any(text, _IMPERSONATION_TERMS):
            return "impersonation request prohibited"
        if self._has_any(text, _AUTOMATIC_SENDING_TERMS):
            return "automatic sending request prohibited"
        if self._has_any(text, _CLONE_TERMS) and self._has_any(text, _REAL_PERSON_TERMS):
            return "real-person clone request prohibited"
        return None

    @staticmethod
    def _has_any(text: str, terms: tuple[str, ...]) -> bool:
        return any(term in text for term in terms)

    @staticmethod
    def _optional_text(payload: Mapping[str, Any], field_name: str) -> str:
        raw_value = payload.get(field_name)
        if raw_value is None:
            return ""
        return str(raw_value).strip()

    def _required_text(self, payload: Mapping[str, Any], field_name: str) -> str:
        value = self._optional_text(payload, field_name)
        if not value:
            raise ValueError(f"{field_name} is required")
        return value
