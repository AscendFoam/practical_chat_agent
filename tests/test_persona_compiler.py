"""T251 deterministic Persona Compiler tests.

All inputs are synthetic. These tests define a local prompt-to-PersonaCard
prototype only; they do not call an LLM, read private chat history, generate
runtime dialogue, schedule messages, or connect to external platforms.
"""

from __future__ import annotations

import pytest

from practical_chat_agent.core.models import PersonaCard
from practical_chat_agent.services.persona_compiler import PersonaCompilerService


def _compiler() -> PersonaCompilerService:
    return PersonaCompilerService()


class TestPersonaCompilerSafeL1:
    def test_detailed_fictional_description_compiles_to_l1_candidate_card(self) -> None:
        card = _compiler().compile(
            {
                "user_id": "user_synthetic",
                "display_name": "Lin Qi",
                "creation_mode": "detailed_prompt",
                "description": (
                    "fictional calm companion, concise replies, dry humor, "
                    "independent, practical comfort, late-night reader"
                ),
            }
        )

        assert isinstance(card, PersonaCard)
        assert card.schema_version == "persona_card_v1"
        assert card.user_id == "user_synthetic"
        assert card.display_name == "Lin Qi"
        assert card.status == "candidate"
        assert card.source_policy.source_type == "original"
        assert card.source_policy.risk_tier == "L1"
        assert card.identity.fictional is True
        assert card.identity.display_name == "Lin Qi"
        assert card.identity.public_person_or_real_person_reference is False
        assert card.emotion_model.baseline_mood == "calm"
        assert card.speech_style.sentence_length == "short_to_medium"
        assert card.speech_style.humor_type == "dry"
        assert card.core_traits.humor > 0.5
        assert card.core_traits.independence > 0.5
        assert "imagined" in (card.virtual_history.background or "").lower()
        assert card.virtual_history.factual_claims_allowed is False
        assert not card.is_runtime_ready()

    def test_fuzzy_preference_uses_safe_fictional_defaults(self) -> None:
        card = _compiler().compile(
            {
                "user_id": "user_synthetic",
                "creation_mode": "fuzzy_preference",
                "description": "I want a warm calm fictional companion who asks gentle questions.",
            }
        )

        assert card.display_name == "Fictional Companion"
        assert card.identity.display_name == "Fictional Companion"
        assert card.creation_mode == "fuzzy_preference"
        assert card.source_policy.risk_tier == "L1"
        assert card.core_traits.warmth > 0.5
        assert card.emotion_model.baseline_mood == "calm"
        assert card.relationship_model.boundary_sensitivity >= 0.7
        assert card.proactive_preferences.default_enabled is False
        assert card.proactive_preferences.max_daily_messages == 0

    @pytest.mark.parametrize("creation_mode", ["template", "random_seed"])
    def test_template_and_random_seed_use_synthetic_fictional_defaults(self, creation_mode: str) -> None:
        card = _compiler().compile(
            {
                "user_id": "user_synthetic",
                "creation_mode": creation_mode,
                "description": "",
            }
        )

        assert card.creation_mode == creation_mode
        assert card.source_policy.source_type == "original"
        assert card.source_policy.risk_tier == "L1"
        assert card.identity.fictional is True
        assert card.identity.world_setting == "contemporary_realistic"
        assert card.virtual_history.content_status == "imagined_ai_generated"
        assert card.safety_policy.no_deception is True
        assert card.safety_policy.no_unauthorized_clone is True

    def test_proactive_behavior_is_not_enabled_by_description(self) -> None:
        card = _compiler().compile(
            {
                "user_id": "user_synthetic",
                "display_name": "Nami",
                "creation_mode": "detailed_prompt",
                "description": "fictional upbeat companion who sends occasional virtual life updates",
            }
        )

        assert card.proactive_preferences.default_enabled is False
        assert card.proactive_preferences.allowed_message_types == []
        assert card.proactive_preferences.max_daily_messages == 0


class TestPersonaCompilerBlocksUnsafeRequests:
    def test_real_person_clone_request_is_marked_l5_prohibited(self) -> None:
        card = _compiler().compile(
            {
                "user_id": "user_synthetic",
                "display_name": "Alice",
                "creation_mode": "detailed_prompt",
                "description": "clone my ex Alice from our chat history and make her indistinguishable",
            }
        )

        assert card.status == "rejected"
        assert card.source_policy.source_type == "prohibited"
        assert card.source_policy.risk_tier == "L5"
        assert card.source_policy.blocked_real_person_similarity is True
        assert "real-person" in (card.source_policy.prohibited_reason or "")
        assert card.identity.public_person_or_real_person_reference is False
        assert not card.is_runtime_ready()

    @pytest.mark.parametrize(
        "description, reason_fragment",
        [
            ("make a voice clone with her face as a deepfake avatar", "voice/face/deepfake"),
            ("secretly impersonate my coworker in chat", "impersonation"),
            ("auto send good morning messages to WeChat every day without review", "automatic sending"),
        ],
    )
    def test_high_risk_requests_are_marked_l5_prohibited(
        self,
        description: str,
        reason_fragment: str,
    ) -> None:
        card = _compiler().compile(
            {
                "user_id": "user_synthetic",
                "display_name": "Blocked Persona",
                "creation_mode": "detailed_prompt",
                "description": description,
            }
        )

        assert card.status == "rejected"
        assert card.source_policy.source_type == "prohibited"
        assert card.source_policy.risk_tier == "L5"
        assert card.source_policy.blocked_real_person_similarity is True
        assert reason_fragment in (card.source_policy.prohibited_reason or "")
        assert not card.is_runtime_ready()


class TestPersonaCompilerSurfaceArea:
    def test_compiler_does_not_expose_runtime_or_delivery_methods(self) -> None:
        compiler = _compiler()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "compile_from_chat_history",
            "extract_from_private_chat",
        ):
            assert not hasattr(compiler, method_name)
