# T378: Memory Lifecycle Dry-Run Apply Plans

## Task ID

T378

## Goal

Implement local deterministic dry-run plans for memory lifecycle decisions.

T378 should turn M26 memory governance candidates plus T377 review decisions
into preview-only apply plans. It must not mutate `MemoryEventStore`, delete
records, write lifecycle changes, enable retrieval, call providers, read
private data, send messages, create UI, or connect to platforms/media.

## Why Now

T377 unified candidate review records. Before building any real apply path, the
project needs deterministic dry-run records that show what would happen and
what would remain blocked.

## Allowed Files

Future T378 worker may create or modify only:

- `src/practical_chat_agent/services/memory_lifecycle_dry_run.py`
- `tests/test_memory_lifecycle_dry_run_apply.py`
- `docs/data_contracts/memory_lifecycle_dry_run_apply_contract.md`
- `docs/tasks/M27_review_queue_dry_run_apply/T379_persona_growth_dry_run_apply.md`
- `docs/worker_summary/T378_worker_summary.md`
- `docs/07_handoff.md`

If T378 needs other source files, fixtures, task-board edits, private data,
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
- Do not delete, freeze, archive, supersede, or suppress real records.
- Do not enable retrieval for withdrawn or review-required memory.
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
- `docs/data_contracts/review_queue_candidate_contract.md`
- `docs/data_contracts/memory_governance_candidate_contract.md`
- `docs/data_contracts/memory_event_v2_contract.md`
- `src/practical_chat_agent/services/review_queue.py`
- `src/practical_chat_agent/services/memory_governance.py`
- `src/practical_chat_agent/services/memory_event_store.py`
- relevant M26/M27 tests.

## Expected Outputs

### 1. Dry-Run Plan Records And Service

Create `src/practical_chat_agent/services/memory_lifecycle_dry_run.py` with:

- `MemoryLifecycleDryRunEffect`
- `MemoryLifecycleDryRunPlan`
- `MemoryLifecycleDryRunService`

Required behavior:

- create deletion cascade dry-run effects from
  `MemoryDeletionCascadePlan`;
- create supersession dry-run effects from `MemorySupersessionCandidate`;
- create contradiction-resolution dry-run effects from
  `MemoryContradictionCandidate`;
- optionally attach a `ReviewQueueDecisionRecord`;
- preserve source candidate ids and memory ids;
- mark every effect as preview-only;
- keep `applies_changes=false` and `writes_memory_store=false`;
- never mutate `MemoryEventStore`.

### 2. Tests

Create `tests/test_memory_lifecycle_dry_run_apply.py` with synthetic-only tests
that prove:

- deletion cascade dry-run plans list suppress/delete/training-exclusion
  effects without mutating the store;
- supersession dry-run plans preview a lifecycle transition without changing
  source memory lifecycle state;
- contradiction dry-run plans preview request-clarification or supersession
  effects without overwriting memory;
- review decisions are referenced but not applied;
- withdrawn or review-required memory is not made retrieval-eligible;
- models reject forbidden private/provider/outbound/media fields;
- service exposes no send/schedule/deliver/provider/mutation/media methods.

### 3. Data Contract

Create `docs/data_contracts/memory_lifecycle_dry_run_apply_contract.md`
describing implemented records, invariants, forbidden fields, tests,
verification, non-actions, and residual risks.

### 4. Next Task Package

Create
`docs/tasks/M27_review_queue_dry_run_apply/T379_persona_growth_dry_run_apply.md`
for persona growth dry-run apply plans.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T378_worker_summary.md` and append a T378 worker
record to `docs/07_handoff.md`.

Do not mark T378 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_lifecycle_dry_run.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_lifecycle_dry_run_apply.py tests\test_review_queue_candidates.py tests\test_memory_governance_candidates.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial memory lifecycle, dry-run safety, privacy, review queue,
product-safety, and documentation-accuracy review.

Reviewer should block if T378 mutates stores, applies decisions, enables
retrieval incorrectly, allows private/provider/outbound/media fields, reads
private data, calls providers, exposes send/schedule/deliver/runtime methods,
or implies launch or production readiness.
