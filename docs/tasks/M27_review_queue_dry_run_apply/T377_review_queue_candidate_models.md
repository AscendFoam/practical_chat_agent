# T377: Review Queue Candidate Models

## Task ID

T377

## Goal

Implement local deterministic review queue records that can wrap M26 candidate
records into a unified synthetic review queue.

T377 should create a small service for queueing memory-governance,
persona-growth, and synthetic distillation candidates as review items. It must
not apply decisions, mutate stores, write persona versions, call providers,
read private data, send messages, create UI, or connect to platforms/media.

## Why Now

M26 produced several candidate record families, but they are not yet unified
for review. M27 starts by making a common review queue shape so later tasks can
dry-run apply decisions without building runtime mutation paths.

## Allowed Files

Future T377 worker may create or modify only:

- `src/practical_chat_agent/services/review_queue.py`
- `tests/test_review_queue_candidates.py`
- `docs/data_contracts/review_queue_candidate_contract.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T378_memory_lifecycle_dry_run_apply.md`
- `docs/worker_summary/T377_worker_summary.md`
- `docs/07_handoff.md`

If T377 needs other source files, fixtures, task-board edits, private data,
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
- Do not modify existing store mutation semantics.
- Do not apply review decisions.
- Do not write PersonaVersionStore records.
- Do not create UI, routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not implement real-person recreation, authorized digital twin support,
  grief/deceased-person resurrection, ex-partner clone, family-member clone, or
  public-figure imitation.
- Do not modify `docs/04_task_board.md`.
- Do not claim launch approval, legal compliance, app-store acceptance,
  clinical validation, regulator acceptance, user-study validation, or real
  user evidence.

## Inputs To Read

Required:

- `docs/product/m27_review_queue_dry_run_apply_scope.md`
- `docs/review/M26_review.md`
- `docs/data_contracts/memory_governance_candidate_contract.md`
- `docs/data_contracts/persona_growth_candidate_implementation_contract.md`
- `docs/data_contracts/synthetic_distillation_input_implementation_contract.md`
- `docs/data_contracts/memory_retrieval_explanation_integration_contract.md`
- `src/practical_chat_agent/services/memory_governance.py`
- `src/practical_chat_agent/services/persona_growth.py`
- `src/practical_chat_agent/services/synthetic_distillation_input.py`
- `src/practical_chat_agent/services/memory_retrieval_explanation.py`
- relevant existing M26 tests.

## Expected Outputs

### 1. Review Queue Records And Service

Create `src/practical_chat_agent/services/review_queue.py` with local Pydantic
records and deterministic helpers:

- `ReviewQueueItem`
- `ReviewQueueSnapshot`
- `ReviewQueueDecisionRecord`
- `ReviewQueueService`

Required behavior:

- wrap memory contradiction, memory supersession, deletion cascade,
  persona-growth evidence, persona-growth patch, synthetic distillation
  manifest, de-identified style feature, and retrieval explanation results;
- preserve candidate ids and source refs;
- expose safe display summaries and reason labels;
- compute simple deterministic priority from candidate type and risk labels;
- provide queue snapshot ordering by priority and created time;
- record approve/reject/freeze/request-changes decisions as review records
  only;
- reject extra private/provider/outbound/platform/media fields;
- expose no runtime delivery, provider, mutation, voice/avatar, or media
  methods.

### 2. Tests

Create `tests/test_review_queue_candidates.py` with synthetic-only tests that
prove:

- governance, persona-growth, and synthetic distillation candidates can be
  wrapped as review items;
- queue snapshots sort high-risk or deletion items before routine items;
- decision records do not apply changes;
- blocked or review-required labels remain visible;
- safe summaries do not retain raw private text;
- models reject forbidden private/provider/outbound/media fields;
- service does not expose send/schedule/deliver/provider/mutation/media
  methods.

### 3. Data Contract

Create `docs/data_contracts/review_queue_candidate_contract.md` describing
implemented records, invariants, priority behavior, forbidden fields,
verification, non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M27_review_queue_dry_run_apply/T378_memory_lifecycle_dry_run_apply.md`
for memory lifecycle dry-run apply plans.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T377_worker_summary.md` and append a T377 worker
record to `docs/07_handoff.md`.

Do not mark T377 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\review_queue.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_queue_candidates.py tests\test_memory_governance_candidates.py tests\test_persona_growth_candidates.py tests\test_synthetic_distillation_input_candidates.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial review-queue, product-safety, privacy, lifecycle, persona-safety,
distillation-safety, and documentation-accuracy review.

Reviewer should block if T377 applies decisions, mutates stores/personas,
allows private/provider/outbound/media fields, reads private data, calls
providers, exposes send/schedule/deliver/runtime methods, or implies launch or
production readiness.
