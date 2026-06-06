"""T466 source draft apply-readiness payload contract tests.

The apply-readiness payload is a deterministic synthetic preview. It must not
read private data, call providers, retain raw source content, create
embeddings, extract traits from real content, write stores, apply persona
changes, send messages, connect adapters, or enable media runtime.
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


REQUIRED_FIELD_PATHS = {
    "style.tone",
    "style.pacing",
    "style.humor",
    "relationship.boundary_style",
    "memory.use_preference",
    "growth.short_term_hint",
}

REQUIRED_READINESS_OUTCOMES = {
    "blocked",
    "needs_manual_review",
    "ready_for_future_apply_design",
}

EXPECTED_APPLY_POLICY = {
    "mode": "preview_only",
    "apply_executor_enabled": False,
    "writes_persona_card": False,
    "writes_persona_version_store": False,
    "writes_memory_store": False,
    "writes_review_store": False,
    "writes_runtime_store": False,
    "automatic_apply": False,
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
    "apply_executor_enabled",
    "apply_ready",
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _draft() -> dict[str, Any]:
    return _payload()["source_proposal_persona_draft"]


def _readiness() -> dict[str, Any]:
    return _payload()["source_draft_apply_readiness"]


def _walk(value: Any) -> Iterator[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_adapter_state_includes_source_draft_apply_readiness_payload() -> None:
    readiness = _readiness()

    assert readiness["schema_version"] == "m43.source_draft_apply_readiness.v1"
    assert readiness["readiness_title"]
    assert readiness["source_draft_ref"]["schema_version"] == (
        "m42.source_proposal_persona_draft.v1"
    )
    assert readiness["evaluated_draft_change_ids"]
    assert readiness["field_readiness_records"]
    assert readiness["blocked_condition_records"]
    assert readiness["required_review_gate_refs"]
    assert readiness["rollback_dependency_refs"]
    assert readiness["readiness_outcome_labels"]
    assert readiness["review_required"] is True
    assert readiness["apply_policy"] == EXPECTED_APPLY_POLICY
    assert readiness["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS


def test_field_readiness_records_cover_draft_changes_and_required_outcomes() -> None:
    draft = _draft()
    readiness = _readiness()
    draft_change_by_id = {
        change["draft_change_id"]: change
        for change in draft["draft_field_changes"]
    }
    blocked_condition_ids = {
        condition["blocked_condition_id"]
        for condition in readiness["blocked_condition_records"]
    }
    gate_ids = {
        gate["review_gate_result_id"]
        for gate in draft["review_gate_results"]
    }
    rollback_ids = {ref["rollback_ref_id"] for ref in draft["rollback_refs"]}

    assert set(readiness["evaluated_draft_change_ids"]) == set(draft_change_by_id)
    assert {
        record["persona_field_path"]
        for record in readiness["field_readiness_records"]
    } == REQUIRED_FIELD_PATHS
    assert {
        record["readiness_outcome"]
        for record in readiness["field_readiness_records"]
    } == REQUIRED_READINESS_OUTCOMES

    for record in readiness["field_readiness_records"]:
        draft_change = draft_change_by_id[record["draft_change_id"]]
        assert record["persona_field_path"] == draft_change["persona_field_path"]
        assert record["readiness_record_id"]
        assert record["readiness_outcome"] in REQUIRED_READINESS_OUTCOMES
        assert record["safe_summary"]
        assert set(record["blocking_condition_ids"]).issubset(blocked_condition_ids)
        assert set(record["required_review_gate_result_ids"]).issubset(gate_ids)
        assert record["required_review_gate_result_ids"]
        assert set(record["rollback_ref_ids"]).issubset(rollback_ids)
        assert record["rollback_ref_ids"]
        assert record["future_apply_design_notes"]
        assert record["preview_only"] is True
        assert record["mutation_allowed"] is False
        assert record["review_required"] is True


def test_blocked_conditions_gates_rollbacks_and_outcomes_are_review_safe() -> None:
    readiness = _readiness()

    for condition in readiness["blocked_condition_records"]:
        assert condition["blocked_condition_id"]
        assert condition["condition_code"]
        assert condition["severity"] in {"low", "medium", "high"}
        assert condition["safe_summary"]
        assert condition["affected_draft_change_ids"]
        assert condition["blocks_apply"] is True

    for gate in readiness["required_review_gate_refs"]:
        assert gate["review_gate_result_id"]
        assert gate["gate_code"]
        assert gate["status"] in {"passed", "needs_review", "blocked"}
        assert gate["required_before_apply"] is True

    for rollback in readiness["rollback_dependency_refs"]:
        assert rollback["rollback_ref_id"]
        assert rollback["dependent_draft_change_ids"]
        assert rollback["restore_summary"]
        assert rollback["runtime_rollback_ready"] is False

    assert {label["outcome"] for label in readiness["readiness_outcome_labels"]} == (
        REQUIRED_READINESS_OUTCOMES
    )


def test_non_execution_flags_and_recursive_scan_block_runtime_surfaces() -> None:
    readiness = _readiness()
    serialized = json.dumps(readiness, ensure_ascii=False).lower()

    assert readiness["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS
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

    for value in _walk(readiness):
        if not isinstance(value, dict):
            continue
        for key in UNSAFE_TRUE_KEYS:
            if key in value:
                assert value[key] is False


def test_demo_state_json_route_serves_source_draft_apply_readiness() -> None:
    response = TextFirstWebDemoLocalServer().route(
        "/demo-state.json",
        user_id="source_readiness_synthetic",
    )
    payload = json.loads(response.text)

    assert response.status_code == 200
    assert (
        payload["source_draft_apply_readiness"]["schema_version"]
        == "m43.source_draft_apply_readiness.v1"
    )
    assert payload["source_draft_apply_readiness"]["review_required"] is True
