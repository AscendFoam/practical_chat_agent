# WeCom Customer Service Inbound Contract

Task: T231 WeCom Customer Service Inbound Contract Spike

Status: worker draft for review

## Scope

This contract defines a local, synthetic-only inbound normalizer for the WeCom
WeChat Customer Service surface. It is not a live WeChat adapter and does not
authorize callback servers, polling, sync loops, credential loading, platform
API calls, delivery, memory writes, or runtime wiring.

The implementation surface is:

- `WeComCustomerServiceInboundConnector`
- connector name: `wecom_customer_service`
- input: synthetic fixture payloads shaped like WeCom Customer Service message
  or event records
- output: one `InboundConnectorResult` containing one normalized
  `InboundEvent`

## Why WeCom Customer Service

T230 recommended `Gate M12 Conditional`: personal WeChat automation,
scan-login resurrection, desktop automation, realtime personal-account
send/receive, and unofficial SDK vendoring remain blocked. Captain selected
WeCom Customer Service for T231 because it is an official customer-service
surface with documented inbound/event concepts.

This surface is still not a generic personal WeChat friend-chat adapter and
does not map directly to WeFlow personal chat contacts. T231 therefore proves
only a local contract over redacted synthetic fixtures.

## Official Docs Rechecked

Official Tencent/WeCom docs were rechecked on 2026-05-28:

- WeCom Customer Service "Receive messages and events":
  <https://developer.work.weixin.qq.com/document/path/94670>
- WeCom Customer Service "Send messages":
  <https://developer.work.weixin.qq.com/document/path/94677>

Rechecked facts used by this contract:

- customer-service receive/sync message examples include `msg_list`, `msgid`,
  `open_kfid`, `external_userid`, `send_time`, `origin`, `servicer_userid`,
  `msgtype`, and text content under `text.content`;
- event examples include `event.event_type`, `event.open_kfid`, and
  `event.external_userid`;
- send-failure events include `fail_msgid` and `fail_type`;
- outbound customer-service sending has provider constraints such as a
  customer-message-triggered 48-hour window, a 5-message window limit, and
  failure-event semantics.

T231 does not implement outbound behavior. The outbound constraints are listed
only to preserve the boundary for later tasks.

## Synthetic Fixture Fields

The committed fixtures under
`tests/fixtures/wecom_customer_service_inbound/` contain only synthetic IDs:

- `agent_id`: local synthetic account label for the test fixture.
- `open_kfid`: synthetic customer-service account alias.
- `external_userid`: synthetic customer alias, never a real WeCom external user
  ID.
- `msgid`: synthetic provider message alias.
- `send_time`: synthetic Unix timestamp.
- `msgtype`: synthetic provider message type.
- `text.content`: synthetic text body.
- `event.event_type`: synthetic provider event type.
- `event.fail_msgid`: synthetic failed outbound message alias.
- `event.fail_type`: synthetic failure code copied as contract data.

No fixture contains real OpenIDs, external user IDs, tenant IDs, app IDs,
tokens, secrets, QR codes, private recipients, or private chat content.

## Payload Shapes

The connector accepts two local shapes.

Synthetic wrapper shape:

```json
{
  "_meta": {
    "connector_name": "wecom_customer_service",
    "synthetic": true
  },
  "agent_id": "wecom_kf_account_support",
  "msg_list": [
    {
      "msgid": "msg_alias_text_001",
      "open_kfid": "kf_alias_support",
      "external_userid": "customer_alias_001",
      "send_time": 1716883200,
      "msgtype": "text",
      "text": {
        "content": "Hello, I need help with my appointment."
      }
    }
  ]
}
```

Document-shaped event payload:

```json
{
  "agent_id": "wecom_kf_account_support",
  "event": {
    "event_type": "msg_send_fail",
    "open_kfid": "kf_alias_support",
    "external_userid": "customer_alias_001",
    "fail_msgid": "msg_alias_outbound_001",
    "fail_type": 4
  }
}
```

The current repository inbound abstraction returns one `InboundEvent` per
connector parse. If a future live sync response contains multiple messages, a
later task must define batching before adding polling or callback handling.

## Mapping To InboundEvent

