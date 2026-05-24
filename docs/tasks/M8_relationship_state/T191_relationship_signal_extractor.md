# Task T191: RelationshipSignal Extractor

## Task ID

T191

## Goal

Extract conservative, evidence-backed relationship signals from approved feedback and approved metadata so later M8 tasks can propose reviewable state deltas without reading raw chat history.

## Why Now

T190 is accepted with `PASS_WITH_WARNINGS`: the repo now has a stable `RelationshipState` / `RelationshipDeltaCandidate` contract, but nothing yet produces the intermediate signals that `signal_refs` are supposed to reference.

This is the next smallest safe step because:

- it keeps M8 additive and review-first
- it does not mutate relationship state
- it creates the minimal executable layer that T192 needs before any delta proposal work

## Read First

- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/T190_review.md`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/tasks/M8_relationship_state/T192_relationship_delta_candidate.md`
- `docs/tasks/M8_relationship_state/T193_relationship_review_cli.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/feedback.py`

## Inputs To Respect

- T190 is the authoritative schema boundary for `RelationshipState` and `RelationshipDeltaCandidate`.
- T191 should operate only on already-approved or already-reviewed metadata surfaces already present in the repo workflow, such as feedback artifacts and approved-store-derived metadata.
- Ambiguous situations should be skipped rather than forced into a relationship dimension.
- Signals are observations, not state snapshots and not deltas.

## Forbidden Scope

- Do not read raw chat history.
- Do not auto-update RelationshipState.
- Do not generate `RelationshipDeltaCandidate` records yet.
- Do not add a review CLI.
- Do not call an LLM unless Captain explicitly expands scope.
- Do not send messages or integrate platforms.
- Do not collapse dimensions into a single score.

## Allowed Files

- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/relationship_state_contract.md`
- `tests/test_relationship_signals.py`
- `docs/07_handoff.md`

## Expected Output

Produce:

- an additive relationship-signal model in `core/models.py` that later tasks can reference by id
- a conservative extractor service in `services/feedback.py` that turns approved feedback / approved metadata into zero or more relationship signals
- deterministic, committed synthetic tests covering:
  - signal extraction from clear accepted / rejected / boundary-style feedback patterns
  - no-signal behavior for ambiguous or unsupported inputs
  - evidence-ref preservation
  - no raw-text storage in produced signals
- a short contract update that explains what a relationship signal is and how it differs from state and delta layers

## Implementation Notes

- Prefer under-generation. If a dimension inference is weak or ambiguous, emit no signal.
- Keep signal records dimension-specific and evidence-backed.
- If you need a strength / direction field, keep it explicit and deterministic; do not smuggle in a full state score.
- Reuse existing review/status/provenance patterns where they fit, but do not invent automatic approval semantics.
- Do not redesign unrelated feedback, patch, planner, or context-assembly flows.

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/feedback.py`
- `pytest tests/test_relationship_signals.py -q`
- `pytest tests/ -q`

Acceptance criteria:

- Produced signals are explicit about contact, dimension, provenance, and evidence.
- Produced signals do not include raw chat transcript, raw feedback text, or edited reply text.
- Unsupported inputs are skipped conservatively rather than forced into speculative relationship claims.
- No `RelationshipState` mutation or `RelationshipDeltaCandidate` generation occurs in this task.
- T190 schema semantics remain intact.

## Reviewer Type

adversarial

## Reviewer Focus

- Are the extracted signals conservative enough to avoid speculative relationship overreach?
- Does the task stay on metadata-driven signal extraction rather than drifting into state mutation or delta generation?
- Are evidence refs preserved without storing private raw text?
