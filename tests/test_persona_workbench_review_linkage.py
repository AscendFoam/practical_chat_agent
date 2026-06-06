"""T426 persona workbench review-linkage tests.

All review cards are deterministic synthetic previews. They must not read
private data, call providers, write stores, apply traits, send messages,
connect adapters, or enable media runtime.
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
    "writes_runtime_store",
    "uses_platform_adapter",
    "uses_media_runtime",
}


def _payload() -> dict[str, Any]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _review_workspace() -> dict[str, Any]:
    return _payload()["review_workspace"]


def _workbench() -> dict[str, Any]:
    return _payload()["persona_distillation_workbench"]


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


def test_review_workspace_includes_persona_workbench_review_cards() -> None:
    review = _review_workspace()
    workbench = _workbench()
    cards = review["workbench_review_cards"]

    assert len(cards) == len(workbench["extracted_trait_candidates"]) + len(
        workbench["blocked_requests"]
    )
    assert any(tab["key"] == "distillation" and tab["count"] == len(cards) for tab in review["filter_tabs"])
    assert all(card["schema_version"] == "review_workspace_persona_workbench_card_v1" for card in cards)
    assert all(card["source_surface"] == "persona_distillation_workbench" for card in cards)
    assert {card["card_kind"] for card in cards} == {
        "persona_workbench_trait_review",
        "persona_workbench_blocked_request",
    }


def test_trait_review_cards_are_evidence_linked_and_preview_only() -> None:
    workbench = _workbench()
    evidence_ids = {evidence["evidence_id"] for evidence in workbench["evidence_refs"]}
    trait_ids = {
        candidate["trait_id"]: candidate
        for candidate in workbench["extracted_trait_candidates"]
    }
    trait_cards = [
        card
        for card in _review_workspace()["workbench_review_cards"]
        if card["card_kind"] == "persona_workbench_trait_review"
    ]

    assert len(trait_cards) == len(trait_ids)
    for card in trait_cards:
        candidate = trait_ids[card["candidate_id"]]
        assert card["candidate_kind"] == "persona_distillation_trait"
        assert card["trait_category"] == candidate["category"]
        assert card["candidate_value"] == candidate["candidate_value"]
        assert card["confidence_band"] == candidate["confidence_band"]
        assert set(card["evidence_ref_ids"]).issubset(evidence_ids)
        assert "distillation" in card["filter_keys"]
        assert card["review_required"] is True
        assert card["preview_only"] is True
        assert card["changes_state"] is False
        assert card["mutation_allowed"] is False
        assert card["automatic_apply"] is False
        assert card["sends_messages"] is False


def test_blocked_request_review_cards_remain_blocked_and_non_mutating() -> None:
    blocked_by_id = {
        request["blocked_request_id"]: request
        for request in _workbench()["blocked_requests"]
    }
    blocked_cards = [
        card
        for card in _review_workspace()["workbench_review_cards"]
        if card["card_kind"] == "persona_workbench_blocked_request"
    ]

    assert len(blocked_cards) == len(blocked_by_id)
    for card in blocked_cards:
        request = blocked_by_id[card["blocked_request_id"]]
        assert card["request_type"] == request["request_type"]
        assert card["blocked_status"] == "blocked"
        assert card["risk_reason"] == request["risk_reason"]
        assert card["user_facing_explanation"] == request["user_facing_explanation"]
        assert "blocked" in card["filter_keys"]
        assert "distillation" in card["filter_keys"]
        assert card["review_required"] is True
        assert card["preview_only"] is True
        assert card["changes_state"] is False
        assert card["mutation_allowed"] is False
        assert card["automatic_apply"] is False
        assert card["sends_messages"] is False


def test_workbench_review_cards_have_no_unsafe_true_states_or_private_surfaces() -> None:
    cards = _review_workspace()["workbench_review_cards"]
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


def test_static_fallback_includes_distillation_review_cards_and_renderer_details() -> None:
    js = _asset_text("js")
    css = _asset_text("css")

    assert "workbench_review_cards" in js
    assert '{ key: "distillation", label: "Distillation", count: 12 }' in js
    assert "persona_workbench_trait_review" in js
    assert "persona_workbench_blocked_request" in js
    assert "appendPersonaWorkbenchReviewDetails" in js
    assert "persona-workbench-review-card" in js
    assert ".persona-workbench-review-card" in css
