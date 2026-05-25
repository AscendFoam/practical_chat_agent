# Review: T212

Verdict: PASS

## Summary

T212 adds `ProactiveDraftGenerator` to `src/practical_chat_agent/services/behavior_planner.py`, a deterministic enrichment service that populates `CandidateActionPayload.draft_text` for review-only candidate actions. The implementation is purely additive, draft-only, and strictly non-executing. No message sending, scheduling, platform integration, LLM calls, memory mutation, CLI commands, runtime wiring, or raw transcript paths were introduced. The existing `BehaviorRulePlanner` code is unchanged.

## Blocking Issues

None.

## Non-Blocking Issues

N01. `docs/for_human/T212_review_explanation.md` and `docs/worker_summary/T212_worker_summary.md` allowed-files overrun. Accepted as established convention noise consistent with all prior reviews.

N02. Draft texts are static string literals keyed by `BehaviorActionType`. The texts for `reply_follow_up_draft` and `topic_suggestion` are included in `_PROACTIVE_DRAFT_TEXTS` even though neither action type is produced by the current T211 `BehaviorRulePlanner` rules. This is forward-compatible scaffolding — the drafts are available if future rules or callers produce these action types, and the code is harmless. However, there is no committed test that exercises these two action types through the planner+generator pipeline end-to-end.

N03. `_draft_text_for` has a `KeyError` fallback returning `"Review only: no proactive draft text is available."` with `pragma: no cover`. The fallback is unreachable in normal use because `BehaviorActionType` is a `Literal` constrained by Pydantic validation. The `pragma: no cover` is acceptable but the fallback text could differ from the dict value style slightly (no trailing period, different phrasing). This is cosmetic and non-blocking.

N04. The `enrich()` method uses `model_copy(update=...)` to produce a new `CandidateAction` with the enriched payload, which is correct immutability-preserving behavior. However, `model_copy` does not re-run validators on the copy. This is safe here because the only change is adding `draft_text` to an already-validated payload, and `draft_text` is an optional string field with no validator constraints. But if future schema changes add `draft_text` validators, the `model_copy` path would bypass them. Worth noting as a minor design observation.

N05. `ProactiveDraftGenerator` does not verify that the input candidate has `draft_text=None` before overwriting it. If called on an already-enriched candidate, it silently replaces the existing draft text. This is acceptable for scope (the generator is intended for initial enrichment only) but callers should be aware.

## Missing Tests

M01. No committed test exercises the `Mapping` input path where the mapping contains `draft_text` already set (verifying it gets overwritten vs preserved). The current mapping test (`test_enrich_accepts_stable_mapping_inputs_without_private_text_fields`) uses a fresh planner output that has `draft_text=None`.

M02. No committed test exercises the `reply_follow_up_draft` or `topic_suggestion` action types through the end-to-end planner+generator pipeline. These types exist in `_PROACTIVE_DRAFT_TEXTS` and in `test_enriches_all_supported_candidate_types_with_draft_text` via synthetic construction, but the T211 planner never produces them, so the full pipeline is untested for these types.

M03. No committed test verifies that `enrich()` is idempotent when called twice on the same candidate (producing identical output). The implementation appears deterministic and correct, but this is untested.

## Suspicious Implementation Details

None. The implementation is straightforward deterministic text lookup. The `_PROACTIVE_DRAFT_TEXTS` dict maps each `BehaviorActionType` to a short, review-only string. The `enrich()` method correctly accepts both `CandidateAction` objects and mappings, validates mappings through `model_validate`, and produces a new copy with the draft text populated. All safety invariants are preserved through the immutable copy pattern.

The draft texts themselves are appropriately conservative:
- All contain "review" or "Review only" framing
- None contain send/schedule/platform semantics
- `relationship_check_in_draft` explicitly mentions "low-pressure", "optional", and "non-committal"
- `boundary_review_note` mentions "boundary-sensitive" context checking
- `do_nothing` is a clear no-action statement

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py`: passed.
- `pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py -q`: 48 passed (25 schema + 15 T211 rule planner + 8 T212 draft generator).
- Independent smoke test: `enrich()` correctly populates draft text for `do_nothing` and `relationship_check_in_draft`, preserves all safety invariants, and accepts mapping inputs.
- `models.py` and `test_behavior_schema.py` were not modified. No existing functionality was changed. The `BehaviorRulePlanner` class is completely unchanged.

## Recommended Next Action

T212 is accepted as the deterministic draft-enrichment task for M10. The next task in sequence is T213 (CandidateAction review CLI), which should consume these enriched candidates and provide human review capabilities without sending, scheduling, or platform execution.

The minor test gaps (M01-M03) can be addressed in a later hardening slice or during T213 if they become relevant.
