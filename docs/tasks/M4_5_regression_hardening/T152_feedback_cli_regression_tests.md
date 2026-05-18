# Task T152: Feedback CLI Regression Tests

## Task ID

T152

## Goal

Add committed deterministic tests for the M4 feedback capture, validation, and summary CLI flow.

T152 verifies T140-T142 as a safe feedback loop before any future feedback-to-patch or memory/versioning work.

## Why Now

The updated design direction keeps M4 as feedback capture only. Before later tasks turn feedback into proposals, the project needs tests proving feedback records are private, validatable, summarizable, and non-mutating.

## Inputs To Read

- `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`
- `docs/tasks/M4_feedback_loop/T141_feedback_log_validator.md`
- `docs/tasks/M4_feedback_loop/T142_feedback_summary_exporter.md`
- `docs/review/T140_review.md`
- `docs/review/T141_review.md`
- `docs/review/T142_review.md`
- `docs/review/M4_review.md`
- `docs/review/T151_review.md`
- T140-T142 implementation and handoff records
- T150/T151 tests and fixtures for style consistency
- `docs/review/M3_review.md`

## Allowed Files

- `tests/**`
- `examples/payloads/**` only for safe synthetic/redacted fixtures
- `pyproject.toml` if test config is required
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- Do not read or commit private chat history.
- Do not commit full private feedback contents.
- Do not modify ContactSkill, MemoryFact, approved store records, or planner behavior.
- Do not call an LLM.
- Do not add auto-send, platform integration, DB, vector DB, or UI.

## Required Test Coverage

Add tests for:

- `accept` feedback append
- `edit` feedback append
- `reject` feedback append
- `boundary` feedback append
- invalid candidate rank/id rejected
- invalid plan path rejected or reported safely
- validator catches invalid action-specific fields
- summary exporter reports aggregate counts
- validator report merge into summary is surfaced aggregate-only
- stdout does not print full draft text, edited text, user note, boundary note, raw transcript, or private chat path contents
- feedback flow does not mutate memory/ContactSkill/store records
- private output confinement behavior is enforced or explicitly validated
- corrupted or unreadable log input is surfaced explicitly rather than silently normalized away
- compact validation/summary behavior remains readable without relying on verbose per-record payloads

Prefer tests that directly exercise service behavior where CLI-only coverage would be unnecessarily indirect, but keep at least one end-to-end CLI-path regression for append, validate, and summarize behavior.

If a required safety property cannot be proven without changing implementation behavior, stop and hand the gap back to Captain as a bug task rather than silently broadening scope.

## Verification

Run pytest:

```powershell
$env:PYTHONPATH='src'
pytest tests
```

## Expected Handoff Update

Append a T152 implementation record to `docs/07_handoff.md` with:

- files changed
- fixture shape
- test command/result
- coverage mapping back to T140/T141/T142 obligations
- remaining gaps in M4 feedback validation

## Reviewer Focus

Reviewer type: adversarial.

Reviewer should verify:

- tests prove feedback is recorded, validated, and summarized, not applied
- privacy and stdout checks are meaningful
- corrupted/unreadable input behavior is explicit rather than hand-waved
- compact validation/summary assertions do not depend on verbose per-record payload echoes
- no future milestone behavior is smuggled into M4
