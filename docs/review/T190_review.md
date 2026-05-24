# Review: T190

Verdict: PASS_WITH_WARNINGS

## Summary

T190 defines a conservative, multidimensional `RelationshipState` schema and a `RelationshipDeltaCandidate` contract in `src/practical_chat_agent/core/models.py`, with a supporting data contract document at `docs/data_contracts/relationship_state_contract.md`. The task is schema-only: no signal extraction, no review CLI, no auto-update, no send/platform integration, and no single-score collapse.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: `.claude/settings.json` workspace-artifact overrun

`.claude/settings.json` was modified to add a new compile command to the allowed-tools list. This is the same pattern accepted in T160–T185 reviews: it is a workspace-level permission artifact rather than a T190 functional change. Accepted.

### N02: `RelationshipDeltaDimension.magnitude` has a default of `0.0` instead of being derived from `current_value` and `proposed_value`

The `magnitude` field defaults to `0.0` and is not auto-computed as `abs(proposed_value - current_value)`. A caller could create a delta with `current_value=0.1, proposed_value=0.9, magnitude=0.0`, which is internally inconsistent. The contract document does not explicitly state that magnitude should equal the absolute difference. This is non-blocking because T192 (delta candidate generation) will be responsible for computing magnitude correctly, and the task scope is schema-only. However, it should be noted that downstream consumers cannot rely on magnitude being consistent with current/proposed values at the schema level.

### N03: `RelationshipDeltaDirection` has a `"stable"` option but no guidance on when to use it

The `"stable"` direction is present in the literal but the contract document and task spec do not explain when a "stable" delta would be created. A delta that proposes no change is somewhat contradictory to the concept of a "delta candidate." This is non-blocking because the field is optional-default-`"unknown"` and T192 will decide whether to produce stable-direction deltas.

### N04: `RelationshipState.source_type` does not include a `"delta_approved"` option

The `source_type` literal includes `"heuristic"`, `"signal_extractor"`, `"manual"`, `"unknown"` but does not include a type for states that were produced by applying an approved delta. When T193 approves a `RelationshipDeltaCandidate` and produces an updated `RelationshipState`, the most natural `source_type` would be something like `"delta_approved"` or `"delta_application"`. This is non-blocking because the field is optional and can be extended later, but it is a forward-compatibility note for T193.

## Missing Tests

### M01: No committed automated tests for RelationshipState schema validation

Consistent with the project pattern (schema tasks like T111, T130, T160, T170–T172 all defer schema validation tests to later regression-hardening tasks), but tracked: no committed test exercises `RelationshipState` or `RelationshipDeltaCandidate` validation, boundary enforcement, `is_runtime_ready()`, or `dimension_snapshot()`.

## Suspicious Implementation Details

None found. The implementation is clean, minimal, and uses existing project patterns (`new_id`, `DistillationStatus`, `DistilledArtifactReviewMetadata`, `utc_now`, `Field` constraints). No mocks, stubs, hardcoded outputs, or fake success paths.

## Recommended Next Action

T190 is complete as a schema-only task. The next Current Unique Task should be T191 (relationship signal extractor), which will produce the signal records that `RelationshipDeltaCandidate.signal_refs` can reference. Captain should update `docs/04_task_board.md` to mark T190 complete and set T191 as the Current Unique Task.
