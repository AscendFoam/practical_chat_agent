"""T436 persona version draft ledger payload contract tests.

All examples are deterministic synthetic fixtures. The ledger must not read
private data, call providers, write stores, apply persona changes, send
messages, connect adapters, or enable media runtime.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

from practical_chat_agent.ui.text_first_web_demo_adapter import (
    TextFirstWebDemoAdapter,
)


REQUIRED_OUTCOMES = {
    "accepted_for_future_apply_review",
    "deferred_needs_more_evidence",
    "rejected_boundary_risk",
}

REQUIRED_CONFLICT_CODES = {
    "persona_drift",
    "boundary_weakening",
    "weak_evidence",
    "overattachment_risk",
    "blocked_source_contamination",
}

EXPECTED_NON_EXECUTION_FLAGS = {
    "local_only": True,
    "synthetic_fixture": True,
    "uses_model_provider": False,
    "reads_private_sources": False,
    "writes_persona_store": False,
    "writes_persona_version_store": False,
    "writes_memory_store": False,
    "writes_review_store": False,
    "writes_runtime_store": False,
    "automatic_apply": False,
    "sends_messages": False,
    "uses_platform_adapter": False,
    "uses_media_runtime": False,
}

UNSAFE_TRUE_KEYS = {
    "mutation_allowed",
    "runtime_rollback_ready",
    "uses_model_provider",
    "reads_private_sources",
    "writes_persona_store",
    "writes_persona_version_store",
    "writes_memory_store",
    "writes_review_store",
    "writes_runtime_store",
    "automatic_apply",
    "sends_messages",
    "uses_platform_adapter",
    "uses_media_runtime",
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _evolution() -> dict[str, Any]:
    return _payload()["persona_evolution_preview"]


def _ledger() -> dict[str, Any]:
    return _payload()["persona_version_draft_ledger"]


def _walk(value: Any) -> Iterator[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_adapter_state_includes_persona_version_draft_ledger_payload() -> None:
    ledger = _ledger()

    assert ledger["schema_version"] == "m38.persona_version_draft_ledger.v1"
    assert ledger["ledger_title"]
    assert ledger["review_required"] is True
    assert ledger["source_evolution_preview_ref"]["schema_version"] == (
        "m37.persona_evolution_preview.v1"
    )
    assert ledger["base_persona_snapshot_ref"]["persona_id"] == "persona_synthetic"
    assert ledger["drafts"]
    assert ledger["conflict_notes"]
    assert ledger["review_outcome_labels"]
    assert ledger["rollback_ref_index"]
    assert ledger["apply_policy"] == {
        "mode": "preview_only",
        "mutation_allowed": False,
        "writes_persona_card": False,
        "writes_persona_version_store": False,
        "writes_memory_store": False,
        "writes_review_store": False,
        "writes_runtime_store": False,
    }
    assert ledger["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS


def test_drafts_reference_evolution_patches_risks_and_rollbacks() -> None:
    evolution = _evolution()
    ledger = _ledger()
    patch_ids = {patch["patch_id"] for patch in evolution["proposed_patch_candidates"]}
    risk_ids = {risk["risk_label_id"] for risk in evolution["risk_labels"]}
    rollback_note_ids = {
        note["rollback_note_id"]
        for note in evolution["rollback_notes"]
    }
    rollback_ref_ids = {
        rollback_ref["rollback_ref_id"]
        for rollback_ref in ledger["rollback_ref_index"]
    }

    assert {draft["reviewer_outcome"] for draft in ledger["drafts"]} == REQUIRED_OUTCOMES
    for draft in ledger["drafts"]:
        assert draft["draft_id"]
        assert draft["draft_kind"]
        assert set(draft["source_patch_ids"]).issubset(patch_ids)
        assert set(draft["excluded_patch_ids"]).issubset(patch_ids)
        assert set(draft["risk_label_ids"]).issubset(risk_ids)
        assert set(draft["rollback_ref_ids"]).issubset(rollback_ref_ids)
        assert draft["before_snapshot_summary"]
        assert draft["after_version_summary"]
        assert draft["conflict_note_ids"]
        assert draft["review_required"] is True
        assert draft["apply_status"] == "preview_only"
        assert draft["mutation_allowed"] is False

    for rollback_ref in ledger["rollback_ref_index"]:
        assert set(rollback_ref["related_patch_ids"]).issubset(patch_ids)
        assert set(rollback_ref["related_m37_rollback_note_ids"]).issubset(
            rollback_note_ids
        )


def test_conflict_notes_cover_required_codes_and_block_auto_apply() -> None:
    ledger = _ledger()
    patch_ids = {
        patch["patch_id"]
        for patch in _evolution()["proposed_patch_candidates"]
    }
    risk_ids = {risk["risk_label_id"] for risk in _evolution()["risk_labels"]}

    assert {note["conflict_code"] for note in ledger["conflict_notes"]} == (
        REQUIRED_CONFLICT_CODES
    )
    for note in ledger["conflict_notes"]:
        assert note["conflict_note_id"]
        assert note["severity"] in {"low", "medium", "high"}
        assert note["safe_summary"]
        assert note["mitigation_summary"]
        assert set(note["related_patch_ids"]).issubset(patch_ids)
        assert set(note["related_risk_label_ids"]).issubset(risk_ids)
        assert note["blocks_auto_apply"] is True


def test_blocked_sources_remain_excluded_from_included_patch_sets() -> None:
    ledger = _ledger()
    rejected = [
        draft
        for draft in ledger["drafts"]
        if draft["reviewer_outcome"] == "rejected_boundary_risk"
    ]

    assert rejected
    for draft in ledger["drafts"]:
        assert set(draft["source_patch_ids"]).isdisjoint(draft["excluded_patch_ids"])
    for draft in rejected:
        assert draft["rejection_reason"]
        assert not draft["source_patch_ids"]
        assert draft["excluded_patch_ids"]


def test_rollback_refs_are_metadata_only_and_draft_linked() -> None:
    ledger = _ledger()
    draft_ids = {draft["draft_id"] for draft in ledger["drafts"]}

    for rollback_ref in ledger["rollback_ref_index"]:
        assert rollback_ref["rollback_ref_id"]
        assert set(rollback_ref["related_draft_ids"]).issubset(draft_ids)
        assert rollback_ref["prior_summary"]
        assert rollback_ref["restore_summary"]
        assert rollback_ref["runtime_rollback_ready"] is False


def test_non_execution_flags_and_recursive_scan_block_runtime_surfaces() -> None:
    ledger = _ledger()
    serialized = json.dumps(ledger, ensure_ascii=False).lower()

    assert ledger["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS
    for forbidden in (
        "private/chat_history",
        "private\\chat_history",
        "raw_text",
        "raw_transcript",
        "private_messages",
        "provider_token",
        "api_key",
        "send_queue",
        "webhook",
        "recipient_id",
        "audio_bytes",
        "image_bytes",
        "video_bytes",
        "generated_audio",
        "generated_image",
        "generated_video",
    ):
        assert forbidden not in serialized

    for value in _walk(ledger):
        if not isinstance(value, dict):
            continue
        for key in UNSAFE_TRUE_KEYS:
            if key in value:
                assert value[key] is False
