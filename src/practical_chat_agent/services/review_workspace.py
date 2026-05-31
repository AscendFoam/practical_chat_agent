"""Local review workspace bindings for review-only artifacts.

The records here connect review queue items to source candidates and related
dry-run/readiness artifacts. They do not apply decisions, mutate stores, write
persona versions, call providers, synthesize personas, send messages, or
connect to platform/media runtimes.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import utc_now
from practical_chat_agent.services.distillation_review_readiness import (
    DistillationReviewReadinessSummary,
)
from practical_chat_agent.services.memory_governance import (
    MemoryContradictionCandidate,
    MemoryDeletionCascadePlan,
    MemorySupersessionCandidate,
    PersonaGrowthEvidenceBundle,
)
from practical_chat_agent.services.memory_lifecycle_dry_run import (
    MemoryLifecycleDryRunPlan,
)
from practical_chat_agent.services.memory_retrieval_explanation import (
    MemoryRetrievalExplanationResult,
)
from practical_chat_agent.services.persona_growth import PersonaGrowthPatchCandidate
from practical_chat_agent.services.persona_growth_dry_run import PersonaGrowthDryRunPlan
from practical_chat_agent.services.review_queue import ReviewCandidateKind, ReviewQueueItem
from practical_chat_agent.services.synthetic_distillation_input import (
    DeidentifiedStyleFeatureCandidate,
    SyntheticDistillationInputManifest,
)


ReviewWorkspaceIssueSeverity = Literal["blocker", "warning"]
ReviewWorkspaceArtifactKind = Literal[
    "memory_lifecycle_dry_run_plan",
    "persona_growth_dry_run_plan",
    "distillation_review_readiness_summary",
]


class _ReviewWorkspaceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReviewWorkspaceBindingIssue(_ReviewWorkspaceRecord):
    schema_version: str = "review_workspace_binding_issue_v1"
    issue_id: str = Field(default_factory=lambda: new_id("rwissue"))
    issue_code: str = Field(..., min_length=1)
    severity: ReviewWorkspaceIssueSeverity
    safe_summary: str = Field(..., min_length=1)
    source_ref: str | None = None
    blocks_workspace: bool = True
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_issue(self) -> "ReviewWorkspaceBindingIssue":
        if self.severity == "blocker":
            self.blocks_workspace = True
        return self


class ReviewWorkspaceCandidateBinding(_ReviewWorkspaceRecord):
    schema_version: str = "review_workspace_candidate_binding_v1"
    binding_id: str = Field(default_factory=lambda: new_id("rwbind"))
    queue_item_id: str = Field(..., min_length=1)
    candidate_kind: ReviewCandidateKind
    queue_candidate_id: str = Field(..., min_length=1)
    source_candidate_id: str = Field(..., min_length=1)
    source_schema_version: str | None = None
    owner_user_id: str | None = None
    persona_id: str | None = None
    safe_summary: str = Field(..., min_length=1)
    reason_labels: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    priority_score: int = Field(default=50, ge=0, le=100)
    priority_band: str = "normal"
    issues: list[ReviewWorkspaceBindingIssue] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    binding_ready: bool = False
    review_required: bool = True
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_candidate_binding(self) -> "ReviewWorkspaceCandidateBinding":
        if not self.review_required:
            raise ValueError("review workspace candidate bindings require review")
        if self.runtime_ready:
            raise ValueError("review workspace candidate bindings are never runtime-ready")
        self.reason_labels = _ordered_unique(self.reason_labels)
        self.source_refs = _ordered_unique(self.source_refs)
        self.issue_codes = _ordered_unique([issue.issue_code for issue in self.issues])
        self.blocking_issue_codes = _blocking_codes(self.issues)
        self.binding_ready = not self.blocking_issue_codes
        return self


class ReviewWorkspaceArtifactBinding(_ReviewWorkspaceRecord):
    schema_version: str = "review_workspace_artifact_binding_v1"
    binding_id: str = Field(default_factory=lambda: new_id("rwart"))
    artifact_kind: ReviewWorkspaceArtifactKind
    artifact_id: str = Field(..., min_length=1)
    source_candidate_kind: ReviewCandidateKind
    source_candidate_id: str = Field(..., min_length=1)
    candidate_binding_id: str = Field(..., min_length=1)
    queue_item_id: str = Field(..., min_length=1)
    review_queue_item_ids: list[str] = Field(default_factory=list)
    review_decision_ids: list[str] = Field(default_factory=list)
    safe_summary: str = Field(..., min_length=1)
    source_refs: list[str] = Field(default_factory=list)
    issues: list[ReviewWorkspaceBindingIssue] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    artifact_ready: bool = False
    preview_only: bool = True
    review_required: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_artifact_binding(self) -> "ReviewWorkspaceArtifactBinding":
        if not self.preview_only:
            raise ValueError("review workspace artifact bindings are preview-only")
        if not self.review_required:
            raise ValueError("review workspace artifact bindings require review")
        if self.applies_changes:
            raise ValueError("review workspace artifact bindings cannot apply changes")
        if self.writes_memory_store:
            raise ValueError("review workspace artifact bindings cannot write memory stores")
        if self.writes_persona_version:
            raise ValueError("review workspace artifact bindings cannot write persona versions")
        if self.runtime_ready:
            raise ValueError("review workspace artifact bindings are never runtime-ready")
        self.review_queue_item_ids = _ordered_unique(self.review_queue_item_ids)
        self.review_decision_ids = _ordered_unique(self.review_decision_ids)
        self.source_refs = _ordered_unique(self.source_refs)
        self.issue_codes = _ordered_unique([issue.issue_code for issue in self.issues])
        self.blocking_issue_codes = _blocking_codes(self.issues)
        self.artifact_ready = not self.blocking_issue_codes
        return self


class ReviewWorkspaceBundle(_ReviewWorkspaceRecord):
    schema_version: str = "review_workspace_bundle_v1"
    bundle_id: str = Field(default_factory=lambda: new_id("rwbundle"))
    candidate_bindings: list[ReviewWorkspaceCandidateBinding] = Field(default_factory=list)
    artifact_bindings: list[ReviewWorkspaceArtifactBinding] = Field(default_factory=list)
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

    @model_validator(mode="after")
    def validate_bundle(self) -> "ReviewWorkspaceBundle":
        if not self.preview_only:
            raise ValueError("review workspace bundles are preview-only")
        if not self.review_required:
            raise ValueError("review workspace bundles require review")
        if self.applies_changes:
            raise ValueError("review workspace bundles cannot apply changes")
        if self.writes_memory_store:
            raise ValueError("review workspace bundles cannot write memory stores")
        if self.writes_persona_version:
            raise ValueError("review workspace bundles cannot write persona versions")
        if self.runtime_ready:
            raise ValueError("review workspace bundles are never runtime-ready")

        issue_codes: list[str] = []
        blocking_codes: list[str] = []
        for binding in self.candidate_bindings:
            issue_codes.extend(binding.issue_codes)
            blocking_codes.extend(binding.blocking_issue_codes)
        for binding in self.artifact_bindings:
            issue_codes.extend(binding.issue_codes)
            blocking_codes.extend(binding.blocking_issue_codes)

        self.issue_codes = _ordered_unique(issue_codes)
        self.blocking_issue_codes = _ordered_unique(blocking_codes)
        self.workspace_ready = not self.blocking_issue_codes and all(
            binding.binding_ready for binding in self.candidate_bindings
        ) and all(binding.artifact_ready for binding in self.artifact_bindings)
        return self


class ReviewWorkspaceService:
    """Create review-only bindings for queue items and local review artifacts."""

    def bind_candidate(
        self,
        queue_item: ReviewQueueItem,
        source_candidate: object,
    ) -> ReviewWorkspaceCandidateBinding:
        source = _candidate_ref(source_candidate)
        issues: list[ReviewWorkspaceBindingIssue] = []
        if queue_item.candidate_kind != source.candidate_kind:
            _add_issue(
                issues,
                issue_code="candidate_kind_mismatch",
                safe_summary="[SYNTHETIC] Queue item kind does not match source candidate kind.",
                source_ref=queue_item.item_id,
            )
        if queue_item.candidate_id != source.candidate_id:
            _add_issue(
                issues,
                issue_code="candidate_id_mismatch",
                safe_summary="[SYNTHETIC] Queue item candidate id does not match source candidate id.",
                source_ref=queue_item.item_id,
            )
        return ReviewWorkspaceCandidateBinding(
            queue_item_id=queue_item.item_id,
            candidate_kind=queue_item.candidate_kind,
            queue_candidate_id=queue_item.candidate_id,
            source_candidate_id=source.candidate_id,
            source_schema_version=source.schema_version,
            owner_user_id=queue_item.owner_user_id or source.owner_user_id,
            persona_id=queue_item.persona_id or source.persona_id,
            safe_summary=queue_item.safe_summary,
            reason_labels=list(queue_item.reason_labels),
            source_refs=list(queue_item.source_refs),
            priority_score=queue_item.priority_score,
            priority_band=queue_item.priority_band,
            issues=issues,
        )

    def bind_artifact(
        self,
        candidate_binding: ReviewWorkspaceCandidateBinding,
        artifact: object,
    ) -> ReviewWorkspaceArtifactBinding:
        artifact_ref = _artifact_ref(artifact)
        issues: list[ReviewWorkspaceBindingIssue] = []
        if candidate_binding.candidate_kind != artifact_ref.source_candidate_kind:
            _add_issue(
                issues,
                issue_code="artifact_candidate_kind_mismatch",
                safe_summary="[SYNTHETIC] Artifact source kind does not match candidate binding kind.",
                source_ref=artifact_ref.artifact_id,
            )
        if candidate_binding.source_candidate_id != artifact_ref.source_candidate_id:
            _add_issue(
                issues,
                issue_code="artifact_source_candidate_id_mismatch",
                safe_summary="[SYNTHETIC] Artifact source id does not match candidate binding source id.",
                source_ref=artifact_ref.artifact_id,
            )
        if (
            artifact_ref.artifact_kind == "distillation_review_readiness_summary"
            and candidate_binding.queue_item_id not in artifact_ref.review_queue_item_ids
        ):
            _add_issue(
                issues,
                issue_code="review_queue_item_ref_mismatch",
                safe_summary="[SYNTHETIC] Artifact does not reference the bound review queue item.",
                source_ref=artifact_ref.artifact_id,
            )
        for issue_code in artifact_ref.blocking_issue_codes:
            _add_issue(
                issues,
                issue_code=issue_code,
                safe_summary=f"[SYNTHETIC] Artifact blocks readiness: {issue_code}.",
                source_ref=artifact_ref.artifact_id,
            )
        return ReviewWorkspaceArtifactBinding(
            artifact_kind=artifact_ref.artifact_kind,
            artifact_id=artifact_ref.artifact_id,
            source_candidate_kind=artifact_ref.source_candidate_kind,
            source_candidate_id=artifact_ref.source_candidate_id,
            candidate_binding_id=candidate_binding.binding_id,
            queue_item_id=candidate_binding.queue_item_id,
            review_queue_item_ids=artifact_ref.review_queue_item_ids,
            review_decision_ids=artifact_ref.review_decision_ids,
            safe_summary=artifact_ref.safe_summary,
            source_refs=artifact_ref.source_refs,
            issues=issues,
        )

    def build_bundle(
        self,
        *,
        candidate_bindings: Iterable[ReviewWorkspaceCandidateBinding] | None = None,
        artifact_bindings: Iterable[ReviewWorkspaceArtifactBinding] | None = None,
    ) -> ReviewWorkspaceBundle:
        return ReviewWorkspaceBundle(
            candidate_bindings=list(candidate_bindings or []),
            artifact_bindings=list(artifact_bindings or []),
        )


class _CandidateRef(BaseModel):
    candidate_kind: ReviewCandidateKind
    candidate_id: str
    schema_version: str | None = None
    owner_user_id: str | None = None
    persona_id: str | None = None


class _ArtifactRef(BaseModel):
    artifact_kind: ReviewWorkspaceArtifactKind
    artifact_id: str
    source_candidate_kind: ReviewCandidateKind
    source_candidate_id: str
    review_queue_item_ids: list[str] = Field(default_factory=list)
    review_decision_ids: list[str] = Field(default_factory=list)
    safe_summary: str
    source_refs: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)


def _candidate_ref(candidate: object) -> _CandidateRef:
    if isinstance(candidate, MemoryContradictionCandidate):
        return _CandidateRef(
            candidate_kind="memory_contradiction",
            candidate_id=candidate.candidate_id,
            schema_version=candidate.schema_version,
            owner_user_id=candidate.user_id,
        )
    if isinstance(candidate, MemorySupersessionCandidate):
        return _CandidateRef(
            candidate_kind="memory_supersession",
            candidate_id=candidate.candidate_id,
            schema_version=candidate.schema_version,
        )
    if isinstance(candidate, MemoryDeletionCascadePlan):
        return _CandidateRef(
            candidate_kind="memory_deletion_cascade",
            candidate_id=candidate.plan_id,
            schema_version=candidate.schema_version,
            owner_user_id=candidate.user_id,
        )
    if isinstance(candidate, PersonaGrowthEvidenceBundle):
        return _CandidateRef(
            candidate_kind="persona_growth_evidence",
            candidate_id=candidate.bundle_id,
            schema_version=candidate.schema_version,
            persona_id=candidate.persona_id,
        )
    if isinstance(candidate, PersonaGrowthPatchCandidate):
        return _CandidateRef(
            candidate_kind="persona_growth_patch",
            candidate_id=candidate.patch_id,
            schema_version=candidate.schema_version,
            owner_user_id=candidate.user_id,
            persona_id=candidate.persona_id,
        )
    if isinstance(candidate, SyntheticDistillationInputManifest):
        return _CandidateRef(
            candidate_kind="synthetic_distillation_manifest",
            candidate_id=candidate.manifest_id,
            schema_version=candidate.schema_version,
            owner_user_id=candidate.user_id,
        )
    if isinstance(candidate, DeidentifiedStyleFeatureCandidate):
        return _CandidateRef(
            candidate_kind="deidentified_style_feature",
            candidate_id=candidate.feature_id,
            schema_version=candidate.schema_version,
        )
    if isinstance(candidate, MemoryRetrievalExplanationResult):
        return _CandidateRef(
            candidate_kind="memory_retrieval_explanation",
            candidate_id=candidate.bundle.bundle_id,
            schema_version=candidate.schema_version,
        )
    raise TypeError(f"unsupported review workspace candidate type: {type(candidate).__name__}")


def _artifact_ref(artifact: object) -> _ArtifactRef:
    if isinstance(artifact, MemoryLifecycleDryRunPlan):
        queue_refs = [artifact.review_decision_id] if artifact.review_decision_id else []
        return _ArtifactRef(
            artifact_kind="memory_lifecycle_dry_run_plan",
            artifact_id=artifact.plan_id,
            source_candidate_kind=artifact.source_candidate_kind,
            source_candidate_id=artifact.source_candidate_id,
            review_queue_item_ids=queue_refs,
            review_decision_ids=queue_refs,
            safe_summary=artifact.safe_summary,
            source_refs=artifact.affected_memory_ids,
            blocking_issue_codes=[],
        )
    if isinstance(artifact, PersonaGrowthDryRunPlan):
        queue_refs = [artifact.review_decision_id] if artifact.review_decision_id else []
        return _ArtifactRef(
            artifact_kind="persona_growth_dry_run_plan",
            artifact_id=artifact.plan_id,
            source_candidate_kind="persona_growth_patch",
            source_candidate_id=artifact.patch_id,
            review_queue_item_ids=queue_refs,
            review_decision_ids=queue_refs,
            safe_summary=artifact.safe_summary,
            source_refs=[artifact.patch_id, artifact.persona_id],
            blocking_issue_codes=[],
        )
    if isinstance(artifact, DistillationReviewReadinessSummary):
        return _ArtifactRef(
            artifact_kind="distillation_review_readiness_summary",
            artifact_id=artifact.summary_id,
            source_candidate_kind="synthetic_distillation_manifest",
            source_candidate_id=artifact.manifest_id,
            review_queue_item_ids=list(artifact.review_queue_item_ids),
            safe_summary=artifact.safe_summary,
            source_refs=[artifact.manifest_id, *artifact.feature_ids],
            blocking_issue_codes=list(artifact.blocking_issue_codes),
        )
    raise TypeError(f"unsupported review workspace artifact type: {type(artifact).__name__}")


def _add_issue(
    issues: list[ReviewWorkspaceBindingIssue],
    *,
    issue_code: str,
    safe_summary: str,
    source_ref: str | None = None,
    severity: ReviewWorkspaceIssueSeverity = "blocker",
) -> None:
    if any(issue.issue_code == issue_code for issue in issues):
        return
    issues.append(
        ReviewWorkspaceBindingIssue(
            issue_code=issue_code,
            severity=severity,
            safe_summary=safe_summary,
            source_ref=source_ref,
        )
    )


def _blocking_codes(issues: Iterable[ReviewWorkspaceBindingIssue]) -> list[str]:
    return _ordered_unique(
        [
            issue.issue_code
            for issue in issues
            if issue.blocks_workspace or issue.severity == "blocker"
        ]
    )


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
