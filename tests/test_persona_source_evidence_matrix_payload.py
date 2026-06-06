"""T448 persona source evidence matrix payload contract tests.

All examples are deterministic synthetic fixtures. The matrix must not read
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


REQUIRED_TRAIT_PATHS = {
    "style.tone",
    "style.pacing",
    "style.humor",
    "relationship.boundary_style",
    "memory.use_preference",
    "growth.short_term_hint",
}

REQUIRED_QUALITY_CODES = {
    "strong_synthetic_description",
    "fuzzy_seed",
    "synthetic_dialogue_fixture",
    "blocked_archive_placeholder",
    "blocked_third_party_private_source",
}

REQUIRED_GATE_CODES = {
    "consent",
    "minimization",
    "redaction",
    "uncertainty",
    "anti_deception",
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
    "raw_content_retained",
    "mutation_allowed",
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _manifest() -> dict[str, Any]:
    return _payload()["persona_source_intake_manifest"]


def _matrix() -> dict[str, Any]:
    return _payload()["persona_source_evidence_matrix"]


def _walk(value: Any) -> Iterator[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_adapter_state_includes_persona_source_evidence_matrix_payload() -> None:
    matrix = _matrix()

    assert matrix["schema_version"] == "m40.persona_source_evidence_matrix.v1"
    assert matrix["matrix_title"]
    assert matrix["source_intake_manifest_ref"]["schema_version"] == (
        "m39.persona_source_intake_manifest.v1"
    )
    assert matrix["review_required"] is True
    assert matrix["eligible_source_ids"]
    assert matrix["excluded_source_refs"]
    assert matrix["evidence_rows"]
    assert matrix["trait_hypotheses"]
    assert matrix["quality_labels"]
    assert matrix["review_gate_results"]
    assert matrix["apply_policy"] == {
        "mode": "preview_only",
        "source_files_read": False,
        "raw_content_retained": False,
        "creates_embeddings": False,
        "performs_extraction": False,
        "writes_persona_card": False,
        "writes_persona_version_store": False,
        "writes_memory_store": False,
        "writes_review_store": False,
        "writes_runtime_store": False,
    }
    assert matrix["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS


def test_matrix_links_to_intake_manifest_eligible_and_excluded_sources() -> None:
    manifest = _manifest()
    matrix = _matrix()
    eligible_source_ids = {
        candidate["source_id"]
        for candidate in manifest["source_candidates"]
        if candidate["extraction_eligible"] is True
    }
    ineligible_sources = {
        candidate["source_id"]: candidate
        for candidate in manifest["source_candidates"]
        if candidate["extraction_eligible"] is False
    }

    assert set(matrix["eligible_source_ids"]) == eligible_source_ids
    assert {row["source_id"] for row in matrix["evidence_rows"]}.issubset(
        eligible_source_ids
    )
    assert {ref["source_id"] for ref in matrix["excluded_source_refs"]} == set(
        ineligible_sources
    )
    for ref in matrix["excluded_source_refs"]:
        source = ineligible_sources[ref["source_id"]]
        assert ref["source_kind"] == source["source_kind"]
        assert ref["blocked_reason_ids"] == source["blocked_reason_ids"]
        assert ref["excluded_from_evidence"] is True
        assert ref["raw_content_retained"] is False
        assert ref["mutation_allowed"] is False


def test_evidence_rows_use_eligible_sources_quality_labels_and_review_gates() -> None:
    matrix = _matrix()
    quality_label_ids = {
        label["quality_label_id"]
        for label in matrix["quality_labels"]
    }
    gate_result_ids = {
        gate["review_gate_result_id"]
        for gate in matrix["review_gate_results"]
    }
    eligible_ids = set(matrix["eligible_source_ids"])

    for row in matrix["evidence_rows"]:
        assert row["evidence_row_id"]
        assert row["source_id"] in eligible_ids
        assert row["source_kind"]
        assert row["evidence_kind"]
        assert row["safe_summary"]
        assert row["quality_label_id"] in quality_label_ids
        assert set(row["supports_trait_paths"]).issubset(REQUIRED_TRAIT_PATHS)
        assert row["supports_trait_paths"]
        assert row["uncertainty_notes"]
        assert set(row["review_gate_result_ids"]).issubset(gate_result_ids)
        assert row["raw_content_retained"] is False
        assert row["review_required"] is True


def test_trait_hypotheses_cover_required_paths_and_cite_evidence_rows() -> None:
    matrix = _matrix()
    evidence_ids = {row["evidence_row_id"] for row in matrix["evidence_rows"]}
    gate_result_ids = {
        gate["review_gate_result_id"]
        for gate in matrix["review_gate_results"]
    }

    assert {trait["trait_path"] for trait in matrix["trait_hypotheses"]} == (
        REQUIRED_TRAIT_PATHS
    )
    for trait in matrix["trait_hypotheses"]:
        assert trait["trait_hypothesis_id"]
        assert trait["hypothesis_summary"]
        assert set(trait["supporting_evidence_row_ids"]).issubset(evidence_ids)
        assert trait["supporting_evidence_row_ids"]
        assert set(trait["conflicting_evidence_row_ids"]).issubset(evidence_ids)
        assert trait["confidence_band"] in {"low", "medium", "high"}
        assert trait["uncertainty_summary"]
        assert set(trait["review_gate_result_ids"]).issubset(gate_result_ids)
        assert trait["apply_status"] == "preview_only"
        assert trait["mutation_allowed"] is False


def test_quality_labels_and_review_gate_results_cover_required_codes() -> None:
    matrix = _matrix()

    assert {label["quality_code"] for label in matrix["quality_labels"]} == (
        REQUIRED_QUALITY_CODES
    )
    for label in matrix["quality_labels"]:
        assert label["quality_label_id"]
        assert label["severity"] in {"low", "medium", "high"}
        assert label["safe_summary"]
        assert label["blocks_unreviewed_extraction"] in {True, False}

    assert {gate["gate_code"] for gate in matrix["review_gate_results"]} == (
        REQUIRED_GATE_CODES
    )
    for gate in matrix["review_gate_results"]:
        assert gate["review_gate_result_id"]
        assert gate["status"] in {"passed", "needs_review", "blocked"}
        assert gate["safe_summary"]
        assert gate["blocks_extraction_when_failed"] is True


def test_non_execution_flags_and_recursive_scan_block_runtime_surfaces() -> None:
    matrix = _matrix()
    serialized = json.dumps(matrix, ensure_ascii=False).lower()

    assert matrix["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS
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

    for value in _walk(matrix):
        if not isinstance(value, dict):
            continue
        for key in UNSAFE_TRUE_KEYS:
            if key in value:
                assert value[key] is False


def test_demo_state_json_route_serves_source_evidence_matrix() -> None:
    response = TextFirstWebDemoLocalServer().route(
        "/demo-state.json",
        user_id="source_evidence_synthetic",
    )
    payload = json.loads(response.text)

    assert response.status_code == 200
    assert (
        payload["persona_source_evidence_matrix"]["schema_version"]
        == "m40.persona_source_evidence_matrix.v1"
    )
    assert payload["persona_source_evidence_matrix"]["review_required"] is True
