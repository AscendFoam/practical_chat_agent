# Task T142: Feedback Summary Exporter

## Task ID

T142

## Goal

Implement a safe feedback summary exporter for T140/T141 feedback logs.

T142 should produce aggregate review summaries that help humans understand feedback patterns without exposing private draft text, edited text, notes, or raw chat content.

## Why Now

After feedback capture and validation, the next safe M4 step is visibility: answer what users tend to accept, edit, reject, or flag as boundary-sensitive. This keeps M4 as feedback capture/analysis only and delays proposal generation, versioning, rollback, and memory mutation to later milestones.

## Inputs To Read

- `docs/reference/gpt的后续设计思路(更新版).md`
- `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`
- `docs/tasks/M4_feedback_loop/T141_feedback_log_validator.md`
- T140/T141 feedback models and service implementation
- `docs/review/M3_review.md`

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

Do not edit other files unless Captain explicitly expands scope.

## Forbidden Scope

- Do not create or apply preference/boundary/memory update proposals.
- Do not implement version diff, rollback, freeze, or ContactSkill mutation.
- Do not call an LLM.
- Do not introduce database, vector DB, UI, realtime platform integration, or sending.
- Do not read from `private/chat_history/`.
- Do not export full draft text, edited text, user notes, boundary notes, or raw private content.

## Expected Implementation

Add summary/export logic over validated feedback logs.

The summary should include safe aggregate fields such as:

- total feedback records
- count by action: accept/edit/reject/boundary/skip/prefer_other if supported
- count by candidate type or approach label when available
- count by reason tag when available
- count by policy risk flag snapshot
- count of feedback records with boundary labels
- invalid/skipped record counts if validation results are integrated
- source plan/candidate ids only, not full content

Add a CLI command. Prefer:

```text
chat-reply-feedback-summary --input <feedback.jsonl> [--output <private summary.json>]
```

Default stdout should be a concise safe summary. If an output file is supported, prefer private output paths and document path behavior in the handoff.

## Verification

Use synthetic or redacted fixtures only.

Required checks:

- Compile changed Python files.
- Run summary over a feedback log containing accept/edit/reject/boundary.
- Confirm aggregate counts are correct.
- Confirm stdout and output file do not include full draft text, edited text, user notes, boundary notes, raw transcript, or private chat path contents.
- Confirm no ContactSkill/MemoryFact/store record is modified.

## Expected Handoff Update

Append a T142 implementation record to `docs/07_handoff.md` with:

- files changed
- summary fields
- CLI command
- verification commands and outcomes
- explicit statement that no proposal generation, versioning/rollback/freeze, memory mutation, ContactSkill mutation, LLM calls, or platform integration were added

## Reviewer Focus

Reviewer type: adversarial.

Reviewer should verify:

- summary output is aggregate and privacy-safe
- no automatic learning/update behavior is introduced
- M4 remains feedback capture/validation/summary only
