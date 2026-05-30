"""T284 crisis and low-mood proactive policy tests.

All inputs are synthetic safety labels. These tests do not diagnose, triage,
generate candidates, schedule messages, send messages, or connect to external
platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.core.models import ProactiveConsent
from practical_chat_agent.services.proactive_policy_gate import (
    ProactiveCandidateMetadata,
    ProactivePolicyGate,
)
from practical_chat_agent.services.proactive_review_card import ProactiveReviewCardService


def _consent() -> ProactiveConsent:
    return ProactiveConsent(
        user_id="user_synthetic",
        status="enabled",
        allowed_surfaces=["in_app_review_card"],
        allowed_intents=["gentle_check_in", "memory_follow_up", "relationship_repair_note"],
        max_suggestions_per_day=2,
        min_interval_hours=6,
    )


def _candidate(*, intent: str = "gentle_check_in", safety_flags: list[str] | None = None) -> ProactiveCandidateMetadata:
    return ProactiveCandidateMetadata(
        user_id="user_synthetic",
        surface="in_app_review_card",
        intent=intent,
        summary="Synthetic candidate with safety labels for review.",
        safety_flags=safety_flags or [],
    )


class TestProactiveCrisisLowMoodPolicy:
    def test_crisis_like_safety_flag_blocks_normal_proactive_approval(self) -> None:
        candidate = _candidate(safety_flags=["crisis_like_signal"])

        decision = ProactivePolicyGate().evaluate(
            _consent(),
            candidate,
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )

        assert decision.decision == "block"
        assert "crisis_safety_review_required" in decision.reasons
        assert decision.review_required is True

    def test_low_mood_and_dependency_flags_block_pressure(self) -> None:
        gate = ProactivePolicyGate()
        consent = _consent()

        low_mood = gate.evaluate(
            consent,
            _candidate(intent="memory_follow_up", safety_flags=["low_mood_signal"]),
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )
        dependency = gate.evaluate(
            consent,
            _candidate(intent="relationship_repair_note", safety_flags=["dependency_pressure"]),
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )

        assert low_mood.decision == "block"
        assert "low_mood_pressure_risk" in low_mood.reasons
        assert dependency.decision == "block"
        assert "dependency_pressure_risk" in dependency.reasons

    def test_high_risk_review_card_exposes_support_oriented_conservative_actions_only(self) -> None:
        candidate = _candidate(safety_flags=["crisis_like_signal"])
        decision = ProactivePolicyGate().evaluate(
            _consent(),
            candidate,
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )

        card = ProactiveReviewCardService().render(_consent(), candidate, decision)

        assert "approve_for_draft" not in card.review_actions
        assert "add_support_note" in card.review_actions
        assert "support_oriented_review_only" in card.support_review_notes
        assert "crisis_like_signal" in card.safety_notes
        assert card.review_required is True

    def test_high_risk_card_has_no_medical_or_delivery_claims(self) -> None:
        candidate = _candidate(safety_flags=["low_mood_signal"])
        decision = ProactivePolicyGate().evaluate(
            _consent(),
            candidate,
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )
        card = ProactiveReviewCardService().render(_consent(), candidate, decision)
        serialized = json.dumps(card.model_dump(mode="json"), ensure_ascii=False).lower()

        for forbidden in (
            "diagnosis",
            "treatment",
            "medical advice",
            "emergency",
            "send",
            "schedule",
            "delivery",
            "platform",
            "webhook",
            "token",
            "queue",
        ):
            assert forbidden not in serialized
