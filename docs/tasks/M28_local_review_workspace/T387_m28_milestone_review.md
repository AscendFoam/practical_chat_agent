# T387: M28 Milestone Review

## Task ID

T387

## Goal

Review M28 Local Review Workspace outputs before any later milestone expands
into user-facing review UI, real import/de-identification, semantic retrieval
ranking, provider-backed extraction, proactive candidates, voice/avatar
runtime, media generation, platform delivery, monetization, or real apply
executors.

T387 is a read-focused adversarial review task. It should inspect the M28
scope, implementation files, tests, data contracts, worker summaries, and
handoff records, then write a milestone review outcome. It must not implement
new product behavior, apply decisions, mutate stores, read private data, call
providers, send messages, generate media, or modify the task board.

## Why Now

T382 through T386 implemented the M28 local review workspace foundation:
scope, candidate/artifact bindings, local snapshot storage, review decision
impact previews, and safe export manifests. M28 needs a checkpoint that
verifies these pieces remain review-only and documents residual risks before
opening the next milestone.

## Allowed Files

Future T387 reviewer may create or modify only:

- `docs/review/M28_review.md`
- `docs/worker_summary/T387_worker_summary.md`
- `docs/07_handoff.md`

If T387 needs source edits, test edits, task-board edits, private data,
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

- `docs/product/m28_local_review_workspace_scope.md`
- `docs/tasks/M28_local_review_workspace/T382_m28_scope.md`
- `docs/tasks/M28_local_review_workspace/T383_review_workspace_bindings.md`
- `docs/tasks/M28_local_review_workspace/T384_review_workspace_snapshot_store.md`
- `docs/tasks/M28_local_review_workspace/T385_review_decision_impact_preview.md`
- `docs/tasks/M28_local_review_workspace/T386_review_workspace_safe_export.md`
- `docs/data_contracts/review_workspace_binding_contract.md`
- `docs/data_contracts/review_workspace_snapshot_store_contract.md`
- `docs/data_contracts/review_decision_impact_preview_contract.md`
- `docs/data_contracts/review_workspace_safe_export_contract.md`
- `docs/worker_summary/T382_worker_summary.md`
- `docs/worker_summary/T383_worker_summary.md`
- `docs/worker_summary/T384_worker_summary.md`
- `docs/worker_summary/T385_worker_summary.md`
- `docs/worker_summary/T386_worker_summary.md`
- M28 implementation and focused test files.

## Expected Outputs

### 1. Milestone Review

Create `docs/review/M28_review.md` with:

- verdict: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- reviewed files and tests;
- issues found, if any, ordered by severity;
- verification commands and observed results;
- explicit non-actions confirmed;
- residual risks and recommended next milestone gates.

Reviewer should block if M28 reads private data, exports raw private content,
mutates memory/persona state, applies review decisions, calls providers,
exposes send/schedule/deliver/provider/runtime/media methods, allows
private/provider/outbound/media fields, or implies launch or production
readiness.

### 2. Worker Summary And Handoff

Write `docs/worker_summary/T387_worker_summary.md` and append a T387 reviewer
record to `docs/07_handoff.md`.

Do not mark M28 or T387 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_bindings.py tests\test_review_workspace_snapshot_store.py tests\test_review_decision_impact_preview.py tests\test_review_workspace_safe_export.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial milestone review for privacy, review-only semantics, binding
correctness, path safety, safe export safety, dry-run safety, product-safety,
and documentation accuracy.
