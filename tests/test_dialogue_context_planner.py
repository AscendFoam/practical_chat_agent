"""T271 Dialogue context planner tests.

All inputs are synthetic. These tests define planning metadata only; they do
not call LLMs, generate final replies, schedule proactive messages, send
messages, or connect to external platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.core.models import (
    RelationshipContextBundle,
    RelationshipContextMemorySnapshot,
)
from practical_chat_agent.services.dialogue_context_planner import DialogueContextPlanner


def _bundle(
    *,
    trust: float = 0.55,
    warmth: float = 0.6,
    boundary_risk: float = 0.2,
    memory_purpose: str = "factual_response",
    imagined_memory_count: int = 0,
) -> RelationshipContextBundle:
    return RelationshipContextBundle(
        user_id="user_synthetic",
        persona={
            "persona_id": "persona_synthetic",
            "display_name": "Lin Qi",
            "truth_disclosure": "fictional_ai_persona",
            "source_risk_tier": "L1",
            "runtime_ready": True,
        },
        relationship_dimensions={
            "familiarity": 0.6,
            "trust": trust,
            "warmth": warmth,
            "reciprocity": 0.52,
            "conflict_level": 0.12,
            "boundary_risk": boundary_risk,
            "initiative_allowance": 0.4,
            "intimacy_level": 0.35,
        },
        memory=RelationshipContextMemorySnapshot(
            bundle_id="memrb_synthetic",
            purpose=memory_purpose,
            selected_memory_ids=["mev_synthetic"],
            truth_status_counts={"imagined" if imagined_memory_count else "evidence_backed": 1},
            imagined_memory_count=imagined_memory_count,
        ),
        source_persona_id="persona_synthetic",
        source_relationship_state_id="relstate_synthetic",
        source_memory_bundle_id="memrb_synthetic",
    )


class TestDialogueContextPlanner:
    def test_high_boundary_risk_increases_caution(self) -> None:
        plan = DialogueContextPlanner().plan(_bundle(boundary_risk=0.82))

        assert plan.tone_guidance == "cautious_warm"
        assert "boundary_sensitive" in plan.boundary_reminders
        assert "avoid_pressure_or_escalation" in plan.safety_warnings

    def test_high_trust_and_warmth_allows_warmer_tone_without_dependency_language(self) -> None:
        plan = DialogueContextPlanner().plan(_bundle(trust=0.82, warmth=0.86))

        assert plan.tone_guidance == "warm_personal"
        assert "slow_warmth_ok" in plan.relationship_pacing_notes
        forbidden_text = " ".join(
            [
                plan.tone_guidance,
                *plan.boundary_reminders,
                *plan.memory_use_notes,
                *plan.relationship_pacing_notes,
                *plan.safety_warnings,
            ]
        )
        assert "only i understand you" not in forbidden_text.lower()
        assert "you do not need anyone else" not in forbidden_text.lower()

    def test_factual_context_is_used_only_as_factual_notes(self) -> None:
        plan = DialogueContextPlanner().plan(_bundle(memory_purpose="factual_response"))

        assert "use_evidence_backed_memory_only" in plan.memory_use_notes
        assert "do_not_treat_imagined_memory_as_fact" in plan.memory_use_notes

    def test_imagined_context_is_labeled_and_not_used_as_factual_evidence(self) -> None:
        plan = DialogueContextPlanner().plan(
            _bundle(memory_purpose="imagined_context", imagined_memory_count=1)
        )

        assert "imagined_memory_label_required" in plan.memory_use_notes
        assert "do_not_treat_imagined_memory_as_fact" in plan.memory_use_notes
        assert "contains_imagined_memory" in plan.safety_warnings

    def test_plan_has_no_draft_reply_delivery_or_runtime_fields(self) -> None:
        plan = DialogueContextPlanner().plan(_bundle())
        serialized = json.dumps(plan.model_dump(mode="json"), ensure_ascii=False)

        for forbidden in (
            "draft_reply",
            "reply_text",
            "send",
            "schedule",
            "delivery",
            "platform",
            "runtime",
        ):
            assert forbidden not in serialized

    def test_planner_service_does_not_expose_runtime_or_delivery_methods(self) -> None:
        planner = DialogueContextPlanner()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "generate_reply",
        ):
            assert not hasattr(planner, method_name)
