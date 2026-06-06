"""T343 static web demo state switching tests.

All state is synthetic and local. These tests inspect static assets only; they
do not start a server, call model providers, read private chat logs, generate
media, or enable outbound behavior.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _paths() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def test_scenario_controls_exist_for_required_review_states() -> None:
    html = Path(_paths()["html"]).read_text(encoding="utf-8")

    assert 'id="scenario-controls"' in html
    for scenario in (
        "safe-review",
        "blocked-persona",
        "crisis-chat",
        "dependency-proactive",
        "life-review",
        "controls-review",
        "voice-avatar-locked",
    ):
        assert f'data-scenario="{scenario}"' in html


def test_switching_logic_is_local_and_preserves_base_payload() -> None:
    js = Path(_paths()["js"]).read_text(encoding="utf-8")

    assert "const baseState" in js
    assert "function cloneState" in js
    assert "function setScenario" in js
    assert "window.TEXT_FIRST_WEB_DEMO_STATE" in js
    assert "fetch(" not in js
    assert "XMLHttpRequest" not in js


def test_scenario_switching_preserves_visible_ai_synthetic_labels() -> None:
    html = Path(_paths()["html"]).read_text(encoding="utf-8")
    js = Path(_paths()["js"]).read_text(encoding="utf-8")

    assert "AI-generated synthetic companion" in html
    assert "scenario-status" in html
    assert "AI-generated" in js
    assert "locked_research_only" in js


def test_state_switching_assets_have_no_external_media_provider_or_outbound_fields() -> None:
    paths = _paths()
    combined = "\n".join(Path(path).read_text(encoding="utf-8") for path in paths.values()).lower()

    for forbidden in (
        "http://",
        "https://",
        "provider_token",
        "api_key",
        "generated_audio_path",
        "generated_video_path",
        "microphone",
        "camera",
        '"sends_messages": true',
        '"calls_provider": true',
        '"uses_model_provider": true',
        '"uses_private_source": true',
        '"reads_private_sources": true',
        '"writes_runtime_store": true',
        '"automatic_apply": true',
        '"uses_platform_adapter": true',
        '"media_runtime_enabled": true',
        '"uses_media_runtime": true',
        "send_queue",
        "schedule",
        "delivery",
        "webhook",
        "queue",
    ):
        assert forbidden not in combined
