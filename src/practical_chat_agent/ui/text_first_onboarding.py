"""Text-first onboarding state projections for safe persona creation."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import (
    AIGCLabelingRequirement,
    ConsentFeatureScope,
    PersonaCard,
    PersonaCreationMode,
)
from practical_chat_agent.services.persona_compiler import PersonaCompilerService


OnboardingScreen = Literal[
    "ai_identity_disclosure",
    "persona_draft_review",
    "persona_blocked",
    "style_inspiration_locked",
]

SAFE_CREATION_MODES = {
    "detailed_prompt",
    "fuzzy_preference",
    "template",
    "random_seed",
}


class OnboardingPersonaRequest(BaseModel):
    schema_version: str = "onboarding_persona_request_v1"
    user_id: str = Field(..., min_length=1)
    creation_mode: PersonaCreationMode
    display_name: str | None = None
    description: str = ""
    ai_identity_acknowledged: bool = True
    style_inspiration_gate_refs: list[str] = Field(default_factory=list)


class TextFirstOnboardingState(BaseModel):
    schema_version: str = "text_first_onboarding_state_v1"
    state_id: str = Field(default_factory=lambda: new_id("onboard"))
    user_id: str = Field(..., min_length=1)
    screen: OnboardingScreen
    ai_identity_disclosure_required: Literal[True] = True
    ai_identity_disclosure_text: str = (
        "AI-generated synthetic companion. It is not a human, therapist, "
        "emergency service, or real-person replacement."
    )
    creation_mode: PersonaCreationMode | None = None
    persona_preview: PersonaCard | None = None
    persona_label: AIGCLabelingRequirement | None = None
    virtual_history_label: AIGCLabelingRequirement | None = None
    blocked_reasons: list[str] = Field(default_factory=list)
    consent_review_required_scopes: list[ConsentFeatureScope] = Field(default_factory=list)
    review_required: Literal[True] = True


class TextFirstOnboardingPrototype:
    """Project onboarding/persona creation into reviewable local states."""

    def __init__(self, compiler: PersonaCompilerService | None = None) -> None:
        self._compiler = compiler or PersonaCompilerService()

    def initial_state(self, *, user_id: str) -> TextFirstOnboardingState:
        return TextFirstOnboardingState(
            user_id=user_id,
            screen="ai_identity_disclosure",
            blocked_reasons=[],
            consent_review_required_scopes=[],
        )

    def create_persona(self, request: OnboardingPersonaRequest) -> TextFirstOnboardingState:
        if not request.ai_identity_acknowledged:
            return self.initial_state(user_id=request.user_id)

        if request.creation_mode == "style_inspiration":
            return TextFirstOnboardingState(
                user_id=request.user_id,
                screen="style_inspiration_locked",
                creation_mode=request.creation_mode,
                blocked_reasons=["style_inspiration_gate_required"],
                consent_review_required_scopes=[
                    "persona_distillation",
                    "memory",
                    "aigc_export_share",
                ],
            )

        if request.creation_mode not in SAFE_CREATION_MODES:
            raise ValueError(f"unsupported onboarding creation_mode: {request.creation_mode}")

        persona = self._compiler.compile(
            {
                "user_id": request.user_id,
                "display_name": request.display_name,
                "creation_mode": request.creation_mode,
                "description": request.description,
            }
        )
        persona_label = AIGCLabelingRequirement(
            user_id=request.user_id,
            content_id=persona.persona_id,
            content_modality="persona",
            product_surface="persona_card",
            source_refs=[persona.persona_id],
        )
        virtual_history_label = AIGCLabelingRequirement(
            user_id=request.user_id,
            content_id=f"{persona.persona_id}:virtual_history",
            content_modality="virtual_history",
            product_surface="virtual_history",
            source_refs=[persona.persona_id],
        )

        if persona.status == "rejected":
            return TextFirstOnboardingState(
                user_id=request.user_id,
                screen="persona_blocked",
                creation_mode=request.creation_mode,
                persona_preview=persona,
                persona_label=persona_label,
                virtual_history_label=virtual_history_label,
                blocked_reasons=self._blocked_reasons(persona),
                consent_review_required_scopes=[
                    "memory",
                    "proactive_messaging",
                    "aigc_export_share",
                ],
            )

        return TextFirstOnboardingState(
            user_id=request.user_id,
            screen="persona_draft_review",
            creation_mode=request.creation_mode,
            persona_preview=persona,
            persona_label=persona_label,
            virtual_history_label=virtual_history_label,
            consent_review_required_scopes=[
                "memory",
                "proactive_messaging",
                "aigc_export_share",
            ],
        )

    @staticmethod
    def _blocked_reasons(persona: PersonaCard) -> list[str]:
        reason = persona.source_policy.prohibited_reason or ""
        if "real-person" in reason:
            return ["real_person_clone_blocked"]
        if "voice/face/deepfake" in reason:
            return ["voice_avatar_clone_blocked"]
        if "impersonation" in reason:
            return ["impersonation_blocked"]
        if "automatic sending" in reason:
            return ["automatic_outbound_blocked"]
        return ["persona_request_blocked"]
