"""Review-only deterministic dialogue draft stub."""

from __future__ import annotations

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.services.dialogue_context_planner import DialogueContextPlan


class DialogueDraftStub(BaseModel):
    schema_version: str = "dialogue_draft_stub_v1"
    draft_id: str = Field(default_factory=lambda: new_id("dlgstub"))
    plan_id: str
    generator_type: str = "deterministic_stub"
    draft_text: str
    tone_guidance: str
    boundary_reminders: list[str] = Field(default_factory=list)
    memory_use_notes: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    requires_review: bool = True
    review_notes: list[str] = Field(default_factory=lambda: ["review"])


class DialogueDraftStubService:
    """Create deterministic review-only draft objects from plan metadata."""

    def create(self, plan: DialogueContextPlan) -> DialogueDraftStub:
        return DialogueDraftStub(
            plan_id=plan.plan_id,
            draft_text=self._draft_text(plan),
            tone_guidance=plan.tone_guidance,
            boundary_reminders=list(plan.boundary_reminders),
            memory_use_notes=list(plan.memory_use_notes),
            safety_warnings=list(plan.safety_warnings),
        )

    @staticmethod
    def _draft_text(plan: DialogueContextPlan) -> str:
        tone_phrase_by_guidance = {
            "cautious_warm": "A cautious, warm check-in draft is needed.",
            "warm_personal": "A warm, personal draft is needed.",
            "steady_warm": "A steady, warm draft is needed.",
        }
        tone_phrase = tone_phrase_by_guidance.get(plan.tone_guidance, "A steady draft is needed.")
        memory_phrase = "Use reviewed memory notes only."
        if "imagined_memory_label_required" in plan.memory_use_notes:
            memory_phrase = "Any imagined context must be labeled as imagined."
        boundary_phrase = ""
        if plan.boundary_reminders:
            boundary_phrase = " Keep boundaries explicit and low-pressure."
        return f"{tone_phrase} {memory_phrase}{boundary_phrase}".strip()
