# T395 Worker Summary

Task: T395 Local Visual QA Fallback
Status: worker draft for review

## Files Changed

- `src/practical_chat_agent/ui/text_first_web_demo_static.py`
- `tests/test_review_workspace_visual_qa_fallback.py`
- `docs/data_contracts/review_workspace_visual_qa_fallback_contract.md`
- `docs/tasks/M30_review_workspace_hardening/T396_manual_apply_preview_scope.md`
- `docs/worker_summary/T395_worker_summary.md`
- `docs/07_handoff.md`

## Work Completed

- Added tests for a deterministic local review workspace QA snapshot.
- Verified RED before implementation:
  - `$env:PYTHONPATH='src'; pytest tests\test_review_workspace_visual_qa_fallback.py -q -o cache_dir=artifacts\t395_pytest_cache --basetemp=artifacts\t395_pytest_basetemp`
  - Result before implementation: failed with `3 failed` because
    `TextFirstWebDemoStaticShell` did not expose
    `build_review_workspace_qa_snapshot`.
- Added `TextFirstWebDemoStaticShell.build_review_workspace_qa_snapshot`.
- Snapshot verifies static review targets, adapter-backed review cards, status
  tones, blocker text, safe export text, and action-control absence.
- Created the visual QA fallback contract.
- Created T396 for manual apply preview scoping.

## Verification

Focused GREEN:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_static.py
```

Result: passed.

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_visual_qa_fallback.py tests\test_review_workspace_static_panel.py -q -o cache_dir=artifacts\t395_pytest_cache --basetemp=artifacts\t395_pytest_basetemp
```

Result: passed, `9 passed`.

Full T395 verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_static.py
```

Result: passed.

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_visual_qa_fallback.py tests\test_review_workspace_static_panel.py -q -o cache_dir=artifacts\t395_pytest_cache --basetemp=artifacts\t395_pytest_basetemp
```

Result: passed, `9 passed`.

```powershell
git diff --check
```

Result: passed with CRLF warnings only.

## Explicit Non-Actions

- No screenshot capture, browser automation, package install, local server
  route, private data reader, source ingestion from real logs, extraction,
  embedding, vector search, retrieval ranking, similarity scoring,
  model-provider call, PersonaCard synthesis, final reply generation,
  proactive candidate, scheduler, queue persistence, webhook, token, platform
  adapter, outbound messaging, voice/avatar runtime, media generation,
  package-manager dependency, or task-board edit was added.
- No review decision apply path, memory store mutation, PersonaCard mutation,
  PersonaVersionStore write, deletion executor, retrieval enablement, or
  provider-backed payload was added.
- No legal advice, compliance completion, app-store approval, launch approval,
  user-study validation, real user evidence, or regulator acceptance was
  claimed.
- No `private/chat_history/`, `private/distilled/`, or private artifact
  content was read, quoted, summarized, transformed, or committed.

## Remaining Risks

- Snapshot QA is structured local evidence, not rendered screenshot evidence.
- It cannot catch CSS overlap, viewport framing, or real click behavior.
- Browser visual QA should still be performed when local navigation is
  available.
- Manual apply preview remains unscoped until T396.
