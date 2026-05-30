"""T324 text-first proactive settings prototype tests.

All records are synthetic. These tests define local settings projections only;
they do not generate candidates, schedule messages, send messages, or connect
to platforms.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from practical_chat_agent.core.models import ProactiveConsent
from practical_chat_agent.services.companion_safety_policy import (
    CompanionSafetyPolicy,
    CompanionSafetySignal,
)
from practical_chat_agent.services.proactive_policy_gate import (
    ProactiveCandidateMetadata,
    ProactivePolicyGate,
)
from practical_chat_agent.ui.text_first_proactive_settings import (
    TextFirstProactiveSettingsPrototype,
    TextFirstProactiveSettingsRequest,
)


def _enabled_consent() -> ProactiveConsent:
    return ProactiveConsent(
        user_id="user_synthetic",
        status="enabled",
        allowed_surfaces=["in_app_review_card"],
        allowed_intents=["gentle_check_in", "shared_interest"],
        quiet_hours={"timezone": "Asia/Shanghai", "start": "22:00", "end": "08:00"},
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


def _state(**overrides: object):
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "consent": _enabled_consent(),
    }
    data.update(overrides)
    return TextFirstProactiveSettingsPrototype().project(TextFirstProactiveSettingsRequest(**data))


def test_disabled_paused_and_revoked_consent_appear_as_not_active_settings() -> None:
    paused = ProactiveConsent(
        user_id="user_synthetic",
        status="paused",
        pause_reasons=["user_requested_pause"],
    )
    revoked = ProactiveConsent(
        user_id="user_synthetic",
        status="revoked",
        revoked_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    disabled_state = _state(consent=ProactiveConsent(user_id="user_synthetic", status="disabled"))
    paused_state = _state(consent=paused)
    revoked_state = _state(consent=revoked)

    assert disabled_state.screen == "proactive_disabled"
    assert paused_state.screen == "proactive_paused"
    assert revoked_state.screen == "proactive_revoked"
    for state in (disabled_state, paused_state, revoked_state):
        assert state.outreach_allowed is False
        assert state.has_pending_action is False
        assert "consent_not_enabled" in state.policy_reasons


def test_enabled_consent_displays_review_surfaces_intents_quiet_hours_and_frequency() -> None:
    state = _state()

    assert state.screen == "proactive_enabled_review"
    assert state.consent_status == "enabled"
    assert state.allowed_surfaces == ["in_app_review_card"]
    assert state.allowed_intents == ["gentle_check_in", "shared_interest"]
    assert state.quiet_hours_timezone == "Asia/Shanghai"
    assert state.quiet_hours_start == "22:00"
    assert state.quiet_hours_end == "08:00"
    assert state.max_suggestions_per_day == 2
    assert state.min_interval_hours == 6
    assert state.review_required is True


def test_policy_gate_allow_defer_and_block_decisions_are_reflected_without_sending() -> None:
    gate = ProactivePolicyGate()
    consent = _enabled_consent()
    allow = gate.evaluate(
        consent,
        _candidate(),
        recent_suggestion_count=0,
        hours_since_last_suggestion=24,
        is_quiet_hours=False,
    )
    defer = gate.evaluate(
        consent,
        _candidate(),
        recent_suggestion_count=0,
        hours_since_last_suggestion=24,
        is_quiet_hours=True,
    )
    block = gate.evaluate(
        consent,
        _candidate(safety_flags=["dependency_pressure"]),
        recent_suggestion_count=0,
        hours_since_last_suggestion=24,
        is_quiet_hours=False,
    )

    assert _state(policy_decision=allow).screen == "proactive_allowed_for_review"
    assert _state(policy_decision=defer).screen == "proactive_deferred"
    blocked_state = _state(policy_decision=block)
    assert blocked_state.screen == "proactive_blocked"
    assert "dependency_pressure_risk" in blocked_state.policy_reasons
    assert blocked_state.outreach_allowed is False


def test_crisis_dependency_reasons_keep_proactive_outreach_blocked() -> None:
    safety_decision = CompanionSafetyPolicy().evaluate(
        CompanionSafetySignal(
            user_id="user_synthetic",
            surface="proactive_review_card",
            signal_summary="Synthetic dependency signal.",
            risk_indicators=["dependency_pressure"],
            recent_dependency_score=0.8,
        )
    )

    state = _state(safety_decision=safety_decision)

    assert state.screen == "proactive_blocked"
    assert "proactive_outreach_blocked" in state.safety_reasons
    assert "dependency_deescalation_required" in state.safety_reasons
    assert state.outreach_allowed is False


def test_proactive_settings_payload_has_no_raw_private_or_delivery_platform_fields() -> None:
    state = _state()

    serialized = json.dumps(state.model_dump(mode="json"), ensure_ascii=False).lower()

    for forbidden in (
        "raw_text",
        "raw_transcript",
        "chat_history",
        "private_messages",
        "send",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "token",
        "queue",
    ):
        assert forbidden not in serialized


def test_proactive_settings_prototype_does_not_expose_runtime_or_outbound_methods() -> None:
    prototype = TextFirstProactiveSettingsPrototype()

    for method_name in (
        "create_candidate",
        "send",
        "schedule",
        "deliver",
        "execute",
        "run_runtime",
        "notify",
    ):
        assert not hasattr(prototype, method_name)
