# T382: M28 Local Review Workspace Scope

## Task ID

T382

## Goal

Define the M28 local review workspace milestone and create the first
implementation task package.

T382 is docs-only / scope-only. It must not modify implementation code, tests,
stores, CLIs, routes, UI, provider integrations, platform adapters, outbound
messaging, voice/avatar runtime, media behavior, or private data.

## Why Now

M27 closed with `PASS_WITH_WARNINGS`. The next milestone should address the
review warnings by making candidate bindings and safe workspace grouping
explicit before any future review UI, persistence, or apply executor.

## Allowed Files

Future T382 worker may create or modify only:

- `docs/product/m28_local_review_workspace_scope.md`
- `docs/tasks/M28_local_review_workspace/T382_m28_scope.md`
- `docs/tasks/M28_local_review_workspace/T383_review_workspace_bindings.md`
- `docs/worker_summary/T382_worker_summary.md`
- `docs/07_handoff.md`

If T382 needs source files, tests, task-board edits, private data, Browser
runs, model-provider calls, package changes, persistence, routes, stores, CLIs,
platform adapters, outbound messaging, voice/avatar runtime, or media
generation, Captain must revise this package before assignment.

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
- Do not create UI, routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or persistence behavior.
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

- `docs/review/M27_review.md`
- `docs/product/m27_review_queue_dry_run_apply_scope.md`
- `docs/data_contracts/review_queue_candidate_contract.md`
- `docs/data_contracts/memory_lifecycle_dry_run_apply_contract.md`
- `docs/data_contracts/persona_growth_dry_run_apply_contract.md`
- `docs/data_contracts/distillation_review_readiness_contract.md`
- `docs/07_handoff.md`

## Expected Outputs

### 1. M28 Product Scope

Create `docs/product/m28_local_review_workspace_scope.md` describing:

- objective and product rationale;
- M27 warnings addressed by M28;
- invariants preserved from M27;
- implementation sequence;
- local synthetic fixture strategy;
- acceptance gates;
- explicit non-goals;
- M28 exit criteria;
- residual risks.

### 2. First Implementation Task Package

Create `docs/tasks/M28_local_review_workspace/T383_review_workspace_bindings.md`
for local review workspace binding records and tests.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T382_worker_summary.md` and append a T382 worker
record to `docs/07_handoff.md`.

Do not mark T382 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial product-scope, review-only semantics, privacy, dry-run safety, and
documentation-accuracy review.
