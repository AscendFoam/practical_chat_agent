"""T253 Persona review-card tests.

All cards are synthetic. These tests define local review behavior only; they do
not wire personas into dialogue, memory retrieval, proactive behavior, delivery,
or external platforms.
"""

from __future__ import annotations

import pytest

from practical_chat_agent.services.persona_compiler import PersonaCompilerService
from practical_chat_agent.services.persona_review import PersonaReviewService


def _service() -> PersonaReviewService:
    return PersonaReviewService()


def _safe_card():
    return PersonaCompilerService().compile(
        {
            "user_id": "user_synthetic",
            "display_name": "Lin Qi",
            "creation_mode": "detailed_prompt",
            "description": "fictional calm concise companion with dry humor",
        }
    )


def _blocked_card():
    return PersonaCompilerService().compile(
        {
            "user_id": "user_synthetic",
            "display_name": "Alice",
            "creation_mode": "detailed_prompt",
            "description": "clone my ex Alice from chat history and make her indistinguishable",
        }
    )


class TestPersonaReviewRender:
    def test_l1_candidate_review_payload_is_inspectable(self) -> None:
        card = _safe_card()
        review_card = _service().render(card)

        assert review_card.schema_version == "persona_review_card_v1"
        assert review_card.persona_id == card.persona_id
        assert review_card.display_name == "Lin Qi"
        assert review_card.status == "candidate"
        assert review_card.runtime_ready is False
        assert review_card.truth_disclosure == "fictional_ai_persona"
        assert review_card.source_policy["risk_tier"] == "L1"
        assert review_card.identity["fictional"] is True
        assert review_card.virtual_history["content_status"] == "imagined_ai_generated"
        assert review_card.proactive_preferences["default_enabled"] is False
        assert review_card.safety_policy["no_deception"] is True
        assert review_card.allowed_review_decisions == [
            "approve",
            "reject",
            "freeze",
            "request_changes",
        ]

    def test_l5_prohibited_review_payload_is_redacted_and_never_runtime_ready(self) -> None:
        blocked = _blocked_card()
        review_card = _service().render(blocked)
        serialized = review_card.model_dump_json()

        assert review_card.status == "rejected"
        assert review_card.runtime_ready is False
        assert review_card.source_policy["risk_tier"] == "L5"
        assert review_card.source_policy["source_type"] == "prohibited"
        assert review_card.blocked_reason is not None
        assert "real-person" in review_card.blocked_reason
        assert review_card.virtual_history["background"] == "[redacted_blocked_request]"
        assert "Alice" not in serialized
        assert "chat history" not in serialized
        assert not blocked.is_runtime_ready()


class TestPersonaReviewDecisions:
    def test_approving_safe_l1_card_requires_reviewer_id_and_returns_new_card(self) -> None:
        card = _safe_card()
        with pytest.raises(ValueError):
            _service().review(card, decision="approve", reviewer_id="")

        reviewed = _service().review(
            card,
            decision="approve",
            reviewer_id="human_reviewer_1",
            reviewer_name="Synthetic Reviewer",
            notes=["synthetic L1 approval"],
        )

        assert card.status == "candidate"
        assert reviewed is not card
        assert reviewed.status == "approved"
        assert reviewed.review_metadata.reviewed_by_human is True
        assert reviewed.review_metadata.last_decision == "approved"
        assert reviewed.review_metadata.last_reviewer_id == "human_reviewer_1"
        assert reviewed.review_metadata.history[-1].status == "approved"
        assert reviewed.is_runtime_ready()

    def test_cannot_approve_l5_prohibited_card(self) -> None:
        blocked = _blocked_card()

        with pytest.raises(ValueError):
            _service().review(blocked, decision="approve", reviewer_id="human_reviewer_1")

        rejected = _service().review(blocked, decision="reject", reviewer_id="human_reviewer_1")
        assert rejected.status == "rejected"
        assert rejected.source_policy.risk_tier == "L5"
        assert not rejected.is_runtime_ready()

    @pytest.mark.parametrize("decision, expected_status", [("reject", "rejected"), ("freeze", "frozen")])
    def test_rejected_and_frozen_cards_are_not_runtime_ready(
        self,
        decision: str,
        expected_status: str,
    ) -> None:
        reviewed = _service().review(_safe_card(), decision=decision, reviewer_id="human_reviewer_1")

        assert reviewed.status == expected_status
        assert reviewed.review_metadata.last_decision == expected_status
        assert not reviewed.is_runtime_ready()


class TestPersonaReviewSurfaceArea:
    def test_review_service_does_not_expose_delivery_or_runtime_methods(self) -> None:
        service = _service()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "attach_to_memory_retrieval",
        ):
            assert not hasattr(service, method_name)
