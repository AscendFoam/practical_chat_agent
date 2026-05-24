# Task T193: Relationship Review CLI

## Task ID

T193

## Goal

Implement explicit human review over `RelationshipDeltaCandidate` records with approve/reject/freeze/archive actions, while keeping review separate from state application.

## Why Now

T192 is accepted with `PASS_WITH_WARNINGS`: the repo now has reviewable delta candidates, but there is no committed workflow for a human to approve or reject them.

This is the next safe step because:

- it keeps M8 review-first
- it turns delta candidates into auditable review artifacts
- it still avoids applying approved deltas to `RelationshipState`

## Read First

- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/T192_review.md`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/tasks/M8_relationship_state/T192_relationship_delta_candidate.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/feedback.py`

## Forbidden Scope

- Do not auto-approve relationship changes.
- Do not auto-apply approved deltas to `RelationshipState`.
- Do not modify unrelated memory/ContactSkill records.
- Do not send messages.

## Allowed Files

- `src/practical_chat_agent/app/main.py`
- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/core/models.py` (only if a minimal review-lifecycle helper or field addition is truly required)
- `tests/test_relationship_review_cli.py`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/07_handoff.md`

## Expected Output

Produce:

- a CLI review surface for `RelationshipDeltaCandidate` artifacts
- explicit approve / reject / freeze / archive actions that update `status` and review metadata
- deterministic tests covering:
  - valid review actions
  - invalid action handling
  - runtime-ready approval path
  - preservation of evidence refs, signal refs, and dimension changes through review
  - no state application and no unrelated mutation
- a short handoff update that explains the review flow and what remains deferred to later M8 tasks

## Implementation Notes

- Keep review semantics explicit. Prefer all-or-nothing delta review unless you are also explicitly documenting and testing a partial-approval model.
- Reuse existing review/status/history patterns from prior review CLIs where that keeps behavior consistent.
- Preserve candidate content during review; this task should add decisions, not reinterpret the delta itself.
- Do not broaden scope into `RelationshipState` mutation, compact-context wiring, or outbound behavior.

## Verification

- `python -m py_compile src/practical_chat_agent/app/main.py src/practical_chat_agent/services/feedback.py src/practical_chat_agent/core/models.py`
- `pytest tests/test_relationship_review_cli.py -q`
- `pytest tests/ -q`

Acceptance criteria:

- A reviewer can approve, reject, freeze, or archive a delta candidate explicitly.
- Approval updates lifecycle fields and makes runtime-ready behavior testable without applying the delta.
- Review actions preserve evidence refs, signal refs, and dimension changes.
- No `RelationshipState` mutation occurs in this task.
- The review model is explicit and not left ambiguous.

## Reviewer Type

adversarial

## Reviewer Focus

- Does the CLI keep review separate from state application?
- Are review actions explicit, auditable, and consistent with existing review metadata patterns?
- Did the task avoid drifting into partial-approval ambiguity without a documented model?
