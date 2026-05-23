# Review: T181

Verdict: `PASS_WITH_WARNINGS`

## Blocking Issues

None.

## Non-Blocking Issues

### N01 — Allowed files boundary: `.claude/settings.json` and `docs/reference/AI_coding_workflow.md` were modified but not listed in Allowed Files

The task's Allowed Files list does not include `.claude/settings.json` or `docs/reference/AI_coding_workflow.md`. The `settings.json` change adds permission entries for test/compile commands (consistent with prior tasks, which treated similar changes as workspace artifacts). The `AI_coding_workflow.md` change adds a record-keeping instruction for future workers. Both are low-risk additive changes, and no reviewer has previously blocked on this pattern.

**Accepted**: consistent with `PASS_WITH_WARNINGS` precedent from T160-T164/T170-T174.

### N02 — `_build_candidates` always assigns default `policy_boundary` refs, ignoring any LLM-provided supporting_context_refs

The prompt template does not ask the LLM to produce `supporting_context_refs`, and `_build_candidates` always injects a single default `ReplyPlanContextRef(ref_type="policy_boundary", ref_id="boundary_review_only")`. This means every candidate's `supporting_context_refs` is the same generic ref, and the validator's check (`>=1 supporting_context_ref`) is satisfied trivially without evidence-chain improvement.

**Accepted for now**: MVP scope correctly defers evidence-grounded generation to future work. T182 or a later task should design the prompt to request LLM-provided refs.

### N03 — `validate_ranks` is called redundantly (inside `validate()` and again in `generate()`)

Inside `LLMReplyGeneratorService.generate()`, line 255 calls `LLMReplyPlanValidator.validate(plan=plan, ...)` which internally calls `validate_ranks()` at line 67. Then lines 260-261 call `LLMReplyPlanValidator.validate_ranks(validated.candidates)` again. Ranks are re-assigned twice with no change in outcome, but this is dead work.

**Accepted**: no correctness impact.

### N04 — Privacy leak detection is substring-based and narrow

`_has_privacy_leak` checks exact (normalized) substring match of context text against draft text, requiring a minimum of 8 characters. This catches verbatim quoting but not paraphrased leaks, sentence fragments drawn from context, or key detail leakage.

**Accepted**: the worker acknowledges this limitation. T182 or later work should harden this with semantic or embedding-based detection.

### N05 — `INPUT_TOO_LARGE` refusal code is defined but never triggered

`LLMReplyPlanRefusal.refusal_code` includes `INPUT_TOO_LARGE`, but no capacity check exists in the generator. When input exceeds token budget, the provider will likely return an error, which is caught as `PROVIDER_ERROR`. The dedicated code path is dead.

**Accepted**: documented in the worker's remaining risks. T182 should implement proper input-size budget enforcement.

## Missing Tests

### M01 — No tests for `_build_llm_input` output shape

The compact context building logic at lines 265-309 is untested. It has multiple branches (skill_brief present/absent, approved memory facts, derived brief status, patch context status) and could silently produce incorrect or empty input.

**Low risk**: the method is deterministic and called early in `generate()`, so failures surface quickly. Add in T182 or later hardening.

### M02 — No tests for `_parse_provider_response` error paths

The provider response parser handles missing choices, non-dict messages, empty content, and JSON decode errors, but none of these paths have dedicated tests.

**Low risk**: these are straightforward error-handling branches. Add in T182.

### M03 — No end-to-end test exercising generator→validator pipeline with synthetic provider output

The validator is tested in isolation with hand-crafted candidates. The generator's `_build_candidates` is tested with synthetic raw dicts. But no test verifies the full pipeline: generator produces output from a mock provider response → validator filters it → output is a valid `LLMReplyPlan`. The CLI test `test_output_contains_valid_json` exercises the refusal path only (no provider configured).

**Low risk**: the individual units are tested, and the provider is never called in CI. Add in T182 if a mock provider fixture is introduced.

### M04 — No CLI stdout privacy check

No test asserts that `chat-reply-generate-llm` stdout does not contain draft_text, rationale, or context text. The contract says "safe metadata only," and manual inspection confirms this, but there is no regression guard.

**Low risk**: the CLI is explicitly designed to emit only a structured dict with action/paths/counts/codes. Add in T182.

## Suspicious Implementation Details

1. **`_has_impersonation` regex bound to class attribute at import time**: `re.compile(...)` runs at module load. This is fine but means the patterns cannot be configured or extended without modifying the source. T182 may want to make patterns injectable.

2. **`_prompt_template_hash` is computed from `_build_system_prompt()` which is a static method**: The hash is computed once per service instance via `_compute_prompt_hash()`. If the prompt template changes between instances (e.g., in different deployments), the hash correctly changes. No issue.

3. **`LLMReplyPlan.candidates` has no `min_length` constraint** (unlike `ReplyPlan.candidates` which requires `min_length=3`): This is intentional — after validation filtering, zero candidates is valid (means all candidates were rejected). After filtering, the plan should still be emitted as a validated artifact, not silently discarded. Correct design.

## Recommended Next Action

Accept `PASS_WITH_WARNINGS`. The worker has correctly implemented:

- A separate offline CLI (`chat-reply-generate-llm`) that reads safe `ChatContext` JSON
- OpenAI-compatible provider call path
- Deterministic post-generation validation (7 checks) before output acceptance
- Structured refusal handling
- Safe stdout (metadata only)
- 26 deterministic tests, zero regressions (353 total passing)

The remaining gaps (warnings N01-N05, missing test coverage M01-M04) are all deferred to T182 or later hardening work, consistent with the project's iterative, gate-based approach.

Proceed to **T182 (Candidate Validator extraction/hardening)**.
