# Outbound Send Gate Contract

Task: T220 OutboundMessageRequest Schema + T221 OutboundSendGate + T222 Local Fake Adapter + T223 Feishu Sandbox Adapter + T224 Feishu Review Card
Status: worker draft for review

## Scope

M11 starts in five explicit layers:

- T220: inert outbound request contract
- T221: deterministic gate decision over that contract
- T222: local fake adapter simulation after the gate
- T223: Feishu-specific sandbox payload/result boundary
- T224: review-card rendering and inert review-intent parsing

The committed surfaces are:

- `OutboundMessagePayload`
- `OutboundRequestHumanApproval`
- `OutboundRequestSendGate`
- `OutboundMessageRequest`
- `OutboundSendGateConfig`
- `OutboundSendGateContext`
- `OutboundSendGateDecision`
- `OutboundSendGate`
- `FakeOutboundAdapterConfig`
- `FakeOutboundDeliveryResult`
- `LocalFakeOutboundAdapter`
- `FeishuSandboxRecipient`
- `FeishuSandboxAdapterConfig`
- `FeishuSandboxTransportResponse`
- `FeishuSandboxDeliveryResult`
- `FeishuSandboxOutboundAdapter`
- `FeishuReviewCardConfig`
- `FeishuReviewIntent`
- `FeishuReviewCardRenderResult`
- `FeishuReviewIntentParseResult`
- `FeishuReviewCardBuilder`
- `FeishuReviewIntentParser`

This contract still does not include delivery, adapters, schedulers, CLI send
commands, runtime loops, or external services. T222 adds only a local fake
adapter simulation layer, and T223 adds only a Feishu sandbox adapter boundary,
not a production platform adapter. T224 adds only a presentation and inert
review-intent layer, not approval application or delivery.

## Relationship To M10 CandidateAction

`CandidateAction` remains a review-only behavior artifact from M10.

Its role in M11 is evidence only:

- `OutboundMessageRequest.source_type="candidate_action"` records evidence origin
- `source_candidate_action_id` stores the candidate artifact id
- `source_context_refs` carry review-safe supporting refs

This does **not** make a request sendable. The following still are not outbound
authorization:

- `CandidateAction.status="approved"`
- `review_state="reviewed"`
- `CandidateAction.is_runtime_visible()`

T221 evaluates only `OutboundMessageRequest.human_approval`,
`OutboundMessageRequest.send_gate`, payload text, supplied history, and
supplied gate context.

T222 still does not treat reviewed `CandidateAction` artifacts as send or
adapter authorization. Direct `CandidateAction` inputs are rejected at the fake
adapter boundary.

T223 keeps the same rule. Reviewed `CandidateAction` artifacts may inform
evidence origin only; they never satisfy Feishu adapter authorization by
themselves.

T224 also keeps the same rule. Review cards may display candidate-derived
evidence references carried through `OutboundMessageRequest`, but card rendering
and action parsing do not turn those artifacts into approval or delivery
authorization.

## OutboundMessageRequest Layer

`OutboundMessageRequest` stays the top-level outbound-intent record.

Key fields:

- `request_id`
- `contact_id`
- `user_id`
- `source_type`
- `source_candidate_action_id`
- `source_context_refs`
- `payload`
- `channel_preference`
- `risk_flags`
- `human_approval`
- `send_gate`
- `created_at`
- `updated_at`

`channel_preference` is data only:

- valid values are `unspecified`, `feishu`, and `wechat`
- it is not a live adapter target
- there is no connector handle, platform client, or delivery object

`human_approval` and `send_gate` are separate:

- `human_approval` records explicit outbound approval status
- `send_gate` records explicit gate evaluation status

## OutboundMessagePayload Boundary

`OutboundMessagePayload` carries draft-only outbound text plus optional safe
summary and review-safe metadata.

Forbidden metadata keys include the full outbound-specific superset:

- `send_at`
- `scheduled_at`
- `scheduler_id`
- `schedule_id`
- `timer_id`
- `reminder_id`
- `platform`
- `channel_id`
- `webhook_url`
- `recipient_address`
- `adapter_payload`
- `adapter_config`
- `platform_target`
- `platform_token`
- `bot_token`
- `app_secret`
- `open_id`
- `chat_id`
- `receive_id`
- `receive_id_type`
- `feishu_open_id`
- `feishu_chat_id`
- `delivery_connector_name`
- `delivery_response`
- `send_result`
- `access_token`
- `api_key`
- `raw_transcript`
- `chat_history`
- `private_messages`

The payload is intentionally not an adapter payload and not a scheduler job.

