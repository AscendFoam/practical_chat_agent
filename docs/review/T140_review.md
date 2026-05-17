# Review: T140

Verdict: PASS_WITH_WARNINGS

## Summary

T140 implements a feedback log schema and minimal CLI for recording human feedback (accept/edit/reject/boundary) on ReplyPlan candidates. The implementation is clean, narrowly scoped, and respects all forbidden boundaries. No auto-send, no ContactSkill/Memory mutation, no DB/vector DB/LLM calls, no `private/chat_history/` reads, and no private content enters committed docs.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: Silent data loss on corrupted log file

`_append_record` (feedback.py:95-100) catches `OSError`, `JSONDecodeError`, and `ValidationError` on an existing output file and silently replaces the entire log with a fresh `ReplyFeedbackLog()`. This means a corrupted or manually-edited log will lose all prior records without any warning to the user. For a single-user offline tool this is acceptable now, but a warning to stderr would be safer.

**Why:** MVP single-user context makes this low-risk, but silent truncation is a data-loss vector.

### N02: `source_plan_path` stored as absolute or relative string depending on caller

The `source_plan_path` field on `ReplyFeedbackRecord` stores `str(plan_path)`, which resolves to whatever the caller passed (could be absolute or relative). If the plan file is later moved or the working directory changes, this reference becomes stale.

**Why:** Handoff already notes this risk. Acceptable for MVP; T141/T150 can add path normalization if needed.

### N03: `_count_records` re-reads and re-validates the entire log file

After `_append_record` writes the log, `_count_records` (feedback.py:110-118) reads and validates it again just to return `len(log.records)`. This is redundant since the count is deterministic after the append. Minor performance waste, not a correctness issue.

**Why:** Low impact for expected log sizes, but unnecessary I/O.

### N04: `reply_plan_id` maps to `approved_contact_skill_record_id`

In feedback.py:45, `reply_plan_id` is populated from `plan.source_context.approved_contact_skill_record_id`. The task package says "reply_plan_id or source plan identifier when available." The `ReplyPlan` model itself does not have a stable `plan_id` field, so this is a reasonable approximation, but it conflates the plan identity with the approved skill record identity.

**Why:** The `ReplyPlan` schema (T130) has no explicit `plan_id` field. Using `approved_contact_skill_record_id` as a proxy works for current single-plan-per-skill usage but may need adjustment if multiple plans reference the same skill.

### N05: No path confinement enforcement

The CLI accepts `--output` as any writable path. The task package says "output to a private output path" and the handoff says "Output confined to requested private output path," but neither the service nor the CLI validates that the output is actually under `private/`. A user could accidentally write feedback logs to a non-private location.

**Why:** The tool is single-user and CLI-driven, so the user controls the path. Path confinement would be a hardening step for T141/T152.

### N06: `ReplyFeedbackAction` is a `Literal` type alias, not an enum

`ReplyFeedbackAction` is defined as `Literal["accept", "edit", "reject", "boundary"]` rather than a `StrEnum`. This is consistent with how the project uses `Literal` in other places (e.g., `ReplyPlanMode`), so it's fine for now, but it means action values are not self-documenting in Pydantic JSON schema output.

**Why:** Consistent with existing codebase patterns. No action needed.

## Missing Tests

- No committed automated tests. Worker verified via manual CLI invocations on a synthetic fixture at `private/distilled/t140_feedback_fixture/`. This is consistent with the project pattern of deferring committed tests to T150/T152.
- Missing test coverage:
  - Schema validation (valid/invalid action values, required fields)
  - Service: valid accept/edit/reject/boundary flows
  - Service: invalid candidate rank rejection
  - Service: edit without `--edited-text` rejection
  - Service: boundary without label or note rejection
  - Service: corrupted log file handling (N01 above)
  - CLI: stdout does not contain draft text, edited text, or private notes
  - CLI: output is valid JSON
  - CLI: path behavior

All deferred to T150/T152 per project convention.

## Suspicious Implementation Details

None found. The implementation is straightforward and uses standard Pydantic patterns. No mocks, stubs, hardcoded outputs, or fake success paths detected.

Specific checks:
- `FeedbackService` loads and validates the `ReplyPlan` via `ReplyPlan.model_validate_json`, not a mock.
- Candidate resolution iterates real `plan.candidates`, not a stubbed list.
- `new_id("fb")` generates real unique IDs, not hardcoded values.
- The CLI delegates all logic to the service and only formats output.

## Scope Compliance

- **Allowed files checked:** `models.py`, `feedback.py`, `main.py`, `07_handoff.md` — all within scope.
- **No forbidden files modified.**
- **No `private/chat_history/` reads.**
- **No ContactSkill/MemoryFact/approved store mutation.**
- **No auto-send, DB, vector DB, LLM, or realtime integration.**
- **No private content in stdout or committed docs.**
- **Feedback is recorded only; not applied to any downstream system.**

## Recommended Next Action

- Captain should accept T140 as complete with warnings.
- T141 (feedback log validator) should address N01 (corrupted log warning) and N05 (path confinement).
- T150/T152 should add committed regression tests covering schema, service, CLI, and privacy-safety checks.
- Update `docs/04_task_board.md` to mark T140 complete when Captain decides.
