# Task T190: RelationshipState Schema

## Task ID

T190

## Goal

Define multidimensional `RelationshipState` schema and `RelationshipDeltaCandidate` concepts.

Do not use a single likeability score and do not auto-update relationship state.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not implement extraction or review CLI.
- Do not auto-update state.
- Do not send messages or integrate platforms.

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

## Reviewer Type

normal
