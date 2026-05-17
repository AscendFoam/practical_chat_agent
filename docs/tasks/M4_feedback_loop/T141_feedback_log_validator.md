# Task T141: Feedback Log Validator

## Task ID

T141

## Goal

Implement a read-only validator for T140 feedback logs.

T141 must verify that feedback records are structurally valid, reference existing `ReplyPlan` candidates, satisfy action-specific requirements, and remain safe/private. It must not convert feedback into proposals and must not apply feedback to memory or ContactSkill.

## Why Now

T140 proved that private feedback can be recorded, but the recorded log is not yet trustworthy enough for downstream review work by default.

This task is next because the captain accepted T140 with deferred warnings:

- corrupted or unreadable logs must be surfaced explicitly rather than silently treated as clean input
- stale `source_plan_path` references must be detected and reported safely
- non-private path behavior must at least be warned about before M4 can rely on these logs

T141 therefore hardens the log as evidence without turning feedback into automatic learning.

## Inputs To Read

- `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`
- `docs/review/T140_review.md`
- `docs/review/M3_review.md`
- `docs/data_contracts/reply_plan_contract.md`
- T140 feedback models and service implementation in:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

Do not edit other files unless Captain explicitly expands scope.

## Forbidden Scope

- Do not create preference, boundary, memory, or ContactSkill update proposals.
- Do not modify feedback logs, `ReplyPlan` files, ContactSkill records, MemoryFact records, approved stores, planner templates, or outbound behavior.
- Do not call an LLM.
- Do not introduce database, vector DB, migrations, UI, realtime platform integration, background jobs, or sending.
- Do not read from `private/chat_history/`.
- Do not print full draft text, edited text, user notes, boundary notes, raw transcript text, or other private payload text to stdout.

## Expected Implementation

Add validator logic that can inspect one feedback log and the referenced `ReplyPlan` files.

The validator should check at minimum:

- feedback log top-level shape is valid
- required record fields are present
- `action` is valid
- referenced plan path exists when required
- referenced candidate rank/id exists in the plan
- `edit` feedback includes `edited_text`
- `boundary` feedback includes at least one of `boundary_label` or `boundary_note`
- source plan/candidate contact id matches the feedback record
- `reply_plan_id` / candidate metadata are internally coherent enough for later review use
- path/privacy warnings are surfaced when logs or referenced paths are outside expected private locations
- corrupted or unreadable log input is surfaced explicitly rather than silently treated as empty-success input
- records can be summarized without leaking full text

T141 may respond to deferred T140 warnings, but only in read-only form:

- N01: explicit corrupted/unreadable log reporting
- N02: explicit stale or suspicious `source_plan_path` reporting
- N05: explicit private-path warnings

## CLI

Add a CLI command. Prefer:

```text
chat-reply-feedback-validate --input <feedback-log.json> [--strict]
```

The CLI should emit a safe summary containing only ids, counts, booleans, warning codes, and safe paths, such as:

- total records
- valid record count
- invalid record count
- counts by action
- missing plan count
- missing candidate count
- contact mismatch count
- action-specific field failure counts
- corrupted/unreadable-input count
- privacy/safety warnings

If a structured validation report object is introduced, keep it local to the feedback scope and do not echo edited text, notes, drafts, or transcript text into that report.

## Verification

Use synthetic or redacted fixtures only.

Required checks:

- Compile changed Python files.
- Validate a good feedback log containing accept/edit/reject/boundary.
- Validate a bad feedback log containing invalid action, invalid rank, missing edit payload, and missing boundary details.
- Validate a feedback log whose referenced plan path is missing.
- Validate a corrupted or unreadable feedback log fixture and confirm the validator reports failure/warning instead of silently treating it as empty-success input.
- Validate a log located outside `private/` or referencing paths outside `private/` and confirm privacy warnings are surfaced safely.
- Confirm validator is read-only and does not mutate feedback logs, plans, memory, ContactSkill, or approved stores.
- Confirm stdout contains only safe summaries and ids/counts, not full draft/edit/note text.

## Expected Handoff Update

Append a T141 implementation record to `docs/07_handoff.md` with:

- files changed
- validator behavior
- CLI command
- verification commands and outcomes
- explicit statement that no proposals, memory updates, ContactSkill updates, LLM calls, or platform integration were added

## Reviewer Focus

Reviewer type: adversarial.

Reviewer should verify:

- validation is read-only
- invalid references fail safely
- corrupted input is surfaced explicitly
- private-path warnings are surfaced without leaking private text
- stdout and docs do not leak private feedback contents
- T141 does not prematurely implement T142/T160/T162-style proposals
