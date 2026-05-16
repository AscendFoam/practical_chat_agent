# T132 Review: Reply Policy

Reviewer: Claude Code (adversarial review)
Date: 2026-05-16

## Scope

Files changed:
- `src/practical_chat_agent/services/policy.py` (~327 new lines: `ReplyPlanPolicyProfile`, `ReplyCandidatePolicyAssessment`, `ReplyPlanPolicyEngine`)
- `src/practical_chat_agent/services/reply_planner.py` (refactored to thread `policy_profile` through all methods; new `_build_candidate` helper, conservative template branch, `_clamp_confidence`)
- `docs/07_handoff.md` (section 26 appended)

## Task Completion Check

| Requirement | Status |
|---|---|
| Preserve `ReplyPlanner.generate(context=...) -> ReplyPlan` contract | Met |
| Preserve T131 `priority_rank` unique ordering + `contact_id` alignment | Met (unchanged) |
| Handle `boundary_sensitive` risk category | Met (keyword + intent detection, conservative drafts) |
| Handle `over_proactive` risk category | Met (context-sensitive per-candidate detection with no-pressure exemption) |
| Handle `impersonation_risk` category | Met (keyword-based candidate text scanning) |
| Handle `thin_context` category | Met (explicit via policy profile, confidence penalty, conservative template set) |
| High-risk → at least one conservative / no-pressure candidate | Met (conservative mode shifts all 3 drafts to no-pressure wording) |
| `risk_flags` + `boundary_reminders` use reviewable language | Met (explicit English caution strings) |
| Candidate text stays from user perspective, no contact simulation | Met (templates unchanged in this regard) |
| Output remains valid T130 `ReplyPlan` with 3+ candidates | Met |
| `docs/07_handoff.md` updated | Met (section 26) |

## Forbidden Scope Check

- No auto-send, delivery connector, realtime platform, scheduler, outbound automation. Confirmed.
- No DB migration, vector DB, pgvector, embedding, persistence changes. Confirmed.
- No reading `private/chat_history/`. Confirmed.
- No full ContactSkill JSON, all memory facts, or raw transcript text injected into output surface. Confirmed (runtime texts used for keyword detection only, never echoed).
- No lowering of existing outbound `PolicyEngine` safety. Confirmed (existing `PolicyEngine` class untouched).
- No rewriting T131 into LLM drafting system. Confirmed (still deterministic templates).
- No advancing T133 or M4. Confirmed.

## Positive Findings

P01: **Clean separation of concerns.** `ReplyPlanPolicyEngine` is a standalone class in `policy.py`, injected through `ReplyPlanner.__init__(policy_engine=...)`. The planner remains focused on candidate assembly; the policy engine focuses on risk detection.

P02: **T131 N03 partially addressed.** T131 reviewer noted that `strategy_hints` and `relationship_summary` from the approved contact skill were unused. T132's `build_profile()` now reads `skill_texts = [relationship_summary, *strategy_hints]` for boundary and tone detection. `_shared_boundary_reminders()` also includes `strategy_hints[:1]`.

P03: **Context-sensitive over-proactivity.** In baseline context, `optional_follow_up` is not flagged as `over_proactive`. In conservative mode (thin context / boundary-sensitive / avoid-follow-up), it IS flagged. No-pressure cues ("先不往前推", "等你方便", "no rush") correctly exempt candidates from false-positive `over_proactive` flags.

P04: **Conservative template set is meaningfully different.** The `conservative_mode` drafts shift from invitation-style wording ("继续说说你现在最在意的是哪一部分") to explicit no-pressure wording ("你不用现在展开", "先不把话题往前推"). This is a visible behavioral change.

P05: **Impersonation detection is proactive.** Even though current templates don't contain impersonation cues, the detector runs on every candidate. This provides forward-compatibility when LLM-generated drafts are introduced later.

P06: **Confidence penalties are additive and traceable.** Each penalty (`thin_context` -0.10, `boundary_sensitive` -0.06, `over_proactive` -0.08, `impersonation_risk` -0.15) has a corresponding `risk_flag` and `boundary_reminder`. `_clamp_confidence` clamps to [0.0, 1.0].

