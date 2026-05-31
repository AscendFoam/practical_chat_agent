"""T353 static web demo accessibility and friendly-label tests.

These tests inspect local static assets only. They do not call model providers,
read private data, generate media, or enable outbound behavior.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


def _assets() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _read(asset: str) -> str:
    return Path(_assets()[asset]).read_text(encoding="utf-8")


def test_tabs_and_panels_have_accessible_relationships() -> None:
    html = _read("html")

    assert '<nav class="tabs" aria-label="Demo sections" role="tablist">' in html
    for panel in ("chat", "persona", "memory", "life", "proactive", "controls", "voice-avatar"):
        tab_id = f"tab-{panel}"
        panel_id = f"{panel}-panel"
        assert f'id="{tab_id}"' in html
        assert f'role="tab"' in html
        assert f'aria-controls="{panel_id}"' in html
        assert f'id="{panel_id}"' in html
        assert f'role="tabpanel"' in html
        assert f'aria-labelledby="{tab_id}"' in html

    assert 'id="tab-chat" class="tab is-active" data-tab="chat" type="button" role="tab" aria-selected="true"' in html
    assert 'id="persona-panel" class="panel" data-panel="persona" role="tabpanel" aria-labelledby="tab-persona" hidden' in html


def test_scenario_buttons_expose_pressed_state() -> None:
    html = _read("html")
    js = _read("js")

    assert 'aria-pressed="true"' in html
    assert 'data-scenario="safe-review" type="button" aria-pressed="true"' in html
    for scenario in (
        "blocked-persona",
        "crisis-chat",
        "dependency-proactive",
        "life-review",
        "controls-review",
        "voice-avatar-locked",
    ):
        assert f'data-scenario="{scenario}" type="button" aria-pressed="false"' in html

    assert 'setAttribute("aria-pressed"' in js
    assert 'setAttribute("aria-selected"' in js
    assert "panel.hidden =" in js


def test_javascript_maps_technical_states_to_friendly_labels() -> None:
    js = _read("js")

    for label in (
        "Evidence-backed",
        "Imagined",
        "Fictional AI persona",
        "Real-person recreation is blocked",
        "Crisis safety review required",
        "Proactive outreach is blocked",
        "No messages can be sent",
        "Voice is off",
        "Needs review",
        "Avatar locked for research review",
        "Real-person likeness is blocked",
        "Not real-world activity",
    ):
        assert label in js

    assert "function friendlyLabel" in js
    assert "voice enabled: " not in js
    assert "outreach allowed: " not in js


def test_css_preserves_focus_and_long_label_wrapping() -> None:
    css = _read("css")

    assert ".tab:focus-visible" in css
    assert ".scenario:focus-visible" in css
    assert "overflow-wrap: anywhere;" in css
    assert "word-break: normal;" in css

