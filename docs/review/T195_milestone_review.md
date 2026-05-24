# Review: T195 - Relationship-Aware Reply Eval

Verdict: PASS_WITH_WARNINGS

## Evaluation Method

Traced the end-to-end data flow from `ApprovedRelationshipContext` (T194) through `ChatContextAssembler` -> `ReplyPlanPolicyEngine` -> `ReplyPlanner` -> `ReplyPlan`. Checked every code path where approved relationship context could change reply behavior.

## Impact Chain

```text
ApprovedRelationshipContext (loaded)
  -> ChatContextAssembler adds relationship_context plus summary / retrieval-note text
  -> ReplyPlanner does not read relationship_context.deltas
  -> ReplyPlanPolicyEngine does not read relationship_context.deltas
  -> PolicyEngine sensitive-topic scan only checks memory_retrieval_notes[:3]
  -> relationship-context notes are English while sensitive-topic keywords are Chinese substring checks
  -> the claimed note-keyword trigger does not fire
  -> no reply-plan behavior changes result from approved relationship context today
```

## Findings

### 1. Relationship context does NOT currently change reply behavior

The corrected code-path analysis shows no active behavioral mechanism. The worker's original keyword-match explanation was wrong:

- relationship-context notes are English (`relationship_context ...`)
- `_SENSITIVE_TOPIC_KEYWORDS` are Chinese substring checks
- the policy engine only inspects `memory_retrieval_notes[:3]`

So the claimed trigger path does not fire, and approved relationship context currently has zero behavioral effect on `ReplyPlan` output.

### 2. Dimension-level nuance is absent

The `ApprovedRelationshipDeltaBrief` contents (dimension changes, delta summary, evidence refs) are not directly consumed by `ReplyPlanner` or `ReplyPlanPolicyEngine`.

They exist in:

- `ChatContext.relationship_context.deltas` -> populated but unused for decision-making
- `ChatContext.summary` -> stored in `ReplyPlanSourceContext.chat_context_summary`, informational only
- `memory_retrieval_notes` -> visible text only, not semantic relationship-state consumption

There is no code path that maps a dimension change such as `boundary_risk` increase to a concrete planner or policy adjustment.

### 3. Summary and retrieval-note surfaces are observational only

`ChatContext.summary` can include approved relationship guidance text, and relationship notes can appear in retrieval notes. These surfaces are review-visible, but they are not consumed by any decision point in the reply pipeline.

### 4. M8 result is infrastructure plus evaluation, not planner completion

The repository now has:

- approval-gated relationship-state contracts and review flow
- compact runtime context exposure
- a completed evaluation proving what the current planner does and does not consume

What it does not have is semantic planner usage of relationship deltas. That remains later scoped work.

## Recommended Next Actions

1. Accept T195, but correct any handoff or milestone-review language that claims the current planner is already relationship-aware.
2. If dimension-aware behavior is desired later, add explicit `relationship_context` consumption in `ReplyPlanPolicyEngine.build_profile()` or equivalent planner logic.
3. Keep T200/M9 separate from this gap; T195 is evaluation-only and does not authorize implementation changes.

## Scope Compliance

- Allowed files: `docs/review/T195_milestone_review.md`, `docs/07_handoff.md`
- No code changes: verified
- No private artifacts committed: verified
- No state application or context mutation: verified

## Verdict: PASS_WITH_WARNINGS

**W1**: The worker's original keyword-match mechanism claim was incorrect and required correction in captain governance sync.

**W2**: The dimension-change values (magnitude, direction, dimension name) are present in `ChatContext` but not directly used by `ReplyPlanner` or `PolicyEngine`. Dimension-aware draft adjustment is not implemented.

**W3**: The `ReplyPlanSourceContext.chat_context_summary` field and relationship retrieval notes carry visible guidance text but are informational only; they do not affect any decision point in the pipeline.
