"""T385 review decision impact preview tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, apply decisions, mutate stores, write persona versions, synthesize
personas, send messages, or connect to external platforms.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

from practical_chat_agent.services.review_queue import ReviewQueueDecisionRecord
from practical_chat_agent.services.review_workspace import (
    ReviewWorkspaceArtifactBinding,
    ReviewWorkspaceBindingIssue,
    ReviewWorkspaceBundle,
    ReviewWorkspaceCandidateBinding,
)


def _preview_module() -> Any:
    try:
        return importlib.import_module(
            "practical_chat_agent.services.review_decision_impact_preview"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(f"review_decision_impact_preview module is missing: {exc}")


def _service() -> Any:
    return _preview_module().ReviewDecisionImpactPreviewService()


def _candidate_binding(
    *,
    queue_item_id: str = "rqitem_memory_synthetic",
    candidate_kind: str = "memory_deletion_cascade",
    candidate_id: str = "memdel_synthetic",
    issue: ReviewWorkspaceBindingIssue | None = None,
) -> ReviewWorkspaceCandidateBinding:
    return ReviewWorkspaceCandidateBinding(
        binding_id="rwbind_memory_synthetic",
        queue_item_id=queue_item_id,
        candidate_kind=candidate_kind,
        queue_candidate_id=candidate_id,
        source_candidate_id=candidate_id,
        source_schema_version="synthetic_candidate_v1",
        owner_user_id="user_synthetic",
        safe_summary="[SYNTHETIC] Review deletion cascade.",
        reason_labels=["consent_withdrawal"],
        source_refs=["synthetic_memory_ref"],
        priority_score=90,
        priority_band="critical",
        issues=[issue] if issue else [],
    )


def _artifact_binding(
    candidate_binding: ReviewWorkspaceCandidateBinding,
    *,
    artifact_kind: str = "memory_lifecycle_dry_run_plan",
    artifact_id: str = "mldplan_synthetic",
    issue: ReviewWorkspaceBindingIssue | None = None,
) -> ReviewWorkspaceArtifactBinding:
    return ReviewWorkspaceArtifactBinding(
        binding_id=f"rwart_{artifact_id}",
        artifact_kind=artifact_kind,
        artifact_id=artifact_id,
        source_candidate_kind=candidate_binding.candidate_kind,
        source_candidate_id=candidate_binding.source_candidate_id,
        candidate_binding_id=candidate_binding.binding_id,
        queue_item_id=candidate_binding.queue_item_id,
        review_decision_ids=["rqdec_synthetic"],
        safe_summary="[SYNTHETIC] Preview artifact impact.",
        source_refs=["synthetic_artifact_ref"],
        issues=[issue] if issue else [],
    )


def _bundle(
    *,
    candidate_binding: ReviewWorkspaceCandidateBinding | None = None,
    artifact_bindings: list[ReviewWorkspaceArtifactBinding] | None = None,
) -> ReviewWorkspaceBundle:
    binding = candidate_binding or _candidate_binding()
    return ReviewWorkspaceBundle(
        bundle_id="rwbundle_synthetic",
        candidate_bindings=[binding],
        artifact_bindings=list(artifact_bindings or []),
    )


def _decision(
    *,
    item_id: str = "rqitem_memory_synthetic",
    candidate_kind: str = "memory_deletion_cascade",
    candidate_id: str = "memdel_synthetic",
    decision: str = "approve",
) -> ReviewQueueDecisionRecord:
    return ReviewQueueDecisionRecord(
        decision_id="rqdec_synthetic",
        item_id=item_id,
        candidate_kind=candidate_kind,
        candidate_id=candidate_id,
        reviewer_id="reviewer_synthetic",
        decision=decision,
        decision_notes=["[SYNTHETIC] Reviewer decision note."],
    )


class TestReviewDecisionImpactPreview:
    def test_approve_ready_bundle_is_future_manual_apply_eligible_without_applying(self) -> None:
        candidate_binding = _candidate_binding()
        artifact = _artifact_binding(candidate_binding)
        preview = _service().preview_decision(
            _bundle(candidate_binding=candidate_binding, artifact_bindings=[artifact]),
            _decision(decision="approve"),
        )

        assert preview.bundle_id == "rwbundle_synthetic"
        assert preview.decision_id == "rqdec_synthetic"
        assert preview.candidate_binding_id == candidate_binding.binding_id
        assert preview.preview_outcome == "future_manual_apply_eligible"
        assert preview.future_manual_apply_eligible is True
        assert preview.blocking_issue_codes == []
        assert preview.review_required is True
        assert preview.preview_only is True
        assert preview.applies_changes is False
        assert preview.writes_memory_store is False
        assert preview.writes_persona_version is False
        assert preview.runtime_ready is False
        assert [impact.artifact_id for impact in preview.artifact_impacts] == [
            artifact.artifact_id
        ]
        assert preview.artifact_impacts[0].applies_changes is False
        assert preview.artifact_impacts[0].writes_memory_store is False
        assert preview.artifact_impacts[0].writes_persona_version is False

    @pytest.mark.parametrize(
        ("decision", "outcome"),
        [
            ("reject", "rejected_for_future_apply"),
            ("freeze", "frozen_for_later_reconsideration"),
            ("request_changes", "changes_requested_before_apply"),
        ],
    )
    def test_non_approve_decisions_map_to_non_applying_outcomes(
        self,
        decision: str,
        outcome: str,
    ) -> None:
        preview = _service().preview_decision(_bundle(), _decision(decision=decision))

        assert preview.preview_outcome == outcome
        assert preview.future_manual_apply_eligible is False
        assert preview.applies_changes is False
        assert preview.writes_memory_store is False
        assert preview.writes_persona_version is False

    def test_mismatched_decision_refs_block_preview(self) -> None:
        bundle = _bundle()

        missing_item = _service().preview_decision(
            bundle,
            _decision(item_id="rqitem_missing"),
        )
        kind_mismatch = _service().preview_decision(
            bundle,
            _decision(candidate_kind="persona_growth_patch"),
        )
        id_mismatch = _service().preview_decision(
            bundle,
            _decision(candidate_id="memdel_other"),
        )

        assert missing_item.preview_outcome == "blocked_before_apply"
        assert "decision_item_not_in_workspace" in missing_item.blocking_issue_codes
        assert "decision_candidate_kind_mismatch" in kind_mismatch.blocking_issue_codes
        assert "decision_candidate_id_mismatch" in id_mismatch.blocking_issue_codes

    def test_workspace_binding_blockers_are_carried_into_preview(self) -> None:
        issue = ReviewWorkspaceBindingIssue(
            issue_code="candidate_id_mismatch",
            severity="blocker",
            safe_summary="[SYNTHETIC] Candidate id mismatch.",
        )
        binding = _candidate_binding(issue=issue)

        preview = _service().preview_decision(_bundle(candidate_binding=binding), _decision())

        assert preview.preview_outcome == "blocked_before_apply"
        assert preview.future_manual_apply_eligible is False
        assert "candidate_id_mismatch" in preview.blocking_issue_codes

    def test_artifact_impacts_preserve_safe_refs_without_applying(self) -> None:
        candidate_binding = _candidate_binding(
            candidate_kind="persona_growth_patch",
            candidate_id="pgpatch_synthetic",
        )
        artifact = _artifact_binding(
            candidate_binding,
            artifact_kind="persona_growth_dry_run_plan",
            artifact_id="pgdplan_synthetic",
        )
        preview = _service().preview_decision(
            _bundle(candidate_binding=candidate_binding, artifact_bindings=[artifact]),
            _decision(
                candidate_kind="persona_growth_patch",
                candidate_id="pgpatch_synthetic",
            ),
        )

        impact = preview.artifact_impacts[0]
        assert impact.artifact_kind == "persona_growth_dry_run_plan"
        assert impact.artifact_id == "pgdplan_synthetic"
        assert impact.review_decision_ids == ["rqdec_synthetic"]
        assert impact.source_refs == ["synthetic_artifact_ref"]
        assert impact.preview_only is True
        assert impact.applies_changes is False
        assert impact.writes_persona_version is False

    def test_artifact_blockers_are_carried_into_preview(self) -> None:
        candidate_binding = _candidate_binding()
        artifact_issue = ReviewWorkspaceBindingIssue(
            issue_code="artifact_source_candidate_id_mismatch",
            severity="blocker",
            safe_summary="[SYNTHETIC] Artifact source mismatch.",
        )
        artifact = _artifact_binding(candidate_binding, issue=artifact_issue)

        preview = _service().preview_decision(
            _bundle(candidate_binding=candidate_binding, artifact_bindings=[artifact]),
            _decision(),
        )

        assert preview.preview_outcome == "blocked_before_apply"
        assert "artifact_source_candidate_id_mismatch" in preview.blocking_issue_codes
        assert preview.artifact_impacts[0].blocking_issue_codes == [
            "artifact_source_candidate_id_mismatch"
        ]

    def test_serialized_preview_contains_no_private_provider_outbound_or_media_fields(
        self,
    ) -> None:
        preview = _service().preview_decision(_bundle(), _decision())
        serialized = preview.model_dump_json().lower()

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


class TestReviewDecisionImpactPreviewSafetyBoundaries:
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
