# Task T150: ReplyPlanner Regression Tests

## Task ID

T150

## Goal

Add committed deterministic regression tests for the M3 `ReplyPlanner` and policy layer.

T150 closes the key M3 Conditional gap: current ReplyPlanner behavior has inline/private verification, but no committed fixtures/tests that can run in a clean environment.

## Why Now

M3 was accepted only as `Conditional`. Before LLM-assisted drafting, feedback-to-patch proposals, platform adapters, or relationship-state logic, the project needs repeatable tests that guard privacy, boundary behavior, contact alignment, and candidate structure.

## Inputs To Read

- `docs/review/M3_review.md`
- `docs/review/T133_review.md`
- `docs/review/T133_milestone_review.md`
- `docs/tasks/M3_relationship_reply_planner/T130_reply_plan_schema.md`
- `docs/tasks/M3_relationship_reply_planner/T131_reply_planner.md`
- `docs/tasks/M3_relationship_reply_planner/T132_reply_policy.md`
- `docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`
- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/services/policy.py`
- `src/practical_chat_agent/core/models.py`

## Allowed Files

- `tests/**`
- `examples/payloads/**` only for safe synthetic/redacted fixtures
- `pyproject.toml` if pytest config is required
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

Do not edit planner implementation unless Captain explicitly opens a bug-fix task.

## Forbidden Scope

- Do not use private chat history or private eval artifacts as committed fixtures.
- Do not commit raw transcript text, real names, real platform IDs, or private paths.
- Do not call an LLM.
- Do not modify ReplyPlanner behavior in this task.
- Do not add auto-send, platform integration, database, vector DB, or UI.

## Required Test Coverage

Add pytest coverage for at least:

- baseline friend context emits valid 3-candidate `ReplyPlan`
- practical colleague context emits valid 3-candidate `ReplyPlan`
- thin context produces `thin_context` risk behavior and conservative confidence
- sensitive/boundary context produces boundary reminders/risk flags
- false-positive probe stays bounded and does not over-escalate beyond expected policy behavior
- subtle false-negative probe documents current limitation or expected detection behavior
- privacy leakage probe: raw inbound text is not echoed in `ReplyPlan`
- contact_id mismatch is rejected
- approved-store missing/not_configured path still emits safe candidates
- candidate `priority_rank` is unique and stable
- non-approved record ids do not leak into candidate refs

## Verification

Required commands:

```powershell
$env:PYTHONPATH='src'
pytest tests
```

If the full suite cannot run, record the blocker in `docs/07_handoff.md` and `docs/08_risks_and_open_questions.md`.

## Expected Handoff Update

Append a T150 implementation record to `docs/07_handoff.md` with:

- files changed
- fixture shape
- test command and result
- any tests intentionally marking current limitations
- which M3 risks were reduced or remain open

## Reviewer Focus

Reviewer type: normal with privacy checks.

Reviewer should verify:

- tests are committed and deterministic
- fixtures are synthetic/redacted
- no private raw content is included
- tests cover the exact M3 Conditional obligations