## T221 Gate Inputs

`OutboundSendGate.evaluate()` accepts:

- a validated `OutboundMessageRequest`
- or a stable mapping that validates to `OutboundMessageRequest`

Optional evaluation inputs:

- `now`
- `recent_requests`
- `context`
- `existing_audit`

`recent_requests` are explicit in-memory synthetic/local request snapshots.
T221 does not require a repository, database, queue, or scheduler.

`OutboundSendGateContext` is review-safe only and may provide:

- `latest_inbound_text`
- `latest_user_text`
- `self_echo_reference_texts`

## T221 Config Shape

`OutboundSendGateConfig` controls deterministic policy evaluation:

- `evaluator_id`
- `manual_only_mode`
- `kill_switch_enabled`
- `quiet_hours_start`
- `quiet_hours_end`
- `timezone_name`
- `frequency_limit_count`
- `frequency_limit_window_seconds`
- `duplicate_window_seconds`

Current mainline is manual-only. T221 keeps `manual_only_mode=True` and does
not provide a non-human-approved send path.

## T221 Decision Shape

`OutboundSendGateDecision` returns:

- `evaluated_request`
- `allowed`
- `blocked_reasons`
- `passed_checks`
- `gate_notes`

The returned request is a new audited copy. The input request is not mutated in
place.

## Gate Lifecycle

Pre-gate request lifecycle:

1. request exists
2. outbound human approval may be pending, approved, or rejected
3. `send_gate.gate_state` is usually `not_evaluated`
4. request is not sendable by default

T221 evaluation lifecycle:

1. evaluate request against deterministic local policy
2. create a new `OutboundRequestSendGate`
3. set:
   - `gate_state="allowed"` when all checks pass
   - `gate_state="blocked"` when any blocking rule fails
4. record:
   - `evaluator_id`
   - `evaluated_at`
   - `gate_notes`
5. return `OutboundSendGateDecision`

Only after both are true can `OutboundMessageRequest.is_sendable()` return
`true`:

- `human_approval.review_state=="approved"` and `approved_by_human==true`
- `send_gate.gate_state=="allowed"`

## Allowed Vs Blocked Semantics

`allowed` means:

- policy checks passed
- the request is eligible for a later adapter task to consider
- the gate state is auditable

`allowed` does **not** mean:

- message delivered
- adapter selected
- fake adapter executed
- Feishu sandbox payload prepared
- Feishu or WeChat API called
- scheduler created
- background job queued

`blocked` means:

- at least one deterministic policy rule failed
- the gate records why
- no delivery side effect occurs

## T222 Fake Adapter Inputs

`LocalFakeOutboundAdapter.deliver()` accepts:

- a validated `OutboundMessageRequest`
- or a stable mapping that validates to `OutboundMessageRequest`

The fake adapter rejects:

- any request where `request.is_sendable()` is `false`
- any request whose outbound human approval is not explicitly approved
- any request whose `send_gate.gate_state` is not `allowed`
- direct `CandidateAction` instances
- mappings that represent `CandidateAction` records
- invalid mappings that do not validate to `OutboundMessageRequest`

`OutboundMessageRequest.is_sendable()` is the adapter boundary. T222 does not
bypass that check and does not infer sendability from prior review artifacts.

## T222 Fake Delivery Result Shape

`FakeOutboundDeliveryResult` returns:

- `adapter_name`
- `delivery_status`
- `delivered`
- `request_id`
- `contact_id`
- `user_id`
- `channel_preference`
- `delivered_at`
- `payload_preview`
- `audit_notes`

Current local statuses are:

- `fake_delivered`
- `blocked_not_sendable`
- `blocked_invalid_request`

`payload_preview` is intentionally truncated review-safe text. T222 does not
persist full raw transcript fields, adapter payload blobs, or delivery
responses.

## T222 Fake Adapter Lifecycle

T222 fake-adapter lifecycle:

1. accept an outbound request or stable mapping
2. reject direct `CandidateAction` input
3. validate request shape locally
4. require `request.is_sendable()==true`
5. return a deterministic in-memory `FakeOutboundDeliveryResult`
6. record local audit notes that distinguish fake simulation from real delivery

The adapter returns a new result object only. It does not mutate the input
request, create a scheduler job, or write to a platform.

## Gate `allowed` Vs Fake `fake_delivered` Vs Real Delivery

These states are deliberately different:

- gate `allowed`: deterministic policy eligibility only
- fake `fake_delivered`: local synthetic adapter simulation only
- real delivery: out of scope for T222 and still not implemented here

