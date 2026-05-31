"""T413 integrated demo scenario spine tests.

All examples are synthetic. The scenario spine is a local product-review
surface and does not read private chat history, call providers, write stores,
send messages, or connect to external platforms/media.
"""

from __future__ import annotations

import json
from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_adapter import (
    TextFirstWebDemoAdapter,
)
from practical_chat_agent.ui.text_first_web_demo_local_server import (
    TextFirstWebDemoLocalServer,
)
from practical_chat_agent.ui.text_first_web_demo_static import (
    TextFirstWebDemoStaticShell,
)


def _state_payload() -> dict[str, object]:
    state = TextFirstWebDemoAdapter().build_synthetic_demo_state()
    return state.model_dump(mode="json")


def _assets() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def test_adapter_state_includes_integrated_scenario_spine() -> None:
    payload = _state_payload()
    scenario = payload["integrated_scenario"]

    assert scenario["schema_version"] == "integrated_demo_scenario_spine_v1"
    assert scenario["scenario_title"] == "Controlled companion review path"
    assert scenario["persona_promise"]
    assert scenario["memory_promise"]
    assert scenario["review_promise"]
    assert scenario["proactive_promise"]
    assert scenario["life_stream_promise"]
    assert scenario["voice_avatar_boundary"]
    assert scenario["commercial_positioning"]
    assert scenario["readiness_summary"]


def test_integrated_scenario_steps_are_safe_and_cover_existing_sections() -> None:
    scenario = _state_payload()["integrated_scenario"]
    steps = scenario["scenario_steps"]
    section_keys = {step["section_key"] for step in steps}

    assert len(steps) >= 8
    assert {
        "chat",
        "persona",
        "memory",
        "review",
        "proactive",
        "life",
        "controls",
        "voice-avatar",
    }.issubset(section_keys)
    for step in steps:
        assert step["step_label"]
        assert step["safe_summary"]
        assert step["section_key"] in section_keys
        assert "raw" not in json.dumps(step, ensure_ascii=False).lower()


def test_commercial_positioning_excludes_dependency_and_impersonation_claims() -> None:
    scenario = _state_payload()["integrated_scenario"]
    commercial_text = json.dumps(
        scenario["commercial_positioning"],
        ensure_ascii=False,
    ).lower()

    for forbidden in (
        "dependency_pressure",
        "guilt",
        "impersonat",
        "replacement",
        "crisis_paywall",
        "private_chat_monetization",
    ):
        assert forbidden not in commercial_text


def test_static_assets_include_integrated_scenario_hooks() -> None:
    paths = _assets()
    html = Path(paths["html"]).read_text(encoding="utf-8")
    js = Path(paths["js"]).read_text(encoding="utf-8")
    css = Path(paths["css"]).read_text(encoding="utf-8")

    assert 'id="integrated-scenario"' in html
    assert 'id="scenario-spine-list"' in html
    assert 'id="scenario-readiness"' in html
    assert 'id="scenario-commercial"' in html
    assert "drawIntegratedScenario" in js
    assert "integrated_scenario" in js
    assert ".scenario-spine-grid" in css


def test_served_payload_and_assets_have_no_forbidden_surfaces() -> None:
    server = TextFirstWebDemoLocalServer()
    combined = "\n".join(
        response.text
        for response in (
            server.route("/"),
            server.route("/demo-state.json"),
            server.route("/text_first_web_demo.css"),
            server.route("/text_first_web_demo.js"),
        )
    ).lower()

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
        assert forbidden not in combined
