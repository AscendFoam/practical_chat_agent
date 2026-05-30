# T273: Relationship Dialogue M16 Gate Review

## Task ID

T273

## Goal

Perform a documentation gate review for M16 relationship/dialogue consumption
by summarizing T270 through T272, recording verification evidence, known gaps,
and the allowed next milestone entry point.

## Why Now

T270-T272 have implemented local context packaging, deterministic planning
metadata, and review-only deterministic draft stubs. Before moving into M17
proactive consent, the project needs a gate record that distinguishes this
local/review-first dialogue foundation from runtime generation, sending,
platform integration, and product UI.

## Allowed Files

Future T273 worker may create or modify only:

- `docs/review/M16_review.md`
- `docs/tasks/M17_proactive_engine_consent/T280_proactive_consent_schema.md`
- `docs/worker_summary/T273_worker_summary.md`
- `docs/07_handoff.md`

If T273 needs code changes, tests, task-board edits, or implementation work,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement code.
- Do not implement proactive candidates, schedulers, outbound requests,
  automatic sending, platform integration, or web demo.
- Do not implement real-person style extraction, clone behavior, voice/face
  work, or Live2D/video simulation.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/data_contracts/relationship_context_bundle_contract.md`
- `docs/data_contracts/dialogue_context_plan_contract.md`
- `docs/data_contracts/dialogue_draft_stub_contract.md`
- `docs/worker_summary/T270_worker_summary.md`
- `docs/worker_summary/T271_worker_summary.md`
- `docs/worker_summary/T272_worker_summary.md`
- `tests/test_relationship_context_bundle_schema.py`
- `tests/test_dialogue_context_planner.py`
- `tests/test_dialogue_draft_stub.py`

## Expected Outputs

### 1. M16 Review

Create `docs/review/M16_review.md` with:

- task coverage summary;
- implemented code and contract list;
- verification commands and results;
- explicit non-actions;
- review-first dialogue boundary assessment;
- residual risks;
- gate recommendation.

### 2. M17 Entry Task Package

Create `docs/tasks/M17_proactive_engine_consent/T280_proactive_consent_schema.md`
for proactive consent schema work. T280 should not generate candidates or send
messages.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T273_worker_summary.md` and append a T273 worker
record to `docs/07_handoff.md`.

Do not mark T273 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_relationship_context_bundle_schema.py tests\test_dialogue_context_planner.py tests\test_dialogue_draft_stub.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that M16 can be considered a local review-first dialogue
foundation only, not runtime AI chat, proactive behavior, sending, platform
integration, or web demo.
