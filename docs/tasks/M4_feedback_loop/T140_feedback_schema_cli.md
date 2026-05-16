# Task T140: Feedback Schema CLI

## Task ID

T140

## Goal

Define a review-only feedback log schema and implement a minimal CLI for recording human feedback on `ReplyPlan` candidates:

- `accept`: user accepts a candidate draft as-is.
- `edit`: user edits a candidate draft; store the edited text and/or diff reference.
- `reject`: user rejects a candidate draft.
- `boundary`: user records that a candidate violated or approached a relationship boundary.

T140 starts M4 under Gate M3 = `Conditional`. It must collect feedback as evidence for later proposal/versioning tasks, not automatically change memory, ContactSkill, planner templates, or send any message.

## Why Now

T130-T133 proved the review-only ReplyPlanner structure is viable but conditional: draft quality is still template-driven, no committed regression tests exist, and relationship-aware maturity must not be claimed yet.

The next safe step is to capture human feedback in a durable private log so later tasks can propose preference/boundary updates with review. Feedback capture must remain human-approved and offline-first.

## Inputs To Read

- `docs/review/T133_review.md`
- `docs/review/M3_review.md`
- `docs/data_contracts/reply_plan_contract.md`
- `docs/tasks/M3_relationship_reply_planner/T130_reply_plan_schema.md`
- `docs/tasks/M3_relationship_reply_planner/T131_reply_planner.md`
- `docs/tasks/M3_relationship_reply_planner/T132_reply_policy.md`
- `docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`
- Existing models in `src/practical_chat_agent/core/models.py`
- Existing CLI patterns in `src/practical_chat_agent/app/main.py`

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

Do not edit other files unless Captain explicitly expands scope.

## Forbidden Scope

- Do not train, fine-tune, or call an LLM.
- Do not auto-send, draft-send, schedule, or integrate with realtime platforms.
- Do not modify ContactSkill, MemoryFact, approved store records, or planner templates automatically.
- Do not introduce database, vector DB, migrations, background jobs, or UI.
- Do not read from `private/chat_history/`.
- Do not write private feedback contents into `docs/`, `examples/`, or `tests/`.
- Do not claim feedback has updated relationship memory; T140 only records feedback.

## Expected Implementation

Add Pydantic models or equivalent typed structures for feedback logging. Suggested names:

- `ReplyFeedbackAction`
- `ReplyFeedbackRecord`
- `ReplyFeedbackLog`

Each feedback record should include at minimum:

- stable `feedback_id`
- `created_at`
- `contact_id`
- `reply_plan_id` or source plan identifier when available
- `candidate_id` or `priority_rank`
- `action`
- optional `user_note`
- optional `edited_text` for `edit`
- optional `boundary_label` / `boundary_note` for `boundary`
- safe references to the source `ReplyPlan` path or candidate metadata

Add a small service in `src/practical_chat_agent/services/feedback.py` that:

- loads a `ReplyPlan` JSON from a user-supplied path
- validates the chosen candidate exists
- appends feedback to a JSONL or JSON log under a private output path
- keeps path behavior conservative and explicit
- emits only safe summaries to stdout

Add a CLI command in `src/practical_chat_agent/app/main.py`. The exact command name is worker's choice, but prefer something explicit such as:

```text
chat-reply-feedback --plan <path> --candidate-rank <n> --action accept|edit|reject|boundary --output <private path> [--note ...] [--edited-text ...] [--boundary-label ...]
```

## Verification

Use synthetic or redacted input only.

Required checks:

- Compile the changed Python files.
- Run the CLI on a synthetic `ReplyPlan` fixture stored outside committed docs/tests, preferably under `private/distilled/t140_feedback_fixture/`.
- Verify `accept`, `edit`, `reject`, and `boundary` actions each append a valid record.
- Verify invalid candidate rank/id is rejected.
- Verify CLI stdout does not print full draft text, edited text, private notes, raw transcript, or private chat path contents.
- Verify no ContactSkill/MemoryFact/store record is modified by feedback capture.
- Verify output is confined to the requested private output path.

## Expected Handoff Update

Append a T140 implementation record to `docs/07_handoff.md` with:

- files changed
- schema/service/CLI behavior
- verification commands and outcomes
- remaining risks
- explicit statement that no memory/ContactSkill update, auto-send, realtime integration, DB, vector DB, or LLM call was added

## Reviewer Focus

Reviewer type: normal with privacy and scope checks.

Reviewer should verify:

- feedback is recorded, not applied automatically
- all M3 conditional constraints remain intact
- private content stays out of committed docs
- invalid candidate references fail safely
- stdout summaries are safe
