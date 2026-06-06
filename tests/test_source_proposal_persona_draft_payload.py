"""T460 source proposal persona draft payload contract tests.

The draft payload is a deterministic synthetic preview. It must not read
private data, call providers, retain raw source content, create embeddings,
extract traits from real content, write stores, apply persona changes, send
messages, connect adapters, or enable media runtime.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

from practical_chat_agent.ui.text_first_web_demo_adapter import (
    TextFirstWebDemoAdapter,
)
from practical_chat_agent.ui.text_first_web_demo_local_server import (
    TextFirstWebDemoLocalServer,
)


REQUIRED_DRAFT_FIELD_PATHS = {
    "style.tone",
    "style.pacing",
    "style.humor",
    "relationship.boundary_style",
    "memory.use_preference",
    "growth.short_term_hint",
}

EXPECTED_NON_EXECUTION_FLAGS = {
    "local_only": True,
    "synthetic_fixture": True,
    "uses_model_provider": False,
    "reads_private_sources": False,
    "retains_raw_source_content": False,
    "creates_embeddings": False,
    "performs_extraction": False,
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
    "uses_model_provider",
    "reads_private_sources",
    "retains_raw_source_content",
    "creates_embeddings",
    "performs_extraction",
    "writes_persona_store",
    "writes_persona_version_store",
    "writes_memory_store",
    "writes_review_store",
    "writes_runtime_store",
    "automatic_apply",
    "sends_messages",
    "uses_platform_adapter",
    "uses_media_runtime",
    "mutation_allowed",
    "draft_apply_allowed",
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _proposal() -> dict[str, Any]:
    return _payload()["source_evidence_persona_proposal"]


def _draft() -> dict[str, Any]:
    return _payload()["source_proposal_persona_draft"]


def _walk(value: Any) -> Iterator[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_adapter_state_includes_source_proposal_persona_draft_payload() -> None:
    draft = _draft()

    assert draft["schema_version"] == "m42.source_proposal_persona_draft.v1"
    assert draft["draft_title"]
    assert draft["source_proposal_ref"]["schema_version"] == (
        "m41.source_evidence_persona_proposal.v1"
    )
    assert draft["base_persona_snapshot"]
    assert draft["selected_proposal_ids"]
    assert draft["draft_field_changes"]
    assert draft["unchanged_field_summaries"]
    assert draft["conflict_notes"]
    assert draft["rollback_refs"]
    assert draft["review_gate_results"]
    assert draft["draft_outcome_labels"]
    assert draft["review_required"] is True
    assert draft["apply_policy"] == {
        "mode": "preview_only",
        "writes_persona_card": False,
        "writes_persona_version_store": False,
        "writes_memory_store": False,
        "writes_review_store": False,
        "writes_runtime_store": False,
        "automatic_apply": False,
    }
    assert draft["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS


def test_draft_field_changes_cover_required_paths_and_cite_m41_proposals() -> None:
    proposal = _proposal()
    draft = _draft()
    proposal_by_id = {
        candidate["proposal_id"]: candidate
        for candidate in proposal["proposal_candidates"]
    }
    conflict_ids = {note["conflict_note_id"] for note in draft["conflict_notes"]}
    rollback_ids = {ref["rollback_ref_id"] for ref in draft["rollback_refs"]}
    gate_ids = {gate["review_gate_result_id"] for gate in draft["review_gate_results"]}

    assert set(draft["selected_proposal_ids"]).issubset(proposal_by_id)
    assert {
        change["persona_field_path"]
        for change in draft["draft_field_changes"]
    } == REQUIRED_DRAFT_FIELD_PATHS

    for change in draft["draft_field_changes"]:
        assert change["draft_change_id"]
        assert change["before_summary"]
        assert change["after_summary"]
        assert set(change["source_proposal_ids"]).issubset(proposal_by_id)
        assert change["source_proposal_ids"]
        source_candidate = proposal_by_id[change["source_proposal_ids"][0]]
        assert change["persona_field_path"] == source_candidate["persona_field_path"]
        assert change["source_trait_hypothesis_ids"] == source_candidate["source_trait_hypothesis_ids"]
        assert change["supporting_evidence_row_ids"] == source_candidate["supporting_evidence_row_ids"]
        assert change["confidence_band"] == source_candidate["confidence_band"]
        assert change["risk_label_ids"] == source_candidate["risk_label_ids"]
        assert set(change["conflict_note_ids"]).issubset(conflict_ids)
        assert change["conflict_note_ids"]
        assert set(change["rollback_ref_ids"]).issubset(rollback_ids)
        assert change["rollback_ref_ids"]
        assert set(change["review_gate_result_ids"]).issubset(gate_ids)
        assert change["review_gate_result_ids"]
        assert change["draft_status"] == "preview_only"
        assert change["mutation_allowed"] is False
        assert change["review_required"] is True


def test_conflict_rollback_gate_and_outcome_labels_are_review_safe() -> None:
    draft = _draft()

    for note in draft["conflict_notes"]:
        assert note["conflict_note_id"]
        assert note["conflict_code"]
        assert note["severity"] in {"low", "medium", "high"}
        assert note["safe_summary"]
        assert note["blocks_auto_apply"] is True

    for ref in draft["rollback_refs"]:
        assert ref["rollback_ref_id"]
        assert ref["safe_summary"]
        assert ref["restore_summary"]
        assert ref["runtime_rollback_ready"] is False

    for gate in draft["review_gate_results"]:
        assert gate["review_gate_result_id"]
        assert gate["gate_code"]
        assert gate["status"] in {"passed", "needs_review", "blocked"}
        assert gate["safe_summary"]
        assert gate["blocks_apply_when_failed"] is True

    assert {label["outcome"] for label in draft["draft_outcome_labels"]} == {
        "needs_manual_review",
        "blocked_by_policy",
        "ready_for_future_apply_design",
    }


def test_non_execution_flags_and_recursive_scan_block_runtime_surfaces() -> None:
    draft = _draft()
    serialized = json.dumps(draft, ensure_ascii=False).lower()

    assert draft["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS
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

    for value in _walk(draft):
        if not isinstance(value, dict):
            continue
        for key in UNSAFE_TRUE_KEYS:
            if key in value:
                assert value[key] is False


def test_demo_state_json_route_serves_source_proposal_persona_draft() -> None:
    response = TextFirstWebDemoLocalServer().route(
        "/demo-state.json",
        user_id="source_draft_synthetic",
    )
    payload = json.loads(response.text)

    assert response.status_code == 200
    assert (
        payload["source_proposal_persona_draft"]["schema_version"]
        == "m42.source_proposal_persona_draft.v1"
    )
    assert payload["source_proposal_persona_draft"]["review_required"] is True
