"""T378 memory lifecycle dry-run apply tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, apply decisions, mutate stores, delete records, send messages, or connect
to external platforms/media.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import MemoryEvent, MemoryProvenance
from practical_chat_agent.services.memory_event_store import MemoryEventStore
from practical_chat_agent.services.memory_governance import (
    MemoryContradictionCandidate,
    MemoryDeletionCascadePlan,
    MemorySupersessionCandidate,
)
from practical_chat_agent.services.review_queue import ReviewQueueService


def _dry_run() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.memory_lifecycle_dry_run")
    except ModuleNotFoundError as exc:
        pytest.fail(f"memory_lifecycle_dry_run module is missing: {exc}")


def _service() -> Any:
    return _dry_run().MemoryLifecycleDryRunService()


def _store(tmp_path: Path) -> MemoryEventStore:
    return MemoryEventStore(tmp_path / "memory_events.json")


def _factual(**overrides: object) -> MemoryEvent:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "event_type": "factual",
        "truth_status": "evidence_backed",
        "summary": "[SYNTHETIC] User prefers concise replies.",
        "provenance": MemoryProvenance(
            source_type="synthetic_test",
            evidence_refs=["synthetic_event_lifecycle_001"],
        ),
        "sensitivity": "low",
    }
    data.update(overrides)
    return MemoryEvent(**data)


class TestMemoryLifecycleDryRunPlans:
    def test_deletion_cascade_plan_lists_effects_without_mutating_store(self, tmp_path: Path) -> None:
        store = _store(tmp_path)
        event = store.append(_factual()).event
        deletion = MemoryDeletionCascadePlan.for_consent_withdrawal(
            user_id=event.user_id,
            target_memory_ids=[event.event_id],
            affected_artifact_refs=["retrieval_bundle:synthetic"],
        )
        item = ReviewQueueService().item_from_candidate(deletion)
        decision = ReviewQueueService().record_decision(
            item,
            reviewer_id="reviewer_synthetic",
            decision="approve",
            decision_notes=["[SYNTHETIC] Preview only."],
        )

        plan = _service().plan_from_candidate(deletion, decision_record=decision)

        assert plan.source_candidate_id == deletion.plan_id
        assert plan.review_decision_id == decision.decision_id
        assert plan.applies_changes is False
        assert plan.writes_memory_store is False
        assert [effect.action for effect in plan.effects] == [
            "suppress_retrieval",
            "training_exclusion",
        ]
        assert all(effect.preview_only for effect in plan.effects)
        assert all(effect.retrieval_enabled_after is False for effect in plan.effects)
        assert store.get(event.event_id).lifecycle_state == "active"

    def test_supersession_plan_previews_transition_without_changing_lifecycle(
        self,
        tmp_path: Path,
    ) -> None:
        store = _store(tmp_path)
        source = store.append(_factual(summary="[SYNTHETIC] User prefers short replies.")).event
        replacement = store.append(
            _factual(summary="[SYNTHETIC] User now prefers detailed replies.")
        ).event
        candidate = MemorySupersessionCandidate.from_memory_ids(
            source_memory_id=source.event_id,
            replacement_memory_id=replacement.event_id,
            reason="[SYNTHETIC] Newer preference should be reviewed.",
        )

        plan = _service().plan_from_candidate(candidate)

        assert plan.source_candidate_kind == "memory_supersession"
        assert plan.affected_memory_ids == [source.event_id, replacement.event_id]
        assert plan.effects[0].action == "supersede"
        assert plan.effects[0].memory_id == source.event_id
        assert plan.effects[0].replacement_memory_id == replacement.event_id
        assert store.get(source.event_id).lifecycle_state == "active"

    def test_contradiction_plan_previews_clarification_without_overwriting_memory(
        self,
        tmp_path: Path,
    ) -> None:
        store = _store(tmp_path)
        old_event = store.append(_factual(summary="[SYNTHETIC] User prefers short replies.")).event
        new_event = store.append(
            _factual(summary="[SYNTHETIC] User now prefers detailed replies.")
        ).event
        candidate = MemoryContradictionCandidate.from_events(
            [old_event, new_event],
            conflict_type="preference_change",
            safe_summary="[SYNTHETIC] Reply length preference changed.",
            proposed_resolution="request_clarification",
        )

        plan = _service().plan_from_candidate(candidate)

        assert plan.source_candidate_kind == "memory_contradiction"
        assert [effect.action for effect in plan.effects] == [
            "request_clarification",
            "request_clarification",
        ]
        assert store.get(old_event.event_id).summary == old_event.summary
        assert store.get(new_event.event_id).summary == new_event.summary

    def test_review_required_memory_is_not_made_retrieval_eligible(self) -> None:
        event = _factual(sensitivity="high")
        deletion = MemoryDeletionCascadePlan.for_consent_withdrawal(
            user_id=event.user_id,
            target_memory_ids=[event.event_id],
        )

        plan = _service().plan_from_candidate(deletion)

        assert event.retrieval_permission.review_required is True
        assert all(effect.retrieval_enabled_after is False for effect in plan.effects)
        assert "retrieval_not_enabled_by_dry_run" in plan.blocked_reasons


class TestMemoryLifecycleDryRunSafetyBoundaries:
    def test_models_forbid_extra_private_provider_outbound_and_media_fields(self) -> None:
        module = _dry_run()

        with pytest.raises(ValidationError):
            module.MemoryLifecycleDryRunEffect(
                action="delete",
                memory_id="mev_synthetic",
                safe_summary="[SYNTHETIC] Preview delete.",
                provider_credentials="secret",
            )

        plan = _service().plan_from_candidate(
            MemoryDeletionCascadePlan.for_consent_withdrawal(
                user_id="user_synthetic",
                target_memory_ids=["mev_synthetic"],
            )
        )
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
            "mutate_store",
            "apply_decision",
            "delete_memory",
            "update_lifecycle",
            "write_persona_version",
            "generate_reply",
            "generate_voice",
            "generate_avatar",
            "generate_audio",
            "generate_image",
            "generate_video",
        ):
            assert not hasattr(service, method_name)
