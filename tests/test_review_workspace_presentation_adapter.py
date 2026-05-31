"""T389 review workspace presentation adapter tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, apply decisions, mutate stores, write persona versions, synthesize
personas, send messages, or connect to external platforms.
"""

from __future__ import annotations

import importlib
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
from practical_chat_agent.services.review_workspace_export import (
    ReviewWorkspaceSafeExportManifest,
    ReviewWorkspaceSafeExportService,
)


def _adapter_module() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.ui.review_workspace_adapter")
    except ModuleNotFoundError as exc:
        pytest.fail(f"review_workspace_adapter module is missing: {exc}")


def _adapter() -> Any:
    return _adapter_module().ReviewWorkspacePresentationAdapter()


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
        safe_summary=f"[SYNTHETIC] Present {candidate_kind}.",
        reason_labels=["synthetic_review_reason"],
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
        safe_summary=f"[SYNTHETIC] Present {artifact_kind}.",
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
) -> ReviewQueueDecisionRecord:
    return ReviewQueueDecisionRecord(
        decision_id=decision_id,
        item_id=binding.queue_item_id,
        candidate_kind=binding.candidate_kind,
        candidate_id=binding.queue_candidate_id,
        reviewer_id="reviewer_synthetic",
        decision="approve",
    )


def _impact(
    bundle: ReviewWorkspaceBundle,
    binding: ReviewWorkspaceCandidateBinding,
    *,
    decision_id: str,
) -> ReviewDecisionImpactPreview:
    return ReviewDecisionImpactPreviewService().preview_decision(
        bundle,
        _decision(binding, decision_id=decision_id),
    )


def _records() -> tuple[
    ReviewWorkspaceBundle,
    ReviewWorkspaceBundle,
    ReviewDecisionImpactPreview,
    ReviewDecisionImpactPreview,
    ReviewWorkspaceSafeExportManifest,
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
    memory_impact = _impact(memory_bundle, memory_binding, decision_id="rqdec_memory")
    persona_impact = _impact(persona_bundle, persona_binding, decision_id="rqdec_persona")
    export_manifest = ReviewWorkspaceSafeExportService().build_manifest(
        [memory_bundle, persona_bundle],
        impact_previews=[memory_impact, persona_impact],
    )
    return memory_bundle, persona_bundle, memory_impact, persona_impact, export_manifest


class TestReviewWorkspacePresentationAdapter:
    def test_workspace_bundles_produce_safe_presentation_cards(self) -> None:
        memory_bundle, persona_bundle, _, _, _ = _records()

        panel = _adapter().build_panel(bundles=[memory_bundle, persona_bundle])

        workspace_cards = [
            card for card in panel.cards if card.card_kind == "workspace_item"
        ]
        assert len(workspace_cards) == 2
        blocked = workspace_cards[0]
        assert blocked.safe_summary == "[SYNTHETIC] Present memory_deletion_cascade."
        assert blocked.status_badges[0].tone == "blocked"
        assert "memory" in blocked.filter_keys
        assert "blocked" in blocked.filter_keys
        assert blocked.review_required is True
        assert blocked.preview_only is True
        assert blocked.applies_changes is False
        assert blocked.writes_memory_store is False
        assert blocked.writes_persona_version is False
        assert blocked.runtime_ready is False

    def test_decision_impact_previews_produce_outcome_status_badges(self) -> None:
        _, _, memory_impact, persona_impact, _ = _records()

        panel = _adapter().build_panel(
            bundles=[],
            impact_previews=[memory_impact, persona_impact],
        )

        impact_cards = [card for card in panel.cards if card.card_kind == "decision_impact"]
        assert [card.decision_id for card in impact_cards] == [
            "rqdec_memory",
            "rqdec_persona",
        ]
        assert impact_cards[0].status_badges[0].label == "Blocked before apply"
        assert impact_cards[0].status_badges[0].tone == "blocked"
        assert impact_cards[1].status_badges[0].label == "Eligible for later manual apply"
        assert impact_cards[1].status_badges[0].tone == "eligible"

    def test_export_manifest_produces_safe_count_summary(self) -> None:
        _, _, _, _, export_manifest = _records()

        panel = _adapter().build_panel(bundles=[], export_manifest=export_manifest)

        export_cards = [card for card in panel.cards if card.card_kind == "export_summary"]
        assert len(export_cards) == 1
        assert export_cards[0].counts["candidate_kind:memory_deletion_cascade"] == 1
        assert export_cards[0].counts["candidate_kind:persona_growth_patch"] == 1
        assert export_cards[0].counts["blocker:candidate_id_mismatch"] == 2
        assert export_cards[0].status_badges[0].label == "Safe export summary"

    def test_tabs_filters_and_ordering_are_deterministic(self) -> None:
        memory_bundle, persona_bundle, memory_impact, persona_impact, export_manifest = _records()

        panel = _adapter().build_panel(
            bundles=[persona_bundle, memory_bundle],
            impact_previews=[persona_impact, memory_impact],
            export_manifest=export_manifest,
        )

        assert [tab["key"] for tab in panel.filter_tabs] == [
            "all",
            "blocked",
            "eligible",
            "memory",
            "persona",
            "distillation",
        ]
        assert panel.cards[0].filter_keys[:2] == ["all", "blocked"]
        assert panel.cards[0].bundle_id == "rwbundle_b_memory"
        assert panel.cards[-1].card_kind == "export_summary"

    def test_serialized_panel_contains_no_private_provider_outbound_or_media_fields(self) -> None:
        memory_bundle, persona_bundle, memory_impact, persona_impact, export_manifest = _records()
        panel = _adapter().build_panel(
            bundles=[memory_bundle, persona_bundle],
            impact_previews=[memory_impact, persona_impact],
            export_manifest=export_manifest,
        )
        serialized = panel.model_dump_json().lower()

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


class TestReviewWorkspacePresentationAdapterSafetyBoundaries:
    def test_adapter_does_not_expose_runtime_or_delivery_methods(self) -> None:
        adapter = _adapter()

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
            assert not hasattr(adapter, method_name)
