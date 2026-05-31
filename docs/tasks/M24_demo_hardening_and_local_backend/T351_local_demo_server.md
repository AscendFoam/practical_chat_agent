# T351: Local Demo Server

## Task ID

T351

## Goal

Implement a dependency-free local run path for the text-first web demo so
reviewers can load adapter-generated synthetic state through a stable local
preview instead of relying only on static fallback state.

## Why Now

M23 proved the static shell and scenario switching. M24 should first make the
demo easier to run and inspect locally, before changing labels, accessibility,
or layout behavior.

## Allowed Files

Future T351 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_local_server.py`
- `tests/test_text_first_web_demo_local_server.py`
- `docs/data_contracts/local_web_demo_server_contract.md`
- `docs/tasks/M24_demo_hardening_and_local_backend/T352_friendly_labels_accessibility_contract.md`
- `docs/worker_summary/T351_worker_summary.md`
- `docs/07_handoff.md`

If T351 needs CSS/JS/HTML changes, package-manager dependencies, browser QA,
model-provider calls, generated media, voice/avatar runtime, private data
processing, task-board edits, platform adapters, outbound messaging, screenshot
artifacts, or launch claims, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers.
- Do not synthesize audio, generate images/video, clone voices/faces, capture
  microphone/camera input, or process media samples.
- Do not add external network assets or package-manager dependencies.
- Do not add production backend routes, persistence, platform delivery, push
  notification, send, schedule, queue, webhook, token, adapter, or realtime
  fields.
- Do not enable voice, avatar, Live2D, camera, microphone, ASR, TTS, or media
  runtime.
- Do not modify `docs/04_task_board.md`.
- Do not claim legal advice, compliance completion, app-store approval, launch
  approval, user-study validation, regulator acceptance, or real user evidence.

## Inputs To Read

Required:

- `docs/product/m24_demo_hardening_scope.md`
- `docs/review/M23_review.md`
- `docs/data_contracts/text_first_web_demo_state_contract.md`
- `docs/data_contracts/static_web_demo_shell_contract.md`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/text_first_web_demo_static.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_adapter.py`

## Expected Outputs

### 1. Local Server Helper

Create `src/practical_chat_agent/ui/text_first_web_demo_local_server.py` with a
small dependency-free helper that can:

- render adapter-backed HTML for `/`;
- serve the existing local CSS and JS assets;
- optionally expose synthetic adapter payload JSON at a review-only local route;
- return explicit content types;
- reject path traversal;
- expose a testable route/response function that does not require a long-lived
  server process in unit tests.

Acceptable standard-library building blocks include `http.server`, `dataclasses`,
`pathlib`, and `json`. Do not introduce a web framework.

### 2. Tests

Create `tests/test_text_first_web_demo_local_server.py` covering:

- root route returns HTML containing adapter-generated state;
- CSS route returns CSS content type and local CSS;
- JS route returns JavaScript content type and local JS;
- optional JSON state route returns synthetic state and `review_required=true`;
- unknown path returns a not-found response;
- path traversal is rejected;
- response bodies contain no provider credentials, private chat text, generated
  media paths, platform delivery fields, send queues, schedules, webhooks,
  microphone/camera prompts, or runtime voice/avatar enablement.

Use repo-local pytest cache and basetemp paths during verification.

### 3. Data Contract

Create `docs/data_contracts/local_web_demo_server_contract.md` documenting:

- routes;
- response types;
- synthetic-data source;
- no-runtime boundaries;
- forbidden fields and non-actions;
- local-only run assumptions.

### 4. Next Task Package

Create
`docs/tasks/M24_demo_hardening_and_local_backend/T352_friendly_labels_accessibility_contract.md`
for friendly labels and accessibility contract work.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T351_worker_summary.md` and append a T351 worker
record to `docs/07_handoff.md`.

Do not mark T351 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_local_server.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_adapter.py -q -o cache_dir=artifacts\t351_pytest_cache --basetemp=artifacts\t351_pytest_basetemp
```

```powershell
git diff --check
```

Browser verification is not required for T351 unless the task package is revised
to allow Browser QA. T354 is expected to cover Browser QA for the M24 local run
path.

## Reviewer Type

Adversarial architecture and product/safety UX review recommended.

Reviewer should block if the local server reads private data, calls providers,
adds write/send/schedule/platform routes, enables voice/avatar/media runtime,
uses external dependencies, serves files outside the static asset directory, or
claims production readiness.