P07: **No existing functionality broken.** `PolicyEngine` is untouched. `chat-reply-plan` CLI is unchanged. T131 tests would still pass.

## Non-blocking Issues

N01: **`runtime_texts` reads `latest_message_text`, event text, memory `fact`/`claim` for keyword detection.** `build_profile()` assembles a list including `context.latest_message_text`, event texts (up to 3), memory facts (up to 2), memory claims (up to 2), and retrieval notes (up to 3). These are passed to `_contains_any` for keyword matching only; they are never echoed into the output plan. This is safe by design (detection-only consumption), but it's worth noting because the approved-store brief fields and runtime text enter the policy detection path. The `[:2]`/`[:3]` caps keep exposure bounded.

**Why non-blocking:** The texts are consumed for keyword detection only and never appear in the output. This is analogous to a content filter scanning input without forwarding it. The task forbids injection into "prompt-facing / review-facing surface," not reading for internal classification.

N02: **`_SENSITIVE_TOPIC_KEYWORDS` includes "关系" which is broad.** "关系" (relationship) naturally appears in relationship summaries and strategy hints. If present, `sensitive_topic` becomes True, but `boundary_sensitive` requires either an explicit boundary cue OR `emotion_intent AND sensitive_topic`. The dual-condition logic prevents a single broad keyword from triggering conservative mode on its own.

**Why non-blocking:** The compound trigger condition provides adequate guard. False positive risk is low for expected input.

N03: **`_contains_any` does substring matching without word boundaries.** "space" matches "workspace", "loss" matches "glossary", "health" matches "unhealthy". This could cause false positives on unexpected input.

**Why non-blocking:** Current input texts are compact and controlled. Substring matching is the same approach used consistently in T112/T113. T150 could introduce boundary-aware matching if false positives appear in practice.

N04: **`_dedupe` is duplicated across `policy.py` (twice: `PolicyEngine` and `ReplyPlanPolicyEngine`) and `reply_planner.py`.** Three separate implementations of the same logic.

**Why non-blocking:** Minor code duplication. T150 or a future refactor could extract to a shared utility. No correctness risk.

N05: **No committed test or fixture.** Verification was inline synthetic only. Same as T131 N04.

**Why non-blocking:** Deferred to T150.

N06: **`_candidate_is_over_proactive` has two identical terminal branches.** The `if approach_label == "paced_next_step"` branch and the final `return` do the same thing. Dead conditional.

**Why non-blocking:** Minor redundancy. No correctness impact.

N07: **`build_profile` reads `memory.claim` from `approved_store_context.memory_facts`.** The task says "不把全部 memory facts 注入... surface". Reading `claim` for detection (limited to `[:2]`) is not injection, but it does consume compact approved text that T123 exposed.

**Why non-blocking:** Claims are used for keyword detection only, never echoed. The `[:2]` cap keeps it bounded. This is consistent with how `relationship_summary` and `strategy_hints` are consumed.

## Missing Tests

No committed automated tests. Expected per task scope; tracked for T150.

## Suspicious Implementation Details

None found. The implementation is straightforward keyword-based policy logic. No hidden state, no side effects, no network calls.

## Verdict

**PASS_WITH_WARNINGS**

T132 correctly adds a policy/boundary risk layer to the T131 ReplyPlanner. All four required risk categories (`boundary_sensitive`, `over_proactive`, `impersonation_risk`, `thin_context`) are handled with explicit detection, conservative template switching, per-candidate risk flags, boundary reminders, and confidence penalties. The T131 contract is preserved. No forbidden scope is violated. The policy engine is cleanly separated and injectable.

The warnings are quality concerns appropriate for future refinement: broad keyword matching, code duplication, and no committed tests. None block the task from proceeding.

## Warning Disposition (Captain action required)

- N01: **accepted** — runtime text consumed for keyword detection only, never echoed. Design is safe.
- N02: **accepted** — broad keyword "关系" mitigated by compound trigger condition.
- N03: **accepted/deferred** — substring matching is consistent with prior tasks; T150 may refine.
- N04: **accepted** — minor code duplication, no correctness risk.
- N05: **deferred** — automated tests tracked for T150.
- N06: **accepted** — dead conditional, no impact.
- N07: **accepted** — claim text consumed for detection only, bounded by `[:2]`.
