"""T377 review queue candidate tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, apply decisions, mutate stores, write persona versions, send messages, or
connect to external platforms/media.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import MemoryEvent, MemoryProvenance
from practical_chat_agent.services.memory_governance import (
    MemoryContradictionCandidate,
    MemoryDeletionCascadePlan,
    MemorySupersessionCandidate,
    PersonaGrowthEvidenceBundle,
)
from practical_chat_agent.services.memory_retrieval_explanation import (
    MemoryRetrievalExplanationService,
)
from practical_chat_agent.services.persona_compiler import PersonaCompilerService
from practical_chat_agent.services.persona_growth import (
    PersonaGrowthFieldChange,
    PersonaGrowthPatchCandidate,
)
from practical_chat_agent.services.synthetic_distillation_input import (
    CloneRiskDecision,
    DeidentifiedStyleFeatureCandidate,
    DistillationConsentRef,
    SyntheticDistillationInputManifest,
    SyntheticDistillationSourceSegment,
    SyntheticSpeakerAlias,
)


def _review_queue() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.review_queue")
    except ModuleNotFoundError as exc:
        pytest.fail(f"review_queue module is missing: {exc}")


def _service() -> Any:
    return _review_queue().ReviewQueueService()


def _factual(**overrides: object) -> MemoryEvent:
    data: dict[str, object] = {
        "user_id": "user_synthetic",
        "event_type": "factual",
        "truth_status": "evidence_backed",
        "summary": "[SYNTHETIC] User prefers concise replies.",
        "provenance": MemoryProvenance(
            source_type="synthetic_test",
            evidence_refs=["synthetic_event_review_queue_001"],
        ),
        "sensitivity": "low",
    }
    data.update(overrides)
    return MemoryEvent(**data)


def _persona() -> Any:
    return PersonaCompilerService().compile(
        {
            "user_id": "user_synthetic",
            "display_name": "Lin Qi",
            "creation_mode": "detailed_prompt",
            "description": "fictional calm concise companion with dry humor",
        }
    )


def _persona_growth_patch() -> PersonaGrowthPatchCandidate:
    persona = _persona()
    memory = _factual(summary="[SYNTHETIC] User asked for warmer replies.")
    evidence = PersonaGrowthEvidenceBundle.from_events(
        persona_id=persona.persona_id,
        events=[memory],
    )
    change = PersonaGrowthFieldChange(
        field_path="core_traits.warmth",
        old_value_summary="0.55",
        proposed_value_summary="0.59",
        numeric_delta=0.04,
        change_reason="[SYNTHETIC] User asked for warmer replies.",
        source_memory_ids=[memory.event_id],
    )
    return PersonaGrowthPatchCandidate.from_persona_card(
        persona,
        trigger_type="memory_pattern",
        trigger_summary="[SYNTHETIC] Warmer reply preference.",
        changes=[change],
        evidence_bundle=evidence,
        user_facing_explanation="[SYNTHETIC] Propose slightly warmer replies.",
    )


def _distillation_manifest() -> SyntheticDistillationInputManifest:
    consent = DistillationConsentRef(
        feature_scope="persona_distillation",
        policy_version="synthetic_policy_v1",
        actor_type="user",
        granted=True,
        evidence_ref="synthetic_consent_ref_001",
    )
    segment = SyntheticDistillationSourceSegment(
        speaker_alias="STYLE_SUBJECT_A",
        segment_kind="message",
        synthetic_text="[SYNTHETIC] concise warm reply with dry humor",
        source_ref="synthetic_segment_001",
        allowed_feature_families=["tone", "length", "humor"],
    )
    return SyntheticDistillationInputManifest(
        manifest_id="manifest_synthetic",
        user_id="user_synthetic",
        input_mode="synthetic_chat_segments",
        consent_refs=[consent],
        speaker_map=[
            SyntheticSpeakerAlias(
                speaker_alias="STYLE_SUBJECT_A",
                speaker_role="style_subject",
                is_target_style_subject=True,
            )
        ],
        segments=[segment],
        clone_risk_decision=CloneRiskDecision.from_flags(
            manifest_id="manifest_synthetic",
            risk_flags=[],
        ),
    )


class TestReviewQueueWrapping:
    def test_wraps_memory_governance_candidates_with_priority_and_refs(self) -> None:
        old_event = _factual(summary="[SYNTHETIC] User prefers short replies.")
        new_event = _factual(summary="[SYNTHETIC] User now prefers detailed replies.")
        contradiction = MemoryContradictionCandidate.from_events(
            [old_event, new_event],
            conflict_type="preference_change",
            safe_summary="[SYNTHETIC] Reply length preference changed.",
            proposed_resolution="request_clarification",
        )
        supersession = MemorySupersessionCandidate.from_memory_ids(
            source_memory_id=old_event.event_id,
            replacement_memory_id=new_event.event_id,
            reason="[SYNTHETIC] Newer preference should be reviewed.",
        )
        deletion = MemoryDeletionCascadePlan.for_consent_withdrawal(
            user_id="user_synthetic",
            target_memory_ids=[old_event.event_id],
            affected_artifact_refs=["retrieval_bundle:synthetic"],
        )

        contradiction_item = _service().item_from_candidate(contradiction)
        supersession_item = _service().item_from_candidate(supersession)
        deletion_item = _service().item_from_candidate(deletion)

        assert contradiction_item.candidate_kind == "memory_contradiction"
        assert contradiction_item.candidate_id == contradiction.candidate_id
        assert old_event.event_id in contradiction_item.source_refs
        assert "preference_change" in contradiction_item.reason_labels
        assert supersession_item.candidate_kind == "memory_supersession"
        assert supersession_item.review_required is True
        assert deletion_item.priority_band == "critical"
        assert deletion_item.priority_score > contradiction_item.priority_score

    def test_wraps_persona_growth_distillation_and_retrieval_candidates(self) -> None:
        patch = _persona_growth_patch()
        manifest = _distillation_manifest()
        feature = DeidentifiedStyleFeatureCandidate(
            manifest_id=manifest.manifest_id,
            feature_family="tone",
            feature_label="warm",
            value_summary="[SYNTHETIC] Warm concise style.",
            evidence_segment_ids=["sdseg_001"],
            source_speaker_aliases=["STYLE_SUBJECT_A"],
        )
        retrieval_result = MemoryRetrievalExplanationService().build_bundle(
            [_factual()],
            purpose="factual_response",
            query_summary="answer with factual memory",
        )

        service = _service()
        patch_item = service.item_from_candidate(patch)
        manifest_item = service.item_from_candidate(manifest)
        feature_item = service.item_from_candidate(feature)
        retrieval_item = service.item_from_candidate(retrieval_result)

        assert patch_item.candidate_kind == "persona_growth_patch"
        assert patch.patch_id == patch_item.candidate_id
        assert patch.persona_id == patch_item.persona_id
        assert "memory_pattern" in patch_item.reason_labels
        assert manifest_item.candidate_kind == "synthetic_distillation_manifest"
        assert manifest_item.owner_user_id == "user_synthetic"
        assert feature_item.candidate_kind == "deidentified_style_feature"
        assert feature_item.safe_summary == feature.value_summary
        assert retrieval_item.candidate_kind == "memory_retrieval_explanation"
        assert retrieval_result.bundle.bundle_id == retrieval_item.candidate_id


class TestReviewQueueSnapshotAndDecisions:
    def test_snapshot_sorts_high_risk_or_deletion_items_before_routine_items(self) -> None:
        deletion = MemoryDeletionCascadePlan.for_consent_withdrawal(
            user_id="user_synthetic",
            target_memory_ids=["mev_withdrawn"],
        )
        routine_feature = DeidentifiedStyleFeatureCandidate(
            manifest_id="manifest_synthetic",
            feature_family="tone",
            feature_label="warm",
            value_summary="[SYNTHETIC] Warm concise style.",
        )

        snapshot = _service().build_snapshot(
            [
                _service().item_from_candidate(routine_feature),
                _service().item_from_candidate(deletion),
            ]
        )

        assert snapshot.items[0].candidate_kind == "memory_deletion_cascade"
        assert snapshot.high_priority_item_ids == [snapshot.items[0].item_id]
        assert snapshot.counts_by_kind["memory_deletion_cascade"] == 1
        assert snapshot.counts_by_kind["deidentified_style_feature"] == 1

    def test_decision_record_does_not_apply_changes(self) -> None:
        item = _service().item_from_candidate(_persona_growth_patch())

        decision = _service().record_decision(
            item,
            reviewer_id="reviewer_synthetic",
            decision="approve",
            decision_notes=["[SYNTHETIC] Approved for later dry-run only."],
        )

        assert decision.item_id == item.item_id
        assert decision.candidate_id == item.candidate_id
        assert decision.applies_changes is False
        assert decision.writes_memory_store is False
        assert decision.writes_persona_version is False
        assert item.review_status == "queued"


class TestReviewQueueSafetyBoundaries:
    def test_models_forbid_extra_private_provider_outbound_and_media_fields(self) -> None:
        module = _review_queue()

        with pytest.raises(ValidationError):
            module.ReviewQueueItem(
                candidate_kind="memory_contradiction",
                candidate_id="memctr_synthetic",
                title="[SYNTHETIC] Review contradiction",
                safe_summary="[SYNTHETIC] Safe summary.",
                provider_credentials="secret",
            )

        item = _service().item_from_candidate(_persona_growth_patch())
        serialized = item.model_dump_json().lower()
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
