# Task T192: RelationshipDeltaCandidate

## Task ID

T192

## Goal

Generate reviewable `RelationshipDeltaCandidate` records from conservative relationship signals without auto-applying them.

## Why Now

T191 is accepted with `PASS_WITH_WARNINGS`: the repo now has sparse but evidence-backed relationship signals, and T192 is the smallest next step that can turn those signals into explicit candidate deltas.

This is the next safe step because:

- it keeps M8 review-first
- it consumes the signal layer rather than inventing new extraction logic
- it prepares the ground for T193 human review without changing any state yet

## Read First

- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/T191_review.md`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/tasks/M8_relationship_state/T190_relationship_state_schema.md`
- `docs/tasks/M8_relationship_state/T191_relationship_signal_extractor.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/feedback.py`

## Inputs To Respect

- T190 is the authoritative schema boundary for `RelationshipState` and `RelationshipDeltaCandidate`.
- T191 signals are the only approved input surface for this task.
- Deltas should be conservative and explicit; ambiguous or under-supported changes should be skipped rather than forced.
- Magnitude, direction, and rationale must remain reviewable and deterministic.

## Forbidden Scope

- Do not auto-approve or apply deltas.
- Do not mutate `RelationshipState`.
- Do not collapse dimensions into one score.
- Do not send messages.
- Do not introduce raw-text dependencies.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/feedback.py`
- `tests/test_relationship_deltas.py`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/07_handoff.md`

## Expected Output

Produce:

- an additive delta-generation path that consumes T191 signals and emits one or more `RelationshipDeltaCandidate` records
- explicit dimension-change records that preserve contact, source state, evidence refs, and signal refs
- deterministic tests covering:
  - clear signal-to-delta mapping
  - no-delta behavior for ambiguous or unsupported signal sets
  - magnitude/direction consistency
  - preservation of evidence refs and signal refs
  - no state mutation or raw-text leakage
- a short handoff update that explains how T191 signals become T192 delta candidates and what remains deferred to T193

## Implementation Notes

- Keep the mapping conservative. If a signal set is weak, emit no delta.
- Prefer explicit per-dimension candidate records over aggregated fuzzy summaries.
- Recompute or validate `magnitude` from current/proposed values instead of trusting defaults.
- Avoid contradictory `stable` semantics unless the rule is documented in the contract first.
- Do not broaden scope into review CLI, approved-state application, or context injection.

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/feedback.py`
- `pytest tests/test_relationship_deltas.py -q`
- `pytest tests/ -q`

Acceptance criteria:

- Produced deltas are explicit about contact, source state, changed dimensions, evidence refs, and signal refs.
- Produced deltas do not imply automatic approval or state mutation.
- Magnitude and direction are internally consistent or the candidate is rejected.
- Ambiguous signal sets are skipped conservatively.
- T190/T191 semantics remain intact.

## Reviewer Type

adversarial

## Reviewer Focus

- Are the generated deltas conservative enough to avoid speculative relationship changes?
- Is magnitude validated or recomputed rather than blindly trusted?
- Does the task stay delta-only and avoid review or state-application logic?
