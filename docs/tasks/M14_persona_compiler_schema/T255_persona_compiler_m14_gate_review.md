# T255: Persona Compiler M14 Gate Review

## Task ID

T255

## Goal

Perform a read/write documentation gate review for M14 by summarizing the
implemented Persona Compiler foundation from T250 through T254, recording
verification evidence, known gaps, and the allowed next milestone entry point.

## Why Now

T250-T254 have created the schema, local compiler, synthetic deidentification
guard, review-card service, and local version store. Before moving into M15
Memory OS v2, the project needs a compact gate record that distinguishes what
is implemented from what remains prohibited or future-only.

## Allowed Files

Future T255 worker may create or modify only:

- `docs/review/M14_review.md`
- `docs/tasks/M15_memory_os_v2/T260_memory_event_schema.md`
- `docs/worker_summary/T255_worker_summary.md`
- `docs/07_handoff.md`

If T255 needs code changes, tests, task-board edits, or implementation work,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement code.
- Do not wire PersonaCard into runtime dialogue, memory retrieval, proactive
  behavior, outbound requests, schedulers, or platform integration.
- Do not implement real-person style extraction, voice/face/avatar work,
  public-figure cloning, ex-partner/family cloning, deceased-person mode, or
  deceptive impersonation.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/data_contracts/deidentification_guard_contract.md`
- `docs/data_contracts/persona_review_card_contract.md`
- `docs/data_contracts/persona_version_store_contract.md`
- `docs/worker_summary/T250_worker_summary.md`
- `docs/worker_summary/T251_worker_summary.md`
- `docs/worker_summary/T252_worker_summary.md`
- `docs/worker_summary/T253_worker_summary.md`
- `docs/worker_summary/T254_worker_summary.md`
- `tests/test_persona_card_schema.py`
- `tests/test_persona_compiler.py`
- `tests/test_deidentification_guard.py`
- `tests/test_persona_review.py`
- `tests/test_persona_version_store.py`

## Expected Outputs

### 1. M14 Review

Create `docs/review/M14_review.md` with:

- task coverage summary;
- implemented code and contract list;
- verification commands and results;
- explicit non-actions;
- safety boundary assessment;
- residual risks;
- gate recommendation.

### 2. M15 Entry Task Package

Create `docs/tasks/M15_memory_os_v2/T260_memory_event_schema.md` for Memory OS
v2 schema work. It should stay schema/local/test-first and must preserve
factual/inferred/relational/procedural/imagined memory separation.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T255_worker_summary.md` and append a T255 worker
record to `docs/07_handoff.md`.

Do not mark T255 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_card_schema.py tests\test_persona_compiler.py tests\test_deidentification_guard.py tests\test_persona_review.py tests\test_persona_version_store.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that M14 can be considered a local Persona Compiler
foundation only, not a runtime companion product, clone system, proactive
engine, voice/avatar system, or platform integration.
