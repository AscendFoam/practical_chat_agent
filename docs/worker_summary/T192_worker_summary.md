# T192 Worker Summary

## Task

T192: RelationshipDeltaCandidate — generate reviewable `RelationshipDeltaCandidate` records from conservative relationship signals without auto-applying them.

## What Changed

### `src/practical_chat_agent/services/feedback.py`

Added `RelationshipDeltaGenerator` class with `generate_from_signals()` method. The generator:

- Consumes T191 `RelationshipSignal` records and a current `RelationshipState`.
- Filters signals to those matching `current_state.contact_id`.
- Groups signals by `dimension_name`.
- Requires consistent direction per dimension (all increase or all decrease). Contradictory, unknown-only, or stable-only directions skip the dimension.
- Uses max signal strength as the effective delta magnitude, attenuated by `_MAGNITUDE_SCALE=0.2`.
- Skips dimensions where max strength < `_MIN_STRENGTH=0.3`.
- Recomputes `magnitude` as `abs(proposed_value - current_value)` rather than trusting signal strength.
- Validates `direction` from actual proposed vs current values rather than blindly trusting signal direction.
- Clamps proposed values to [0.0, 1.0]; skips dimensions where clamping produces no effective change.
- Collects and deduplicates `evidence_refs` from contributing signals (state evidence excluded).
- Collects all `signal_id` values into `signal_refs`.
- Generated deltas always have `status="candidate"`; no auto-approve or state mutation.

Added `RelationshipDeltaCandidate`, `RelationshipDeltaDimension`, and `RelationshipState` to imports.

### `tests/test_relationship_deltas.py` (new)

26 tests covering:

- Clear signal-to-delta mapping (boundary_violation, too_intimate, too_eager).
- No-delta behavior (empty signals, wrong contact, unknown direction, weak signal, contradictory directions, stable direction).
- Magnitude/direction consistency (magnitude equals abs diff, decrease validated, upper/lower boundary clamping, no delta at boundaries).
- Evidence ref and signal ref preservation (evidence preserved, signal refs preserved, evidence deduplicated, state evidence excluded).
- No state mutation.
- Delta candidate properties (status is candidate, rationale nonempty, no raw text).
- Multi-signal aggregation (max strength used, all signal refs collected, rationale counts).

### `docs/data_contracts/relationship_state_contract.md`

Added "RelationshipDeltaCandidate Generation (T192)" section documenting:

- Delta generation rules (contact filtering, dimension grouping, direction consistency, strength aggregation, minimum strength, magnitude attenuation, magnitude recomputation, direction validation, boundary clamping, evidence deduplication, signal refs).
- Delta generation parameters table (`_MAGNITUDE_SCALE=0.2`, `_MIN_STRENGTH=0.3`).
- Example delta generation walkthrough.
- Delta safety constraints (no auto-approve, no state mutation, no raw text, evidence-backed, conservative aggregation).

Updated scope description to reflect T192 coverage.

### `docs/07_handoff.md`

Added T192 Worker Completion Record documenting what changed, delta generation design, relationship to T191, verification results, and explicit non-actions.

## Verification

1. Compile check passed: `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/feedback.py`
2. T192 test suite: 26 tests passed, 0 failures.
3. Full existing test suite: 488 tests passed (26 new + 462 existing), 0 failures, no regression.

## Remaining Risks

- The `_MAGNITUDE_SCALE=0.2` and `_MIN_STRENGTH=0.3` are heuristic defaults, not calibrated against real data. T193 review or later tasks may want to adjust these after observing real delta proposals.
- The generator uses max signal strength for aggregation. Alternative strategies (weighted sum, evidence count weighting) were considered but deferred for simplicity. If signal density increases, a more nuanced aggregation may be warranted.
- Only 3 of 8 relationship dimensions are reachable through current T191 signal extraction rules. Dimensions without signals (familiarity, trust, warmth, reciprocity, conflict_level) cannot produce delta candidates. This is intentionally conservative.
- The generator does not yet support partial delta approval. If a delta proposes changes to multiple dimensions, T193 review should decide whether to allow dimension-level partial approval or require all-or-nothing.
- `RelationshipDeltaDimension.magnitude` is not schema-enforced to equal `abs(proposed_value - current_value)` (deferred from T190 N02). The generator validates this programmatically, but future schema evolution could add a model validator.
