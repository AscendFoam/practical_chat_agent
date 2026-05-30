# WeCom Customer Service Safety Contract

Task: T233 WeCom Customer Service Provider Safety Gate

Status: worker draft for review

## Scope

This contract defines a deterministic local provider-constraint safety gate for
the WeCom Customer Service surface selected by M12. It runs after an
`OutboundMessageRequest` has explicit outbound human approval and an
`OutboundSendGate` result where `is_sendable()` is already true.

The committed surface is:

- `WeComCustomerServiceRecipient`
- `WeComCustomerServiceSafetyConfig`
- `WeComCustomerServiceSafetyContext`
- `WeComCustomerServiceSafetyDecision`
- `WeComCustomerServiceSafetyGate`

This gate returns provider eligibility only. It does not prepare a WeCom API
payload, call Tencent/WeCom APIs, load credentials, register callbacks, poll or
sync messages, schedule work, send messages, mutate requests, or update runtime
state.

## Official Docs Status

T233 did not refetch external documentation. It relies on the T230/T231
documented facts that were rechecked on 2026-05-28:

- WeCom Customer Service receive/sync message concepts exist.
- WeCom Customer Service send behavior has provider constraints including a
  customer-message-triggered service window and a 5-message window limit.
- Provider identifiers such as `open_kfid` and `external_userid` are platform
  data, not repo contact identity.

These facts remain drift-sensitive. Official Tencent/WeCom docs must be
rechecked before any live account, credential, callback, or API task.

## Inputs

`WeComCustomerServiceSafetyGate.evaluate()` accepts:

- a validated `OutboundMessageRequest`;
- or a stable mapping that validates to `OutboundMessageRequest`.

It requires a `WeComCustomerServiceSafetyContext` with:

- `now`
- `recipient_map`
- optional `existing_audit`

The recipient map is explicit local safety context keyed by repo `contact_id`.
It is not stored in `OutboundMessagePayload.metadata`.

## Recipient Record

`WeComCustomerServiceRecipient` records reviewed aliases and provider window
state:

- `contact_id`
- `recipient_alias`
- `open_kfid_alias`
- `external_user_alias`
- `service_window_expires_at`
- `messages_sent_in_window`
- `manual_send_allowed`

The fields named as aliases are safe audit labels only. They are not live
provider IDs and must not be treated as `open_kfid`, `external_userid`, OpenID,
UnionID, access tokens, secrets, callback tokens, or tenant identifiers.

## Config Shape

`WeComCustomerServiceSafetyConfig` defaults to:

- `surface="wecom_customer_service"`
- `manual_send_only=True`
- `proactive_send_disabled=True`
- `provider_kill_switch_enabled=False`
- `max_messages_per_window=5`

The config rejects `manual_send_only=False` and
`proactive_send_disabled=False`. The current mainline remains manual-send-only
and does not support proactive sends.

## Decision Shape

`WeComCustomerServiceSafetyDecision` returns:

- `safety_state`: `allowed` or `blocked`
- `reason_codes`
- `request_id`
- `contact_id`
- `user_id`
- `recipient_alias`
- `open_kfid_alias`
- `external_user_alias`
- `audit_notes`
- `provider_surface`

The decision is a new in-memory object. The input `OutboundMessageRequest` is
not mutated.

## Required Blocking Rules

The gate blocks when any of these rules fail:

- request is not already `OutboundMessageRequest.is_sendable()`;
- `channel_preference` is not `wechat`;
- config `surface` is not `wecom_customer_service`;
- no recipient map entry exists for `request.contact_id`;
- provider kill switch is enabled;
- recipient `manual_send_allowed` is false;
- `service_window_expires_at` is missing;
- `service_window_expires_at` is at or before `context.now`;
- `messages_sent_in_window >= max_messages_per_window`;
- payload metadata contains provider identity, credential, or recipient
  smuggling keys.

Current provider-smuggling keys are:

- `external_userid`
- `open_kfid`
- `open_id`
- `unionid`
- `access_token`
- `corpsecret`
- `encoding_aes_key`
- `callback_token`
- `wecom_external_userid`
- `wecom_open_kfid`

Non-sendable requests are blocked before provider checks. This keeps pending
approval or blocked send-gate requests from receiving provider eligibility
details.

## Allow Semantics

`allowed` means only:

- request sendability was already established by human approval plus
  `OutboundSendGate`;
- the request is channel-compatible with the WeCom Customer Service safety
  surface;
- an explicit recipient alias record exists;
- the local service-window and 5-message quota checks pass;
- the provider kill switch is clear;
- no provider identity or credential keys were smuggled through payload
  metadata.

`allowed` does not mean:

- message delivered;
- payload prepared;
- API compatibility proven;
- live account eligible;
- credentials available;
- callback server configured;
- recipient mapping valid against production provider data.

The decision audit records `provider_eligible_not_delivery` and
`provider_payload_not_prepared` on the allow path.

## Audit Notes

Caller-provided audit notes are preserved from context and from the optional
`existing_audit` argument. Gate notes are deterministic, flat strings such as:

- `request_validated`
- `request_sendable_verified`
- `wechat_channel_verified`
- `provider_surface_configured`
- `provider_kill_switch_clear`
- `provider_metadata_clear`
- `recipient_mapping_verified`
- `manual_send_allowed`
- `service_window_active`
- `message_window_quota_clear`
- `provider_safety_allowed`
- `provider_safety_blocked`

Audit notes never include provider credential values. Tests assert that
metadata-smuggled values are not copied into audit notes.

## Test Coverage

`tests/test_wecom_customer_service_safety_gate.py` covers:

- allowed path for a sendable request with active service window;
- pending approval and blocked send-gate requests blocking before provider
  checks;
- missing recipient mapping;
- non-`wechat` channel preferences;
- missing WeCom Customer Service surface config;
- config rejection for non-manual or proactive modes;
- missing and expired service windows;
- 5-message window limit;
- provider kill switch;
- `manual_send_allowed=False`;
- provider identity and credential metadata keys;
- mapping input parity with model input;
- input request non-mutation.

## What T233 Does Not Authorize

T233 does not authorize:

- WeCom outbound adapter implementation;
- WeCom payload preparation;
- live API calls;
- credential reads;
- callback registration;
- webhook routes;
- polling or sync loops;
- scheduler, retry, runtime, or CLI send paths;
- automatic sending;
- store or memory mutation;
- production WeCom compatibility claims.

## Future T232 Boundary

T232 remains blocked until T233 passes review and Captain rewrites the task
package. A future T232 may only be a dry-run outbound payload-preparation task
with synthetic fixtures, explicit reviewed recipient context, no credentials,
and no live delivery.

## Remaining Risks

- Official docs may drift before live work.
- Recipient aliases are not proven provider identities.
- Service-window and message-count values are supplied context, not live
  provider state.
- No credential, tenant, callback, encryption/decryption, failure-event, or
  production acknowledgement behavior is implemented.
- `channel_preference="wechat"` is still broad and only narrows to this safety
  surface through explicit T233 config.
