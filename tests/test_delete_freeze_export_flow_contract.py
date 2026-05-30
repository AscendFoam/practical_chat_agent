"""T303 delete/freeze/export local flow contract tests.

All fixtures are synthetic. These tests define dry-run preview, confirmation,
audit, and export manifest objects only; they do not mutate records, delete
files, write exports, call an LLM, or enable outbound/platform behavior.
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from practical_chat_agent.core.models import (
    ControlAuditEvent,
    ControlExportManifest,
    ControlOperationConfirmation,
    ControlOperationPreview,
    ControlOperationTarget,
)


def _memory_target(**overrides: object) -> ControlOperationTarget:
    data: dict[str, object] = {
        "artifact_type": "memory_event",
        "artifact_id": "mem_synthetic_001",
        "user_id": "user_synthetic",
        "persona_id": "persona_synthetic",
        "current_state": "active",
        "review_required": False,
        "retrieval_eligible": True,
        "runtime_eligible": True,
        "provenance_refs": ["synthetic_event_001"],
        "safety_labels": [],
    }
    data.update(overrides)
    return ControlOperationTarget(**data)


def test_delete_and_freeze_previews_are_dry_run_and_mark_eligibility_changes() -> None:
    target = _memory_target()

    soft_delete = ControlOperationPreview.for_target(
        operation="soft_delete",
        target=target,
        reason="Synthetic local deletion preview.",
    )
    hard_delete = ControlOperationPreview.for_target(
        operation="hard_delete",
        target=target,
        reason="Synthetic local hard-deletion preview.",
    )
    freeze = ControlOperationPreview.for_target(
        operation="freeze",
        target=target,
        reason="Synthetic local freeze preview.",
    )

    assert soft_delete.schema_version == "control_operation_preview_v1"
    assert soft_delete.dry_run is True
    assert soft_delete.requires_confirmation is True
    assert soft_delete.operation == "soft_delete"
    assert soft_delete.hard_delete is False
    assert soft_delete.would_change_state_to == "deleted"
    assert soft_delete.retrieval_eligible_after is False
    assert soft_delete.runtime_eligible_after is False
    assert soft_delete.writes_records is False
    assert soft_delete.source_files_untouched is True

    assert hard_delete.hard_delete is True
    assert hard_delete.would_change_state_to == "deleted"
    assert freeze.operation == "freeze"
    assert freeze.would_change_state_to == "frozen"
    assert freeze.retrieval_eligible_after is False
    assert freeze.runtime_eligible_after is False


def test_confirmation_references_dry_run_preview_without_executing() -> None:
    preview = ControlOperationPreview.for_target(
        operation="freeze",
        target=_memory_target(),
        reason="Synthetic freeze preview.",
    )

    confirmation = ControlOperationConfirmation.from_preview(
        preview,
        actor_id="human_reviewer_1",
        confirmed=True,
        confirmation_phrase="CONFIRM",
        reason="Synthetic reviewer confirmed the preview.",
    )

    assert confirmation.schema_version == "control_operation_confirmation_v1"
    assert confirmation.preview_id == preview.preview_id
    assert confirmation.confirmation_status == "confirmed"
    assert confirmation.executes_operation is False
    assert confirmation.writes_records is False
    assert confirmation.writes_export_files is False

    with pytest.raises(ValidationError):
        ControlOperationConfirmation(
            preview_id="",
            operation="freeze",
            target=_memory_target(),
            actor_id="human_reviewer_1",
            confirmed=True,
            confirmation_phrase="CONFIRM",
            reason="Missing preview id should fail.",
        )


def test_audit_event_preserves_actor_target_reason_and_summaries() -> None:
    preview = ControlOperationPreview.for_target(
        operation="soft_delete",
        target=_memory_target(),
        reason="Synthetic delete preview.",
    )
    confirmation = ControlOperationConfirmation.from_preview(
        preview,
        actor_id="human_reviewer_1",
        confirmed=True,
        confirmation_phrase="CONFIRM",
        reason="Synthetic reviewer confirmed the preview.",
    )

    audit = ControlAuditEvent.from_preview(
        preview,
        actor_id="human_reviewer_1",
        before_summary="Memory was active and retrieval eligible.",
        after_summary="Memory would become deleted and not retrieval eligible.",
        confirmation=confirmation,
        safety_flags=["high_impact_control"],
    )

    assert audit.schema_version == "control_audit_event_v1"
    assert audit.actor_id == "human_reviewer_1"
    assert audit.user_id == "user_synthetic"
    assert audit.target.artifact_id == "mem_synthetic_001"
    assert audit.operation == "soft_delete"
    assert audit.confirmation_status == "confirmed"
    assert audit.before_summary == "Memory was active and retrieval eligible."
    assert audit.after_summary == "Memory would become deleted and not retrieval eligible."
    assert audit.reason == "Synthetic delete preview."
    assert "high_impact_control" in audit.safety_flags


def test_export_manifest_labels_imagined_aigc_review_and_provenance_metadata() -> None:
    target = _memory_target(
        artifact_id="mem_imagined_001",
        review_required=True,
        provenance_refs=["synthetic_imagined_event_001"],
        safety_labels=["imagined_content", "ai_generated", "review_required"],
    )

    manifest = ControlExportManifest.from_targets(
        user_id="user_synthetic",
        targets=[target],
        reason="Synthetic manifest-only export preview.",
    )

    assert manifest.schema_version == "control_export_manifest_v1"
    assert manifest.target_count == 1
    assert manifest.contains_imagined_content is True
    assert manifest.contains_aigc_content is True
    assert manifest.contains_review_required_items is True
    assert manifest.imagined_target_ids == ["mem_imagined_001"]
    assert manifest.aigc_target_ids == ["mem_imagined_001"]
    assert manifest.review_required_target_ids == ["mem_imagined_001"]
    assert manifest.provenance_refs == ["synthetic_imagined_event_001"]
    assert manifest.writes_export_files is False


def test_flow_payloads_have_no_raw_private_delivery_or_platform_fields() -> None:
    preview = ControlOperationPreview.for_target(
        operation="export",
        target=_memory_target(safety_labels=["review_required"], review_required=True),
        reason="Synthetic manifest preview.",
    )
    confirmation = ControlOperationConfirmation.from_preview(
        preview,
        actor_id="human_reviewer_1",
        confirmed=False,
        confirmation_phrase="",
        reason="Synthetic reviewer left preview unconfirmed.",
    )
    audit = ControlAuditEvent.from_preview(
        preview,
        actor_id="human_reviewer_1",
        before_summary="Target can be inspected.",
        after_summary="Target would be listed in a manifest.",
        confirmation=confirmation,
        safety_flags=["review_required"],
    )
    manifest = ControlExportManifest.from_targets(
        user_id="user_synthetic",
        targets=[preview.target],
        reason="Synthetic manifest-only preview.",
    )

    for model in (preview, confirmation, audit, manifest):
        for method_name in (
            "execute",
            "apply",
            "delete",
            "freeze",
            "unfreeze",
            "write_export",
            "send",
            "schedule",
        ):
            assert not hasattr(model, method_name)

    serialized = json.dumps(
        {
            "preview": preview.model_dump(mode="json"),
            "confirmation": confirmation.model_dump(mode="json"),
            "audit": audit.model_dump(mode="json"),
            "manifest": manifest.model_dump(mode="json"),
        },
        ensure_ascii=False,
    ).lower()
    for forbidden in (
        "raw_text",
        "raw_transcript",
        "chat_history",
        "private_messages",
        "send",
        "schedule",
        "delivery",
        "platform",
        "webhook",
        "token",
        "queue",
    ):
        assert forbidden not in serialized
