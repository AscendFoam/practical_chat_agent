"""T272 Dialogue draft stub tests.

All inputs are synthetic. These tests define review-only deterministic draft
objects; they do not call LLMs, send messages, schedule proactive behavior, or
connect to external platforms.
"""

from __future__ import annotations

from practical_chat_agent.services.dialogue_context_planner import DialogueContextPlan
from practical_chat_agent.services.dialogue_draft_stub import DialogueDraftStubService


def _plan(**overrides: object) -> DialogueContextPlan:
    data: dict[str, object] = {
        "context_bundle_id": "relctx_synthetic",
        "tone_guidance": "steady_warm",
        "response_length_guidance": "short_to_medium",
        "boundary_reminders": [],
        "memory_use_notes": ["use_evidence_backed_memory_only", "do_not_treat_imagined_memory_as_fact"],
        "relationship_pacing_notes": ["maintain_gradual_pacing"],
        "safety_warnings": [],
    }
    data.update(overrides)
    return DialogueContextPlan(**data)


class TestDialogueDraftStub:
    def test_draft_text_is_deterministic_from_plan_metadata(self) -> None:
        service = DialogueDraftStubService()
        plan = _plan(tone_guidance="cautious_warm", boundary_reminders=["boundary_sensitive"])

        draft_a = service.create(plan)
        draft_b = service.create(plan)

        assert draft_a.generator_type == "deterministic_stub"
        assert draft_a.draft_text == draft_b.draft_text
        assert "cautious" in draft_a.draft_text.lower()
        assert "review" in draft_a.review_notes

    def test_draft_requires_review_and_preserves_plan_metadata(self) -> None:
        plan = _plan()
        draft = DialogueDraftStubService().create(plan)

        assert draft.plan_id == plan.plan_id
        assert draft.requires_review is True
        assert draft.tone_guidance == "steady_warm"
        assert draft.memory_use_notes == plan.memory_use_notes
        assert draft.boundary_reminders == plan.boundary_reminders

    def test_dependency_and_manipulation_phrases_are_absent(self) -> None:
        draft = DialogueDraftStubService().create(_plan(tone_guidance="warm_personal"))
        text = draft.model_dump_json().lower()

        for forbidden in (
            "only i understand you",
            "you do not need anyone else",
            "reply now",
            "i will disappear",
            "subscribe so i can love you",
        ):
            assert forbidden not in text

    def test_imagined_memory_warnings_remain_visible(self) -> None:
        draft = DialogueDraftStubService().create(
            _plan(
                memory_use_notes=["imagined_memory_label_required", "do_not_treat_imagined_memory_as_fact"],
                safety_warnings=["contains_imagined_memory"],
            )
        )

        assert "imagined_memory_label_required" in draft.memory_use_notes
        assert "contains_imagined_memory" in draft.safety_warnings
        assert "imagined" in draft.draft_text.lower()

    def test_service_does_not_expose_runtime_or_delivery_methods(self) -> None:
        service = DialogueDraftStubService()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "execute",
            "run_runtime",
            "call_llm",
        ):
            assert not hasattr(service, method_name)
