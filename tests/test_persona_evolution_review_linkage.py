"""T432 persona evolution review-linkage tests.

All evolution review cards are deterministic synthetic previews. They must not
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


def _evolution() -> dict[str, Any]:
    return _payload()["persona_evolution_preview"]


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


def test_review_workspace_includes_persona_evolution_review_cards() -> None:
    review = _review_workspace()
    evolution = _evolution()
    cards = review["evolution_review_cards"]
    expected_count = (
        len(evolution["proposed_patch_candidates"])
        + len(evolution["risk_labels"])
        + len(evolution["rollback_notes"])
        + len(evolution["blocked_source_exclusions"])
    )

    assert len(cards) == expected_count
    assert any(tab["key"] == "evolution" and tab["count"] == len(cards) for tab in review["filter_tabs"])
    assert all(card["schema_version"] == "review_workspace_persona_evolution_card_v1" for card in cards)
    assert all(card["source_surface"] == "persona_evolution_preview" for card in cards)
    assert {card["card_kind"] for card in cards} == {
        "persona_evolution_patch_review",
        "persona_evolution_risk_review",
        "persona_evolution_rollback_review",
        "persona_evolution_blocked_source_exclusion",
    }


def test_patch_review_cards_are_linked_to_risks_and_rollbacks() -> None:
    evolution = _evolution()
    patches_by_id = {
        patch["patch_id"]: patch
        for patch in evolution["proposed_patch_candidates"]
    }
    risk_ids = {risk["risk_label_id"] for risk in evolution["risk_labels"]}
    rollback_ids = {note["rollback_note_id"] for note in evolution["rollback_notes"]}
    cards = [
        card
        for card in _review_workspace()["evolution_review_cards"]
        if card["card_kind"] == "persona_evolution_patch_review"
    ]

    assert len(cards) == len(patches_by_id)
    for card in cards:
        patch = patches_by_id[card["patch_id"]]
        assert card["candidate_kind"] == "persona_evolution_patch"
        assert card["changed_field_path"] == patch["changed_field_path"]
        assert card["before_summary"] == patch["before_summary"]
        assert card["after_summary"] == patch["after_summary"]
        assert set(card["risk_label_ids"]).issubset(risk_ids)
        assert set(card["rollback_note_ids"]).issubset(rollback_ids)
        assert "evolution" in card["filter_keys"]
        assert card["review_required"] is True
        assert card["preview_only"] is True
        assert card["changes_state"] is False
        assert card["mutation_allowed"] is False
        assert card["automatic_apply"] is False
        assert card["sends_messages"] is False


def test_risk_rollback_and_exclusion_cards_preserve_safe_metadata() -> None:
    review_cards = _review_workspace()["evolution_review_cards"]
    evolution = _evolution()
    risk_by_id = {risk["risk_label_id"]: risk for risk in evolution["risk_labels"]}
    rollback_by_id = {
        note["rollback_note_id"]: note
        for note in evolution["rollback_notes"]
    }
    exclusion_by_id = {
        exclusion["blocked_request_id"]: exclusion
        for exclusion in evolution["blocked_source_exclusions"]
    }

    risk_cards = [card for card in review_cards if card["card_kind"] == "persona_evolution_risk_review"]
    rollback_cards = [card for card in review_cards if card["card_kind"] == "persona_evolution_rollback_review"]
    exclusion_cards = [
        card
        for card in review_cards
        if card["card_kind"] == "persona_evolution_blocked_source_exclusion"
    ]

    assert len(risk_cards) == len(risk_by_id)
    assert len(rollback_cards) == len(rollback_by_id)
    assert len(exclusion_cards) == len(exclusion_by_id)

    for card in risk_cards:
        risk = risk_by_id[card["risk_label_id"]]
        assert card["risk_code"] == risk["risk_code"]
        assert card["mitigation_summary"] == risk["mitigation_summary"]
        assert card["blocks_auto_apply"] is True

    for card in rollback_cards:
        note = rollback_by_id[card["rollback_note_id"]]
        assert card["target_patch_ids"] == note["target_patch_ids"]
        assert card["rollback_summary"] == note["rollback_summary"]
        assert card["runtime_rollback_ready"] is False

    for card in exclusion_cards:
        exclusion = exclusion_by_id[card["blocked_request_id"]]
        assert card["request_type"] == exclusion["request_type"]
        assert card["exclusion_reason"] == exclusion["exclusion_reason"]
        assert card["excluded_from_patch_generation"] is True
        assert card["mutation_allowed"] is False


def test_evolution_review_cards_have_no_unsafe_true_states_or_private_surfaces() -> None:
    cards = _review_workspace()["evolution_review_cards"]
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


def test_static_fallback_includes_evolution_review_cards_and_renderer_details() -> None:
    js = _asset_text("js")
    css = _asset_text("css")

    assert "evolution_review_cards" in js
    assert '{ key: "evolution", label: "Evolution", count: 20 }' in js
    assert "review_workspace_persona_evolution_card_v1" in js
    assert "persona_evolution_patch_review" in js
    assert "persona_evolution_risk_review" in js
    assert "persona_evolution_rollback_review" in js
    assert "persona_evolution_blocked_source_exclusion" in js
    assert "attachPersonaEvolutionReviewCards" in js
    assert "personaEvolutionReviewCards" in js
    assert "appendPersonaEvolutionReviewDetails" in js
    assert "persona-evolution-review-card" in js
    assert ".persona-evolution-review-card" in css
