# T376: M27 Review Queue And Dry-Run Apply Scope

## Task ID

T376

## Goal

Define the M27 milestone scope and create the first M27 implementation task
package.

M27 should turn M26 candidate records into local review queue and dry-run apply
foundations without adding private-data ingestion, provider calls, runtime
mutation, proactive outreach, platform delivery, voice/avatar behavior, media
generation, or real-person recreation.

## Allowed Files

Future T376 worker may create or modify only:

- `docs/product/m27_review_queue_dry_run_apply_scope.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T377_review_queue_candidate_models.md`
- `docs/worker_summary/T376_worker_summary.md`
- `docs/07_handoff.md`

If T376 needs Python source, tests, fixtures, private data, Browser runs,
provider calls, package changes, task-board edits, routes, stores, CLIs,
persistence behavior, outbound messaging, platform adapters, voice/avatar
runtime, or media generation, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not add or modify Python source code or tests in T376.
- Do not call model providers.
- Do not implement review queue models, dry-run planners, UI, routes, CLIs,
  stores, schedulers, queues, webhooks, auth, tokens, recipient ids, delivery
  state, microphone, camera, ASR, TTS, voice cloning, voice/avatar likeness,
  Live2D, generated audio, generated image, generated video, or media capture.
- Do not implement real-person recreation, authorized digital twin support,
  grief/deceased-person resurrection, ex-partner clone, family-member clone, or
  public-figure imitation.
- Do not modify `docs/04_task_board.md`.
- Do not claim launch approval, legal compliance, app-store acceptance,
  clinical validation, regulator acceptance, user-study validation, or real
  user evidence.

## Inputs To Read

Required:

- `docs/review/M26_review.md`
- `docs/product/m26_memory_persona_implementation_scope.md`
- `docs/data_contracts/memory_governance_candidate_contract.md`
- `docs/data_contracts/persona_growth_candidate_implementation_contract.md`
- `docs/data_contracts/synthetic_distillation_input_implementation_contract.md`
- `docs/data_contracts/memory_retrieval_explanation_integration_contract.md`
- `docs/worker_summary/T371_worker_summary.md`
- `docs/worker_summary/T372_worker_summary.md`
- `docs/worker_summary/T373_worker_summary.md`
- `docs/worker_summary/T374_worker_summary.md`
- `docs/worker_summary/T375_worker_summary.md`

## Expected Outputs

### 1. M27 Scope

Create `docs/product/m27_review_queue_dry_run_apply_scope.md` covering:

- objective and rationale;
- M26 invariants to preserve;
- implementation sequence T377-T381;
- synthetic fixture strategy;
- acceptance gates;
- non-goals;
- exit criteria;
- residual risks.

### 2. T377 Task Package

Create
`docs/tasks/M27_review_queue_dry_run_apply/T377_review_queue_candidate_models.md`
for local review queue candidate records and tests.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T376_worker_summary.md` and append a T376 worker
record to `docs/07_handoff.md`.

Do not mark T376 complete in `docs/04_task_board.md`.

## Verification

Minimum command:

```powershell
git diff --check
```

## Reviewer Type

Adversarial milestone-scope, product-safety, privacy, memory lifecycle,
persona-safety, distillation-safety, and documentation-accuracy review.

Reviewer should block if T376 recommends private-data ingestion,
provider-backed extraction, runtime mutation, automatic sending, platform
delivery, voice/avatar runtime, generated media, real-person recreation,
commercial launch claims, or legal/clinical/regulatory claims.
