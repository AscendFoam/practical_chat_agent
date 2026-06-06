"""T450 persona source evidence Review Workspace linkage tests.

All source evidence review cards are deterministic synthetic previews. They
must not read private data, call providers, retain raw source content, extract
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
    "raw_content_retained",
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _review_workspace() -> dict[str, Any]:
    return _payload()["review_workspace"]


def _matrix() -> dict[str, Any]:
    return _payload()["persona_source_evidence_matrix"]


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


def test_review_workspace_includes_persona_source_evidence_review_cards() -> None:
    review = _review_workspace()
    matrix = _matrix()
    cards = review["source_evidence_review_cards"]
    expected_count = (
        len(matrix["excluded_source_refs"])
        + len(matrix["evidence_rows"])
        + len(matrix["trait_hypotheses"])
        + len(matrix["quality_labels"])
        + len(matrix["review_gate_results"])
    )
    source_tab = next(tab for tab in review["filter_tabs"] if tab["key"] == "source")
    evidence_tab = next(tab for tab in review["filter_tabs"] if tab["key"] == "evidence")

    assert len(cards) == expected_count
    assert source_tab["count"] == len(review["source_intake_review_cards"]) + len(cards)
    assert evidence_tab["count"] == len(cards)
    assert all(
        card["schema_version"] == "review_workspace_persona_source_evidence_card_v1"
        for card in cards
    )
    assert all(card["source_surface"] == "persona_source_evidence_matrix" for card in cards)
    assert all("source" in card["filter_keys"] and "evidence" in card["filter_keys"] for card in cards)
    assert {card["card_kind"] for card in cards} == {
        "persona_source_evidence_exclusion_review",
        "persona_source_evidence_row_review",
        "persona_source_trait_hypothesis_review",
        "persona_source_quality_label_review",
        "persona_source_review_gate_result_review",
    }


def test_evidence_row_and_trait_review_cards_preserve_safe_matrix_metadata() -> None:
    matrix = _matrix()
    cards = _review_workspace()["source_evidence_review_cards"]
    evidence_by_id = {
        row["evidence_row_id"]: row
        for row in matrix["evidence_rows"]
    }
    trait_by_id = {
        trait["trait_hypothesis_id"]: trait
        for trait in matrix["trait_hypotheses"]
    }

    evidence_cards = [
        card for card in cards if card["card_kind"] == "persona_source_evidence_row_review"
    ]
    trait_cards = [
        card for card in cards if card["card_kind"] == "persona_source_trait_hypothesis_review"
    ]

    assert len(evidence_cards) == len(evidence_by_id)
    assert len(trait_cards) == len(trait_by_id)
    for card in evidence_cards:
        row = evidence_by_id[card["evidence_row_id"]]
        assert card["source_id"] == row["source_id"]
        assert card["source_kind"] == row["source_kind"]
        assert card["evidence_kind"] == row["evidence_kind"]
        assert card["quality_label_id"] == row["quality_label_id"]
        assert card["supports_trait_paths"] == row["supports_trait_paths"]
        assert card["uncertainty_notes"] == row["uncertainty_notes"]
        assert card["review_gate_result_ids"] == row["review_gate_result_ids"]
        assert card["raw_content_retained"] is False
        assert card["review_required"] is True

    for card in trait_cards:
        trait = trait_by_id[card["trait_hypothesis_id"]]
        assert card["trait_path"] == trait["trait_path"]
        assert card["confidence_band"] == trait["confidence_band"]
        assert card["supporting_evidence_row_ids"] == trait["supporting_evidence_row_ids"]
        assert card["conflicting_evidence_row_ids"] == trait["conflicting_evidence_row_ids"]
        assert card["review_gate_result_ids"] == trait["review_gate_result_ids"]
        assert card["apply_status"] == "preview_only"
        assert card["mutation_allowed"] is False


def test_exclusion_quality_and_gate_review_cards_preserve_safe_metadata() -> None:
    matrix = _matrix()
    cards = _review_workspace()["source_evidence_review_cards"]
    exclusions_by_id = {
        ref["source_id"]: ref
        for ref in matrix["excluded_source_refs"]
    }
    quality_by_id = {
        label["quality_label_id"]: label
        for label in matrix["quality_labels"]
    }
    gates_by_id = {
        gate["review_gate_result_id"]: gate
        for gate in matrix["review_gate_results"]
    }

    exclusion_cards = [
        card for card in cards if card["card_kind"] == "persona_source_evidence_exclusion_review"
    ]
    quality_cards = [
        card for card in cards if card["card_kind"] == "persona_source_quality_label_review"
    ]
    gate_cards = [
        card for card in cards if card["card_kind"] == "persona_source_review_gate_result_review"
    ]

    assert len(exclusion_cards) == len(exclusions_by_id)
    assert len(quality_cards) == len(quality_by_id)
    assert len(gate_cards) == len(gates_by_id)

    for card in exclusion_cards:
        ref = exclusions_by_id[card["source_id"]]
        assert card["source_kind"] == ref["source_kind"]
        assert card["blocked_reason_ids"] == ref["blocked_reason_ids"]
        assert card["excluded_from_evidence"] is True
        assert card["raw_content_retained"] is False
        assert card["mutation_allowed"] is False

    for card in quality_cards:
        label = quality_by_id[card["quality_label_id"]]
        assert card["quality_code"] == label["quality_code"]
        assert card["severity"] == label["severity"]
        assert card["blocks_unreviewed_extraction"] == label["blocks_unreviewed_extraction"]

    for card in gate_cards:
        gate = gates_by_id[card["review_gate_result_id"]]
        assert card["gate_code"] == gate["gate_code"]
        assert card["status"] == gate["status"]
        assert card["blocks_extraction_when_failed"] is True


def test_source_evidence_review_cards_have_no_unsafe_true_states_or_private_surfaces() -> None:
    cards = _review_workspace()["source_evidence_review_cards"]
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


def test_static_fallback_includes_source_evidence_review_cards_and_renderer_details() -> None:
    js = _asset_text("js")

    assert "source_evidence_review_cards" in js
    assert '{ key: "evidence", label: "Evidence", count: 22 }' in js
    assert "review_workspace_persona_source_evidence_card_v1" in js
    assert "persona_source_evidence_exclusion_review" in js
    assert "persona_source_evidence_row_review" in js
    assert "persona_source_trait_hypothesis_review" in js
    assert "persona_source_quality_label_review" in js
    assert "persona_source_review_gate_result_review" in js
    assert "attachPersonaSourceEvidenceReviewCards" in js
    assert "personaSourceEvidenceReviewCards" in js
    assert "appendPersonaSourceEvidenceReviewDetails" in js
    assert "persona-source-evidence-review-card" in js
