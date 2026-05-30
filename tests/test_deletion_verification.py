"""T304 deletion verification tests.

All records are synthetic. These tests verify local tombstone, dry-run,
confirmation, audit, and manifest boundaries only; they do not remove source
files, write exports, call an LLM, or enable outbound/platform behavior.
"""

from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.core.models import (
    ControlAuditEvent,
    ControlExportManifest,
    ControlOperationConfirmation,
    ControlOperationPreview,
    ControlOperationTarget,
)
from practical_chat_agent.services.persona_compiler import PersonaCompilerService
from practical_chat_agent.services.persona_version_store import PersonaVersionStore


def _store(tmp_path: Path) -> PersonaVersionStore:
    return PersonaVersionStore(tmp_path / "persona_versions.json")


def _card():
    return PersonaCompilerService().compile(
        {
            "user_id": "user_synthetic",
            "display_name": "Lin Qi",
            "creation_mode": "detailed_prompt",
            "description": "fictional calm concise companion with dry humor",
        }
    )


def _target(**overrides: object) -> ControlOperationTarget:
    data: dict[str, object] = {
        "artifact_type": "persona_card",
        "artifact_id": "persona_synthetic",
        "user_id": "user_synthetic",
        "persona_id": "persona_synthetic",
        "current_state": "active",
        "review_required": False,
        "retrieval_eligible": True,
        "runtime_eligible": True,
        "provenance_refs": ["synthetic_persona_version_001"],
        "safety_labels": [],
    }
    data.update(overrides)
    return ControlOperationTarget(**data)


def test_persona_delete_appends_tombstone_and_preserves_prior_versions(tmp_path: Path) -> None:
    store = _store(tmp_path)
    saved = store.save(_card())

    deleted = store.delete(saved.persona_id, reason="synthetic user deletion request")

    versions = store.list_versions(saved.persona_id)
    assert [record.version_id for record in versions] == [saved.version_id, deleted.version_id]
    assert versions[0].deleted is False
    assert versions[1].deleted is True
    assert versions[1].operation == "delete"
    assert versions[1].card.status == "archived"
    assert store.latest_record(saved.persona_id).version_id == saved.version_id
    assert store.latest_record(saved.persona_id, include_deleted=True).version_id == deleted.version_id
    assert store.path.is_file()


def test_persona_delete_export_payload_omits_raw_private_and_delivery_fields(tmp_path: Path) -> None:
    store = _store(tmp_path)
    saved = store.save(_card())
    store.delete(saved.persona_id, reason="synthetic user deletion request")

    serialized = json.dumps(store.export_persona(saved.persona_id), ensure_ascii=False).lower()

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


def test_dry_run_delete_confirmation_and_audit_do_not_execute() -> None:
    preview = ControlOperationPreview.for_target(
        operation="soft_delete",
        target=_target(),
        reason="Synthetic delete verification preview.",
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
        before_summary="Persona was active.",
        after_summary="Persona would be deleted.",
        confirmation=confirmation,
        safety_flags=["deletion_verification"],
    )

    assert preview.dry_run is True
    assert preview.retrieval_eligible_after is False
    assert preview.runtime_eligible_after is False
    assert confirmation.executes_operation is False
    assert confirmation.writes_records is False
    assert audit.executes_operation is False
    assert audit.writes_records is False
    assert audit.confirmation_status == "confirmed"


def test_hard_delete_is_high_impact_preview_only() -> None:
    preview = ControlOperationPreview.for_target(
        operation="hard_delete",
        target=_target(),
        reason="Synthetic hard-delete verification preview.",
    )

    assert preview.hard_delete is True
    assert preview.dry_run is True
    assert preview.requires_confirmation is True
    assert preview.source_files_untouched is True
    assert preview.writes_records is False
    assert preview.writes_export_files is False
    assert "hard_delete_preview_only" in preview.safety_flags
    assert "high_impact_control" in preview.safety_flags


def test_delete_manifest_payload_is_redacted_and_manifest_only() -> None:
    target = _target(
        review_required=True,
        safety_labels=["review_required"],
        provenance_refs=["synthetic_persona_version_001"],
    )
    preview = ControlOperationPreview.for_target(
        operation="export",
        target=target,
        reason="Synthetic deletion verification manifest.",
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
        targets=[target],
        reason="Synthetic manifest-only deletion verification.",
    )

    assert manifest.writes_export_files is False
    assert manifest.source_files_untouched is True
    assert manifest.contains_review_required_items is True

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
