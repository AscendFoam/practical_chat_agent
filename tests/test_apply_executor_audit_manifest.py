"""T409 apply executor audit manifest tests.

All examples are synthetic. The manifest only normalizes existing local apply
audit records. These tests do not read private chat history, call providers,
write stores, send messages, or connect to external platforms/media.
"""

from __future__ import annotations

import importlib
from datetime import datetime, timezone

import pytest

from practical_chat_agent.services.memory_lifecycle_apply_executor import (
    MemoryLifecycleApplyAudit,
)
from practical_chat_agent.services.persona_growth_apply_executor import (
    PersonaGrowthApplyAudit,
)


def _module():
    return importlib.import_module(
        "practical_chat_agent.services.apply_executor_audit_manifest"
    )


def _persona_audit(*, created_at: datetime | None = None) -> PersonaGrowthApplyAudit:
    return PersonaGrowthApplyAudit(
        apply_id="pgapply_synthetic",
        persona_id="persona_synthetic",
        patch_id="pgpatch_synthetic",
        plan_id="pgplan_synthetic",
        review_decision_id="rqdec_persona_apply",
        eligibility_id="mapelig_persona_apply",
        approval_id="aeapproval_persona_apply",
        reviewer_id="reviewer_synthetic",
        prior_version_id="pver_001",
        new_version_id="pver_002",
        rollback_target_version_id="pver_001",
        changed_field_paths=["identity.name", "style.tone"],
        safe_summary="[SYNTHETIC] Local persona growth apply completed.",
        created_at=created_at
        or datetime(2026, 5, 31, 1, 0, 0, tzinfo=timezone.utc),
    )


def _memory_audit(*, created_at: datetime | None = None) -> MemoryLifecycleApplyAudit:
    return MemoryLifecycleApplyAudit(
        apply_id="mlapply_synthetic",
        plan_id="mldplan_synthetic",
        source_candidate_kind="memory_supersession",
        source_candidate_id="memsup_synthetic",
        review_decision_id="rqdec_memory_apply",
        eligibility_id="mapelig_memory_apply",
        approval_id="aeapproval_memory_apply",
        reviewer_id="reviewer_synthetic",
        affected_memory_ids=["mev_old"],
        prior_lifecycle_states={"mev_old": "active"},
        new_lifecycle_states={"mev_old": "superseded"},
        rollback_record_ids={"mev_old": "memrec_prior"},
        applied_record_ids={"mev_old": "memrec_applied"},
        safe_summary="[SYNTHETIC] Local memory lifecycle apply completed.",
        created_at=created_at
        or datetime(2026, 5, 31, 1, 1, 0, tzinfo=timezone.utc),
    )


def test_manifest_normalizes_persona_and_memory_audits_with_rollback() -> None:
    module = _module()
    manifest = module.ApplyExecutorAuditManifestBuilder().build(
        [
            _memory_audit(created_at=datetime(2026, 5, 31, 1, 1, tzinfo=timezone.utc)),
            _persona_audit(created_at=datetime(2026, 5, 31, 1, 0, tzinfo=timezone.utc)),
        ]
    )

    assert manifest.schema_version == "apply_executor_audit_manifest_v1"
    assert manifest.entry_count == 2
    assert [entry.apply_type for entry in manifest.entries] == [
        "persona_growth",
        "memory_lifecycle",
    ]

    persona_entry = manifest.entries[0]
    assert persona_entry.apply_id == "pgapply_synthetic"
    assert persona_entry.source_artifact_id == "pgpatch_synthetic"
    assert persona_entry.rollback_refs["rollback_target_version_id"] == "pver_001"
    assert persona_entry.changed_field_paths == ["identity.name", "style.tone"]
    assert persona_entry.affected_memory_ids == []

    memory_entry = manifest.entries[1]
    assert memory_entry.apply_id == "mlapply_synthetic"
    assert memory_entry.source_artifact_id == "mldplan_synthetic"
    assert memory_entry.rollback_refs["mev_old"] == "memrec_prior"
    assert memory_entry.applied_refs["mev_old"] == "memrec_applied"
    assert memory_entry.affected_memory_ids == ["mev_old"]
    assert memory_entry.changed_field_paths == []


def test_manifest_rejects_unsupported_audit_schema() -> None:
    module = _module()

    with pytest.raises(module.ApplyExecutorAuditManifestError):
        module.ApplyExecutorAuditManifestBuilder().build([{"schema_version": "unknown"}])


def test_manifest_rejects_missing_rollback_evidence() -> None:
    module = _module()
    missing_persona_rollback = _persona_audit().model_copy(
        update={"rollback_target_version_id": ""}
    )
    missing_memory_rollback = _memory_audit().model_copy(update={"rollback_record_ids": {}})

    with pytest.raises(module.ApplyExecutorAuditManifestError):
        module.ApplyExecutorAuditManifestBuilder().build([missing_persona_rollback])

    with pytest.raises(module.ApplyExecutorAuditManifestError):
        module.ApplyExecutorAuditManifestBuilder().build([missing_memory_rollback])


def test_manifest_contains_no_private_provider_outbound_or_media_fields() -> None:
    module = _module()
    manifest = module.ApplyExecutorAuditManifestBuilder().build(
        [_persona_audit(), _memory_audit()]
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
        "generated_audio",
        "generated_image",
        "generated_video",
    ):
        assert forbidden not in serialized


def test_manifest_builder_exposes_no_provider_outbound_scheduler_or_media_methods() -> None:
    builder = _module().ApplyExecutorAuditManifestBuilder()

    for method_name in (
        "send",
        "schedule",
        "deliver",
        "call_provider",
        "open_webhook",
        "write_persona_version",
        "write_memory_store",
        "generate_reply",
        "generate_voice",
        "generate_avatar",
        "generate_audio",
        "generate_image",
        "generate_video",
        "connect_platform",
    ):
        assert not hasattr(builder, method_name)
