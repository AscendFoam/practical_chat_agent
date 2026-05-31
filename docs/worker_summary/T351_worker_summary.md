# T351 Worker Summary

## Changed

- Added `tests/test_text_first_web_demo_local_server.py`.
- Added `src/practical_chat_agent/ui/text_first_web_demo_local_server.py`.
- Added `docs/data_contracts/local_web_demo_server_contract.md`.
- Added
  `docs/tasks/M24_demo_hardening_and_local_backend/T352_friendly_labels_accessibility_contract.md`.
- Appended the T351 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## Implementation Result

T351 adds a dependency-free local route helper:

- root `/` and `/text_first_web_demo.html` return adapter-backed HTML;
- `/demo-state.json` returns synthetic adapter payload JSON;
- CSS and JS routes return existing local static assets with explicit content
  types;
- unknown routes return `404`;
- decoded path traversal and backslash paths return `403`;
- responses include `Cache-Control: no-store`;
- `build_http_server(...)` can create a standard-library local HTTP server for
  review tooling;
- unit tests validate routes without keeping a server process alive.

## TDD Evidence

RED command:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t351_pytest_cache_red --basetemp=artifacts\t351_pytest_basetemp_red
```

Result: failed as expected because
`practical_chat_agent.ui.text_first_web_demo_local_server` did not exist.

GREEN command:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t351_pytest_cache_green --basetemp=artifacts\t351_pytest_basetemp_green
```

Result: passed, `6 passed`.

## Explicit Non-Actions

- No static UI edit, browser QA, model-provider call, final reply generation,
  private data processing, voice/avatar runtime, media generation, external
  network asset, package manager, platform adapter, outbound messaging,
  screenshot artifact, or task-board edit was added.
- No legal advice, compliance completion, app-store approval, launch approval,
  user-study validation, real user evidence, or regulator acceptance was
  claimed.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- T351 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_local_server.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t351_pytest_cache --basetemp=artifacts\t351_pytest_basetemp
```

Result: passed, `17 passed`.

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Remaining Risks

- Browser verification of the local run path is deferred to a later M24 task.
- T351 does not change friendly labels, keyboard behavior, accessibility
  semantics, or responsive layout.
- The helper is local review infrastructure, not a production server.

## Recommended Reviewer Type

Adversarial architecture and product/safety UX review.
