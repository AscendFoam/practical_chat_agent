# T390: Review Workspace Static Panel

## Task ID

T390

## Goal

Add a local static review workspace panel to the existing text-first web demo
assets.

T390 should consume a synthetic, UI-ready payload from the T389 presentation
adapter and render review items, blocker states, decision outcomes, and safe
export counts in the local static demo. It must remain local-only, synthetic,
non-sending, non-mutating, and accessible.

## Why Now

T389 produces UI-ready presentation models in Python. T390 can now bind those
models to the existing static demo shell without adding providers, private
data, platform delivery, voice/avatar runtime, generated media, or apply
executors.

## Allowed Files

Future T390 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_review_workspace_static_panel.py`
- `docs/data_contracts/review_workspace_static_panel_contract.md`
- `docs/tasks/M29_review_workspace_ui/T391_review_workspace_local_server_payload.md`
- `docs/worker_summary/T390_worker_summary.md`
- `docs/07_handoff.md`

If T390 needs other source files, fixtures, task-board edits, private data,
Browser runs beyond local static QA, model-provider calls, package changes,
routes, CLIs, platform adapters, outbound messaging, voice/avatar runtime,
media generation, persistence outside local static assets, or apply executors,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, runtime persona mutation, or
  runtime memory mutation.
- Do not apply review decisions or dry-run plans.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not add routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.
- Do not claim launch approval, legal compliance, app-store acceptance,
  clinical validation, regulator acceptance, user-study validation, or real
  user evidence.

## Inputs To Read

Required:

- `docs/product/m29_review_workspace_ui_scope.md`
- `docs/data_contracts/review_workspace_presentation_contract.md`
- `src/practical_chat_agent/ui/review_workspace_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- existing web demo static/accessibility tests.

## Expected Outputs

### 1. Static Review Panel

Modify the static web demo assets to add a local review workspace panel that:

- has a stable tab/section for review workspace cards;
- renders synthetic presentation cards from a local fixture payload;
- displays status badges for blocked, eligible, review, and info states;
- displays blocker codes and safe summaries;
- displays safe export counts;
- preserves review-required, preview-only, and non-apply labels;
- keeps layout responsive and accessible;
- does not introduce nested cards, marketing hero sections, decorative orbs,
  or text overlap.

### 2. Tests

Create `tests/test_review_workspace_static_panel.py` with tests that prove:

- static assets include the review workspace panel target;
- JS fixture data contains review workspace cards and filter tabs;
- blocked and eligible states are renderable;
- forbidden private/provider/outbound/media fields are absent;
- the panel does not expose send/schedule/deliver/apply/provider/mutation or
  media controls.

### 3. Data Contract

Create `docs/data_contracts/review_workspace_static_panel_contract.md`
describing implemented static panel behavior, data assumptions, forbidden
fields, tests, verification, non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M29_review_workspace_ui/T391_review_workspace_local_server_payload.md`
for integrating the review workspace presentation payload with the existing
local demo server if needed.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T390_worker_summary.md` and append a T390 worker
record to `docs/07_handoff.md`.

Do not mark T390 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_static_panel.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_accessibility.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial static UI review for privacy, non-apply safety, accessibility,
responsive layout, product-safety, and documentation accuracy.
