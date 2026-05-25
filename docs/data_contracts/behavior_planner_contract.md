# Behavior Planner Contract

Task: T210 Behavior Schema  
Status: worker draft for review

## Scope

M10 opens with data contracts only. These models describe reviewable proactive
behavior candidates, but they do not plan, rank, schedule, send, execute,
integrate with a platform, mutate memory, or write private artifacts.

The committed schemas are:

- `AgentSelfState`
- `BehaviorPolicy`
- `CandidateActionPayload`
- `CandidateAction`

## AgentSelfState

`AgentSelfState` is a compact review-safe state snapshot for future behavior
drafting. It carries only identifiers, safe summaries, artifact references, and
risk labels.

Required fields:

- `agent_id`
- `user_id`

Optional fields:

- `contact_id`
- `availability_state`
- `current_focus`
- `approved_context_refs`
- `recent_signal_refs`
- `risk_flags`

Privacy boundary:

- It must not be treated as a raw transcript cache.
- It has no `raw_text`, `transcript`, `chat_history`, or `private_messages`
  field.
- References should point to approved/review-safe artifacts rather than raw
  chat records.

## BehaviorPolicy

`BehaviorPolicy` is the explicit safety envelope for future behavior
candidates.

Default invariants:

- `policy_mode` is `draft_only_review_required`.
- `human_review_required` is always `true`.
- `auto_send_allowed` is always `false`.
- `platform_execution_allowed` is always `false`.
- `scheduler_allowed` is always `false`.

Allowed draft-only action types:

- `relationship_check_in_draft`
- `reply_follow_up_draft`
- `topic_suggestion`
- `boundary_review_note`
- `memory_review_prompt`
- `do_nothing`

These categories are not executable actions. They are reviewable suggestions or
notes for a human user.

`CandidateAction.action_type` must be included in the attached
`BehaviorPolicy.allowed_action_types`; mismatches are rejected by schema
validation.

Forbidden payload fields include:

- transport or execution keys such as `platform`, `channel_id`,
  `webhook_url`, and `recipient_address`
- scheduling keys such as `send_at` and `scheduled_at`
- private/raw content keys such as `raw_transcript`, `chat_history`, and
  `private_messages`
- credential keys such as `access_token` and `api_key`

## CandidateActionPayload

`CandidateActionPayload` is a non-executable payload shape. It supports:

- `safe_summary`
- optional `draft_text`
- `review_notes`
- `metadata`

`safe_summary` is required. `draft_text` is optional so a candidate can be a
review note or `do_nothing` recommendation without carrying message text.

`metadata` rejects forbidden transport, scheduling, credential, and raw
transcript keys.

## CandidateAction

`CandidateAction` is a review-only proactive behavior artifact.

Required fields:

- `contact_id`
- `user_id`
- `action_type`
- `title`
- `rationale`
- `supporting_context_refs`

Default invariants:

- `action_mode` is `draft_only_review_required`.
- `status` is `candidate`.
- `human_review_required` is always `true`.
- `auto_send_allowed` is always `false`.
- `platform_execution_allowed` is always `false`.
- `scheduler_allowed` is always `false`.
- `platform_target` is always `null`.

Lifecycle:

- `candidate`: draft artifact awaiting human review.
- `approved`: human-approved artifact that may be visible to later review-safe
  surfaces.
- `rejected`: reviewed artifact that should not be used.
- `frozen`: retained but not runtime-visible.
- `archived`: historical artifact only.

Runtime visibility is data-only and still non-executable. `is_runtime_visible()`
requires `status="approved"` plus human-reviewed approval metadata. Even then,
the artifact remains a draft/review surface and cannot send, schedule, or
execute.

## Evidence And References

Every `CandidateAction` requires at least one `supporting_context_ref`.
References use the existing `ReplyPlanContextRef` contract and should point to
approved/review-safe surfaces such as approved ContactSkill records, approved
memory fact records, memory hits, policy boundaries, or recent event ids that
are already safe for compact context use.

T210 does not reopen raw transcript ingestion.

## Relationship To OutboundSendGate

T210 deliberately stops before outbound work. Later milestones may define
`OutboundMessageRequest`, `OutboundSendGate`, and platform adapters, but this
contract does not authorize:

- automatic sending
- real scheduling
- background jobs
- Feishu, WeChat, email, notification, browser, or desktop integration
- memory, ContactSkill, relationship-state, or approved-store mutation
- LLM calls, embeddings, vector DBs, or external provider use

## T211 Rule Engine Scope

T211 adds `BehaviorRulePlanner`, a deterministic local service that proposes
zero or more `CandidateAction` records from:

- `AgentSelfState`
- optional `BehaviorPolicy`
- optional `safe_context_labels`

