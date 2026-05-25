# Task T213: CandidateAction Review CLI

## Task ID

T213

## Goal

Implement manual review for draft/enriched `CandidateAction` records without sending, scheduling, or platform execution.

This task should let a human mark a candidate action as approved, rejected, frozen, or archived, and record review metadata/history. Approval is review visibility only; it is not send authorization.

## Why Now

T210 defined the non-executable candidate-action schema, T211 added deterministic candidate proposal, and T212 added deterministic review-safe draft text. The next safe step is an explicit human review layer before any behavior safety evaluation or outbound send-gate work.

## Inputs To Read

- `AGENTS.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/data_contracts/behavior_planner_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/behavior_planner.py`
- `src/practical_chat_agent/app/main.py`
- Existing review CLI/service patterns, especially:
  - `src/practical_chat_agent/services/feedback.py`
  - `tests/test_relationship_review_cli.py`
  - `tests/test_feedback_cli.py`

## Allowed Files

- `src/practical_chat_agent/services/behavior_planner.py`
- `src/practical_chat_agent/app/main.py`
- `tests/test_behavior_rule_planner.py`
- `tests/test_behavior_review_cli.py`
- `docs/data_contracts/behavior_planner_contract.md`
- `docs/worker_summary/T213_worker_summary.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not send messages.
- Do not schedule real actions, create timers, reminders, background jobs, automations, or recurring tasks.
- Do not integrate Feishu, WeChat, browser, desktop, notification, email, webhook, or any platform adapter.
- Do not create `OutboundMessageRequest`, call `OutboundSendGate`, or introduce send-gate behavior.
- Do not call an LLM, provider API, embedding service, vector DB, Mem0/Zep, or any external service.
- Do not mutate `MemoryFact`, `ContactSkill`, `RelationshipState`, `PreferencePatchCandidate`, approved stores, private artifacts, or unrelated review metadata.
- Do not read `private/chat_history/` or commit private chat content.
- Do not treat `status="approved"` or `is_runtime_visible()` as sendable, schedulable, executable, or platform-targeted.
- Do not update `docs/04_task_board.md`; Captain will mark completion after review.

## Expected Output

Add a manual review service for `CandidateAction`, preferably in `src/practical_chat_agent/services/behavior_planner.py`, with a name such as `CandidateActionReviewService`.

The service should:

- Accept a `CandidateAction` object or mapping that validates to one.
- Accept one review decision: `approve`, `reject`, `freeze`, or `archive`.
- Require a reviewer identifier.
- Optionally accept a review note.
- Return a new reviewed `CandidateAction` without mutating the input object.
- Update:
  - `status`
  - `review_metadata.review_state`
  - `review_metadata.reviewed_by_human`
  - `review_metadata.last_decision`
  - `review_metadata.last_reviewed_at`
  - `review_metadata.last_reviewer_id`
  - `review_metadata.history`
  - `review_metadata.decision_notes` when note is provided
- Preserve:
  - `action_type`
  - `payload.safe_summary`
  - `payload.draft_text`
  - `supporting_context_refs`
  - `risk_flags`
  - `policy`
  - all no-send/no-platform/no-scheduler invariants

Add a CLI command in `src/practical_chat_agent/app/main.py`, for example `chat-behavior-review-action`, that:

- reads a JSON file containing one `CandidateAction`
- applies a manual decision
- writes a reviewed JSON file
- prints only safe metadata to stdout, such as `action_id`, `contact_id`, `action_type`, `status`, `review_state`, `reviewer`, `history_count`, and output path
- never prints raw private text or full draft text to stdout

Path policy:

- Default or recommended outputs should be under `private/`.
- If the implementation permits arbitrary output paths, it must at least document and test that stdout remains safe.
- Do not write to `docs/`, `examples/`, or `tests/fixtures` as part of operational CLI use.

Update `docs/data_contracts/behavior_planner_contract.md` with:

- T213 review scope
- supported decisions
- review metadata semantics
- approved-is-not-sendable boundary
- CLI safe-output expectations
- relationship to T214 and later OutboundSendGate milestones

Write `docs/worker_summary/T213_worker_summary.md` with:

- files changed
- service/CLI behavior added
- verification commands/results
- explicit non-actions
- remaining risks

Append a T213 implementation record to `docs/07_handoff.md`.

## Verification

Run:

```powershell
python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py src/practical_chat_agent/app/main.py
pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py tests/test_behavior_review_cli.py -q
pytest tests/ -q
```

If the Windows default temp directory is inaccessible in this sandbox, set `TEMP` and `TMP` to a workspace-local temp directory before running pytest and record that fact in `docs/07_handoff.md`.

Minimum test coverage expected:

- service approves candidate and sets review metadata/history
- service rejects, freezes, and archives candidate with correct statuses
- service rejects invalid decision strings
- service requires non-empty reviewer id
- service preserves payload draft text and supporting refs
- service returns a new object and does not mutate the input
- approved candidate remains non-sendable/non-schedulable/non-platform-executable
- CLI can review a synthetic candidate JSON file
- CLI stdout does not print full draft text or private/raw content
- CLI output JSON validates as `CandidateAction`
- CLI handles missing input and invalid candidate JSON safely

## Docs To Update

- `docs/data_contracts/behavior_planner_contract.md`
- `docs/07_handoff.md`
- `docs/worker_summary/T213_worker_summary.md`

Do not update `docs/04_task_board.md`; Captain will mark completion after review.

## Reviewer Type

adversarial
