"""Review-only decision impact previews for local workspace bundles.

The records here summarize what a review queue decision would mean for a
review workspace bundle. They do not apply decisions, mutate stores, write
persona versions, call providers, generate replies, send messages, or connect
to platform/media runtimes.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import utc_now
from practical_chat_agent.services.review_queue import (
    ReviewCandidateKind,
    ReviewDecision,
    ReviewQueueDecisionRecord,
)
from practical_chat_agent.services.review_workspace import (
    ReviewWorkspaceArtifactBinding,
    ReviewWorkspaceArtifactKind,
    ReviewWorkspaceBindingIssue,
    ReviewWorkspaceBundle,
    ReviewWorkspaceCandidateBinding,
)


ReviewDecisionImpactSeverity = Literal["blocker", "warning"]
ReviewDecisionImpactOutcome = Literal[
    "future_manual_apply_eligible",
    "blocked_before_apply",
    "rejected_for_future_apply",
    "frozen_for_later_reconsideration",
    "changes_requested_before_apply",
]


class _ReviewDecisionImpactRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReviewDecisionImpactIssue(_ReviewDecisionImpactRecord):
    schema_version: str = "review_decision_impact_issue_v1"
    issue_id: str = Field(default_factory=lambda: new_id("rdiissue"))
    issue_code: str = Field(..., min_length=1)
    severity: ReviewDecisionImpactSeverity
    safe_summary: str = Field(..., min_length=1)
    source_ref: str | None = None
    blocks_preview: bool = True
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_issue(self) -> "ReviewDecisionImpactIssue":
        if self.severity == "blocker":
            self.blocks_preview = True
        return self


class ReviewDecisionArtifactImpact(_ReviewDecisionImpactRecord):
    schema_version: str = "review_decision_artifact_impact_v1"
    impact_id: str = Field(default_factory=lambda: new_id("rdiart"))
    artifact_kind: ReviewWorkspaceArtifactKind
    artifact_id: str = Field(..., min_length=1)
    candidate_binding_id: str = Field(..., min_length=1)
    queue_item_id: str = Field(..., min_length=1)
    review_decision_ids: list[str] = Field(default_factory=list)
    safe_summary: str = Field(..., min_length=1)
    source_refs: list[str] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    preview_only: bool = True
    review_required: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @classmethod
    def from_binding(
        cls,
        binding: ReviewWorkspaceArtifactBinding,
    ) -> "ReviewDecisionArtifactImpact":
        return cls(
            artifact_kind=binding.artifact_kind,
            artifact_id=binding.artifact_id,
            candidate_binding_id=binding.candidate_binding_id,
            queue_item_id=binding.queue_item_id,
            review_decision_ids=list(binding.review_decision_ids),
            safe_summary=binding.safe_summary,
            source_refs=list(binding.source_refs),
            issue_codes=list(binding.issue_codes),
            blocking_issue_codes=list(binding.blocking_issue_codes),
        )

    @model_validator(mode="after")
    def validate_artifact_impact(self) -> "ReviewDecisionArtifactImpact":
        if not self.preview_only:
            raise ValueError("review decision artifact impacts are preview-only")
        if not self.review_required:
            raise ValueError("review decision artifact impacts require review")
        if self.applies_changes:
            raise ValueError("review decision artifact impacts cannot apply changes")
        if self.writes_memory_store:
            raise ValueError("review decision artifact impacts cannot write memory stores")
        if self.writes_persona_version:
            raise ValueError("review decision artifact impacts cannot write persona versions")
        if self.runtime_ready:
            raise ValueError("review decision artifact impacts are never runtime-ready")
        self.review_decision_ids = _ordered_unique(self.review_decision_ids)
        self.source_refs = _ordered_unique(self.source_refs)
        self.issue_codes = _ordered_unique(self.issue_codes)
        self.blocking_issue_codes = _ordered_unique(self.blocking_issue_codes)
        return self


class ReviewDecisionImpactPreview(_ReviewDecisionImpactRecord):
    schema_version: str = "review_decision_impact_preview_v1"
    preview_id: str = Field(default_factory=lambda: new_id("rdiprev"))
    bundle_id: str = Field(..., min_length=1)
    decision_id: str = Field(..., min_length=1)
    item_id: str = Field(..., min_length=1)
    candidate_kind: ReviewCandidateKind
    candidate_id: str = Field(..., min_length=1)
    reviewer_id: str = Field(..., min_length=1)
    decision: ReviewDecision
    candidate_binding_id: str | None = None
    safe_summary: str = Field(..., min_length=1)
    reason_labels: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    artifact_impacts: list[ReviewDecisionArtifactImpact] = Field(default_factory=list)
    issues: list[ReviewDecisionImpactIssue] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    preview_outcome: ReviewDecisionImpactOutcome = "blocked_before_apply"
    future_manual_apply_eligible: bool = False
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_preview(self) -> "ReviewDecisionImpactPreview":
        if not self.preview_only:
            raise ValueError("review decision impact previews are preview-only")
        if not self.review_required:
            raise ValueError("review decision impact previews require review")
        if self.applies_changes:
            raise ValueError("review decision impact previews cannot apply changes")
        if self.writes_memory_store:
            raise ValueError("review decision impact previews cannot write memory stores")
        if self.writes_persona_version:
            raise ValueError("review decision impact previews cannot write persona versions")
        if self.runtime_ready:
            raise ValueError("review decision impact previews are never runtime-ready")

        self.reason_labels = _ordered_unique(self.reason_labels)
        self.source_refs = _ordered_unique(self.source_refs)
        issue_codes: list[str] = [issue.issue_code for issue in self.issues]
        blocking_codes: list[str] = [
            issue.issue_code
            for issue in self.issues
            if issue.blocks_preview or issue.severity == "blocker"
        ]
        for impact in self.artifact_impacts:
            issue_codes.extend(impact.issue_codes)
            blocking_codes.extend(impact.blocking_issue_codes)

        self.issue_codes = _ordered_unique(issue_codes)
        self.blocking_issue_codes = _ordered_unique(blocking_codes)
        if self.blocking_issue_codes:
            self.preview_outcome = "blocked_before_apply"
            self.future_manual_apply_eligible = False
        else:
            self.preview_outcome = _outcome_for_decision(self.decision)
            self.future_manual_apply_eligible = self.decision == "approve"
        return self


class ReviewDecisionImpactPreviewService:
    """Build non-applying review decision impact previews."""

    def preview_decision(
        self,
        bundle: ReviewWorkspaceBundle,
        decision_record: ReviewQueueDecisionRecord,
    ) -> ReviewDecisionImpactPreview:
        candidate_binding, issues = _candidate_binding_for_decision(
            bundle,
            decision_record,
        )
        if candidate_binding is None:
            artifact_impacts: list[ReviewDecisionArtifactImpact] = []
            safe_summary = "[SYNTHETIC] Review decision did not match this workspace."
            reason_labels: list[str] = []
            source_refs: list[str] = []
            candidate_binding_id = None
        else:
            issues.extend(_issues_from_binding(candidate_binding))
            artifact_bindings = [
                artifact
                for artifact in bundle.artifact_bindings
                if artifact.candidate_binding_id == candidate_binding.binding_id
            ]
            artifact_impacts = [
                ReviewDecisionArtifactImpact.from_binding(artifact)
                for artifact in artifact_bindings
            ]
            safe_summary = candidate_binding.safe_summary
            reason_labels = list(candidate_binding.reason_labels)
            source_refs = list(candidate_binding.source_refs)
            candidate_binding_id = candidate_binding.binding_id

        return ReviewDecisionImpactPreview(
            bundle_id=bundle.bundle_id,
            decision_id=decision_record.decision_id,
            item_id=decision_record.item_id,
            candidate_kind=decision_record.candidate_kind,
            candidate_id=decision_record.candidate_id,
            reviewer_id=decision_record.reviewer_id,
            decision=decision_record.decision,
            candidate_binding_id=candidate_binding_id,
            safe_summary=safe_summary,
            reason_labels=reason_labels,
            source_refs=source_refs,
            artifact_impacts=artifact_impacts,
            issues=issues,
        )


def _candidate_binding_for_decision(
    bundle: ReviewWorkspaceBundle,
    decision_record: ReviewQueueDecisionRecord,
) -> tuple[ReviewWorkspaceCandidateBinding | None, list[ReviewDecisionImpactIssue]]:
    issues: list[ReviewDecisionImpactIssue] = []
    item_match = next(
        (
            binding
            for binding in bundle.candidate_bindings
            if binding.queue_item_id == decision_record.item_id
        ),
        None,
    )
    if item_match is None:
        _add_issue(
            issues,
            issue_code="decision_item_not_in_workspace",
            safe_summary="[SYNTHETIC] Review decision item id is not in the workspace.",
            source_ref=decision_record.decision_id,
        )
        return None, issues

    if item_match.candidate_kind != decision_record.candidate_kind:
        _add_issue(
            issues,
            issue_code="decision_candidate_kind_mismatch",
            safe_summary="[SYNTHETIC] Review decision kind does not match workspace binding.",
            source_ref=item_match.binding_id,
        )
    if item_match.queue_candidate_id != decision_record.candidate_id:
        _add_issue(
            issues,
            issue_code="decision_candidate_id_mismatch",
            safe_summary="[SYNTHETIC] Review decision candidate id does not match workspace binding.",
            source_ref=item_match.binding_id,
        )
    return item_match, issues


def _issues_from_binding(
    binding: ReviewWorkspaceCandidateBinding,
) -> list[ReviewDecisionImpactIssue]:
    return [
        _issue_from_workspace_issue(issue, source_ref=binding.binding_id)
        for issue in binding.issues
    ]


def _issue_from_workspace_issue(
    issue: ReviewWorkspaceBindingIssue,
    *,
    source_ref: str,
) -> ReviewDecisionImpactIssue:
    return ReviewDecisionImpactIssue(
        issue_code=issue.issue_code,
        severity=issue.severity,
        safe_summary=issue.safe_summary,
        source_ref=issue.source_ref or source_ref,
        blocks_preview=issue.blocks_workspace,
    )


def _add_issue(
    issues: list[ReviewDecisionImpactIssue],
    *,
    issue_code: str,
    safe_summary: str,
    source_ref: str | None = None,
    severity: ReviewDecisionImpactSeverity = "blocker",
) -> None:
    if any(issue.issue_code == issue_code for issue in issues):
        return
    issues.append(
        ReviewDecisionImpactIssue(
            issue_code=issue_code,
            severity=severity,
            safe_summary=safe_summary,
            source_ref=source_ref,
        )
    )


def _outcome_for_decision(decision: ReviewDecision) -> ReviewDecisionImpactOutcome:
    if decision == "approve":
        return "future_manual_apply_eligible"
    if decision == "reject":
        return "rejected_for_future_apply"
    if decision == "freeze":
        return "frozen_for_later_reconsideration"
    return "changes_requested_before_apply"


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
