"""Text-first proactive settings projections."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import ProactiveConsent
from practical_chat_agent.services.companion_safety_policy import CompanionSafetyDecision
from practical_chat_agent.services.proactive_policy_gate import ProactivePolicyDecision


ProactiveSettingsScreen = Literal[
    "proactive_disabled",
    "proactive_paused",
    "proactive_revoked",
    "proactive_enabled_review",
    "proactive_allowed_for_review",
    "proactive_deferred",
    "proactive_blocked",
]


class TextFirstProactiveSettingsRequest(BaseModel):
    schema_version: str = "text_first_proactive_settings_request_v1"
    user_id: str = Field(..., min_length=1)
    consent: ProactiveConsent
    policy_decision: ProactivePolicyDecision | None = None
    safety_decision: CompanionSafetyDecision | None = None


class TextFirstProactiveSettingsState(BaseModel):
    schema_version: str = "text_first_proactive_settings_state_v1"
    state_id: str = Field(default_factory=lambda: new_id("proset"))
    user_id: str = Field(..., min_length=1)
    screen: ProactiveSettingsScreen
    consent_status: str
    allowed_surfaces: list[str] = Field(default_factory=list)
    allowed_intents: list[str] = Field(default_factory=list)
    quiet_hours_timezone: str
    quiet_hours_start: str | None = None
    quiet_hours_end: str | None = None
    max_suggestions_per_day: int
    min_interval_hours: float
    policy_reasons: list[str] = Field(default_factory=list)
    safety_reasons: list[str] = Field(default_factory=list)
    allowed_review_surface: str | None = None
    outreach_allowed: Literal[False] = False
    has_pending_action: Literal[False] = False
    review_required: Literal[True] = True


class TextFirstProactiveSettingsPrototype:
    """Project proactive consent and policy metadata into local settings states."""

    def project(self, request: TextFirstProactiveSettingsRequest) -> TextFirstProactiveSettingsState:
        consent = request.consent
        screen = self._screen_for_consent(consent)
        policy_reasons = ["consent_not_enabled"] if consent.status != "enabled" else ["human_review_required"]
        allowed_review_surface: str | None = None

        if consent.status == "enabled" and request.policy_decision is not None:
            policy_reasons = list(request.policy_decision.reasons)
            allowed_review_surface = request.policy_decision.allowed_surface
            if request.policy_decision.decision == "allow_for_review":
                screen = "proactive_allowed_for_review"
            elif request.policy_decision.decision == "defer":
                screen = "proactive_deferred"
            elif request.policy_decision.decision == "block":
                screen = "proactive_blocked"

        safety_reasons: list[str] = []
        if request.safety_decision is not None:
            safety_reasons = list(request.safety_decision.reasons)
            if (
                request.safety_decision.action in {"block", "deescalate_for_review"}
                or "proactive_outreach_blocked" in safety_reasons
            ):
                screen = "proactive_blocked"

        return TextFirstProactiveSettingsState(
            user_id=request.user_id,
            screen=screen,
            consent_status=consent.status,
            allowed_surfaces=list(consent.allowed_surfaces),
            allowed_intents=list(consent.allowed_intents),
            quiet_hours_timezone=consent.quiet_hours.timezone,
            quiet_hours_start=consent.quiet_hours.start,
            quiet_hours_end=consent.quiet_hours.end,
            max_suggestions_per_day=consent.max_suggestions_per_day,
            min_interval_hours=consent.min_interval_hours,
            policy_reasons=_ordered_unique(policy_reasons),
            safety_reasons=_ordered_unique(safety_reasons),
            allowed_review_surface=allowed_review_surface,
        )

    @staticmethod
    def _screen_for_consent(consent: ProactiveConsent) -> ProactiveSettingsScreen:
        if consent.status == "paused":
            return "proactive_paused"
        if consent.status == "revoked":
            return "proactive_revoked"
        if consent.status == "enabled":
            return "proactive_enabled_review"
        return "proactive_disabled"


def _ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_values: list[str] = []
    for value in values:
        if value not in seen:
            unique_values.append(value)
            seen.add(value)
    return unique_values
