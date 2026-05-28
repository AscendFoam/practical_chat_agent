# Task T231: WeCom Customer Service Inbound Contract Spike

## Task ID

T231

## Goal

Implement a local, synthetic-only inbound contract for one official
WeChat-family surface: WeCom WeChat Customer Service.

The task should prove whether documented WeCom Customer Service message/event
payload shapes can be normalized into this repository's `InboundEvent` boundary
without credentials, live callbacks, polling, private chat reads, memory writes,
or runtime delivery behavior.

This is not a live WeChat adapter. It is a contract and fixture spike.

## Why Now

T230 passed review with `Gate M12 Conditional`.

The research result blocks generic personal-WeChat automation, scan-login
resurrection, unofficial SDKs, desktop automation, and live outbound delivery.
It allows only a narrowed, official-platform path that starts with synthetic
fixtures and a pure normalizer.

WeCom WeChat Customer Service is selected for T231 because it is an official
WeChat-family customer-service surface with documented inbound and outbound
concepts, service-window constraints, and failure-event semantics. It still
does not map cleanly to arbitrary WeFlow personal chat contacts, so this task
must keep all output synthetic and contract-level.

## Allowed Files

Worker may edit only:

- `src/practical_chat_agent/connectors/inbound/wecom_customer_service.py`
- `src/practical_chat_agent/connectors/inbound/__init__.py`
- `tests/test_wecom_customer_service_inbound.py`
- `tests/fixtures/wecom_customer_service_inbound/**`
- `docs/data_contracts/wecom_customer_service_inbound_contract.md`
- `docs/worker_summary/T231_worker_summary.md`
- `docs/07_handoff.md`

If the worker believes another file is necessary, stop and report the need
instead of editing outside this list.

## Forbidden Scope

- Do not implement live callback routes, webhook servers, polling/sync loops,
  background jobs, schedulers, runtime ingestion hooks, or `AppContainer`
  wiring.
- Do not call WeChat, WeCom, Tencent, Feishu, or any external platform API.
- Do not install packages, clone SDKs, vendor SDK code, or copy unofficial SDK
  snippets.
- Do not use real `corpsecret`, app secret, `access_token`, callback Token,
  EncodingAESKey, tenant ID, app ID, OpenID, external user ID, `open_kfid`, chat
  ID, cookies, QR codes, or private recipients.
- Do not implement encryption/decryption, signature verification with real
  secrets, OAuth, tenant setup, credential loading, environment-variable
  handling, or IP allowlists.
- Do not send messages, prepare outbound payloads, retry delivery, or interpret
  provider acceptance as delivery.
- Do not read `private/chat_history/`, `private/distilled/`, or any private
  artifact.
- Do not mutate memory, ContactSkill, RelationshipState, feedback logs,
  approved stores, or outbound request/gate state.
- Do not modify `src/practical_chat_agent/core/models.py`, outbound adapters,
  send-gate behavior, CLI commands, runtime services, or task board.
- Do not claim production readiness or live WeCom compatibility.

## Inputs To Read

- `README.md`
- `AGENTS.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/review/T230_wechat_adapter_research.md`
- `docs/review/T230_review.md`
- `docs/data_contracts/outbound_send_gate_contract.md`
- Existing inbound connector pattern:
  - `src/practical_chat_agent/connectors/inbound/base.py`
  - `src/practical_chat_agent/connectors/inbound/feishu_bot.py`
  - `src/practical_chat_agent/services/inbound.py`
- Existing `InboundEvent`, `InboundConnectorResult`, and enums in
  `src/practical_chat_agent/core/models.py` and
  `src/practical_chat_agent/core/enums.py`.

If official docs are rechecked, use only official Tencent/WeCom docs and record
retrieval dates in the data contract. If network access is unavailable, state
that the worker used the T230 research citations and treated current platform
facts as drift-sensitive.

## Expected Implementation

Create `WeComCustomerServiceInboundConnector` as a pure local parser behind the
existing `InboundConnector` abstraction.

The connector should:

- expose `connector_name = "wecom_customer_service"`;
- implement `can_handle_payload(payload)` for the synthetic fixture wrapper
  and documented WeCom Customer Service shaped payloads used by this task;
- implement `parse_inbound_payload(payload)` returning
  `InboundConnectorResult`;
- map incoming customer text messages to `InboundEvent` with:
  - `platform=Platform.WECHAT`
  - `source_type=SourceType.CHAT_MESSAGE`
  - `direction=Direction.INBOUND`
  - `channel_type=ChannelType.DM`
  - `content_type=ContentType.TEXT`
  - deterministic `event_id` from provider-safe synthetic fields
  - `channel_id` scoped to the synthetic `open_kfid` / customer-service session
  - `account_id` scoped to the synthetic customer-service account
  - `actor_id` from a synthetic external-user alias, not a real platform ID
  - `text` from the synthetic message body
  - `raw` containing only the synthetic fixture payload and contract metadata;
- map non-text or provider event/failure shapes to conservative
  `ContentType.SYSTEM` events or explicit parser errors, whichever is clearer
  and covered by tests;
- never infer repo `contact_id` or memory identity from provider IDs;
- never inspect private files or environment variables.

The synthetic fixture set should include at minimum:

- one inbound text message;
- one non-text message or unsupported message type;
- one provider event/failure-style payload relevant to WeCom Customer Service;
- one malformed payload that must be rejected deterministically;
- one payload that resembles personal-WeChat/desktop automation and must not be
  accepted by this connector.

The data contract document should explain:

- why WeCom Customer Service was selected for this contract spike;
- which fixture fields are synthetic provider identity fields;
- how the connector maps provider fields to `InboundEvent`;
- which provider constraints remain unresolved: credential flow, callback
  verification, encryption/signature handling, service windows, recipient
  mapping, delivery/failure semantics, and account eligibility;
- why this task does not authorize T232 live outbound delivery.

## Expected Output

- A new local connector module with deterministic parsing only.
- Committed synthetic fixtures with fake IDs and no private content.
- Focused tests for can-handle behavior, successful text normalization,
  unsupported/event behavior, malformed rejection, and rejection of
  personal-WeChat/desktop-like payloads.
- `docs/data_contracts/wecom_customer_service_inbound_contract.md`.
- `docs/worker_summary/T231_worker_summary.md`.
- A T231 worker completion record appended to `docs/07_handoff.md`.

Worker must not update `docs/04_task_board.md`; Captain updates that only after
review.

## Verification

Run at minimum:

```powershell
python -m py_compile src/practical_chat_agent/connectors/inbound/wecom_customer_service.py
pytest tests/test_wecom_customer_service_inbound.py -q
git diff --check
git status --short
```

If the worker changes `connectors/inbound/__init__.py`, include it in the
`py_compile` command.

The worker summary must record all commands, results, explicit non-actions, and
remaining risks.

## Docs To Update

During worker execution:

- `docs/data_contracts/wecom_customer_service_inbound_contract.md`
- `docs/worker_summary/T231_worker_summary.md`
- `docs/07_handoff.md`

After reviewer approval, Captain will update:

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type

adversarial
