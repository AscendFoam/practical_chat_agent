# Review: T192

Verdict: PASS_WITH_WARNINGS

## Task Goal

Generate reviewable `RelationshipDeltaCandidate` records from T191 relationship signals without auto-applying them.

## What Changed

### `src/practical_chat_agent/services/feedback.py`

Added `RelationshipDeltaGenerator` class (~125 lines) with `generate_from_signals()` method. The implementation:

1. Filters signals to those matching `current_state.contact_id`.
2. Groups signals by `dimension_name`.
3. Requires exactly one consistent direction (all `increase` or all `decrease`) per dimension; contradictory, all-unknown, or all-stable directions skip the dimension.
4. Uses max signal strength as the effective delta magnitude, attenuated by `_MAGNITUDE_SCALE=0.2`.
5. Skips dimensions where max strength < `_MIN_STRENGTH=0.3`.
6. Recomputes `magnitude` as `abs(proposed_value - current_value)` rather than trusting signal strength.
7. Validates `direction` from actual proposed vs current values.
8. Clamps proposed values to [0.0, 1.0]; skips dimensions where clamping produces no effective change (magnitude < 1e-6).
9. Deduplicates `evidence_refs` from contributing signals; state evidence excluded.
10. Collects all `signal_id` values into `signal_refs`.
11. Generated deltas always have `status="candidate"`; no auto-approve or state mutation.

Also added three new imports: `RelationshipDeltaCandidate`, `RelationshipDeltaDimension`, `RelationshipState`.

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

Added "RelationshipDeltaCandidate Generation (T192)" section documenting generation rules, parameters, example walkthrough, and safety constraints.

### `docs/07_handoff.md`

Added T192 Worker Completion Record.

### `.claude/settings.json`

Workspace-artifact permission entries added (consistent with all prior tasks).

## Verification

1. Compile check passed.
2. T192 test suite: 26 tests passed.
3. Full test suite: 488 tests passed (26 new + 462 existing), 0 regressions.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: `_MAGNITUDE_SCALE=0.2` and `_MIN_STRENGTH=0.3` are uncalibrated heuristics

These magic numbers are documented in the contract but have no empirical basis. The worker summary correctly identifies this risk. Not blocking because: (a) they are documented and explicit, (b) the task is candidate-generation-only and all deltas require human review before application, (c) T193 or later calibration tasks can adjust them.

### N02: Max-strength aggregation loses signal-count information

When multiple signals agree on direction for the same dimension, only the maximum strength drives the proposed change. Weaker but corroborating signals contribute nothing to magnitude. This is documented and acceptable for the current conservative scope, but if signal density grows, a weighted or count-aware strategy may be more appropriate.

### N03: `.claude/settings.json` workspace-artifact overrun

Permission entries for T192 verification commands were added. This is consistent with every prior task (T160 through T191) and is a workspace artifact, not a task-scope violation.

### N04: `dimension_name` type-ignore suppression

`dimension_name=dim_name  # type: ignore[arg-type]` appears at line 1414. The `dim_name` comes from `sorted(by_dimension.items())` where keys are plain strings from signal `dimension_name` (typed as `RELATIONSHIP_DIMENSION_NAMES` Literal). The string is then looked up in `snapshot.get(dim_name)`, so runtime correctness is ensured. The suppression is cosmetic/typing only.

### N05: `_DIRECTION_SIGN` uses string keys instead of `RelationshipDeltaDirection` Literal

The `_DIRECTION_SIGN` dict maps plain strings `"increase"` and `"decrease"` to sign values. This is consistent with how T191 handles direction strings but technically bypasses the Literal type. No correctness issue.

## Missing Tests

### M01: No test for dimension not present in state snapshot

If a signal references a dimension name that does not exist in `RelationshipState` (e.g., a typo or future dimension), `snapshot.get(dim_name)` returns `None` and the dimension is skipped. This is correct behavior but untested. A test confirming this would strengthen the safety argument.

### M02: No test for mixed increase/decrease signals with unknown/stable companions

The direction-consistency check allows mixed directions as long as `known_directions - {"unknown", "stable"}` has exactly one element. For example, one `increase` + two `unknown` signals should produce a delta. This is tested implicitly by the existing "unknown direction" test (which uses a single unknown signal), but a test with a mix of known + unknown directions on the same dimension would be more explicit.

### M03: No test for `is_runtime_ready()` returning False on the delta

`test_delta_status_is_candidate` checks `status == "candidate"` but does not assert `is_runtime_ready() == False`. The test only does `assert not deltas[0].is_runtime_ready()` which is present at line 314 — this is actually covered. M03 withdrawn.

### M04: No test for empty `evidence_refs` after deduplication with state-evidence-only signals

If all signals happen to carry only state evidence refs (which are excluded), the delta could have empty `evidence_refs`, violating `min_length=1` on `RelationshipDeltaCandidate`. This scenario is unlikely given T191 signal construction but is not explicitly tested.

## Suspicious Implementation Details

### S01: `validated_direction` can be `"stable"` but the code earlier filters `"stable"` directions

In `_compute_dimension_change`, if `proposed_value == current_value` after clamping, the method returns `None` (because `recomputed_magnitude < 1e-6`). So the `validated_direction = "stable"` branch at line 1411 is dead code. This is not a bug — it's defensive programming — but it is unreachable.

### S02: `signal_refs` may contain duplicates if the same signal contributes to multiple dimension calculations

Looking at the code flow: `all_signal_refs.append(sig.signal_id)` happens inside `for sig in dim_signals` for each dimension. Since signals are grouped by dimension, each signal can only appear in one dimension group, so no duplication is possible. This is correct but worth noting the implicit assumption.

### S03: `sorted(by_dimension.items())` iteration order is deterministic but arbitrary

The generator processes dimensions in alphabetical order, which is deterministic. This is good for reproducibility but means dimension-change ordering depends on naming rather than semantic importance. Not a concern for candidate-only output.

## Scope Compliance

- Allowed files check:
  - `src/practical_chat_agent/core/models.py`: No changes needed. Correct — T190 schemas were sufficient.
  - `src/practical_chat_agent/services/feedback.py`: Changed. Within allowed scope.
  - `tests/test_relationship_deltas.py`: New file. Within allowed scope.
  - `docs/data_contracts/relationship_state_contract.md`: Changed. Within allowed scope.
  - `docs/07_handoff.md`: Changed. Within allowed scope.
  - `.claude/settings.json`: Changed. Consistent workspace-artifact pattern.
- No forbidden scope violations detected:
  - No auto-approve or auto-apply.
  - No `RelationshipState` mutation.
  - No scalar collapse (dimensions remain independent).
  - No send/platform integration.
  - No raw-text dependencies.
  - No LLM calls.

## Recommended Next Action

T192 is complete. The next M8 task should be T193 (relationship review CLI), which will allow human review of the delta candidates produced by this generator. T193 must:

1. Present delta candidates with their dimension changes, evidence refs, and signal refs.
2. Allow approve/reject/freeze decisions on individual deltas.
3. Not auto-apply approved deltas to `RelationshipState` — that can be deferred to a later task or kept manual.
4. Consider whether dimension-level partial approval is needed (the worker summary flags this open question).
