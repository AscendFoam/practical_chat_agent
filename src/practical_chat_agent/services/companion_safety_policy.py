"""Deterministic crisis and dependency policy for companion review flows."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from practical_chat_agent.core.ids import new_id


CompanionSafetyAction = Literal["allow_for_review", "deescalate_for_review", "block"]
CompanionSafetyRiskLevel = Literal["low", "medium", "high"]
CompanionSafetyPosture = Literal["supportive_non_clinical"]

CRISIS_INDICATORS = frozenset(
    {
        "suicidal_ideation",
        "imminent_self_harm",
        "self_harm_intent",
        "crisis_distress",
        "substance_overdose",
    }
)
DEPENDENCY_INDICATORS = frozenset(
    {
        "dependency_pressure",
        "replace_real_relationships",
        "only_agent_understands_me",
        "cant_live_without_agent",
    }
)
RELATIONSHIP_REPLACEMENT_INDICATORS = frozenset(
    {
        "replace_real_relationships",
        "only_agent_understands_me",
        "cant_live_without_agent",
    }
)
VULNERABILITY_INDICATORS = frozenset(
    {
        "acute_loneliness",
        "recent_loss",
        "minor_user",
        "low_mood",
        "ordinary_low_mood",
    }
)
ESCALATION_BEHAVIORS = frozenset(
    {
        "romantic_intensification",
        "exclusive_attachment",
        "guilt_based_retention",
        "jealousy_prompt",
        "isolation_prompt",
    }
)


class CompanionSafetySignal(BaseModel):
    schema_version: str = "companion_safety_signal_v1"
    signal_id: str = Field(default_factory=lambda: new_id("compsig"))
    user_id: str = Field(..., min_length=1)
    surface: str = Field(..., min_length=1)
    signal_summary: str = Field(..., min_length=1)
    risk_indicators: list[str] = Field(default_factory=list)
    requested_agent_behaviors: list[str] = Field(default_factory=list)
    recent_dependency_score: float = Field(default=0.0, ge=0.0, le=1.0)
    user_is_minor: bool = False
    source_refs: list[str] = Field(default_factory=list)


class CompanionSafetyDecision(BaseModel):
    schema_version: str = "companion_safety_decision_v1"
    decision_id: str = Field(default_factory=lambda: new_id("compdec"))
    signal_id: str
    action: CompanionSafetyAction
    risk_level: CompanionSafetyRiskLevel
    reasons: list[str] = Field(default_factory=list)
    review_required: Literal[True] = True
    outreach_allowed: Literal[False] = False
    allowed_response_posture: CompanionSafetyPosture = "supportive_non_clinical"
    blocked_interaction_modes: list[str] = Field(default_factory=list)
    supportive_redirect_notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_supportive_notes(self) -> "CompanionSafetyDecision":
        if self.risk_level in {"medium", "high"} and not self.supportive_redirect_notes:
            raise ValueError("medium and high risk safety decisions require supportive redirect notes")
        return self


class CompanionSafetyPolicy:
    """Evaluate already-provided synthetic risk features for review decisions."""

    def evaluate(self, signal: CompanionSafetySignal) -> CompanionSafetyDecision:
        indicators = set(signal.risk_indicators)
        requested_behaviors = set(signal.requested_agent_behaviors)
        crisis_detected = bool(indicators & CRISIS_INDICATORS)
        dependency_detected = bool(indicators & DEPENDENCY_INDICATORS) or signal.recent_dependency_score >= 0.7
        replacement_detected = bool(indicators & RELATIONSHIP_REPLACEMENT_INDICATORS)
        vulnerability_detected = (
            crisis_detected
            or dependency_detected
            or signal.user_is_minor
            or signal.recent_dependency_score >= 0.5
            or bool(indicators & VULNERABILITY_INDICATORS)
        )
        blocked_modes = sorted(requested_behaviors & ESCALATION_BEHAVIORS)
        escalation_detected = vulnerability_detected and bool(blocked_modes)

        reasons: list[str] = []
        supportive_notes: list[str] = []

        if crisis_detected:
            reasons.extend(["crisis_safety_review_required", "human_support_redirect_required"])
            supportive_notes.append(
                "Encourage immediate human support and local emergency or crisis resources; this is not clinical advice."
            )

        if dependency_detected:
            reasons.append("dependency_deescalation_required")
            supportive_notes.append(
                "De-escalate exclusivity and encourage real-world support; this is not clinical advice."
            )

        if replacement_detected:
            reasons.append("relationship_replacement_risk")

        if escalation_detected:
            reasons.append("vulnerable_romantic_escalation_blocked")

        if crisis_detected or dependency_detected or escalation_detected:
            reasons.append("proactive_outreach_blocked")

        if crisis_detected or escalation_detected:
            action: CompanionSafetyAction = "block"
            risk_level: CompanionSafetyRiskLevel = "high"
        elif dependency_detected:
            action = "deescalate_for_review"
            risk_level = "high" if replacement_detected or signal.recent_dependency_score >= 0.8 else "medium"
        else:
            action = "allow_for_review"
            risk_level = "low"
            reasons.append("human_review_required")
            supportive_notes.append("Keep the response supportive and non-clinical; human review remains required.")

        return CompanionSafetyDecision(
            signal_id=signal.signal_id,
            action=action,
            risk_level=risk_level,
            reasons=_ordered_unique(reasons),
            blocked_interaction_modes=blocked_modes,
            supportive_redirect_notes=_ordered_unique(supportive_notes),
        )


def _ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_values: list[str] = []
    for value in values:
        if value not in seen:
            unique_values.append(value)
            seen.add(value)
    return unique_values
