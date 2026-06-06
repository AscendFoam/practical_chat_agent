"""T442 persona source intake manifest payload contract tests.

All examples are deterministic synthetic fixtures. The manifest must not read
private data, call providers, retain raw source content, create embeddings,
extract traits, write stores, apply persona changes, send messages, connect
adapters, or enable media runtime.
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


REQUIRED_SOURCE_KINDS = {
    "detailed_description",
    "fuzzy_seed",
    "synthetic_dialogue_excerpt",
    "user_provided_archive_placeholder",
    "third_party_private_source_placeholder",
}

REQUIRED_GATE_CODES = {
    "explicit_consent_required",
    "private_source_minimization_required",
    "real_person_replacement_blocked",
    "deception_blocked",
    "sensitive_data_redaction_required",
    "reviewer_approval_required",
}

REQUIRED_BLOCKED_CODES = {
    "represented_person_consent_missing",
    "third_party_private_chat_material",
    "deceptive_replacement_request",
    "sensitive_data_not_redacted",
    "undisclosed_real_person_impersonation",
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
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _manifest() -> dict[str, Any]:
    return _payload()["persona_source_intake_manifest"]


def _walk(value: Any) -> Iterator[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_adapter_state_includes_persona_source_intake_manifest_payload() -> None:
    manifest = _manifest()

    assert manifest["schema_version"] == "m39.persona_source_intake_manifest.v1"
    assert manifest["manifest_title"]
    assert manifest["review_required"] is True
    assert manifest["source_candidates"]
    assert manifest["source_policy_gates"]
    assert manifest["blocked_source_categories"]
    assert manifest["redaction_profiles"]
    assert manifest["apply_policy"] == {
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
        "reviewer_approval_required_before_future_extraction": True,
    }
    assert manifest["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS


def test_source_candidates_have_consent_minimization_redaction_and_gate_metadata() -> None:
    manifest = _manifest()
    source_candidates = manifest["source_candidates"]
    redaction_profile_ids = {
        profile["redaction_profile_id"]
        for profile in manifest["redaction_profiles"]
    }
    gate_ids = {gate["gate_id"] for gate in manifest["source_policy_gates"]}
    blocked_reason_ids = {
        category["blocked_reason_id"]
        for category in manifest["blocked_source_categories"]
    }

    assert {candidate["source_kind"] for candidate in source_candidates} == (
        REQUIRED_SOURCE_KINDS
    )
    assert sum(1 for candidate in source_candidates if not candidate["extraction_eligible"]) >= 2

    for candidate in source_candidates:
        assert candidate["source_id"]
        assert candidate["fixture_label"]
        assert candidate["declared_owner"]
        assert candidate["consent_status"]
        assert candidate["minimization_status"]
        assert candidate["redaction_profile_id"] in redaction_profile_ids
        assert candidate["safe_summary"]
        assert candidate["raw_content_retained"] is False
        assert set(candidate["review_gate_ids"]).issubset(gate_ids)
        assert set(candidate["blocked_reason_ids"]).issubset(blocked_reason_ids)
        assert candidate["review_required"] is True
        if not candidate["extraction_eligible"]:
            assert candidate["blocked_reason_ids"]


def test_policy_gates_block_failed_extraction_and_cover_required_codes() -> None:
    manifest = _manifest()

    assert {gate["gate_code"] for gate in manifest["source_policy_gates"]} == (
        REQUIRED_GATE_CODES
    )
    for gate in manifest["source_policy_gates"]:
        assert gate["gate_id"]
        assert gate["enabled"] is True
        assert gate["safe_summary"]
        assert gate["blocks_extraction_when_failed"] is True


def test_blocked_categories_and_redaction_profiles_are_explicit_review_artifacts() -> None:
    manifest = _manifest()

    assert {
        category["blocked_code"]
        for category in manifest["blocked_source_categories"]
    } == REQUIRED_BLOCKED_CODES
    for category in manifest["blocked_source_categories"]:
        assert category["blocked_reason_id"]
        assert category["severity"] in {"medium", "high"}
        assert category["safe_summary"]
        assert category["blocks_extraction"] is True

    redaction_profiles = manifest["redaction_profiles"]
    assert len(redaction_profiles) >= 4
    for profile in redaction_profiles:
        assert profile["redaction_profile_id"]
        assert profile["profile_label"]
        assert profile["redaction_status"]
        assert profile["safe_summary"]
        assert profile["retains_raw_content"] is False
        assert profile["requires_review"] is True


def test_non_execution_flags_and_recursive_scan_block_runtime_surfaces() -> None:
    manifest = _manifest()
    serialized = json.dumps(manifest, ensure_ascii=False).lower()

    assert manifest["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS
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

    for value in _walk(manifest):
        if not isinstance(value, dict):
            continue
        for key in UNSAFE_TRUE_KEYS:
            if key in value:
                assert value[key] is False


def test_demo_state_json_route_serves_source_intake_manifest() -> None:
    response = TextFirstWebDemoLocalServer().route(
        "/demo-state.json",
        user_id="source_intake_synthetic",
    )
    payload = json.loads(response.text)

    assert response.status_code == 200
    assert (
        payload["persona_source_intake_manifest"]["schema_version"]
        == "m39.persona_source_intake_manifest.v1"
    )
    assert payload["persona_source_intake_manifest"]["review_required"] is True
