"""Local-only manifest for completed apply executor audits."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import utc_now
from practical_chat_agent.services.memory_lifecycle_apply_executor import (
    MemoryLifecycleApplyAudit,
)
from practical_chat_agent.services.persona_growth_apply_executor import (
    PersonaGrowthApplyAudit,
)


ApplyExecutorAuditType = Literal["persona_growth", "memory_lifecycle"]
ApplyExecutorSourceArtifactKind = Literal[
    "persona_growth_patch",
    "memory_lifecycle_plan",
]


class ApplyExecutorAuditManifestError(ValueError):
    """Raised when apply audit records cannot be safely manifested."""


class _ApplyExecutorAuditManifestRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ApplyExecutorAuditManifestEntry(_ApplyExecutorAuditManifestRecord):
    schema_version: str = "apply_executor_audit_manifest_entry_v1"
    entry_id: str = Field(default_factory=lambda: new_id("aementry"))
    apply_type: ApplyExecutorAuditType
    apply_id: str = Field(..., min_length=1)
    source_artifact_kind: ApplyExecutorSourceArtifactKind
    source_artifact_id: str = Field(..., min_length=1)
    review_decision_id: str = Field(..., min_length=1)
    eligibility_id: str = Field(..., min_length=1)
    approval_id: str = Field(..., min_length=1)
    reviewer_id: str = Field(..., min_length=1)
    rollback_refs: dict[str, str] = Field(default_factory=dict)
    applied_refs: dict[str, str] = Field(default_factory=dict)
    changed_field_paths: list[str] = Field(default_factory=list)
    affected_memory_ids: list[str] = Field(default_factory=list)
    safe_summary: str = Field(..., min_length=1)
    final_confirmation: Literal["confirmed"] = "confirmed"
    local_only: bool = True
    review_required: bool = True
    automatic_apply: bool = False
    calls_provider: bool = False
    sends_messages: bool = False
    runtime_ready: bool = False
    created_at: datetime

    @model_validator(mode="after")
    def validate_entry(self) -> "ApplyExecutorAuditManifestEntry":
        _validate_local_review_flags(
            final_confirmation=self.final_confirmation,
            local_only=self.local_only,
            review_required=self.review_required,
            automatic_apply=self.automatic_apply,
            calls_provider=self.calls_provider,
            sends_messages=self.sends_messages,
            runtime_ready=self.runtime_ready,
            record_name="apply executor audit manifest entries",
        )
        if not _non_empty_values(self.rollback_refs):
            raise ValueError("apply executor audit manifest entries require rollback refs")
        self.changed_field_paths = _ordered_unique(self.changed_field_paths)
        self.affected_memory_ids = _ordered_unique(self.affected_memory_ids)
        return self


class ApplyExecutorAuditManifest(_ApplyExecutorAuditManifestRecord):
    schema_version: str = "apply_executor_audit_manifest_v1"
    manifest_id: str = Field(default_factory=lambda: new_id("aemanifest"))
    entries: list[ApplyExecutorAuditManifestEntry] = Field(default_factory=list)
    entry_count: int = Field(default=0, ge=0)
    local_only: bool = True
    review_required: bool = True
    automatic_apply: bool = False
    calls_provider: bool = False
    sends_messages: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_manifest(self) -> "ApplyExecutorAuditManifest":
        _validate_local_review_flags(
            final_confirmation="confirmed",
            local_only=self.local_only,
            review_required=self.review_required,
            automatic_apply=self.automatic_apply,
            calls_provider=self.calls_provider,
            sends_messages=self.sends_messages,
            runtime_ready=self.runtime_ready,
            record_name="apply executor audit manifests",
        )
        self.entries = sorted(
            self.entries,
            key=lambda entry: (entry.created_at, entry.apply_id),
        )
        self.entry_count = len(self.entries)
        return self


class ApplyExecutorAuditManifestBuilder:
    """Normalize completed local apply audits into a reviewable manifest."""

    def build(self, audits: Iterable[object]) -> ApplyExecutorAuditManifest:
        entries = [_entry_from_audit(audit) for audit in audits]
        return ApplyExecutorAuditManifest(entries=entries)


def _entry_from_audit(audit: object) -> ApplyExecutorAuditManifestEntry:
    if isinstance(audit, PersonaGrowthApplyAudit):
        return _entry_from_persona_growth(audit)
    if isinstance(audit, MemoryLifecycleApplyAudit):
        return _entry_from_memory_lifecycle(audit)
    schema_version = _schema_version(audit)
    raise ApplyExecutorAuditManifestError(
        f"unsupported apply audit schema: {schema_version or type(audit).__name__}"
    )


def _entry_from_persona_growth(
    audit: PersonaGrowthApplyAudit,
) -> ApplyExecutorAuditManifestEntry:
    _validate_common_audit(audit, record_name="persona growth apply audit")
    if not audit.rollback_target_version_id:
        raise ApplyExecutorAuditManifestError(
            "persona growth apply audit requires rollback target version id"
        )
    rollback_refs = {
        "prior_version_id": audit.prior_version_id,
        "rollback_target_version_id": audit.rollback_target_version_id,
    }
    if not _non_empty_values(rollback_refs):
        raise ApplyExecutorAuditManifestError(
            "persona growth apply audit requires rollback refs"
        )
    return ApplyExecutorAuditManifestEntry(
        apply_type="persona_growth",
        apply_id=audit.apply_id,
        source_artifact_kind="persona_growth_patch",
        source_artifact_id=audit.patch_id,
        review_decision_id=audit.review_decision_id,
        eligibility_id=audit.eligibility_id,
        approval_id=audit.approval_id,
        reviewer_id=audit.reviewer_id,
        rollback_refs=rollback_refs,
        applied_refs={"new_version_id": audit.new_version_id},
        changed_field_paths=list(audit.changed_field_paths),
        safe_summary=audit.safe_summary,
        created_at=audit.created_at,
    )


def _entry_from_memory_lifecycle(
    audit: MemoryLifecycleApplyAudit,
) -> ApplyExecutorAuditManifestEntry:
    _validate_common_audit(audit, record_name="memory lifecycle apply audit")
    if not audit.affected_memory_ids:
        raise ApplyExecutorAuditManifestError(
            "memory lifecycle apply audit requires affected memory ids"
        )
    missing_rollback_ids = [
        memory_id
        for memory_id in audit.affected_memory_ids
        if not audit.rollback_record_ids.get(memory_id)
    ]
    if missing_rollback_ids:
        raise ApplyExecutorAuditManifestError(
            "memory lifecycle apply audit requires rollback record ids"
        )
    return ApplyExecutorAuditManifestEntry(
        apply_type="memory_lifecycle",
        apply_id=audit.apply_id,
        source_artifact_kind="memory_lifecycle_plan",
        source_artifact_id=audit.plan_id,
        review_decision_id=audit.review_decision_id,
        eligibility_id=audit.eligibility_id,
        approval_id=audit.approval_id,
        reviewer_id=audit.reviewer_id,
        rollback_refs=dict(audit.rollback_record_ids),
        applied_refs=dict(audit.applied_record_ids),
        affected_memory_ids=list(audit.affected_memory_ids),
        safe_summary=audit.safe_summary,
        created_at=audit.created_at,
    )


def _validate_common_audit(audit: object, *, record_name: str) -> None:
    try:
        _validate_local_review_flags(
            final_confirmation=getattr(audit, "final_confirmation"),
            local_only=getattr(audit, "local_only"),
            review_required=getattr(audit, "review_required"),
            automatic_apply=getattr(audit, "automatic_apply"),
            calls_provider=getattr(audit, "calls_provider"),
            sends_messages=getattr(audit, "sends_messages"),
            runtime_ready=getattr(audit, "runtime_ready"),
            record_name=record_name,
        )
    except ValueError as exc:
        raise ApplyExecutorAuditManifestError(str(exc)) from exc


def _validate_local_review_flags(
    *,
    final_confirmation: str,
    local_only: bool,
    review_required: bool,
    automatic_apply: bool,
    calls_provider: bool,
    sends_messages: bool,
    runtime_ready: bool,
    record_name: str,
) -> None:
    if final_confirmation != "confirmed":
        raise ValueError(f"{record_name} require confirmed final confirmation")
    if not local_only:
        raise ValueError(f"{record_name} must stay local-only")
    if not review_required:
        raise ValueError(f"{record_name} require review")
    if automatic_apply:
        raise ValueError(f"{record_name} cannot be automatic")
    if calls_provider:
        raise ValueError(f"{record_name} cannot call providers")
    if sends_messages:
        raise ValueError(f"{record_name} cannot send messages")
    if runtime_ready:
        raise ValueError(f"{record_name} are not runtime-ready")


def _schema_version(audit: object) -> str | None:
    if isinstance(audit, dict):
        value = audit.get("schema_version")
        return value if isinstance(value, str) else None
    value = getattr(audit, "schema_version", None)
    return value if isinstance(value, str) else None


def _non_empty_values(values: dict[str, str]) -> bool:
    return bool(values) and all(key and value for key, value in values.items())


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
