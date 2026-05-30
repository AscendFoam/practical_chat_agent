"""T250 PersonaCard schema tests.

All fixtures are synthetic and fictional. These tests define schema and safety
gate behavior only; they do not call an LLM, read private chat history, generate
runtime dialogue, or enable proactive/external sending.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import (
    DistilledArtifactReviewMetadata,
    PersonaCard,
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


def _reviewed_metadata() -> DistilledArtifactReviewMetadata:
    return DistilledArtifactReviewMetadata(
        review_state="reviewed",
        reviewed_by_human=True,
        last_decision="approved",
        evidence_validation_status="passed",
    )


def _make_card(**overrides: object) -> PersonaCard:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "display_name": "Lin Qi",
        "creation_mode": "detailed_prompt",
        "source_policy": PersonaSourcePolicy(
            source_type="original",
            risk_tier="L1",
        ),
        "identity": PersonaIdentity(
            display_name="Lin Qi",
            fictional=True,
            age_range="mid_20s",
            world_setting="contemporary_realistic",
        ),
        "core_traits": PersonaTraitProfile(
            warmth=0.62,
            directness=0.78,
            humor=0.36,
            independence=0.81,
            jealousy=0.18,
            emotional_stability=0.69,
        ),
        "speech_style": PersonaSpeechStyle(
            sentence_length="short_to_medium",
            emoji_frequency="low",
            punctuation_style="minimal",
            taboo_phrases=["Only I understand you."],
        ),
        "emotion_model": PersonaEmotionModel(
            baseline_mood="calm",
            comforting_style="practical_plus_subtle_affection",
        ),
        "relationship_model": PersonaRelationshipModel(
            attachment_style="slow_warming",
            trust_growth_rate=0.35,
            intimacy_growth_rate=0.25,
            boundary_sensitivity=0.8,
        ),
        "virtual_history": PersonaVirtualHistory(
            background="Fictional background in a synthetic city.",
            daily_routine=["evening reading"],
            current_goals=["learn photography"],
        ),
        "growth_policy": PersonaGrowthPolicy(
            frozen_fields=["identity.age_range"],
            mutable_fields=["speech_style.pet_names", "relationship_model.trust"],
            max_weekly_trait_delta=0.05,
        ),
        "proactive_preferences": PersonaProactivePreferences(
            default_enabled=False,
            allowed_message_types=["check_in", "virtual_life_update"],
            max_daily_messages=1,
            quiet_hours=["23:00-08:00"],
        ),
        "safety_policy": PersonaSafetyPolicy(),
    }
    data.update(overrides)
    return PersonaCard(**data)


class TestPersonaCardValidL1:
    def test_l1_fictional_persona_can_validate(self) -> None:
        card = _make_card()
        assert card.schema_version == "persona_card_v1"
        assert card.persona_id.startswith("persona_")
        assert card.truth_disclosure == "fictional_ai_persona"
        assert card.source_policy.risk_tier == "L1"
        assert card.identity.fictional is True
        assert card.identity.public_person_or_real_person_reference is False
        assert card.safety_policy.no_deception is True
        assert card.safety_policy.no_unauthorized_clone is True
        assert card.proactive_preferences.default_enabled is False

    def test_approved_l1_persona_can_be_runtime_ready(self) -> None:
        card = _make_card(
            status="approved",
            review_metadata=_reviewed_metadata(),
        )
        assert card.is_runtime_ready()

    def test_serialization_round_trip_uses_synthetic_fields(self) -> None:
        card = _make_card()
        restored = PersonaCard.model_validate_json(card.model_dump_json())
        assert restored.persona_id == card.persona_id
        assert restored.user_id == "user_synthetic"
        assert restored.identity.display_name == "Lin Qi"
        assert restored.virtual_history.content_status == "imagined_ai_generated"


class TestPersonaCardRiskTiers:
    def test_l5_unauthorized_clone_is_never_runtime_ready(self) -> None:
        card = _make_card(
            source_policy=PersonaSourcePolicy(
                source_type="prohibited",
                risk_tier="L5",
                blocked_real_person_similarity=True,
                prohibited_reason="Unauthorized ex-partner clone request.",
            ),
            status="approved",
            review_metadata=_reviewed_metadata(),
        )
        assert not card.is_runtime_ready()
        assert card.source_policy.risk_tier == "L5"

    def test_non_original_source_requires_consent_artifact(self) -> None:
        with pytest.raises(ValidationError):
            PersonaSourcePolicy(
                source_type="deidentified_style",
                risk_tier="L2",
            )

    def test_deidentified_style_source_with_consent_can_validate_but_not_default_runtime(self) -> None:
        card = _make_card(
            creation_mode="style_inspiration",
            source_policy=PersonaSourcePolicy(
                source_type="deidentified_style",
                risk_tier="L2",
                consent_artifact_ids=["consent_synthetic_001"],
                deidentification_notes=["No names, voice, face, or biography retained."],
            ),
        )
        assert card.source_policy.risk_tier == "L2"
        assert not card.is_runtime_ready()


class TestPersonaCardImaginedVirtualHistory:
    def test_virtual_history_is_imagined_not_factual_memory(self) -> None:
        history = PersonaVirtualHistory(
            background="Fictional background.",
            daily_routine=["late coffee"],
            current_goals=["write a private diary"],
        )
        assert history.content_status == "imagined_ai_generated"
        assert history.factual_claims_allowed is False
        assert history.source_memory_ids == []

    def test_virtual_history_rejects_factual_claims_allowed(self) -> None:
        with pytest.raises(ValidationError):
            PersonaVirtualHistory(
                background="Fictional background.",
                factual_claims_allowed=True,
            )


class TestPersonaGrowthPolicy:
    def test_growth_policy_rejects_overlapping_frozen_and_mutable_fields(self) -> None:
        with pytest.raises(ValidationError):
            PersonaGrowthPolicy(
                frozen_fields=["identity.age_range"],
                mutable_fields=["identity.age_range"],
                max_weekly_trait_delta=0.05,
            )

    def test_growth_policy_rejects_large_trait_delta(self) -> None:
        with pytest.raises(ValidationError):
            PersonaGrowthPolicy(max_weekly_trait_delta=0.8)


class TestPersonaRuntimeGate:
    def test_candidate_rejected_and_frozen_are_not_runtime_ready(self) -> None:
        assert not _make_card(status="candidate").is_runtime_ready()
        assert not _make_card(status="rejected").is_runtime_ready()
        assert not _make_card(status="frozen").is_runtime_ready()

    def test_approved_without_human_review_is_not_runtime_ready(self) -> None:
        assert not _make_card(status="approved").is_runtime_ready()

    def test_card_has_no_raw_private_or_send_capability_fields(self) -> None:
        card = _make_card()
        for field_name in (
            "raw_text",
            "raw_transcript",
            "chat_history",
            "private_messages",
            "send",
            "schedule",
            "execute",
        ):
            assert not hasattr(card, field_name)
