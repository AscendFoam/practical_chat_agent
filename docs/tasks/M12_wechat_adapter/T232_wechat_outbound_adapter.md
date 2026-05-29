# Task T232: WeChat-Family Outbound Adapter

## Status

Blocked placeholder. Do not assign this task to a worker yet.

## Task ID

T232

## Current Decision

T230 produced `Gate M12 Conditional`, not live outbound authorization.

T232 must remain blocked until:

- T231 has selected and reviewed exactly one official WeChat-family inbound
  surface;
- T233 has defined and reviewed the local provider-constraint safety gate for
  that surface;
- Captain has reviewed the T231 result and updated governance docs;
- a later Captain task package defines provider-specific recipient mapping,
  service-window checks, credential prerequisites, and synthetic dry-run
  payload behavior;
- the user explicitly accepts the selected official surface's product mismatch
  with personal WeFlow chat contacts.

## Forbidden Until Rewritten

- No live WeChat, WeCom, Official Account, Mini Program, Feishu, or Tencent API
  calls.
- No credentials, tokens, tenant IDs, app IDs, OpenIDs, external user IDs,
  `open_kfid`, QR codes, cookies, or private recipients.
- No outbound delivery, retry, polling, callback registration, background job,
  scheduler, runtime loop, or CLI send path.
- No unofficial SDK vendoring, scan-login resurrection, personal-WeChat
  automation, or desktop automation.
- No memory, ContactSkill, RelationshipState, feedback-log, approved-store, or
  private-artifact mutation.

## Future Shape

When rewritten, T232 should likely be a dry-run official-surface outbound
adapter similar to T223 Feishu sandbox:

- consume only `OutboundMessageRequest` records where explicit human approval
  and `OutboundSendGate` make `is_sendable()` true;
- consume only requests allowed by the T233 WeCom Customer Service provider
  safety gate;
- require a reviewed explicit recipient map outside
  `OutboundMessagePayload.metadata`;
- enforce provider service-window and quota preconditions before preparing any
  payload;
- default to dry-run and injected fake transport only;
- record safe audit evidence without claiming production delivery.

## Reviewer Type

adversarial
