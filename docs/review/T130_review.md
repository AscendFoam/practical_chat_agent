# T130 Review: ReplyPlan Schema

Reviewer: Claude Code reviewer
Date: 2026-05-15

## Scope

T130 定义 ReplyPlan schema 和 prompt contract。任务包：`docs/tasks/M3_relationship_reply_planner/T130_reply_plan_schema.md`

审查范围：本次 diff 涉及 3 个文件。

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/reply_plan_contract.md`
- `docs/07_handoff.md`

## Checklist

### 1. Task completion

任务包要求：

| 要求 | 状态 |
| --- | --- |
| Represent at least 3 candidate reply drafts | Done — `ReplyPlan.candidates` has `min_length=3` |
| Per-candidate: draft text, rationale, cited refs, risk flags, boundary reminders, confidence | Done — `ReplyPlanCandidate` has all fields; `supporting_context_refs` min_length=1, `boundary_reminders` min_length=1, `confidence` optional |
| Overall planning metadata: contact_id, source context ids, policy/boundary summary, notes on differences | Done — `ReplyPlan` has `contact_id`, `source_context`, `policy_boundary_summary` (min_length=1), `notes_on_candidate_differences` (min_length=1) |
| Compatible with T123 ChatContext brief | Done — `ReplyPlanSourceContext.approved_store_status` reuses `ApprovedStoreContextStatus` literal; `approved_contact_skill_record_id`, `approved_memory_record_ids`, `approved_store_evidence_refs` accept T123 compact ids |
| Prompt contract expectations (review-only, no impersonation, conservative for uncertain) | Done — Section 1 and Section 6 of `reply_plan_contract.md` |
| Field names explicit and review-friendly | Done — all names are self-documenting |
| Do not overfit to one contact or demo | Done — `contact_id` is generic, no hardcoded values in models |

### 2. No forbidden scope violations

| Forbidden | Check |
| --- | --- |
| No LLM call | Confirmed — no new service, no LLM import |
| No reply generation logic | Confirmed — only schema models |
| No message sending | Confirmed |
| No auto-rewrite of ContactSkill/memory/policy | Confirmed |
| No DB / migration / vector DB | Confirmed |
| No reading `private/chat_history/` | Confirmed |
| No raw transcript / real names / platform IDs in docs | Confirmed — contract uses `contact_xxx`, `skillstore_001`, synthetic example text |

### 3. No pseudo-implementation / mock / stub / hardcode

All four new models (`ReplyPlanContextRef`, `ReplyPlanSourceContext`, `ReplyPlanCandidate`, `ReplyPlan`) are real Pydantic models with proper field constraints. No mock data, no placeholder functions, no hardcoded logic.

`ReplyPlanMode = Literal["candidate_review_only"]` is a correct Literal type — not a hardcoded string pretending to be an enum. It is extensible: if future modes are needed, the Literal can be extended.

`ReplyPlanContextRefType` covers all reference types needed for T123 integration and future T131/T132.

### 4. Verification adequacy

Worker ran:

- `compileall src/practical_chat_agent/core/models.py` — passed.
- Synthetic `ReplyPlan.model_validate(...)` with 3 candidates — confirmed schema can hold 3+ candidates, cite approved-store ids, and does not require raw transcript.

I independently re-ran compileall and it passed. The synthetic validation is adequate for a schema-only task.

### 5. Over-engineering check

The models are minimal: 4 Pydantic classes + 2 Literal types. No unnecessary abstractions, no inheritance hierarchies beyond what Pydantic requires, no helper methods, no validators beyond field constraints. This is appropriately scoped for a schema definition task.

`ReplyPlanSourceContext` has 7 fields, all directly related to the task package's requirement for "source context ids." None are speculative.

### 6. Existing functionality preserved

- `ChatContext`, `ApprovedStoreContext`, `ChatSuggestion`, `AgentTurnResult`, and all other existing models are untouched.
- No changes to `chat_context.py`, `container.py`, or `main.py`.
- The new models are standalone additions, not modifications to existing types.

### 7. Documentation quality

`reply_plan_contract.md` is well-structured:

- Section 1: Usage boundary — clear anti-impersonation and review-only rules.
- Section 2: T123 compatibility — explains how `ReplyPlan` consumes compact brief.
- Section 3–5: Schema overview and field semantics — complete field table with required/optional annotations.
- Section 6: Prompt contract expectations — actionable rules for T131.
- Section 7: Validation expectations.
- Section 8: Non-goals.

No docs claim unverified work is done. The contract explicitly states it is "for candidate generation and review only."

### 8. Privacy / data safety

- No real contact names, chat text, or platform IDs in any changed file.
- JSON example in contract uses `contact_xxx`, synthetic `skillstore_001`, etc.
- `draft_text` examples in the contract are generic Chinese phrases, not extracted from real conversations.

## Non-blocking Issues

### N01: `ReplyPlanMode` is currently a single-value Literal

`ReplyPlanMode = Literal["candidate_review_only"]` has exactly one value. This is correct for T130 — no other mode is needed now. If T131+ introduces modes like `"auto_select"` or `"batch_review"`, this Literal should be extended. No action needed now; just noting for awareness.

### N02: `priority_rank` has no uniqueness constraint within a ReplyPlan

`ReplyPlanCandidate.priority_rank` uses `ge=1` but nothing prevents two candidates from having the same rank. This is a minor modeling gap — Pydantic does not natively support cross-field uniqueness within a list. T131 should either sort by `priority_rank` or ensure the planner assigns unique ranks. Low risk for a schema-only task.

### N03: `approach_label` is free-form string

`approach_label` has `min_length=1` but no enum constraint. The contract JSON example uses `"conservative_acknowledgment"`, `"light_follow_up"`, `"warm_but_guarded"`. This is acceptable for MVP — later tasks can tighten if needed.

### N04: `ReplyPlanSourceContext` does not carry `contact_id`

The `contact_id` lives on `ReplyPlan` itself, not on `ReplyPlanSourceContext`. This means `ReplyPlanSourceContext` could theoretically be populated with ids from a different contact than the parent plan. This is a low-risk modeling choice — T131 can validate at assembly time. Noting for awareness.

## Blocking Issues

None.

## Missing Tests

T130 is a schema-only task. The task package does not require automated tests. Compile verification and synthetic model validation are adequate.

Per project convention, automated Pydantic model validation tests are deferred to T150 (R031/R032/R033 pattern).

## Verdict

**PASS_WITH_WARNINGS**

T130 correctly implements the ReplyPlan schema and prompt contract without scope violations, pseudo-implementation, or privacy leaks. The schema supports 3+ candidates, is compatible with T123, and the contract documentation is thorough and honest. The four non-blocking issues are minor modeling observations, not correctness problems.

## Summary for Captain

- T130 is complete and ready for T131.
- N01–N04 are non-blocking; Captain decides whether to accept or defer.
- T131 should note: `priority_rank` uniqueness, `approach_label` validation, and `contact_id` alignment between `ReplyPlan` and `ReplyPlanSourceContext`.
- No R-numbered new risk items needed beyond existing R028–R033.
