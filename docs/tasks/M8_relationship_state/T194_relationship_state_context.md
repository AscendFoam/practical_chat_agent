# Task T194: RelationshipState Compact Context

## Task ID

T194

## Goal

Inject compact, approval-gated relationship-state guidance into `ChatContext` without exposing raw signal history, raw delta review history, or mutating state.

## Why Now

T193 is accepted with `PASS_WITH_WARNINGS`: the repo now has explicit human review over relationship deltas, but relationship-state information is still not available to runtime context in a compact, approved form.

This is the next safe step because:

- it keeps M8 additive and context-only
- it consumes the review-approved surface rather than inventing a new raw data path
- it avoids state mutation and outbound behavior changes

## Read First

- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/T193_review.md`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/tasks/M8_relationship_state/T193_relationship_review_cli.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/chat_context.py`

## Forbidden Scope

- Do not inject raw signal history.
- Do not auto-update state.
- Do not change sending behavior.
- Do not reopen delta review semantics or apply approved deltas.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/chat_context.py`
- `tests/test_relationship_context.py`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/07_handoff.md`

## Expected Output

Produce:

- additive `ChatContext` support for compact approved relationship-state guidance
- assembler logic that reads only approved/runtime-ready relationship-state inputs
- deterministic tests covering:
  - approved relationship-state context load success
  - fallback behavior when no approved relationship-state data is available
  - no raw signal-history or review-history leakage
  - coexistence with existing approved store / approved patch / derived-brief context
  - no send-behavior change
- a short handoff update explaining what context fields were added and what remains deferred to T195 or later

## Implementation Notes

- Keep the injected surface compact and reviewer-safe; prefer summaries or bounded fields over full internal artifacts.
- Treat T193 approval as a review signal, not as a substitute for evidence validation.
- Preserve existing `ChatContext` fallback behavior when relationship-state context is absent.
- Do not broaden scope into applying approved deltas or mutating stored relationship state.

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/chat_context.py`
- `pytest tests/test_relationship_context.py -q`
- `pytest tests/ -q`

Acceptance criteria:

- Only approved/runtime-ready relationship-state guidance enters `ChatContext`.
- Raw signal history, raw review history, and raw private text do not enter `ChatContext`.
- Existing context assembly behavior remains intact when no approved relationship-state data exists.
- No `RelationshipState` mutation or send-behavior change occurs in this task.

## Reviewer Type

normal

## Reviewer Focus

- Does the context layer expose only compact, approved relationship-state guidance?
- Is fallback behavior preserved when relationship-state context is absent?
- Did the task avoid slipping into state application or send-behavior changes?
