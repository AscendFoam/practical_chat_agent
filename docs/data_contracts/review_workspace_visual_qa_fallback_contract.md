# Review Workspace Visual QA Fallback Contract

Task: T395 Local Visual QA Fallback
Status: worker draft for review

## Scope

This contract describes the deterministic local QA snapshot added to
`TextFirstWebDemoStaticShell`:

- `build_review_workspace_qa_snapshot(user_id=...)`

The snapshot exists because browser navigation to local files/localhost was
blocked in this environment during M29. It is not screenshot evidence and does
not replace a browser/manual visual check when that path is available.

## Implemented Snapshot

The snapshot returns:

- `schema_version=review_workspace_visual_qa_snapshot_v1`
- `user_id`
- `static_targets`
- `projection_policy`
- `filter_tabs`
- `card_count`
- `card_titles`
- `status_tones`
- `status_badge_text`
- `blocker_text`
- `safe_export_text`
- `action_controls_present`
- `browser_screenshot=false`
- `local_snapshot_only=true`

`static_targets` confirms the static shell contains:

- `#tab-review`
- `#review-panel`
- `#review-filters`
- `#review-workspace-list`
- `#review-export-summary`

The review card data comes from the same synthetic adapter-backed payload used
by `/demo-state.json`.

## Required Invariants

- Snapshot generation is local and deterministic.
- Snapshot generation does not start a browser or server.
- Snapshot generation does not read private files.
- Snapshot generation does not call providers.
- Snapshot generation does not write files.
- Snapshot generation does not apply decisions or mutate memory/persona state.
- Snapshot data must not contain private/provider/outbound/media fields.
- Snapshot data must report whether review action controls are present.

## Tests

Implemented tests:

- `tests/test_review_workspace_visual_qa_fallback.py`

Covered behavior:

- snapshot includes review static targets;
- snapshot includes review cards and key titles;
- snapshot includes blocked and eligible status tones;
- snapshot includes blocker text and safe export text;
- snapshot reports no action controls;
- snapshot contains no forbidden private/provider/outbound/media fields.

Regression tests also run:

- `tests/test_review_workspace_static_panel.py`

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_static.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_visual_qa_fallback.py tests\test_review_workspace_static_panel.py -q -o cache_dir=artifacts\t395_pytest_cache --basetemp=artifacts\t395_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T395 does not implement:

- screenshot capture;
- browser automation;
- package installs;
- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- PersonaCard synthesis;
- final companion reply generation;
- runtime memory or persona mutation;
- decision apply paths;
- deletion executors;
- new local server routes;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- This is structured local QA evidence, not a rendered screenshot.
- It cannot catch CSS overlap, viewport framing, or real click behavior.
- Browser visual QA should still be performed when local navigation is
  available.
- Manual apply preview remains unscoped until T396.
