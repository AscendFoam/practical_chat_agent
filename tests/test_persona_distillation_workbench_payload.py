"""T424 persona distillation workbench payload contract tests.

All examples are deterministic synthetic fixtures. The workbench payload must
not read private sources, call providers, write stores, apply traits, send
messages, connect platform adapters, or enable media runtime.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

from practical_chat_agent.ui.text_first_web_demo_adapter import (
    TextFirstWebDemoAdapter,
)


REQUIRED_INPUT_MODES = {
    "detailed_description",
    "fuzzy_seed",
    "synthetic_dialogue_excerpt",
    "random_fictional_seed",
}

REQUIRED_TRAIT_CATEGORIES = {
    "tone",
    "pacing",
    "attachment_style",
    "humor_style",
    "boundary_style",
    "topic_affinity",
    "taboo_pattern",
    "memory_use_preference",
    "growth_hint",
}

REQUIRED_BLOCKED_REQUEST_TYPES = {
    "real_person_clone_or_replacement",
    "deception_or_impersonation",
    "private_import_without_consent",
}

REQUIRED_SAFETY_GATES = {
    "synthetic_only_gate",
    "clone_deception_blocker",
    "private_source_blocker",
    "human_review_gate",
    "non_mutation_gate",
    "outbound_blocker",
}

EXPECTED_NON_EXECUTION_FLAGS = {
    "local_only": True,
    "synthetic_fixture": True,
    "uses_model_provider": False,
    "reads_private_sources": False,
    "writes_runtime_store": False,
    "automatic_apply": False,
    "sends_messages": False,
    "uses_platform_adapter": False,
    "uses_media_runtime": False,
}

UNSAFE_TRUE_KEYS = {
    "private_source_allowed",
    "contains_private_content",
    "real_person_reference",
    "raw_content_retained",
    "raw_private_content_included",
    "mutation_allowed",
    "uses_model_provider",
    "reads_private_sources",
    "writes_runtime_store",
    "automatic_apply",
    "sends_messages",
    "uses_platform_adapter",
    "uses_media_runtime",
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _workbench() -> dict[str, Any]:
    return _payload()["persona_distillation_workbench"]


def _walk(value: Any) -> Iterator[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_adapter_state_includes_persona_distillation_workbench_payload() -> None:
    payload = _payload()
    workbench = payload["persona_distillation_workbench"]

    assert workbench["schema_version"] == "m36.persona_distillation_workbench.v1"
    assert workbench["workbench_title"]
    assert workbench["review_required"] is True
    assert workbench["apply_policy"] == {
        "mode": "preview_only",
        "mutation_allowed": False,
        "writes_persona_card": False,
        "writes_memory_store": False,
        "writes_review_store": False,
    }
    assert workbench["input_modes"]
    assert workbench["synthetic_inputs"]
    assert workbench["evidence_refs"]
    assert workbench["extracted_trait_candidates"]
    assert workbench["blocked_requests"]
    assert workbench["safety_gates"]
    assert workbench["non_execution_flags"]


def test_input_modes_and_synthetic_inputs_cover_supported_sources() -> None:
    workbench = _workbench()
    modes = workbench["input_modes"]
    synthetic_inputs = workbench["synthetic_inputs"]

    assert {mode["mode_id"] for mode in modes} == REQUIRED_INPUT_MODES
    for mode in modes:
        assert mode["label"]
        assert mode["description"]
        assert mode["source_policy"]
        assert mode["accepted_fixture_kind"] == "synthetic"
        assert mode["requires_review"] is True
        assert mode["private_source_allowed"] is False

    assert REQUIRED_INPUT_MODES.issubset(
        {synthetic_input["mode_id"] for synthetic_input in synthetic_inputs}
    )
    for synthetic_input in synthetic_inputs:
        assert synthetic_input["input_id"]
        assert synthetic_input["mode_id"] in REQUIRED_INPUT_MODES
        assert synthetic_input["fixture_label"]
        assert synthetic_input["safe_summary"]
        assert synthetic_input["detail_level"] in {"high", "medium", "low"}
        assert synthetic_input["contains_private_content"] is False
        assert synthetic_input["real_person_reference"] is False
        assert synthetic_input["raw_content_retained"] is False


def test_trait_candidates_use_safe_evidence_and_preview_only_status() -> None:
    workbench = _workbench()
    evidence_by_id = {
        evidence["evidence_id"]: evidence for evidence in workbench["evidence_refs"]
    }
    synthetic_inputs_by_id = {
        synthetic_input["input_id"]: synthetic_input
        for synthetic_input in workbench["synthetic_inputs"]
    }
    candidates = workbench["extracted_trait_candidates"]

    assert {candidate["category"] for candidate in candidates} == REQUIRED_TRAIT_CATEGORIES
    for evidence in evidence_by_id.values():
        assert evidence["source_input_id"] in synthetic_inputs_by_id
        assert evidence["source_mode_id"] in REQUIRED_INPUT_MODES
        assert evidence["source_kind"] == "synthetic_fixture"
        assert evidence["safe_summary"]
        assert evidence["raw_private_content_included"] is False

    for candidate in candidates:
        assert candidate["trait_id"]
        assert candidate["candidate_value"]
        assert candidate["confidence_band"] in {"low", "medium", "high"}
        assert candidate["evidence_ref_ids"]
        assert set(candidate["evidence_ref_ids"]).issubset(evidence_by_id)
        assert candidate["safe_summary"]
        assert candidate["review_status"] == "needs_review"
        assert candidate["apply_status"] == "preview_only"
        assert candidate["mutation_allowed"] is False


def test_blocked_requests_capture_clone_deception_and_private_import_risks() -> None:
    workbench = _workbench()
    blocked_requests = workbench["blocked_requests"]

    assert {item["request_type"] for item in blocked_requests} == REQUIRED_BLOCKED_REQUEST_TYPES
    for item in blocked_requests:
        assert item["blocked_request_id"]
        assert item["risk_reason"]
        assert item["safe_summary"]
        assert item["user_facing_explanation"]
        assert item["source_mode_id"] in REQUIRED_INPUT_MODES
        assert item["status"] == "blocked"
        assert item["raw_private_content_included"] is False
        assert item["mutation_allowed"] is False


def test_safety_gates_and_non_execution_flags_are_explicit() -> None:
    workbench = _workbench()
    gates = workbench["safety_gates"]

    assert {gate["gate_id"] for gate in gates} == REQUIRED_SAFETY_GATES
    for gate in gates:
        assert gate["enabled"] is True
        assert gate["label"]
        assert gate["safe_summary"]

    assert workbench["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS


def test_workbench_payload_has_no_unsafe_true_states_or_private_surfaces() -> None:
    workbench = _workbench()
    serialized = json.dumps(workbench, ensure_ascii=False).lower()

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

    for value in _walk(workbench):
        if not isinstance(value, dict):
            continue
        for key in UNSAFE_TRUE_KEYS:
            if key in value:
                assert value[key] is False
