"""T395 local visual QA fallback tests.

The fallback is deterministic local inspection data. It does not open a
browser, call providers, read private data, generate media, or enable outbound
behavior.
"""

from __future__ import annotations

import json

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _snapshot() -> dict[str, object]:
    return TextFirstWebDemoStaticShell().build_review_workspace_qa_snapshot(
        user_id="qa_synthetic"
    )


def test_review_workspace_visual_qa_snapshot_contains_static_targets_and_cards() -> None:
    snapshot = _snapshot()

    assert snapshot["schema_version"] == "review_workspace_visual_qa_snapshot_v1"
    assert snapshot["user_id"] == "qa_synthetic"
    assert snapshot["static_targets"] == {
        "tab_review": True,
        "review_panel": True,
        "review_filters": True,
        "review_workspace_list": True,
        "review_export_summary": True,
    }
    assert snapshot["card_count"] >= 3
    assert "Memory review item" in snapshot["card_titles"]
    assert "Decision impact preview" in snapshot["card_titles"]
    assert "Safe export summary" in snapshot["card_titles"]


def test_review_workspace_visual_qa_snapshot_covers_key_review_text() -> None:
    snapshot = _snapshot()

    assert "blocked" in snapshot["status_tones"]
    assert "eligible" in snapshot["status_tones"]
    assert "Blocked before state change" in snapshot["status_badge_text"]
    assert "Eligible for later manual review" in snapshot["status_badge_text"]
    assert "Candidate id mismatch" in snapshot["blocker_text"]
    assert "Safe export summary" in snapshot["safe_export_text"]


def test_review_workspace_visual_qa_snapshot_has_no_action_controls_or_forbidden_fields() -> None:
    snapshot = _snapshot()
    serialized = json.dumps(snapshot, ensure_ascii=False).lower()

    assert snapshot["action_controls_present"] is False
    for forbidden in (
        "raw_text",
        "raw_transcript",
        "chat_history",
        "private_messages",
        "provider_credentials",
        "platform_recipient",
        "send_queue",
        "webhook",
        "token",
        "microphone",
        "camera",
        "audio_bytes",
        "image_bytes",
        "video_bytes",
        "apply_decision",
        "mutate_store",
        "write_persona_version",
        "generate_audio",
        "generate_image",
        "generate_video",
    ):
        assert forbidden not in serialized
