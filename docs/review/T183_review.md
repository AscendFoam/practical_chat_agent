# Review: T183

Verdict: `PASS_WITH_WARNINGS`

## Blocking Issues

None.

## Non-Blocking Issues

### N01 — `.claude/settings.json` modified outside Allowed Files

Permission entries for new test commands were added to `.claude/settings.json`, which is not in the task's Allowed Files list. This is the same pattern as every previous task from T160-T182 and has been consistently accepted as a workspace artifact.

**Accepted**: consistent with `PASS_WITH_WARNINGS` precedent.

### N02 — No committed test exercises the LLM-candidate merge success path

All 18 committed tests only exercise refusal and exception fallback paths for the hybrid mode:
- `TestHybridLlmUnavailable`: provider returns refusal (no API key)
- `TestHybridLlmError`: provider raises `RuntimeError`
- `TestCLIHybridFlag`: provider unavailable at CLI level

The `_merge_candidates()` success path (LLM returns valid candidates → merge → policy assessment → rerank) is validated **only** via the private live smoke test (`private/distilled/t183_smoke/`). If a future refactor breaks the merge logic or the `_build_llm_candidate` policy assessment path for valid LLM candidates, no committed test would catch it.

Low risk because:
- The merge code is simple, deterministic, and well-documented.
- The private smoke test produced and validated real hybrid output (1 template + 2 LLM candidates, contiguous ranks 1..3, policy assessment applied).
- The hybrid code path is additive and does not affect template-only mode.

A synthetic `LLMReplyGeneratorService` subclass returning valid candidates (test-only) would provide resilience against future regressions.

**Deferred**: acceptable for current scope; T184 or a follow-up can add merge-path coverage.

## Missing Tests

### M01 — No end-to-end hybrid success test

No committed test validates the scenario where LLM returns valid candidates that flow through `_merge_candidates()` → `normalize_ranks()` → policy assessment. A test-only subclass returning a valid `LLMReplyPlan` with candidates would cover this without a live provider call.

**Deferred**: low risk due to deterministic merge logic and private smoke validation.

### M02 — No explicit reranked-order assertion after merge

No committed test asserts that final `priority_rank` values are `[1, 2, 3]` after a hybrid merge. The `normalize_ranks()` function is imported and used, but the hybrid code path is not explicitly verified for rank contiguity by committed tests. Existing T150 tests cover this for template-only mode.

**Deferred**: same as M01.

## Suspicious Implementation Details

1. **`_RaisingGenerator` inherits with `api_key="sk-test"` only for exception testing** — The class raises before reaching provider calls, so configuration values are irrelevant. Acceptable for testing the exception catch.

2. **`disabled_generator` fixture passes `enabled=True` with `api_key=None`** — The generator correctly refuses via `availability_reason()` → `"OPENAI_API_KEY is not configured"`, so the test is correct. The `enabled=True` value is slightly misleading in naming but functionally harmless.

## Recommended Next Action

Proceed to **T184 (Planner Holdout Eval)**. Optionally add a committed test with a synthetic valid-candidate generator to protect the merge path against future refactors before or during T184.
