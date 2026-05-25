# T211 Review Explanation

## What This Task Is About (In Plain Language)

In T210, the project defined the data shapes (schemas) for proactive behavior suggestions — things like "maybe check in with this friend" or "review the boundary-sensitive context before suggesting anything." But those schemas were just empty forms; nobody was filling them in.

T211 builds the first "brain" that can actually look at a situation and decide what suggestions to propose. It's a simple, deterministic rule engine: given some information about the current state (who the user is, what contacts are relevant, what risk flags exist), it applies a fixed set of conservative rules and produces a list of draft-only suggestion candidates.

Think of it like a cautious advisor who looks at your situation and says "here are some things you *might* want to do — but you need to review each one before anything happens." The advisor never sends messages, never schedules anything, and never acts on its own.

## What The Implementation Changed

### Code Changes

**New service added: `src/practical_chat_agent/services/behavior_planner.py`**

The `BehaviorRulePlanner` class has one public method: `plan()`. It takes:

1. **`self_state`** (`AgentSelfState`): A compact snapshot of what the assistant knows about the current situation — who the agent is, who the user is, what contact is relevant, what approved information is available, any risk flags.
2. **`policy`** (optional `BehaviorPolicy`): Rules about what kinds of suggestions are allowed. If not provided, a default policy is used.
3. **`safe_context_labels`** (optional list of strings): Short caller-provided labels like `"memory_review"` or `"boundary_sensitive"`.

The method runs four rules in a fixed, deterministic order:

1. **`boundary_review_note`**: If risk flags or labels indicate boundary-sensitive context, produce a conservative review note. This says "slow down and review the boundary situation before suggesting any proactive behavior."
2. **`memory_review_prompt`**: If there are recent safe signal refs or labels requesting memory/relationship review, produce a prompt to check recent memory or relationship signals.
3. **`relationship_check_in_draft`**: If there is at least one approved context ref and no hard proactive-blocking risk flags (like `thin_context`, `boundary_sensitive`, `privacy_risk`, etc.), suggest a low-pressure relationship check-in.
4. **`do_nothing`**: If no other rule fired and the policy allows it, emit a "do nothing" candidate. If the policy doesn't allow `do_nothing` either, return an empty list.

Each rule checks whether its action type is allowed by the policy before emitting a candidate. After all rules fire, the result is truncated to `max_candidates`.

Every emitted candidate:
- Is a valid `CandidateAction` from T210
- Has `human_review_required=True` (cannot be bypassed)
- Has `auto_send_allowed=False` (cannot be changed)
- Has at least one supporting context reference
- Contains no forbidden metadata keys (no `send_at`, `platform`, `access_token`, etc.)

**New tests added: `tests/test_behavior_rule_planner.py`**

15 tests in 4 test classes:
- `TestBehaviorRulePlannerFallback` (2 tests): Thin context produces `do_nothing`; disallowed `do_nothing` produces empty list.
- `TestBehaviorRulePlannerRules` (4 tests): Boundary input, signal refs, approved context ref requirement, hard risk blocking.
- `TestBehaviorRulePlannerOrderingAndPolicy` (4 tests): Deterministic ordering, `max_candidates` limit, policy disallows rules, policy disallows `do_nothing`.
- `TestBehaviorRulePlannerCandidateSafety` (5 tests): Candidates validate as `CandidateAction`, safety invariants preserved, no forbidden metadata, supporting refs preserved, public API rejects raw text parameters.

**Updated contract document: `docs/data_contracts/behavior_planner_contract.md`**

Added sections documenting T211 rule-engine scope, input boundary, rule firing semantics, output ordering and limits, and the relationship to later M10 tasks (T212/T213/T214).

### What Was NOT Changed

- `src/practical_chat_agent/core/models.py` was not modified.
- `tests/test_behavior_schema.py` was not modified.
- No existing models, services, CLI commands, or runtime behavior was changed.
- No message sending, scheduling, platform integration, or automation was added.
- No LLM calls, embeddings, vector databases, or external services were introduced.
- No memory, ContactSkill, relationship state, or approved store mutation occurred.
- No raw chat history or private content was read or committed.

## Why This Matters For The Project

This is the first executable layer of **Milestone 10 (BehaviorPlanner)**. The M10 roadmap in `docs/04_task_board.md` shows:

- T210 (done): Define the data schemas for behavior candidates
- **T211 (this task)**: Build the rule engine that generates candidates
- T212 (next): Generate proactive draft text
- T213: Build a review CLI for humans to approve/reject candidates
- T214: Safety evaluation

T211 proves that the repo can produce candidate actions deterministically while preserving all T210 safety invariants. The rule engine is intentionally conservative and under-generative: it prefers fewer candidates with clear rationale over speculative proactive behavior. This is by design — the project's core principle is that the assistant should never act on its own without human review.

The architecture follows the same pattern used successfully in earlier milestones:
- M8 (RelationshipState) built T191 signal extraction before T192 delta generation and T193 review
- M9 (MemoryRetrieval) built T200 contracts before T201 local retriever and T202 eval
- M7 (LLM Planner) built T180 contracts before T181 offline CLI and T182 validation

The key design decisions in T211:
1. **Fixed rule order**: Rules always fire in the same order, making output predictable and testable.
2. **Policy enforcement before emission**: Each rule checks the policy's `allowed_action_types` before creating a candidate, preventing unauthorized candidates from ever being constructed.
3. **Stable action IDs**: Candidate IDs are deterministic hashes of safe identifiers, enabling idempotent re-planning.
4. **No raw text input**: The public API only accepts compact safe labels and references, never raw transcripts or chat history.

## Why I Gave PASS

The task goal is fully met. The worker:

1. **Implemented the deterministic rule engine** with all four required rules (`boundary_review_note`, `memory_review_prompt`, `relationship_check_in_draft`, `do_nothing`) in the documented fixed order.

2. **Preserved all T210 safety invariants** on every emitted candidate through the Pydantic model constructors, which enforce `Literal[True]`/`Literal[False]` at the type level.

3. **Provided adequate test coverage** (15 tests) covering all 12 test categories listed in the task spec: thin context fallback, deterministic ordering, `max_candidates` limit, policy enforcement, candidate validation, safety invariants, forbidden metadata absence, supporting refs, boundary-sensitive behavior, memory/review signal behavior, relationship check-in requirements, and no raw text API surface.

4. **Stayed within scope** — no forbidden activities (no sending, scheduling, platform integration, memory mutation, LLM calls, raw transcript access, models.py changes, or existing file modifications).

5. **Updated the contract document** with clear T211 scope documentation including rule semantics, input boundaries, output ordering, and downstream task relationships.

6. **Passed all verification**: compilation, 40 combined T210+T211 tests, and a full test suite (762 tests passed, no regressions).

There are five minor test coverage gaps (M01-M05): no test for label-only memory-review triggering, no test for each individual proactive-blocking flag, no test for `contact_id=None` fallback, no test for single boundary note on multiple flags, and no test for label-triggered boundary review. These are non-blocking because the implementation is correct (confirmed via independent smoke testing), the rules are simple and deterministic, and the gaps can be closed in a later hardening slice.
