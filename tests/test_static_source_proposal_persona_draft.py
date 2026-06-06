"""T461 static source proposal persona draft rendering tests.

These tests inspect local static assets only. They do not call providers, read
private data, retain raw source content, create embeddings, extract traits,
write stores, apply persona changes, send messages, connect adapters, or enable
media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


REQUIRED_DRAFT_PATHS = (
    "style.tone",
    "style.pacing",
    "style.humor",
    "relationship.boundary_style",
    "memory.use_preference",
    "growth.short_term_hint",
)

REQUIRED_OUTCOMES = (
    "needs_manual_review",
    "blocked_by_policy",
    "ready_for_future_apply_design",
)


def _paths() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _asset_text(name: str) -> str:
    return Path(_paths()[name]).read_text(encoding="utf-8")


def test_static_html_exposes_source_proposal_persona_draft_section_and_targets() -> None:
    html = _asset_text("html")

    for expected in (
        'id="source-proposal-persona-draft"',
        'id="source-draft-title"',
        'id="source-draft-schema"',
        'id="source-draft-non-execution-list"',
        'id="source-draft-proposal-summary"',
        'id="source-draft-base-snapshot"',
        'id="source-draft-selected-proposal-list"',
        'id="source-draft-field-change-list"',
        'id="source-draft-unchanged-field-list"',
        'id="source-draft-conflict-list"',
        'id="source-draft-rollback-list"',
        'id="source-draft-gate-list"',
        'id="source-draft-outcome-list"',
    ):
        assert expected in html


def test_static_js_fallback_contains_source_proposal_persona_draft_contract_values() -> None:
    js = _asset_text("js")

    assert "source_proposal_persona_draft" in js
    assert "m42.source_proposal_persona_draft.v1" in js
    assert "drawSourceProposalPersonaDraft" in js
    for field_path in REQUIRED_DRAFT_PATHS:
        assert field_path in js
    for outcome in REQUIRED_OUTCOMES:
        assert outcome in js


def test_static_js_renders_draft_lists_without_action_controls() -> None:
    js = _asset_text("js")

    for expected in (
        "source-draft-proposal-summary",
        "source-draft-base-snapshot",
        "source-draft-selected-proposal-list",
        "source-draft-field-change-list",
        "source-draft-unchanged-field-list",
        "source-draft-conflict-list",
        "source-draft-rollback-list",
        "source-draft-gate-list",
        "source-draft-outcome-list",
        "source-draft-non-execution-list",
        "source-draft-card",
        "source-draft-unchanged-card",
        "source-draft-conflict-card",
        "source-draft-rollback-card",
        "source-draft-gate-card",
        "source-draft-outcome-card",
    ):
        assert expected in js

    for forbidden in (
        "draftImport",
        "draftUpload",
        "draftRead",
        "draftRetain",
        "draftExtract",
        "draftEmbed",
        "draftApply",
        "draftCommit",
        "draftMutate",
        "draftClone",
        "draftConnect",
        "draftSend",
        "draftPublish",
        "draftGenerateMedia",
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


def test_static_css_has_source_draft_grid_and_responsive_rules() -> None:
    css = _asset_text("css")

    for expected in (
        ".source-proposal-persona-draft",
        ".source-draft-layout",
        ".source-draft-grid",
        ".source-draft-card",
        ".source-draft-unchanged-card",
        ".source-draft-conflict-card",
        ".source-draft-rollback-card",
        ".source-draft-gate-card",
        ".source-draft-outcome-card",
    ):
        assert expected in css

    assert "@media (max-width: 720px)" in css
    assert ".source-draft-layout" in css
    assert ".source-draft-grid" in css
