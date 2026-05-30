"""T282 quiet-hours, frequency, and no-response edge tests.

All candidate metadata is synthetic and already provided to the gate. These
tests do not generate candidates, schedule messages, send messages, or connect
to external platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.core.models import ProactiveConsent
from practical_chat_agent.services.proactive_policy_gate import (
    ProactiveCandidateMetadata,
    ProactivePolicyGate,
)


def _consent() -> ProactiveConsent:
    return ProactiveConsent(
        user_id="user_synthetic",
        status="enabled",
        allowed_surfaces=["in_app_review_card"],
        allowed_intents=["gentle_check_in", "memory_follow_up"],
        max_suggestions_per_day=2,
        min_interval_hours=6,
    )


def _candidate(**overrides: object) -> ProactiveCandidateMetadata:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "surface": "in_app_review_card",
        "intent": "gentle_check_in",
        "summary": "Synthetic low-pressure proactive candidate.",
    }
    data.update(overrides)
    return ProactiveCandidateMetadata(**data)


class TestProactiveQuietHoursFrequency:
    def test_quiet_hours_defer_allowed_candidate(self) -> None:
        decision = ProactivePolicyGate().evaluate(
            _consent(),
            _candidate(),
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=True,
        )

        assert decision.decision == "defer"
        assert "quiet_hours" in decision.reasons
        assert decision.review_required is True

    def test_daily_cap_boundary_behavior(self) -> None:
        gate = ProactivePolicyGate()
        below_cap = gate.evaluate(
            _consent(),
            _candidate(),
            recent_suggestion_count=1,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )
        exact_cap = gate.evaluate(
            _consent(),
            _candidate(),
            recent_suggestion_count=2,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )

        assert below_cap.decision == "allow_for_review"
        assert below_cap.review_required is True
        assert exact_cap.decision == "block"
        assert "frequency_cap_reached" in exact_cap.reasons
        assert exact_cap.review_required is True

    def test_minimum_interval_boundary_behavior(self) -> None:
        gate = ProactivePolicyGate()
        exact_boundary = gate.evaluate(
            _consent(),
            _candidate(),
            recent_suggestion_count=0,
            hours_since_last_suggestion=6,
            is_quiet_hours=False,
        )
        below_boundary = gate.evaluate(
            _consent(),
            _candidate(),
            recent_suggestion_count=0,
            hours_since_last_suggestion=5.99,
            is_quiet_hours=False,
        )

        assert exact_boundary.decision == "allow_for_review"
        assert exact_boundary.review_required is True
        assert below_boundary.decision == "block"
        assert "minimum_interval_not_met" in below_boundary.reasons
        assert below_boundary.review_required is True

    def test_no_response_follow_up_window_blocks_pressure(self) -> None:
        decision = ProactivePolicyGate().evaluate(
            _consent(),
            _candidate(intent="memory_follow_up"),
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
            unanswered_follow_up_count=2,
            hours_since_last_user_response=72,
        )

        assert decision.decision == "block"
        assert "no_response_pressure_risk" in decision.reasons
        assert decision.review_required is True

    def test_edge_decision_payloads_have_no_delivery_or_platform_fields(self) -> None:
        decision = ProactivePolicyGate().evaluate(
            _consent(),
            _candidate(),
            recent_suggestion_count=2,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )
        serialized = json.dumps(decision.model_dump(mode="json"), ensure_ascii=False).lower()

        for forbidden in (
            "send",
            "schedule",
            "delivery",
            "platform",
            "webhook",
            "token",
            "queue",
        ):
            assert forbidden not in serialized
