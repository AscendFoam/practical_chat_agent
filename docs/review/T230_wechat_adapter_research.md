# T230 WeChat Adapter Research

Date: 2026-05-28

## Executive Decision

`Gate M12 Conditional`

M12 should not proceed as a generic "WeChat adapter" milestone. The only
defensible path is a narrow, official-platform adapter path for business or
customer-service surfaces, and even that should begin with synthetic contract
fixtures and no live calls.

Personal WeChat account automation, scan-login resurrection, realtime friend
chat ingestion, desktop automation, and unofficial SDK vendoring remain blocked.
The repository can keep researching official WeCom / Official Account / Mini
Program / WeChat Customer Service surfaces, but implementation should proceed
only after Captain rewrites T231/T232/T233 around one selected official surface,
tenant/app prerequisites, explicit recipient mapping, and the M11 send-gate
boundary.

## Scope Audited

Repository files and docs read:

- `README.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/tasks/M12_wechat_adapter/T230_wechat_adapter_research_spike.md`
- `docs/data_contracts/outbound_send_gate_contract.md`
- `src/practical_chat_agent/core/models.py` symbol locations for
  `OutboundMessageRequest`, `OutboundRequestHumanApproval`,
  `OutboundRequestSendGate`, `channel_preference`, and `is_sendable`
- `src/practical_chat_agent/services/outbound_send_gate.py` symbol locations
- `src/practical_chat_agent/services/feishu_review_card.py` symbol locations

External official docs consulted on 2026-05-28:

- WeCom "Send application message":
  <https://developer.work.weixin.qq.com/document/path/90236>
- WeCom "Receive messages and events":
  <https://developer.work.weixin.qq.com/document/path/90238>
- WeCom `access_token`:
  <https://developer.work.weixin.qq.com/document/path/91039>
- WeCom "WeChat Customer Service / send message":
  <https://developer.work.weixin.qq.com/document/path/94677>
- WeCom "WeChat Customer Service / receive messages and events":
  <https://developer.work.weixin.qq.com/document/path/94670>
- Official Account customer-service introduction:
  <https://developers.weixin.qq.com/doc/service/guide/product/kf/intro.html>
- Official Account `sendCustomMessage`:
  <https://developers.weixin.qq.com/doc/service/api/customer/message/api_sendcustommessage>
- Official Account ordinary message receiving:
  <https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html>
- Mini Program `sendCustomMessage`:
  <https://developers.weixin.qq.com/miniprogram/dev/server/API/kf-mgnt/kf-message/api_sendcustommessage.html>

No `private/chat_history/` files were read. No private chat content, real
recipient identifiers, credentials, QR codes, cookies, tenant IDs, app IDs,
OpenIDs, chat IDs, or personal account data were used.

## Option Matrix