The public planner API does not accept raw transcript, chat history, private
message, or message text parameters.

## T211 Input Boundary

Accepted inputs are review-safe and compact:

- approved context refs from `AgentSelfState.approved_context_refs`
- recent safe signal refs from `AgentSelfState.recent_signal_refs`
- compact risk flags from `AgentSelfState.risk_flags`
- short caller-provided safe labels such as `memory_review` or
  `boundary_sensitive`

The planner does not read `private/chat_history/`, store files, platform
payloads, message transport fields, or raw conversation text.

## T211 Rule Semantics

Rules fire in this deterministic order:

1. `boundary_review_note`: fires for boundary-sensitive risk flags or safe
   labels.
2. `memory_review_prompt`: fires when recent safe signal refs exist or safe
   labels request memory/relationship review.
3. `relationship_check_in_draft`: fires only when at least one approved context
   ref exists and no hard proactive-blocking risk flag is present.
4. `do_nothing`: fallback when no other candidate is emitted and the policy
   allows it.

Hard proactive-blocking risk flags include `thin_context`,
`boundary_sensitive`, `boundary_risk`, `high_sensitivity`, `privacy_risk`, and
`blocked_proactive`.

`do_nothing` is the chosen fallback behavior for empty/thin context. If policy
does not allow `do_nothing` and no other allowed rule emits, the planner returns
an empty list.

## T211 Output Ordering And Limits

Ordering is rule-order deterministic. Candidate ids are stable hashes derived
from agent id, user id, contact id, action type, and supporting ref ids.

`BehaviorPolicy.allowed_action_types` is enforced before a candidate is
emitted. `BehaviorPolicy.max_candidates` is applied after rule filtering while
preserving order.

Every emitted candidate:

- validates as `CandidateAction`
- has at least one `supporting_context_ref`
- carries rule-specific rationale, risk flags, and review-safe
  `payload.safe_summary`
- keeps `human_review_required=true`
- keeps `auto_send_allowed=false`
- keeps `platform_execution_allowed=false`
- keeps `scheduler_allowed=false`
- keeps `platform_target=null`
- contains no forbidden payload metadata keys

## T211 Relationship To Later M10 Tasks

T211 does not generate final user-facing message drafts. T212 owns draft
generation. T213 owns CandidateAction review flow. T214 owns behavior safety
evaluation.

T211 does not authorize automatic sending, real scheduling, platform
integration, runtime loops, store mutation, LLM calls, or outbound gate bypass.

## T212 Draft Enrichment Scope

T212 enriches an existing safe `CandidateAction` with review-only draft text.
It does not change the candidate's action type, evidence refs, risk flags,
policy, or execution boundaries.

Accepted input shapes:

- a validated `CandidateAction`
- a stable candidate-action mapping that validates to `CandidateAction`

Output shape:

- the same `CandidateAction` with `payload.draft_text` populated
- all no-send / no-scheduler / no-platform invariants preserved

Draft safety constraints:

- keep text short, conservative, and clearly review-only
- do not echo raw transcript or private-text content
- do not add transport, scheduling, or platform semantics
- do not try to increase engagement or imitate a real person

Recommended draft families:

- `boundary_review_note`: boundary-sensitive review note
- `memory_review_prompt`: memory or relationship review reminder
- `relationship_check_in_draft`: low-pressure, non-committal check-in draft
- `do_nothing`: explicit review-safe no-action note

T212 remains the bridge between deterministic candidate proposal and the
later review surface. T213 should consume these enriched candidates in a
review CLI. T214 should evaluate the resulting behavior safety, not authorize
execution.

## T213 Review Scope

T213 adds an explicit human review layer for `CandidateAction` records.
It may change review status and review metadata, but it does not authorize
outbound execution or platform delivery.

Supported decisions:

- `approve`
- `reject`
- `freeze`
- `archive`

Review metadata semantics:

- `review_state` becomes `reviewed`
- `reviewed_by_human` becomes `true`
- `last_decision` mirrors the normalized decision status
- `last_reviewed_at` records the review timestamp
- `last_reviewer_id` stores the human reviewer id
- `history` appends a `DistilledArtifactReviewDecision`
- `decision_notes` appends the optional note when present

Approved is not sendable:

- `status="approved"` only means the candidate is visible to later
  review-safe surfaces
- it does not imply send authorization
- it does not imply scheduler, platform, or runtime execution approval

CLI safe-output expectations:

- print action id, contact id, action type, status, and review metadata only
- do not print full draft text or raw private content to stdout
- default or recommended file outputs should stay under `private/`

T213 precedes later OutboundSendGate milestones. Any later execution path must
still respect review-only candidate semantics and human-approved outbound
policy.
