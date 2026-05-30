# T262: Memory Lifecycle Policy

## Task ID

T262

## Goal

Define and implement deterministic local lifecycle policy helpers for Memory OS
v2, including eligibility for remember, freeze, delete, archive, decay, and
compression recommendations. The policy must preserve user control and never
turn imagined memory into factual memory.

## Why Now

T260 defines MemoryEvent schemas and T261 persists them locally. The next safe
step is lifecycle policy before retrieval ranking or dialogue consumption:
which memories are eligible to keep, review, freeze, decay, compress, or delete.

## Allowed Files

Future T262 worker may create or modify only:

- `src/practical_chat_agent/services/memory_lifecycle_v2.py`
- `tests/test_memory_lifecycle_v2.py`
- `docs/data_contracts/memory_lifecycle_v2_contract.md`
- `docs/tasks/M15_memory_os_v2/T263_memory_retrieval_bundle_contract.md`
- `docs/worker_summary/T262_worker_summary.md`
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
- Do not mutate stores directly unless the policy contract explicitly returns a
  recommendation for a caller to apply.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/memory_event_store.py`
- `tests/test_memory_event_schema.py`
- `tests/test_memory_event_store.py`
- `docs/data_contracts/memory_event_v2_contract.md`
- `docs/data_contracts/memory_event_store_v2_contract.md`
- `docs/architecture/M13_persona_memory_relationship_architecture.md`

## Expected Outputs

### 1. Lifecycle Policy Service

Implement a deterministic local service that returns policy recommendations for
individual `MemoryEvent` records. Recommendations should include:

- keep;
- review_required;
- freeze;
- delete;
- archive;
- decay;
- compress.

### 2. Tests

Add focused tests proving:

- high-sensitivity memory requires review;
- deleted/frozen/archived memory is never recommended for retrieval;
- imagined memory can be kept only as imagined memory;
- low-salience old memory can be recommended for decay or compression;
- explicit user-delete signal recommends delete;
- policy returns recommendations only and does not mutate stores;
- service exposes no send/schedule/runtime methods.

### 3. Contract Doc

Create `docs/data_contracts/memory_lifecycle_v2_contract.md` describing inputs,
recommendation fields, policy rules, and non-actions.

### 4. Next Task Package

Create
`docs/tasks/M15_memory_os_v2/T263_memory_retrieval_bundle_contract.md` for a
schema-only retrieval bundle contract. T263 should not implement ranking.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T262_worker_summary.md` and append a T262 worker
record to `docs/07_handoff.md`.

Do not mark T262 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_lifecycle_v2.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_lifecycle_v2.py tests\test_memory_event_store.py tests\test_memory_event_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T262 is policy/recommendation work only and does
not open private readers, retrieval ranking, runtime dialogue, proactive
behavior, or platform integration.
