# T381: M27 Milestone Review

## Task ID

T381

## Goal

Review M27 Review Queue And Dry-Run Apply outputs before any later milestone
expands into user-facing review UI, real import/de-identification, semantic
retrieval ranking, provider-backed extraction, proactive candidates,
voice/avatar runtime, media generation, platform delivery, or monetization.

T381 is a read-focused adversarial review task. It should inspect the M27
scope, implementation files, tests, data contracts, worker summaries, and
handoff records, then write a milestone review outcome. It must not implement
new product behavior, apply decisions, mutate stores, read private data, call
providers, send messages, generate media, or modify the task board.

## Why Now

T377 through T380 implemented the local review queue, memory lifecycle
dry-run apply plans, persona growth dry-run apply plans, and synthetic
distillation readiness summaries. M27 needs a checkpoint that verifies these
pieces remain review-only and documents residual risks before opening the next
milestone.

## Allowed Files

Future T381 reviewer may create or modify only:

- `docs/review/M27_review.md`
- `docs/worker_summary/T381_worker_summary.md`
- `docs/07_handoff.md`

If T381 needs source edits, test edits, task-board edits, private data,
Browser runs, model-provider calls, package changes, persistence, routes,
stores, CLIs, platform adapters, outbound messaging, voice/avatar runtime, or
media generation, Captain must create a separate fix task package.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not modify source files or tests as part of the review task.
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

- `docs/product/m27_review_queue_dry_run_apply_scope.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T376_m27_scope.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T377_review_queue_candidate_models.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T378_memory_lifecycle_dry_run_apply.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T379_persona_growth_dry_run_apply.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T380_distillation_review_readiness.md`
- `docs/data_contracts/review_queue_candidate_contract.md`
- `docs/data_contracts/memory_lifecycle_dry_run_apply_contract.md`
- `docs/data_contracts/persona_growth_dry_run_apply_contract.md`
- `docs/data_contracts/distillation_review_readiness_contract.md`
- `docs/worker_summary/T376_worker_summary.md`
- `docs/worker_summary/T377_worker_summary.md`
- `docs/worker_summary/T378_worker_summary.md`
- `docs/worker_summary/T379_worker_summary.md`
- `docs/worker_summary/T380_worker_summary.md`
- M27 implementation and focused test files.

## Expected Outputs

### 1. Milestone Review

Create `docs/review/M27_review.md` with:

- verdict: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- reviewed files and tests;
- issues found, if any, ordered by severity;
- verification commands and observed results;
- explicit non-actions confirmed;
- residual risks and recommended next milestone gates.

Reviewer should block if M27 reads private data, retains source text in
readiness summaries, mutates memory/persona state, applies review decisions,
calls providers, exposes send/schedule/deliver/provider/runtime/media methods,
allows private/provider/outbound/media fields, or implies launch or production
readiness.

### 2. Worker Summary And Handoff

Write `docs/worker_summary/T381_worker_summary.md` and append a T381 reviewer
record to `docs/07_handoff.md`.

Do not mark M27 or T381 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_queue_candidates.py tests\test_memory_lifecycle_dry_run_apply.py tests\test_persona_growth_dry_run_apply.py tests\test_distillation_review_readiness.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial milestone review for privacy, clone-risk, review-only semantics,
dry-run safety, product-safety, and documentation accuracy.
