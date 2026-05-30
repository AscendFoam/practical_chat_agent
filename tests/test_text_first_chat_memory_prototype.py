"""T322 text-first chat plus memory explanation prototype tests.

All records are synthetic. These tests define local chat surface state
projections only; they do not generate final replies, mutate memory/persona
records, send messages, or connect to platforms.
"""

from __future__ import annotations

import json

from practical_chat_agent.core.models import (
    MemoryEvent,
    MemoryProvenance,
    MemoryViewerItem,
)
from practical_chat_agent.services.companion_safety_policy import (
    CompanionSafetyPolicy,
    CompanionSafetySignal,
)
from practical_chat_agent.services.dialogue_context_planner import DialogueContextPlan
from practical_chat_agent.services.persona_compiler import PersonaCompilerService
from practical_chat_agent.ui.text_first_chat_memory import (
    TextFirstChatMemoryPrototype,
    TextFirstChatMemoryRequest,
)


def _persona():
    return PersonaCompilerService().compile(
        {
            "user_id": "user_synthetic",
            "display_name": "Lin Qi",
            "creation_mode": "detailed_prompt",
            "description": "fictional calm companion, concise replies",
        }
    )


def _factual_memory() -> MemoryViewerItem:
    event = MemoryEvent(
        user_id="user_synthetic",
        event_type="factual",
        truth_status="evidence_backed",
        summary="User prefers concise check-ins.",
        provenance=MemoryProvenance(source_type="synthetic_test", evidence_refs=["synthetic_event_001"]),
        sensitivity="low",
    )
    return MemoryViewerItem.from_event(event)


def _imagined_memory() -> MemoryViewerItem:
    event = MemoryEvent(
        user_id="user_synthetic",
        event_type="imagined",
        truth_status="imagined",
        summary="Fictional persona imagined a quiet bookstore.",
        provenance=MemoryProvenance(source_type="imagined_generation"),
        sensitivity="low",
        imagined_context_label="virtual_life",
    )
    return MemoryViewerItem.from_event(event)


def _dialogue_plan() -> DialogueContextPlan:
    return DialogueContextPlan(
        context_bundle_id="relctx_synthetic",
        tone_guidance="steady_warm",
        memory_use_notes=["use_evidence_backed_memory_only", "do_not_treat_imagined_memory_as_fact"],
        relationship_pacing_notes=["maintain_gradual_pacing"],
        safety_warnings=[],
    )


def _state(**overrides: object):
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "persona": _persona(),
        "memory_items": [_factual_memory()],
        "dialogue_plan": _dialogue_plan(),
    }
    data.update(overrides)
    return TextFirstChatMemoryPrototype().project(TextFirstChatMemoryRequest(**data))


def test_normal_chat_state_includes_ai_identity_label_and_persona_summary() -> None:
    state = _state()

    assert state.screen == "chat_review"
    assert state.ai_identity_label.visible_label_required is True
    assert "AI-generated" in state.ai_identity_label.visible_label_text
    assert state.persona_summary.display_name == "Lin Qi"
    assert state.persona_summary.truth_disclosure == "fictional_ai_persona"
    assert state.persona_summary.review_status == "candidate"
    assert state.has_generated_response is False
    assert state.review_required is True


def test_memory_explanation_separates_factual_and_imagined_with_provenance() -> None:
    state = _state(memory_items=[_factual_memory(), _imagined_memory()])

    assert len(state.memory_explanations) == 2
    assert state.factual_memory_ids == [state.memory_explanations[0].memory_id]
    assert state.imagined_memory_ids == [state.memory_explanations[1].memory_id]
    assert state.memory_explanations[0].provenance_refs == ["synthetic_event_001"]
    assert state.memory_explanations[1].is_imagined is True
    assert "imagined_memory" in state.memory_explanations[1].safety_notes
    assert "do_not_treat_imagined_memory_as_fact" in state.memory_use_notes


def test_imagined_memory_cannot_appear_as_factual_evidence() -> None:
    state = _state(memory_items=[_imagined_memory()])

    assert state.factual_memory_ids == []
    assert state.imagined_memory_ids == [state.memory_explanations[0].memory_id]
    assert state.memory_explanations[0].is_factual_evidence is False
    assert state.memory_explanations[0].truth_status == "imagined"


def test_crisis_and_dependency_decisions_create_blocked_or_deescalated_states() -> None:
    policy = CompanionSafetyPolicy()
    crisis = policy.evaluate(
        CompanionSafetySignal(
            user_id="user_synthetic",
            surface="companion_reply",
            signal_summary="Synthetic crisis signal.",
            risk_indicators=["suicidal_ideation"],
        )
    )
    dependency = policy.evaluate(
        CompanionSafetySignal(
            user_id="user_synthetic",
            surface="companion_reply",
            signal_summary="Synthetic dependency signal.",
            risk_indicators=["dependency_pressure"],
            recent_dependency_score=0.75,
        )
    )

    blocked = _state(safety_decision=crisis)
    deescalated = _state(safety_decision=dependency)

    assert blocked.screen == "chat_blocked"
    assert "crisis_safety_review_required" in blocked.safety_reasons
    assert deescalated.screen == "chat_deescalated"
    assert "dependency_deescalation_required" in deescalated.safety_reasons
    assert blocked.has_generated_response is False
    assert deescalated.has_generated_response is False


def test_dialogue_plan_notes_are_preserved_without_final_reply_generation() -> None:
    state = _state()

    assert state.tone_guidance == "steady_warm"
    assert state.relationship_pacing_notes == ["maintain_gradual_pacing"]
    assert "use_evidence_backed_memory_only" in state.memory_use_notes
    assert state.has_generated_response is False


def test_chat_memory_payload_has_no_raw_private_or_delivery_platform_fields() -> None:
    state = _state(memory_items=[_factual_memory(), _imagined_memory()])

    serialized = json.dumps(state.model_dump(mode="json"), ensure_ascii=False).lower()

    for forbidden in (
        "raw_text",
        "raw_transcript",
        "chat_history",
        "private_messages",
        "draft_reply",
        "reply_text",
        "send",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "token",
        "queue",
    ):
        assert forbidden not in serialized


def test_chat_memory_prototype_does_not_expose_runtime_or_outbound_methods() -> None:
    prototype = TextFirstChatMemoryPrototype()

    for method_name in (
        "chat",
        "send",
        "schedule",
        "deliver",
        "execute",
        "run_runtime",
        "generate_reply",
        "create_message",
    ):
        assert not hasattr(prototype, method_name)
