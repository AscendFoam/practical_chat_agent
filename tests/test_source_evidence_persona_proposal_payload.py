"""T454 source evidence persona proposal payload contract tests.

The proposal payload is a deterministic synthetic preview. It must not read
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


REQUIRED_PERSONA_FIELD_PATHS = {
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
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _matrix() -> dict[str, Any]:
    return _payload()["persona_source_evidence_matrix"]


def _proposal() -> dict[str, Any]:
    return _payload()["source_evidence_persona_proposal"]


def _walk(value: Any) -> Iterator[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_adapter_state_includes_source_evidence_persona_proposal_payload() -> None:
    proposal = _proposal()

    assert proposal["schema_version"] == "m41.source_evidence_persona_proposal.v1"
    assert proposal["proposal_title"]
    assert proposal["source_evidence_matrix_ref"]["schema_version"] == (
        "m40.persona_source_evidence_matrix.v1"
    )
    assert proposal["review_required"] is True
    assert proposal["proposal_candidates"]
    assert proposal["risk_labels"]
    assert proposal["rollback_notes"]
    assert proposal["review_gate_results"]
    assert proposal["proposal_outcome_labels"]
    assert proposal["apply_policy"] == {
        "mode": "preview_only",
        "writes_persona_card": False,
        "writes_persona_version_store": False,
        "writes_memory_store": False,
        "writes_review_store": False,
        "writes_runtime_store": False,
        "automatic_apply": False,
    }
    assert proposal["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS


def test_proposal_candidates_cover_required_paths_and_cite_m40_evidence() -> None:
    matrix = _matrix()
    proposal = _proposal()
    trait_ids = {
        trait["trait_hypothesis_id"]
        for trait in matrix["trait_hypotheses"]
    }
    evidence_ids = {
        row["evidence_row_id"]
        for row in matrix["evidence_rows"]
    }
    risk_ids = {risk["risk_label_id"] for risk in proposal["risk_labels"]}
    rollback_ids = {note["rollback_note_id"] for note in proposal["rollback_notes"]}
    gate_ids = {gate["review_gate_result_id"] for gate in proposal["review_gate_results"]}

    assert {
        candidate["persona_field_path"]
        for candidate in proposal["proposal_candidates"]
    } == REQUIRED_PERSONA_FIELD_PATHS
    for candidate in proposal["proposal_candidates"]:
        assert candidate["proposal_id"]
        assert candidate["proposed_value_summary"]
        assert candidate["rationale_summary"]
        assert set(candidate["source_trait_hypothesis_ids"]).issubset(trait_ids)
        assert candidate["source_trait_hypothesis_ids"]
        assert set(candidate["supporting_evidence_row_ids"]).issubset(evidence_ids)
        assert candidate["supporting_evidence_row_ids"]
        assert candidate["confidence_band"] in {"low", "medium", "high"}
        assert set(candidate["risk_label_ids"]).issubset(risk_ids)
        assert candidate["risk_label_ids"]
        assert set(candidate["rollback_note_ids"]).issubset(rollback_ids)
        assert candidate["rollback_note_ids"]
        assert set(candidate["review_gate_result_ids"]).issubset(gate_ids)
        assert candidate["review_gate_result_ids"]
        assert candidate["proposal_status"] == "preview_only"
        assert candidate["mutation_allowed"] is False
        assert candidate["review_required"] is True


def test_risk_rollback_gate_and_outcome_labels_are_review_safe() -> None:
    proposal = _proposal()

    for risk in proposal["risk_labels"]:
        assert risk["risk_label_id"]
        assert risk["risk_code"]
        assert risk["severity"] in {"low", "medium", "high"}
        assert risk["safe_summary"]
        assert risk["blocks_auto_apply"] is True

    for note in proposal["rollback_notes"]:
        assert note["rollback_note_id"]
        assert note["safe_summary"]
        assert note["restore_summary"]
        assert note["runtime_rollback_ready"] is False

    for gate in proposal["review_gate_results"]:
        assert gate["review_gate_result_id"]
        assert gate["gate_code"]
        assert gate["status"] in {"passed", "needs_review", "blocked"}
        assert gate["safe_summary"]
        assert gate["blocks_apply_when_failed"] is True

    assert {label["outcome"] for label in proposal["proposal_outcome_labels"]} == {
        "needs_manual_review",
        "blocked_by_policy",
        "ready_for_future_apply_design",
    }


def test_non_execution_flags_and_recursive_scan_block_runtime_surfaces() -> None:
    proposal = _proposal()
    serialized = json.dumps(proposal, ensure_ascii=False).lower()

    assert proposal["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS
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

    for value in _walk(proposal):
        if not isinstance(value, dict):
            continue
        for key in UNSAFE_TRUE_KEYS:
            if key in value:
                assert value[key] is False


def test_demo_state_json_route_serves_source_evidence_persona_proposal() -> None:
    response = TextFirstWebDemoLocalServer().route(
        "/demo-state.json",
        user_id="source_proposal_synthetic",
    )
    payload = json.loads(response.text)

    assert response.status_code == 200
    assert (
        payload["source_evidence_persona_proposal"]["schema_version"]
        == "m41.source_evidence_persona_proposal.v1"
    )
    assert payload["source_evidence_persona_proposal"]["review_required"] is True
