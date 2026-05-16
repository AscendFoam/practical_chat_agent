# T131 Review: Relationship-Aware Reply Planner

Reviewer: Claude Code (adversarial review)
Date: 2026-05-16

## Scope

Files changed:
- `src/practical_chat_agent/services/reply_planner.py` (new file, 329 lines)
- `src/practical_chat_agent/app/main.py` (new `chat-reply-plan` CLI command, ~55 lines added)
- `docs/07_handoff.md` (section 23 appended)

## Task Completion Check

| Requirement | Status |
|---|---|
| Service generates ReplyPlan from compact ChatContext | Met |
| At least 3 candidates | Met (exactly 3) |
| Each candidate has draft_text, rationale, cited refs, risk_flags, boundary_reminders, confidence | Met |
| Candidates are meaningfully distinct, not minor paraphrases | Met (structurally distinct: acknowledgment vs optional follow-up vs paced next-step) |
| Planner consumes compact approved-store context only | Met |
| Planner does not require raw transcript text | Met |
| `priority_rank` values are stable and unique | Met (hardcoded 1/2/3, validated by `_validate_plan`) |
| `ReplyPlan.contact_id` aligns with source context | Met (validated by `_validate_contact_alignment`) |
| CLI or service can generate a plan from safe synthetic context | Met (`chat-reply-plan` CLI) |
| No send logic, DB integration, vector DB, policy rewrite, or private transcript leakage | Met |
| handoff.md updated | Met (section 23) |

## Forbidden Scope Check

- No message sending. Confirmed.
- No contact impersonation or "what the other person would say" output. Confirmed.
- No raw transcript reading from `private/chat_history/`. Confirmed.
- No full raw transcript, full ContactSkill JSON, or all memory facts injected. Confirmed.
- No DB migration, vector DB, realtime platform integration, policy rewrite, auto-approval, or automatic sending. Confirmed.

## Positive Findings

P01: **T130 warning enforcement is correct.** `_validate_contact_alignment` checks both `ApprovedStoreContext.contact_id` and the approved skill's `contact_id` against `ChatContext.user_id`. `_validate_plan` verifies unique and sequential `priority_rank`. These address both T130 N02 and N04 directly.

P02: **Safe summary reconstruction.** `_build_safe_context_summary` rebuilds a summary from platform enum values, counts, and status strings instead of copying `ChatContext.summary` or `latest_message_text`. Raw message text does not leak into the plan.

P03: **Clean ref provenance.** Candidate refs are built only from approved record ids, evidence refs, recent event ids, runtime memory hit ids, and policy-boundary refs. `source_record_ids` is never read, so non-approved ids cannot leak.

P04: **Thin-context awareness.** When `approved_store_status != "loaded"`, the planner adds `_BOUNDARY_THIN_CONTEXT`, lowers confidence values, and appends a note about conservative positioning.

P05: **Minimal CLI surface.** `chat-reply-plan` reads a ChatContext JSON, validates it with Pydantic, generates the plan, and outputs only the plan JSON or a safe metadata summary. No raw context is echoed.

P06: **No existing functionality broken.** The changes are additive: one new service file, one new CLI command, and one handoff section.

## Non-blocking Issues

N01: **Draft templates are hardcoded and only coarsely relationship-aware.** `_draft_templates` returns fixed Chinese text strings selected by `relationship_type` with only minor wording differences between types (e.g., "接住你这条消息" vs "记下这个点"). The three candidates represent structurally distinct approaches (pure acknowledgment, optional follow-up, paced next-step), which satisfies the "not minor paraphrases" requirement. However, the drafts do not incorporate `ApprovedContactSkillBrief.relationship_summary`, `ApprovedContactSkillBrief.strategy_hints`, or `ApprovedMemoryFactBrief.claim` text, which are the primary relationship-aware content that T123 was designed to supply.

**Why this is non-blocking:** The task does not require LLM calls. The worker explicitly states "T131 is heuristic and deterministic; it proves the safe planning surface and contract wiring, but not yet the final quality ceiling." T132 (boundary/policy validation) and T133 (holdout evaluation) are designed to assess and improve candidate quality. The current template approach establishes the correct wiring and safety boundary that later tasks can build on.

N02: **Confidence values are arbitrary hardcodes.** Values 0.78/0.71/0.66 (with approved refs) and 0.68/0.63/0.58 (without) communicate precision not supported by evidence. No relationship quality, context richness, or evidence strength metric informs these numbers.

**Why this is non-blocking:** The task schema marks `confidence` as optional. The values correctly decrease across the three candidates and drop when approved context is thin. T132/T133 can introduce evidence-weighted confidence.

N03: **`strategy_hints` and `relationship_summary` from approved contact skill are not used in draft generation.** `ApprovedContactSkillBrief` provides `strategy_hints` and `relationship_summary` fields specifically for runtime use, but `_build_candidates` reads only `relationship_type` from the skill and `boundary_reminders` for shared boundaries.

**Why this is non-blocking:** The wiring for consuming these fields exists (the planner reads `contact_skill` from the context). Adding their use is a targeted enhancement that T132 or a subsequent improvement can introduce without structural changes.

N04: **No committed test or fixture.** Verification was performed with an inline synthetic context only. No test file or fixture was committed.

**Why this is non-blocking:** T150 is explicitly tasked with building automated tests. The inline verification was honestly reported and is sufficient for contract-wiring validation at this stage.

N05: **`_dedupe` lacks type annotation on `values` parameter.** `def _dedupe(values)` accepts any iterable without a type hint. Minor style issue; no correctness risk.

N06: **`relationship_type` fallback to "unknown" may not cover all `ContactRelationshipType` enum values.** If the enum is extended beyond friend/classmate/family/colleague/unknown, new types would silently fall into the "unknown" template set. Low risk for MVP.

## Missing Tests

No committed automated tests. This is expected per task scope and tracked for T150. Inline synthetic verification was performed and reported.

## Suspicious Implementation Details

None found. The implementation is straightforward and honest about its limitations.

## Verdict

**PASS_WITH_WARNINGS**

The task is complete within its stated scope. The ReplyPlanner service and CLI correctly wire T123 compact approved-store context into T130 ReplyPlan output with proper safety checks (contact alignment, unique ranking, safe summary, no raw transcript). The three candidates are structurally distinct. No forbidden scope is violated.

The main limitation is that candidate drafts are generic hardcoded templates selected only by coarse `relationship_type`, without using `strategy_hints`, `relationship_summary`, or memory fact claims. This makes the planner's "relationship-awareness" shallow but structurally correct. The limitation is honestly stated in the handoff and is an appropriate target for T132/T133 quality improvement.

## Warning Disposition (Captain action required)

- N01: **accepted/deferred** — shallow relationship-awareness acknowledged; T132/T133 should evaluate whether `strategy_hints` and `relationship_summary` can be integrated into draft generation (potentially via LLM-assisted drafting in a later milestone).
- N02: **accepted** — arbitrary confidence hardcodes are acceptable for contract-wiring MVP.
- N03: **accepted/deferred** — unused approved-skill fields are a targeted improvement opportunity for T132.
- N04: **deferred** — automated tests tracked for T150.
- N05: **accepted** — minor style issue.
- N06: **accepted** — enum coverage is sufficient for current MVP.
