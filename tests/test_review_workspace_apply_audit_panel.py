"""T410 review workspace apply audit panel tests.

All examples are synthetic. The panel projects already-normalized local apply
audit entries and does not read private chat history, call providers, write
stores, send messages, or connect to external platforms/media.
"""

from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_adapter import (
    TextFirstWebDemoAdapter,
)


ROOT = Path(__file__).resolve().parents[1]
STATIC_JS = ROOT / "src" / "practical_chat_agent" / "ui" / "static" / "text_first_web_demo.js"
STATIC_CSS = ROOT / "src" / "practical_chat_agent" / "ui" / "static" / "text_first_web_demo.css"


def _review_workspace() -> dict[str, object]:
    state = TextFirstWebDemoAdapter().build_synthetic_demo_state()
    return state.review_workspace


def test_review_workspace_payload_includes_apply_audit_manifest_cards() -> None:
    review = _review_workspace()

    cards = review["apply_audit_entries"]

    assert len(cards) == 2
    assert {card["apply_type"] for card in cards} == {
        "persona_growth",
        "memory_lifecycle",
    }
    assert all(card["card_kind"] == "apply_audit_manifest_entry" for card in cards)
    assert all(card["review_required"] is True for card in cards)
    assert all(card["changes_state"] is False for card in cards)


def test_apply_audit_cards_preserve_rollback_and_gate_references() -> None:
    review = _review_workspace()
    cards = {
        card["apply_type"]: card
        for card in review["apply_audit_entries"]
    }

    persona = cards["persona_growth"]
    assert persona["source_artifact_id"] == "pgpatch_webdemo_persona"
    assert persona["review_decision_id"] == "rqdec_webdemo_persona"
    assert persona["eligibility_id"] == "mapelig_webdemo_persona"
    assert persona["approval_id"] == "aeapproval_webdemo_persona"
    assert persona["rollback_refs"]["rollback_target_version_id"] == "pver_webdemo_001"
    assert persona["changed_field_paths"] == ["style.tone", "relationship.pacing"]

    memory = cards["memory_lifecycle"]
    assert memory["source_artifact_id"] == "mldplan_webdemo_memory"
    assert memory["review_decision_id"] == "rqdec_webdemo_memory"
    assert memory["eligibility_id"] == "mapelig_webdemo_memory"
    assert memory["approval_id"] == "aeapproval_webdemo_memory"
    assert memory["rollback_refs"]["mev_webdemo_old"] == "memrec_webdemo_prior"
    assert memory["affected_memory_ids"] == ["mev_webdemo_old"]


def test_review_workspace_apply_audit_payload_has_no_forbidden_fields() -> None:
    serialized = json.dumps(_review_workspace(), ensure_ascii=False).lower()

    for forbidden in (
        "raw_text",
        "raw_transcript",
        "chat_history",
        "private_messages",
        "provider_credentials",
        "platform_recipient",
        "send_queue",
        "schedule",
        "webhook",
        "token",
        "microphone",
        "camera",
        "audio_bytes",
        "image_bytes",
        "video_bytes",
        "generated_audio",
        "generated_image",
        "generated_video",
    ):
        assert forbidden not in serialized


def test_static_assets_include_apply_audit_panel_hooks_without_delivery_or_media_actions() -> None:
    script = STATIC_JS.read_text(encoding="utf-8")
    styles = STATIC_CSS.read_text(encoding="utf-8")
    combined = f"{script}\n{styles}".lower()

    assert "apply_audit_entries" in script
    assert "appendApplyAuditDetails" in script
    assert "apply-audit-card" in styles

    for forbidden in (
        "platform_recipient",
        "send_queue",
        "open_webhook",
        "call_provider",
        "generate_audio",
        "generate_image",
        "generate_video",
        "connect_platform",
    ):
        assert forbidden not in combined
