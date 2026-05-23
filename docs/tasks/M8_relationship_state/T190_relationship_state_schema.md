# Task T190: RelationshipState Schema

## Task ID

T190

## Goal

Define a conservative multidimensional `RelationshipState` schema and a `RelationshipDeltaCandidate` contract for reviewable state changes.

Keep the model review-first and avoid collapsing relationship state into a single scalar score.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/07_handoff.md`

## Read First

- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/tasks/M8_relationship_state/T191_relationship_signal_extractor.md`
- `docs/tasks/M8_relationship_state/T192_relationship_delta_candidate.md`

## Forbidden Scope

- Do not implement extraction or review CLI.
- Do not auto-update state.
- Do not send messages or integrate platforms.
- Do not read raw chat history.
- Do not collapse the model into a single score.

## Expected Fields

- familiarity
- trust
- warmth
- reciprocity
- conflict_level
- boundary_risk
- initiative_allowance
- intimacy_level
- uncertainty
- recent_interaction_temperature
- relevant timestamps
- evidence refs
- relationship delta rationale
- review status / provenance fields

## Expected Output

- A schema that can represent multiple relationship dimensions without implying automatic action.
- A `RelationshipDeltaCandidate` shape that stays reviewable and explicit about evidence.
- Documentation that makes the next M8 steps unambiguous.

## Implementation Notes

- Keep the schema conservative and additive.
- Prefer explicit field names over inferred meaning.
- Preserve review-only interpretation; this task is about data shape, not state mutation.

## Reviewer Type

normal
