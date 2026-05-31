"""Review-only synthetic distillation readiness summaries.

This module aggregates synthetic distillation manifests, abstract style
features, and review queue refs into a safe local readiness surface. It does
not synthesize personas, retain source text, call providers, generate replies,
send messages, or connect to platform/media runtimes.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import utc_now
from practical_chat_agent.services.review_queue import ReviewQueueItem
from practical_chat_agent.services.synthetic_distillation_input import (
    DeidentifiedStyleFeatureCandidate,
    SyntheticDistillationInputManifest,
)


DistillationReadinessIssueSeverity = Literal["blocker", "warning"]


class _DistillationReadinessRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DistillationReadinessIssue(_DistillationReadinessRecord):
    schema_version: str = "distillation_readiness_issue_v1"
    issue_id: str = Field(default_factory=lambda: new_id("sdissue"))
    issue_code: str = Field(..., min_length=1)
    severity: DistillationReadinessIssueSeverity
    safe_summary: str = Field(..., min_length=1)
    source_ref: str | None = None
    blocks_readiness: bool = True
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_issue(self) -> "DistillationReadinessIssue":
        if self.severity == "blocker":
            self.blocks_readiness = True
        return self


class DistillationReviewReadinessSummary(_DistillationReadinessRecord):
    schema_version: str = "distillation_review_readiness_summary_v1"
    summary_id: str = Field(default_factory=lambda: new_id("sdready"))
    manifest_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    feature_ids: list[str] = Field(default_factory=list)
    review_queue_item_ids: list[str] = Field(default_factory=list)
    safe_summary: str = "[SYNTHETIC] Distillation review readiness summary."
    issues: list[DistillationReadinessIssue] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    source_text_retained: bool = False
    ready_for_persona_synthesis: bool = False
    review_required: bool = True
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_summary(self) -> "DistillationReviewReadinessSummary":
        if not self.review_required:
            raise ValueError("distillation readiness summaries require review")
        if self.runtime_ready:
            raise ValueError("distillation readiness summaries are never runtime-ready")

        self.feature_ids = _ordered_unique(self.feature_ids)
        self.review_queue_item_ids = _ordered_unique(self.review_queue_item_ids)
        self.issue_codes = _ordered_unique([issue.issue_code for issue in self.issues])
        self.blocking_issue_codes = _ordered_unique(
            [
                issue.issue_code
                for issue in self.issues
                if issue.blocks_readiness or issue.severity == "blocker"
            ]
        )
        if self.blocking_issue_codes or self.source_text_retained:
            self.ready_for_persona_synthesis = False
        return self


class DistillationReviewReadinessService:
    """Build review-only readiness summaries for synthetic distillation inputs."""

    def build_summary(
        self,
        manifest: SyntheticDistillationInputManifest,
        *,
        features: Iterable[DeidentifiedStyleFeatureCandidate] | None = None,
        review_items: Iterable[ReviewQueueItem] | None = None,
    ) -> DistillationReviewReadinessSummary:
        feature_list = list(features or [])
        review_item_list = list(review_items or [])
        issues: list[DistillationReadinessIssue] = []

        for reason in manifest.blocking_reasons:
            _add_issue(
                issues,
                issue_code=reason,
                safe_summary=f"[SYNTHETIC] Manifest blocks readiness: {reason}.",
                source_ref=manifest.manifest_id,
            )

        if not _has_active_persona_distillation_consent(manifest):
            _add_issue(
                issues,
                issue_code="persona_distillation_consent_missing_or_withdrawn",
                safe_summary="[SYNTHETIC] Active persona-distillation consent is missing or withdrawn.",
                source_ref=manifest.manifest_id,
            )

        if any(consent.withdrawn for consent in manifest.consent_refs):
            _add_issue(
                issues,
                issue_code="withdrawn_consent",
                safe_summary="[SYNTHETIC] Consent has been withdrawn.",
                source_ref=manifest.manifest_id,
            )

        if not manifest.clone_risk_decision.safe_transformation_allowed:
            _add_issue(
                issues,
                issue_code="clone_risk_blocked",
                safe_summary="[SYNTHETIC] Clone-risk decision blocks style transformation.",
                source_ref=manifest.clone_risk_decision.decision_id,
            )

        if manifest.source_category != "synthetic":
            _add_issue(
                issues,
                issue_code=manifest.source_category,
                safe_summary="[SYNTHETIC] Source category is not enabled for readiness.",
                source_ref=manifest.manifest_id,
            )

        if not feature_list:
            _add_issue(
                issues,
                issue_code="no_style_features",
                safe_summary="[SYNTHETIC] No de-identified style features were supplied.",
                source_ref=manifest.manifest_id,
            )

        source_text_retained = False
        feature_ids: list[str] = []
        for feature in feature_list:
            feature_ids.append(feature.feature_id)

            if feature.manifest_id != manifest.manifest_id:
                _add_issue(
                    issues,
                    issue_code="feature_manifest_mismatch",
                    safe_summary="[SYNTHETIC] Style feature does not match the manifest.",
                    source_ref=feature.feature_id,
                )

            if not feature.review_required:
                _add_issue(
                    issues,
                    issue_code="feature_not_review_required",
                    safe_summary="[SYNTHETIC] Style feature is missing review requirement.",
                    source_ref=feature.feature_id,
                )

            if feature.source_text_retained:
                source_text_retained = True
                _add_issue(
                    issues,
                    issue_code="source_text_retained",
                    safe_summary="[SYNTHETIC] Style feature retained source text.",
                    source_ref=feature.feature_id,
                )

            if feature.blocked_from_persona_synthesis:
                _add_issue(
                    issues,
                    issue_code="feature_blocked_from_persona_synthesis",
                    safe_summary="[SYNTHETIC] Style feature is blocked from persona synthesis.",
                    source_ref=feature.feature_id,
                )

            for reason in feature.blocking_reasons:
                _add_issue(
                    issues,
                    issue_code=reason,
                    safe_summary=f"[SYNTHETIC] Style feature blocks readiness: {reason}.",
                    source_ref=feature.feature_id,
                )

        review_queue_item_ids = [item.item_id for item in review_item_list]
        ready = not issues and not source_text_retained
        return DistillationReviewReadinessSummary(
            manifest_id=manifest.manifest_id,
            user_id=manifest.user_id,
            feature_ids=feature_ids,
            review_queue_item_ids=review_queue_item_ids,
            issues=issues,
            source_text_retained=source_text_retained,
            ready_for_persona_synthesis=ready,
        )


def _has_active_persona_distillation_consent(
    manifest: SyntheticDistillationInputManifest,
) -> bool:
    return any(
        consent.feature_scope == "persona_distillation"
        and consent.granted
        and not consent.withdrawn
        for consent in manifest.consent_refs
    )


def _add_issue(
    issues: list[DistillationReadinessIssue],
    *,
    issue_code: str,
    safe_summary: str,
    source_ref: str | None = None,
    severity: DistillationReadinessIssueSeverity = "blocker",
) -> None:
    if any(issue.issue_code == issue_code for issue in issues):
        return
    issues.append(
        DistillationReadinessIssue(
            issue_code=issue_code,
            severity=severity,
            safe_summary=safe_summary,
            source_ref=source_ref,
        )
    )


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
