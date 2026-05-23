# Review: T184

Verdict: `PASS_WITH_WARNINGS`

## Blocking Issues

None.

## Non-Blocking Issues

### N01 — `.claude/settings.json` modified outside Allowed Files

Permission entries for evaluation commands were added to `.claude/settings.json`, which is not in the task's Allowed Files list. This is the same pattern as every task from T160-T183 and has been consistently accepted as a workspace artifact.

**Accepted**: consistent with `PASS_WITH_WARNINGS` precedent.

### N02 — Self-reported ratings without independent verification

The naturalness (3/5 → 4/5), evidence usage, boundary adherence, and other scores are self-reported by the worker based on manual inspection of all 12 output plans. No second reviewer independently rated the outputs. The review document transparently describes this as "self-reported by worker based on manual inspection," so there is no deception, but the ratings carry limited inter-rater reliability.

**Accepted**: acceptable for an MVP milestone eval; T184's task scope does not require blind review.

### N03 — Hybrid diversity metric is based on approach_label count only

The "candidate diversity" metric is measured as the count of unique `approach_label` values (3 per mode = equal). This does not capture semantic diversity of draft text. Two candidates with different labels could still be semantically similar. The per-scenario qualitative observations partially compensate for this.

**Accepted**: approach_label count is a reasonable first proxy; qualitative observations capture the remaining nuance.

## Missing Tests

The task package explicitly forbids adding new tests, fixtures, or code changes ("Do not add new tests, fixtures, or code changes as part of this task"). No test-coverage gap is therefore chargeable to T184.

The T183-deferred M01 (no committed synthetic valid-candidate merge test) is correctly re-identified in T184's findings and carried forward as a Gate M7 condition. This is the right disposition.

## Suspicious Implementation Details

None.

The private eval script (`private/t184_run_eval.py`) is a legitimate, well-structured automation tool that generates synthetic anonymized contexts, runs `chat-reply-plan` in both modes via subprocess, and collects structured analysis. It does not mock or fake any results — all 12 output plans are real `ReplyPlan` artifacts produced by the actual planner against a real Deepseek provider.

## Recommended Next Action

Accept the `Conditional` Gate M7 (Holdout Eval Stage) verdict and proceed with the worker's recommended **T185 Hybrid Planner Language and Safety Alignment** as a narrow follow-up task to fix:
1. LLM output language mismatch (enforce Chinese to match template language).
2. LLM safety constraint bypass in thin_context/boundary_sensitive scenarios.
3. Committed regression test for the valid-candidate merge path (closes T183 M01).

T185 must stay narrow: no new provider integrations, no expansion of planner scope, and no change to template-only mode behavior.
