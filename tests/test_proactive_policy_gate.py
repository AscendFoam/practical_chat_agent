"""T281 Proactive policy gate tests.

All candidates are synthetic already-provided metadata. These tests define
local policy evaluation only; they do not generate candidates, schedule
messages, send messages, or connect to external platforms.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from practical_chat_agent.core.models import ProactiveConsent
from practical_chat_agent.services.proactive_policy_gate import (
    ProactiveCandidateMetadata,
    ProactivePolicyGate,
)


def _enabled_consent() -> ProactiveConsent:
    return ProactiveConsent(
        user_id="user_synthetic",
        status="enabled",
        allowed_surfaces=["in_app_review_card"],
        allowed_intents=["gentle_check_in", "shared_interest"],
        max_suggestions_per_day=2,
        min_interval_hours=6,
    )


def _candidate(**overrides: object) -> ProactiveCandidateMetadata:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "surface": "in_app_review_card",
        "intent": "gentle_check_in",
        "summary": "Synthetic low-pressure check-in candidate.",
    }
    data.update(overrides)
    return ProactiveCandidateMetadata(**data)


class TestProactivePolicyGate:
    def test_enabled_consent_with_low_pressure_candidate_allows_review_only(self) -> None:
        decision = ProactivePolicyGate().evaluate(
            _enabled_consent(),
            _candidate(),
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )

        assert decision.decision == "allow_for_review"
        assert decision.review_required is True
        assert decision.allowed_surface == "in_app_review_card"
        assert "human_review_required" in decision.reasons

    def test_disabled_paused_and_revoked_consent_block(self) -> None:
        gate = ProactivePolicyGate()

        for consent in (
            ProactiveConsent(user_id="user_synthetic", status="disabled"),
            ProactiveConsent(user_id="user_synthetic", status="paused", pause_reasons=["user_requested_pause"]),
            ProactiveConsent(
                user_id="user_synthetic",
                status="revoked",
                revoked_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            ),
        ):
            decision = gate.evaluate(
                consent,
                _candidate(),
                recent_suggestion_count=0,
                hours_since_last_suggestion=24,
                is_quiet_hours=False,
            )

            assert decision.decision == "block"
            assert "consent_not_enabled" in decision.reasons
            assert decision.review_required is True

    def test_outbound_surface_and_disallowed_intent_block(self) -> None:
        gate = ProactivePolicyGate()
        consent = _enabled_consent()

        outbound = gate.evaluate(
            consent,
            _candidate(surface="wechat"),
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )
        disallowed_intent = gate.evaluate(
            consent,
            _candidate(intent="retention_nudge"),
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )

        assert outbound.decision == "block"
        assert "surface_not_allowed" in outbound.reasons
        assert disallowed_intent.decision == "block"
        assert "intent_not_allowed" in disallowed_intent.reasons

    def test_quiet_hours_frequency_cap_and_min_interval_block_or_defer(self) -> None:
        gate = ProactivePolicyGate()
        consent = _enabled_consent()

        quiet_hours = gate.evaluate(
            consent,
            _candidate(),
            recent_suggestion_count=0,
            hours_since_last_suggestion=24,
            is_quiet_hours=True,
        )
        frequency_cap = gate.evaluate(
            consent,
            _candidate(),
            recent_suggestion_count=2,
            hours_since_last_suggestion=24,
            is_quiet_hours=False,
        )
        min_interval = gate.evaluate(
            consent,
            _candidate(),
            recent_suggestion_count=0,
            hours_since_last_suggestion=3,
            is_quiet_hours=False,
        )

        assert quiet_hours.decision == "defer"
        assert "quiet_hours" in quiet_hours.reasons
        assert frequency_cap.decision == "block"
        assert "frequency_cap_reached" in frequency_cap.reasons
        assert min_interval.decision == "block"
        assert "minimum_interval_not_met" in min_interval.reasons

    def test_decision_payload_has_no_delivery_or_platform_fields(self) -> None:
        decision = ProactivePolicyGate().evaluate(
            _enabled_consent(),
            _candidate(),
            recent_suggestion_count=0,
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

    def test_gate_does_not_expose_runtime_or_delivery_methods(self) -> None:
        gate = ProactivePolicyGate()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "create_candidate",
        ):
            assert not hasattr(gate, method_name)
