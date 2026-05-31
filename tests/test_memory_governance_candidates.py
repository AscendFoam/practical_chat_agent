"""T371 memory governance candidate tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, rank retrieval, mutate runtime memory state, generate dialogue, schedule
messages, or connect to external platforms.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import MemoryEvent, MemoryProvenance
from practical_chat_agent.services.memory_event_store import MemoryEventStore


def _governance() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.memory_governance")
    except ModuleNotFoundError as exc:
        pytest.fail(f"memory_governance module is missing: {exc}")


def _provenance(**overrides: object) -> MemoryProvenance:
    data: dict[str, object] = {
        "source_type": "synthetic_test",
        "evidence_refs": ["synthetic_event_001"],
        "source_summary": "[SYNTHETIC] User preference note.",
    }
    data.update(overrides)
    return MemoryProvenance(**data)


def _factual(**overrides: object) -> MemoryEvent:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "event_type": "factual",
        "truth_status": "evidence_backed",
        "summary": "[SYNTHETIC] User said they prefer concise evening check-ins.",
        "provenance": _provenance(),
        "sensitivity": "low",
    }
    data.update(overrides)
    return MemoryEvent(**data)


def _imagined() -> MemoryEvent:
    return MemoryEvent(
        user_id="user_synthetic",
        event_type="imagined",
        truth_status="imagined",
        summary="[SYNTHETIC] Fictional persona dreamed about a quiet bookstore.",
        provenance=MemoryProvenance(source_type="imagined_generation"),
        sensitivity="low",
        imagined_context_label="dream_log",
    )


class TestMemoryContradictionCandidate:
    def test_contradiction_candidate_is_review_required_and_preserves_memory_ids(self) -> None:
        module = _governance()
        old_event = _factual(summary="[SYNTHETIC] User prefers short replies.")
        new_event = _factual(summary="[SYNTHETIC] User now prefers detailed replies.")

        candidate = module.MemoryContradictionCandidate.from_events(
            [old_event, new_event],
            new_evidence_refs=["synthetic_event_002"],
            conflict_type="preference_change",
            safe_summary="[SYNTHETIC] Reply-length preference changed.",
            proposed_resolution="request_clarification",
            safety_warnings=["needs_user_confirmation"],
        )

        assert candidate.schema_version == "memory_contradiction_candidate_v1"
        assert candidate.candidate_id.startswith("memctr_")
        assert candidate.user_id == "user_synthetic"
        assert candidate.memory_ids == [old_event.event_id, new_event.event_id]
        assert candidate.review_required is True
        assert candidate.proposed_resolution == "request_clarification"
        assert "needs_user_confirmation" in candidate.safety_warnings

    def test_contradiction_candidate_rejects_single_memory_conflict(self) -> None:
        module = _governance()

        with pytest.raises(ValidationError):
            module.MemoryContradictionCandidate(
                user_id="user_synthetic",
                memory_ids=["mev_one"],
                new_evidence_refs=["synthetic_event_002"],
                conflict_type="fact_conflict",
                safe_summary="[SYNTHETIC] Too little evidence.",
                proposed_resolution="keep_both",
            )


class TestMemorySupersessionCandidate:
    def test_supersession_candidate_does_not_update_memory_store(self, tmp_path: Any) -> None:
        module = _governance()
        source = _factual(summary="[SYNTHETIC] User prefers short replies.")
        replacement = _factual(summary="[SYNTHETIC] User prefers detailed replies.")
        store = MemoryEventStore(tmp_path / "memory_events.json")
        store.append(source)
        store.append(replacement)

        candidate = module.MemorySupersessionCandidate.from_memory_ids(
            source_memory_id=source.event_id,
            replacement_memory_id=replacement.event_id,
            reason="[SYNTHETIC] Newer explicit preference supersedes older preference.",
        )

        assert candidate.schema_version == "memory_supersession_candidate_v1"
        assert candidate.review_required is True
        assert candidate.applies_lifecycle_update is False
        assert store.get(source.event_id).lifecycle_state == "active"


class TestMemoryDeletionCascadePlan:
    def test_consent_withdrawal_plan_is_review_required_and_not_completed(self) -> None:
        module = _governance()

        plan = module.MemoryDeletionCascadePlan.for_consent_withdrawal(
            user_id="user_synthetic",
            target_memory_ids=["mev_alpha"],
            affected_artifact_refs=["retrieval_bundle:synthetic"],
        )

        assert plan.schema_version == "memory_deletion_cascade_plan_v1"
        assert plan.plan_id.startswith("memdel_")
        assert plan.trigger_type == "consent_withdrawal"
        assert plan.review_required is True
        assert plan.completed is False
        assert "suppress_retrieval" in plan.recommended_actions
        assert "training_exclusion" in plan.recommended_actions


class TestMemoryExplanationTrace:
    def test_explanation_trace_exposes_include_and_exclude_reasons(self) -> None:
        module = _governance()
        event = _factual()

        included = module.MemoryExplanationTrace.included_from_event(
            event,
            surface="viewer",
            reason="eligible active factual memory",
        )
        excluded = module.MemoryExplanationTrace.excluded_from_event(
            event,
            surface="retrieval_bundle",
            reason="review_required memory excluded from factual response",
            safety_warnings=["review_required"],
        )

        assert included.memory_id == event.event_id
        assert included.included is True
        assert included.truth_status == "evidence_backed"
        assert included.provenance_refs == ["synthetic_event_001"]
        assert included.reason == "eligible active factual memory"
        assert excluded.included is False
        assert excluded.reason == "review_required memory excluded from factual response"
        assert "review_required" in excluded.safety_warnings


class TestPersonaGrowthEvidenceBundle:
    def test_growth_evidence_uses_safe_summaries_and_blocks_imagined_factual_evidence(self) -> None:
        module = _governance()
        factual = _factual()
        imagined = _imagined()

        bundle = module.PersonaGrowthEvidenceBundle.from_events(
            persona_id="persona_synthetic",
            events=[factual, imagined],
            evidence_purpose="factual_persona_growth",
        )

        assert bundle.schema_version == "persona_growth_evidence_bundle_v1"
        assert bundle.review_required is True
        assert bundle.memory_ids == [factual.event_id]
        assert bundle.safe_summaries[factual.event_id].startswith("[SYNTHETIC]")
        assert bundle.blocked_memory_ids == [imagined.event_id]
        assert bundle.exclusion_reasons[imagined.event_id] == "imagined_memory_not_valid_for_factual_growth"

    def test_growth_evidence_blocks_dependency_or_clone_risk_warnings(self) -> None:
        module = _governance()
        event = _factual()

        bundle = module.PersonaGrowthEvidenceBundle.from_events(
            persona_id="persona_synthetic",
            events=[event],
            evidence_purpose="factual_persona_growth",
            safety_warnings_by_memory_id={
                event.event_id: ["dependency_language", "real_person_similarity"],
            },
        )

        assert bundle.memory_ids == []
        assert bundle.blocked_memory_ids == [event.event_id]
        assert bundle.exclusion_reasons[event.event_id] == "blocking_safety_warning"
        assert "dependency_language" in bundle.safety_warnings
        assert "real_person_similarity" in bundle.safety_warnings


class TestMemoryGovernanceForbiddenSurface:
    def test_models_forbid_extra_private_provider_outbound_and_media_fields(self) -> None:
        module = _governance()

        with pytest.raises(ValidationError):
            module.MemoryDeletionCascadePlan(
                user_id="user_synthetic",
                trigger_type="user_delete",
                target_memory_ids=["mev_alpha"],
                affected_artifact_refs=[],
                recommended_actions=["delete"],
                provider_credentials="secret",
            )

        forbidden_field_names = {
            "raw_private_text",
            "full_transcript",
            "provider_credentials",
            "platform_recipient_id",
            "send_queue",
            "schedule",
            "webhook",
            "token",
            "microphone_prompt",
            "camera_prompt",
            "audio_bytes",
            "image_bytes",
            "video_bytes",
        }
        for model in (
            module.MemoryContradictionCandidate,
            module.MemorySupersessionCandidate,
            module.MemoryDeletionCascadePlan,
            module.MemoryExplanationTrace,
            module.PersonaGrowthEvidenceBundle,
        ):
            assert forbidden_field_names.isdisjoint(model.model_fields)

    def test_candidate_objects_do_not_expose_runtime_or_delivery_methods(self) -> None:
        module = _governance()
        candidate = module.MemorySupersessionCandidate.from_memory_ids(
            source_memory_id="mev_old",
            replacement_memory_id="mev_new",
            reason="[SYNTHETIC] Newer memory should be reviewed as a replacement.",
        )

        for method_name in (
            "send",
            "schedule",
            "deliver",
            "call_provider",
            "open_webhook",
            "mutate_store",
            "apply_lifecycle_update",
            "run_runtime",
            "capture_microphone",
            "capture_camera",
            "generate_audio",
            "generate_image",
            "generate_video",
        ):
            assert not hasattr(candidate, method_name)
