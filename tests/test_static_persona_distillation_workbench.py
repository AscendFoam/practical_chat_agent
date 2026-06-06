"""T425 static persona distillation workbench rendering tests.

These tests inspect local static assets only. They do not call providers, read
private data, write stores, apply traits, send messages, connect adapters, or
enable media runtime.
"""

from __future__ import annotations

from pathlib import Path

from practical_chat_agent.ui.text_first_web_demo_static import TextFirstWebDemoStaticShell


REQUIRED_MODE_IDS = (
    "detailed_description",
    "fuzzy_seed",
    "synthetic_dialogue_excerpt",
    "random_fictional_seed",
)

REQUIRED_TRAIT_CATEGORIES = (
    "tone",
    "pacing",
    "attachment_style",
    "humor_style",
    "boundary_style",
    "topic_affinity",
    "taboo_pattern",
    "memory_use_preference",
    "growth_hint",
)

REQUIRED_BLOCKED_TYPES = (
    "real_person_clone_or_replacement",
    "deception_or_impersonation",
    "private_import_without_consent",
)


def _paths() -> dict[str, str]:
    return TextFirstWebDemoStaticShell().asset_paths()


def _asset_text(name: str) -> str:
    return Path(_paths()[name]).read_text(encoding="utf-8")


def test_static_html_exposes_persona_workbench_section_and_targets() -> None:
    html = _asset_text("html")

    for expected in (
        'id="persona-workbench"',
        'id="workbench-title"',
        'id="workbench-schema"',
        'id="workbench-mode-list"',
        'id="workbench-input-list"',
        'id="workbench-evidence-list"',
        'id="workbench-trait-list"',
        'id="workbench-blocked-list"',
        'id="workbench-gate-list"',
        'id="workbench-non-execution-list"',
    ):
        assert expected in html


def test_static_js_fallback_contains_workbench_contract_values() -> None:
    js = _asset_text("js")

    assert "persona_distillation_workbench" in js
    assert "m36.persona_distillation_workbench.v1" in js
    assert "drawPersonaWorkbench" in js
    for mode_id in REQUIRED_MODE_IDS:
        assert mode_id in js
    for category in REQUIRED_TRAIT_CATEGORIES:
        assert category in js
    for request_type in REQUIRED_BLOCKED_TYPES:
        assert request_type in js


def test_static_js_renders_workbench_lists_without_action_controls() -> None:
    js = _asset_text("js")

    for expected in (
        "workbench-mode-list",
        "workbench-input-list",
        "workbench-evidence-list",
        "workbench-trait-list",
        "workbench-blocked-list",
        "workbench-gate-list",
        "workbench-non-execution-list",
        "workbench-trait-card",
        "workbench-blocked-card",
    ):
        assert expected in js

    for forbidden in (
        "workbenchApply",
        "workbenchClone",
        "workbenchUpload",
        "workbenchRecord",
        "workbenchConnect",
        "workbenchSend",
        "workbenchPublish",
        "workbenchGenerateMedia",
        '"uses_model_provider": true',
        '"reads_private_sources": true',
        '"writes_runtime_store": true',
        '"automatic_apply": true',
        '"sends_messages": true',
        '"uses_platform_adapter": true',
        '"uses_media_runtime": true',
    ):
        assert forbidden not in js


def test_static_css_has_workbench_grid_and_responsive_rules() -> None:
    css = _asset_text("css")

    for expected in (
        ".persona-workbench",
        ".workbench-layout",
        ".workbench-trait-grid",
        ".workbench-blocked-grid",
        ".workbench-trait-card",
        ".workbench-blocked-card",
    ):
        assert expected in css

    assert ".workbench-layout" in css
    assert "@media (max-width: 720px)" in css
    assert ".workbench-trait-grid" in css
