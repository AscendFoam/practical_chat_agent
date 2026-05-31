"""T379 persona growth dry-run apply tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, mutate PersonaCard, write persona versions, apply decisions, send
messages, or connect to external platforms/media.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import MemoryEvent, MemoryProvenance
from practical_chat_agent.services.memory_governance import PersonaGrowthEvidenceBundle
from practical_chat_agent.services.persona_compiler import PersonaCompilerService
from practical_chat_agent.services.persona_growth import (
    PersonaGrowthFieldChange,
    PersonaGrowthPatchCandidate,
)
from practical_chat_agent.services.review_queue import ReviewQueueService


def _dry_run() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.persona_growth_dry_run")
    except ModuleNotFoundError as exc:
        pytest.fail(f"persona_growth_dry_run module is missing: {exc}")


def _service() -> Any:
    return _dry_run().PersonaGrowthDryRunService()


def _persona() -> Any:
    return PersonaCompilerService().compile(
        {
            "user_id": "user_synthetic",
            "display_name": "Lin Qi",
            "creation_mode": "detailed_prompt",
            "description": "fictional calm concise companion with dry humor",
        }
    )


def _memory() -> MemoryEvent:
    return MemoryEvent(
        user_id="user_synthetic",
        event_type="factual",
        truth_status="evidence_backed",
        summary="[SYNTHETIC] User asked for warmer replies.",
        provenance=MemoryProvenance(
            source_type="synthetic_test",
            evidence_refs=["synthetic_event_persona_growth_001"],
        ),
        sensitivity="low",
    )


def _change(**overrides: object) -> PersonaGrowthFieldChange:
    data: dict[str, object] = {
        "field_path": "core_traits.warmth",
        "old_value_summary": "0.55",
        "proposed_value_summary": "0.59",
        "numeric_delta": 0.04,
        "change_reason": "[SYNTHETIC] User asked for warmer replies.",
        "source_memory_ids": ["mev_synthetic"],
    }
    data.update(overrides)
    return PersonaGrowthFieldChange(**data)


def _patch(*, risky: bool = False, weekly_used: float = 0.0) -> tuple[Any, PersonaGrowthPatchCandidate]:
    persona = _persona()
    memory = _memory()
    evidence = PersonaGrowthEvidenceBundle.from_events(
        persona_id=persona.persona_id,
        events=[memory],
    )
    change = _change(
        source_memory_ids=[memory.event_id],
        risk_labels=["dependency_language"] if risky else [],
    )
    patch = PersonaGrowthPatchCandidate.from_persona_card(
        persona,
        trigger_type="memory_pattern",
        trigger_summary="[SYNTHETIC] Warmer reply preference.",
        changes=[change],
        evidence_bundle=evidence,
        user_facing_explanation="[SYNTHETIC] Propose slightly warmer replies.",
        weekly_trait_delta_by_field={"core_traits.warmth": weekly_used},
    )
    return persona, patch


class TestPersonaGrowthDryRunPlans:
    def test_plan_preserves_persona_state_and_lists_safe_field_preview(self) -> None:
        persona, patch = _patch(weekly_used=0.01)
        before = persona.model_dump(mode="json")
        item = ReviewQueueService().item_from_candidate(patch)
        decision = ReviewQueueService().record_decision(
            item,
            reviewer_id="reviewer_synthetic",
            decision="approve",
            decision_notes=["[SYNTHETIC] Preview only."],
        )

        plan = _service().plan_from_patch(
            patch,
            source_persona=persona,
            decision_record=decision,
        )

        assert persona.model_dump(mode="json") == before
        assert plan.patch_id == patch.patch_id
        assert plan.persona_id == persona.persona_id
        assert plan.source_persona_version == persona.version
        assert plan.review_decision_id == decision.decision_id
        assert plan.applies_changes is False
        assert plan.writes_persona_version is False
        assert plan.ready_for_later_manual_apply is True
        assert plan.weekly_trait_delta_after["core_traits.warmth"] == 0.05
        assert [preview.field_path for preview in plan.field_previews] == ["core_traits.warmth"]
        assert plan.field_previews[0].blocks_apply is False

    def test_blocking_labels_prevent_apply_readiness(self) -> None:
        persona, patch = _patch(risky=True)

        plan = _service().plan_from_patch(patch, source_persona=persona)

        assert plan.ready_for_later_manual_apply is False
        assert plan.blocking_risk_labels == ["dependency_language"]
        assert plan.blocked_field_paths == ["core_traits.warmth"]
        assert plan.field_previews[0].blocks_apply is True

    def test_review_decision_is_referenced_but_not_applied(self) -> None:
        persona, patch = _patch()
        item = ReviewQueueService().item_from_candidate(patch)
        decision = ReviewQueueService().record_decision(
            item,
            reviewer_id="reviewer_synthetic",
            decision="reject",
            decision_notes=["[SYNTHETIC] Reject for now."],
        )

        plan = _service().plan_from_patch(
            patch,
            source_persona=persona,
            decision_record=decision,
        )

        assert plan.review_decision == "reject"
        assert plan.ready_for_later_manual_apply is False
        assert "review_decision_not_applied_by_dry_run" in plan.blocked_reasons
        assert persona.version == patch.source_persona_version


class TestPersonaGrowthDryRunSafetyBoundaries:
    def test_models_forbid_extra_private_provider_outbound_and_media_fields(self) -> None:
        module = _dry_run()

        with pytest.raises(ValidationError):
            module.PersonaGrowthDryRunFieldPreview(
                field_path="core_traits.warmth",
                old_value_summary="0.55",
                proposed_value_summary="0.59",
                change_reason="[SYNTHETIC] Preview only.",
                provider_credentials="secret",
            )

        _, patch = _patch()
        plan = _service().plan_from_patch(patch)
        serialized = plan.model_dump_json().lower()
        for forbidden in (
            "raw_text",
            "raw_transcript",
            "chat_history",
            "private_messages",
            "provider_credentials",
            "platform_recipient",
            "send_queue",
            "schedule",
            "webhook",
            "token",
            "microphone",
            "camera",
            "audio_bytes",
            "image_bytes",
            "video_bytes",
        ):
            assert forbidden not in serialized

    def test_service_does_not_expose_runtime_or_delivery_methods(self) -> None:
        service = _service()

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "call_provider",
            "open_webhook",
            "mutate_persona",
            "apply_decision",
            "apply_persona_growth",
            "write_persona_version",
            "generate_reply",
            "generate_voice",
            "generate_avatar",
            "generate_audio",
            "generate_image",
            "generate_video",
        ):
            assert not hasattr(service, method_name)
