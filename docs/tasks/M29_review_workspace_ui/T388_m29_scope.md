# T388: M29 Review Workspace Presentation Scope

## Task ID

T388

## Goal

Open M29 for a local review workspace presentation layer.

T388 should define the product and engineering scope for turning M28 review
workspace records into safe, UI-ready presentation models and a local static
review panel. It must not implement UI code, mutate memory/persona state, call
providers, send messages, read private data, or connect to platforms/media.

## Why Now

M28 closed with `PASS_WITH_WARNINGS` and recommended keeping the next milestone
focused on a local review UI or presentation adapter before any mutation
executor. T388 records that scope and creates the first implementation task.

## Allowed Files

Future T388 worker may create or modify only:

- `docs/product/m29_review_workspace_ui_scope.md`
- `docs/tasks/M29_review_workspace_ui/T388_m29_scope.md`
- `docs/tasks/M29_review_workspace_ui/T389_review_workspace_presentation_adapter.md`
- `docs/worker_summary/T388_worker_summary.md`
- `docs/07_handoff.md`

If T388 needs source edits, tests, task-board edits, private data, Browser
runs, model-provider calls, package changes, routes, CLIs, platform adapters,
outbound messaging, voice/avatar runtime, media generation, persistence, or
apply executors, Captain must create a separate implementation task package.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not modify source files or tests as part of this scope task.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, runtime persona mutation, or
  runtime memory mutation.
- Do not apply review decisions or dry-run plans.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not create UI, routes, CLIs, schedulers, queues, webhooks, auth, tokens,
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

- `docs/review/M28_review.md`
- `docs/product/m28_local_review_workspace_scope.md`
- M28 data contracts and worker summaries.

## Expected Outputs

### 1. Scope Document

Create `docs/product/m29_review_workspace_ui_scope.md` with:

- objective;
- why M29 follows M28;
- product rationale;
- invariants to preserve;
- implementation sequence;
- synthetic fixture strategy;
- acceptance gates;
- explicit non-goals;
- exit criteria;
- residual risks.

### 2. Next Task Package

Create
`docs/tasks/M29_review_workspace_ui/T389_review_workspace_presentation_adapter.md`
for local review workspace presentation view models.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T388_worker_summary.md` and append a T388 worker
record to `docs/07_handoff.md`.

Do not mark T388 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial milestone-scope review for product safety, privacy, non-apply
safety, UI-scope containment, and documentation accuracy.
