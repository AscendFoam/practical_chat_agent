# Review: T210

Verdict: PASS

## Summary

T210 adds four Pydantic models to `core/models.py` defining the opening M10 behavior-planner data contracts: `AgentSelfState`, `BehaviorPolicy`, `CandidateActionPayload`, and `CandidateAction`. The implementation is schema-only, draft-only, and strictly non-executable. No planner logic, scheduling, platform integration, message sending, memory mutation, LLM calls, or raw transcript paths were introduced.

## Blocking Issues

None.

## Non-Blocking Issues

N01. `docs/for_human/T210_review_explanation.md` allowed-files overrun. The task package allows `docs/data_contracts/behavior_planner_contract.md`, `docs/worker_summary/T210_worker_summary.md`, `docs/07_handoff.md`, `src/practical_chat_agent/core/models.py`, and `tests/test_behavior_schema.py`. The reviewer-written explanation document is an established convention artifact, not a worker scope violation. Accepted as convention noise consistent with all prior reviews.

N02. `docs/worker_summary/T210_worker_summary.md` allowed-files overrun. Worker summaries have been treated as convention noise across all prior task reviews. Accepted.

N03. Forbidden metadata key test gap: `CandidateActionPayload` rejects 11 forbidden keys in `_CANDIDATE_ACTION_FORBIDDEN_PAYLOAD_FIELDS`, but `test_payload_rejects_forbidden_execution_and_private_keys` only exercises 9 of them. The credential keys `access_token` and `api_key` are not independently covered by a committed test. This is a low-risk gap because the `field_validator` on `metadata` applies to the full frozenset, but an explicit test would make the credential boundary regression-guarded.

N04. `CandidateAction.status` reuses `DistillationStatus`, which includes `not_human_reviewed` among its values. This status value is not semantically ideal for action candidates but is harmless because the review lifecycle uses only candidate/approved/rejected/frozen/archived. The reuse is consistent with how `MemoryFactCandidate` and `RelationshipDeltaCandidate` handle status elsewhere in the codebase.

N05. `BehaviorPolicy` and `CandidateAction` each duplicate the four `Literal[True]`/`Literal[False]` safety invariant fields (`human_review_required`, `auto_send_allowed`, `platform_execution_allowed`, `scheduler_allowed`). The duplication ensures each artifact is independently safe even if detached from its policy, which is a defensible design choice for this contract-first stage. A future refactor could extract a shared mixin if the pattern grows.

## Missing Tests

M01. No committed test verifies that `BehaviorPolicy.max_candidates` rejects zero or negative values. The field has `ge=1` constraint but lacks a dedicated validation test.

M02. No committed test verifies `AgentSelfState` with `contact_id=None` survives JSON round-trip. The current round-trip test always sets `contact_id` to a non-None value.

M03. No committed test verifies `CandidateActionPayload` credential forbidden keys (`access_token`, `api_key`) are rejected. See N03.

M04. No committed test verifies `CandidateActionPayload.review_notes` preservation through JSON round-trip.

## Suspicious Implementation Details

None. The implementation is straightforward Pydantic schema work with appropriate validators. The `Literal[True]`/`Literal[False]` pattern for safety invariants is a strong type-level guarantee that prevents bypass. The `model_validator` ensuring `action_type` is in the policy's `allowed_action_types` is correctly implemented. The `is_runtime_visible()` helper correctly delegates to the existing `DistilledArtifactReviewMetadata.is_runtime_ready()` pattern.

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py`: passed.
- `pytest tests/test_behavior_schema.py -q`: 25 passed.
- `pytest tests/ -q`: 731 passed, 16 failed (all pre-existing `ModuleNotFoundError: No module named 'typer'` failures in unrelated CLI tests). No T210-related regressions.

## Recommended Next Action

T210 is accepted as the schema-only opening task for M10. The next task in sequence is T211 (action-planner rule engine), which should consume these contracts and implement deterministic candidate generation without sending, scheduling, or platform execution.

The minor test gaps (M01-M04) can be addressed in a later hardening slice or during T211 if they become relevant to that task's scope.
