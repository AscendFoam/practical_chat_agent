# T260: Memory Event Schema

## Task ID

T260

## Goal

Implement Memory OS v2 base schemas for typed memory events with explicit truth
status, provenance, sensitivity, lifecycle, retrieval permissions, and
separation between factual, inferred, relational, procedural, and imagined
memory.

## Why Now

M14 established PersonaCard source policy and imagined virtual history. The next
system layer needs memory records that can support human-like companion
continuity without contaminating factual memory with imagined persona content.

## Allowed Files

Future T260 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `tests/test_memory_event_schema.py`
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/tasks/M15_memory_os_v2/T261_memory_store_v2.md`
- `docs/worker_summary/T260_worker_summary.md`
- `docs/07_handoff.md`

If the task needs storage services, retrieval logic, CLI wiring, UI, runtime
dialogue, private readers, or migrations, Captain must revise this package
before assignment.

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

- `docs/review/M14_review.md`
- `docs/architecture/M13_persona_memory_relationship_architecture.md`
- `docs/reference/和gpt-pro的对话.md`
- `src/practical_chat_agent/core/models.py`
- `tests/test_persona_card_schema.py`
- `docs/data_contracts/persona_card_v1_contract.md`

## Expected Outputs

### 1. Memory Event Models

Add local schema models for:

- `MemoryEvent`
- `MemoryTruthStatus`
- `MemoryEventType`
- `MemoryProvenance`
- `MemoryLifecycleState`
- `MemoryRetrievalPermission`

The schema must distinguish:

- factual memory;
- inferred memory;
- relational memory;
- procedural memory;
- imagined memory.

### 2. Invariants

Tests must prove:

- factual memory requires evidence refs;
- inferred memory requires confidence and inference rationale;
- relational memory requires relationship dimension labels;
- procedural memory can record preferences and habits without pretending they
  are facts;
- imagined memory must use imagined truth status and cannot be retrieved as
  factual evidence;
- deleted/frozen memory is not retrieval-eligible;
- sensitive memory defaults to review-required;
- raw private transcript fields are absent.

### 3. Contract Doc

Create `docs/data_contracts/memory_event_v2_contract.md` describing fields,
truth statuses, provenance, lifecycle, retrieval permission, and non-actions.

### 4. Next Task Package

Create `docs/tasks/M15_memory_os_v2/T261_memory_store_v2.md` for local store
work only.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T260_worker_summary.md` and append a T260 worker
record to `docs/07_handoff.md`.

Do not mark T260 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_event_schema.py tests\test_persona_card_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T260 creates schemas only and does not smuggle
private reads, retrieval behavior, runtime dialogue, proactive behavior, or
platform integration into Memory OS v2.
