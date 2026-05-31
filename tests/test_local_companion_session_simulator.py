"""T418 local companion session simulator tests.

All examples are deterministic synthetic fixtures. The session payload does
not read private chat history, call providers, write stores, send messages, or
connect to external platforms/media.
"""

from __future__ import annotations

import json

from practical_chat_agent.ui.text_first_web_demo_adapter import (
    TextFirstWebDemoAdapter,
)
from practical_chat_agent.ui.text_first_web_demo_local_server import (
    TextFirstWebDemoLocalServer,
)


def _payload() -> dict[str, object]:
    return TextFirstWebDemoAdapter().build_synthetic_demo_state().model_dump(mode="json")


def _session() -> dict[str, object]:
    return _payload()["companion_session"]


def test_adapter_state_includes_local_companion_session_payload() -> None:
    session = _session()

    assert session["schema_version"] == "local_companion_session_v1"
    assert session["session_title"]
    assert session["session_summary"]
    assert session["persona_snapshot"]
    assert session["turns"]
    assert session["persona_cues"]
    assert session["memory_recalls"]
    assert session["safety_notes"]
    assert session["post_turn_candidates"]
    assert session["non_execution_flags"]


def test_session_turns_are_ordered_synthetic_and_grounded() -> None:
    session = _session()
    turns = session["turns"]

    assert [turn["turn_id"] for turn in turns] == sorted(
        turn["turn_id"] for turn in turns
    )
    assert {turn["speaker"] for turn in turns}.issubset({"user", "companion"})
    assert all(turn["safe_text"] for turn in turns)
    assert all(turn["generated_by"] == "deterministic_synthetic_fixture" for turn in turns)

    companion_turns = [turn for turn in turns if turn["speaker"] == "companion"]
    assert any(turn["used_memory_recall_ids"] for turn in companion_turns)
    assert any(turn["used_persona_cue_ids"] for turn in companion_turns)
    assert all(isinstance(turn["review_trace"], str) for turn in turns)


def test_memory_recalls_expose_reviewed_summaries_only() -> None:
    session = _session()

    for recall in session["memory_recalls"]:
        assert recall["recall_id"]
        assert recall["memory_kind"] in {
            "factual",
            "relational",
            "procedural",
            "imagined",
        }
        assert recall["truth_status"] in {"evidence_backed", "inferred", "imagined"}
        assert recall["reviewed_summary"]
        assert recall["source_label"].startswith("synthetic_")
        assert recall["raw_source_available"] is False
        serialized = json.dumps(recall, ensure_ascii=False).lower()
        for forbidden in (
            "raw_text",
            "raw_transcript",
            "private_messages",
            "private/chat_history",
            "private\\chat_history",
        ):
            assert forbidden not in serialized


def test_post_turn_candidates_are_review_only_and_non_executing() -> None:
    session = _session()
    candidates = session["post_turn_candidates"]
    candidate_kinds = {candidate["candidate_kind"] for candidate in candidates}

    assert {"memory_candidate", "persona_growth_patch", "proactive_suggestion"}.issubset(
        candidate_kinds
    )
    for candidate in candidates:
        assert candidate["candidate_id"]
        assert candidate["originating_turn_id"]
        assert candidate["safe_summary"]
        assert candidate["review_required"] is True
        assert candidate["preview_only"] is True
        assert candidate["changes_state"] is False
        assert candidate["automatic_apply"] is False
        assert candidate["sends_messages"] is False


def test_non_execution_flags_preserve_local_boundaries() -> None:
    flags = _session()["non_execution_flags"]

    assert flags == {
        "local_only": True,
        "synthetic_fixture": True,
        "calls_provider": False,
        "uses_private_source": False,
        "writes_runtime_store": False,
        "automatic_apply": False,
        "sends_messages": False,
        "media_runtime_enabled": False,
    }


def test_served_demo_state_includes_session_without_forbidden_surfaces() -> None:
    response = TextFirstWebDemoLocalServer().route(
        "/demo-state.json",
        user_id="session_synthetic",
    )
    payload = json.loads(response.text)

    assert response.status_code == 200
    assert payload["companion_session"]["schema_version"] == "local_companion_session_v1"

    serialized = json.dumps(payload["companion_session"], ensure_ascii=False).lower()
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
        "audio_bytes",
        "image_bytes",
        "video_bytes",
        "generated_audio",
        "generated_image",
        "generated_video",
    ):
        assert forbidden not in serialized
