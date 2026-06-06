"""T468 source draft apply-readiness Review Workspace linkage tests.

All readiness review cards are deterministic synthetic previews. They must not
read private data, call providers, retain raw source content, extract traits,
write stores, apply persona changes, send messages, connect adapters, or
enable media runtime.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from practical_chat_agent.ui.text_first_web_demo_adapter import (
    TextFirstWebDemoAdapter,
)
from practical_chat_agent.ui.text_first_web_demo_static import (
    TextFirstWebDemoStaticShell,
)


UNSAFE_TRUE_KEYS = {
    "changes_state",
    "mutation_allowed",
    "automatic_apply",
    "sends_messages",
    "runtime_ready",
    "runtime_rollback_ready",
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
    "uses_platform_adapter",
    "uses_media_runtime",
    "apply_executor_enabled",
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _review_workspace() -> dict[str, Any]:
    return _payload()["review_workspace"]


def _readiness() -> dict[str, Any]:
    return _payload()["source_draft_apply_readiness"]


def _assets() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _asset_text(name: str) -> str:
    return Path(_assets()[name]).read_text(encoding="utf-8")


def _walk(value: Any) -> Iterator[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_review_workspace_includes_source_readiness_review_cards() -> None:
    review = _review_workspace()
    readiness = _readiness()
    cards = review["source_readiness_review_cards"]
    expected_count = (
        len(readiness["field_readiness_records"])
        + len(readiness["blocked_condition_records"])
        + len(readiness["required_review_gate_refs"])
        + len(readiness["rollback_dependency_refs"])
        + len(readiness["readiness_outcome_labels"])
    )
    readiness_tab = next(tab for tab in review["filter_tabs"] if tab["key"] == "readiness")

    assert len(cards) == expected_count
    assert readiness_tab["count"] == len(cards)
    assert all(
        card["schema_version"] == "review_workspace_source_draft_apply_readiness_card_v1"
        for card in cards
    )
    assert all(card["source_surface"] == "source_draft_apply_readiness" for card in cards)
    assert all("readiness" in card["filter_keys"] for card in cards)
    assert {card["card_kind"] for card in cards} == {
        "source_readiness_field_record_review",
        "source_readiness_blocked_condition_review",
        "source_readiness_gate_ref_review",
        "source_readiness_rollback_dependency_review",
        "source_readiness_outcome_review",
    }


def test_readiness_field_record_cards_preserve_safe_metadata() -> None:
    readiness = _readiness()
    cards = _review_workspace()["source_readiness_review_cards"]
    record_by_id = {
        record["readiness_record_id"]: record
        for record in readiness["field_readiness_records"]
    }
    field_cards = [
        card for card in cards if card["card_kind"] == "source_readiness_field_record_review"
    ]

    assert len(field_cards) == len(record_by_id)
    for card in field_cards:
        record = record_by_id[card["readiness_record_id"]]
        assert card["draft_change_id"] == record["draft_change_id"]
        assert card["persona_field_path"] == record["persona_field_path"]
        assert card["readiness_outcome"] == record["readiness_outcome"]
        assert card["safe_summary"] == record["safe_summary"]
        assert card["blocking_condition_ids"] == record["blocking_condition_ids"]
        assert card["required_review_gate_result_ids"] == record["required_review_gate_result_ids"]
        assert card["rollback_ref_ids"] == record["rollback_ref_ids"]
        assert card["future_apply_design_notes"] == record["future_apply_design_notes"]
        assert card["preview_only"] is True
        assert card["mutation_allowed"] is False
        assert card["review_required"] is True


def test_readiness_support_cards_preserve_safe_metadata() -> None:
    readiness = _readiness()
    cards = _review_workspace()["source_readiness_review_cards"]
    condition_by_id = {
        condition["blocked_condition_id"]: condition
        for condition in readiness["blocked_condition_records"]
    }
    gate_by_id = {
        gate["review_gate_result_id"]: gate
        for gate in readiness["required_review_gate_refs"]
    }
    rollback_by_id = {
        rollback["rollback_ref_id"]: rollback
        for rollback in readiness["rollback_dependency_refs"]
    }
    outcome_by_id = {
        label["outcome_label_id"]: label
        for label in readiness["readiness_outcome_labels"]
    }

    condition_cards = [card for card in cards if card["card_kind"] == "source_readiness_blocked_condition_review"]
    gate_cards = [card for card in cards if card["card_kind"] == "source_readiness_gate_ref_review"]
    rollback_cards = [card for card in cards if card["card_kind"] == "source_readiness_rollback_dependency_review"]
    outcome_cards = [card for card in cards if card["card_kind"] == "source_readiness_outcome_review"]

    assert len(condition_cards) == len(condition_by_id)
    assert len(gate_cards) == len(gate_by_id)
    assert len(rollback_cards) == len(rollback_by_id)
    assert len(outcome_cards) == len(outcome_by_id)

    for card in condition_cards:
        condition = condition_by_id[card["blocked_condition_id"]]
        assert card["condition_code"] == condition["condition_code"]
        assert card["severity"] == condition["severity"]
        assert card["affected_draft_change_ids"] == condition["affected_draft_change_ids"]
        assert card["blocks_apply"] is True

    for card in gate_cards:
        gate = gate_by_id[card["review_gate_result_id"]]
        assert card["gate_code"] == gate["gate_code"]
        assert card["status"] == gate["status"]
        assert card["required_before_apply"] is True

    for card in rollback_cards:
        rollback = rollback_by_id[card["rollback_ref_id"]]
        assert card["dependent_draft_change_ids"] == rollback["dependent_draft_change_ids"]
        assert card["restore_summary"] == rollback["restore_summary"]
        assert card["runtime_rollback_ready"] is False

    for card in outcome_cards:
        outcome = outcome_by_id[card["outcome_label_id"]]
        assert card["outcome"] == outcome["outcome"]
        assert card["safe_summary"] == outcome["safe_summary"]


def test_source_readiness_review_cards_have_no_unsafe_true_states_or_private_surfaces() -> None:
    cards = _review_workspace()["source_readiness_review_cards"]
    serialized = json.dumps(cards, ensure_ascii=False).lower()

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

    for value in _walk(cards):
        if not isinstance(value, dict):
            continue
        for key in UNSAFE_TRUE_KEYS:
            if key in value:
                assert value[key] is False


def test_static_fallback_includes_source_readiness_review_cards_and_renderer_details() -> None:
    js = _asset_text("js")

    assert "source_readiness_review_cards" in js
    assert '{ key: "readiness", label: "Readiness", count: 22 }' in js
    assert "review_workspace_source_draft_apply_readiness_card_v1" in js
    assert "source_readiness_field_record_review" in js
    assert "source_readiness_blocked_condition_review" in js
    assert "source_readiness_gate_ref_review" in js
    assert "source_readiness_rollback_dependency_review" in js
    assert "source_readiness_outcome_review" in js
    assert "attachSourceDraftApplyReadinessReviewCards" in js
    assert "sourceDraftApplyReadinessReviewCards" in js
    assert "appendSourceDraftApplyReadinessReviewDetails" in js
    assert "source-readiness-review-card" in js
