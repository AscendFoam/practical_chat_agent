# Task T234: M12 WeChat Adapter Milestone Review

## Task ID

T234

## Goal

Produce the Milestone 12 gate review for the WeChat-family adapter slice.

The review must consolidate what T230-T233 actually prove:

```text
T230 research gate
  -> T231 synthetic WeCom Customer Service inbound contract
  -> T233 local provider safety gate
  -> T232 local dry-run outbound payload preparation
```

The review must recommend a gate status for M12 without authorizing live
WeChat/WeCom delivery, credentials, callbacks, polling, unofficial SDKs,
personal-WeChat automation, or realtime platform behavior.

## Why Now

T232 has passed review as a deterministic local dry-run outbound adapter. M12
now has all planned local/synthetic pieces completed at the task level:

- T230: `PASS`, `Gate M12 Conditional` research decision.
- T231: `PASS`, synthetic inbound contract for WeCom Customer Service.
- T233: `PASS`, local provider-safety gate.
- T232: `PASS`, local dry-run payload preparation behind T233.

The next task should not add another implementation layer. M12 needs a
milestone-level review that states what is proven, what remains unproven, and
whether future work should continue as a narrowed live-readiness research track,
stay local-only, or pause.

## Allowed Files

Worker may edit only:

- `docs/review/M12_review.md`
- `docs/worker_summary/T234_worker_summary.md`
- `docs/07_handoff.md`

If another file appears necessary, stop and report the need instead of editing
outside this list.

## Forbidden Scope

- Do not modify code, tests, schemas, services, CLIs, configs, package
  metadata, task board, risk docs, decision log, or task packages.
- Do not implement or modify any WeChat, WeCom, Tencent, Feishu, browser,
  desktop, webhook, callback, polling, sync, scheduler, runtime, or CLI send
  behavior.
- Do not call external platform APIs.
- Do not load or read credentials, environment variables, tokens, cookies,
  tenant IDs, app IDs, OpenIDs, UnionIDs, external user IDs, `open_kfid`,
  callback Token, EncodingAESKey, corpsecret, app secrets, QR codes, or real
  recipient IDs.
- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not create live provider fixtures or copy private content.
- Do not claim production readiness, official API payload compatibility, live
  callback compatibility, provider acknowledgement semantics, real recipient
  mapping, or live delivery.
- Do not start Milestone 13 or assign future implementation work.

## Inputs To Inspect

Use committed/repo-local material only:

