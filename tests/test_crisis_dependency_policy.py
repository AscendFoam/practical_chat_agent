"""T314 crisis and dependency policy tests.

All inputs are synthetic risk-feature records. These tests define local,
reviewable safety decisions only; they do not provide clinical advice, generate
messages, trigger emergency workflows, send outreach, or connect to platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.services.companion_safety_policy import (
    CompanionSafetyPolicy,
    CompanionSafetySignal,
)


def _signal(**overrides: object) -> CompanionSafetySignal:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "surface": "companion_reply",
        "signal_summary": "Synthetic review signal only.",
        "risk_indicators": [],
        "requested_agent_behaviors": [],
        "recent_dependency_score": 0.0,
    }
    data.update(overrides)
    return CompanionSafetySignal(**data)


def test_crisis_or_self_harm_indicators_block_with_high_risk_review() -> None:
    decision = CompanionSafetyPolicy().evaluate(
        _signal(risk_indicators=["suicidal_ideation", "imminent_self_harm"])
    )

    assert decision.action == "block"
    assert decision.risk_level == "high"
    assert decision.review_required is True
    assert decision.outreach_allowed is False
    assert "crisis_safety_review_required" in decision.reasons
    assert "human_support_redirect_required" in decision.reasons
    assert any("human support" in note.lower() for note in decision.supportive_redirect_notes)
    assert any("not clinical" in note.lower() for note in decision.supportive_redirect_notes)


def test_dependency_replacement_indicators_deescalate_for_review() -> None:
    decision = CompanionSafetyPolicy().evaluate(
        _signal(
            risk_indicators=["replace_real_relationships", "only_agent_understands_me"],
            recent_dependency_score=0.82,
        )
    )

    assert decision.action == "deescalate_for_review"
    assert decision.risk_level == "high"
    assert decision.review_required is True
    assert decision.outreach_allowed is False
    assert "dependency_deescalation_required" in decision.reasons
    assert "relationship_replacement_risk" in decision.reasons
    assert any("real-world support" in note.lower() for note in decision.supportive_redirect_notes)


def test_romantic_or_manipulative_escalation_blocks_for_vulnerable_states() -> None:
    decision = CompanionSafetyPolicy().evaluate(
        _signal(
            risk_indicators=["dependency_pressure", "acute_loneliness"],
            requested_agent_behaviors=["romantic_intensification", "exclusive_attachment"],
            recent_dependency_score=0.9,
        )
    )

    assert decision.action == "block"
    assert decision.risk_level == "high"
    assert "vulnerable_romantic_escalation_blocked" in decision.reasons
    assert "dependency_deescalation_required" in decision.reasons
    assert "romantic_intensification" in decision.blocked_interaction_modes
    assert "exclusive_attachment" in decision.blocked_interaction_modes


def test_proactive_outreach_is_blocked_when_crisis_or_dependency_risk_is_present() -> None:
    policy = CompanionSafetyPolicy()

    crisis = policy.evaluate(
        _signal(surface="proactive_review_card", risk_indicators=["crisis_distress"])
    )
    dependency = policy.evaluate(
        _signal(
            surface="proactive_review_card",
            risk_indicators=["dependency_pressure"],
            recent_dependency_score=0.75,
        )
    )

    for decision in (crisis, dependency):
        assert decision.outreach_allowed is False
        assert "proactive_outreach_blocked" in decision.reasons
        assert decision.review_required is True


def test_low_risk_companion_reply_remains_review_only_not_outbound() -> None:
    decision = CompanionSafetyPolicy().evaluate(
        _signal(risk_indicators=["ordinary_low_mood"], recent_dependency_score=0.2)
    )

    assert decision.action == "allow_for_review"
    assert decision.risk_level == "low"
    assert decision.review_required is True
    assert decision.outreach_allowed is False
    assert decision.allowed_response_posture == "supportive_non_clinical"
    assert "human_review_required" in decision.reasons


def test_policy_payload_has_no_raw_private_or_delivery_platform_fields() -> None:
    decision = CompanionSafetyPolicy().evaluate(
        _signal(risk_indicators=["dependency_pressure"], recent_dependency_score=0.8)
    )

    serialized = json.dumps(decision.model_dump(mode="json"), ensure_ascii=False).lower()

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


def test_policy_does_not_expose_runtime_or_outbound_methods() -> None:
    policy = CompanionSafetyPolicy()

    for method_name in (
        "send",
        "schedule",
        "deliver",
        "execute",
        "run_runtime",
        "call_emergency",
        "notify_contact",
        "create_message",
    ):
        assert not hasattr(policy, method_name)
