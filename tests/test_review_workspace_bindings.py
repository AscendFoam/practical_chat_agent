"""T383 review workspace binding tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, apply decisions, mutate stores, write persona versions, retain source
text, synthesize personas, send messages, or connect to external platforms.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import MemoryEvent, MemoryProvenance
from practical_chat_agent.services.distillation_review_readiness import (
    DistillationReviewReadinessService,
)
from practical_chat_agent.services.memory_governance import MemoryDeletionCascadePlan
from practical_chat_agent.services.memory_lifecycle_dry_run import (
    MemoryLifecycleDryRunService,
)
from practical_chat_agent.services.persona_compiler import PersonaCompilerService
from practical_chat_agent.services.persona_growth import (
    PersonaGrowthFieldChange,
    PersonaGrowthPatchCandidate,
)
from practical_chat_agent.services.persona_growth_dry_run import (
    PersonaGrowthDryRunService,
)
from practical_chat_agent.services.review_queue import ReviewQueueService
from practical_chat_agent.services.synthetic_distillation_input import (
    CloneRiskDecision,
    DeidentifiedStyleFeatureCandidate,
    DistillationConsentRef,
    SyntheticDistillationInputManifest,
    SyntheticDistillationSourceSegment,
    SyntheticSpeakerAlias,
)


def _workspace() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.review_workspace")
    except ModuleNotFoundError as exc:
        pytest.fail(f"review_workspace module is missing: {exc}")


def _service() -> Any:
    return _workspace().ReviewWorkspaceService()


def _queue_service() -> ReviewQueueService:
    return ReviewQueueService()


def _memory() -> MemoryEvent:
    return MemoryEvent(
        user_id="user_synthetic",
        event_type="factual",
        truth_status="evidence_backed",
        summary="[SYNTHETIC] User asked for warmer replies.",
        provenance=MemoryProvenance(
            source_type="synthetic_test",
            evidence_refs=["synthetic_event_workspace_001"],
        ),
        sensitivity="low",
    )


def _deletion_plan(memory_id: str = "mev_synthetic") -> MemoryDeletionCascadePlan:
    return MemoryDeletionCascadePlan.for_consent_withdrawal(
        user_id="user_synthetic",
        target_memory_ids=[memory_id],
        affected_artifact_refs=["retrieval_bundle:synthetic"],
    )


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
    memory = _memory()
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
        user_facing_explanation="[SYNTHETIC] Propose slightly warmer replies.",
    )


def _manifest() -> SyntheticDistillationInputManifest:
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


def _feature(manifest_id: str = "manifest_synthetic") -> DeidentifiedStyleFeatureCandidate:
    return DeidentifiedStyleFeatureCandidate(
        manifest_id=manifest_id,
        feature_family="tone",
        feature_label="warm",
        value_summary="[SYNTHETIC] Warm concise style.",
        evidence_segment_ids=["sdseg_001"],
        source_speaker_aliases=["STYLE_SUBJECT_A"],
    )


class TestReviewWorkspaceCandidateBindings:
    def test_matching_queue_item_and_source_candidate_are_ready(self) -> None:
        candidate = _deletion_plan()
        item = _queue_service().item_from_candidate(candidate)

        binding = _service().bind_candidate(item, candidate)

        assert binding.queue_item_id == item.item_id
        assert binding.candidate_kind == "memory_deletion_cascade"
        assert binding.queue_candidate_id == candidate.plan_id
        assert binding.source_candidate_id == candidate.plan_id
        assert binding.binding_ready is True
        assert binding.blocking_issue_codes == []
        assert binding.review_required is True

    def test_candidate_kind_mismatch_blocks_workspace_readiness(self) -> None:
        item = _queue_service().item_from_candidate(_persona_growth_patch())

        binding = _service().bind_candidate(item, _deletion_plan())

        assert binding.binding_ready is False
        assert "candidate_kind_mismatch" in binding.blocking_issue_codes

    def test_candidate_id_mismatch_blocks_workspace_readiness(self) -> None:
        source_patch = _persona_growth_patch()
        different_patch = _persona_growth_patch()
        item = _queue_service().item_from_candidate(source_patch)

        binding = _service().bind_candidate(item, different_patch)

        assert binding.binding_ready is False
        assert "candidate_id_mismatch" in binding.blocking_issue_codes


class TestReviewWorkspaceArtifactBindings:
    def test_memory_lifecycle_plan_attaches_only_to_matching_candidate_id(self) -> None:
        candidate = _deletion_plan("mev_one")
        item = _queue_service().item_from_candidate(candidate)
        binding = _service().bind_candidate(item, candidate)
        plan = MemoryLifecycleDryRunService().plan_from_candidate(candidate)

        artifact = _service().bind_artifact(binding, plan)

        assert artifact.artifact_kind == "memory_lifecycle_dry_run_plan"
        assert artifact.source_candidate_id == candidate.plan_id
        assert artifact.artifact_ready is True
        assert artifact.blocking_issue_codes == []

        mismatched_plan = MemoryLifecycleDryRunService().plan_from_candidate(
            _deletion_plan("mev_two")
        )
        mismatched_artifact = _service().bind_artifact(binding, mismatched_plan)

        assert mismatched_artifact.artifact_ready is False
        assert "artifact_source_candidate_id_mismatch" in mismatched_artifact.blocking_issue_codes

    def test_persona_growth_plan_attaches_only_to_matching_patch_id(self) -> None:
        patch = _persona_growth_patch()
        item = _queue_service().item_from_candidate(patch)
        binding = _service().bind_candidate(item, patch)
        plan = PersonaGrowthDryRunService().plan_from_patch(patch)

        artifact = _service().bind_artifact(binding, plan)

        assert artifact.artifact_kind == "persona_growth_dry_run_plan"
        assert artifact.source_candidate_id == patch.patch_id
        assert artifact.artifact_ready is True

        mismatched_artifact = _service().bind_artifact(
            binding,
            PersonaGrowthDryRunService().plan_from_patch(_persona_growth_patch()),
        )

        assert mismatched_artifact.artifact_ready is False
        assert "artifact_source_candidate_id_mismatch" in mismatched_artifact.blocking_issue_codes

    def test_distillation_readiness_preserves_queue_refs_and_blocks_mismatches(self) -> None:
        manifest = _manifest()
        feature = _feature(manifest.manifest_id)
        manifest_item = _queue_service().item_from_candidate(manifest)
        feature_item = _queue_service().item_from_candidate(feature)
        binding = _service().bind_candidate(manifest_item, manifest)
        summary = DistillationReviewReadinessService().build_summary(
            manifest,
            features=[feature],
            review_items=[feature_item],
        )

        artifact = _service().bind_artifact(binding, summary)

        assert artifact.artifact_kind == "distillation_review_readiness_summary"
        assert artifact.source_candidate_id == manifest.manifest_id
        assert artifact.review_queue_item_ids == [feature_item.item_id]
        assert artifact.artifact_ready is False
        assert "review_queue_item_ref_mismatch" in artifact.blocking_issue_codes


class TestReviewWorkspaceBundleAndSafetyBoundaries:
    def test_bundle_is_not_ready_when_any_binding_blocks(self) -> None:
        item = _queue_service().item_from_candidate(_persona_growth_patch())
        blocked_binding = _service().bind_candidate(item, _deletion_plan())

        bundle = _service().build_bundle(candidate_bindings=[blocked_binding])

        assert bundle.workspace_ready is False
        assert "candidate_kind_mismatch" in bundle.blocking_issue_codes
        assert bundle.applies_changes is False
        assert bundle.writes_memory_store is False
        assert bundle.writes_persona_version is False

    def test_models_forbid_extra_private_provider_outbound_and_media_fields(self) -> None:
        module = _workspace()

        with pytest.raises(ValidationError):
            module.ReviewWorkspaceBindingIssue(
                issue_code="candidate_id_mismatch",
                severity="blocker",
                safe_summary="[SYNTHETIC] Candidate id mismatch.",
                provider_credentials="secret",
            )

        candidate = _deletion_plan()
        item = _queue_service().item_from_candidate(candidate)
        bundle = _service().build_bundle(
            candidate_bindings=[_service().bind_candidate(item, candidate)]
        )
        serialized = bundle.model_dump_json().lower()
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
            "mutate_persona",
            "apply_decision",
            "apply_persona_growth",
            "write_persona_version",
            "delete_memory",
            "update_lifecycle",
            "synthesize_persona",
            "generate_reply",
            "generate_voice",
            "generate_avatar",
            "generate_audio",
            "generate_image",
            "generate_video",
        ):
            assert not hasattr(service, method_name)
