# Task T232: WeCom Customer Service Dry-Run Outbound Adapter

## Task ID

T232

## Goal

Implement a deterministic dry-run outbound adapter for the selected M12
official surface: WeCom Customer Service.

This adapter must run after both:

1. `OutboundSendGate`, represented by `OutboundMessageRequest.is_sendable()`.
2. T233 `WeComCustomerServiceSafetyGate`, represented by an explicit
   `WeComCustomerServiceSafetyDecision` with `safety_state="allowed"`.

The adapter may prepare a review-safe, synthetic dry-run payload from approved
outbound text and reviewed provider aliases. It must not call WeCom APIs, load
credentials, send messages, register callbacks, retry delivery, mutate stores,
or claim live provider compatibility.

## Why Now

T231 proved only a synthetic inbound contract. T233 then passed review as a
local provider-constraint safety gate that blocks unsafe WeCom Customer Service
eligibility before any payload preparation.

T232 is now the next safe M12 task because the repo can add a payload
preparation boundary without crossing into live delivery. The goal is to prove
that an already-sendable request plus an already-allowed T233 safety decision
can become a deterministic dry-run artifact with audit evidence and no platform
side effects.

## Allowed Files

Worker may edit only:

- `src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py`
- `tests/test_wecom_customer_service_outbound_adapter.py`
- `tests/fixtures/wecom_customer_service_outbound/*.json`
- `docs/data_contracts/wecom_customer_service_outbound_contract.md`
- `docs/worker_summary/T232_worker_summary.md`
- `docs/07_handoff.md`

If another file appears necessary, stop and report the need instead of editing
outside this list.

## Forbidden Scope

- Do not call WeChat, WeCom, Tencent, Feishu, or any external platform API.
- Do not load or read credentials, environment variables, tokens, cookies,
  tenant IDs, app IDs, OpenIDs, UnionIDs, external user IDs, `open_kfid`,
  callback Token, EncodingAESKey, corpsecret, app secrets, QR codes, or real
  recipient IDs.
- Do not add live transport, injected transport, fake transport, retry logic,
  acknowledgement handling, failure-event mutation, callback routes, webhook
  routes, polling/sync loops, schedulers, background jobs, CLI commands,
  runtime wiring, or `AppContainer` wiring.
- Do not send messages or represent any result as delivered, accepted by
  provider, queued by provider, retried, or acknowledged.
- Do not bypass T233 by reconstructing provider eligibility from raw context
  inside the adapter. The adapter must require an explicit allowed
  `WeComCustomerServiceSafetyDecision`.
- Do not store or expose real provider identifiers. Use only aliases from the
  safety decision.
- Do not copy arbitrary `OutboundMessagePayload.metadata` into the prepared
  provider dry-run payload.
- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not mutate memory, ContactSkill, RelationshipState, feedback logs,
  approved stores, inbound event stores, outbound requests, or safety
  decisions.
- Do not modify `src/practical_chat_agent/core/models.py`,
  `OutboundSendGate`, T233 safety gate code, inbound connectors, Feishu
  adapters, fake adapters, runtime services, task board, or tests outside the
  allowed test file.
- Do not claim production readiness, official API payload compatibility, live
  WeCom account eligibility, callback compatibility, or live-delivery
  readiness.

## Inputs To Read

- `README.md`
- `AGENTS.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/review/T233_review.md`
- `docs/data_contracts/outbound_message_request_contract.md` if present
- `docs/data_contracts/outbound_send_gate_contract.md`
- `docs/data_contracts/wecom_customer_service_safety_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/wecom_customer_service_safety.py`
- Existing adapter patterns:
  - `src/practical_chat_agent/services/outbound_fake_adapter.py`
  - `src/practical_chat_agent/services/feishu_outbound_adapter.py`
  - `tests/test_outbound_fake_adapter.py`
  - `tests/test_feishu_outbound_adapter.py`
  - `tests/test_wecom_customer_service_safety_gate.py`

Official docs do not need to be fetched for this task unless the worker wants
to recheck them. If rechecked, cite only official Tencent/WeCom documentation
and record retrieval dates in the outbound contract. If not rechecked, treat
T230/T233 provider facts as drift-sensitive.

## Expected Implementation

Create `WeComCustomerServiceDryRunOutboundAdapter` as a pure local payload
preparation boundary.

Recommended objects:

- `WeComCustomerServiceDryRunConfig`
  - `provider_surface: str = "wecom_customer_service"`
  - `dry_run_only: bool = True`
  - validate that `dry_run_only` remains true for this task
- `WeComCustomerServiceDryRunResult`
  - `delivery_status: Literal[...]`
  - `request_id: str | None`
  - `contact_id: str | None`
  - `user_id: str | None`
  - `provider_surface: str`
  - `recipient_alias: str | None`
  - `open_kfid_alias: str | None`
  - `external_user_alias: str | None`
  - `prepared_payload: dict[str, object] | None`
  - `audit_notes: list[str]`

