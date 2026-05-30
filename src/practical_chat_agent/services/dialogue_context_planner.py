"""Deterministic planning metadata from relationship context bundles."""

from __future__ import annotations

from pydantic import BaseModel, Field

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import RelationshipContextBundle


class DialogueContextPlan(BaseModel):
    schema_version: str = "dialogue_context_plan_v1"
    plan_id: str = Field(default_factory=lambda: new_id("dlgplan"))
    context_bundle_id: str
    tone_guidance: str
    response_length_guidance: str = "short_to_medium"
    boundary_reminders: list[str] = Field(default_factory=list)
    memory_use_notes: list[str] = Field(default_factory=list)
    relationship_pacing_notes: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)


class DialogueContextPlanner:
    """Build non-generative dialogue planning metadata."""

    def plan(self, bundle: RelationshipContextBundle) -> DialogueContextPlan:
        dimensions = bundle.relationship_dimensions
        trust = dimensions.get("trust", 0.0)
        warmth = dimensions.get("warmth", 0.0)
        boundary_risk = dimensions.get("boundary_risk", 0.0)

        boundary_reminders: list[str] = []
        relationship_pacing_notes: list[str] = []
        safety_warnings: list[str] = list(bundle.safety_warnings)

        if boundary_risk >= 0.7:
            tone_guidance = "cautious_warm"
            boundary_reminders.append("boundary_sensitive")
            relationship_pacing_notes.append("slow_down_and_check_consent")
            safety_warnings.append("avoid_pressure_or_escalation")
        elif trust >= 0.75 and warmth >= 0.75:
            tone_guidance = "warm_personal"
            relationship_pacing_notes.append("slow_warmth_ok")
        else:
            tone_guidance = "steady_warm"
            relationship_pacing_notes.append("maintain_gradual_pacing")

        memory_use_notes = self._memory_use_notes(bundle)
        if bundle.memory.imagined_memory_count:
            safety_warnings.append("contains_imagined_memory")

        return DialogueContextPlan(
            context_bundle_id=bundle.context_bundle_id,
            tone_guidance=tone_guidance,
            boundary_reminders=self._dedupe(boundary_reminders),
            memory_use_notes=self._dedupe(memory_use_notes),
            relationship_pacing_notes=self._dedupe(relationship_pacing_notes),
            safety_warnings=self._dedupe(safety_warnings),
        )

    @staticmethod
    def _memory_use_notes(bundle: RelationshipContextBundle) -> list[str]:
        notes = ["do_not_treat_imagined_memory_as_fact"]
        if bundle.memory.purpose == "factual_response":
            notes.append("use_evidence_backed_memory_only")
        if bundle.memory.imagined_memory_count or bundle.memory.purpose == "imagined_context":
            notes.append("imagined_memory_label_required")
        return notes

    @staticmethod
    def _dedupe(values: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for value in values:
            if value not in seen:
                seen.add(value)
                result.append(value)
        return result