For customer text messages:

| Provider field | `InboundEvent` field |
| --- | --- |
| synthetic `msgid`, `open_kfid`, `external_userid`, `msgtype` | deterministic hashed `event_id` |
| fixed WeCom surface | `platform=Platform.WECHAT` |
| message payload | `source_type=SourceType.CHAT_MESSAGE` |
| `open_kfid` + `external_userid` | `channel_id="wecom_cs:<open_kfid>:<external_userid>"` |
| fixed customer-service one-to-one scope | `channel_type=ChannelType.DM` |
| `open_kfid` | `account_id="wecom_kf:<open_kfid>"` |
| `external_userid` synthetic alias | `actor_id` |
| fixed inbound customer event | `direction=Direction.INBOUND` |
| `msgtype="text"` | `content_type=ContentType.TEXT` |
| non-text `msgtype` | `content_type=ContentType.SYSTEM` with unsupported-type text |
| `send_time` | `occurred_at` as aware UTC |
| `text.content` | `text` |
| source payload + contract metadata | `raw` |

For provider events, including send-failure events:

- `source_type=SourceType.SYSTEM_EVENT`
- `content_type=ContentType.SYSTEM`
- `text` is a short synthetic-safe event summary such as
  `WeCom Customer Service event: msg_send_fail; fail_type=4`

## Parser Behavior

`can_handle_payload(payload)` returns `true` when:

- `_meta.connector_name` or `connector_name` is `wecom_customer_service`;
- or the payload has a documented-like `msg_list` with `open_kfid`,
  `external_userid`, and `msgtype`;
- or the payload has a documented-like `event` with `event_type`,
  `open_kfid`, and `external_userid`.

`parse_inbound_payload(payload)`:

- returns `InboundConnectorResult` for valid synthetic message/event payloads;
- raises `ValueError("not a WeCom Customer Service inbound payload")` for
  personal-WeChat/desktop-like payloads;
- raises a deterministic `ValueError` listing missing required fields for
  malformed WeCom-shaped payloads;
- never infers repo `contact_id`, memory identity, outbound recipient mapping,
  or approved-store identity from provider IDs.

## Raw Payload Boundary

`InboundEvent.raw` contains:

- `contract.surface="wecom_customer_service"`
- `contract.payload_kind="message"` or `"event"`
- `contract.synthetic_only=true`
- `contract.official_docs_rechecked="2026-05-28"`
- the synthetic source payload

This raw block is acceptable only because T231 fixtures are synthetic. A future
live adapter must define redaction rules before storing real provider IDs,
message text, callback bodies, failure responses, or provider metadata.

## What T231 Does Not Authorize

T231 does not authorize:

- live callback routes;
- webhook servers;
- polling or `sync_msg` loops;
- background jobs or schedulers;
- platform API calls;
- credentials, tokens, callback Token, EncodingAESKey, OAuth, or tenant setup;
- signature verification or encryption/decryption with real secrets;
- `AppContainer` wiring or runtime ingestion hooks;
- outbound payload preparation, sending, retries, or delivery interpretation;
- memory, ContactSkill, RelationshipState, feedback-log, approved-store, or
  outbound gate mutation;
- private chat-history or private distilled artifact reads;
- personal WeChat automation, scan-login resurrection, desktop automation, or
  unofficial SDKs.

## Why T232 Remains Blocked

T232 live outbound remains blocked because T231 does not solve:

- account/tenant eligibility;
- credential handling;
- callback verification;
- encryption/decryption;
- service-window tracking;
- 5-message window enforcement;
- recipient mapping ownership;
- provider failure-event processing;
- delivery acknowledgement semantics.

A future outbound task may only start after Captain approves a provider-specific
recipient mapping and tenant prerequisite model.

## Remaining Risks

- Official documentation can change and must be rechecked before live work.
- Current fixtures model only a narrow subset of message/event fields.
- The connector parses one message per call; batching remains undefined.
- Synthetic `external_userid` aliases are not repo contacts.
- Non-text handling is conservative and does not download media or inspect
  provider attachments.
- Send-failure event handling is represented as inbound system evidence only;
  no outbound state is mutated.