T222 proves only that a gate-approved request can cross a safe local adapter
boundary. It does not prove Feishu, WeChat, webhook, email, browser, desktop,
notification, or runtime delivery.

## T223 Feishu Sandbox Adapter Inputs

`FeishuSandboxOutboundAdapter.deliver()` accepts:

- a validated `OutboundMessageRequest`
- or a stable mapping that validates to `OutboundMessageRequest`

The adapter rejects:

- any request where `request.is_sendable()` is `false`
- direct `CandidateAction` instances
- candidate-shaped mappings
- invalid mappings that do not validate to `OutboundMessageRequest`
- requests whose `channel_preference` is not explicitly `feishu`
- requests without an explicit sandbox recipient mapping outside payload
  metadata

T223 chooses the conservative channel rule:

- `channel_preference="feishu"` is required
- `channel_preference="unspecified"` is not auto-mapped
- `channel_preference="wechat"` is blocked

## T223 Feishu Sandbox Config Shape

`FeishuSandboxAdapterConfig` controls the sandbox adapter boundary:

- `adapter_name`
- `dry_run_by_default`
- `recipient_map`

`recipient_map` is explicit adapter configuration keyed by `contact_id`. It is
not stored inside `OutboundMessagePayload.metadata`.

Each `FeishuSandboxRecipient` records:

- `recipient_type`
- `recipient_id`

Current synthetic recipient types are:

- `open_id`
- `chat_id`

## T223 Feishu Sandbox Result Shape

`FeishuSandboxDeliveryResult` returns:

- `adapter_name`
- `delivery_status`
- `delivered`
- `request_id`
- `contact_id`
- `user_id`
- `channel_preference`
- `recipient_type`
- `recipient_id`
- `prepared_payload`
- `provider_message_id`
- `result_at`
- `audit_notes`

Current statuses are:

- `feishu_dry_run_ready`
- `feishu_sandbox_sent`
- `blocked_not_sendable`
- `blocked_invalid_request`
- `blocked_missing_recipient`
- `blocked_wrong_channel`
- `blocked_transport_error`
- `blocked_transport_unavailable`

`result_at` is normalized to aware UTC.

## T223 Feishu Sandbox Lifecycle

T223 sandbox lifecycle:

1. accept an outbound request or stable mapping
2. reject candidate input and non-sendable requests
3. require `channel_preference=="feishu"`
4. resolve explicit sandbox recipient mapping by `contact_id`
5. build a Feishu-compatible text payload from `request.payload.draft_text`
   only
6. return dry-run payload readiness by default
7. optionally call an injected fake/sandbox transport when dry-run is disabled

The adapter does not mutate the input request, does not read secrets from the
environment, and does not create scheduler/runtime side effects.

## Gate `allowed` Vs Fake `fake_delivered` Vs Feishu Sandbox Vs Real Delivery

These states remain distinct:

- gate `allowed`: deterministic policy eligibility only
- fake `fake_delivered`: local synthetic adapter simulation only
- Feishu `feishu_dry_run_ready`: Feishu sandbox payload prepared only
- Feishu `feishu_sandbox_sent`: injected fake/sandbox transport succeeded only
- real production delivery: still out of scope and unclaimed

T223 proves only that a gate-approved request can be transformed into a
Feishu-compatible sandbox payload and optionally passed to an injected fake
transport. It does not claim production Feishu delivery.

## T224 Feishu Review Card Inputs

`FeishuReviewCardBuilder.render()` accepts:

- a validated `OutboundMessageRequest`
- or a stable mapping that validates to `OutboundMessageRequest`
- an optional `FeishuSandboxDeliveryResult` summary

The builder rejects:

- direct `CandidateAction` instances
- candidate-shaped mappings
- invalid mappings that do not validate to `OutboundMessageRequest`

Unlike T222/T223 adapters, T224 may render both sendable and non-sendable
requests. Review presentation does not imply sendability or delivery.

## T224 Feishu Review Card Payload Shape

`FeishuReviewCardRenderResult` returns:

- `renderer_name`
- `render_status`
- `rendered`
- `request_id`
- `contact_id`
- `user_id`
- `channel_preference`
- `sendable`
- `card_payload`
- `audit_notes`

Current render statuses are:

- `card_rendered`
- `blocked_invalid_request`

The local Feishu-compatible card payload includes review-safe sections for:

- request identity
- approval state
- gate state
- sendability
- risk flags
- gate audit notes
- draft preview
- optional sandbox result summary
- inert review-intent buttons

Draft truncation is display-only. It is not claimed as redaction.

## T224 Review Intent Action Values

