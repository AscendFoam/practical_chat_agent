"""UI-ready presentation models for local review workspace records.

The adapter projects safe M28 review records into deterministic view models for
a later local static panel. It does not apply decisions, mutate stores, write
persona versions, call providers, generate replies, send messages, or connect
to platform/media runtimes.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from practical_chat_agent.core.ids import new_id
from practical_chat_agent.core.models import utc_now
from practical_chat_agent.services.review_decision_impact_preview import (
    ReviewDecisionImpactOutcome,
    ReviewDecisionImpactPreview,
)
from practical_chat_agent.services.review_queue import ReviewCandidateKind
from practical_chat_agent.services.review_workspace import (
    ReviewWorkspaceArtifactBinding,
    ReviewWorkspaceBundle,
    ReviewWorkspaceCandidateBinding,
)
from practical_chat_agent.services.review_workspace_export import (
    ReviewWorkspaceSafeExportManifest,
)


ReviewWorkspacePresentationTone = Literal["blocked", "eligible", "review", "info"]
ReviewWorkspacePresentationCardKind = Literal[
    "workspace_item",
    "decision_impact",
    "export_summary",
]


class _ReviewWorkspacePresentationRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReviewWorkspaceStatusBadge(_ReviewWorkspacePresentationRecord):
    schema_version: str = "review_workspace_status_badge_v1"
    badge_id: str = Field(default_factory=lambda: new_id("rwbadge"))
    label: str = Field(..., min_length=1)
    tone: ReviewWorkspacePresentationTone
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_badge(self) -> "ReviewWorkspaceStatusBadge":
        _validate_non_runtime_flags(
            review_required=self.review_required,
            preview_only=self.preview_only,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="review workspace status badges",
        )
        self.issue_codes = _ordered_unique(self.issue_codes)
        self.blocking_issue_codes = _ordered_unique(self.blocking_issue_codes)
        return self


class ReviewWorkspacePresentationCard(_ReviewWorkspacePresentationRecord):
    schema_version: str = "review_workspace_presentation_card_v1"
    card_id: str = Field(default_factory=lambda: new_id("rwcard"))
    card_kind: ReviewWorkspacePresentationCardKind
    title: str = Field(..., min_length=1)
    display_label: str = Field(..., min_length=1)
    safe_summary: str = Field(..., min_length=1)
    filter_keys: list[str] = Field(default_factory=list)
    status_badges: list[ReviewWorkspaceStatusBadge] = Field(default_factory=list)
    bundle_id: str | None = None
    queue_item_id: str | None = None
    candidate_kind: ReviewCandidateKind | None = None
    candidate_id: str | None = None
    decision_id: str | None = None
    preview_outcome: ReviewDecisionImpactOutcome | None = None
    reason_labels: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    issue_codes: list[str] = Field(default_factory=list)
    blocking_issue_codes: list[str] = Field(default_factory=list)
    counts: dict[str, int] = Field(default_factory=dict)
    urgency_rank: int = Field(default=2, ge=0)
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_card(self) -> "ReviewWorkspacePresentationCard":
        _validate_non_runtime_flags(
            review_required=self.review_required,
            preview_only=self.preview_only,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="review workspace presentation cards",
        )
        self.filter_keys = _ordered_unique(self.filter_keys)
        self.reason_labels = _ordered_unique(self.reason_labels)
        self.source_refs = _ordered_unique(self.source_refs)
        self.issue_codes = _ordered_unique(self.issue_codes)
        self.blocking_issue_codes = _ordered_unique(self.blocking_issue_codes)
        self.counts = {key: self.counts[key] for key in sorted(self.counts)}
        return self


class ReviewWorkspacePresentationPanel(_ReviewWorkspacePresentationRecord):
    schema_version: str = "review_workspace_presentation_panel_v1"
    panel_id: str = Field(default_factory=lambda: new_id("rwpanel"))
    cards: list[ReviewWorkspacePresentationCard] = Field(default_factory=list)
    filter_tabs: list[dict[str, Any]] = Field(default_factory=list)
    review_required: bool = True
    preview_only: bool = True
    applies_changes: bool = False
    writes_memory_store: bool = False
    writes_persona_version: bool = False
    runtime_ready: bool = False
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def validate_panel(self) -> "ReviewWorkspacePresentationPanel":
        _validate_non_runtime_flags(
            review_required=self.review_required,
            preview_only=self.preview_only,
            applies_changes=self.applies_changes,
            writes_memory_store=self.writes_memory_store,
            writes_persona_version=self.writes_persona_version,
            runtime_ready=self.runtime_ready,
            record_name="review workspace presentation panels",
        )
        self.cards = sorted(self.cards, key=_card_sort_key)
        self.filter_tabs = _filter_tabs(self.cards)
        return self


class ReviewWorkspacePresentationAdapter:
    """Project safe review workspace records into UI-ready cards."""

    def build_panel(
        self,
        *,
        bundles: Iterable[ReviewWorkspaceBundle],
        impact_previews: Iterable[ReviewDecisionImpactPreview] | None = None,
        export_manifest: ReviewWorkspaceSafeExportManifest | None = None,
    ) -> ReviewWorkspacePresentationPanel:
        cards: list[ReviewWorkspacePresentationCard] = []
        for bundle in bundles:
            for binding in bundle.candidate_bindings:
                artifacts = [
                    artifact
                    for artifact in bundle.artifact_bindings
                    if artifact.candidate_binding_id == binding.binding_id
                ]
                cards.append(_workspace_card(bundle, binding, artifacts))
        for preview in impact_previews or []:
            cards.append(_impact_card(preview))
        if export_manifest is not None:
            cards.append(_export_summary_card(export_manifest))
        return ReviewWorkspacePresentationPanel(cards=cards)


def _workspace_card(
    bundle: ReviewWorkspaceBundle,
    binding: ReviewWorkspaceCandidateBinding,
    artifacts: Iterable[ReviewWorkspaceArtifactBinding],
) -> ReviewWorkspacePresentationCard:
    artifact_ids = [artifact.artifact_id for artifact in artifacts]
    category = _category_for_candidate_kind(binding.candidate_kind)
    blocked = bool(binding.blocking_issue_codes or bundle.blocking_issue_codes)
    filter_keys = _filter_keys(category=category, blocked=blocked)
    blocking_codes = _ordered_unique(
        [*binding.blocking_issue_codes, *bundle.blocking_issue_codes]
    )
    issue_codes = _ordered_unique([*binding.issue_codes, *bundle.issue_codes])
    return ReviewWorkspacePresentationCard(
        card_kind="workspace_item",
        title=_title_for_candidate_kind(binding.candidate_kind),
        display_label=binding.candidate_kind.replace("_", " "),
        safe_summary=binding.safe_summary,
        filter_keys=filter_keys,
        status_badges=[
            _status_badge(
                label="Blocked" if blocked else "Review ready",
                tone="blocked" if blocked else "eligible",
                issue_codes=issue_codes,
                blocking_issue_codes=blocking_codes,
            )
        ],
        bundle_id=bundle.bundle_id,
        queue_item_id=binding.queue_item_id,
        candidate_kind=binding.candidate_kind,
        candidate_id=binding.queue_candidate_id,
        reason_labels=list(binding.reason_labels),
        source_refs=_ordered_unique([*binding.source_refs, *artifact_ids]),
        issue_codes=issue_codes,
        blocking_issue_codes=blocking_codes,
        urgency_rank=0 if blocked else 1,
    )


def _impact_card(preview: ReviewDecisionImpactPreview) -> ReviewWorkspacePresentationCard:
    category = _category_for_candidate_kind(preview.candidate_kind)
    blocked = bool(preview.blocking_issue_codes)
    filter_keys = _filter_keys(category=category, blocked=blocked)
    label, tone = _badge_for_outcome(preview.preview_outcome)
    return ReviewWorkspacePresentationCard(
        card_kind="decision_impact",
        title="Decision impact preview",
        display_label=preview.preview_outcome.replace("_", " "),
        safe_summary=preview.safe_summary,
        filter_keys=filter_keys,
        status_badges=[
            _status_badge(
                label=label,
                tone=tone,
                issue_codes=preview.issue_codes,
                blocking_issue_codes=preview.blocking_issue_codes,
            )
        ],
        bundle_id=preview.bundle_id,
        queue_item_id=preview.item_id,
        candidate_kind=preview.candidate_kind,
        candidate_id=preview.candidate_id,
        decision_id=preview.decision_id,
        preview_outcome=preview.preview_outcome,
        reason_labels=list(preview.reason_labels),
        source_refs=list(preview.source_refs),
        issue_codes=list(preview.issue_codes),
        blocking_issue_codes=list(preview.blocking_issue_codes),
        urgency_rank=0 if blocked else 1,
    )


def _export_summary_card(
    manifest: ReviewWorkspaceSafeExportManifest,
) -> ReviewWorkspacePresentationCard:
    counts: dict[str, int] = {}
    for key, value in manifest.counts_by_candidate_kind.items():
        counts[f"candidate_kind:{key}"] = value
    for key, value in manifest.counts_by_artifact_kind.items():
        counts[f"artifact_kind:{key}"] = value
    for key, value in manifest.counts_by_decision_outcome.items():
        counts[f"decision_outcome:{key}"] = value
    for key, value in manifest.counts_by_blocker_code.items():
        counts[f"blocker:{key}"] = value
    return ReviewWorkspacePresentationCard(
        card_kind="export_summary",
        title="Safe export summary",
        display_label="safe export summary",
        safe_summary="[SYNTHETIC] Safe export manifest summary.",
        filter_keys=["all"],
        status_badges=[
            _status_badge(
                label="Safe export summary",
                tone="info",
                issue_codes=[],
                blocking_issue_codes=[],
            )
        ],
        counts=counts,
        urgency_rank=3,
    )


def _status_badge(
    *,
    label: str,
    tone: ReviewWorkspacePresentationTone,
    issue_codes: Iterable[str],
    blocking_issue_codes: Iterable[str],
) -> ReviewWorkspaceStatusBadge:
    return ReviewWorkspaceStatusBadge(
        label=label,
        tone=tone,
        issue_codes=list(issue_codes),
        blocking_issue_codes=list(blocking_issue_codes),
    )


def _badge_for_outcome(
    outcome: ReviewDecisionImpactOutcome,
) -> tuple[str, ReviewWorkspacePresentationTone]:
    if outcome == "blocked_before_apply":
        return "Blocked before apply", "blocked"
    if outcome == "future_manual_apply_eligible":
        return "Eligible for later manual apply", "eligible"
    if outcome == "rejected_for_future_apply":
        return "Rejected for future apply", "review"
    if outcome == "frozen_for_later_reconsideration":
        return "Frozen for later review", "review"
    return "Changes requested", "review"


def _filter_keys(*, category: str, blocked: bool) -> list[str]:
    state_key = "blocked" if blocked else "eligible"
    return _ordered_unique(["all", state_key, category])


def _filter_tabs(cards: list[ReviewWorkspacePresentationCard]) -> list[dict[str, Any]]:
    return [
        {"key": key, "label": label, "count": sum(key in card.filter_keys for card in cards)}
        for key, label in (
            ("all", "All"),
            ("blocked", "Blocked"),
            ("eligible", "Eligible"),
            ("memory", "Memory"),
            ("persona", "Persona"),
            ("distillation", "Distillation"),
        )
    ]


def _category_for_candidate_kind(candidate_kind: ReviewCandidateKind) -> str:
    if candidate_kind.startswith("memory_"):
        return "memory"
    if candidate_kind.startswith("persona_"):
        return "persona"
    if candidate_kind in {"synthetic_distillation_manifest", "deidentified_style_feature"}:
        return "distillation"
    return "memory"


def _title_for_candidate_kind(candidate_kind: ReviewCandidateKind) -> str:
    if candidate_kind.startswith("memory_"):
        return "Memory review item"
    if candidate_kind.startswith("persona_"):
        return "Persona review item"
    if candidate_kind in {"synthetic_distillation_manifest", "deidentified_style_feature"}:
        return "Distillation review item"
    return "Review item"


def _card_sort_key(card: ReviewWorkspacePresentationCard) -> tuple[int, str, str, str, str, str]:
    return (
        card.urgency_rank,
        card.bundle_id or "",
        card.queue_item_id or "",
        card.candidate_id or "",
        card.decision_id or "",
        card.card_id,
    )


def _validate_non_runtime_flags(
    *,
    review_required: bool,
    preview_only: bool,
    applies_changes: bool,
    writes_memory_store: bool,
    writes_persona_version: bool,
    runtime_ready: bool,
    record_name: str,
) -> None:
    if not review_required:
        raise ValueError(f"{record_name} require review")
    if not preview_only:
        raise ValueError(f"{record_name} are preview-only")
    if applies_changes:
        raise ValueError(f"{record_name} cannot apply changes")
    if writes_memory_store:
        raise ValueError(f"{record_name} cannot write memory stores")
    if writes_persona_version:
        raise ValueError(f"{record_name} cannot write persona versions")
    if runtime_ready:
        raise ValueError(f"{record_name} are never runtime-ready")


def _ordered_unique(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result
