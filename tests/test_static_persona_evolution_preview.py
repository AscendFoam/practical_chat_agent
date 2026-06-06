"""T431 static persona evolution preview rendering tests.

These tests inspect local static assets only. They do not call providers, read
private data, write stores, apply persona changes, send messages, connect
adapters, or enable media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


REQUIRED_CHANGED_FIELD_PATHS = (
    "style.tone",
    "style.pacing",
    "style.humor",
    "relationship.boundary_style",
    "memory.use_preference",
    "growth.short_term_hint",
)

REQUIRED_RISK_CODES = (
    "persona_drift",
    "overattachment_risk",
    "unclear_evidence",
    "boundary_weakening",
    "blocked_source_excluded",
)


def _paths() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _asset_text(name: str) -> str:
    return Path(_paths()[name]).read_text(encoding="utf-8")


def test_static_html_exposes_persona_evolution_section_and_targets() -> None:
    html = _asset_text("html")

    for expected in (
        'id="persona-evolution"',
        'id="evolution-title"',
        'id="evolution-schema"',
        'id="evolution-non-execution-list"',
        'id="evolution-source-summary"',
        'id="evolution-snapshot"',
        'id="evolution-patch-list"',
        'id="evolution-risk-list"',
        'id="evolution-rollback-list"',
        'id="evolution-exclusion-list"',
    ):
        assert expected in html


def test_static_js_fallback_contains_evolution_contract_values() -> None:
    js = _asset_text("js")

    assert "persona_evolution_preview" in js
    assert "m37.persona_evolution_preview.v1" in js
    assert "drawPersonaEvolutionPreview" in js
    for field_path in REQUIRED_CHANGED_FIELD_PATHS:
        assert field_path in js
    for risk_code in REQUIRED_RISK_CODES:
        assert risk_code in js


def test_static_js_renders_evolution_lists_without_action_controls() -> None:
    js = _asset_text("js")

    for expected in (
        "evolution-source-summary",
        "evolution-snapshot",
        "evolution-patch-list",
        "evolution-risk-list",
        "evolution-rollback-list",
        "evolution-exclusion-list",
        "evolution-non-execution-list",
        "evolution-patch-card",
        "evolution-risk-card",
        "evolution-exclusion-card",
    ):
        assert expected in js

    for forbidden in (
        "evolutionApply",
        "evolutionCommit",
        "evolutionMutate",
        "evolutionClone",
        "evolutionUpload",
        "evolutionRecord",
        "evolutionConnect",
        "evolutionSend",
        "evolutionPublish",
        "evolutionGenerateMedia",
        '"uses_model_provider": true',
        '"reads_private_sources": true',
        '"writes_persona_store": true',
        '"writes_memory_store": true',
        '"writes_review_store": true',
        '"writes_runtime_store": true',
        '"automatic_apply": true',
        '"sends_messages": true',
        '"uses_platform_adapter": true',
        '"uses_media_runtime": true',
    ):
        assert forbidden not in js


def test_static_css_has_evolution_grid_and_responsive_rules() -> None:
    css = _asset_text("css")

    for expected in (
        ".persona-evolution",
        ".evolution-layout",
        ".evolution-patch-grid",
        ".evolution-risk-grid",
        ".evolution-patch-card",
        ".evolution-exclusion-card",
    ):
        assert expected in css

    assert "@media (max-width: 720px)" in css
    assert ".evolution-layout" in css
    assert ".evolution-patch-grid" in css
