# T253: Persona Review Card Contract

## Task ID

T253

## Goal

Define a local review-card contract for PersonaCard candidates so a user or
human reviewer can inspect, edit, approve, reject, freeze, or request changes
before any persona becomes runtime-visible.

## Why Now

T250 defines PersonaCard v1, T251 creates safe L1 candidate cards, and T252
adds a synthetic deidentification guard. The next safe step is a review/edit
contract that keeps generated personas behind explicit review instead of
directly wiring them into dialogue or proactive behavior.

## Allowed Files

Future T253 worker may create or modify only:

- `src/practical_chat_agent/services/persona_review.py`
- `tests/test_persona_review.py`
- `docs/data_contracts/persona_review_card_contract.md`
- `docs/tasks/M14_persona_compiler_schema/T254_persona_version_store.md`
- `docs/worker_summary/T253_worker_summary.md`
- `docs/07_handoff.md`

If T253 needs CLI wiring, persistence stores, migrations, app UI, runtime
dialogue, or additional core models, Captain must revise this package before
assignment.

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
- Do not mark any PersonaCard runtime-ready without explicit reviewed metadata.
- Do not wire PersonaCard into runtime dialogue or memory retrieval.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/persona_compiler.py`
- `src/practical_chat_agent/services/deidentification_guard.py`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/data_contracts/deidentification_guard_contract.md`
- `tests/test_persona_card_schema.py`
- `tests/test_persona_compiler.py`
- `tests/test_deidentification_guard.py`

## Expected Outputs

### 1. Review Card Contract

Create a contract doc for a local review card that exposes:

- persona identity and disclosure;
- source policy and risk tier;
- traits and speech style;
- virtual history with imagined-content label;
- growth policy;
- proactive preferences;
- safety flags;
- blocked/prohibited reasons when present;
- edit operations and review decisions.

### 2. Review Service

Implement a deterministic local service that can:

- render a safe review payload from a PersonaCard;
- redact unsafe prohibited details;
- accept review decisions such as approve, reject, freeze, or request changes;
- update review metadata without mutating the original card in place.

### 3. Tests

Add focused tests proving:

- L1 candidate review payload is inspectable;
- L5 prohibited card stays blocked and non-runtime-ready;
- approving a safe L1 card requires explicit reviewer id and decision;
- rejected/frozen decisions keep runtime readiness false;
- review service does not expose send/schedule/runtime methods.

### 4. Next Task Package

Create `docs/tasks/M14_persona_compiler_schema/T254_persona_version_store.md`
for local version-store work only.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T253_worker_summary.md` and append a T253 worker
record to `docs/07_handoff.md`.

Do not mark T253 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_review.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_review.py tests\test_persona_compiler.py tests\test_deidentification_guard.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T253 remains review-first and does not open runtime
persona consumption, proactive behavior, external sending, or clone paths.
