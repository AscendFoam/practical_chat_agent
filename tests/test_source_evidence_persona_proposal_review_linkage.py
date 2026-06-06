"""T456 source evidence persona proposal Review Workspace linkage tests.

All source proposal review cards are deterministic synthetic previews. They
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


def _proposal() -> dict[str, Any]:
    return _payload()["source_evidence_persona_proposal"]


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


def test_review_workspace_includes_source_proposal_review_cards() -> None:
    review = _review_workspace()
    proposal = _proposal()
    cards = review["source_proposal_review_cards"]
    expected_count = (
        len(proposal["proposal_candidates"])
        + len(proposal["risk_labels"])
        + len(proposal["rollback_notes"])
        + len(proposal["review_gate_results"])
        + len(proposal["proposal_outcome_labels"])
    )
    proposal_tab = next(tab for tab in review["filter_tabs"] if tab["key"] == "proposal")

    assert len(cards) == expected_count
    assert proposal_tab["count"] == len(cards)
    assert all(
        card["schema_version"] == "review_workspace_source_evidence_persona_proposal_card_v1"
        for card in cards
    )
    assert all(card["source_surface"] == "source_evidence_persona_proposal" for card in cards)
    assert all("proposal" in card["filter_keys"] for card in cards)
    assert {card["card_kind"] for card in cards} == {
        "source_persona_proposal_candidate_review",
        "source_persona_proposal_risk_review",
        "source_persona_proposal_rollback_review",
        "source_persona_proposal_gate_review",
        "source_persona_proposal_outcome_review",
    }


def test_proposal_candidate_review_cards_preserve_safe_metadata() -> None:
    proposal = _proposal()
    cards = _review_workspace()["source_proposal_review_cards"]
    candidate_by_id = {
        candidate["proposal_id"]: candidate
        for candidate in proposal["proposal_candidates"]
    }
    candidate_cards = [
        card for card in cards if card["card_kind"] == "source_persona_proposal_candidate_review"
    ]

    assert len(candidate_cards) == len(candidate_by_id)
    for card in candidate_cards:
        candidate = candidate_by_id[card["proposal_id"]]
        assert card["persona_field_path"] == candidate["persona_field_path"]
        assert card["proposed_value_summary"] == candidate["proposed_value_summary"]
        assert card["rationale_summary"] == candidate["rationale_summary"]
        assert card["source_trait_hypothesis_ids"] == candidate["source_trait_hypothesis_ids"]
        assert card["supporting_evidence_row_ids"] == candidate["supporting_evidence_row_ids"]
        assert card["confidence_band"] == candidate["confidence_band"]
        assert card["risk_label_ids"] == candidate["risk_label_ids"]
        assert card["rollback_note_ids"] == candidate["rollback_note_ids"]
        assert card["review_gate_result_ids"] == candidate["review_gate_result_ids"]
        assert card["proposal_status"] == "preview_only"
        assert card["mutation_allowed"] is False
        assert card["review_required"] is True


def test_risk_rollback_gate_and_outcome_cards_preserve_safe_metadata() -> None:
    proposal = _proposal()
    cards = _review_workspace()["source_proposal_review_cards"]
    risk_by_id = {risk["risk_label_id"]: risk for risk in proposal["risk_labels"]}
    rollback_by_id = {note["rollback_note_id"]: note for note in proposal["rollback_notes"]}
    gate_by_id = {gate["review_gate_result_id"]: gate for gate in proposal["review_gate_results"]}
    outcome_by_id = {
        label["outcome_label_id"]: label
        for label in proposal["proposal_outcome_labels"]
    }

    risk_cards = [card for card in cards if card["card_kind"] == "source_persona_proposal_risk_review"]
    rollback_cards = [card for card in cards if card["card_kind"] == "source_persona_proposal_rollback_review"]
    gate_cards = [card for card in cards if card["card_kind"] == "source_persona_proposal_gate_review"]
    outcome_cards = [card for card in cards if card["card_kind"] == "source_persona_proposal_outcome_review"]

    assert len(risk_cards) == len(risk_by_id)
    assert len(rollback_cards) == len(rollback_by_id)
    assert len(gate_cards) == len(gate_by_id)
    assert len(outcome_cards) == len(outcome_by_id)

    for card in risk_cards:
        risk = risk_by_id[card["risk_label_id"]]
        assert card["risk_code"] == risk["risk_code"]
        assert card["severity"] == risk["severity"]
        assert card["blocks_auto_apply"] is True

    for card in rollback_cards:
        note = rollback_by_id[card["rollback_note_id"]]
        assert card["restore_summary"] == note["restore_summary"]
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


def test_source_proposal_review_cards_have_no_unsafe_true_states_or_private_surfaces() -> None:
    cards = _review_workspace()["source_proposal_review_cards"]
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


def test_static_fallback_includes_source_proposal_review_cards_and_renderer_details() -> None:
    js = _asset_text("js")

    assert "source_proposal_review_cards" in js
    assert '{ key: "proposal", label: "Proposal", count: 21 }' in js
    assert "review_workspace_source_evidence_persona_proposal_card_v1" in js
    assert "source_persona_proposal_candidate_review" in js
    assert "source_persona_proposal_risk_review" in js
    assert "source_persona_proposal_rollback_review" in js
    assert "source_persona_proposal_gate_review" in js
    assert "source_persona_proposal_outcome_review" in js
    assert "attachSourceEvidencePersonaProposalReviewCards" in js
    assert "sourceEvidencePersonaProposalReviewCards" in js
    assert "appendSourceEvidencePersonaProposalReviewDetails" in js
    assert "source-proposal-review-card" in js
