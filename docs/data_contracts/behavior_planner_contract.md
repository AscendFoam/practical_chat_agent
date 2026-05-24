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
