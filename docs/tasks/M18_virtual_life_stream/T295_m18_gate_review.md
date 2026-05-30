# T295: M18 Gate Review

## Task ID

T295

## Goal

Perform a documentation gate review for M18 virtual life stream work by
summarizing T290 through T294, recording verification evidence, known gaps, and
the allowed next milestone entry point.

## Why Now

M18 has implemented review-only virtual life post schemas, deterministic local
generation stubs, AIGC disclosure metadata, imagined/factual contamination
guards, and local review cards. Before moving into M19 control-surface work,
the project needs a gate record that distinguishes review-only virtual life
drafts from publishing, platform integration, UI, and realtime product behavior.

## Allowed Files

Future T295 worker may create or modify only:

- `docs/review/M18_review.md`
- `docs/tasks/M19_memory_persona_control_surface/T300_memory_persona_control_requirements.md`
- `docs/worker_summary/T295_worker_summary.md`
- `docs/07_handoff.md`

If T295 needs code changes, tests, task-board edits, or implementation work,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement control UI.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not implement real social-feed integration, voice/avatar/video behavior,
  Live2D, web demo, or product UI.
- Do not implement real-person clone behavior, deceased-person simulation, or
  deceptive impersonation paths.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/data_contracts/role_dynamic_post_contract.md`
- `docs/data_contracts/virtual_life_engine_contract.md`
- `docs/data_contracts/virtual_life_review_card_contract.md`
- `docs/worker_summary/T290_worker_summary.md`
- `docs/worker_summary/T291_worker_summary.md`
- `docs/worker_summary/T292_worker_summary.md`
- `docs/worker_summary/T293_worker_summary.md`
- `docs/worker_summary/T294_worker_summary.md`
- `tests/test_role_dynamic_post_schema.py`
- `tests/test_virtual_life_engine_text_generator.py`
- `tests/test_virtual_life_aigc_labeling.py`
- `tests/test_virtual_life_contamination.py`
- `tests/test_virtual_life_review_card.py`

## Expected Outputs

### 1. M18 Review

Create `docs/review/M18_review.md` with:

- task coverage summary;
- implemented code and contract list;
- verification commands and results;
- explicit non-actions;
- virtual life safety boundary assessment;
- residual risks;
- gate recommendation.

### 2. M19 Entry Task Package

Create
`docs/tasks/M19_memory_persona_control_surface/T300_memory_persona_control_requirements.md`.
T300 should define local/prototype control requirements for viewing, editing,
deleting, freezing, exporting, and auditing persona/memory records. It should
not build UI yet.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T295_worker_summary.md` and append a T295 worker
record to `docs/07_handoff.md`.

Do not mark T295 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_role_dynamic_post_schema.py tests\test_virtual_life_engine_text_generator.py tests\test_virtual_life_aigc_labeling.py tests\test_virtual_life_contamination.py tests\test_virtual_life_review_card.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that M18 remains local and review-only, not publishing,
sending, platform integration, realtime product UI, or web demo.
