"""T438 persona version draft review-linkage tests.

All version review cards are deterministic synthetic previews. They must not
read private data, call providers, write stores, apply persona changes, send
messages, connect adapters, or enable media runtime.
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
    "uses_model_provider",
    "reads_private_sources",
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


def _ledger() -> dict[str, Any]:
    return _payload()["persona_version_draft_ledger"]


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


def test_review_workspace_includes_persona_version_review_cards() -> None:
    review = _review_workspace()
    ledger = _ledger()
    cards = review["version_review_cards"]
    expected_count = (
        len(ledger["drafts"])
        + len(ledger["conflict_notes"])
        + len(ledger["rollback_ref_index"])
        + len(ledger["review_outcome_labels"])
    )

    assert len(cards) == expected_count
    assert any(tab["key"] == "version" and tab["count"] == len(cards) for tab in review["filter_tabs"])
    assert all(card["schema_version"] == "review_workspace_persona_version_card_v1" for card in cards)
    assert all(card["source_surface"] == "persona_version_draft_ledger" for card in cards)
    assert {card["card_kind"] for card in cards} == {
        "persona_version_draft_review",
        "persona_version_conflict_review",
        "persona_version_rollback_review",
        "persona_version_outcome_review",
    }


def test_draft_review_cards_expose_outcomes_and_patch_sets() -> None:
    drafts_by_id = {draft["draft_id"]: draft for draft in _ledger()["drafts"]}
    cards = [
        card
        for card in _review_workspace()["version_review_cards"]
        if card["card_kind"] == "persona_version_draft_review"
    ]

    assert len(cards) == len(drafts_by_id)
    for card in cards:
        draft = drafts_by_id[card["draft_id"]]
        assert card["candidate_kind"] == "persona_version_draft"
        assert card["reviewer_outcome"] == draft["reviewer_outcome"]
        assert card["source_patch_ids"] == draft["source_patch_ids"]
        assert card["excluded_patch_ids"] == draft["excluded_patch_ids"]
        assert card["conflict_note_ids"] == draft["conflict_note_ids"]
        assert card["rollback_ref_ids"] == draft["rollback_ref_ids"]
        assert "version" in card["filter_keys"]
        assert card["review_required"] is True
        assert card["preview_only"] is True
        assert card["changes_state"] is False
        assert card["mutation_allowed"] is False
        assert card["automatic_apply"] is False
        assert card["sends_messages"] is False


def test_conflict_rollback_and_outcome_cards_preserve_safe_metadata() -> None:
    review_cards = _review_workspace()["version_review_cards"]
    ledger = _ledger()
    conflict_by_id = {
        note["conflict_note_id"]: note
        for note in ledger["conflict_notes"]
    }
    rollback_by_id = {
        ref["rollback_ref_id"]: ref
        for ref in ledger["rollback_ref_index"]
    }
    outcome_by_id = {
        outcome["outcome"]: outcome
        for outcome in ledger["review_outcome_labels"]
    }

    conflict_cards = [card for card in review_cards if card["card_kind"] == "persona_version_conflict_review"]
    rollback_cards = [card for card in review_cards if card["card_kind"] == "persona_version_rollback_review"]
    outcome_cards = [card for card in review_cards if card["card_kind"] == "persona_version_outcome_review"]

    assert len(conflict_cards) == len(conflict_by_id)
    assert len(rollback_cards) == len(rollback_by_id)
    assert len(outcome_cards) == len(outcome_by_id)

    for card in conflict_cards:
        conflict = conflict_by_id[card["conflict_note_id"]]
        assert card["conflict_code"] == conflict["conflict_code"]
        assert card["mitigation_summary"] == conflict["mitigation_summary"]
        assert card["blocks_auto_apply"] is True

    for card in rollback_cards:
        rollback = rollback_by_id[card["rollback_ref_id"]]
        assert card["related_draft_ids"] == rollback["related_draft_ids"]
        assert card["restore_summary"] == rollback["restore_summary"]
        assert card["runtime_rollback_ready"] is False

    for card in outcome_cards:
        outcome = outcome_by_id[card["outcome"]]
        assert card["label"] == outcome["label"]
        assert card["safe_summary"] == outcome["safe_summary"]


def test_version_review_cards_have_no_unsafe_true_states_or_private_surfaces() -> None:
    cards = _review_workspace()["version_review_cards"]
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


def test_static_fallback_includes_version_review_cards_and_renderer_details() -> None:
    js = _asset_text("js")
    css = _asset_text("css")

    assert "version_review_cards" in js
    assert '{ key: "version", label: "Version", count: 14 }' in js
    assert "review_workspace_persona_version_card_v1" in js
    assert "persona_version_draft_review" in js
    assert "persona_version_conflict_review" in js
    assert "persona_version_rollback_review" in js
    assert "persona_version_outcome_review" in js
    assert "attachPersonaVersionDraftReviewCards" in js
    assert "personaVersionDraftReviewCards" in js
    assert "appendPersonaVersionDraftReviewDetails" in js
    assert "persona-version-review-card" in js
    assert ".persona-version-review-card" in css
