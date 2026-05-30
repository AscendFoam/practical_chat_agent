"""Deterministic review-first proactive policy gate."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import ProactiveConsent


ProactivePolicyDecisionValue = Literal["allow_for_review", "block", "defer"]


class ProactiveCandidateMetadata(BaseModel):
    schema_version: str = "proactive_candidate_metadata_v1"
    candidate_id: str = Field(default_factory=lambda: new_id("procand"))
    user_id: str = Field(..., min_length=1)
    surface: str = Field(..., min_length=1)
    intent: str = Field(..., min_length=1)
    summary: str = Field(..., min_length=1)
    safety_flags: list[str] = Field(default_factory=list)


class ProactivePolicyDecision(BaseModel):
    schema_version: str = "proactive_policy_decision_v1"
    decision_id: str = Field(default_factory=lambda: new_id("propold"))
    candidate_id: str
    decision: ProactivePolicyDecisionValue
    reasons: list[str] = Field(default_factory=list)
    review_required: bool = True
    allowed_surface: str | None = None


class ProactivePolicyGate:
    """Evaluate already-provided proactive candidate metadata."""

    def evaluate(
        self,
        consent: ProactiveConsent,
        candidate: ProactiveCandidateMetadata,
        *,
        recent_suggestion_count: int,
        hours_since_last_suggestion: float,
        is_quiet_hours: bool,
    ) -> ProactivePolicyDecision:
        if consent.status != "enabled":
            return self._decision(candidate, "block", ["consent_not_enabled"])

        if candidate.surface not in consent.allowed_surfaces:
            return self._decision(candidate, "block", ["surface_not_allowed"])

        if candidate.intent not in consent.allowed_intents:
            return self._decision(candidate, "block", ["intent_not_allowed"])

        if is_quiet_hours:
            return self._decision(candidate, "defer", ["quiet_hours"])

        if recent_suggestion_count >= consent.max_suggestions_per_day:
            return self._decision(candidate, "block", ["frequency_cap_reached"])

        if hours_since_last_suggestion < consent.min_interval_hours:
            return self._decision(candidate, "block", ["minimum_interval_not_met"])

        return self._decision(
            candidate,
            "allow_for_review",
            ["human_review_required"],
            allowed_surface=candidate.surface,
        )

    @staticmethod
    def _decision(
        candidate: ProactiveCandidateMetadata,
        decision: ProactivePolicyDecisionValue,
        reasons: list[str],
        *,
        allowed_surface: str | None = None,
    ) -> ProactivePolicyDecision:
        return ProactivePolicyDecision(
            candidate_id=candidate.candidate_id,
            decision=decision,
            reasons=reasons,
            allowed_surface=allowed_surface,
        )
