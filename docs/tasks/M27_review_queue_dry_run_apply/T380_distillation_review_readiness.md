# T380: Distillation Review Readiness Aggregator

## Task ID

T380

## Goal

Implement a local deterministic aggregator for synthetic distillation review
readiness.

T380 should combine `SyntheticDistillationInputManifest`,
`DeidentifiedStyleFeatureCandidate`, and review queue records into a safe
readiness summary. It must not synthesize personas, read real chat logs, retain
source text, call providers, compute embeddings, score real-person similarity,
generate media, send messages, create UI, or connect to platforms.

## Why Now

T377 created review queue records and T378/T379 added dry-run apply plans.
Synthetic distillation still needs a local readiness surface that makes consent,
clone risk, source-text retention, and blocked feature reasons visible before
any later persona synthesis work.

## Allowed Files

Future T380 worker may create or modify only:

- `src/practical_chat_agent/services/distillation_review_readiness.py`
- `tests/test_distillation_review_readiness.py`
- `docs/data_contracts/distillation_review_readiness_contract.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T381_m27_milestone_review.md`
- `docs/worker_summary/T380_worker_summary.md`
- `docs/07_handoff.md`

If T380 needs other source files, fixtures, task-board edits, private data,
Browser runs, model-provider calls, package changes, persistence, routes,
stores, CLIs, platform adapters, outbound messaging, voice/avatar runtime, or
media generation, Captain must revise this package before assignment.

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
- Do not retain source text.
- Do not approve real-person recreation or digital twin behavior.
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
- `docs/data_contracts/review_queue_candidate_contract.md`
- `docs/data_contracts/synthetic_distillation_input_implementation_contract.md`
- `src/practical_chat_agent/services/review_queue.py`
- `src/practical_chat_agent/services/synthetic_distillation_input.py`
- relevant synthetic distillation and review queue tests.

## Expected Outputs

### 1. Readiness Records And Service

Create `src/practical_chat_agent/services/distillation_review_readiness.py`
with:

- `DistillationReadinessIssue`
- `DistillationReviewReadinessSummary`
- `DistillationReviewReadinessService`

Required behavior:

- summarize manifest readiness;
- summarize feature readiness;
- include review queue item refs when supplied;
- block readiness for withdrawn consent, missing active persona-distillation
  consent, clone-risk block, retained source text, blocked features, forbidden
  source categories, and manifest blocking reasons;
- preserve only ids, aliases, labels, safe summaries, and issue codes;
- keep `ready_for_persona_synthesis=false` unless all review-only prerequisites
  are structurally satisfied.

### 2. Tests

Create `tests/test_distillation_review_readiness.py` with synthetic-only tests
that prove:

- active synthetic manifest plus safe feature can produce a review-ready
  summary;
- withdrawn consent blocks readiness;
- clone-risk block prevents readiness;
- retained source text or blocked features prevent readiness;
- missing active persona-distillation consent prevents readiness;
- review queue refs are preserved without applying decisions;
- models reject forbidden private/provider/outbound/media fields;
- service exposes no send/schedule/deliver/provider/synthesis/media methods.

### 3. Data Contract

Create `docs/data_contracts/distillation_review_readiness_contract.md`
describing implemented records, invariants, forbidden fields, tests,
verification, non-actions, and residual risks.

### 4. Next Task Package

Create `docs/tasks/M27_review_queue_dry_run_apply/T381_m27_milestone_review.md`
for M27 milestone review.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T380_worker_summary.md` and append a T380 worker
record to `docs/07_handoff.md`.

Do not mark T380 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\distillation_review_readiness.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_distillation_review_readiness.py tests\test_synthetic_distillation_input_candidates.py tests\test_review_queue_candidates.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial distillation-safety, clone-risk, privacy, review queue,
product-safety, and documentation-accuracy review.

Reviewer should block if T380 reads private data, retains source text, enables
persona synthesis from blocked inputs, calls providers, exposes
send/schedule/deliver/runtime methods, allows private/provider/outbound/media
fields, or implies launch or production readiness.
