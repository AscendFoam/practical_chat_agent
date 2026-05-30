# T264: Memory Consolidation Stub

## Task ID

T264

## Goal

Implement a deterministic local consolidation-stub service that groups
synthetic MemoryEvent records and returns consolidation candidates without
calling LLMs, mutating stores, ranking retrieval, or generating runtime
dialogue.

## Why Now

T260-T263 define MemoryEvent schemas, store, lifecycle policy, and retrieval
bundle packaging. The next Memory OS v2 step is a consolidation boundary that
can later support summarize/decay/compress workflows while preserving factual,
inferred, relational, procedural, and imagined separation.

## Allowed Files

Future T264 worker may create or modify only:

- `src/practical_chat_agent/services/memory_consolidation_v2.py`
- `tests/test_memory_consolidation_v2.py`
- `docs/data_contracts/memory_consolidation_v2_contract.md`
- `docs/tasks/M15_memory_os_v2/T265_memory_os_m15_gate_review.md`
- `docs/worker_summary/T264_worker_summary.md`
- `docs/07_handoff.md`

If the task needs core schema changes, vector search, ranking, private readers,
CLI wiring, UI, runtime dialogue, or migrations, Captain must revise this
package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement retrieval ranking, vector search, semantic similarity,
  runtime dialogue, proactive candidates, schedulers, outbound requests, or
  platform integration.
- Do not mutate `MemoryEventStore` directly.
- Do not merge imagined memory into factual outputs.
- Do not implement real-person style extraction, clone behavior, voice/face
  work, or Live2D/video simulation.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/memory_lifecycle_v2.py`
- `src/practical_chat_agent/services/memory_event_store.py`
- `tests/test_memory_event_schema.py`
- `tests/test_memory_lifecycle_v2.py`
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/memory_lifecycle_v2_contract.md`
- `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`

## Expected Outputs

### 1. Consolidation Stub

Implement a service that accepts synthetic `MemoryEvent` records and returns
candidate groups with:

- group id;
- event ids;
- event type;
- proposed operation: keep, review, decay, compress, or separate_imagined;
- rationale;
- safety warnings.

### 2. Tests

Add focused tests proving:

- factual events can be grouped only with factual events;
- imagined events stay separate from factual consolidation groups;
- review-required or high-sensitivity events recommend review;
- low-salience old events can recommend decay/compress;
- service returns candidates only and does not mutate stores;
- service exposes no send/schedule/runtime methods.

### 3. Contract Doc

Create `docs/data_contracts/memory_consolidation_v2_contract.md`.

### 4. Next Task Package

Create `docs/tasks/M15_memory_os_v2/T265_memory_os_m15_gate_review.md` for an
M15 gate review.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T264_worker_summary.md` and append a T264 worker
record to `docs/07_handoff.md`.

Do not mark T264 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_consolidation_v2.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_consolidation_v2.py tests\test_memory_retrieval_bundle_schema.py tests\test_memory_lifecycle_v2.py tests\test_memory_event_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T264 remains deterministic, local, and
recommendation-only, with no LLM calls, private reads, runtime dialogue, or
imagined-to-factual contamination.
