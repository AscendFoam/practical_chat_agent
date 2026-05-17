# Task T141: Feedback Log Validator

## Task ID

T141

## Goal

Implement a read-only validator for T140 feedback logs.

T141 must verify that feedback records are structurally valid, reference existing `ReplyPlan` candidates, satisfy action-specific requirements, and remain safe/private. It must not convert feedback into proposals and must not apply feedback to memory or ContactSkill.

## Why Now

The updated design direction keeps M4 focused on feedback capture, not automatic learning. Before feedback can become preference/boundary proposals in a later milestone, the project needs a deterministic validator that can tell whether feedback logs are safe and usable.

## Inputs To Read

- `docs/reference/gpt的后续设计思路(更新版).md`
- `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`
- T140 feedback models and service implementation
- `docs/data_contracts/reply_plan_contract.md`
- `docs/review/M3_review.md`

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

Do not edit other files unless Captain explicitly expands scope.

## Forbidden Scope

- Do not create preference/boundary/memory update proposals.
- Do not modify ContactSkill, MemoryFact, approved store records, planner templates, or feedback logs.
- Do not call an LLM.
- Do not introduce database, vector DB, UI, realtime platform integration, or sending.
- Do not read from `private/chat_history/`.
- Do not print full draft text, edited text, user notes, boundary notes, or private raw content to stdout.

## Expected Implementation

Add validator logic that can inspect one feedback log and the referenced `ReplyPlan` files.

The validator should check at minimum:

- required fields are present
- `action` is valid
- referenced plan path exists when required
- referenced candidate rank/id exists in the plan
- `edit` feedback includes `edited_text` or an explicit safe diff reference
- `boundary` feedback includes `boundary_label` and/or `boundary_note`
- source plan/candidate contact id matches the feedback record
- output paths remain private or explicitly user-specified safe paths
- records can be summarized without leaking full text

Add a CLI command. Prefer:

```text
chat-reply-feedback-validate --input <feedback.jsonl> [--strict]
```

The CLI should emit a safe summary:

- total records
- counts by action
- invalid record count
- missing plan/candidate references
- action-specific field failures
- privacy/safety warnings

## Verification

Use synthetic or redacted fixtures only.

Required checks:

- Compile changed Python files.
- Validate a good feedback log containing accept/edit/reject/boundary.
- Validate a bad feedback log containing invalid action, invalid rank, missing edit payload, and missing boundary details.
- Confirm validator is read-only and does not mutate feedback logs, plans, memory, or ContactSkill.
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
- stdout and docs do not leak private feedback contents
- T141 does not prematurely implement T160/T162-style proposals
