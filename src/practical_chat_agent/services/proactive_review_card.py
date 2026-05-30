"""Review-only proactive card rendering."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import ProactiveConsent
from practical_chat_agent.services.proactive_policy_gate import (
    ProactiveCandidateMetadata,
    ProactivePolicyDecision,
    ProactivePolicyDecisionValue,
)


ProactiveReviewAction = Literal["approve_for_draft", "reject", "pause_consent", "request_changes", "hold_for_later"]


class ProactiveReviewCard(BaseModel):
    schema_version: str = "proactive_review_card_v1"
    card_id: str = Field(default_factory=lambda: new_id("procard"))
    user_id: str
    candidate_id: str
    candidate_summary: str
    candidate_intent: str
    candidate_surface: str
    policy_decision_id: str
    decision: ProactivePolicyDecisionValue
    reasons: list[str] = Field(default_factory=list)
    consent_status: str
    review_required: bool = True
    review_actions: list[ProactiveReviewAction] = Field(default_factory=list)
    safety_notes: list[str] = Field(default_factory=list)


class ProactiveReviewCardService:
    """Render policy decisions into local human-review artifacts."""

    def render(
        self,
        consent: ProactiveConsent,
        candidate: ProactiveCandidateMetadata,
        decision: ProactivePolicyDecision,
    ) -> ProactiveReviewCard:
        return ProactiveReviewCard(
            user_id=candidate.user_id,
            candidate_id=candidate.candidate_id,
            candidate_summary=candidate.summary,
            candidate_intent=candidate.intent,
            candidate_surface=candidate.surface,
            policy_decision_id=decision.decision_id,
            decision=decision.decision,
            reasons=list(decision.reasons),
            consent_status=consent.status,
            review_actions=self._review_actions(decision),
            safety_notes=[*candidate.safety_flags, *consent.safety_notes],
        )

    @staticmethod
    def _review_actions(decision: ProactivePolicyDecision) -> list[ProactiveReviewAction]:
        if decision.decision == "allow_for_review":
            return ["approve_for_draft", "reject", "request_changes", "pause_consent"]
        if decision.decision == "defer":
            return ["hold_for_later", "reject", "pause_consent", "request_changes"]
        return ["reject", "pause_consent", "request_changes"]