| Candidate surface | Official/support status | Requirements and constraints | Fit with this repo | Recommendation |
| --- | --- | --- | --- | --- |
| Personal WeChat account friend chat | No official server API found in the audited WeChat-family developer docs for arbitrary personal-account friend message send/receive. Existing repo plan explicitly paused scan/login/realtime personal-account work. | Any practical route would likely require QR/session automation, desktop automation, unofficial SDKs, hooks, scraping, or private client state. Recipient identity and audit would be unstable and compliance risk is high. | Does not fit M11 boundaries. It would revive T01 and create automatic personal-account delivery risk. | Block. Do not implement T231/T232/T233 against personal WeChat. |
| WeCom internal app messages | Official. WeCom documents app messages, `access_token` via `corpid`/`corpsecret`, callbacks with URL/Token/EncodingAESKey, recipient fields such as `touser`, `toparty`, `totag`, and app `agentid`. It also documents rate constraints such as per-app person-times/day and per-member minute/hour limits. | Requires enterprise tenant, self-built app, secret handling, configured callbacks, member UserID mapping, IP/callback allowlists as applicable, app scope, rate-limit handling, and delivery-failure interpretation. | Technically compatible with `OutboundMessageRequest` and `OutboundSendGate`, but recipient mapping is enterprise-member identity, not personal WeChat contacts from WeFlow. | Conditional. Candidate for a future WeCom-only adapter, not a personal WeChat adapter. Start with synthetic payload contracts only. |
| WeCom "WeChat Customer Service" | Official. WeCom docs expose customer-service receive/sync behavior and `kf/send_msg` with `touser` external user ID plus `open_kfid`. Docs state customer messages are constrained by active customer-service state, a 48-hour window after customer message, and a 5-message limit for that window. | Requires verified/eligible enterprise setup, customer-service account, `open_kfid`, external user ID mapping, callback or sync token flow, failure-event handling, session-state checks, and customer-service policy compliance. API success is not final delivery; failure events must be observed. | Better than personal WeChat because it is official and has clear session gates, but it is customer-service, not friend chat. It could respect M11 if proactive sends are blocked and outbound is only response-window/manual-approved. | Conditional. Best official WeChat-family candidate if the product can be reframed as customer-service reply assistance. No live implementation until account setup and callback semantics are reviewed. |
| Official Account customer-service messages | Official. Official docs expose customer-service messaging through `POST /cgi-bin/message/custom/send` with `access_token`, `touser` OpenID, and a documented 48-hour service window after user interaction. The guide documents per-scenario message quotas such as user-message-triggered service replies. | Requires Official Account, verified service/account capabilities, app credentials, configured message callback URL, OpenID mapping, response-window tracking, quota tracking, encryption/signature handling, and review of template/customer-service policy. | Compatible only for Official Account subscribers and customer-service flows. It cannot address arbitrary personal WeChat contacts. | Conditional. Acceptable as a future official customer-service adapter after a narrowed task package; not a generic WeChat adapter. |
| Mini Program customer-service messages | Official. Mini Program docs expose the same customer-service message send endpoint and OpenID-based recipient identity for user/customer-service interactions. | Requires Mini Program app, app credentials, OpenID mapping, customer-service event context, 48-hour-style service window constraints, callback/event handling, and account configuration. | Fits only Mini Program customer-service flows. It is not suitable for WeFlow personal chat replay contacts. | Conditional/Defer. Useful only if the product scope includes Mini Program customer support. |
| Desktop automation / manual-copy workflow | Manual copy itself can be human-operated, but automation of desktop WeChat would be fragile and not an official API path. | True manual copy requires no credentials in this repo and no adapter. Desktop automation would require UI driving, session state, screenshots, or OCR and would violate T230 forbidden scope if implemented. | Manual handoff can preserve human approval because the repository only renders a draft. Automated desktop send does not fit. | Allow manual handoff as non-adapter UX only; block desktop automation. |
| Continue Feishu/manual handoff instead of WeChat | Already supported at local/sandbox/review-card level by M11. No production Feishu claim exists. | Requires continuing the current review-only/manual-send posture. | Strongest current fit. It avoids WeChat compliance uncertainty and preserves send-gate semantics. | Prefer as default until an official WeChat-family account surface is selected and reviewed. |

## Compatibility With Existing Architecture

### InboundEvent

Only official callback or polling/sync payloads should be considered as future
inbound sources. WeCom app callbacks require configured URL, Token, and
EncodingAESKey. Official Account and Mini Program callbacks push user messages
to a configured developer URL. WeCom WeChat Customer Service has its own
customer-service receive/sync model and event/failure callbacks.

A future T231 may map synthetic official callback examples to `InboundEvent`
only if it:

- uses synthetic fixtures with fake IDs and no private transcript text;
- validates signature/encryption fields as contract data, without real secrets;
- records provider event IDs or message IDs as evidence refs;
- keeps platform IDs out of memory facts unless explicitly redacted or aliased;
- does not create a live callback server, webhook route, polling loop, or API
  client in the first task.

### OutboundMessageRequest

All acceptable future outbound paths must start from `OutboundMessageRequest`.
`CandidateAction` review state remains evidence only and cannot authorize a
send. `channel_preference="wechat"` is currently too broad for production
adapter selection because it does not distinguish WeCom internal app, WeCom
Customer Service, Official Account, Mini Program, or manual handoff. A future
task should either keep adapter choice in explicit adapter config or introduce a
reviewed subchannel contract before any platform call.

`OutboundMessagePayload.metadata` must not carry OpenID, external_userid,
UserID, `open_kfid`, access tokens, app secrets, webhook URLs, raw transcripts,
or adapter payloads. Recipient mapping must live in explicit adapter
configuration or a reviewed recipient map, following the M11 Feishu boundary.

### OutboundSendGate

The existing gate remains necessary but not sufficient. It can enforce local
human approval, quiet hours, duplicate suppression, frequency limits, empty-text
blocking, self-echo checks, and kill-switch behavior. Official WeChat-family
surfaces add provider-specific constraints that must be layered after the M11
gate, including:

- service-window eligibility, especially customer-service 48-hour windows;
- per-user or per-app quotas;
- recipient type restrictions;
- account verification and app-scope requirements;
- delivery failure callbacks or final-delivery ambiguity;
- provider content restrictions.

Provider API success must not be treated as final delivery unless official
callback/ack semantics are implemented and audited.

### Explicit Recipient Mapping

Every candidate official path needs a different recipient identity:

- WeCom internal app: enterprise member `userid`, party, or tag identity.
- WeCom WeChat Customer Service: external customer ID plus `open_kfid`.
- Official Account / Mini Program: user OpenID for that app/account.
- Manual handoff: no stored platform recipient is required; the human selects
  the recipient outside the repository.

