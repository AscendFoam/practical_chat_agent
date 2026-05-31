"""T384 review workspace snapshot store tests.

All examples are synthetic. These tests do not read private chat history, call
LLMs, apply decisions, mutate stores, write persona versions, synthesize
personas, send messages, or connect to external platforms.
"""

from __future__ import annotations

import importlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from practical_chat_agent.services.review_workspace import (
    ReviewWorkspaceBindingIssue,
    ReviewWorkspaceBundle,
    ReviewWorkspaceCandidateBinding,
)


def _store_module() -> Any:
    try:
        return importlib.import_module("practical_chat_agent.services.review_workspace_store")
    except ModuleNotFoundError as exc:
        pytest.fail(f"review_workspace_store module is missing: {exc}")


def _store(root: Path) -> Any:
    return _store_module().ReviewWorkspaceSnapshotStore(root)


def _candidate_binding(
    *,
    candidate_kind: str = "memory_deletion_cascade",
    candidate_id: str = "memdel_synthetic",
    owner_user_id: str | None = "user_synthetic",
    persona_id: str | None = None,
    priority_band: str = "critical",
    issue: ReviewWorkspaceBindingIssue | None = None,
) -> ReviewWorkspaceCandidateBinding:
    return ReviewWorkspaceCandidateBinding(
        queue_item_id=f"rqitem_{candidate_id}",
        candidate_kind=candidate_kind,
        queue_candidate_id=candidate_id,
        source_candidate_id=candidate_id,
        source_schema_version="synthetic_candidate_v1",
        owner_user_id=owner_user_id,
        persona_id=persona_id,
        safe_summary="[SYNTHETIC] Review workspace binding.",
        reason_labels=["synthetic_reason"],
        source_refs=["synthetic_ref"],
        priority_score=90 if priority_band == "critical" else 55,
        priority_band=priority_band,
        issues=[issue] if issue else [],
    )


def _bundle(
    *,
    bundle_id: str,
    candidate_kind: str = "memory_deletion_cascade",
    candidate_id: str = "memdel_synthetic",
    owner_user_id: str | None = "user_synthetic",
    persona_id: str | None = None,
    priority_band: str = "critical",
    blocked: bool = False,
    created_at: datetime | None = None,
) -> ReviewWorkspaceBundle:
    issue = (
        ReviewWorkspaceBindingIssue(
            issue_code="candidate_id_mismatch",
            severity="blocker",
            safe_summary="[SYNTHETIC] Candidate id mismatch.",
        )
        if blocked
        else None
    )
    return ReviewWorkspaceBundle(
        bundle_id=bundle_id,
        candidate_bindings=[
            _candidate_binding(
                candidate_kind=candidate_kind,
                candidate_id=candidate_id,
                owner_user_id=owner_user_id,
                persona_id=persona_id,
                priority_band=priority_band,
                issue=issue,
            )
        ],
        created_at=created_at or datetime(2026, 5, 31, tzinfo=timezone.utc),
    )


class TestReviewWorkspaceSnapshotStore:
    def test_save_and_load_bundle_preserves_readiness_and_issues(self, tmp_path: Path) -> None:
        store = _store(tmp_path / "snapshots")
        bundle = _bundle(bundle_id="rwbundle_one", blocked=True)

        path = store.save_bundle(bundle)
        loaded = store.load_bundle(bundle.bundle_id)

        assert path.exists()
        assert loaded.bundle_id == bundle.bundle_id
        assert loaded.workspace_ready is False
        assert loaded.blocking_issue_codes == ["candidate_id_mismatch"]

    def test_list_and_filter_bundles_are_deterministic(self, tmp_path: Path) -> None:
        store = _store(tmp_path / "snapshots")
        later = datetime(2026, 5, 31, 1, 0, tzinfo=timezone.utc)
        earlier = datetime(2026, 5, 31, 0, 0, tzinfo=timezone.utc)
        memory_bundle = _bundle(
            bundle_id="rwbundle_memory",
            candidate_kind="memory_deletion_cascade",
            candidate_id="memdel_synthetic",
            owner_user_id="user_synthetic",
            priority_band="critical",
            blocked=True,
            created_at=later,
        )
        persona_bundle = _bundle(
            bundle_id="rwbundle_persona",
            candidate_kind="persona_growth_patch",
            candidate_id="pgpatch_synthetic",
            owner_user_id="user_synthetic",
            persona_id="persona_synthetic",
            priority_band="normal",
            blocked=False,
            created_at=earlier,
        )

        store.save_bundle(memory_bundle)
        store.save_bundle(persona_bundle)

        assert [bundle.bundle_id for bundle in store.list_bundles()] == [
            "rwbundle_persona",
            "rwbundle_memory",
        ]
        assert [bundle.bundle_id for bundle in store.filter_bundles(candidate_kind="persona_growth_patch")] == [
            "rwbundle_persona"
        ]
        assert [bundle.bundle_id for bundle in store.filter_bundles(owner_user_id="user_synthetic")] == [
            "rwbundle_persona",
            "rwbundle_memory",
        ]
        assert [bundle.bundle_id for bundle in store.filter_bundles(persona_id="persona_synthetic")] == [
            "rwbundle_persona"
        ]
        assert [bundle.bundle_id for bundle in store.filter_bundles(priority_band="critical")] == [
            "rwbundle_memory"
        ]
        assert [bundle.bundle_id for bundle in store.filter_bundles(has_blockers=True)] == [
            "rwbundle_memory"
        ]
        assert [bundle.bundle_id for bundle in store.filter_bundles(has_blockers=False)] == [
            "rwbundle_persona"
        ]

    def test_rejects_path_traversal(self, tmp_path: Path) -> None:
        store = _store(tmp_path / "snapshots")
        bundle = _bundle(bundle_id="rwbundle_pathsafe")

        with pytest.raises(ValueError):
            store.save_bundle(bundle, file_name="../escape.json")

        with pytest.raises(ValueError):
            store.load_bundle("../escape")

    def test_serialized_snapshot_contains_no_private_provider_outbound_or_media_fields(
        self,
        tmp_path: Path,
    ) -> None:
        store = _store(tmp_path / "snapshots")
        bundle = _bundle(bundle_id="rwbundle_safe")

        path = store.save_bundle(bundle)
        serialized = path.read_text(encoding="utf-8").lower()

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


class TestReviewWorkspaceSnapshotStoreSafetyBoundaries:
    def test_store_does_not_expose_runtime_or_delivery_methods(self, tmp_path: Path) -> None:
        store = _store(tmp_path / "snapshots")

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
            assert not hasattr(store, method_name)
