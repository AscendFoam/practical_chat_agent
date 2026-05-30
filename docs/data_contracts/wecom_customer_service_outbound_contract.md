# WeCom Customer Service Outbound Dry-Run Contract

Task: T232 WeCom Customer Service Dry-Run Outbound Adapter

Status: worker draft for review

## Scope

This contract defines a deterministic local dry-run payload preparation boundary
for the WeCom Customer Service surface selected by M12.

The committed surface is:

- `WeComCustomerServiceDryRunConfig`
- `WeComCustomerServiceDryRunResult`
- `WeComCustomerServiceDryRunOutboundAdapter`

The adapter runs only after both upstream gates are represented explicitly:

- `OutboundMessageRequest.is_sendable()` is true, proving explicit outbound
  human approval plus an allowed `OutboundSendGate`.
- A matching T233 `WeComCustomerServiceSafetyDecision` exists with
  `safety_state="allowed"`.

The adapter prepares an in-memory synthetic dry-run payload only. It does not
send, queue, retry, acknowledge, register callbacks, poll, sync, load
credentials, call APIs, or mutate stores.

## Official Docs Status

T232 did not refetch external documentation. It relies on T230/T231/T233
documented facts and treats them as drift-sensitive. Official Tencent/WeCom
docs must be rechecked before any live account, credential, callback, API,
provider payload compatibility, or delivery task.

## Inputs

`WeComCustomerServiceDryRunOutboundAdapter.prepare_dry_run()` accepts:

- a validated `OutboundMessageRequest`;
- or a stable mapping that validates to `OutboundMessageRequest`;
- a required explicit `WeComCustomerServiceSafetyDecision`;
- or a stable mapping convertible to `WeComCustomerServiceSafetyDecision`;
- optional `existing_audit`.

Direct `CandidateAction` inputs and candidate-shaped mappings are rejected.
Reviewed `CandidateAction` records remain evidence only and never satisfy
outbound adapter authorization.

## Config Shape

`WeComCustomerServiceDryRunConfig` defaults to:

- `provider_surface="wecom_customer_service"`
- `dry_run_only=True`

The config rejects `dry_run_only=False`. T232 has no live mode.

## Result Shape

`WeComCustomerServiceDryRunResult` returns:

- `delivery_status`
- `delivered=False`
- `request_id`
- `contact_id`
- `user_id`
- `provider_surface`
- `recipient_alias`
- `open_kfid_alias`
- `external_user_alias`
- `prepared_payload`
- `audit_notes`

Current statuses are:

- `wecom_dry_run_ready`
- `blocked_invalid_request`
- `blocked_candidate_action_input`
- `blocked_not_sendable`
- `blocked_channel_mismatch`
- `blocked_safety_missing`
- `blocked_safety_not_allowed`
- `blocked_safety_mismatch`
- `blocked_missing_safety_aliases`

No status means sent, accepted, queued, acknowledged, retried, failed by
provider, or delivered.

## Validation Rules

The adapter rejects:

- direct `CandidateAction` model inputs;
- candidate-shaped mappings;
- invalid request mappings;
- requests where `is_sendable()` is false;
- requests where `channel_preference` is not `wechat`;
- missing safety decisions;
- safety decisions where `safety_state!="allowed"`;
- safety decisions whose `provider_surface` is not `wecom_customer_service`;
- safety decisions whose `request_id`, `contact_id`, or `user_id` does not
  match the outbound request;
- safety decisions missing `recipient_alias`, `open_kfid_alias`, or
  `external_user_alias`;
- safety decisions whose audit does not include both
  `provider_eligible_not_delivery` and `provider_payload_not_prepared`.

The adapter does not reconstruct provider eligibility from raw recipient
context. It consumes only the explicit T233 decision.

## Dry-Run Payload Shape

The prepared payload is built only on the allow path:

```json
{
  "provider_surface": "wecom_customer_service",
  "dry_run": true,
  "request_id": "outreq_synthetic",
  "contact_id": "contact_synthetic",
  "user_id": "user_synthetic",
  "recipient_aliases": {
    "recipient_alias": "recipient_alias_synthetic",
    "open_kfid_alias": "kf_alias_synthetic",
    "external_user_alias": "external_user_alias_synthetic"
  },
  "message": {
    "msg_type": "text",
    "text": "Synthetic outbound draft for WeCom dry run."
  },
  "safe_summary": "A review-safe summary of the outbound draft.",
  "source": {
    "source_type": "human_authored",
    "source_candidate_action_id": null
  }
}
```

The payload includes:

- provider surface;
- dry-run marker;
- request/contact/user scope;
- recipient aliases only;
- approved draft text from `OutboundMessagePayload.draft_text`;
- optional safe summary;
- source audit context.

The payload does not include:

- arbitrary `OutboundMessagePayload.metadata`;
- credentials;
- real provider IDs;
- access tokens;
- corpsecret;
- callback Token;
- EncodingAESKey;
- endpoint URLs;
- tenant IDs;
- retry fields;
- transport fields;
- delivery responses;
- provider acknowledgement data.

## Audit Notes

The adapter preserves caller audit notes and T233 safety audit notes with
deduplication. Successful dry-run readiness records:

- `request_sendable_verified`
- `wecom_safety_decision_verified`
- `wecom_dry_run_payload_prepared`
- `wecom_dry_run_only`
- `no_provider_delivery`

Blocked paths record a `wecom_dry_run_blocked` audit note.

## Test Coverage

`tests/test_wecom_customer_service_outbound_adapter.py` covers:

- allowed sendable request plus matching allowed T233 decision;
- pending human approval and blocked send gate;
- missing safety decision;
- blocked T233 safety decision;
- mismatched safety decision request/contact/user identity;
- wrong safety provider surface;
- missing safety aliases;
- missing T233 boundary audit notes;
- non-`wechat` channel preferences;
- direct `CandidateAction` model input;
- candidate-shaped mapping;
- invalid request mapping;
- request and safety mapping parity;
- metadata not copied into prepared payload;
- input request and safety decision non-mutation;
- absence of `transport`, `send`, and `deliver` seams.

## What T232 Does Not Authorize

T232 does not authorize:

- live WeCom outbound delivery;
- real WeCom API payload compatibility claims;
- provider API calls;
- credential reads;
- callback routes;
- webhook routes;
- polling or sync loops;
- live or fake transport hooks;
- retries;
- acknowledgement or failure-event handling;
- scheduler/background/runtime/CLI send paths;
- automatic sending;
- memory, ContactSkill, RelationshipState, feedback, approved-store, inbound,
  outbound request, or safety-decision mutation;
- private artifact reads;
- production readiness claims.

## Remaining Risks

- T232 proves only local dry-run payload preparation, not live WeCom API
  compatibility.
- The payload shape is synthetic and review-safe; it is not an official API
  request contract.
- T233 safety decisions are local provider eligibility snapshots, not live
  provider state.
- Recipient aliases are not proven provider identifiers.
- Credentials, tenant eligibility, callback verification, encryption,
  provider failure events, acknowledgement semantics, retries, and production
  recipient mapping remain unresolved.
