# M12 WeChat Adapter Milestone Review

## Verdict

Gate recommendation: `Gate M12 Conditional`.

M12 is coherent and reviewable as a local, synthetic, dry-run-only adapter
slice. It proves a constrained chain:

- T230 narrowed unsafe WeChat-family surfaces and kept personal WeChat,
  scan-login, desktop automation, realtime personal-account send/receive, and
  unofficial SDKs blocked.
- T231 defined a synthetic-only WeCom Customer Service inbound normalization
  contract.
- T233 defined a local provider-safety eligibility decision after
  `OutboundMessageRequest.is_sendable()`.
- T232 defined local dry-run payload preparation that requires a matching
  allowed T233 safety decision.

M12 does not authorize live WeChat or WeCom delivery, credentials, callbacks,
webhooks, polling, sync loops, transport, retries, provider acknowledgement,
failure-event mutation, production recipient mapping, automatic sending,
personal-WeChat automation, or unofficial SDK use.

## Scope Evaluated

Documents inspected:

- `README.md`
- `AGENTS.md` working agreement from the current thread
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/tasks/M12_wechat_adapter/T230_wechat_adapter_research_spike.md`
- `docs/tasks/M12_wechat_adapter/T231_wechat_inbound_adapter.md`
- `docs/tasks/M12_wechat_adapter/T233_wechat_safety_mode.md`
- `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md`
- `docs/tasks/M12_wechat_adapter/T234_m12_milestone_review.md`
- `docs/review/T230_review.md`
- `docs/review/T230_wechat_adapter_research.md`
- `docs/review/T231_review.md`
- `docs/review/T233_review.md`
- `docs/review/T232_review.md`
- `docs/worker_summary/T230_worker_summary.md`
- `docs/worker_summary/T231_worker_summary.md`
- `docs/worker_summary/T233_worker_summary.md`
- `docs/worker_summary/T232_worker_summary.md`
- `docs/data_contracts/wecom_customer_service_inbound_contract.md`
- `docs/data_contracts/wecom_customer_service_safety_contract.md`
- `docs/data_contracts/wecom_customer_service_outbound_contract.md`
- `docs/data_contracts/outbound_send_gate_contract.md`

Code and tests inspected:

- `src/practical_chat_agent/connectors/inbound/wecom_customer_service.py`
- `src/practical_chat_agent/services/wecom_customer_service_safety.py`
- `src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py`
- `tests/test_wecom_customer_service_inbound.py`
- `tests/test_wecom_customer_service_safety_gate.py`
- `tests/test_wecom_customer_service_outbound_adapter.py`
- `tests/test_outbound_message_request_schema.py`
- `tests/test_outbound_send_gate.py`

No private chat history, private distilled artifacts, credentials, environment
secrets, live provider accounts, callbacks, or platform APIs were read or used.
T234 did not refetch external WeCom documentation; it evaluated the repository
evidence and the documented T230/T231 recheck date of 2026-05-28.

## Task Matrix

| Task | Review state | What it proves | What it does not prove |
| --- | --- | --- | --- |
| T230 research gate | PASS | Official-surface direction was narrowed to WeCom Customer Service for local review work; unsafe personal WeChat, scan-login, desktop automation, realtime personal-account behavior, and unofficial SDKs remain blocked. | Live account eligibility, credentials, callbacks, recipient mapping, outbound API compatibility, or delivery. |
| T231 synthetic inbound adapter | PASS | Synthetic WeCom Customer Service message and event payloads can be normalized deterministically into one `InboundEvent`; malformed and personal-WeChat-like payloads are rejected. | Live callbacks, polling, sync loops, signature verification, encryption/decryption, batching, store writes, or private identity mapping. |
| T233 provider safety mode | PASS | A local safety gate can block or allow provider eligibility after human approval plus `OutboundSendGate`, using explicit recipient aliases, service-window context, quota context, kill switch, channel checks, and metadata-smuggling checks. | Payload preparation, API compatibility, delivery, live provider state, credentials, callback state, or production recipient IDs. |
| T232 dry-run outbound adapter | PASS | A local adapter can prepare a review-safe dry-run payload only when the request is sendable and a matching T233 allowed decision exists; the result records `delivered=False`, `wecom_dry_run_only`, and `no_provider_delivery`. | Transport, provider API calls, real WeCom payload contract, retries, acknowledgement, failure-event mutation, runtime/CLI send paths, or automatic sending. |

## Safety Matrix

| Safety area | M12 status |
| --- | --- |
| Official surface selection | Conditional. WeCom Customer Service is the only allowed M12 surface for local synthetic review artifacts. Personal WeChat automation remains blocked. |
| Inbound behavior | Synthetic fixture normalization only. No callbacks, webhooks, polling, sync loops, batching, or live signature/encryption behavior. |
| Outbound request state | `OutboundMessageRequest` remains inert until explicit human approval and an allowed `OutboundSendGate`; reviewed `CandidateAction` evidence alone is insufficient. |
| Provider safety state | T233 `allowed` means provider eligibility snapshot only, not payload prepared and not delivery. |
| Dry-run payload state | T232 `wecom_dry_run_ready` means local payload prepared for review only, with `dry_run=true` and `delivered=False`. |
| Credential handling | Not implemented and not authorized. No token, secret, app ID, tenant ID, callback token, EncodingAESKey, OpenID, UnionID, `open_kfid`, or `external_userid` reads. |
| Recipient identity | Only synthetic aliases are used. No alias is proven to be a provider recipient ID. |
| Metadata privacy | T233 blocks provider identity or credential smuggling through request metadata; T232 does not copy arbitrary metadata into prepared payloads. |
| Live state | Service-window expiry and message counts are local context supplied to T233, not live provider state. |
| Store mutation | No memory, ContactSkill, RelationshipState, feedback, approved-store, inbound-store, outbound request, safety-decision, or runtime mutation is authorized by M12. |
| Delivery semantics | Not implemented. No sent, queued, accepted, acknowledged, retried, failed-by-provider, or delivered state is proven. |

## Evaluation Questions

1. What does M12 prove? It proves a local synthetic chain from research gate,
   through synthetic inbound normalization, through local provider eligibility,
   to dry-run payload preparation behind existing manual approval gates.
2. What does M12 not prove? It does not prove live WeCom or WeChat API
   compatibility, account eligibility, credentials, callback security,
   encryption, polling, transport, acknowledgement, retries, failure handling,
   production recipient mapping, or delivery.
3. Did T230 keep unsafe paths blocked? Yes. The accepted T230 evidence keeps
   personal WeChat automation, scan-login resurrection, desktop automation,
   realtime personal-account behavior, and unofficial SDK vendoring blocked.
4. Is T231 synthetic only? Yes. T231 accepts synthetic WeCom Customer Service
   message/event shapes and records `synthetic_only=true`; it does not define
   live callback, polling, signature, encryption, or store behavior.
5. Is T233 provider eligibility local only? Yes. T233 consumes local context and
   returns `allowed` or `blocked` eligibility; allow-path audit explicitly says
   `provider_eligible_not_delivery` and `provider_payload_not_prepared`.
6. Does T232 require a matching allowed safety decision and avoid delivery? Yes.
   T232 rejects missing, blocked, mismatched, wrong-surface, or incomplete
   safety decisions, produces only dry-run results, and exposes no `transport`,
   `send`, or `deliver` seam.
7. Are state meanings distinct? Yes. Candidate actions are evidence only;
   `OutboundMessageRequest.is_sendable()` means human approval plus send gate;
   T233 `allowed` means provider eligibility; T232 `wecom_dry_run_ready` means
   local dry-run payload prepared. None means live delivery.
8. Are tests synthetic, private-free, credential-free, and network-free? Yes.
   The inspected tests use synthetic fixtures and local models/services only.
   Verification ran without network, credentials, or private artifacts.
9. What gate should M12 receive? `Gate M12 Conditional`. It permits the local
   synthetic/dry-run artifacts to stand as reviewed M12 evidence, but blocks all
   live platform integration until separately scoped, reviewed work resolves the
   remaining live-readiness risks.

## Verification Results

Commands run for T234:

```text
python -m py_compile src/practical_chat_agent/connectors/inbound/wecom_customer_service.py src/practical_chat_agent/services/wecom_customer_service_safety.py src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py
```

Result: passed.

```text
pytest tests/test_wecom_customer_service_inbound.py tests/test_wecom_customer_service_safety_gate.py tests/test_wecom_customer_service_outbound_adapter.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q
```

Result: passed, `90 passed, 2 warnings in 0.10s`. The warnings were pytest
cache-provider warnings because `.pytest_cache` could not be written in this
environment.

```text
git diff --check
```

Result: passed. Git reported line-ending conversion warnings for pre-existing
dirty files in this Windows working copy.

```text
git status --short
```

Result: ran successfully. The worktree already contained pre-existing modified
and untracked files from earlier/Captain work; after T234 edits, status includes
the allowed T234 files `docs/review/M12_review.md`,
`docs/worker_summary/T234_worker_summary.md`, and `docs/07_handoff.md`. Git
also reported global ignore permission warnings for
`C:\Users\26410/.config/git/ignore`.

## Residual Risks

- Official WeCom/Tencent documentation may drift before any future live work.
- WeCom Customer Service may still be a product mismatch for WeFlow personal
  chat exports and personal relationship workflows.
- `channel_preference="wechat"` remains broad; current narrowing depends on
  explicit T233/T232 WeCom Customer Service surfaces.
- Synthetic inbound fixtures cover only a narrow subset of message and event
  fields.
- T231 parses one message per call; live batching remains undefined.
- Raw provider payload retention is acceptable only for synthetic fixtures;
  live redaction rules do not exist.
- T233 service-window and quota checks use supplied local context, not live
  provider state.
- Recipient aliases are not production provider identifiers.
- Credentials, tenant/app eligibility, callback token and EncodingAESKey
  handling, signature verification, encryption/decryption, and secret storage
  remain unresolved.
- T232 dry-run payload shape is review-safe and synthetic; it is not an
  official WeCom API request contract.
- Provider acknowledgement, failure-event handling, retry semantics, and
  outbound state mutation are unresolved.
- M12 completion can be overread as live readiness unless the conditional gate
  boundary remains explicit.

## Gate Recommendation

Recommend `Gate M12 Conditional`.

This gate allows:

- treating T230, T231, T233, and T232 as accepted M12 evidence for the local
  synthetic WeCom Customer Service slice;
- keeping and using the synthetic inbound contract, local safety gate, and
  dry-run payload preparation in review-safe, private-free local workflows;
- future docs-only or design-only live-readiness tasks if they are explicitly
  assigned and reviewed.

This gate blocks:

- live WeChat or WeCom API calls;
- credential, token, secret, tenant, app, QR-code, callback, EncodingAESKey, or
  real recipient reads;
- callback/webhook routes, polling, sync loops, schedulers, runtime wiring, or
  CLI send paths;
- transport, fake transport, retries, acknowledgement, failure-event mutation,
  or delivery interpretation;
- automatic sending;
- personal WeChat automation, scan-login resurrection, desktop automation, and
  unofficial SDK vendoring;
- production readiness or live-delivery claims.

The recommendation is not `Gate M12 Allow` because live platform behavior is
unproven. It is not `Gate M12 Block` because the local synthetic chain is
internally consistent, tested, and useful as a bounded manual-review artifact.

## Future Work Constraints

Any future WeCom/WeChat live-readiness task must be separately assigned and
reviewed, and must preserve the existing manual approval boundaries. Before any
live API call or delivery path is considered, a later task must at minimum:

- recheck official WeCom/Tencent documentation with a dated citation;
- define the exact provider surface and subchannel, not only
  `channel_preference="wechat"`;
- define credential, tenant, app, callback token, EncodingAESKey, and secret
  handling without storing secrets in the repo;
- define callback signature verification, encryption/decryption, replay
  protection, and redaction before storing provider payloads;
- define recipient mapping ownership and prove how repo contacts map to
  provider identities;
- define the live source of service-window and message-count state;
- define batching semantics for multi-message provider responses;
- validate payload compatibility against official docs without sending;
- keep `OutboundMessageRequest`, `OutboundSendGate`, T233 safety decisions, and
  T232 dry-run payloads as distinct states;
- add transport, acknowledgement, failure-event, retry, and mutation behavior
  only in a separate reviewed task package;
- continue blocking personal WeChat automation, scan-login resurrection,
  desktop automation, realtime personal-account send/receive, and unofficial
  SDK vendoring.
