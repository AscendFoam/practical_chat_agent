# Review: T185

Verdict: `PASS_WITH_WARNINGS`

## Blocking Issues

None.

## Non-Blocking Issues

### N01 — `.claude/settings.json` modified outside Allowed Files

Permission entries for T184 eval and T185 compile/test commands were added to `.claude/settings.json`, which is not in the task's Allowed Files list. This is the same pattern as every task from T160-T184 and has been consistently accepted as a workspace artifact.

**Accepted**: consistent with `PASS_WITH_WARNINGS` precedent.

### N02 — Safety context detection is heuristic

The `thin_context` / `boundary_sensitive` detection in `_build_llm_input()` uses substring matching on `approved_store_context.status` and `boundary.sensitivity_summary` rather than integrating with the `ReplyPlanPolicyEngine`. This means:
- `thin_context` triggers when no approved store data exists, which is correct but also triggers for any case where the store is simply not configured (even when the planner might have enough context from other sources).
- `boundary_sensitive` detection uses substring match on `"sensitive"` or `"high"`, which may produce false positives (e.g., "not sensitive" still matches) or false negatives (e.g., "elevated concern" without the word "sensitive").

The worker acknowledges this in remaining risks. Acceptable for the narrow prompt-level scope and because the policy engine still provides a second layer of defense.

### N03 — Language enforcement is prompt-level, not hard enforcement

The Chinese language requirement (rule 6) is implemented as a prompt instruction rather than as a post-generation validator check. An LLM that ignores the instruction could still produce English text without detection. The worker acknowledges this in remaining risks.

This is an acceptable trade-off for the current scope: adding a language detection validator would require either heuristics (character set detection) or a separate classifier, which would be over-engineering for the narrow alignment task. The deterministic validator already catches impersonation and privacy leaks as a second line of defense.

## Missing Tests

None. The task's primary test gap (merge success path regression) is addressed by the 3 new `TestHybridMergeSuccessPath` tests. These tests:
- Verify template[0] is preserved as safety baseline (`test_merge_keeps_template_first`)
- Verify LLM candidates replace template ranks 2+ (`test_merge_includes_llm_candidates`)
- Verify final ranks are contiguous 1..3 (`test_merge_ranks_contiguous`)

This closes T183's M01 (no end-to-end hybrid success test) and M02 (no explicit reranked-order assertion) gaps.

A secondary test gap (no test that the system prompt text actually contains the Chinese instruction) is acceptable: testing prompt text existence would be testing the source code literal, not LLM behavior, and testing actual LLM output language would require a live provider call.

## Suspicious Implementation Details

### 1. `_MockSuccessGenerator` is a test-only subclass — correctly scoped

The `_MockSuccessGenerator` is defined inside the test file and returns pre-built valid candidates without calling a real provider. This is precisely the pattern recommended by the task ("If a minimal test helper is needed, keep it inside the existing hybrid test surface"). It is not shipped as production code.

### 2. `_normalize_label` regex is correct

The normalization pipeline (`strip().lower()` → `re.sub(r"[^a-z0-9]+", "_")` → `strip("_")` → `re.sub(r"_+", "_")` → `or "llm_generated"`) handles all edge cases correctly:
- Mixed-case and punctuation → clean snake_case
- All-non-alphanumeric → falls back to "llm_generated"
- Multiple contiguous separators → collapsed to single underscore

### 3. No changes to `reply_planner.py` or `app/main.py` needed

The worker correctly identified that all fixes were prompt/label/validation-level and required no planner or CLI changes. This is the right call — narrower than the allowed files scope.

## Recommended Next Action

Accept T185 as complete. Gate M7 conditions (language alignment, safety constraints, label normalization, merge-path test) are all resolved.

The M7 holdout gate should now be revisited. If the Captain agrees that T185 resolves the four Gate M7 conditions, the gate can be moved to a positive verdict, allowing M8 (RelationshipState) to begin.

Remaining open items for the Captain's attention:
- **LLM confidence calibration** (R039 subset) was explicitly deferred by T185 and remains open.
- **Safety context detection** could be improved by integrating with `ReplyPlanPolicyEngine` in a future task, but is acceptable for current scope.
- **Language enforcement** remains prompt-level; a future task could add post-generation language detection if mixed-language output becomes a real problem.