Each rendered button value encodes inert review-intent data with:

- `schema_version`
- `request_id`
- `action`

Current actions are:

- `approve`
- `request_edit`
- `reject`
- `boundary_feedback`

These values are presentation intent only. T224 does not apply the decision.

## T224 Review Intent Parser

`FeishuReviewIntentParser.parse()` accepts a synthetic Feishu card-action
mapping and returns `FeishuReviewIntentParseResult`.

Successful parses return:

- `parse_status="intent_parsed"`
- `accepted=true`
- a validated `FeishuReviewIntent`

Rejected parses return:

- `parse_status="blocked_invalid_action"`
- `accepted=false`
- `intent=null`

The parser rejects:

- malformed or missing action-value mappings
- missing schema version
- missing request id
- unknown action values
- cross-request payloads when an expected request id is supplied

Parsing yields inert intent data only. It does not mutate request approval,
re-run the gate, call adapters, send messages, or write feedback/memory.

## Gate Vs Fake Vs Sandbox Vs Card Vs Parsed Intent

These states remain distinct:

- gate `allowed`: deterministic policy eligibility only
- fake `fake_delivered`: local synthetic adapter simulation only
- Feishu `feishu_dry_run_ready` / `feishu_sandbox_sent`: sandbox evidence only
- review card `card_rendered`: human-review presentation only
- parsed review intent `intent_parsed`: inert user intent only, not applied
  approval or delivery

T224 adds visibility and synthetic interaction data only. It does not apply or
persist review outcomes.

## Audit Note Conventions

T221 keeps gate notes deterministic and flat. Typical note families are:

- pass notes such as:
  - `manual_only_mode_enabled`
  - `human_approval_approved`
  - `kill_switch_disabled`
  - `quiet_hours_clear`
  - `frequency_limit_clear`
  - `duplicate_check_clear`
  - `self_echo_clear`
  - `payload_text_present`
- blocking notes such as:
  - `human_approval_pending`
  - `human_approval_rejected`
  - `kill_switch_enabled`
  - `quiet_hours_blocked`
  - `frequency_limit_exceeded`
  - `duplicate_suppressed`
  - `self_echo_prevention`
  - `empty_draft_text`
- final state note:
  - `gate_allowed`
  - `gate_blocked`

These are policy/audit notes only.

## Policy Rules

T221 implements these blocking rules:

1. Manual-only approval
   - blocks pending or rejected outbound approval
   - reviewed `CandidateAction` evidence is irrelevant to this check
2. Kill switch
   - blocks all requests when enabled
3. Quiet hours
   - blocks requests inside the configured local HH:MM window
   - supports overnight windows such as `23:00` to `08:00`
4. Frequency limit
   - blocks excess same-scope requests using supplied recent request history
   - T221 treats prior gate-`allowed` requests as send-equivalent history
5. Duplicate suppression
   - blocks same normalized draft text for the same contact, user, and channel
     preference within the duplicate window
6. Self-echo prevention
   - blocks text identical to supplied latest inbound/user text or explicit
     self-echo reference text
7. Defensive empty-text rejection
   - blocks whitespace-only draft text even if schema `min_length` passed

## Scope Matching Rules

For frequency and duplicate checks, the current T221 scope is:

- same `contact_id`
- same `user_id`
- same `channel_preference`

This remains local deterministic policy, not platform addressing.

## Privacy And Execution Boundaries

T221 preserves the compact-context rule:

- no raw transcript reads
- no private chat-history fields
- no adapter payload smuggling
- no scheduler or timer objects
- no credentials or platform tokens
- no repository or database dependency
- no external platform or runtime delivery side effect
- no production Feishu credential or webhook flow
- no recipient mapping smuggled through outbound payload metadata

All tests and examples must stay synthetic.

## What T224 Still Does Not Authorize

T224 does not authorize:

- message sending
- scheduling
- reminders, timers, background jobs, or automations
- production Feishu adapter execution
- approval, edit, reject, or boundary-feedback application
- feedback-log writes or memory writes
- WeChat adapter execution
- webhook, email, browser, desktop, or notification delivery
- CLI send commands or runtime loops
- real delivery completion
- platform API calls, connector handles, or delivery credentials
- webhook registration, event callbacks, or bot installation flows
- mutation of `CandidateAction`, memory records, ContactSkill, relationship
  state, approved stores, or private artifacts
- treating gate `allowed`, fake `fake_delivered`, `feishu_dry_run_ready`, or
  `feishu_sandbox_sent`, `card_rendered`, or `intent_parsed` as production
  delivery or applied approval completion
