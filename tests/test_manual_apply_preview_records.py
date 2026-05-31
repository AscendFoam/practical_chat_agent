"""T397 manual apply preview record tests.

All records are synthetic and non-mutating. These tests do not read private
data, call providers, apply decisions, mutate stores, generate media, or enable
outbound behavior.
"""

from __future__ import annotations

import importlib

import pytest

from practical_chat_agent.services.review_decision_impact_preview import (
    ReviewDecisionImpactPreview,
    ReviewDecisionImpactPreviewService,
)
from practical_chat_agent.services.review_queue import ReviewQueueDecisionRecord
from practical_chat_agent.services.review_workspace import (
    ReviewWorkspaceArtifactBinding,
    ReviewWorkspaceBindingIssue,
    ReviewWorkspaceBundle,
    ReviewWorkspaceCandidateBinding,
)


def _module():
    return importlib.import_module("practical_chat_agent.services.manual_apply_preview")


def _impact(*, blocked: bool = False) -> ReviewDecisionImpactPreview:
    issues = []
    if blocked:
        issues.append(
            ReviewWorkspaceBindingIssue(
                issue_code="candidate_id_mismatch",
                severity="blocker",
                safe_summary="[SYNTHETIC] Candidate id mismatch.",
            )
        )
    binding = ReviewWorkspaceCandidateBinding(
        binding_id="rwbind_manual_preview",
        queue_item_id="rqitem_manual_preview",
        candidate_kind="persona_growth_patch",
        queue_candidate_id="pgpatch_manual_preview",
        source_candidate_id="pgpatch_manual_preview",
        source_schema_version="synthetic_candidate_v1",
        owner_user_id="user_synthetic",
        persona_id="persona_synthetic",
        safe_summary="[SYNTHETIC] Review persona growth patch before manual apply.",
        reason_labels=["memory_pattern"],
        source_refs=["synthetic_persona_ref"],
        priority_score=60,
        priority_band="normal",
        issues=issues,
    )
    artifact = ReviewWorkspaceArtifactBinding(
        binding_id="rwart_manual_preview",
        artifact_kind="persona_growth_dry_run_plan",
        artifact_id="pgdplan_manual_preview",
        source_candidate_kind=binding.candidate_kind,
        source_candidate_id=binding.source_candidate_id,
        candidate_binding_id=binding.binding_id,
        queue_item_id=binding.queue_item_id,
        review_decision_ids=["rqdec_manual_preview"],
        safe_summary="[SYNTHETIC] Preview persona growth dry-run effect.",
        source_refs=["synthetic_persona_artifact_ref"],
    )
    bundle = ReviewWorkspaceBundle(
        bundle_id="rwbundle_manual_preview",
        candidate_bindings=[binding],
        artifact_bindings=[artifact],
    )
    decision = ReviewQueueDecisionRecord(
        decision_id="rqdec_manual_preview",
        item_id=binding.queue_item_id,
        candidate_kind=binding.candidate_kind,
        candidate_id=binding.queue_candidate_id,
        reviewer_id="reviewer_synthetic",
        decision="approve",
    )
    return ReviewDecisionImpactPreviewService().preview_decision(bundle, decision)


def _ready_record():
    module = _module()
    return module.ManualApplyPreviewRecord.from_impact_preview(
        _impact(),
        required_gates=[
            module.ManualApplyPreviewGate(
                gate_code="human_approval",
                label="Human approval",
                safe_summary="[SYNTHETIC] Human approval is present.",
                satisfied=True,
            ),
            module.ManualApplyPreviewGate(
                gate_code="dry_run_artifact_present",
                label="Dry-run artifact present",
                safe_summary="[SYNTHETIC] Dry-run artifact is present.",
                satisfied=True,
            ),
        ],
        effects=[
            module.ManualApplyPreviewEffect(
                effect_kind="persona_version_preview",
                target_ref="persona_synthetic",
                safe_summary="[SYNTHETIC] Persona warmth would be adjusted.",
                artifact_ids=["pgdplan_manual_preview"],
                rollback_notes=["[SYNTHETIC] Keep previous persona version available."],
            )
        ],
        rollback_notes=["[SYNTHETIC] Revert by keeping previous persona version."],
    )


def test_manual_apply_preview_record_is_serializable_and_non_mutating() -> None:
    record = _ready_record()
    payload = record.model_dump(mode="json")

    assert payload["schema_version"] == "manual_apply_preview_record_v1"
    assert payload["candidate_kind"] == "persona_growth_patch"
    assert payload["decision_id"] == "rqdec_manual_preview"
    assert payload["preview_outcome"] == "future_manual_apply_eligible"
    assert payload["manual_apply_preview_eligible"] is True
    assert payload["review_required"] is True
    assert payload["preview_only"] is True
    assert payload["applies_changes"] is False
    assert payload["writes_memory_store"] is False
    assert payload["writes_persona_version"] is False
    assert payload["runtime_ready"] is False
    assert payload["effect_count"] == 1


def test_unsatisfied_gate_blocks_manual_apply_preview() -> None:
    module = _module()
    record = module.ManualApplyPreviewRecord.from_impact_preview(
        _impact(),
        required_gates=[
            module.ManualApplyPreviewGate(
                gate_code="active_consent_scope",
                label="Active consent scope",
                safe_summary="[SYNTHETIC] Consent scope is missing.",
                satisfied=False,
                blocking_issue_codes=["manual_apply_gate_unsatisfied"],
            )
        ],
        effects=[],
        rollback_notes=["[SYNTHETIC] No rollback path until consent is active."],
    )

    assert record.manual_apply_preview_eligible is False
    assert "manual_apply_gate_unsatisfied" in record.blocking_issue_codes
    assert record.applies_changes is False


def test_blocked_impact_preview_is_ineligible() -> None:
    module = _module()
    record = module.ManualApplyPreviewRecord.from_impact_preview(
        _impact(blocked=True),
        required_gates=[],
        effects=[],
        rollback_notes=["[SYNTHETIC] Resolve blockers before reconsidering."],
    )

    assert record.preview_outcome == "blocked_before_apply"
    assert record.manual_apply_preview_eligible is False
    assert "candidate_id_mismatch" in record.blocking_issue_codes


def test_serialized_manual_apply_preview_contains_no_forbidden_fields() -> None:
    serialized = _ready_record().model_dump_json().lower()

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
        "queue_item_id",
        "apply_decision",
        "mutate_store",
        "write_persona_version",
        "generate_audio",
        "generate_image",
        "generate_video",
    ):
        assert forbidden not in serialized


def test_manual_apply_preview_records_expose_no_runtime_or_apply_methods() -> None:
    module = _module()

    for target in (
        module.ManualApplyPreviewGate,
        module.ManualApplyPreviewEffect,
        module.ManualApplyPreviewRecord,
    ):
        for method_name in (
            "apply",
            "apply_decision",
            "mutate_store",
            "mutate_persona",
            "write_persona_version",
            "delete_memory",
            "call_provider",
            "generate_reply",
            "send",
            "schedule",
            "deliver",
            "generate_audio",
            "generate_image",
            "generate_video",
        ):
            assert not hasattr(target, method_name)


def test_manual_apply_preview_rejects_mutating_flags() -> None:
    module = _module()

    with pytest.raises(ValueError):
        module.ManualApplyPreviewRecord.from_impact_preview(
            _impact(),
            required_gates=[],
            effects=[],
            rollback_notes=["[SYNTHETIC] No mutation allowed."],
            applies_changes=True,
        )
