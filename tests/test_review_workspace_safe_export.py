"""T386 review workspace safe export tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, apply decisions, mutate stores, write persona versions, synthesize
personas, send messages, or connect to external platforms.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

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


def _export_module() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.review_workspace_export")
    except ModuleNotFoundError as exc:
        pytest.fail(f"review_workspace_export module is missing: {exc}")


def _service() -> Any:
    return _export_module().ReviewWorkspaceSafeExportService()


def _candidate_binding(
    *,
    binding_id: str,
    queue_item_id: str,
    candidate_kind: str,
    candidate_id: str,
    issue: ReviewWorkspaceBindingIssue | None = None,
) -> ReviewWorkspaceCandidateBinding:
    return ReviewWorkspaceCandidateBinding(
        binding_id=binding_id,
        queue_item_id=queue_item_id,
        candidate_kind=candidate_kind,
        queue_candidate_id=candidate_id,
        source_candidate_id=candidate_id,
        source_schema_version="synthetic_candidate_v1",
        owner_user_id="user_synthetic",
        persona_id="persona_synthetic" if candidate_kind == "persona_growth_patch" else None,
        safe_summary=f"[SYNTHETIC] Export {candidate_kind}.",
        reason_labels=["synthetic_export_reason"],
        source_refs=[f"synthetic_ref_{candidate_id}"],
        priority_score=90 if candidate_kind == "memory_deletion_cascade" else 60,
        priority_band="critical" if candidate_kind == "memory_deletion_cascade" else "normal",
        issues=[issue] if issue else [],
    )


def _artifact_binding(
    binding: ReviewWorkspaceCandidateBinding,
    *,
    artifact_kind: str,
    artifact_id: str,
) -> ReviewWorkspaceArtifactBinding:
    return ReviewWorkspaceArtifactBinding(
        binding_id=f"rwart_{artifact_id}",
        artifact_kind=artifact_kind,
        artifact_id=artifact_id,
        source_candidate_kind=binding.candidate_kind,
        source_candidate_id=binding.source_candidate_id,
        candidate_binding_id=binding.binding_id,
        queue_item_id=binding.queue_item_id,
        review_decision_ids=[f"rqdec_{artifact_id}"],
        safe_summary=f"[SYNTHETIC] Export {artifact_kind}.",
        source_refs=[f"synthetic_artifact_ref_{artifact_id}"],
    )


def _bundle(
    *,
    bundle_id: str,
    binding: ReviewWorkspaceCandidateBinding,
    artifact: ReviewWorkspaceArtifactBinding,
) -> ReviewWorkspaceBundle:
    return ReviewWorkspaceBundle(
        bundle_id=bundle_id,
        candidate_bindings=[binding],
        artifact_bindings=[artifact],
    )


def _decision(
    binding: ReviewWorkspaceCandidateBinding,
    *,
    decision_id: str,
    decision: str = "approve",
) -> ReviewQueueDecisionRecord:
    return ReviewQueueDecisionRecord(
        decision_id=decision_id,
        item_id=binding.queue_item_id,
        candidate_kind=binding.candidate_kind,
        candidate_id=binding.queue_candidate_id,
        reviewer_id="reviewer_synthetic",
        decision=decision,
    )


def _impact(
    bundle: ReviewWorkspaceBundle,
    binding: ReviewWorkspaceCandidateBinding,
    *,
    decision_id: str,
    decision: str = "approve",
) -> ReviewDecisionImpactPreview:
    return ReviewDecisionImpactPreviewService().preview_decision(
        bundle,
        _decision(binding, decision_id=decision_id, decision=decision),
    )


def _synthetic_records() -> tuple[
    ReviewWorkspaceBundle,
    ReviewWorkspaceBundle,
    ReviewDecisionImpactPreview,
    ReviewDecisionImpactPreview,
]:
    blocker = ReviewWorkspaceBindingIssue(
        issue_code="candidate_id_mismatch",
        severity="blocker",
        safe_summary="[SYNTHETIC] Candidate id mismatch.",
    )
    memory_binding = _candidate_binding(
        binding_id="rwbind_memory",
        queue_item_id="rqitem_memory",
        candidate_kind="memory_deletion_cascade",
        candidate_id="memdel_synthetic",
        issue=blocker,
    )
    persona_binding = _candidate_binding(
        binding_id="rwbind_persona",
        queue_item_id="rqitem_persona",
        candidate_kind="persona_growth_patch",
        candidate_id="pgpatch_synthetic",
    )
    memory_bundle = _bundle(
        bundle_id="rwbundle_b_memory",
        binding=memory_binding,
        artifact=_artifact_binding(
            memory_binding,
            artifact_kind="memory_lifecycle_dry_run_plan",
            artifact_id="mldplan_synthetic",
        ),
    )
    persona_bundle = _bundle(
        bundle_id="rwbundle_a_persona",
        binding=persona_binding,
        artifact=_artifact_binding(
            persona_binding,
            artifact_kind="persona_growth_dry_run_plan",
            artifact_id="pgdplan_synthetic",
        ),
    )
    return (
        memory_bundle,
        persona_bundle,
        _impact(memory_bundle, memory_binding, decision_id="rqdec_memory"),
        _impact(persona_bundle, persona_binding, decision_id="rqdec_persona"),
    )


class TestReviewWorkspaceSafeExport:
    def test_manifest_includes_safe_workspace_and_impact_summaries(self) -> None:
        memory_bundle, _, memory_impact, _ = _synthetic_records()

        manifest = _service().build_manifest(
            [memory_bundle],
            impact_previews=[memory_impact],
        )

        workspace_item = manifest.workspace_items[0]
        impact_item = manifest.impact_items[0]

        assert workspace_item.bundle_id == "rwbundle_b_memory"
        assert workspace_item.candidate_kind == "memory_deletion_cascade"
        assert workspace_item.safe_summary == "[SYNTHETIC] Export memory_deletion_cascade."
        assert workspace_item.artifact_ids == ["mldplan_synthetic"]
        assert workspace_item.review_required is True
        assert workspace_item.preview_only is True
        assert workspace_item.applies_changes is False
        assert impact_item.decision_id == "rqdec_memory"
        assert impact_item.preview_outcome == "blocked_before_apply"
        assert impact_item.safe_summary == workspace_item.safe_summary
        assert impact_item.applies_changes is False
        assert manifest.applies_changes is False
        assert manifest.runtime_ready is False

    def test_counts_and_ordering_are_deterministic(self) -> None:
        memory_bundle, persona_bundle, memory_impact, persona_impact = _synthetic_records()

        manifest = _service().build_manifest(
            [memory_bundle, persona_bundle],
            impact_previews=[memory_impact, persona_impact],
        )

        assert [item.bundle_id for item in manifest.workspace_items] == [
            "rwbundle_a_persona",
            "rwbundle_b_memory",
        ]
        assert [item.decision_id for item in manifest.impact_items] == [
            "rqdec_persona",
            "rqdec_memory",
        ]
        assert manifest.counts_by_candidate_kind == {
            "memory_deletion_cascade": 1,
            "persona_growth_patch": 1,
        }
        assert manifest.counts_by_artifact_kind == {
            "memory_lifecycle_dry_run_plan": 1,
            "persona_growth_dry_run_plan": 1,
        }
        assert manifest.counts_by_decision_outcome == {
            "blocked_before_apply": 1,
            "future_manual_apply_eligible": 1,
        }
        assert manifest.counts_by_blocker_code == {"candidate_id_mismatch": 2}

    def test_write_manifest_rejects_path_traversal(self, tmp_path: Path) -> None:
        memory_bundle, _, memory_impact, _ = _synthetic_records()
        service = _service()
        manifest = service.build_manifest([memory_bundle], impact_previews=[memory_impact])

        path = service.write_manifest(
            manifest,
            tmp_path / "exports",
            file_name="manifest.json",
        )

        assert path.exists()

        with pytest.raises(ValueError):
            service.write_manifest(
                manifest,
                tmp_path / "exports",
                file_name="../escape.json",
            )

    def test_serialized_export_contains_no_private_provider_outbound_or_media_fields(self) -> None:
        memory_bundle, persona_bundle, memory_impact, persona_impact = _synthetic_records()
        manifest = _service().build_manifest(
            [memory_bundle, persona_bundle],
            impact_previews=[memory_impact, persona_impact],
        )
        serialized = manifest.model_dump_json().lower()

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


class TestReviewWorkspaceSafeExportSafetyBoundaries:
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
