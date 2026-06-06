"""T467 static source draft apply-readiness rendering tests.

These tests inspect local static assets only. They do not call providers, read
private data, retain raw source content, create embeddings, extract traits,
write stores, apply persona changes, send messages, connect adapters, or enable
media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


REQUIRED_FIELD_PATHS = (
    "style.tone",
    "style.pacing",
    "style.humor",
    "relationship.boundary_style",
    "memory.use_preference",
    "growth.short_term_hint",
)

REQUIRED_OUTCOMES = (
    "blocked",
    "needs_manual_review",
    "ready_for_future_apply_design",
)


def _paths() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _asset_text(name: str) -> str:
    return Path(_paths()[name]).read_text(encoding="utf-8")


def test_static_html_exposes_source_draft_apply_readiness_section_and_targets() -> None:
    html = _asset_text("html")

    for expected in (
        'id="source-draft-apply-readiness"',
        'id="source-readiness-title"',
        'id="source-readiness-schema"',
        'id="source-readiness-non-execution-list"',
        'id="source-readiness-draft-summary"',
        'id="source-readiness-apply-policy-summary"',
        'id="source-readiness-evaluated-change-list"',
        'id="source-readiness-field-record-list"',
        'id="source-readiness-blocked-condition-list"',
        'id="source-readiness-gate-ref-list"',
        'id="source-readiness-rollback-list"',
        'id="source-readiness-outcome-list"',
    ):
        assert expected in html


def test_static_js_fallback_contains_source_draft_apply_readiness_contract_values() -> None:
    js = _asset_text("js")

    assert "source_draft_apply_readiness" in js
    assert "m43.source_draft_apply_readiness.v1" in js
    assert "drawSourceDraftApplyReadiness" in js
    for field_path in REQUIRED_FIELD_PATHS:
        assert field_path in js
    for outcome in REQUIRED_OUTCOMES:
        assert outcome in js


def test_static_js_renders_readiness_lists_without_action_controls() -> None:
    js = _asset_text("js")

    for expected in (
        "source-readiness-draft-summary",
        "source-readiness-apply-policy-summary",
        "source-readiness-evaluated-change-list",
        "source-readiness-field-record-list",
        "source-readiness-blocked-condition-list",
        "source-readiness-gate-ref-list",
        "source-readiness-rollback-list",
        "source-readiness-outcome-list",
        "source-readiness-non-execution-list",
        "source-readiness-card",
        "source-readiness-condition-card",
        "source-readiness-gate-card",
        "source-readiness-rollback-card",
        "source-readiness-outcome-card",
    ):
        assert expected in js

    for forbidden in (
        "readinessImport",
        "readinessUpload",
        "readinessRead",
        "readinessRetain",
        "readinessExtract",
        "readinessEmbed",
        "readinessApply",
        "readinessCommit",
        "readinessMutate",
        "readinessClone",
        "readinessConnect",
        "readinessSend",
        "readinessPublish",
        "readinessGenerateMedia",
        '"uses_model_provider": true',
        '"reads_private_sources": true',
        '"retains_raw_source_content": true',
        '"creates_embeddings": true',
        '"performs_extraction": true',
        '"writes_persona_store": true',
        '"writes_persona_version_store": true',
        '"writes_memory_store": true',
        '"writes_review_store": true',
        '"writes_runtime_store": true',
        '"automatic_apply": true',
        '"sends_messages": true',
        '"uses_platform_adapter": true',
        '"uses_media_runtime": true',
    ):
        assert forbidden not in js


def test_static_css_has_source_readiness_grid_and_responsive_rules() -> None:
    css = _asset_text("css")

    for expected in (
        ".source-draft-apply-readiness",
        ".source-readiness-layout",
        ".source-readiness-grid",
        ".source-readiness-card",
        ".source-readiness-condition-card",
        ".source-readiness-gate-card",
        ".source-readiness-rollback-card",
        ".source-readiness-outcome-card",
    ):
        assert expected in css

    assert "@media (max-width: 720px)" in css
    assert ".source-readiness-layout" in css
    assert ".source-readiness-grid" in css
