# Review: T211

Verdict: PASS

## Summary

T211 adds `BehaviorRulePlanner`, a deterministic local rule engine in `src/practical_chat_agent/services/behavior_planner.py` that proposes review-only `CandidateAction` records from T210 behavior contracts. The implementation is purely additive, candidate-only, and strictly non-executing. No message sending, scheduling, platform integration, LLM calls, memory mutation, CLI commands, runtime wiring, or raw transcript paths were introduced.

## Blocking Issues

None.

## Non-Blocking Issues

N01. `docs/for_human/T211_review_explanation.md` and `docs/worker_summary/T211_worker_summary.md` allowed-files overrun. The task package allows `docs/worker_summary/T211_worker_summary.md` and `docs/07_handoff.md`, `docs/data_contracts/behavior_planner_contract.md`. The reviewer-written explanation is an established convention artifact. Accepted as convention noise consistent with all prior reviews.

N02. `BehaviorRulePlanner._stable_action_id` uses SHA-1 truncated to 16 hex chars. This follows the existing project pattern (T102/T110 event_id and chunk_id use SHA-1 similarly). The collision risk is negligible for the current offline single-user workflow. A future hardening task could upgrade to SHA-256 if needed.

N03. `_BOUNDARY_RULE_FLAGS` and `_PROACTIVE_BLOCKING_FLAGS` overlap on `boundary_sensitive`, `boundary_risk`, and `high_sensitivity`. This is intentional: boundary flags both trigger the boundary review note AND block proactive check-in. The overlap means boundary-sensitive context gets a conservative review note rather than an optimistic check-in suggestion, which is the correct behavior.

N04. `contact_id` fallback: when `AgentSelfState.contact_id` is `None`, `_candidate()` uses `self_state.user_id` as the `CandidateAction.contact_id`. This is a reasonable fallback for the current task scope, but future tasks that consume candidates should be aware that a candidate with `contact_id == user_id` means "no specific contact targeted."

N05. `_normalize_values` uses `casefold()` for case-insensitive deduplication of risk flags and safe labels. This is correct behavior but means that risk flags passed by callers must be ASCII-lowercase to match the hardcoded frozenset keys. The contract documents the expected flag values, so this is acceptable for scope.

## Missing Tests

M01. No committed test verifies that the `memory_review_prompt` rule fires when `safe_context_labels` contains a memory-review label (e.g., `"memory_review"`, `"relationship_review"`) without any `recent_signal_refs`. The current test `test_recent_signal_refs_emit_memory_review_prompt` only exercises the signal-refs path. The label-only path is functionally exercised in the implementation (confirmed via smoke test), but lacks committed test coverage.

M02. No committed test verifies that each of the six hard proactive-blocking flags individually blocks `relationship_check_in_draft`. The test `test_hard_risk_blocks_relationship_check_in` only covers `privacy_risk`, which does not also trigger `boundary_review_note`. The other blocking flags (`thin_context`, `boundary_sensitive`, `boundary_risk`, `high_sensitivity`, `blocked_proactive`) are not independently covered.

M03. No committed test exercises `contact_id=None` in `AgentSelfState` and verifies that the emitted candidate uses `user_id` as the fallback `contact_id`.

M04. No committed test verifies that multiple simultaneous boundary flags produce only a single `boundary_review_note` (not multiple). The current implementation is correct but untested.

M05. No committed test verifies that `safe_context_labels` with boundary-sensitive values (e.g., `"boundary_sensitive"`) triggers the `boundary_review_note` rule via the label path (as opposed to via risk flags).

## Suspicious Implementation Details

None. The implementation is straightforward deterministic rule-engine work. The rule ordering is clear and documented. The `_is_allowed` gate correctly checks `BehaviorPolicy.allowed_action_types`. The `_stable_action_id` hash is deterministic over safe identifiers. The `_candidate()` factory correctly delegates to the Pydantic `CandidateAction` constructor, which enforces T210 invariants including the cross-validator that `action_type` is in `policy.allowed_action_types`.

The public API surface (`plan()`) is intentionally narrow: it accepts `AgentSelfState`, optional `BehaviorPolicy`, and optional `safe_context_labels` (an `Iterable[str]`). It does not accept raw text, transcripts, or private content, which is verified by `test_public_plan_api_does_not_accept_raw_private_text_fields`.

The `do_nothing` fallback is correctly placed last in rule order and only fires when no other candidate was emitted, matching the task contract.

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py`: passed.
- `pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py -q`: 40 passed.
- Independent smoke test: thin context produces `do_nothing`, boundary flags produce `boundary_review_note`, signal refs produce `memory_review_prompt`, approved context refs produce `relationship_check_in_draft`, all safety invariants hold, action_ids are deterministic.
- `models.py` and `test_behavior_schema.py` were not modified (confirmed via `git diff HEAD`). No existing functionality was changed.

## Recommended Next Action

T211 is accepted as the deterministic rule-engine task for M10. The next task in sequence is T212 (proactive draft generator), which should consume these candidates and generate review-safe draft text without sending, scheduling, or platform execution.

The minor test gaps (M01-M05) can be addressed in a later hardening slice or during T212 if they become relevant to that task's scope.
