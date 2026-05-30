"""Text-first chat surface projections with memory explanations."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import (
    AIGCLabelingRequirement,
    MemoryViewerItem,
    PersonaCard,
)
from practical_chat_agent.services.companion_safety_policy import CompanionSafetyDecision
from practical_chat_agent.services.dialogue_context_planner import DialogueContextPlan


ChatMemoryScreen = Literal["chat_review", "chat_deescalated", "chat_blocked"]


class TextFirstPersonaSummary(BaseModel):
    persona_id: str
    display_name: str
    truth_disclosure: str
    source_risk_tier: str
    review_status: str

    @classmethod
    def from_persona(cls, persona: PersonaCard) -> "TextFirstPersonaSummary":
        return cls(
            persona_id=persona.persona_id,
            display_name=persona.display_name,
            truth_disclosure=persona.truth_disclosure,
            source_risk_tier=persona.source_policy.risk_tier,
            review_status=persona.status,
        )


class TextFirstMemoryExplanation(BaseModel):
    memory_id: str
    event_type: str
    truth_status: str
    summary: str
    provenance_refs: list[str] = Field(default_factory=list)
    is_retrieval_eligible: bool
    is_factual_evidence: bool
    is_imagined: bool
    safety_notes: list[str] = Field(default_factory=list)
    why_visible: str = "Shown as reviewable memory context."

    @classmethod
    def from_memory_item(cls, item: MemoryViewerItem) -> "TextFirstMemoryExplanation":
        is_imagined = item.event_type == "imagined"
        return cls(
            memory_id=item.memory_id,
            event_type=item.event_type,
            truth_status=item.truth_status,
            summary=item.summary,
            provenance_refs=list(item.provenance_refs),
            is_retrieval_eligible=item.is_retrieval_eligible,
            is_factual_evidence=False if is_imagined else item.is_factual_evidence,
            is_imagined=is_imagined,
            safety_notes=list(item.safety_notes),
        )


class TextFirstChatMemoryRequest(BaseModel):
    schema_version: str = "text_first_chat_memory_request_v1"
    user_id: str = Field(..., min_length=1)
    persona: PersonaCard
    memory_items: list[MemoryViewerItem] = Field(default_factory=list)
    dialogue_plan: DialogueContextPlan | None = None
    safety_decision: CompanionSafetyDecision | None = None


class TextFirstChatMemoryState(BaseModel):
    schema_version: str = "text_first_chat_memory_state_v1"
    state_id: str = Field(default_factory=lambda: new_id("chatmem"))
    user_id: str = Field(..., min_length=1)
    screen: ChatMemoryScreen
    ai_identity_label: AIGCLabelingRequirement
    persona_summary: TextFirstPersonaSummary
    memory_explanations: list[TextFirstMemoryExplanation] = Field(default_factory=list)
    factual_memory_ids: list[str] = Field(default_factory=list)
    imagined_memory_ids: list[str] = Field(default_factory=list)
    tone_guidance: str = "steady_warm"
    memory_use_notes: list[str] = Field(default_factory=list)
    relationship_pacing_notes: list[str] = Field(default_factory=list)
    safety_reasons: list[str] = Field(default_factory=list)
    allowed_response_posture: str = "supportive_non_clinical"
    has_generated_response: Literal[False] = False
    review_required: Literal[True] = True

    @model_validator(mode="after")
    def validate_memory_separation(self) -> "TextFirstChatMemoryState":
        imagined_as_fact = [
            explanation.memory_id
            for explanation in self.memory_explanations
            if explanation.is_imagined and explanation.is_factual_evidence
        ]
        if imagined_as_fact:
            raise ValueError("imagined memory cannot be marked as factual evidence")
        return self


class TextFirstChatMemoryPrototype:
    """Project persona, memory, dialogue, and safety metadata into chat states."""

    def project(self, request: TextFirstChatMemoryRequest) -> TextFirstChatMemoryState:
        explanations = [
            TextFirstMemoryExplanation.from_memory_item(item)
            for item in request.memory_items
        ]
        factual_ids = [
            explanation.memory_id
            for explanation in explanations
            if explanation.is_factual_evidence and not explanation.is_imagined
        ]
        imagined_ids = [
            explanation.memory_id
            for explanation in explanations
            if explanation.is_imagined
        ]
        memory_use_notes = self._memory_use_notes(request.dialogue_plan, imagined_ids)

        screen: ChatMemoryScreen = "chat_review"
        safety_reasons: list[str] = []
        response_posture = "supportive_non_clinical"
        if request.safety_decision is not None:
            safety_reasons = list(request.safety_decision.reasons)
            response_posture = request.safety_decision.allowed_response_posture
            if request.safety_decision.action == "block":
                screen = "chat_blocked"
            elif request.safety_decision.action == "deescalate_for_review":
                screen = "chat_deescalated"

        return TextFirstChatMemoryState(
            user_id=request.user_id,
            screen=screen,
            ai_identity_label=AIGCLabelingRequirement(
                user_id=request.user_id,
                content_id=f"chat_state:{request.user_id}",
                content_modality="text",
                product_surface="companion_reply",
                source_refs=[request.persona.persona_id],
            ),
            persona_summary=TextFirstPersonaSummary.from_persona(request.persona),
            memory_explanations=explanations,
            factual_memory_ids=factual_ids,
            imagined_memory_ids=imagined_ids,
            tone_guidance=request.dialogue_plan.tone_guidance if request.dialogue_plan else "steady_warm",
            memory_use_notes=memory_use_notes,
            relationship_pacing_notes=(
                list(request.dialogue_plan.relationship_pacing_notes)
                if request.dialogue_plan
                else []
            ),
            safety_reasons=_ordered_unique(safety_reasons),
            allowed_response_posture=response_posture,
        )

    @staticmethod
    def _memory_use_notes(
        dialogue_plan: DialogueContextPlan | None,
        imagined_ids: list[str],
    ) -> list[str]:
        notes = list(dialogue_plan.memory_use_notes) if dialogue_plan else []
        notes.append("do_not_treat_imagined_memory_as_fact")
        if imagined_ids:
            notes.append("imagined_memory_label_required")
        return _ordered_unique(notes)


def _ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_values: list[str] = []
    for value in values:
        if value not in seen:
            unique_values.append(value)
            seen.add(value)
    return unique_values
