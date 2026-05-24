# Review: T195 — Relationship-Aware Reply Eval

Verdict: PASS_WITH_WARNINGS

## Summary

The worker evaluated whether approved relationship-state context (T194) changes `ReplyPlan` behavior. The task goal ("evaluate whether the same inbound scenario produces appropriately different ReplyPlan behavior under different approved relationship-state contexts") is technically met, and no code was modified. However, the evaluation contains a **significant factual error** in the claimed impact mechanism, which must be corrected before the handoff summary can be relied upon.

## Blocking Issues

**None.** The evaluation was performed, documented, and stays within evaluation-only scope. The factual error described below is non-blocking because it does not change the overall verdict (dimension-aware consumption is still absent) and the error can be corrected in documentation.

## Non-Blocking Issues

### W01 (CRITICAL): Worker's claimed keyword-match mechanism is incorrect

The worker's milestone review asserts that relationship context affects reply behavior through this chain:

```
relationship_context notes → keyword "relationship" matches _SENSITIVE_TOPIC_KEYWORDS → conservative_mode
```

This is **incorrect**. The actual code reveals:

1. **Language mismatch**: `_build_relationship_context_notes()` produces English text — `"relationship_context source=..."`, `"relationship_delta_count=N"`, `"relationship_delta <id>: ..."`. The `_SENSITIVE_TOPIC_KEYWORDS` are Chinese characters — `"关系"`, `"感情"`, `"家庭"`, `"父母"`, etc.

2. **`_contains_any` performs substring matching**: `keyword in text` after casefold. The Chinese character `"关系"` is NOT a substring of the English string `"relationship_context source=private/distilled"` — they are completely different Unicode code points. **The match never fires.**

3. **Ordering**: Relationship context notes are appended LAST to `combined_retrieval_notes`. The policy engine reads `memory_retrieval_notes[:3]` — the first 3 notes. Relationship notes would only be in the `[:3]` slice if all other note types (approved-store, approved-patch, derived-brief) contribute zero notes.

4. **Correct finding**: The relationship context from T194 has **ZERO behavioral impact** on reply plans. No code path consumes `ChatContext.relationship_context.deltas` for decision-making. The dimension-change values, delta summaries, and evidence refs are present in the context object but completely inert.

### W02 (Worker's W02, confirmed): Dimension-change values unused

The dimension-change values (magnitude, direction, dimension name) are present in `ChatContext.relationship_context.deltas` but not read by `ReplyPlanner` or `ReplyPlanPolicyEngine`. This finding is correct.

### W03 (Worker's W03, confirmed): Summary is informational only

`ChatContext.summary` carries relationship guidance text that flows into `ReplyPlanSourceContext.chat_context_summary`, but this field is not read by any decision point. This finding is correct.

### W04 (Minor): Allowed files overrun

Worker created `docs/for_human/T195_review_explanation.md` which is not listed in the allowed files (`docs/review/T195_milestone_review.md`, `docs/07_handoff.md`). This follows established project convention (every prior task creates a for_human explanation), but is technically a scope overrun.

## Missing Tests

N/A — T195 is evaluation-only; no code changes are expected and none were made.

## Suspicious Implementation Details

1. **Impact chain diagram is wrong**: The milestone review's central diagram shows a keyword match that does not exist. The diagram is misleading and should be corrected.

2. **Finding #1 overstates behavioral impact**: "Relationship context CAN change reply behavior, but only indirectly" is false in the current implementation. The correct finding is: "Relationship context does NOT change reply behavior in the current implementation. No consumption path exists."

3. **Verdict unaffected**: Despite this error, the practical conclusion (dimension-aware consumption is absent, relationship context is not semantically used) remains correct. The warnings list (W02-W03) captures the right gaps, and the recommended next actions are reasonable.

## Recommended Next Action

1. **Accept** T195 with `PASS_WITH_WARNINGS` — the evaluation task goal is met and no code was modified.

2. **Correct the handoff**: The `docs/07_handoff.md` "Relationship context impact summary" currently claims a keyword match that does not exist. It should be updated to state: *"The approved relationship context does NOT currently affect reply behavior. No code path consumes relationship dimension changes for decision-making. The dimension data exists in ChatContext but is semantically inert."*

3. **Post-M8 scope**: If dimension-aware reply planning is desired, add explicit consumption of `ChatContext.relationship_context.deltas` in `ReplyPlanPolicyEngine.build_profile()` by mapping specific dimension changes to policy adjustments (e.g., `boundary_risk` increase → additional boundary reminders or confidence penalty; `warmth` increase → slightly warmer base tone).

4. **The worker's milestone review** (`docs/review/T195_milestone_review.md`) should be corrected to remove the incorrect keyword-match claim. The review can otherwise stand with corrected findings.
