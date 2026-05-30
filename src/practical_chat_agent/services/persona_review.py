"""Local review-card rendering and review decisions for PersonaCard candidates."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.models import (
    DistillationStatus,
    DistilledArtifactReviewDecision,
    DistilledArtifactReviewMetadata,
    PersonaCard,
    utc_now,
)


PersonaReviewDecision = Literal["approve", "reject", "freeze", "request_changes"]


class PersonaReviewCard(BaseModel):
    schema_version: str = "persona_review_card_v1"
    persona_id: str
    user_id: str
    display_name: str
    status: DistillationStatus
    truth_disclosure: str
    source_policy: dict[str, object] = Field(default_factory=dict)
    identity: dict[str, object] = Field(default_factory=dict)
    traits: dict[str, object] = Field(default_factory=dict)
    speech_style: dict[str, object] = Field(default_factory=dict)
    virtual_history: dict[str, object] = Field(default_factory=dict)
    growth_policy: dict[str, object] = Field(default_factory=dict)
    proactive_preferences: dict[str, object] = Field(default_factory=dict)
    safety_policy: dict[str, object] = Field(default_factory=dict)
    blocked_reason: str | None = None
    allowed_review_decisions: list[PersonaReviewDecision] = Field(
        default_factory=lambda: ["approve", "reject", "freeze", "request_changes"],
    )
    runtime_ready: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonaReviewService:
    """Render PersonaCards for local review and apply explicit review decisions."""

    def render(self, card: PersonaCard) -> PersonaReviewCard:
        virtual_history = card.virtual_history.model_dump(mode="json")
        warnings: list[str] = []

        if card.source_policy.source_type == "prohibited":
            virtual_history["background"] = "[redacted_blocked_request]"
            warnings.append("prohibited_persona_request")
        if card.source_policy.blocked_real_person_similarity:
            warnings.append("blocked_real_person_similarity")

        return PersonaReviewCard(
            persona_id=card.persona_id,
            user_id=card.user_id,
            display_name=card.display_name,
            status=card.status,
            truth_disclosure=card.truth_disclosure,
            source_policy=card.source_policy.model_dump(mode="json"),
            identity=card.identity.model_dump(mode="json"),
            traits=card.core_traits.model_dump(mode="json"),
            speech_style=card.speech_style.model_dump(mode="json"),
            virtual_history=virtual_history,
            growth_policy=card.growth_policy.model_dump(mode="json"),
            proactive_preferences=card.proactive_preferences.model_dump(mode="json"),
            safety_policy=card.safety_policy.model_dump(mode="json"),
            blocked_reason=card.source_policy.prohibited_reason,
            runtime_ready=card.is_runtime_ready(),
            warnings=warnings,
        )

    def review(
        self,
        card: PersonaCard,
        *,
        decision: PersonaReviewDecision,
        reviewer_id: str,
        reviewer_name: str | None = None,
        notes: list[str] | None = None,
    ) -> PersonaCard:
        reviewer_id = reviewer_id.strip()
        if not reviewer_id:
            raise ValueError("reviewer_id is required for persona review decisions")

        next_status = self._status_for_decision(decision)
        if next_status == "approved" and not self._can_approve(card):
            raise ValueError("unsafe PersonaCard cannot be approved")

        review_decision = DistilledArtifactReviewDecision(
            status=next_status,
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            notes=list(notes or []),
            evidence_validation_status="passed" if next_status == "approved" else "not_run",
        )
        review_metadata = DistilledArtifactReviewMetadata(
            review_state="reviewed",
            reviewed_by_human=True,
            last_decision=next_status,
            last_reviewed_at=review_decision.reviewed_at,
            last_reviewer_id=reviewer_id,
            last_reviewer_name=reviewer_name,
            evidence_validation_status=review_decision.evidence_validation_status,
            decision_notes=[
                *card.review_metadata.decision_notes,
                *list(notes or []),
            ],
            history=[*card.review_metadata.history, review_decision],
        )
        return card.model_copy(
            deep=True,
            update={
                "status": next_status,
                "review_metadata": review_metadata,
                "updated_at": utc_now(),
            },
        )

    @staticmethod
    def _status_for_decision(decision: PersonaReviewDecision) -> DistillationStatus:
        if decision == "approve":
            return "approved"
        if decision == "reject":
            return "rejected"
        if decision == "freeze":
            return "frozen"
        return "candidate"

    @staticmethod
    def _can_approve(card: PersonaCard) -> bool:
        if card.source_policy.source_type == "prohibited":
            return False
        if card.source_policy.risk_tier not in {"L1", "L2"}:
            return False
        if card.source_policy.blocked_real_person_similarity:
            return False
        if not card.identity.fictional or card.identity.public_person_or_real_person_reference:
            return False
        return card.safety_policy.no_deception and card.safety_policy.no_unauthorized_clone
