"""Safe local export manifests for review workspace records.

The records here package review workspace bundles and decision impact previews
for local review/audit surfaces. They do not apply decisions, mutate stores,
write persona versions, call providers, generate replies, send messages, or
connect to platform/media runtimes.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import utc_now
from practical_chat_agent.services.review_decision_impact_preview import (
    ReviewDecisionImpactOutcome,
    ReviewDecisionImpactPreview,
)
from practical_chat_agent.services.review_queue import ReviewCandidateKind, ReviewDecision
from practical_chat_agent.services.review_workspace import (
    ReviewWorkspaceArtifactBinding,
    ReviewWorkspaceArtifactKind,
    ReviewWorkspaceBundle,
    ReviewWorkspaceCandidateBinding,
)


class _ReviewWorkspaceExportRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReviewWorkspaceExportItem(_ReviewWorkspaceExportRecord):
    schema_version: str = "review_workspace_export_item_v1"
    export_item_id: str = Field(default_factory=lambda: new_id("rwexpitem"))
    bundle_id: str = Field(..., min_length=1)
    queue_item_id: str = Field(..., min_length=1)
    candidate_binding_id: str = Field(..., min_length=1)
    candidate_kind: ReviewCandidateKind
    candidate_id: str = Field(..., min_length=1)
    safe_summary: str = Field(..., min_length=1)
    reason_labels: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    artifact_kinds: list[ReviewWorkspaceArtifactKind] = Field(default_factory=list)
    artifact_ids: list[str] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    workspace_ready: bool = False
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_binding(
        cls,
        bundle: ReviewWorkspaceBundle,
        binding: ReviewWorkspaceCandidateBinding,
        artifacts: Iterable[ReviewWorkspaceArtifactBinding],
    ) -> "ReviewWorkspaceExportItem":
        ordered_artifacts = sorted(
            list(artifacts),
            key=lambda artifact: (artifact.artifact_kind, artifact.artifact_id),
        )
        return cls(
            bundle_id=bundle.bundle_id,
            queue_item_id=binding.queue_item_id,
            candidate_binding_id=binding.binding_id,
            candidate_kind=binding.candidate_kind,
            candidate_id=binding.queue_candidate_id,
            safe_summary=binding.safe_summary,
            reason_labels=list(binding.reason_labels),
            source_refs=list(binding.source_refs),
            artifact_kinds=[artifact.artifact_kind for artifact in ordered_artifacts],
            artifact_ids=[artifact.artifact_id for artifact in ordered_artifacts],
            issue_codes=[*binding.issue_codes, *bundle.issue_codes],
            blocking_issue_codes=[
                *binding.blocking_issue_codes,
                *bundle.blocking_issue_codes,
            ],
            workspace_ready=bundle.workspace_ready and binding.binding_ready,
        )

    @model_validator(mode="after")
    def validate_export_item(self) -> "ReviewWorkspaceExportItem":
        if not self.review_required:
            raise ValueError("review workspace export items require review")
        if not self.preview_only:
            raise ValueError("review workspace export items are preview-only")
        if self.applies_changes:
            raise ValueError("review workspace export items cannot apply changes")
        if self.writes_memory_store:
            raise ValueError("review workspace export items cannot write memory stores")
        if self.writes_persona_version:
            raise ValueError("review workspace export items cannot write persona versions")
        if self.runtime_ready:
            raise ValueError("review workspace export items are never runtime-ready")
        self.reason_labels = _ordered_unique(self.reason_labels)
        self.source_refs = _ordered_unique(self.source_refs)
        self.artifact_kinds = _ordered_unique(self.artifact_kinds)
        self.artifact_ids = _ordered_unique(self.artifact_ids)
        self.issue_codes = _ordered_unique(self.issue_codes)
        self.blocking_issue_codes = _ordered_unique(self.blocking_issue_codes)
        return self


class ReviewWorkspaceImpactExportItem(_ReviewWorkspaceExportRecord):
    schema_version: str = "review_workspace_impact_export_item_v1"
    export_item_id: str = Field(default_factory=lambda: new_id("rwimpactexp"))
    bundle_id: str = Field(..., min_length=1)
    preview_id: str = Field(..., min_length=1)
    decision_id: str = Field(..., min_length=1)
    item_id: str = Field(..., min_length=1)
    candidate_kind: ReviewCandidateKind
    candidate_id: str = Field(..., min_length=1)
    decision: ReviewDecision
    preview_outcome: ReviewDecisionImpactOutcome
    future_manual_apply_eligible: bool = False
    safe_summary: str = Field(..., min_length=1)
    reason_labels: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    artifact_ids: list[str] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_preview(
        cls,
        preview: ReviewDecisionImpactPreview,
    ) -> "ReviewWorkspaceImpactExportItem":
        artifact_ids = sorted(impact.artifact_id for impact in preview.artifact_impacts)
        return cls(
            bundle_id=preview.bundle_id,
            preview_id=preview.preview_id,
            decision_id=preview.decision_id,
            item_id=preview.item_id,
            candidate_kind=preview.candidate_kind,
            candidate_id=preview.candidate_id,
            decision=preview.decision,
            preview_outcome=preview.preview_outcome,
            future_manual_apply_eligible=preview.future_manual_apply_eligible,
            safe_summary=preview.safe_summary,
            reason_labels=list(preview.reason_labels),
            source_refs=list(preview.source_refs),
            artifact_ids=artifact_ids,
            issue_codes=list(preview.issue_codes),
            blocking_issue_codes=list(preview.blocking_issue_codes),
        )

    @model_validator(mode="after")
    def validate_impact_export_item(self) -> "ReviewWorkspaceImpactExportItem":
        if not self.review_required:
            raise ValueError("review workspace impact export items require review")
        if not self.preview_only:
            raise ValueError("review workspace impact export items are preview-only")
        if self.applies_changes:
            raise ValueError("review workspace impact export items cannot apply changes")
        if self.writes_memory_store:
            raise ValueError("review workspace impact export items cannot write memory stores")
        if self.writes_persona_version:
            raise ValueError("review workspace impact export items cannot write persona versions")
        if self.runtime_ready:
            raise ValueError("review workspace impact export items are never runtime-ready")
        self.reason_labels = _ordered_unique(self.reason_labels)
        self.source_refs = _ordered_unique(self.source_refs)
        self.artifact_ids = _ordered_unique(self.artifact_ids)
        self.issue_codes = _ordered_unique(self.issue_codes)
        self.blocking_issue_codes = _ordered_unique(self.blocking_issue_codes)
        return self


class ReviewWorkspaceSafeExportManifest(_ReviewWorkspaceExportRecord):
    schema_version: str = "review_workspace_safe_export_manifest_v1"
    manifest_id: str = Field(default_factory=lambda: new_id("rwexport"))
    workspace_items: list[ReviewWorkspaceExportItem] = Field(default_factory=list)
    impact_items: list[ReviewWorkspaceImpactExportItem] = Field(default_factory=list)
    counts_by_candidate_kind: dict[str, int] = Field(default_factory=dict)
    counts_by_artifact_kind: dict[str, int] = Field(default_factory=dict)
    counts_by_decision_outcome: dict[str, int] = Field(default_factory=dict)
    counts_by_blocker_code: dict[str, int] = Field(default_factory=dict)
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    generated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_manifest(self) -> "ReviewWorkspaceSafeExportManifest":
        if not self.review_required:
            raise ValueError("review workspace export manifests require review")
        if not self.preview_only:
            raise ValueError("review workspace export manifests are preview-only")
        if self.applies_changes:
            raise ValueError("review workspace export manifests cannot apply changes")
        if self.writes_memory_store:
            raise ValueError("review workspace export manifests cannot write memory stores")
        if self.writes_persona_version:
            raise ValueError("review workspace export manifests cannot write persona versions")
        if self.runtime_ready:
            raise ValueError("review workspace export manifests are never runtime-ready")

        self.workspace_items = sorted(
            self.workspace_items,
            key=lambda item: (item.bundle_id, item.queue_item_id, item.candidate_id),
        )
        self.impact_items = sorted(
            self.impact_items,
            key=lambda item: (
                item.bundle_id,
                item.item_id,
                item.candidate_id,
                item.decision_id,
                item.preview_id,
            ),
        )
        self.counts_by_candidate_kind = _count_sorted(
            item.candidate_kind for item in self.workspace_items
        )
        self.counts_by_artifact_kind = _count_sorted(
            kind
            for item in self.workspace_items
            for kind in item.artifact_kinds
        )
        self.counts_by_decision_outcome = _count_sorted(
            item.preview_outcome for item in self.impact_items
        )
        self.counts_by_blocker_code = _count_sorted(
            [
                *(
                    code
                    for item in self.workspace_items
                    for code in item.blocking_issue_codes
                ),
                *(
                    code
                    for item in self.impact_items
                    for code in item.blocking_issue_codes
                ),
            ]
        )
        return self


class ReviewWorkspaceSafeExportService:
    """Create and write safe local review workspace export manifests."""

    def build_manifest(
        self,
        bundles: Iterable[ReviewWorkspaceBundle],
        *,
        impact_previews: Iterable[ReviewDecisionImpactPreview] | None = None,
    ) -> ReviewWorkspaceSafeExportManifest:
        workspace_items: list[ReviewWorkspaceExportItem] = []
        for bundle in bundles:
            for binding in bundle.candidate_bindings:
                artifacts = [
                    artifact
                    for artifact in bundle.artifact_bindings
                    if artifact.candidate_binding_id == binding.binding_id
                ]
                workspace_items.append(
                    ReviewWorkspaceExportItem.from_binding(
                        bundle,
                        binding,
                        artifacts,
                    )
                )
        impact_items = [
            ReviewWorkspaceImpactExportItem.from_preview(preview)
            for preview in impact_previews or []
        ]
        return ReviewWorkspaceSafeExportManifest(
            workspace_items=workspace_items,
            impact_items=impact_items,
        )

    def write_manifest(
        self,
        manifest: ReviewWorkspaceSafeExportManifest,
        root: Path | str,
        *,
        file_name: str | None = None,
    ) -> Path:
        export_root = Path(root).resolve()
        export_root.mkdir(parents=True, exist_ok=True)
        path = _manifest_path(export_root, file_name or f"{manifest.manifest_id}.json")
        path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
        return path


def _manifest_path(root: Path, file_name: str) -> Path:
    if Path(file_name).is_absolute():
        raise ValueError("review workspace export path must be relative to export root")
    candidate = (root / file_name).resolve()
    if not candidate.is_relative_to(root):
        raise ValueError("review workspace export path escapes export root")
    if candidate.suffix != ".json":
        raise ValueError("review workspace export files must use .json")
    return candidate


def _count_sorted(values: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        if not value:
            continue
        counts[value] = counts.get(value, 0) + 1
    return {key: counts[key] for key in sorted(counts)}


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
