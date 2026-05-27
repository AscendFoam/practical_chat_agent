# Outbound Send Gate Contract

Task: T220 OutboundMessageRequest Schema  
Status: worker draft for review

## Scope

T220 defines the first M11 outbound-send contract as a schema-only boundary.

The committed models are:

- `OutboundMessagePayload`
- `OutboundRequestHumanApproval`
- `OutboundRequestSendGate`
- `OutboundMessageRequest`

This task does not implement send-gate policy, fake adapters, Feishu adapters,
review cards, schedulers, runtime loops, or any real sending path.

## Relationship To M10 CandidateAction

`CandidateAction` remains a review-only behavior artifact from M10.

Its role in T220 is limited to evidence:

- `OutboundMessageRequest.source_type="candidate_action"` records that the
  request was derived from a reviewed proactive candidate
- `source_candidate_action_id` stores the candidate artifact id
- `source_context_refs` may carry review-safe supporting refs

This does **not** make the request sendable. `CandidateAction.status`,
`review_state`, and `is_runtime_visible()` are not outbound authorization.

`OutboundMessageRequest` exists specifically to prevent this confusion by
separating:

- review-only candidate evidence
- outbound draft intent
- later send-gate evaluation

## OutboundMessagePayload

`OutboundMessagePayload` is still draft-only data. It carries:

- required `draft_text`
- optional `safe_summary`
- review-safe `metadata`

The payload is intentionally not a platform adapter payload. It has no
connector object, no channel id, no scheduling field, and no delivery result.

Forbidden metadata keys include transport, scheduler, adapter, credential, and
raw/private-content fields such as:

- `send_at`
- `scheduled_at`
- `scheduler_id`
- `channel_id`
- `webhook_url`
- `adapter_payload`
- `platform_target`
- `access_token`
- `api_key`
- `app_secret`
- `raw_transcript`
- `chat_history`
- `private_messages`

## OutboundMessageRequest

`OutboundMessageRequest` is the top-level outbound-intent record.

Required fields:

- `request_id`
- `contact_id`
- `user_id`
- `source_type`
- `payload`

Optional but important evidence fields:

- `source_candidate_action_id`
- `source_context_refs`
- `risk_flags`

Channel selection is data only:

- `channel_preference` is a compact preference value such as `unspecified`,
  `feishu`, or `wechat`
- it is not a live adapter target
- the request has no `channel_id`, `platform_target`, or connector handle

Source-boundary rules:

- `source_type="candidate_action"` requires `source_candidate_action_id`
- `source_type="human_authored"` must not carry `source_candidate_action_id`

## Human Approval And Gate State

T220 makes human approval explicit and separate from candidate review.

`OutboundRequestHumanApproval` defaults to:

- `review_state="pending_human_approval"`
- `approved_by_human=false`

If the outbound request is later reviewed, it must record:

- `reviewer_id`
- `reviewed_at`

Approved requests must set `approved_by_human=true`. Rejected requests must
keep it `false`.

`OutboundRequestSendGate` defaults to:

- `gate_state="not_evaluated"`

If the gate is later evaluated, it must record:

- `evaluator_id`
- `evaluated_at`

T220 does not decide `allowed` or `blocked`; it only reserves the structure
for T221.

## Pre-T221 Lifecycle

Before T221 exists, the request lifecycle is intentionally inert:

1. A human-authored draft request or candidate-derived draft request is created.
2. `human_approval` stays pending by default.
3. `send_gate` stays not evaluated by default.
4. `is_sendable()` remains `false`.

The request only becomes sendable when both are true:

- outbound human approval is explicitly approved
- later send-gate evaluation is explicitly allowed

T220 provides the check, not the evaluation logic.

## Privacy And Execution Boundaries

The schema preserves the current compact-context rule:

- no raw transcript cache
- no private chat-history fields
- no adapter payload smuggling
- no scheduler or timer fields
- no credentials or platform tokens

The contract is synthetic-test-friendly and does not require any private input.

## What T220 Does Not Authorize

T220 does not authorize:

- message sending
- scheduling
- timers, reminders, background jobs, or automations
- Feishu, WeChat, webhook, email, browser, or desktop adapters
- runtime loops or CLI execution paths
- LLM/provider calls or external services
- mutation of `CandidateAction`, memory records, ContactSkill, relationship
  state, approved stores, or private artifacts
- treating reviewed `CandidateAction` artifacts as executable outbound requests
