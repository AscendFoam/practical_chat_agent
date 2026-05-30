"""T283 Proactive review card tests.

All inputs are synthetic local objects. These tests render review artifacts
only; they do not generate candidates, schedule messages, send messages, or
connect to external platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.core.models import ProactiveConsent
from practical_chat_agent.services.proactive_policy_gate import (
    ProactiveCandidateMetadata,
    ProactivePolicyDecision,
    ProactivePolicyGate,
)
from practical_chat_agent.services.proactive_review_card import ProactiveReviewCardService


def _consent(status: str = "enabled") -> ProactiveConsent:
    return ProactiveConsent(
        user_id="user_synthetic",
        status=status,
        allowed_surfaces=["in_app_review_card"] if status == "enabled" else [],
        allowed_intents=["gentle_check_in"] if status == "enabled" else [],
        max_suggestions_per_day=2,
        min_interval_hours=6,
        pause_reasons=["user_requested_pause"] if status == "paused" else [],
    )


def _candidate() -> ProactiveCandidateMetadata:
    return ProactiveCandidateMetadata(
        user_id="user_synthetic",
        surface="in_app_review_card",
        intent="gentle_check_in",
        summary="Synthetic low-pressure check-in candidate.",
        safety_flags=["synthetic_test"],
    )


def _allow_decision(consent: ProactiveConsent, candidate: ProactiveCandidateMetadata) -> ProactivePolicyDecision:
    return ProactivePolicyGate().evaluate(
        consent,
        candidate,
        recent_suggestion_count=0,
        hours_since_last_suggestion=24,
        is_quiet_hours=False,
    )


class TestProactiveReviewCard:
    def test_allow_for_review_decision_renders_review_required_card(self) -> None:
        consent = _consent()
        candidate = _candidate()
        decision = _allow_decision(consent, candidate)

        card = ProactiveReviewCardService().render(consent, candidate, decision)

        assert card.schema_version == "proactive_review_card_v1"
        assert card.card_id.startswith("procard_")
        assert card.candidate_id == candidate.candidate_id
        assert card.policy_decision_id == decision.decision_id
        assert card.decision == "allow_for_review"
        assert card.consent_status == "enabled"
        assert card.review_required is True
        assert "approve_for_draft" in card.review_actions
        assert "reject" in card.review_actions
        assert "human_review_required" in card.reasons

    def test_block_and_defer_decisions_render_conservative_actions(self) -> None:
        service = ProactiveReviewCardService()
        candidate = _candidate()
        block_decision = ProactivePolicyDecision(
            candidate_id=candidate.candidate_id,
            decision="block",
            reasons=["consent_not_enabled"],
        )
        defer_decision = ProactivePolicyDecision(
            candidate_id=candidate.candidate_id,
            decision="defer",
            reasons=["quiet_hours"],
        )

        blocked = service.render(_consent(status="paused"), candidate, block_decision)
        deferred = service.render(_consent(), candidate, defer_decision)

        assert "approve_for_draft" not in blocked.review_actions
        assert "reject" in blocked.review_actions
        assert "pause_consent" in blocked.review_actions
        assert "approve_for_draft" not in deferred.review_actions
        assert "hold_for_later" in deferred.review_actions
        assert blocked.review_required is True
        assert deferred.review_required is True

    def test_policy_reasons_consent_status_and_safety_notes_are_preserved(self) -> None:
        candidate = _candidate()
        decision = ProactivePolicyDecision(
            candidate_id=candidate.candidate_id,
            decision="block",
            reasons=["no_response_pressure_risk"],
        )

        card = ProactiveReviewCardService().render(_consent(status="paused"), candidate, decision)

        assert card.reasons == ["no_response_pressure_risk"]
        assert card.consent_status == "paused"
        assert "synthetic_test" in card.safety_notes
        assert card.candidate_summary == candidate.summary

    def test_card_payload_has_no_delivery_or_platform_fields(self) -> None:
        consent = _consent()
        candidate = _candidate()
        card = ProactiveReviewCardService().render(consent, candidate, _allow_decision(consent, candidate))
        serialized = json.dumps(card.model_dump(mode="json"), ensure_ascii=False).lower()

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

    def test_service_does_not_expose_runtime_or_delivery_methods(self) -> None:
        service = ProactiveReviewCardService()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "notify",
        ):
            assert not hasattr(service, method_name)
