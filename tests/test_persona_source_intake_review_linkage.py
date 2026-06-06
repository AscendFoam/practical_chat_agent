"""T444 persona source intake Review Workspace linkage tests.

All source intake review cards are deterministic synthetic previews. They must
not read private data, call providers, retain raw source content, extract
traits, write stores, apply persona changes, send messages, connect adapters,
or enable media runtime.
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


def _manifest() -> dict[str, Any]:
    return _payload()["persona_source_intake_manifest"]


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


def test_review_workspace_includes_persona_source_intake_review_cards() -> None:
    review = _review_workspace()
    manifest = _manifest()
    cards = review["source_intake_review_cards"]
    expected_count = (
        len(manifest["source_candidates"])
        + len(manifest["source_policy_gates"])
        + len(manifest["blocked_source_categories"])
        + len(manifest["redaction_profiles"])
    )

    assert len(cards) == expected_count
    source_tab = next(tab for tab in review["filter_tabs"] if tab["key"] == "source")
    assert source_tab["count"] >= len(cards)
    assert all(
        card["schema_version"] == "review_workspace_persona_source_intake_card_v1"
        for card in cards
    )
    assert all(card["source_surface"] == "persona_source_intake_manifest" for card in cards)
    assert {card["card_kind"] for card in cards} == {
        "persona_source_candidate_review",
        "persona_source_policy_gate_review",
        "persona_source_blocked_category_review",
        "persona_source_redaction_profile_review",
    }


def test_source_candidate_review_cards_expose_consent_and_eligibility_metadata() -> None:
    candidates_by_id = {
        candidate["source_id"]: candidate
        for candidate in _manifest()["source_candidates"]
    }
    cards = [
        card
        for card in _review_workspace()["source_intake_review_cards"]
        if card["card_kind"] == "persona_source_candidate_review"
    ]

    assert len(cards) == len(candidates_by_id)
    for card in cards:
        candidate = candidates_by_id[card["source_id"]]
        assert card["candidate_kind"] == "persona_source_candidate"
        assert card["source_kind"] == candidate["source_kind"]
        assert card["declared_owner"] == candidate["declared_owner"]
        assert card["consent_status"] == candidate["consent_status"]
        assert card["minimization_status"] == candidate["minimization_status"]
        assert card["redaction_profile_id"] == candidate["redaction_profile_id"]
        assert card["extraction_eligible"] == candidate["extraction_eligible"]
        assert card["blocked_reason_ids"] == candidate["blocked_reason_ids"]
        assert card["review_gate_ids"] == candidate["review_gate_ids"]
        assert "source" in card["filter_keys"]
        assert card["review_required"] is True
        assert card["preview_only"] is True
        assert card["changes_state"] is False
        assert card["mutation_allowed"] is False
        assert card["automatic_apply"] is False
        assert card["sends_messages"] is False
        assert card["runtime_ready"] is False


def test_gate_blocked_and_redaction_cards_preserve_safe_metadata() -> None:
    cards = _review_workspace()["source_intake_review_cards"]
    manifest = _manifest()
    gates_by_id = {
        gate["gate_id"]: gate
        for gate in manifest["source_policy_gates"]
    }
    blocked_by_id = {
        category["blocked_reason_id"]: category
        for category in manifest["blocked_source_categories"]
    }
    profiles_by_id = {
        profile["redaction_profile_id"]: profile
        for profile in manifest["redaction_profiles"]
    }

    gate_cards = [card for card in cards if card["card_kind"] == "persona_source_policy_gate_review"]
    blocked_cards = [card for card in cards if card["card_kind"] == "persona_source_blocked_category_review"]
    redaction_cards = [card for card in cards if card["card_kind"] == "persona_source_redaction_profile_review"]

    assert len(gate_cards) == len(gates_by_id)
    assert len(blocked_cards) == len(blocked_by_id)
    assert len(redaction_cards) == len(profiles_by_id)

    for card in gate_cards:
        gate = gates_by_id[card["gate_id"]]
        assert card["gate_code"] == gate["gate_code"]
        assert card["enabled"] is True
        assert card["blocks_extraction_when_failed"] is True

    for card in blocked_cards:
        category = blocked_by_id[card["blocked_reason_id"]]
        assert card["blocked_code"] == category["blocked_code"]
        assert card["severity"] == category["severity"]
        assert card["blocks_extraction"] is True

    for card in redaction_cards:
        profile = profiles_by_id[card["redaction_profile_id"]]
        assert card["profile_label"] == profile["profile_label"]
        assert card["redaction_status"] == profile["redaction_status"]
        assert card["retains_raw_content"] is False
        assert card["requires_review"] is True


def test_source_intake_review_cards_have_no_unsafe_true_states_or_private_surfaces() -> None:
    cards = _review_workspace()["source_intake_review_cards"]
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


def test_static_fallback_includes_source_intake_review_cards_and_renderer_details() -> None:
    js = _asset_text("js")

    assert "source_intake_review_cards" in js
    assert '{ key: "source", label: "Source", count: 43 }' in js
    assert "review_workspace_persona_source_intake_card_v1" in js
    assert "persona_source_candidate_review" in js
    assert "persona_source_policy_gate_review" in js
    assert "persona_source_blocked_category_review" in js
    assert "persona_source_redaction_profile_review" in js
    assert "attachPersonaSourceIntakeReviewCards" in js
    assert "personaSourceIntakeReviewCards" in js
    assert "appendPersonaSourceIntakeReviewDetails" in js
    assert "persona-source-review-card" in js
