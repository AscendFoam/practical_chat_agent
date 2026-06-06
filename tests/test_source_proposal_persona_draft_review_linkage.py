"""T462 source proposal persona draft Review Workspace linkage tests.

All draft review cards are deterministic synthetic previews. They must not
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
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _review_workspace() -> dict[str, Any]:
    return _payload()["review_workspace"]


def _draft() -> dict[str, Any]:
    return _payload()["source_proposal_persona_draft"]


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


def test_review_workspace_includes_source_draft_review_cards() -> None:
    review = _review_workspace()
    draft = _draft()
    cards = review["source_draft_review_cards"]
    expected_count = (
        len(draft["draft_field_changes"])
        + len(draft["unchanged_field_summaries"])
        + len(draft["conflict_notes"])
        + len(draft["rollback_refs"])
        + len(draft["review_gate_results"])
        + len(draft["draft_outcome_labels"])
    )
    draft_tab = next(tab for tab in review["filter_tabs"] if tab["key"] == "draft")

    assert len(cards) == expected_count
    assert draft_tab["count"] == len(cards)
    assert all(
        card["schema_version"] == "review_workspace_source_proposal_persona_draft_card_v1"
        for card in cards
    )
    assert all(card["source_surface"] == "source_proposal_persona_draft" for card in cards)
    assert all("draft" in card["filter_keys"] for card in cards)
    assert {card["card_kind"] for card in cards} == {
        "source_persona_draft_field_change_review",
        "source_persona_draft_unchanged_field_review",
        "source_persona_draft_conflict_review",
        "source_persona_draft_rollback_review",
        "source_persona_draft_gate_review",
        "source_persona_draft_outcome_review",
    }


def test_draft_field_review_cards_preserve_safe_metadata() -> None:
    draft = _draft()
    cards = _review_workspace()["source_draft_review_cards"]
    change_by_id = {
        change["draft_change_id"]: change
        for change in draft["draft_field_changes"]
    }
    change_cards = [
        card for card in cards if card["card_kind"] == "source_persona_draft_field_change_review"
    ]

    assert len(change_cards) == len(change_by_id)
    for card in change_cards:
        change = change_by_id[card["draft_change_id"]]
        assert card["persona_field_path"] == change["persona_field_path"]
        assert card["before_summary"] == change["before_summary"]
        assert card["after_summary"] == change["after_summary"]
        assert card["source_proposal_ids"] == change["source_proposal_ids"]
        assert card["source_trait_hypothesis_ids"] == change["source_trait_hypothesis_ids"]
        assert card["supporting_evidence_row_ids"] == change["supporting_evidence_row_ids"]
        assert card["confidence_band"] == change["confidence_band"]
        assert card["risk_label_ids"] == change["risk_label_ids"]
        assert card["conflict_note_ids"] == change["conflict_note_ids"]
        assert card["rollback_ref_ids"] == change["rollback_ref_ids"]
        assert card["review_gate_result_ids"] == change["review_gate_result_ids"]
        assert card["draft_status"] == "preview_only"
        assert card["mutation_allowed"] is False
        assert card["review_required"] is True


def test_draft_support_cards_preserve_safe_metadata() -> None:
    draft = _draft()
    cards = _review_workspace()["source_draft_review_cards"]
    unchanged_by_path = {
        field["field_path"]: field for field in draft["unchanged_field_summaries"]
    }
    conflict_by_id = {note["conflict_note_id"]: note for note in draft["conflict_notes"]}
    rollback_by_id = {ref["rollback_ref_id"]: ref for ref in draft["rollback_refs"]}
    gate_by_id = {gate["review_gate_result_id"]: gate for gate in draft["review_gate_results"]}
    outcome_by_id = {
        label["outcome_label_id"]: label
        for label in draft["draft_outcome_labels"]
    }

    unchanged_cards = [card for card in cards if card["card_kind"] == "source_persona_draft_unchanged_field_review"]
    conflict_cards = [card for card in cards if card["card_kind"] == "source_persona_draft_conflict_review"]
    rollback_cards = [card for card in cards if card["card_kind"] == "source_persona_draft_rollback_review"]
    gate_cards = [card for card in cards if card["card_kind"] == "source_persona_draft_gate_review"]
    outcome_cards = [card for card in cards if card["card_kind"] == "source_persona_draft_outcome_review"]

    assert len(unchanged_cards) == len(unchanged_by_path)
    assert len(conflict_cards) == len(conflict_by_id)
    assert len(rollback_cards) == len(rollback_by_id)
    assert len(gate_cards) == len(gate_by_id)
    assert len(outcome_cards) == len(outcome_by_id)

    for card in unchanged_cards:
        field = unchanged_by_path[card["field_path"]]
        assert card["safe_summary"] == field["safe_summary"]
        assert card["reason"] == field["reason"]

    for card in conflict_cards:
        note = conflict_by_id[card["conflict_note_id"]]
        assert card["conflict_code"] == note["conflict_code"]
        assert card["severity"] == note["severity"]
        assert card["blocks_auto_apply"] is True

    for card in rollback_cards:
        ref = rollback_by_id[card["rollback_ref_id"]]
        assert card["restore_summary"] == ref["restore_summary"]
        assert card["runtime_rollback_ready"] is False

    for card in gate_cards:
        gate = gate_by_id[card["review_gate_result_id"]]
        assert card["gate_code"] == gate["gate_code"]
        assert card["status"] == gate["status"]
        assert card["blocks_apply_when_failed"] is True

    for card in outcome_cards:
        outcome = outcome_by_id[card["outcome_label_id"]]
        assert card["outcome"] == outcome["outcome"]
        assert card["safe_summary"] == outcome["safe_summary"]


def test_source_draft_review_cards_have_no_unsafe_true_states_or_private_surfaces() -> None:
    cards = _review_workspace()["source_draft_review_cards"]
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


def test_static_fallback_includes_source_draft_review_cards_and_renderer_details() -> None:
    js = _asset_text("js")

    assert "source_draft_review_cards" in js
    assert '{ key: "draft", label: "Draft", count: 28 }' in js
    assert "review_workspace_source_proposal_persona_draft_card_v1" in js
    assert "source_persona_draft_field_change_review" in js
    assert "source_persona_draft_unchanged_field_review" in js
    assert "source_persona_draft_conflict_review" in js
    assert "source_persona_draft_rollback_review" in js
    assert "source_persona_draft_gate_review" in js
    assert "source_persona_draft_outcome_review" in js
    assert "attachSourceProposalPersonaDraftReviewCards" in js
    assert "sourceProposalPersonaDraftReviewCards" in js
    assert "appendSourceProposalPersonaDraftReviewDetails" in js
    assert "source-draft-review-card" in js
