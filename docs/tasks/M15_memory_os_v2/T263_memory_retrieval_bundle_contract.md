# T263: Memory Retrieval Bundle Contract

## Task ID

T263

## Goal

Define schema-only retrieval bundle models that package already-selected
MemoryEvent records for future dialogue or review surfaces without implementing
retrieval ranking, search, vector indexing, or runtime dialogue consumption.

## Why Now

T260-T262 define memory events, local storage, and lifecycle recommendations.
Before ranking or runtime use, the project needs a safe contract for how a
future retrieval layer can hand off memory bundles while preserving truth,
provenance, sensitivity, lifecycle, and imagined/factual separation.

## Allowed Files

Future T263 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `tests/test_memory_retrieval_bundle_schema.py`
- `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`
- `docs/tasks/M15_memory_os_v2/T264_memory_consolidation_stub.md`
- `docs/worker_summary/T263_worker_summary.md`
- `docs/07_handoff.md`

If the task needs vector search, ranking, private readers, CLI wiring, UI,
runtime dialogue, or migrations, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement retrieval ranking, vector search, semantic similarity,
  runtime dialogue, proactive candidates, schedulers, outbound requests, or
  platform integration.
- Do not implement real-person style extraction, clone behavior, voice/face
  work, or Live2D/video simulation.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `src/practical_chat_agent/core/models.py`
- `tests/test_memory_event_schema.py`
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/memory_event_store_v2_contract.md`
- `docs/data_contracts/memory_lifecycle_v2_contract.md`

## Expected Outputs

### 1. Retrieval Bundle Schemas

Add schema models for:

- `MemoryRetrievalBundle`
- `MemoryRetrievalBundleItem`
- `MemoryRetrievalPurpose`

The bundle should record:

- purpose;
- query summary;
- selected memory ids;
- excluded memory ids with reasons;
- truth-status counts;
- imagined-memory count;
- safety warnings;
- generated timestamp.

### 2. Invariants

Tests must prove:

- factual purpose cannot include imagined memory as factual evidence;
- deleted/frozen/archived events cannot be included;
- review-required memory cannot be included without an explicit review flag;
- bundle items preserve event type, truth status, provenance refs, and
  retrieval context;
- bundle has no raw transcript, send, schedule, delivery, or runtime fields.

### 3. Contract Doc

Create `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`.

### 4. Next Task Package

Create `docs/tasks/M15_memory_os_v2/T264_memory_consolidation_stub.md` for
local consolidation-stub work only. T264 should not call LLMs.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T263_worker_summary.md` and append a T263 worker
record to `docs/07_handoff.md`.

Do not mark T263 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_retrieval_bundle_schema.py tests\test_memory_event_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T263 remains schema-only and does not implement
search, ranking, runtime dialogue, proactive behavior, or platform integration.