- `README.md`
- `AGENTS.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- Task packages:
  - `docs/tasks/M12_wechat_adapter/T230_wechat_adapter_research_spike.md`
  - `docs/tasks/M12_wechat_adapter/T231_wechat_inbound_adapter.md`
  - `docs/tasks/M12_wechat_adapter/T233_wechat_safety_mode.md`
  - `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md`
- Reviews:
  - `docs/review/T230_review.md`
  - `docs/review/T230_wechat_adapter_research.md`
  - `docs/review/T231_review.md`
  - `docs/review/T233_review.md`
  - `docs/review/T232_review.md`
- Worker summaries:
  - `docs/worker_summary/T230_worker_summary.md`
  - `docs/worker_summary/T231_worker_summary.md`
  - `docs/worker_summary/T233_worker_summary.md`
  - `docs/worker_summary/T232_worker_summary.md`
- Data contracts:
  - `docs/data_contracts/wecom_customer_service_inbound_contract.md`
  - `docs/data_contracts/wecom_customer_service_safety_contract.md`
  - `docs/data_contracts/wecom_customer_service_outbound_contract.md`
  - `docs/data_contracts/outbound_send_gate_contract.md`
- Code and tests:
  - `src/practical_chat_agent/connectors/inbound/wecom_customer_service.py`
  - `src/practical_chat_agent/services/wecom_customer_service_safety.py`
  - `src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py`
  - `tests/test_wecom_customer_service_inbound.py`
  - `tests/test_wecom_customer_service_safety_gate.py`
  - `tests/test_wecom_customer_service_outbound_adapter.py`
  - `tests/test_outbound_message_request_schema.py`
  - `tests/test_outbound_send_gate.py`

Reading these files is allowed for evaluation. Editing them is not allowed
unless they are listed under `Allowed Files`.

## Evaluation Questions

Answer each question explicitly in `docs/review/M12_review.md`:

1. What does M12 prove about safe WeChat-family integration, and what does it
   not prove?
2. Did T230 correctly block unsafe personal-WeChat scan/login/realtime SDK
   paths and narrow the surface to official WeCom Customer Service?
3. Does T231 provide only synthetic inbound normalization, with no live
   callback, polling, credential, runtime, private-read, or store-mutation path?
4. Does T233 enforce provider eligibility locally before payload preparation,
   including sendability, selected surface, explicit recipient aliases,
   service window, message window, kill switch, manual-send-only, and metadata
   smuggling checks?
5. Does T232 require a matching allowed T233 safety decision before preparing a
   dry-run payload, and does it avoid transport/API/delivery semantics?
6. Are `OutboundMessageRequest`, `OutboundSendGate`,
   `WeComCustomerServiceSafetyDecision`, and `WeComCustomerServiceDryRunResult`
   kept as distinct states?
7. Are committed tests synthetic, deterministic, private-content-free,
   credential-free, network-free, and scoped to the M12 local contract?
8. What residual risks remain before any live WeCom callback, credential,
   provider payload, transport, acknowledgement, retry, or failure-event work?
9. Should the milestone gate be `Gate M12 Allow`, `Gate M12 Conditional`, or
   `Gate M12 Block`? If `Allow`, define exactly what is allowed. If
   `Conditional` or `Block`, define exactly what remains blocked.

## Required Report Structure

`docs/review/M12_review.md` must include:

- `Verdict`: one of `Gate M12 Allow`, `Gate M12 Conditional`, or
  `Gate M12 Block`
- `Scope Evaluated`: exact files/docs inspected and commands run
- `Task Matrix`: rows for T230, T231, T233, and T232 with status, proof, and
  non-authorized behavior
- `Safety Matrix`: rows for official surface selection, personal-WeChat block,
  inbound normalization, send-gate dependency, provider safety, dry-run payload,
  credential handling, callbacks/polling, transport/delivery, privacy, and
  state mutation
- `Verification Results`: command outputs summarized with pass/fail status
- `Residual Risks`: concrete risks that remain after T232
- `Gate Recommendation`: what M12 now authorizes and explicitly does not
  authorize
- `Future Work Constraints`: constraints for any later WeCom task

## Verification Commands

Run read-only/local verification where available. At minimum, attempt:

```powershell
python -m py_compile src/practical_chat_agent/connectors/inbound/wecom_customer_service.py src/practical_chat_agent/services/wecom_customer_service_safety.py src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py
pytest tests/test_wecom_customer_service_inbound.py tests/test_wecom_customer_service_safety_gate.py tests/test_wecom_customer_service_outbound_adapter.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q
git diff --check
git status --short
```

Use workspace-local pytest cache/basetemp paths if needed. If a command cannot
run, record the exact command, failure reason, and whether it affects the gate
recommendation.

## Expected Output

Produce:

- a milestone review at `docs/review/M12_review.md`
- a worker summary at `docs/worker_summary/T234_worker_summary.md`
- an appended T234 completion record in `docs/07_handoff.md`

Worker must not update `docs/04_task_board.md`; Captain updates that only after
review.

## Acceptance Criteria

- The report distinguishes implemented local/synthetic behavior from future
  live provider behavior.
- The gate recommendation is specific enough that later Captains cannot
  interpret M12 as live WeCom delivery authorization.
- All residual risks and future-work constraints are tied to concrete missing
  evidence.
- No code or test files are changed.
- No private content is read, quoted, or committed.
- No outbound/send/platform/scheduler behavior is introduced or authorized.

## Reviewer Type

milestone
