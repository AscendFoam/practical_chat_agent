# T254: Persona Version Store

## Task ID

T254

## Goal

Implement a local JSON version store for reviewed PersonaCards so persona
creation, edits, approvals, freezes, and rollbacks can be represented without
wiring personas into runtime dialogue or external platforms.

## Why Now

T253 adds review decisions but no persistence. Before any UI or runtime
consumption, the project needs a local version-store contract that preserves
PersonaCard history and supports inspect, rollback, freeze, export, and delete
semantics.

## Allowed Files

Future T254 worker may create or modify only:

- `src/practical_chat_agent/services/persona_version_store.py`
- `tests/test_persona_version_store.py`
- `docs/data_contracts/persona_version_store_contract.md`
- `docs/tasks/M14_persona_compiler_schema/T255_persona_compiler_m14_gate_review.md`
- `docs/worker_summary/T254_worker_summary.md`
- `docs/07_handoff.md`

If T254 needs migrations, database adapters, app UI, CLI wiring, runtime
dialogue, proactive behavior, or core model changes, Captain must revise this
package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement live platform integration, outbound requests, proactive
  candidates, schedulers, or automatic sending.
- Do not implement real-person style extraction, voice/face/avatar work,
  public-figure cloning, ex-partner/family cloning, deceased-person mode, or
  deceptive impersonation.
- Do not wire PersonaCard into runtime dialogue, memory retrieval, or delivery.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/persona_compiler.py`
- `src/practical_chat_agent/services/persona_review.py`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/data_contracts/persona_review_card_contract.md`
- `tests/test_persona_card_schema.py`
- `tests/test_persona_compiler.py`
- `tests/test_persona_review.py`

## Expected Outputs

### 1. Version Store Contract

Create a contract doc for a local JSON store that supports:

- append-only version records;
- latest active version lookup;
- list versions per persona;
- rollback by version id;
- freeze persona;
- delete/tombstone persona;
- export safe JSON.

### 2. Local Store Service

Implement a deterministic file-backed local service. The store should write
only to caller-provided paths and should not discover private directories.

### 3. Tests

Add focused tests proving:

- saving a candidate card creates version 1;
- saving an approved review copy creates a later version;
- latest lookup returns the latest non-deleted version;
- rollback returns a prior version without mutating history;
- freeze/delete states prevent runtime readiness;
- export omits raw private fields and delivery data;
- store service exposes no runtime/send/schedule methods.

### 4. Next Task Package

Create `docs/tasks/M14_persona_compiler_schema/T255_persona_compiler_m14_gate_review.md`
for an M14 gate-review package that summarizes T250-T254.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T254_worker_summary.md` and append a T254 worker
record to `docs/07_handoff.md`.

Do not mark T254 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_version_store.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_version_store.py tests\test_persona_review.py tests\test_persona_compiler.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T254 is local, file-scoped, review-first, and does
not create runtime persona consumption or outbound behavior.