Use status strings that make dry-run semantics explicit, for example:

- `wecom_dry_run_ready`
- `blocked_invalid_request`
- `blocked_candidate_action_input`
- `blocked_not_sendable`
- `blocked_channel_mismatch`
- `blocked_safety_missing`
- `blocked_safety_not_allowed`
- `blocked_safety_mismatch`
- `blocked_missing_safety_aliases`

The adapter should accept:

- an `OutboundMessageRequest` or stable mapping that validates to one;
- an explicit `WeComCustomerServiceSafetyDecision` or stable mapping that can
  be converted to one;
- optional `existing_audit`.

Required validation behavior:

- reject direct `CandidateAction` model inputs and candidate-shaped mappings;
- reject invalid request mappings with `blocked_invalid_request`;
- reject requests where `request.is_sendable()` is false;
- reject non-`wechat` `channel_preference`;
- reject missing safety decision;
- reject safety decision with `safety_state!="allowed"`;
- reject safety decision with provider surface other than
  `wecom_customer_service`;
- reject safety decision whose `request_id`, `contact_id`, or `user_id` does
  not match the outbound request;
- reject safety decision missing `recipient_alias`, `open_kfid_alias`, or
  `external_user_alias`;
- require the safety decision audit to include the T233 boundary notes
  `provider_eligible_not_delivery` and `provider_payload_not_prepared`;
- preserve caller audit notes and safety audit notes without duplicating them;
- never mutate the input request or safety decision.

Required dry-run payload behavior:

- build a deterministic in-memory payload only when all validations pass;
- include `provider_surface="wecom_customer_service"`;
- include `dry_run=True`;
- include `request_id`, `contact_id`, and `user_id`;
- include a nested recipient-alias object with only:
  - `recipient_alias`
  - `open_kfid_alias`
  - `external_user_alias`
- include a text message body from `OutboundMessagePayload.draft_text`;
- include `safe_summary` if present;
- include `source_type` and `source_candidate_action_id` for audit context;
- do not include arbitrary request metadata, credentials, real provider IDs,
  endpoint URLs, access tokens, callback fields, tenant IDs, retry fields,
  transport fields, or delivery response fields;
- record audit notes such as `request_sendable_verified`,
  `wecom_safety_decision_verified`, `wecom_dry_run_payload_prepared`,
  `wecom_dry_run_only`, and `no_provider_delivery`.

The result must make clear that payload preparation is not delivery.

## Required Tests

Use TDD. Add tests that fail before implementation and then pass.

Minimum test scenarios:

- allowed sendable request plus allowed matching T233 safety decision returns
  `wecom_dry_run_ready` and prepares the expected dry-run payload;
- pending human approval or blocked send gate returns `blocked_not_sendable`;
- missing safety decision returns `blocked_safety_missing`;
- blocked T233 safety decision returns `blocked_safety_not_allowed`;
- mismatched safety decision request/contact/user identity returns
  `blocked_safety_mismatch`;
- wrong safety decision provider surface returns `blocked_safety_mismatch`;
- missing safety aliases returns `blocked_missing_safety_aliases`;
- non-`wechat` channel preference returns `blocked_channel_mismatch`;
- direct `CandidateAction` model input and candidate-shaped mapping are
  rejected;
- invalid request mapping returns `blocked_invalid_request`;
- mapping input validates consistently with model input for both request and
  safety decision;
- arbitrary `OutboundMessagePayload.metadata` is not copied into
  `prepared_payload`;
- input `OutboundMessageRequest` and `WeComCustomerServiceSafetyDecision` are
  not mutated;
- no transport hook or API-call seam exists in the adapter object.

Synthetic fixture files under
`tests/fixtures/wecom_customer_service_outbound/` may be used for request,
safety-decision, and expected-payload examples. They must contain aliases only,
not real provider IDs or private content.

## Expected Output

- `src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py`
- `tests/test_wecom_customer_service_outbound_adapter.py`
- optional synthetic fixtures under
  `tests/fixtures/wecom_customer_service_outbound/`
- `docs/data_contracts/wecom_customer_service_outbound_contract.md`
- `docs/worker_summary/T232_worker_summary.md`
- T232 worker completion record appended to `docs/07_handoff.md`

Worker must not update `docs/04_task_board.md`; Captain updates that only after
review.

## Verification

Run at minimum:

```powershell
python -m py_compile src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py
pytest tests/test_wecom_customer_service_outbound_adapter.py -q
pytest tests/test_wecom_customer_service_outbound_adapter.py tests/test_wecom_customer_service_safety_gate.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q
git diff --check
git status --short
```

Use workspace-local pytest cache/basetemp paths if needed.

The worker summary must record commands, results, explicit non-actions, and
remaining risks.

## Docs To Update

During worker execution:

- `docs/data_contracts/wecom_customer_service_outbound_contract.md`
- `docs/worker_summary/T232_worker_summary.md`
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
