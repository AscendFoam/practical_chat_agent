"""T430 persona evolution preview payload contract tests.

All examples are deterministic synthetic fixtures. The evolution preview must
not read private data, call providers, write stores, apply persona changes,
send messages, connect adapters, or enable media runtime.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

from practical_chat_agent.ui.text_first_web_demo_adapter import (
    TextFirstWebDemoAdapter,
)


REQUIRED_CHANGED_FIELD_PATHS = {
    "style.tone",
    "style.pacing",
    "style.humor",
    "relationship.boundary_style",
    "memory.use_preference",
    "growth.short_term_hint",
}

REQUIRED_RISK_CODES = {
    "persona_drift",
    "overattachment_risk",
    "unclear_evidence",
    "boundary_weakening",
    "blocked_source_excluded",
}

EXPECTED_NON_EXECUTION_FLAGS = {
    "local_only": True,
    "synthetic_fixture": True,
    "uses_model_provider": False,
    "reads_private_sources": False,
    "writes_persona_store": False,
    "writes_memory_store": False,
    "writes_review_store": False,
    "writes_runtime_store": False,
    "automatic_apply": False,
    "sends_messages": False,
    "uses_platform_adapter": False,
    "uses_media_runtime": False,
}

UNSAFE_TRUE_KEYS = {
    "real_person_claim",
    "mutation_allowed",
    "runtime_rollback_ready",
    "uses_model_provider",
    "reads_private_sources",
    "writes_persona_store",
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


def _workbench() -> dict[str, Any]:
    return _payload()["persona_distillation_workbench"]


def _evolution() -> dict[str, Any]:
    return _payload()["persona_evolution_preview"]


def _walk(value: Any) -> Iterator[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_adapter_state_includes_persona_evolution_preview_payload() -> None:
    payload = _payload()
    preview = payload["persona_evolution_preview"]

    assert preview["schema_version"] == "m37.persona_evolution_preview.v1"
    assert preview["preview_title"]
    assert preview["review_required"] is True
    assert preview["apply_policy"] == {
        "mode": "preview_only",
        "mutation_allowed": False,
        "writes_persona_card": False,
        "writes_persona_version_store": False,
        "writes_memory_store": False,
        "writes_review_store": False,
        "writes_runtime_store": False,
    }
    assert preview["source_workbench_ref"]["schema_version"] == (
        "m36.persona_distillation_workbench.v1"
    )
    assert preview["source_trait_candidate_ids"]
    assert preview["persona_snapshot_before"]
    assert preview["proposed_patch_candidates"]
    assert preview["blocked_source_exclusions"]
    assert preview["risk_labels"]
    assert preview["rollback_notes"]
    assert preview["non_execution_flags"]


def test_source_refs_use_only_workbench_trait_candidates_and_evidence() -> None:
    workbench = _workbench()
    preview = _evolution()
    trait_ids = {
        candidate["trait_id"]
        for candidate in workbench["extracted_trait_candidates"]
    }
    evidence_ids = {
        evidence["evidence_id"]
        for evidence in workbench["evidence_refs"]
    }

    assert set(preview["source_trait_candidate_ids"]).issubset(trait_ids)
    for patch in preview["proposed_patch_candidates"]:
        assert set(patch["source_trait_candidate_ids"]).issubset(trait_ids)
        assert set(patch["evidence_ref_ids"]).issubset(evidence_ids)


def test_persona_snapshot_before_is_synthetic_and_non_runtime() -> None:
    snapshot = _evolution()["persona_snapshot_before"]

    assert snapshot["persona_id"] == "persona_synthetic"
    assert snapshot["display_name"]
    assert snapshot["ai_identity_disclosure"]
    assert snapshot["current_trait_summaries"]
    assert snapshot["current_boundary_summary"]
    assert snapshot["current_memory_use_summary"]
    assert snapshot["source_label"] == "synthetic_fixture"
    assert snapshot["real_person_claim"] is False
    assert snapshot["runtime_state_ref"] == "none"


def test_patch_candidates_cover_required_paths_and_are_preview_only() -> None:
    preview = _evolution()
    risk_ids = {risk["risk_label_id"] for risk in preview["risk_labels"]}
    rollback_ids = {note["rollback_note_id"] for note in preview["rollback_notes"]}
    patches = preview["proposed_patch_candidates"]

    assert {patch["changed_field_path"] for patch in patches} == REQUIRED_CHANGED_FIELD_PATHS
    for patch in patches:
        assert patch["patch_id"]
        assert patch["patch_kind"]
        assert patch["source_trait_candidate_ids"]
        assert patch["before_summary"]
        assert patch["after_summary"]
        assert patch["rationale_summary"]
        assert patch["confidence_band"] in {"low", "medium", "high"}
        assert patch["evidence_ref_ids"]
        assert set(patch["risk_label_ids"]).issubset(risk_ids)
        assert set(patch["rollback_note_ids"]).issubset(rollback_ids)
        assert patch["review_status"] == "needs_review"
        assert patch["apply_status"] == "preview_only"
        assert patch["mutation_allowed"] is False


def test_risk_labels_and_rollback_notes_are_linked_and_non_executing() -> None:
    preview = _evolution()
    patch_ids = {patch["patch_id"] for patch in preview["proposed_patch_candidates"]}

    assert {risk["risk_code"] for risk in preview["risk_labels"]} == REQUIRED_RISK_CODES
    for risk in preview["risk_labels"]:
        assert risk["severity"] in {"low", "medium", "high"}
        assert risk["safe_summary"]
        assert risk["mitigation_summary"]
        assert risk["blocks_auto_apply"] is True

    for note in preview["rollback_notes"]:
        assert note["rollback_note_id"]
        assert set(note["target_patch_ids"]).issubset(patch_ids)
        assert note["prior_summary"]
        assert note["rollback_summary"]
        assert note["required_reviewer_action"]
        assert note["runtime_rollback_ready"] is False


def test_blocked_workbench_requests_are_excluded_from_patch_generation() -> None:
    workbench = _workbench()
    preview = _evolution()
    blocked_ids = {
        request["blocked_request_id"]
        for request in workbench["blocked_requests"]
    }
    patch_source_ids = {
        source_id
        for patch in preview["proposed_patch_candidates"]
        for source_id in patch["source_trait_candidate_ids"]
    }

    assert {
        exclusion["blocked_request_id"]
        for exclusion in preview["blocked_source_exclusions"]
    } == blocked_ids
    assert patch_source_ids.isdisjoint(blocked_ids)
    for exclusion in preview["blocked_source_exclusions"]:
        assert exclusion["request_type"]
        assert exclusion["exclusion_reason"]
        assert exclusion["safe_summary"]
        assert exclusion["excluded_from_patch_generation"] is True
        assert exclusion["mutation_allowed"] is False


def test_non_execution_flags_and_recursive_scan_block_runtime_surfaces() -> None:
    preview = _evolution()
    serialized = json.dumps(preview, ensure_ascii=False).lower()

    assert preview["non_execution_flags"] == EXPECTED_NON_EXECUTION_FLAGS
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

    for value in _walk(preview):
        if not isinstance(value, dict):
            continue
        for key in UNSAFE_TRUE_KEYS:
            if key in value:
                assert value[key] is False
