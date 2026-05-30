# T285: M17 Gate Review

## Task ID

T285

## Goal

Perform a documentation gate review for M17 proactive engine consent work by
summarizing T280 through T284, recording verification evidence, known gaps, and
the allowed next milestone entry point.

## Why Now

M17 has implemented local consent, policy gating, edge-case tests, review card
rendering, and crisis/low-mood safety handling. Before moving into M18 virtual
life stream work, the project needs a gate record that distinguishes this
review-first proactive foundation from runtime proactive generation,
scheduling, sending, platform integration, and product UI.

## Allowed Files

Future T285 worker may create or modify only:

- `docs/review/M17_review.md`
- `docs/tasks/M18_virtual_life_stream/T290_role_dynamic_post_schema.md`
- `docs/worker_summary/T285_worker_summary.md`
- `docs/07_handoff.md`

If T285 needs code changes, tests, task-board edits, or implementation work,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement virtual life stream behavior.
- Do not implement proactive candidate generation, scheduling, delivery,
  automatic sending, outbound requests, platform integration, UI, web demo,
  voice/avatar/video behavior, or social feed generation.
- Do not implement diagnosis, treatment, medical advice, emergency handling, or
  external escalation behavior.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/proactive_policy_gate_contract.md`
- `docs/data_contracts/proactive_review_card_contract.md`
- `docs/worker_summary/T280_worker_summary.md`
- `docs/worker_summary/T281_worker_summary.md`
- `docs/worker_summary/T282_worker_summary.md`
- `docs/worker_summary/T283_worker_summary.md`
- `docs/worker_summary/T284_worker_summary.md`
- `tests/test_proactive_consent_schema.py`
- `tests/test_proactive_policy_gate.py`
- `tests/test_proactive_quiet_hours_frequency.py`
- `tests/test_proactive_review_card.py`
- `tests/test_proactive_crisis_low_mood_policy.py`

## Expected Outputs

### 1. M17 Review

Create `docs/review/M17_review.md` with:

- task coverage summary;
- implemented code and contract list;
- verification commands and results;
- explicit non-actions;
- proactive safety boundary assessment;
- residual risks;
- gate recommendation.

### 2. M18 Entry Task Package

Create `docs/tasks/M18_virtual_life_stream/T290_role_dynamic_post_schema.md`.
T290 should define text-first virtual life stream schema only. It should not
generate posts with LLMs or publish anything.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T285_worker_summary.md` and append a T285 worker
record to `docs/07_handoff.md`.

Do not mark T285 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_proactive_consent_schema.py tests\test_proactive_policy_gate.py tests\test_proactive_quiet_hours_frequency.py tests\test_proactive_review_card.py tests\test_proactive_crisis_low_mood_policy.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that M17 is a local, consented, review-first proactive
foundation only, not candidate generation, runtime scheduling, automatic
sending, platform integration, product UI, diagnosis/treatment, emergency
handling, or web demo.
