# T261: Memory Store v2

## Task ID

T261

## Goal

Implement a local JSON Memory OS v2 store for `MemoryEvent` records with
append-only writes, lifecycle updates, safe export, and type-aware list/query
helpers. The store must preserve factual/inferred/relational/procedural/
imagined memory separation and must not implement retrieval ranking or runtime
dialogue consumption.

## Why Now

T260 defines MemoryEvent v2 schema. The next safe step is a caller-path local
store that can persist and inspect memory events before any retrieval layer,
consolidation job, or dialogue integration exists.

## Allowed Files

Future T261 worker may create or modify only:

- `src/practical_chat_agent/services/memory_event_store.py`
- `tests/test_memory_event_store.py`
- `docs/data_contracts/memory_event_store_v2_contract.md`
- `docs/tasks/M15_memory_os_v2/T262_memory_lifecycle_policy.md`
- `docs/worker_summary/T261_worker_summary.md`
- `docs/07_handoff.md`

If the task needs core schema changes, vector search, retrieval ranking,
private readers, CLI wiring, UI, runtime dialogue, or migrations, Captain must
revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement retrieval ranking, runtime dialogue, proactive candidates,
  schedulers, outbound requests, or platform integration.
- Do not implement real-person style extraction, clone behavior, voice/face
  work, or Live2D/video simulation.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `src/practical_chat_agent/core/models.py`
- `tests/test_memory_event_schema.py`
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/review/M14_review.md`

## Expected Outputs

### 1. Local Store Service

Implement a deterministic file-backed local service that writes only to a
caller-provided path and supports:

- append `MemoryEvent`;
- list all events;
- list by user id;
- list by event type;
- get by event id;
- update lifecycle to frozen/deleted/archived;
- export safe JSON.

### 2. Tests

Add focused tests proving:

- factual, inferred, relational, procedural, and imagined events can be stored
  without losing type/truth separation;
- latest exported JSON omits raw private transcript fields;
- lifecycle updates make frozen/deleted events retrieval-ineligible;
- imagined events are never returned by factual-list helpers;
- store exposes no send/schedule/runtime methods.

### 3. Contract Doc

Create `docs/data_contracts/memory_event_store_v2_contract.md` describing file
shape, methods, lifecycle behavior, export behavior, and non-actions.

### 4. Next Task Package

Create `docs/tasks/M15_memory_os_v2/T262_memory_lifecycle_policy.md` for
memory lifecycle/forgetting policy work only.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T261_worker_summary.md` and append a T261 worker
record to `docs/07_handoff.md`.

Do not mark T261 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_event_store.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_event_store.py tests\test_memory_event_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T261 is local store work only and does not open
private readers, retrieval ranking, runtime dialogue, proactive behavior, or
platform integration.