The repo's `contact_id` must map to exactly one reviewed provider recipient
record for the selected adapter. Mapping must not be inferred from raw WeFlow
chat history, `OutboundMessagePayload.metadata`, private files, or model output.

### Review Card / Manual Approval

T224 review-card intent parsing is inert. Future WeChat-family work must not
reuse parsed card intent as applied approval or delivery authorization. A later
approval-application task would need to be explicit and reviewed before any
adapter can consume it.

For now, the safest user workflow is:

1. generate a review-only draft;
2. obtain explicit outbound human approval;
3. run `OutboundSendGate`;
4. for WeChat-family surfaces, either stop at a manual handoff artifact or run a
   synthetic adapter contract test;
5. require a separate future task before live delivery.

### Audit

A future adapter result should record only review-safe audit facts:

- request ID, contact ID, user ID, selected official surface, adapter name;
- provider-safe recipient alias, not raw OpenID/external_userid/UserID;
- gate state and provider constraint checks;
- prepared text preview, not raw transcript;
- provider message ID only when policy permits storing it;
- failure reason and retry guidance, without secrets or response bodies that may
  contain private data.

No hidden memory writes, feedback-log writes, ContactSkill updates, or private
artifact mutations should occur as side effects of inbound or outbound adapter
work.

## Rejected Paths

- Unofficial personal WeChat SDK vendoring: rejected. It would reintroduce
  unsupported client behavior and third-party code risk.
- Scan-login resurrection: rejected. T01 remains blocked, and the current
  mainline explicitly moved away from QR/session validation.
- Realtime personal-account automation: rejected. No official audited API path
  supports arbitrary friend chat send/receive for this repo's purposes.
- Desktop WeChat UI automation: rejected as an adapter path. Manual copy by a
  human is acceptable only because it is outside repo execution.
- Automatic proactive sending: rejected. M11 remains manual-only and
  human-approval-gated.
- Hidden memory, feedback, or ContactSkill writes from adapter events:
  rejected. Adapter work must not mutate stores unless a later task explicitly
  authorizes it.
- Treating provider "accepted" responses as final delivery: rejected unless
  official delivery/failure callback semantics are implemented and reviewed.
- Treating Feishu review-card intent parsing as approval application or delivery
  authorization: rejected.

## Recommended Next Task

T231 should not proceed as a broad "WeChat inbound adapter."

Recommended rewrite:

`T231_official_wechat_family_inbound_contract_spike`

Safe scope:

- choose exactly one official surface before implementation, preferably WeCom
  WeChat Customer Service if the product is customer-service-oriented, or WeCom
  internal app if the target is enterprise-member chat;
- create synthetic, redacted callback/event fixtures from official docs only;
- define a pure normalizer contract from those fixtures to `InboundEvent`;
- no live callback server, no API calls, no token validation using real secrets,
  no polling loop, no account login, no QR scanning, no desktop automation, no
  private chat reads, and no store mutation;
- document which provider fields are identity, event ID, message type, text
  payload, timestamp, delivery/failure state, and audit refs;
- keep outbound T232 blocked until T231 identifies a verified official surface
  and recipient mapping model.

T232 should remain blocked for live outbound delivery. It may later be narrowed
to a dry-run official-surface adapter, similar to T223 Feishu sandbox, but only
after T231 selects the surface and Captain approves credential/tenant
preconditions.

T233 should be rewritten as a safety-mode and provider-constraint design task:
provider window checks, quota checks, manual-send-only defaults, recipient-map
ownership, audit redaction, and kill-switch behavior. It should not implement
delivery.

## Risks And Open Questions

- Compliance risk: this research used official docs but did not perform legal
  or Tencent policy review. Personal WeChat automation remains especially risky.
- Account eligibility: Official Account, Mini Program, WeCom internal app, and
  WeCom Customer Service require real account/tenant/app setup that was not
  available in this task.
- Credential flow: `corpsecret`, app secrets, `access_token`, callback Token,
  and EncodingAESKey handling were not implemented or tested.
- Recipient mapping: no reviewed mapping exists from repo `contact_id` to WeCom
  UserID, external_userid, OpenID, or `open_kfid`.
- Callback verification: no live callback URL, signature verification,
  encryption/decryption, replay defense, or retry behavior was tested.
- Service windows: customer-service windows and quotas must be represented as
  adapter constraints before any outbound call.
- Delivery semantics: official docs distinguish API acceptance from final
  delivery in at least the WeCom Customer Service path; future adapters need
  failure-event handling before claiming delivery.
- Product mismatch: WeFlow personal chat history does not naturally map to
  Official Account / Mini Program / WeCom Customer Service identities.
- Current documentation drift: external facts were retrieved on 2026-05-28 and
  should be rechecked before any implementation task that touches credentials or
  platform APIs.
