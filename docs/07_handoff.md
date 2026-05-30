# Handoff

## Captain Current State Override 2026-05-31 (M13 Research Synthesis / T240 Open)

- Returned research:
  `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`.
- Captain decision: accept the report's core recommendation and open M13 as a
  docs-only commercial companion product boundary pack.
- M12 remains `Gate M12 Conditional` and still authorizes only the
  local/synthetic/dry-run WeCom Customer Service evidence slice.
- Current Unique Task:
  T240 `M13 Commercial Companion Positioning And Safety Boundary Pack`.
- Worker task package:
  `docs/tasks/M13_commercial_companion/T240_commercial_companion_positioning.md`.
- Why this task is next:
  - GPT-Pro research has returned and needs to be converted into repo-owned
    product, safety, architecture, roadmap, and task-package artifacts.
  - Jumping directly to Persona Compiler, proactive messages, UX, voice/avatar,
    or platform delivery would bypass review-first and safety governance.
- Allowed worker scope:
  - create product positioning and competitor matrix docs
  - create clone/persona risk tiers and proactive redlines
  - create M13 persona-memory-relationship architecture and M13+ roadmap docs
  - create the first M14 Persona Compiler task package
  - update only `docs/07_handoff.md` and
    `docs/worker_summary/T240_worker_summary.md` as worker-owned governance
    outputs
- Forbidden worker scope:
  - no implementation code/tests, CLI/runtime/config changes, stores, schemas,
    connectors, adapters, schedulers, or platform work
  - no live WeChat/WeCom/Feishu delivery, credentials, callbacks, webhooks,
    polling, transport, acknowledgements, retries, or automatic sending
  - no unauthorized real-person clone, ex-partner/family/public-figure
    replica, deceased-person resurrection, voice cloning, face/avatar deepfake,
    or deceptive real-person simulation
  - no `private/chat_history/` or private artifact reads
- Verification for T240:
  - `git diff --check`
  - `Test-Path` checks for all expected docs
  - `rg` checks for M13 gate, M14-M22, L1/L5, automatic-sending,
    unauthorized-clone, and imagined-memory coverage in the generated docs
- Recommended reviewer type: adversarial review.
- `/goal` / branch recommendation:
  - A branch-bound `/goal` trial is feasible after the current governance state
    is committed or otherwise snapshotted.
  - Do not ask `/goal` to "finish all M13-M22 tasks" in one run.
  - A safer goal is "complete the current task package, stop for review, then
    wait for Captain judgment."
  - Prefer reverting by abandoning/deleting the trial branch or reverting
    specific commits, not by destructive reset on a dirty main worktree.

## Captain Current State Override 2026-05-30 (T234 / M12 Close)

- T234 completion basis:
  - `docs/worker_summary/T234_worker_summary.md`
  - `docs/review/M12_review.md`
- Captain decision: accept T234 as complete. No separate reviewer pass is
  required because T234 was itself the M12 milestone-review task and changed
  only review/handoff/summary docs.
- M12 gate decision: `Gate M12 Conditional`.
- M12 is complete only as a local/synthetic/dry-run WeCom Customer Service
  evidence slice:
  - T230 research gate narrowed unsafe WeChat-family options.
  - T231 proved synthetic inbound normalization.
  - T233 proved local provider eligibility after `OutboundSendGate`.
  - T232 proved dry-run payload preparation behind a matching allowed T233
    decision.
- M12 does not authorize:
  - live WeChat or WeCom API calls
  - credentials, callbacks, webhooks, polling, sync loops, schedulers, runtime
    wiring, CLI send paths, transport, fake transport, retries,
    acknowledgement, failure-event mutation, or delivery interpretation
  - production recipient mapping or live provider identity claims
  - automatic sending
  - personal-WeChat automation, scan-login resurrection, desktop automation,
    realtime personal-account send/receive, or unofficial SDK vendoring
- Current implementation worker status: no new worker task is assigned yet.
- Current external research action:
  - Prompt file:
    `docs/prompts/commercial_companion_agent_deep_research_prompt.md`
  - Input context:
    `docs/reference/和gpt-pro的对话.md`
  - Owner: user running GPT-Pro outside the worker flow.
- Next Captain action after research returns:
  - synthesize the GPT-Pro report into M13+ milestones
  - update 00-08 governance docs
  - create the first worker task package under `docs/tasks/`
  - preserve review-first, privacy-safe, no-deception, no-unauthorized-clone,
    and no-automatic-send boundaries
- Recommended commercial-product direction to research:
  - Persona Compiler
  - Memory OS v2 with factual/inferred/imagined separation
  - Relationship Engine semantic consumption
  - consented and rate-limited Proactive Engine
  - Virtual Life Stream / role dynamics
  - memory/persona user controls
  - compliance and safety baseline

## Captain Current State Override 2026-05-30 (T232 Review Decision)

- T232 review decision: `PASS`.
- T232 is complete as the WeCom Customer Service dry-run outbound adapter for M12.
- T232 review observation disposition:
  - Accepted: N01 duplicated candidate-action detection is acceptable until shared extraction is justified, N02 safety-decision dataclass coercion blocks malformed mappings sufficiently for dry-run scope, N03 blocked audit notes are consistent, N04 missing safety identity fields defensively mismatch, N05 hardcoded text message type is correct for T232 scope, N06 dry-run config validation is a useful pattern improvement, N07 surface constant/literal duplication is minor, N08 coverage gaps are non-blocking test-strength notes.
  - Deferred: none from the T232 review decision.
  - Rejected: none.
- Captain decision: no T232 repair pass is needed.
- Historical next task at the T232 closeout point: T234 M12 WeChat Adapter
  Milestone Review.
- Historical task package:
  `docs/tasks/M12_wechat_adapter/T234_m12_milestone_review.md`.
- T234 was scoped as docs-only and review-only:
  - may inspect T230/T231/T233/T232 task packages, reviews, worker summaries, data contracts, code, and tests
  - may run local read-only verification commands
  - must not modify code/tests beyond the allowed review docs, call platform APIs, load credentials, add runtime paths, send messages, mutate stores, read private artifacts, or authorize live WeCom behavior
- Captain verification basis:
  - Reviewer reported no blocking issues and no required missing tests.
  - Reviewer verified T232 changed only allowed files and did not modify core models, send-gate behavior, T233 safety gate code, inbound connectors, Feishu/fake adapters, runtime services, CLI commands, or task board.
  - Reviewer verified all required T232 scenarios were covered by 23 focused tests.
  - Worker summary reports `py_compile` passed for `wecom_customer_service_outbound_adapter.py`.
  - Worker summary reports targeted T232 pytest passed: 23 tests.
  - Worker summary reports combined T232 + T233 + outbound schema + send-gate pytest passed: 84 tests.
  - Worker summary reports `git diff --check` passed with line-ending conversion warnings only.
- M12 residual risks carried forward:
  - T232 proves only local deterministic dry-run payload preparation, not live WeCom Customer Service API compatibility.
  - Official Tencent/WeCom docs were not refetched in T232 and may drift before live work.
  - The dry-run payload shape is synthetic and review-safe, not an official API request contract.
  - T233 safety decisions are local snapshots, not live provider state.
  - Recipient aliases are not proven provider identifiers.
  - Credential handling, tenant eligibility, callback verification, encryption/decryption, provider failure events, acknowledgement semantics, retries, and production recipient mapping remain unresolved.
  - M12 task completion must not be interpreted as live WeCom delivery authorization; T234 has stated the gate boundary explicitly.

## Captain Current State Override 2026-05-30 (T233 Review Decision)

- T233 review decision: `PASS`.
- T233 is complete as the WeCom Customer Service provider safety gate for M12.
- T233 review observation disposition:
  - Accepted: N01 `casefold()` comparison is correct for the current ASCII lowercase smuggling-key set, N02 short-circuit blocking is acceptable for this safety-gate contract, N03 surface validation at evaluation time is acceptable for current scope, N04 `_coerce_context` missing-`now` error type is a minor inconsistency, N05 `timezone.utc` normalization is harmless, N06 smuggling checks are partially redundant with model validation but useful for defensive mapping-input paths, N07 additional coverage gaps are non-blocking test-strength notes, N08 `WECom_CUSTOMER_SERVICE_SURFACE` capitalization is cosmetic.
  - Deferred: none from the T233 review decision.
  - Rejected: none.
- Captain decision: no T233 repair pass is needed.
- Current Unique Task: T232 WeCom Customer Service Dry-Run Outbound Adapter.
- Current task package: `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md`.
- T232 must remain dry-run-only and non-delivery:
  - may prepare a deterministic review-safe dry-run payload only from a sendable `OutboundMessageRequest` and a matching T233 `WeComCustomerServiceSafetyDecision(safety_state="allowed")`
  - must reject missing, blocked, or mismatched safety decisions; direct `CandidateAction` inputs; invalid mappings; non-sendable requests; non-`wechat` channel; wrong surface; missing aliases; and arbitrary metadata-copy attempts
  - must use aliases only and must record that dry-run readiness is not delivery
  - must not call platform APIs, load credentials, add live/fake transport, register callbacks, poll/sync messages, retry, add runtime/CLI send paths, mutate stores, read private artifacts, or claim live WeCom compatibility
- Captain verification basis:
  - Reviewer reported no blocking issues and no required missing tests.
  - Reviewer verified T233 changed only allowed files and did not modify core models, send-gate behavior, inbound connectors, outbound adapters, runtime services, CLI commands, or task board.
  - Reviewer verified all required T233 scenarios were covered by 25 focused tests.
  - Worker summary reports `py_compile` passed for `wecom_customer_service_safety.py`.
  - Worker summary reports targeted T233 pytest passed: 25 tests.
  - Worker summary reports combined T233 + outbound schema + send-gate pytest passed: 61 tests.
  - Worker summary reports `git diff --check` passed with line-ending conversion warnings only.
- M12 residual risks carried forward:
  - T233 proves only local deterministic provider eligibility, not live WeCom Customer Service API compatibility.
  - Official Tencent/WeCom docs were not refetched in T233 and may drift before live work.
  - Recipient aliases, service-window expiry, and sent-message counts are supplied local context, not live provider state.
  - Credential handling, tenant eligibility, callback verification, encryption/decryption, provider failure events, acknowledgement semantics, retries, and production recipient mapping remain unresolved.
  - `channel_preference="wechat"` is still broad and only narrows to WeCom Customer Service through explicit T233 safety config.
  - T232 must keep dry-run payload preparation separate from API acceptance, delivery, acknowledgement, retries, and failure-event mutation.

## Captain Current State Override 2026-05-29 (T231 Review Decision)

- T231 review decision: `PASS`.
- T231 is complete as the WeCom Customer Service inbound contract spike for M12.
- T231 review observation disposition:
  - Accepted: N01 `connectors.inbound.__init__` export style is a minor namespace inconsistency, N02 timestamp epoch fallback is acceptable for synthetic-only scope but live work needs invalid-timestamp semantics, N03 first-message-only parsing matches current one-event inbound abstraction and batching remains future scope, N04 timestamp/text/optional/fallback coverage gaps are minor, N05 far-future timestamp heuristic is not practical current risk.
  - Deferred: none from the T231 review decision.
  - Rejected: none.
- Captain decision: no T231 repair pass is needed.
- Current Unique Task: T233 WeCom Customer Service Provider Safety Gate.
- Current task package: `docs/tasks/M12_wechat_adapter/T233_wechat_safety_mode.md`.
- T233 must remain provider-safety-only and non-delivery:
  - may implement a deterministic local provider safety gate over already-sendable `OutboundMessageRequest` records
  - may evaluate explicit recipient map, active service window, 5-message window limit, provider kill switch, manual-send-only defaults, metadata-smuggling blocks, and review-safe audit aliases
  - must not prepare WeCom API payloads, call APIs, load credentials, register callbacks, poll/sync messages, add runtime wiring, send messages, mutate stores, read private artifacts, or update task board
- Captain verification basis:
  - Reviewer reported no blocking issues.
  - Reviewer verified all required T231 scenarios were covered by six committed tests.
  - Reviewer verified T231 changed only allowed files and did not modify core models, outbound adapters, send-gate behavior, CLI commands, runtime services, or task board.
  - Worker summary reports `py_compile` passed for the new connector and inbound package init.
  - Worker summary reports targeted T231 pytest passed: 6 tests.
  - Worker summary reports `git diff --check` passed with line-ending conversion warnings only.
- M12 residual risks carried forward:
  - T231 is synthetic-contract-only and does not prove live WeCom callback compatibility.
  - Timestamp fallback and first-message-only parsing are acceptable for synthetic scope but not sufficient for live sync/callback integration.
  - Official docs may drift before live work.
  - No recipient mapping exists from synthetic WeCom aliases to repo contacts.
  - Provider credential flow, callback verification, encryption/decryption, service-window tracking, quota enforcement, and failure-event state mutation remain unresolved.
  - T232 remains blocked until T233 provider safety passes review and Captain rewrites T232.

## Captain Current State Override 2026-05-28 (T230 Review Decision / M12 Conditional)

- T230 review decision: `PASS`.
- T230 is complete as the WeChat adapter research spike for M12.
- M12 gate decision: `Gate M12 Conditional`.
- T230 review observation disposition:
  - Accepted: N01 external official docs were cited but not independently refetched by reviewer and must be rechecked before implementation, N02 option matrix depth is appropriate for a research spike and future tasks need deeper API/error/session analysis, N03 final surface selection was intentionally unresolved by worker but Captain selects WeCom Customer Service for T231, N04 broad `channel_preference="wechat"` is accepted as a schema limitation that future outbound work must not use as production adapter selection.
  - Deferred: none from the T230 review decision.
  - Rejected: none.
- Captain decision: no T230 repair pass is needed.
- Current Unique Task: T231 WeCom Customer Service Inbound Contract Spike.
- Current task package: `docs/tasks/M12_wechat_adapter/T231_wechat_inbound_adapter.md`.
- T231 must remain synthetic-inbound-contract-only:
  - may add a local deterministic parser/normalizer for synthetic WeCom WeChat Customer Service fixtures into `InboundEvent`
  - may add synthetic fixtures, focused tests, a data contract, worker summary, and handoff record
  - must not add live callback routes, webhook servers, polling/sync loops, platform API calls, credentials, SDKs, runtime ingestion hooks, `AppContainer` wiring, outbound payloads, sending, memory writes, private reads, or task-board updates
- Captain verification basis:
  - Reviewer reported no blocking issues.
  - Reviewer reported no missing tests applicable to T230 because it is docs-only.
  - Reviewer verified T230 changed only allowed files: `docs/review/T230_wechat_adapter_research.md`, `docs/worker_summary/T230_worker_summary.md`, and `docs/07_handoff.md`.
  - Worker summary reports `git diff --check` and the scoped `git diff --check` passed, with line-ending conversion warnings only.
  - Worker summary reports `git status --short` ran and showed pre-existing unrelated dirty files plus T230 allowed-file changes.
- M12 residual risks carried forward:
  - Official docs may drift and must be rechecked before any implementation touches credentials, callbacks, polling, or APIs.
  - WeCom Customer Service is an official customer-service surface, not a generic personal WeChat friend-chat adapter and not a direct WeFlow contact mapping.
  - No live account, tenant, app, callback URL, credential flow, recipient mapping, service-window tracking, delivery callback, or provider failure handling has been tested.
  - Historical note: T231 has since passed; T232 remains blocked until T233 provider safety passes review and Captain rewrites T232.
  - Personal WeChat automation, scan-login resurrection, realtime personal-account send/receive, desktop automation, and unofficial SDK vendoring remain blocked.

## Captain Current State Override 2026-05-28 (T224 Review Decision / M11 Close)

- T224 review decision: `PASS`.
- T224 is complete as the Feishu review-card task for M11.
- M11 is complete at the task level with `Gate M11 Allow` for local/sandbox outbound safety only.
- T224 review observation disposition:
  - Accepted: N01 `.claude/settings.json` allowed-permission overrun is established workspace convention noise, N02 duplicated candidate-shaped mapping detection is acceptable, N03 sandbox-result mapping coercion is acceptable for synthetic current scope, N04 missing config validation edge tests are minor, N05 wide render type signature is intentional for clear runtime rejection, M01-M04 missing mapping-positive, preview-small-limit, frozen-intent, and cosmetic blocked-result tests are useful hardening but non-blocking.
  - Deferred: none from the T224 review decision.
  - Rejected: none.
- Captain decision: no T224 repair pass is needed.
- Current Unique Task: T230 WeChat Adapter Research Spike.
- Current task package: `docs/tasks/M12_wechat_adapter/T230_wechat_adapter_research_spike.md`.
- T230 must remain docs-only and research-only:
  - may research official/supported WeChat-family adapter options and produce a gate recommendation
  - may recommend whether T231/T232/T233 should proceed, be narrowed, or be blocked
  - must not implement connectors, install/vendor SDKs, log in, scan QR codes, send/receive messages, call platform APIs, read credentials/secrets, modify runtime configuration, add callbacks/webhooks, add CLI/runtime paths, or revive the paused personal-WeChat SDK/realtime track
  - must not read `private/chat_history/` or commit private content
- Captain verification basis:
  - Reviewer reported no blocking issues.
  - Reviewer reported all M11 `py_compile` checks passed.
  - Reviewer reported T224-targeted pytest passed: 84 tests.
  - Reviewer reported full-suite status as 844 passed plus 16 pre-existing typer/LLM/CLI-dependent failures in the reviewer environment; worker summary reported 864 passed in the worker environment. No T224-targeted failures were reported.
- M11 residual risks carried forward:
  - Gate `allowed` is not delivery.
  - Fake `fake_delivered` is local synthetic simulation only.
  - Feishu sandbox `feishu_dry_run_ready` / `feishu_sandbox_sent` is sandbox evidence only.
  - Feishu review-card actions are inert review intents only.
  - Feishu sandbox payload/card/callback shapes are not production API validation.
  - T230/M12 must not resume the old scan-login/realtime WeChat track without explicit later authorization.

## Captain Current State Override 2026-05-28 (T223 Review Decision)

- T223 review decision: `PASS`.
- T223 is complete as the Feishu sandbox adapter task for M11.
- T223 review observation disposition:
  - Accepted: N01 duplicated candidate-shaped mapping detection is acceptable, N02 redundant `FeishuSandboxRecipient` runtime validation is harmless defensive code, N03 recipient-map normalization by reassignment is functionally correct, N04 Feishu payload shape is a sandbox approximation that must be validated before production delivery, N05 mutable result dataclasses are acceptable for current scope, M01-M06 missing edge tests are useful hardening targets but non-blocking.
  - Deferred: none from the T223 review decision.
  - Rejected: none.
- Captain decision: no T223 repair pass is needed.
- Current Unique Task: T224 Feishu Review Card.
- Current task package: `docs/tasks/M11_outbound_sendgate_feishu/T224_feishu_review_card.md`.
- T224 must remain local-review-card-only and non-executing:
  - may render deterministic Feishu review-card payloads from `OutboundMessageRequest` plus optional gate / Feishu sandbox result evidence
  - may parse synthetic card-action payloads into inert review-intent data
  - must not apply approvals, edits, rejects, or boundary feedback
  - must not call fake/Feishu adapters, send messages, register webhook/callback servers, read credentials, write feedback logs, write memory, mutate stores/private artifacts, add CLI/runtime send paths, add scheduler/timer/background jobs, or integrate WeChat
  - must not read `private/chat_history/` or commit private content
- Captain verification basis:
  - Reviewer reported no blocking issues.
  - Reviewer reported `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py src/practical_chat_agent/services/feishu_outbound_adapter.py` passed.
  - Reviewer reported targeted outbound schema + gate + fake + Feishu adapter tests passed: 65 tests.
  - Reviewer reported full-suite status as 825 passed plus 16 pre-existing typer/LLM/CLI-dependent failures in the reviewer environment; worker summary reported 845 passed in the worker environment. No T223-targeted failures were reported.
- M11 residual risks carried forward:
  - Gate `allowed` is not delivery.
  - Fake `fake_delivered` is local synthetic simulation only.
  - Feishu sandbox `feishu_dry_run_ready` / `feishu_sandbox_sent` is sandbox evidence only.
  - Feishu sandbox payload shape is not production API validation.
  - T224 review-card actions must remain inert review intents until a later explicit task applies them.
  - Windows named-timezone verification needs either `tzdata` or a documented UTC-only fallback.

## Captain Current State Override 2026-05-28 (T222 Review Decision)

- T222 review decision: `PASS`.
- T222 is complete as the local fake outbound adapter task for M11.
- T222 review observation disposition:
  - Accepted: N01 candidate-shaped mapping detection is intentionally conservative, N02 blocked direct `CandidateAction` model results may omit `contact_id` / `user_id` cosmetically, N03 `payload_preview` truncation is not a privacy boundary for future real adapters, M01 fake-adapter config validation tests are useful hardening, M02 `existing_audit` coverage is useful hardening, M03 preview boundary tests are useful hardening.
  - Deferred: none from the T222 review decision.
  - Rejected: none.
- Captain decision: no T222 repair pass is needed.
- Current Unique Task: T223 Feishu Sandbox Adapter.
- Current task package: `docs/tasks/M11_outbound_sendgate_feishu/T223_feishu_adapter.md`.
- T223 must remain Feishu-sandbox-only and non-production:
  - may consume only `OutboundMessageRequest` records that are already sendable through explicit outbound human approval plus T221 gate `allowed`
  - may prepare Feishu-compatible text payloads from approved outbound draft text and explicit sandbox recipient mapping
  - may default to dry-run and may use an injected fake/sandbox transport in tests
  - must not add production Feishu delivery, credentials, webhook/event handling, scheduler/timer/background jobs, CLI/runtime send paths, AppContainer wiring, automatic sending, WeChat integration, or real external API calls in committed tests
  - must not read `private/chat_history/` or commit private content
- Captain verification basis:
  - Reviewer reported no blocking issues.
  - Reviewer reported `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py` passed.
  - Reviewer reported `pytest tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py` passed: 24 tests.
  - Reviewer reported `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py` passed: 43 tests.
  - Reviewer reported full-suite status as 10 pre-existing typer/LLM/CLI-dependent failures plus 762 passed in the reviewer environment; worker summary reported 823 passed in the worker environment. No T222-targeted failures were reported.
- M11 residual risks carried forward:
  - Gate `allowed` is not delivery.
  - Fake `fake_delivered` is local synthetic simulation only.
  - `payload_preview` truncation is not a privacy boundary for future real adapters.
  - T223/T224 and M12 remain behind later task packages and reviews.
  - Windows named-timezone verification needs either `tzdata` or a documented UTC-only fallback.

## Captain Current State Override 2026-05-28 (T221 Review Decision)

- T221 review decision: `PASS`.
- T221 is complete as the deterministic outbound send-gate task for M11.
- T221 review observation disposition:
  - Accepted: N01 service-layer dataclasses are acceptable, N02 repeated HH:MM parsing is harmless at current scale, N03 `casefold()` normalization is sufficient for current Chinese/Latin checks, N04 Windows named-timezone use requires `tzdata` and is a portability note, N05 manual-only false config correctly errors, N06 `existing_audit` is harmless but untested, N07 decision audit can be read through `evaluated_request.send_gate`, M01-M04 clear-path gate tests should be added early with T222, M05-M10 remaining tests are minor coverage-strength gaps.
  - Deferred: none from the T221 review decision.
  - Rejected: none.
- Captain decision: no T221 repair pass is needed.
- Current Unique Task: T222 Local Fake Adapter.
- Current task package: `docs/tasks/M11_outbound_sendgate_feishu/T222_local_fake_adapter.md`.
- T222 must remain local-fake-only and non-platform:
  - may consume only `OutboundMessageRequest` records that are already sendable through explicit outbound human approval plus T221 gate `allowed`
  - may produce synthetic local fake-delivery records for tests and later adapter-contract validation
  - must not send messages, schedule actions, integrate Feishu/WeChat/webhook/email/browser/desktop adapters, add CLI/runtime send paths, call LLMs/external services, mutate stores/private artifacts, or treat gate `allowed` as real delivery
  - must not read `private/chat_history/` or commit private content
- Captain verification basis:
  - Reviewer reported no blocking issues.
  - Reviewer reported `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py` passed.
  - Reviewer reported targeted outbound schema + gate tests passed: 31 tests after `tzdata` was present.
  - Reviewer reported behavior schema + outbound schema + gate tests passed: 56 tests.
  - Reviewer noted the current full suite has 791 passed plus 16 pre-existing LLM/typer-dependent failures unrelated to T221; worker summary reported 811 passed in the worker environment with workspace temp/cache.
- M11 residual risks carried forward:
  - Gate `allowed` is not delivery.
  - T222 must keep fake delivery local and synthetic.
  - T223/T224 and M12 remain behind later task packages.
  - Windows named-timezone verification needs either `tzdata` or a documented UTC-only fallback.

## Captain Current State Override 2026-05-27 (T220 Review Decision)

- T220 review decision: `PASS`.
- T220 is complete as the schema-only outbound request boundary for M11.
- T220 review observation disposition:
  - Accepted: N01 forbidden metadata frozenset-union style is harmless cleanup debt, N02 full forbidden-key superset documentation can be clearer, N03 no payload max length is acceptable schema-only scope, N04 candidate-action id existence is not store-validated in schema-only scope, N05 approval/gate validators are correct defensive Pydantic v2 usage, N06 allowed-file note is a non-issue, N07 t220 pytest basetemp contents are workspace temp noise, M01 standalone approval/gate validator tests are minor, M02 `is_sendable()` true-path test should be added with T221 gate population, M03 outbound-specific forbidden-key tests should be expanded, M04 timestamp round-trip coverage is minor, M05 all channel values coverage is minor.
  - Deferred: none from the T220 review decision.
  - Rejected: none.
- Captain decision: no T220 repair pass is needed.
- Current Unique Task: T221 OutboundSendGate.
- Current task package: `docs/tasks/M11_outbound_sendgate_feishu/T221_outbound_send_gate.md`.
- T221 must remain gate-only and non-sending:
  - may implement deterministic gate policy over `OutboundMessageRequest`
  - may populate `OutboundRequestSendGate` with explicit allowed/blocked state and audit notes
  - may add focused tests for approval/gate validator edge cases and `is_sendable()` true path
  - must not send messages, schedule actions, integrate fake/Feishu/WeChat/platform adapters, add CLI/runtime send paths, call LLMs/external services, mutate stores/private artifacts, or treat `CandidateAction` review as send authorization
  - must not read `private/chat_history/` or commit private content
- Captain verification basis:
  - Reviewer reported no blocking issues.
  - Reviewer reported `python -m py_compile src/practical_chat_agent/core/models.py` passed.
  - Reviewer reported targeted T220 schema tests passed: 11 tests.
  - Reviewer reported combined behavior schema + outbound schema tests passed: 36 tests.
  - Worker summary reports full-suite verification passed with workspace temp/cache: 791 tests.
- M11 residual risks carried forward:
  - `OutboundMessageRequest` is now a contract, not delivery infrastructure.
  - `channel_preference` remains data-only and is not an adapter target.
  - T221 must make allowed/blocked gate decisions auditable without implementing delivery.
  - Fake adapter, Feishu adapter, WeChat adapter, review card UX, scheduler behavior, and platform failure recovery remain later tasks.

## Captain Current State Override 2026-05-27 (T214 Review Decision / M10 Gate)

- T214 review decision: `PASS`.
- T214 is complete as the behavior safety evaluation task for M10.
- M10 gate decision: `Gate M10 Allow`.
- M10 review artifact: `docs/review/M10_review.md`.
- T214 review observation disposition:
  - Accepted: N01 conflict-handling limitation is conservative scope/design, N02 repeated-review history-count repair is minor test-strength debt outside eval-only scope, N03 CLI path metadata remains accepted offline convention risk, N04 supplementary eval reading of README/02 is harmless, N05 temp/cache cleanup evidence is cosmetic, M01 missing explicit boundary-sensitive draft-enrichment scenario is minor traceability debt, M02 policy-disallowed scenario could trace code more explicitly but is non-blocking.
  - Deferred: none from the T214 review decision.
  - Rejected: none.
- Captain decision: no T214 repair pass is needed.
- Current Unique Task: T220 OutboundMessageRequest Schema.
- Current task package: `docs/tasks/M11_outbound_sendgate_feishu/T220_outbound_message_request_schema.md`.
- T220 must remain schema-only and non-sending:
  - may define a separate `OutboundMessageRequest` contract and tests
  - may document how reviewed `CandidateAction` can be referenced as evidence only
  - must not send messages, schedule actions, integrate platforms, call LLMs, mutate stores, add runtime loops, or treat `CandidateAction` approval as send authorization
  - must not read `private/chat_history/` or commit private content
- Captain verification basis:
  - Reviewer reported no blocking issues.
  - T214 eval reports required py_compile passed.
  - T214 eval reports targeted behavior tests passed: 58 tests.
  - T214 eval reports full-suite verification passed: 780 tests.
- M10 residual risks carried forward:
  - `CandidateAction.status="approved"`, `review_state="reviewed"`, and `is_runtime_visible()` must not be interpreted as send/schedule/platform/runtime authorization.
  - CLI path metadata and default in-place overwrite remain accepted offline conventions, not outbound-ready operational UX.
  - M10 does not cover platform delivery, notification UX, send audit UX, adapter failure recovery, or real scheduling.

## Captain Current State Override 2026-05-25 (T213 Review Decision)

- T213 review decision: `PASS`.
- T213 is complete as the manual CandidateAction review CLI task for M10.
- T213 review observation disposition:
  - Accepted: N01 Captain-authored T212 close-out governance diffs are established convention noise, N02 safe `input_path` / `output_path` stdout follows prior offline CLI convention, N03 T212 reviewer explanation in the working tree is prior reviewer/Captain artifact noise, N04 default in-place overwrite follows existing review-CLI convention and is low risk for offline workflow, N05 `_apply_decision` type suppression is cosmetic typing debt, M01 missing CLI freeze/archive/reject smoke tests are minor, M02 missing repeated-review history-count test is minor, M03 missing CLI reject/freeze/archive round-trip tests are minor.
  - Deferred: none.
  - Rejected: none.
- Captain decision: no T213 repair pass is needed.
- Current Unique Task: T214 Behavior Safety Eval.
- Current task package: `docs/tasks/M10_behavior_planner/T214_behavior_safety_eval.md`.
- T214 must remain evaluation-only and non-executing:
  - may inspect T210-T213 implementation, task packages, reviews, worker summaries, docs, and tests
  - may run local read-only commands/tests and create a committed milestone evaluation report
  - must not modify implementation code, schemas, CLIs, services, tests, fixtures, runtime wiring, or private artifacts
  - must not send messages, schedule actions, integrate platforms, call LLMs, mutate memory/ContactSkill/RelationshipState/approved stores/private artifacts, or treat candidate approval as outbound authorization
  - must not read `private/chat_history/` or commit private content
- Captain verification basis:
  - Reviewer reported no blocking issues.
  - Worker summary reports `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py src/practical_chat_agent/app/main.py` passed.
  - Worker summary reports targeted behavior tests passed: 58 tests.
  - Worker summary reports full-suite verification passed with workspace temp/cache: 780 tests.
- No new deferred T213 risk is opened. Existing project-wide review-only/outbound-gate risks remain active.

## Captain Current State Override 2026-05-25 (T212 Review Decision)

- T212 review decision: `PASS`.
- T212 is complete as the deterministic draft-enrichment task for M10.
- T212 review observation disposition:
  - Accepted: N01 reviewer explanation/worker summary allowed-files overrun is established convention noise, N02 static draft literals keyed by `BehaviorActionType` are acceptable for deterministic scope and forward-compatible `reply_follow_up_draft` / `topic_suggestion` entries are harmless, N03 unreachable fallback with `pragma: no cover` is cosmetic defensive code, N04 `model_copy(update=...)` without revalidation is acceptable because the only change is optional `draft_text` on an already validated payload, N05 overwriting existing `draft_text` is acceptable for initial-enrichment scope, M01 existing-draft overwrite mapping test gap is minor, M02 pipeline coverage for unsupported-but-available draft families is minor, M03 idempotence test gap is minor.
  - Deferred: none.
  - Rejected: none.
- Captain decision: no T212 repair pass is needed.
- Current Unique Task: T213 CandidateAction Review CLI.
- Current task package: `docs/tasks/M10_behavior_planner/T213_candidate_action_review_cli.md`.
- T213 must remain manual-review-only and non-executing:
  - may review enriched `CandidateAction` records and set status/review metadata to approve/reject/freeze/archive
  - must preserve T210/T211/T212 invariants: `human_review_required=True`, `auto_send_allowed=False`, `platform_execution_allowed=False`, `scheduler_allowed=False`, `platform_target=None`
  - must not send messages, schedule actions, integrate platforms, call LLMs, mutate memory/ContactSkill/RelationshipState/approved stores/private artifacts, add runtime loops, or treat approval as outbound authorization
  - must not read `private/chat_history/` or commit private content
- Captain verification basis:
  - Reviewer reported `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py` passed.
  - Reviewer reported `pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py -q` passed: 48 tests.
  - Worker summary reports full-suite verification passed with workspace temp/cache: 770 tests.
- No new deferred T212 risk is opened. Existing project-wide review-only/outbound-gate risks remain active.

## T213 Worker Completion Record

- T213 is the CandidateAction review CLI task for M10.
- Worker must not mark T213 as complete in `docs/04_task_board.md`; only the Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/services/behavior_planner.py`
  - `src/practical_chat_agent/app/main.py`
  - `tests/test_behavior_rule_planner.py`
  - `tests/test_behavior_review_cli.py`
  - `docs/data_contracts/behavior_planner_contract.md`
  - `docs/worker_summary/T213_worker_summary.md`
  - `docs/07_handoff.md`
- Review design:
  - `CandidateActionReviewService.review_candidate()` accepts a validated `CandidateAction` or stable mapping.
  - Supported decisions are `approve`, `reject`, `freeze`, and `archive`.
  - Reviewer id is required.
  - The service returns a new reviewed object and does not mutate the input.
  - Review updates `status`, `review_metadata.review_state`, `reviewed_by_human`, `last_decision`, `last_reviewed_at`, `last_reviewer_id`, `history`, and optional `decision_notes`.
  - Review preserves payload draft text, supporting refs, risk flags, policy, action type, and all no-send/no-platform/no-scheduler invariants.
- CLI design:
  - `chat-behavior-review-action` reads one `CandidateAction` JSON file, applies the review decision, and writes reviewed JSON.
  - Stdout includes only safe metadata: ids, action type, status, review metadata counts, and paths.
  - Stdout does not include full draft text.
- Verification status:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py src/practical_chat_agent/app/main.py` passed.
  - `pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py tests/test_behavior_review_cli.py -q -o cache_dir=artifacts\\t213_pytest_cache --basetemp=artifacts\\t213_pytest_basetemp` passed: 58 tests.
  - `pytest tests -q -o cache_dir=artifacts\\t213_pytest_cache --basetemp=artifacts\\t213_pytest_basetemp` passed: 780 tests.
- Explicit non-actions:
  - No message sending.
  - No real scheduler, timer, reminder, background job, automation, or recurring task.
  - No platform adapter or outbound send-gate behavior.
  - No LLM calls or external services.
  - No memory, ContactSkill, RelationshipState, approved-store, private-artifact, or unrelated review metadata mutation.
  - No task board update.

## T214 Worker Completion Record

- T214 is the behavior safety evaluation task for M10.
- Worker must not mark T214 as complete in `docs/04_task_board.md`; only the Captain may do so after review.
- Files changed:
  - `docs/review/T214_behavior_safety_eval.md`
  - `docs/worker_summary/T214_worker_summary.md`
  - `docs/07_handoff.md`
- Evaluation verdict:
  - Gate recommendation: `Gate M10 Allow`.
  - T210-T213 is safe to accept as a review-only behavior-planner milestone.
  - This does not authorize sending, scheduling, platform execution, runtime autonomy, outbound requests, LLM/provider calls, or state mutation.
- Scope evaluated:
  - T210-T213 task packages, reviews, worker summaries, behavior-planner contract, implementation code, CLI code, and behavior tests.
  - No `private/chat_history/` content was read.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\core\models.py src\practical_chat_agent\services\behavior_planner.py src\practical_chat_agent\app\main.py` passed.
  - `pytest tests\test_behavior_schema.py tests\test_behavior_rule_planner.py tests\test_behavior_review_cli.py -q -o cache_dir=artifacts\t214_pytest_cache --basetemp=artifacts\t214_pytest_basetemp` passed: 58 tests.
  - `pytest tests -q -o cache_dir=artifacts\t214_pytest_cache --basetemp=artifacts\t214_pytest_basetemp` passed: 780 tests.
- Residual risks:
  - CLI stdout includes safe path metadata under the existing offline convention.
  - `chat-behavior-review-action` defaults to in-place overwrite when `--output` is omitted.
  - Later M11 work must not treat `CandidateAction.status="approved"`, `review_state="reviewed"`, or `is_runtime_visible()` as send/schedule/platform/runtime authorization.
  - Minor prior review test-strength gaps remain but do not block M10 review-only acceptance.
- Explicit non-actions:
  - No code, schema, service, CLI, test, fixture, config, or task-board change.
  - No message sending.
  - No scheduler, timer, reminder, background job, automation, or recurring task.
  - No platform adapter, webhook, browser/desktop automation, email, Feishu, or WeChat integration.
  - No LLM calls, embeddings, vector DB, Mem0/Zep, or external service.
  - No memory, ContactSkill, RelationshipState, approved-store, or private-artifact mutation.

## Captain Current State Override 2026-05-25 (T211 Review Decision)

- T211 review decision: `PASS`.
- T211 is complete as the deterministic rule-engine task for M10.
- T211 review observation disposition:
  - Accepted: N01 reviewer explanation allowed-files overrun is established convention noise and worker summary is allowed/conventional, N02 truncated SHA-1 deterministic ids are acceptable for the current offline single-user workflow, N03 overlap between boundary-trigger and proactive-blocking flags is intentional conservative behavior, N04 `contact_id=None` fallback to `user_id` is acceptable for non-contact-targeted candidates, N05 `casefold()` normalization is acceptable with documented safe label expectations, M01 label-only `memory_review_prompt` test gap is minor, M02 per-blocking-flag coverage gap is minor, M03 contact fallback test gap is minor, M04 multi-boundary-flag single-note test gap is minor, M05 boundary-label-only trigger test gap is minor.
  - Deferred: none.
  - Rejected: none.
- Captain decision: no T211 repair pass is needed.
- Current Unique Task: T212 Proactive Draft Generator.
- Current task package: `docs/tasks/M10_behavior_planner/T212_proactive_draft_generator.md`.
- T212 must remain deterministic, local, draft-only, and review-only:
  - may enrich `CandidateActionPayload.draft_text` for existing safe `CandidateAction` records
  - must preserve T210/T211 invariants: `human_review_required=True`, `auto_send_allowed=False`, `platform_execution_allowed=False`, `scheduler_allowed=False`, `platform_target=None`
  - must not send messages, schedule actions, integrate platforms, call LLMs, mutate memory/ContactSkill/RelationshipState/approved stores/private artifacts, add CLI/runtime wiring, or bypass human review
  - must not read `private/chat_history/` or commit private content
- Captain verification basis:
  - Reviewer reported `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py` passed.
  - Reviewer reported `pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py -q` passed: 40 tests.
  - Worker summary reports full-suite verification passed with workspace temp/cache: 762 tests.
- No new deferred T211 risk is opened. Existing project-wide review-only/outbound-gate risks remain active.

## T212 Worker Completion Record

- T212 is the proactive draft generator task for M10.
- Worker must not mark T212 as complete in `docs/04_task_board.md`; only the Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/services/behavior_planner.py`
  - `tests/test_behavior_rule_planner.py`
  - `docs/data_contracts/behavior_planner_contract.md`
  - `docs/worker_summary/T212_worker_summary.md`
  - `docs/07_handoff.md`
- Draft-enrichment design:
  - `ProactiveDraftGenerator.enrich()` accepts a validated `CandidateAction` or stable mapping that validates to one.
  - The generator preserves `action_type`, `supporting_context_refs`, `risk_flags`, `policy`, `status`, and the no-send/no-platform/no-scheduler invariants.
  - Draft text is deterministic per action type and stays short, review-only, and non-committal.
  - Supported draft families:
    - `boundary_review_note`
    - `memory_review_prompt`
    - `relationship_check_in_draft`
    - `reply_follow_up_draft`
    - `topic_suggestion`
    - `do_nothing`
- Verification status:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py` passed.
  - `pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py -q -o cache_dir=artifacts\pytest_cache --basetemp=artifacts\t212_pytest_basetemp` passed: 48 tests.
  - `pytest tests -q -o cache_dir=artifacts\pytest_cache --basetemp=artifacts\t212_pytest_basetemp` passed: 770 tests.
- Explicit non-actions:
  - No send/schedule/platform/runtime wiring.
  - No LLM calls or external services.
  - No memory, ContactSkill, or RelationshipState mutation.
  - No task board update.

## Captain Current State Override 2026-05-25 (T210 Review Decision)

- T210 review decision: `PASS`.
- T210 is complete as the schema-only opening task for M10.
- T210 review observation disposition:
  - Accepted: N01 reviewer explanation allowed-files overrun is established convention noise, N02 worker-summary allowed-files overrun is established convention noise, N03/M03 missing explicit `access_token` / `api_key` tests are low-risk because the shared forbidden-key validator covers the full set, N04 `DistillationStatus` reuse is acceptable for the schema-first lifecycle, N05 duplicated safety invariant fields are acceptable independent-safety redundancy, M01 `max_candidates` boundary test gap is minor, M02 `AgentSelfState(contact_id=None)` round-trip gap is minor, M04 `review_notes` round-trip gap is minor.
  - Deferred: none.
  - Rejected: none.
- Captain decision: no T210 repair pass is needed.
- Current Unique Task: T211 Action Planner Rule Engine.
- Current task package: `docs/tasks/M10_behavior_planner/T211_action_planner_rule_engine.md`.
- T211 must remain deterministic, local, candidate-only, and review-only:
  - may introduce a rule-engine service that emits zero or more `CandidateAction` records from `AgentSelfState`, safe refs, and approved/review-safe context signals
  - must preserve T210 invariants: `human_review_required=True`, `auto_send_allowed=False`, `platform_execution_allowed=False`, `scheduler_allowed=False`, `platform_target=None`
  - must not send messages, schedule actions, integrate platforms, call LLMs, mutate memory/ContactSkill/RelationshipState/approved stores/private artifacts, add runtime/CLI wiring, or bypass human review
  - must not read `private/chat_history/` or commit private content
- Captain verification basis:
  - Reviewer reported `python -m py_compile src/practical_chat_agent/core/models.py` passed.
  - Reviewer reported `pytest tests/test_behavior_schema.py -q` passed: 25 tests.
  - Reviewer reported `pytest tests/ -q` had no T210-related regressions; the reported unrelated full-suite failures were pre-existing missing-`typer` CLI environment failures in that review run.
  - Worker summary reports a separate full-suite run with workspace temp/cache passed: 747 tests.
- No new deferred T210 risk is opened. Existing project-wide review-only/outbound-gate risks remain active.

## Captain Current State Override 2026-05-24 (T203 Review Decision)

- T203 review decision: `PASS`.
- T203 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun is established convention noise, N02 `docs/worker_summary/T203_worker_summary.md` is established worker-summary convention noise, N03 T203 reuses the T202 eval shape rather than importing the T202 runner directly which is acceptable for a spike, N04 documentation/test-count discrepancies are harmless, N05 English keyword memory-type inference is acceptable for spike scope, M01 no `limit=0` test is acceptable for spike scope, M02 no empty-string `contact_id` test is acceptable for spike scope, M03 no direct `ImportError` simulation is acceptable because safe not-configured behavior is covered, M04 non-`Exception` propagation is correct behavior.
  - Deferred: none.
  - Rejected: none.
- T203 is complete as the optional Mem0 adapter spike task for M9.
- M9 completion status: M9 is complete at the task level with Gate M9 `Allow`.
- Current Unique Task: T210 Behavior Schema.
- Current task package: `docs/tasks/M10_behavior_planner/T210_behavior_schema.md`.
- T210 must remain schema-only and draft-only:
  - define `AgentSelfState`, `BehaviorPolicy`, and `CandidateAction` or equivalently named behavior-planner contracts
  - no message sending, send-gate bypass, platform adapter, real scheduler, or background job
  - no memory write-back, ContactSkill mutation, relationship-state mutation, or automatic learning
  - no raw transcript reads or private chat content in committed fixtures/docs/tests
  - no planner execution beyond model validation and contract examples
- Captain verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/memory_retrieval.py src/practical_chat_agent/services/optional_mem0_adapter.py src/practical_chat_agent/services/chat_context.py` passed.
  - After setting `TEMP`/`TMP` to a workspace temp directory, `pytest tests/test_optional_mem0_adapter_spike.py tests/test_memory_retriever_contract.py tests/test_local_approved_store_retriever.py tests/test_memory_retriever_eval_set.py -q` passed: 181 tests, with only `.pytest_cache` permission warnings.
  - After setting `TEMP`/`TMP` to a workspace temp directory, `pytest tests/ -q` passed: 722 tests, with only `.pytest_cache` permission warnings.
- No T203 repair pass is needed because no blocking issue or deferred warning exists.

## T203 Worker Completion Record

- T203 is the optional Mem0 adapter spike task for M9.
- Worker must not mark T203 as complete in `docs/04_task_board.md`; only the Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/services/optional_mem0_adapter.py` (new)
  - `tests/test_optional_mem0_adapter_spike.py` (new)
  - `docs/spikes/T203_mem0_adapter_spike.md` (new)
  - `docs/data_contracts/memory_retriever_contract.md`
  - `docs/07_handoff.md`
- Adapter design:
  - `Mem0AdapterRetriever` implements `MemoryRetriever` protocol (runtime `isinstance` check passes).
  - Accepts a `mem0` cloud API key. If absent or empty, every `retrieve()` returns `status="not_configured"`.
  - If `mem0` package is not installed, returns `not_configured` via lazy import. No hard dependency.
  - Uses `mem0.Memory.search(query, user_id, limit)` when a query is provided.
  - Uses `mem0.Memory.get_all(user_id)` when no query is provided.
  - Converts Mem0 results to `MemoryHit` with `source="external_adapter"`.
  - Memory type inference via keyword heuristics (preference/relationship/reflection/fact).
  - Score from Mem0's `score` field, defaulting to 0.5 when absent.
  - Evidence refs fabricated as `["mem0:<id>"]` since Mem0 lacks structured evidence refs.
  - Does not call `add()`, `delete()`, `update()`, or any write method on the Mem0 client.
  - Test injection via `_client` parameter (documented prototype placeholder for the spike).
- Spike findings:
  - The `MemoryRetriever` protocol is flexible enough for external adapters.
  - Graceful degradation works cleanly when package or config is absent.
  - Key limitations: no review/approval enforcement, heuristic type inference, synthetic evidence refs, ordering depends on Mem0.
  - Recommendation: adapter is technically feasible but should remain optional/off-by-default until review integration, evidence mapping, SDK pinning, and error recovery are addressed.
- Relationship to existing code:
  - No changes to `models.py`, `memory_retrieval.py`, `chat_context.py`, or any runtime/service code.
  - No ReplyPlanner, policy-engine, send-gate, or outbound behavior changes.
  - No ChatContextAssembler modifications.
  - `LocalApprovedStoreRetriever` is unchanged and remains the primary retriever.
- Explicit non-actions:
  - No `mem0` or `mem0ai` dependency added to any requirements file.
  - No vector DB, embedding, or external provider calls in committed code.
  - No auto-write or runtime mutation of memories or store files.
  - No raw chat transcript retrieval path introduced.
  - No ChatContext wiring, planner, policy, or send behavior changes.
  - No production adoption claim.

## Captain Current State Override 2026-05-24 (T202 Review Decision)

- T202 review decision: `PASS`.
- T202 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun is established convention noise, N02 `docs/worker_summary/T202_worker_summary.md` is established worker-summary convention noise, N03 eval coverage on `LocalApprovedStoreRetriever` rather than context-bound `LocalMemoryRetriever` is acceptable for the reusable protocol eval baseline, M01 no dedicated empty-string query case is acceptable because T201 covers it and T202 covers adjacent query boundaries, M02 uniform excluded-record scores are acceptable because exclusion is the behavior under test.
  - Deferred: none.
  - Rejected: none.
- T202 is complete as the retrieval eval set task for M9.
- Current Unique Task: T203 Optional Mem0 Adapter Spike.
- Current task package: `docs/tasks/M9_memory_retrieval_layer/T203_optional_mem0_adapter_spike.md`.
- T203 must remain optional and spike-only:
  - no required Mem0 dependency
  - no production external-memory adoption claim
  - no provider or external service calls in committed tests
  - no private chat content or raw transcript indexing
  - no auto-write, approved-store mutation, or hidden memory update
  - no ChatContext wiring, ReplyPlanner/policy/send behavior change, or platform integration
  - any adapter code must sit behind `MemoryRetriever.retrieve()` / `MemoryRetrieverResult` and gracefully degrade when unavailable
- Captain verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/memory_retrieval.py src/practical_chat_agent/services/chat_context.py` passed.
  - After setting `TEMP`/`TMP` to a workspace temp directory, `pytest tests/test_memory_retriever_contract.py tests/test_local_approved_store_retriever.py tests/test_memory_retriever_eval_set.py -q` passed: 136 tests, with only `.pytest_cache` permission warnings.
  - After setting `TEMP`/`TMP` to a workspace temp directory, `pytest tests/ -q` passed: 677 tests, with only `.pytest_cache` permission warnings.
- No T202 repair pass is needed because no blocking issue or deferred warning exists.

## T202 Worker Completion Record

- T202 is the retrieval eval set task for M9.
- Worker must not mark T202 as complete in `docs/04_task_board.md`; only the Captain may do so after review.
- Files changed:
  - `tests/test_memory_retriever_eval_set.py` (new)
  - `docs/data_contracts/memory_retriever_eval_set.md` (new)
  - `docs/data_contracts/memory_retriever_contract.md`
  - `docs/07_handoff.md`
- Eval set design:
  - `RetrievalEvalCase` dataclass defining eval case contract: case_id, description, contact_id, query, limit, expected_status, expected_hit_memory_ids, expected_min/max_hits, forbidden_memory_ids, expected_candidate_count, tags.
  - `build_synthetic_eval_store()` producing a deterministic `MemoryFactStoreFile` with 15 records: 6 approved + 6 excluded for synth_alice, 3 approved for synth_bob.
  - `run_eval_case()` generic eval runner that asserts expectations on any `MemoryRetriever` through the public `retrieve()` surface.
  - 19 eval cases (E01–E19) covering relevant hits, all 6 non-runtime-ready exclusion types, query matching (single/multi/miss/case-insensitive/substring), deterministic ordering, limit enforcement, cross-contact isolation, unknown-contact boundary, and combined exclusions.
  - 8 contract boundary tests: source provenance, score boundedness, evidence refs, memory type validity, hit/result JSON round-trip, store immutability.
  - 6 coverage audit tests: required tags present, all excluded types covered, multiple contacts, deterministic store build, ordering case requirements, expected record count.
  - 1 reuse demonstration: `run_eval_case()` works through the `MemoryRetriever` protocol interface.
- Synthetic store content:
  - synth_alice approved (6): procedural/0.90, relationship/0.85, episodic/0.75, semantic/0.70, reflection/0.60, procedural/0.50.
  - synth_alice excluded (6): candidate, rejected, frozen, archived, not-human-reviewed, failed-evidence-validation.
  - synth_bob approved (3): semantic/0.80, procedural/0.70, relationship/0.65.
- Relationship to existing code:
  - No changes to `models.py`, `memory_retrieval.py`, `chat_context.py`, or any runtime/service code.
  - No ReplyPlanner, policy-engine, send-gate, or outbound behavior changes.
  - No ChatContextAssembler modifications.
  - Tests consume retrievers through the public `MemoryRetriever` protocol only.
- Explicit non-actions:
  - No retrieval algorithm or scoring changes.
  - No vector DB, Mem0/Zep adapter, or external memory dependency introduced.
  - No auto-write or runtime mutation of memories or store files.
  - No raw chat transcript retrieval path introduced.
  - No provider calls, embedding calls, or external services added.

## Captain Current State Override 2026-05-24 (T201 Review Decision)

- T201 review decision: `PASS`.
- T201 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun is established convention noise, N02 `docs/worker_summary/T201_worker_summary.md` is established worker-summary convention noise, N03 per-call store-file reads without caching are acceptable for current offline-first single-user workflow, M01 `limit=0` test is a harmless boundary guard, M02 concurrent-read tests are outside current single-user offline scope.
  - Deferred: none.
  - Rejected: none.
- T201 is complete as the local approved-store retriever task for M9.
- Current Unique Task: T202 Retrieval Eval Set.
- Current task package: `docs/tasks/M9_memory_retrieval_layer/T202_retrieval_eval_set.md`.
- T202 must stay evaluation-only and synthetic:
  - use only synthetic/redacted committed data
  - exercise retrievers through `MemoryRetriever.retrieve()` and `MemoryRetrieverResult`
  - cover relevant hits, exclusions, query behavior, ordering, and boundary behavior
  - avoid private chat content, raw transcript reads, vector DB, Mem0/Zep, embedding/provider calls, ChatContext wiring, planner/policy changes, send behavior, and external services
- Captain verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/memory_retrieval.py src/practical_chat_agent/services/chat_context.py` passed.
  - Initial pytest target runs failed in setup because the default Windows temp directory was not accessible in this sandbox.
  - After setting `TEMP`/`TMP` to a workspace temp directory, `pytest tests/test_local_approved_store_retriever.py -q` passed: 63 tests.
  - After setting `TEMP`/`TMP` to a workspace temp directory, `pytest tests/test_memory_retriever_contract.py tests/test_local_approved_store_retriever.py -q` passed: 103 tests.
  - After setting `TEMP`/`TMP` to a workspace temp directory, `pytest tests/ -q` passed: 644 tests, with only `.pytest_cache` permission warnings.
- No T201 repair pass is needed because no blocking issue or deferred warning exists.

## T201 Worker Completion Record

- T201 is the local approved-store retriever task for M9.
- Worker must not mark T201 as complete in `docs/04_task_board.md`; only the Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/services/memory_retrieval.py`
  - `tests/test_local_approved_store_retriever.py` (new)
  - `docs/data_contracts/memory_retriever_contract.md`
  - `docs/07_handoff.md`
- Class added:
  - `LocalApprovedStoreRetriever` in `services/memory_retrieval.py`
- Retriever design:
  - Implements the T200 `MemoryRetriever` protocol (runtime `isinstance` check passes).
  - Reads from a `MemoryFactStoreFile` (or directory containing one) on each `retrieve()` call. No caching, no external calls.
  - Filters to only approved/runtime-ready records: `is_runtime_ready() == True`, `subject_id == contact_id`, `evidence_validation_status == "passed"`.
  - Candidate, rejected, frozen, archived, not-human-reviewed, and wrong-contact records never appear in hits.
  - `MemoryHit.score` derived from `MemoryFactCandidate.importance`.
  - `MemoryHit.source` is always `"approved_store"`.
  - `MemoryHit.memory_type` mapped via `to_runtime_memory_type()`.
  - Query matching: simple case-insensitive substring on claim text.
  - Sorting: importance desc, confidence desc, memory_id asc (deterministic).
  - Limit enforced after sorting.
  - `not_configured` status when store file not found; `error` when unparseable.
- Relationship to existing code:
  - `models.py` is unchanged; no new models or types were added.
  - `chat_context.py` is unchanged; no ChatContext wiring.
  - No ReplyPlanner, policy-engine, send-gate, or outbound behavior changes.
  - Reuses `MemoryFactCandidate.to_runtime_memory_type()` for type mapping.
- Verification:
  - Compile passed for models.py, memory_retrieval.py, chat_context.py.
  - T201 test suite: 63 tests covering protocol conformance, approved record retrieval, excluded records (candidate/rejected/frozen/archived/not-reviewed/failed-validation/wrong-contact), query filtering, limit enforcement, source provenance, score derivation, memory-type mapping, evidence-ref preservation, deterministic ordering, store path resolution, edge cases (not found, invalid, empty), notes, contract boundary assertions, JSON round-trip, candidate count.
  - Full existing test suite: 644 tests passed (63 new + 581 existing), no regressions.
- Explicit non-actions:
  - No vector DB, Mem0/Zep adapter, or external memory dependency introduced.
  - No auto-write or runtime mutation of memories or store files.
  - No raw chat transcript retrieval path introduced.
  - No ReplyPlanner, policy-engine, send-gate, or outbound behavior changes.
  - No ChatContextAssembler modifications.
  - No provider calls, embedding calls, or external services added.
  - No models.py changes.
  - No chat_context.py changes.

## Captain Current State Override 2026-05-24 (T200 Review Decision)

- T200 review decision: `PASS`.
- T200 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun is established convention noise, N02 `docs/worker_summary/T200_worker_summary.md` is established worker-summary convention noise, N03 free-form `MemoryHit.source` is acceptable because convention values are documented and future adapter extensibility is intentional, M01 guarded assertions in two adapter tests are minor test-strength observations covered by a direct hit-producing setup test.
  - Deferred: none.
  - Rejected: none.
- T200 is complete as the contract-first MemoryRetriever opening task for M9.
- Current Unique Task: T201 Local Approved-Store Retriever.
- Current task package: `docs/tasks/M9_memory_retrieval_layer/T201_local_approved_store_retriever.md`.
- T201 must implement the T200 protocol locally and approved-only:
  - return `MemoryHit` items with `source="approved_store"`
  - consume only approved/runtime-ready local store records
  - preserve evidence refs
  - exclude candidate/rejected/frozen/archived/not-human-reviewed records
  - avoid vector DB, Mem0/Zep, embedding/provider calls, raw transcript reads, auto-write, planner/policy changes, and outbound behavior
- Captain verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/memory_retrieval.py src/practical_chat_agent/services/chat_context.py` passed.
  - `pytest tests/test_memory_retriever_contract.py -q` passed: 40 tests.
  - `pytest tests/ -q` passed after setting `TEMP`/`TMP` to a workspace temp directory: 581 tests, with only `.pytest_cache` permission warnings. The first full-suite attempt failed in fixture setup because the default Windows temp directory was not accessible in this sandbox.
- No T200 repair pass is needed because no blocking issue or deferred warning exists.

## Captain Current State Override 2026-05-24 (T200 Worker Completion)

- T200 is the MemoryRetriever interface task for M9.
- Worker must not mark T200 as complete in `docs/04_task_board.md`; only the Captain may do so after review.
- T200 has since been accepted by reviewer and Captain with `PASS`; Current Unique Task is now T201.

## T200 Worker Completion Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/memory_retrieval.py`
  - `tests/test_memory_retriever_contract.py` (new)
  - `docs/data_contracts/memory_retriever_contract.md` (new)
  - `docs/07_handoff.md`
- Model/type names added:
  - `MemoryRetrieverStatus` (Literal: "success", "not_configured", "error")
  - `MemoryHit` (Pydantic BaseModel)
  - `MemoryRetrieverResult` (Pydantic BaseModel)
- Protocol/adapter added:
  - `MemoryRetriever` (typing.Protocol, runtime_checkable) in `services/memory_retrieval.py`
  - `convert_retrieval_result()` converter function in `services/memory_retrieval.py`
  - `LocalMemoryRetriever` adapter class in `services/memory_retrieval.py`
- Contract design:
  - `MemoryHit` is a thin, review-safe retrieval result with `hit_id`, `memory_id`, `fact`, `memory_type`, `score`, `evidence_refs`, and `source`. It deliberately carries no raw transcript content, no embedding vectors, and no write/mutation capability.
  - `MemoryRetrieverResult` is the protocol-level envelope with `status`, `contact_id`, `hits`, `candidate_count`, and `notes`.
  - `MemoryRetriever` protocol defines `retrieve(*, contact_id, query=None, limit=8) -> MemoryRetrieverResult`. Implementations must return only approved, review-safe content, never read raw transcripts, and never auto-write or mutate memory.
  - `LocalMemoryRetriever` wraps `MemoryRetrievalService` and implements the protocol via `with_context()` + `retrieve()`.
  - `convert_retrieval_result()` converts service-level `MemoryRetrievalResult` to the protocol-level `MemoryRetrieverResult` contract.
- Relationship to existing code:
  - `MemoryHit` is additive; `ChatContext.memory_hits` (list[MemoryFact]) is unchanged.
  - `MemoryRetrieverResult` parallels but does not replace `MemoryRetrievalResult`.
  - `ChatContextAssembler` is not modified.
  - No ChatContext fields, ReplyPlanner behavior, policy engine, or outbound paths are changed.
- Verification:
  - Compile passed for models.py, memory_retrieval.py, chat_context.py.
  - T200 test suite: 40 tests covering MemoryHit validation, MemoryRetrieverResult validation, protocol conformance (isinstance), LocalMemoryRetriever with/without context, conversion fidelity, limit, source provenance, score derivation, evidence ref preservation, note carry-through, context isolation, JSON round-trip, contract boundary assertions.
  - Full existing test suite: 560 tests passed (40 new + 520 existing), no regressions.
- Explicit non-actions:
  - No vector DB, Mem0/Zep adapter, or external memory dependency introduced.
  - No auto-write or runtime mutation of memories.
  - No raw chat transcript retrieval path introduced.
  - No ReplyPlanner or policy-engine behavior changes.
  - No ChatContextAssembler modifications.
  - No provider calls, embedding calls, or external services added.

## Captain Current State Override 2026-05-24 (T195 Review Decision)

- T195 review decision: `PASS_WITH_WARNINGS`.
- T195 warning disposition:
  - Accepted: W01 worker milestone-review/handoff mechanism claim was factually wrong and is corrected here, W04 `docs/for_human/T195_review_explanation.md` allowed-files overrun is treated as low-risk convention noise.
  - Deferred: W02 relationship dimension-change values present in `ChatContext` but unused by `ReplyPlanner` / `ReplyPlanPolicyEngine`, W03 relationship guidance reaching summary/retrieval-note surfaces is informational only and does not create semantic consumption.
  - Rejected: none.
- T195 is complete as the evaluation-only milestone task for M8.
- M8 completion status: All six M8 tasks (T190 schema, T191 signal extraction, T192 delta generation, T193 delta review, T194 compact context, T195 eval) are complete. M8 delivered the relationship-state pipeline and its evaluation, but not semantic planner consumption of relationship deltas.
- Relationship context impact summary: The approved relationship context does NOT currently affect reply behavior. No code path consumes `ChatContext.relationship_context.deltas` for planner or policy decisions. Relationship guidance reaching summary or retrieval notes is informational only.
- Current Unique Task: T200 MemoryRetriever interface.
- Current task package: `docs/tasks/M9_memory_retrieval_layer/T200_memory_retriever_interface.md`.
- T200 must stay contract-first and local-only:
  - no vector DB or external adapter
  - no Mem0/Zep spike inside T200
  - no raw transcript retrieval
  - no auto-write memory behavior

## Captain Current State Override 2026-05-24 (T193 Review Decision)

- T193 review decision: `PASS_WITH_WARNINGS`.
- T193 warning disposition:
  - Accepted: N02 default input-file overwrite risk follows established review-CLI pattern, N04 `.claude/settings.json` workspace-artifact overrun.
  - Deferred: N01 no committed CLI-level integration tests, N03 no evidence pre-validation gate before approval, M01 no Typer-command test coverage, M02 no explicit empty-string note test.
  - Rejected: none.
- T193 is complete as the explicit relationship-delta review task for M8.
- Current Unique Task: T194 RelationshipState compact context.
- Current task package: `docs/tasks/M8_relationship_state/T194_relationship_state_context.md`.
- T194 must stay context-only and approval-gated:
  - no raw signal history injection
  - no RelationshipState auto-update
  - no send-behavior change
  - no reopening of delta review semantics
- T193/T194 boundary:
  - T193 records human review decisions on delta candidates.
  - T194 exposes compact approved relationship-state guidance only.
  - State application remains outside this task.

## Captain Current State Override 2026-05-24 (T192 Review Decision)

- T192 review decision: `PASS_WITH_WARNINGS`.
- T192 warning disposition:
  - Accepted: N01 heuristic `_MAGNITUDE_SCALE` / `_MIN_STRENGTH` defaults are acceptable for candidate-only scope, N02 max-strength aggregation is acceptable for current conservative scope, N03 `.claude/settings.json` workspace-artifact overrun, N04 `dimension_name` typing suppression is cosmetic debt, N05 `_DIRECTION_SIGN` string-key typing is functionally safe.
  - Deferred: M01 no committed test yet confirms unknown dimensions are skipped safely, M02 no committed test yet covers mixed known+unknown/stable direction sets, M04 no committed test yet covers the state-evidence-only deduplication edge case.
  - Rejected: none.
- T192 is complete as the conservative delta-generation task for M8.
- Current Unique Task: T193 Relationship review CLI.
- Current task package: `docs/tasks/M8_relationship_state/T193_relationship_review_cli.md`.
- T193 must stay review-only and auditable:
  - no auto-apply to `RelationshipState`
  - no unrelated memory/ContactSkill mutation
  - no send/platform integration
  - no dimension semantics rewrite
- T192/T193 boundary:
  - T192 generates candidate deltas only.
  - T193 records explicit human review decisions on those deltas.
  - State application remains outside this task.

## T192 Worker Completion Record

- Files changed:
  - `src/practical_chat_agent/services/feedback.py`
  - `tests/test_relationship_deltas.py` (new)
  - `docs/data_contracts/relationship_state_contract.md`
  - `docs/07_handoff.md`
- Service added:
  - `RelationshipDeltaGenerator` in `services/feedback.py` with `generate_from_signals()` method
- Delta generation design:
  - Consumes T191 `RelationshipSignal` records and a current `RelationshipState`.
  - Filters signals to those matching the state's `contact_id`.
  - Groups signals by `dimension_name`.
  - Requires consistent direction (all increase or all decrease) per dimension; contradictory, unknown, or stable directions are skipped.
  - Uses max signal strength as the effective delta magnitude, attenuated by `_MAGNITUDE_SCALE=0.2`.
  - Skips dimensions where max strength < `_MIN_STRENGTH=0.3`.
  - Recomputes `magnitude` as `abs(proposed_value - current_value)` rather than trusting signal strength directly.
  - Validates `direction` from actual proposed vs current values rather than blindly trusting signal direction.
  - Clamps proposed values to [0.0, 1.0]; skips dimensions where clamping produces no effective change.
  - Collects and deduplicates `evidence_refs` from all contributing signals; state evidence refs are not included.
  - Collects all `signal_id` values into `signal_refs`.
  - Generated deltas always have `status="candidate"`; no auto-approve or state mutation.
- Relationship to T191:
  - T191 signals are the only input surface.
  - The generator does not read raw feedback, raw chat history, or raw text.
  - Delta rationale contains only signal counts and strength values, never raw feedback text.
- Verification:
  - Compile passed for feedback.py.
  - T192 test suite: 26 tests covering clear signal-to-delta mapping, no-delta behavior, magnitude/direction consistency, evidence/signal ref preservation, boundary clamping, state immutability, delta candidate properties, multi-signal aggregation.
  - Full existing test suite: 488 tests passed (26 new + 462 existing), no regressions.
- Explicit non-actions:
  - No `RelationshipState` mutation, auto-approve, review CLI, or state application was added.
  - No LLM call, send/platform integration, scalar collapse, or raw-text dependency was added.
  - No `models.py` change was needed; T190 schemas were sufficient.

## T193 Worker Completion Record

- Files changed:
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `tests/test_relationship_review_cli.py` (new)
  - `docs/data_contracts/relationship_state_contract.md`
  - `docs/07_handoff.md`
- Service added:
  - `RelationshipDeltaReviewService` in `services/feedback.py` with `review_delta()` method.
- Service design:
  - Accepts a `RelationshipDeltaCandidate`, decision string, reviewer identity, and optional note.
  - Returns a *new* delta via `model_copy(deep=True)` 閳?the original delta is not mutated.
  - Validates decisions: `approve`, `reject`, `freeze`, `archive`. Case-insensitive, whitespace-tolerant.
  - Reuses existing `DistilledArtifactReviewDecision` / `DistilledArtifactReviewMetadata` patterns from T120/T163.
  - Appends a review decision to `review_metadata.history`, updates `status`, `review_state`, `reviewed_by_human`, `last_decision`, reviewer fields, and `updated_at`.
  - Approved deltas with `reviewed_by_human=True` and `last_decision="approved"` report `is_runtime_ready() == True`.
  - Evidence refs, signal refs, dimension changes, and delta rationale are preserved unchanged.
  - All-or-nothing review: all dimensions in a delta are reviewed together.
- CLI command added:
  - `relationship-review-delta` with `--input`, `--output` (optional), `--decision`, `--reviewer`, `--note` (optional).
  - Reads a delta JSON file, applies the review decision, writes the updated delta (defaults to overwriting input).
  - Outputs a safe JSON summary: action, decision, delta_id, contact_id, status, is_runtime_ready, dimension count, evidence/signal ref counts, and review metadata.
- Relationship to T192:
  - T192 generates candidate deltas; T193 reviews them.
  - The `relationship-review-delta` CLI consumes the delta JSON format produced by T192.
  - No state application, no auto-approve.
- Verification:
  - Compile passed for main.py, feedback.py, models.py.
  - T193 test suite: 22 tests covering approve/reject/freeze/archive, invalid decisions, case-insensitive handling, runtime-ready gating, evidence/signal/dimension preservation, deep-copy immutability, review metadata updates, history accumulation, multi-dimension all-or-nothing review.
  - Full existing test suite: 510 tests passed (22 new + 488 existing), no regressions.
- Explicit non-actions:
  - No `RelationshipState` mutation or auto-apply.
  - No unrelated memory/ContactSkill mutation.
  - No send/platform integration.
  - No dimension semantics rewrite or partial-approval model.
  - No `models.py` change was needed; T190 schemas were sufficient.

## T194 Worker Completion Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/chat_context.py`
  - `tests/test_relationship_context.py` (new)
  - `docs/data_contracts/relationship_state_contract.md`
  - `docs/07_handoff.md`
- Models added:
  - `ApprovedRelationshipDeltaBrief` 閳?compact summary of one approved delta (dimension changes, summary, evidence refs; no signal refs or review metadata).
  - `ApprovedRelationshipContext` 閳?container with status, source path, contact_id, deltas, and notes.
  - `ChatContext.relationship_context` 閳?additive field, independent from `approved_store_context`, `approved_patch_context`, and `derived_brief_context`.
- Assembler logic added:
  - `__init__` parameter: `approved_relationship_delta_path` (optional `Path` to a directory of delta JSON files).
  - `_load_approved_relationship_context()` 閳?reads delta JSON files, validates each as `RelationshipDeltaCandidate`, filters for runtime-ready only (approved + human-reviewed + matching contact_id), builds compact briefs.
  - `_try_load_runtime_ready_delta()` 閳?per-file try-parse and filter helper.
  - `_build_relationship_context_notes()` 閳?adds relationship delta hints to `memory_retrieval_notes`.
  - Relationship context info included in `_build_summary()` when loaded.
- Context design:
  - Only `status="approved"` AND `reviewed_by_human=True` AND `last_decision="approved"` deltas enter context.
  - Candidate, rejected, frozen, archived, not-human-reviewed, and wrong-contact deltas are excluded.
  - `signal_refs`, `review_metadata.history`, reviewer identities, and review timestamps are stripped from briefs.
  - `delta_summary` capped at 200 characters; `evidence_refs` limited to 6.
  - No `RelationshipState` mutation, no send-behavior change, no raw signal/review leakage.
- Verification:
  - Compile passed for models.py and chat_context.py.
  - T194 test suite: 31 tests covering load success, dimension preservation, multi-dimension deltas, fallback behavior (not_configured, path_missing, no_runtime_ready, contact mismatch, not-human-reviewed), no raw content leakage, coexistence with existing context paths, retrieval notes, summary inclusion, determinism, and no disk writes.
  - Full existing test suite: 541 tests passed (31 new + 510 existing), no regressions.
- Explicit non-actions:
  - No raw signal history or review metadata in context.
  - No `RelationshipState` mutation or auto-update.
  - No send-behavior change or outbound integration.
  - No delta review semantics reopened.
  - No dimension semantics rewrite.
  - No ContactSkill, MemoryFact, or approved store modification.

## T195 Worker Completion Record

- Files changed:
  - `docs/review/T195_milestone_review.md` (new)
  - `docs/for_human/T195_review_explanation.md` (new)
  - `docs/07_handoff.md`
- Evaluation method:
  - Traced end-to-end data flow from `ApprovedRelationshipContext` (T194) through `ChatContextAssembler` 閳?`ReplyPlanPolicyEngine` 閳?`ReplyPlanner` 閳?`ReplyPlan`.
  - Analyzed all code paths where relationship context content can affect reply behavior.
- Captain correction:
  - Reviewer verification showed the originally claimed keyword-match mechanism was incorrect. The authoritative findings below reflect the corrected code-path analysis.
- Key findings:
  - **No current behavioral impact**: Approved relationship context does not currently change reply behavior in the implementation under review.
  - **Dimension-level nuance is absent**: even though dimension changes are present in context, no current code path maps them to planner or policy behavior.
  - **Claimed note-keyword trigger is not real**: relationship-context notes are English, policy sensitive-keyword checks are Chinese substring matches, and the policy engine only inspects `memory_retrieval_notes[:3]`; the claimed trigger path does not fire.
  - **No semantic consumer**: `ApprovedRelationshipDeltaBrief.dimension_changes`, `delta_summary`, and `evidence_refs` are present in `ChatContext.relationship_context`, but no planner or policy code path reads them for decision-making.
  - **Summary is informational only**: `ChatContext.summary` includes relationship guidance text, but `ReplyPlanSourceContext.chat_context_summary` is not read by any decision point.
- Verdict: `PASS_WITH_WARNINGS`:
  - W01: Worker milestone-review/handoff mechanism claim was incorrect and required captain correction.
  - W02: Dimension-change values present in ChatContext but unused by reply planner/policy.
  - W03: Summary/retrieval-note relationship guidance is observational, not behavioral.
- Explicit non-actions:
  - No code changes. Verified: no files under `src/` or `tests/` were modified.
  - No private artifacts committed.
  - No state application or context mutation.
  - No new runtime semantics or context wiring.

## Captain Current State Override 2026-05-24 (T191 Review Decision)

- T191 review decision: `PASS_WITH_WARNINGS`.
- T191 warning disposition:
  - Accepted: N01 handoff test-count mismatch is a documentation accuracy issue, N02 `.claude/settings.json` workspace-artifact overrun, N04 static rule-table typing suppression is acceptable for the current deterministic extractor scope, N05 sparse coverage over three dimensions is intentional and conservative.
  - Deferred: N03 `RelationshipSignal` lacks an `updated_at` field, M01 no committed test yet exercises an approved `RelationshipSignal` runtime-ready path, M02 no committed test yet covers `signal_id` format or non-emptiness.
  - Rejected: none.
- T191 is complete as the conservative signal-extraction task for M8.
- Current Unique Task: T192 RelationshipDeltaCandidate.
- Current task package: `docs/tasks/M8_relationship_state/T192_relationship_delta_candidate.md`.
- T192 must stay delta-only and reviewable:
  - no auto-approve or auto-apply
  - no RelationshipState mutation
  - no send/platform integration
  - no scalar-collapse
  - no raw-text dependency
- T191/T192 boundary:
  - T191 emits signals only.
  - T192 consumes signals and proposes candidate deltas only.
  - T193 later handles human review of those deltas.

## T191 Worker Completion Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/feedback.py`
  - `docs/data_contracts/relationship_state_contract.md`
  - `tests/test_relationship_signals.py` (new)
  - `docs/07_handoff.md`
- Model/type names added:
  - `RelationshipSignalProvenance` (Literal: feedback_boundary, feedback_action, metadata_derived, unknown)
  - `RelationshipSignal` (Pydantic BaseModel)
- Service added:
  - `RelationshipSignalExtractor` in `services/feedback.py` with `extract_from_feedback()` method
- Signal extraction design:
  - Only boundary-labeled feedback with known high-confidence patterns produces signals.
  - `boundary_violation` 閳?boundary_risk increase (0.7 strength).
  - `too_intimate` 閳?boundary_risk increase (0.5) + intimacy_level decrease (0.4).
  - `too_eager` 閳?initiative_allowance decrease (0.5).
  - All other actions (accept, reject, edit), boundary labels without rules, and unlabeled boundary feedback produce zero signals.
  - Each signal carries `evidence_refs` pointing to the source `feedback_id`.
  - No raw text (boundary_note, user_note, edited_text, draft_text) is stored in any signal field.
  - `provenance` is always `"feedback_boundary"` for current extraction rules.
  - `status` defaults to `"candidate"`, `is_runtime_ready()` requires human review approval.
- Relationship to T190:
  - T190 schemas remain intact and unchanged.
  - `RelationshipSignal.signal_id` values can be referenced by future `RelationshipDeltaCandidate.signal_refs`.
  - No `RelationshipState` mutation or `RelationshipDeltaCandidate` generation occurs.
- Verification:
  - Compile passed for models.py and feedback.py.
  - T191 test suite: 21 tests covering clear boundary patterns, no-signal behavior, evidence-ref preservation, no-raw-text, valid-record filtering, multi-contact, and model validation.
  - Full existing test suite: no regressions.
- Explicit non-actions:
  - No raw chat history, raw feedback text, edited text, boundary notes, or user notes were stored.
  - No LLM call, RelationshipState mutation, RelationshipDeltaCandidate generation, review CLI, or send/platform integration was added.
  - No ContactSkill, MemoryFact, approved store, or planner template was modified.

## Captain Current State Override 2026-05-24 (T190 Review Decision)

- T190 review decision: `PASS_WITH_WARNINGS`.
- T190 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun, N04 `RelationshipState.source_type` may stay extensible until approved-delta application actually exists.
  - Deferred: N02 `RelationshipDeltaDimension.magnitude` is not schema-enforced against `current_value` / `proposed_value`, N03 `RelationshipDeltaDirection="stable"` lacks contract guidance, M01 no committed automated schema validation tests yet exist.
  - Rejected: none.
- T190 is complete as the schema-only opening task for M8.
- Current Unique Task: T191 Relationship signal extractor.
- Current task package: `docs/tasks/M8_relationship_state/T191_relationship_signal_extractor.md`.
- T191 must stay extraction-only and conservative:
  - no raw chat-history reads
  - no RelationshipState auto-update
  - no delta generation or review CLI
  - no send/platform integration
  - no LLM dependency unless a later Captain task explicitly expands scope
- T190/T191 boundary:
  - T190 remains the authoritative contract for `RelationshipState` and `RelationshipDeltaCandidate`.
  - T191 may emit relationship signals only; it must not mutate state or imply milestone closure.
  - T192 must later resolve delta-direction / magnitude semantics before state-change review is introduced.

## T190 Worker Completion Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/relationship_state_contract.md` (new)
  - `docs/07_handoff.md`
- Model/enum names added:
  - `InteractionTemperature` (Literal: warm, neutral, cold, mixed, unknown)
  - `RelationshipDeltaDirection` (Literal: increase, decrease, stable, unknown)
  - `RELATIONSHIP_DIMENSION_NAMES` (Literal: familiarity, trust, warmth, reciprocity, conflict_level, boundary_risk, initiative_allowance, intimacy_level)
  - `RelationshipState` (Pydantic BaseModel)
  - `RelationshipDeltaDimension` (Pydantic BaseModel)
  - `RelationshipDeltaCandidate` (Pydantic BaseModel)
- Schema design:
  - `RelationshipState` has 8 independent float dimensions (0.0-1.0), each named explicitly. No single scalar score or weighted combination is derived.
  - `uncertainty` (0.0-1.0) captures overall assessment confidence.
  - `recent_interaction_temperature` uses categorical labels instead of a float, keeping interpretation explicit and reviewable.
  - `evidence_refs` is required (min_length=1). A state without evidence is structurally invalid.
  - `assessment_rationale`, `source_type`, and `source_skill_record_id` provide provenance tracking.
  - `status` defaults to `"candidate"`. `is_runtime_ready()` requires `status == "approved"` AND `reviewed_by_human == True` AND `last_decision == "approved"`.
  - `dimension_snapshot()` returns a dict of dimension names to float values for downstream comparison.
  - `RelationshipDeltaCandidate` captures proposed changes to specific dimensions, with `evidence_refs` (required) and optional `signal_refs` for T191 signals.
  - `RelationshipDeltaDimension` specifies per-dimension current/proposed values, direction, magnitude, and optional rationale.
  - Both models reuse `DistilledArtifactReviewMetadata` for review lifecycle compatibility with T122/T163.
- Relationship to existing `ContactSkillRelationshipState`:
  - The existing model (T111) remains the compatibility fallback inside `ContactSkillCandidate`.
  - The new `RelationshipState` is a separate, more structured model for M8 relationship tracking.
  - They are not merged or replaced.
- Verification:
  - Compile passed.
  - Synthetic model validation passed: created a `RelationshipState` and `RelationshipDeltaCandidate` with safe ids, confirmed `status == "candidate"`, `is_runtime_ready() == False`, and `evidence_refs` enforcement works.
- Explicit non-actions:
  - No signal extraction, review CLI, auto-update, or send/platform integration was added.
  - No raw chat text, feedback text, or private content was stored in any model field.
  - No LLM call, runtime mutation, or downstream integration was added.

## Captain Current State Override 2026-05-23 (T184 Review Decision)

- T184 review decision: `PASS_WITH_WARNINGS`.
- T184 is complete as the holdout evaluation task.
- T184 remains historical; M7 closure is determined by the later T185 review + M7 milestone review.
- The current task state below supersedes this historical entry.

## Captain Current State Override 2026-05-23 (T185 Review Decision + M7 Review)

- T185 review decision: `PASS_WITH_WARNINGS`.
- T185 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun, N02 heuristic safety-context detection, N03 prompt-level language enforcement rather than a hard validator.
  - Deferred: none.
  - Rejected: none.
- T185 is complete as the narrow hybrid alignment task.
- Gate M7 verdict: `Allow`.
- M7 milestone review verdict: `Allow`.
- M7 is now closed: the optional hybrid planner path is committed, regression-hardened, and aligned to the observed holdout gaps.
- Current Unique Task: T190 RelationshipState schema.
- Current task package: `docs/tasks/M8_relationship_state/T190_relationship_state_schema.md`.
- T190 must stay schema-only and conservative: no signal extraction, no review CLI, no auto-update, no send/platform integration, and no single-score collapse.
- T190 should define multidimensional `RelationshipState` and `RelationshipDeltaCandidate` concepts with explicit evidence refs and timestamps.
- T185/T190 boundary:
  - M7 remains opt-in, review-only, and template-compatible.
  - M8 must not auto-update relationship state or send messages.
  - Future relationship work should remain review-first and conservative.

## Captain Current State Override 2026-05-23 (T183 Review Decision)

## Captain Current State Override 2026-05-23 (T183 Review Decision)

- T183 review decision: `PASS_WITH_WARNINGS`.
- T183 warning disposition:
  - Accepted: N01 `.claude/settings.json` workspace-artifact overrun.
  - Deferred: N02 no committed test exercises the valid LLM-candidate merge success path, M01 no end-to-end hybrid success test, M02 no explicit reranked-order assertion after merge.
  - Rejected: none.
- T183 is complete as the opt-in hybrid planner integration M7 task.
- Current Unique Task: T184 Planner Holdout Eval.
- Current task package: `docs/tasks/M7_llm_reply_planner/T184_llm_planner_holdout_eval.md`.
- T184 must stay evaluation-only: no planner code changes, no send/platform integration, no raw private content in committed artifacts, and no quality claim without evidence.
- T184 may compare template vs hybrid outputs on anonymized scenarios, but it must distinguish private smoke evidence from committed tests and must not overclaim quality without holdout data.

## Captain Current State Override 2026-05-23 (T182 Review Decision)

- T182 review decision: `PASS_WITH_WARNINGS`.
- T182 warning disposition:
  - Accepted: N02 `.claude/settings.json` workspace-artifact overrun.
  - Deferred: N01 broken `INPUT_TOO_LARGE` preflight call-site bug, M01 missing regression test for the `INPUT_TOO_LARGE` refusal path.
  - Rejected: none.
- T182 is complete as the shared validator-hardening M7 task.
- Current Unique Task: T183 Hybrid ReplyPlanner.
- Current task package: `docs/tasks/M7_llm_reply_planner/T183_hybrid_reply_planner.md`.
- T183 must stay opt-in, additive, and review-only: no default LLM mode, no ReplyPlanner runtime mutation that bypasses gating, and no send/platform integration.
- T183 may integrate optional LLM candidates only behind explicit controls and must preserve shared deterministic validation, compact-context boundaries, and policy/boundary review.

## Captain Current State Override 2026-05-23 (T181 Review Decision)

- T181 review decision: `PASS_WITH_WARNINGS`.
- T181 warning disposition:
  - Accepted: N01 allowed-files overrun for `.claude/settings.json` and `docs/reference/AI_coding_workflow.md`, N02 default `policy_boundary` refs instead of LLM-provided supporting refs, N03 redundant `validate_ranks` call.
  - Deferred: N04 substring-only privacy leak detection, N05 dead `INPUT_TOO_LARGE` refusal path, M01 `_build_llm_input` output-shape coverage gap, M02 `_parse_provider_response` error-path coverage gap, M03 missing generator-to-validator pipeline test, M04 missing CLI stdout privacy regression test.
  - Rejected: none.
- T181 is complete as the first executable M7 task.
- Current Unique Task: T182 Candidate Validator.
- Current task package: `docs/tasks/M7_llm_reply_planner/T182_candidate_validator.md`.
- T182 must stay validator-only, additive, and private-by-default: no new candidate generation path, no hybrid planner behavior, no default LLM mode, no ReplyPlanner runtime mutation, and no send/platform integration.
- T182 may harden shared deterministic validation, explicit input-budget refusal handling, and regression coverage, but it must preserve the compact-context boundary and review-only gating.

## Captain Current State Override 2026-05-23 (T180 Review Decision)

- T180 review decision: `PASS`.
- T180 is complete as the contract-only M7 opening task.
- Current Unique Task: T181 LLM Candidate Offline CLI.
- Current task package: `docs/tasks/M7_llm_reply_planner/T181_llm_candidate_offline_cli.md`.
- T181 must stay offline, opt-in, additive, and private-output-only: no hybrid planner behavior, no default LLM mode, no ReplyPlanner mutation, and no send/platform integration.
- T181 may consume only safe synthetic/redacted `ChatContext` JSON that already respects the T123/T164/T174 compact-context boundary.
- T181 must output a validated private `LLMReplyPlan` artifact or structured refusal; it must not bypass deterministic validation or review-only gating.

## Captain Current State Override 2026-05-23 (M6 Review)

- Gate M6: `Allow`.
- Current Unique Task: T180 LLM Candidate Generator Contract.
- Current task package: `docs/tasks/M7_llm_reply_planner/T180_llm_candidate_contract.md`.
- M6 is complete: approved `ContactSkill` now supports additive decomposition through committed design, schema, projection, and context integration layers without breaking fallback behavior.
- T180 is contract-only: no LLM calls, no ReplyPlanner behavior changes, no platform/send integration, no runtime mutation, and no deprecation claim.
- Any M7 work must preserve review-only mode, privacy boundaries, and the compact-context contracts from T123/T164/T174.

## Captain Current State Override 2026-05-23 (T174 Review Decision)

- T174 review decision: `PASS`.
- T174 is complete as an additive context-integration-only task.
- Current Unique Task: T180 LLM Candidate Generator Contract.
- Current task package: `docs/tasks/M7_llm_reply_planner/T180_llm_candidate_contract.md`.
- M6 may now close after milestone review; no additional M6 worker repair pass is needed.
- T174 preserved `ApprovedContactSkillBrief` fallback, kept derived briefs additive, and coexisted cleanly with the T164 approved-patch compact-context path.

## Captain Current State Override 2026-05-23 (T173 Review Decision)

- T173 review decision: `PASS`.
- T173 is complete as an additive projection-only task.
- Current Unique Task: T174 Derived Briefs Context Integration.
- Current task package: `docs/tasks/M6_contactskill_decomposition/T174_derived_briefs_context.md`.
- M6 may now enter context integration work, but planner behavior and approved-store semantics remain unchanged.
- T174 is context-integration-only: no planner behavior changes, no ContactSkill mutation, no migration, no new storage, and no deprecation claim.
- T174 must preserve the `ApprovedContactSkillBrief` fallback, keep derived briefs additive, and coexist cleanly with the T164 approved-patch compact-context path.

## Captain Current State Override 2026-05-23 (T172 Review Decision)

- T172 review decision: `PASS`.
- T172 is complete as an additive schema-only task.
- Current Unique Task: T173 ContactSkill Projection Service.
- Current task package: `docs/tasks/M6_contactskill_decomposition/T173_projection_service.md`.
- M6 may now enter lazy projection work, but `ChatContext` and runtime behavior remain unchanged until T174.
- T173 is projection-only: no `ChatContext` integration, no `ReplyPlanner` or policy runtime changes, no ContactSkill mutation, no migration, no new storage, and no deprecation claim.
- T173 must preserve thin policy-brief evidence faithfully, compute sensitivity explicitly, and own the deterministic `important_event_summaries` formatting rule.

## Captain Current State Override 2026-05-23 (T171 Review Decision)

- T171 review decision: `PASS`.
- T171 is complete as an additive schema-only task.
- Current Unique Task: T172 CommunicationPolicyBrief + BoundaryProfileBrief Schemas.
- Current task package: `docs/tasks/M6_contactskill_decomposition/T172_communication_policy_brief_schema.md`.
- M6 may continue with schema work, but projection and runtime behavior remain unchanged until T173-T174.
- T172 is schema-only: no projection service, no `ChatContext` integration, no `ReplyPlanner` or policy runtime changes, no ContactSkill mutation, no migration, and no deprecation claim.
- T172 must formalize sensitivity reduction, important-event ownership, and derived-brief versioning strategy.
- T173 must later make the `unknown` -> `None` communication-style conversion and `relationship_state_summary` projection rules explicit.

## Captain Current State Override 2026-05-22 (T170 Review Decision)

- T170 review decision: `PASS`.
- T170 is complete as a design-only compatibility task.
- Current Unique Task: T171 PartnerPersonaBrief Schema.
- Current task package: `docs/tasks/M6_contactskill_decomposition/T171_partner_persona_brief_schema.md`.
- M6 may now enter additive schema work, but runtime behavior remains unchanged until T173-T174.
- T171 is schema-only: no projection service, no `ChatContext` integration, no `ReplyPlanner` or policy runtime changes, no ContactSkill mutation, no migration, and no deprecation claim.
- T171 must resolve `PartnerPersonaBrief.communication_style_snapshot` typing and keep `source_skill_record_id` / evidence ownership explicit.
- T172 must later formalize the boundary sensitivity reduction rule and any boundary semantics implied by approved patch hints.

## Captain Current State Override 2026-05-22 (T164 Review Decision)

- T164 review decision: `PASS_WITH_WARNINGS`.
- T164 warning disposition:
  - Accepted: N01 `.claude/settings.json` is a workspace artifact rather than a T164 scope violation, N02 duplicated `_compact_text` is low-risk refactor debt, N03 `ApprovedPatchContext.status` reuses a slightly broader enum than strictly necessary, N04 per-assemble `ApprovedPatchContextService()` instantiation is low-impact for the current offline workflow, N05 handoff test wording was inaccurate and is corrected here, N06 carrying deterministic `supporting_cluster_ids` through compact briefs is safe.
  - Deferred: M01 missing explicit frozen/archived exclusion tests, M02 missing `ChatContextAssembler` approved-patch path integration test, M03 missing empty/whitespace `behavior_instruction` edge-case coverage.
  - Rejected: none.
- Current Unique Task: T170 ContactSkill Decomposition Design.
- Current task package: `docs/tasks/M6_contactskill_decomposition/T170_decomposition_design.md`.
- M5 is functionally complete within approval-gated, review-only, non-mutating constraints.
- T170 is design-only: no code edits, no ContactSkill behavior changes, no migration, and no deprecation claim.
- Any M6 design must preserve the existing T120-T164 pipeline and keep ContactSkill runnable as the compatibility fallback aggregate.

## Captain Current State Override 2026-05-22 (T163 Review Decision)

- T163 review decision: `PASS_WITH_WARNINGS`.
- T163 warning disposition:
  - Accepted: N05 `.claude/settings.json` is workspace noise rather than a task-scope violation.
  - Deferred: N01 the contract still overclaims deterministic `patch_id` behavior, N02 no committed automated tests yet cover `PatchReviewService` / `chat-feedback-review-patch`, N03 write-back to the input file by default can risk in-place corruption on write failure, N04 review history can grow without bound.
  - Rejected: none.
- Current Unique Task: T164 Approved Patch Compact Context.
- Current task package: `docs/tasks/M5_feedback_to_patch/T164_approved_patch_context.md`.
- M5 remains approval-gated, compact, review-only, and non-mutating.
- T164 may consume only approved, runtime-ready patches into `ChatContext`, but it may not inject candidate/rejected/frozen/archived patches, mutate ContactSkill/Memory, or add outbound behavior.

## Captain Current State Override 2026-05-18 (T162 Review Decision)

- T162 review decision: `PASS_WITH_WARNINGS`.
- T162 warning disposition:
  - Accepted: N05 `.claude/settings.json` is workspace noise rather than a task-scope violation.
  - Deferred: N01 the patch contract still overclaims deterministic `patch_id` behavior, N02 raw `input_path` remains present in proposal stdout/output, N03 no committed automated proposal tests yet exist, N04 malformed cluster input with empty `contact_id` can still crash proposal generation instead of being skipped defensively.
  - Rejected: none.
- Current Unique Task: T163 Patch Review CLI.
- Current task package: `docs/tasks/M5_feedback_to_patch/T163_patch_review_cli.md`.
- M5 remains deterministic, review-only, and non-mutating.
- T163 may record human review decisions on `PreferencePatchCandidate` proposals, but it may not auto-approve, auto-apply, inject approved patches into runtime context, mutate ContactSkill/Memory, or add outbound behavior.

閺囧瓨鏌婇弮銉︽埂閿?026-05-17

閺囧瓨鏌婇弮銉︽埂閿?026-05-16

## Captain Current State Override 2026-05-18

- T161 review decision: `PASS_WITH_WARNINGS`.
- T161 warning disposition:
  - Accepted: N01 `reason_tag_summary` naming mismatch is acceptable for now because the contract documents the actual meaning, N03 `counts_by_approach_label` may safely degrade when plan files are unavailable, N05 `.claude/settings.json` is workspace noise rather than a T161 scope violation.
  - Deferred: N02 no committed automated tests yet cover the clusterer, N04 raw `input_path` remains present in cluster stdout/output and stays tracked as cross-task path/privacy debt.
  - Rejected: none.
- Current Unique Task: T162 Patch Proposal CLI.
- Current task package: `docs/tasks/M5_feedback_to_patch/T162_patch_proposal_cli.md`.
- M5 remains deterministic, review-only, and non-mutating.
- T162 may generate candidate-only `PreferencePatchCandidate` records from T161 cluster outputs, but it may not review them, approve them, apply them, or inject them into runtime context.

## Captain Current State 2026-05-16

- T133 review decision: `PASS_WITH_WARNINGS`.
- T133 warning disposition: N01/N02/N03/N04/N05 all accepted; no deferred or rejected warnings.
- Gate M3: `Conditional`, documented in `docs/review/M3_review.md`.
- Current Unique Task: T140 Feedback Schema CLI.
- Current task package: `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`.
- M4/T140 may proceed only under review-only constraints: no auto-send, no realtime platform integration, no LLM drafting expansion, no automatic ContactSkill/Memory mutation, and no relationship-aware maturity claim.
- T150 must add committed regression tests covering ReplyPlanner structure, boundary sensitivity, thin context, false positives, subtle false negatives, privacy leakage, contact alignment, and ranking.
- Roadmap update: `docs/reference/gpt閻ㄥ嫬鎮楃紒顓☆啎鐠佲剝鈧繆鐭?閺囧瓨鏌婇悧?.md` is accepted as directionally aligned, but milestone/task ordering has been revised. M4 is feedback capture/validation/summary only; M4.5 is regression hardening; feedback-to-patch, ContactSkill-compatible decomposition, LLM planner, RelationshipState, MemoryRetriever, BehaviorPlanner, Feishu, and WeChat are delayed behind gates.

## 1. 瑜版挸澧犻悩鑸碘偓?
妞ゅ湱娲扮捄顖滃殠瀹告彃鍨忛幑顫偓?
閺冄嗙熅缁惧尅绱?
- T00閿涙瓙eChatBot/iLink SDK 鐎瑰顥婇崪灞肩癌缂佸鐖滈梼鑸殿唽閹恒垺绁撮敍瀹篹view `PASS`閵?- T01閿涙氨娅ヨぐ?session 妤犲矁鐦夐敍瀹篹view `BLOCK`閵?- 閻劍鍩涘鎻掑枀鐎规矮绗夋穱?T01閿涘奔绗夐崘宥嗗腹鏉╂稑浜曟穱?SDK 閻ц缍嶉妴浣瑰閹诲繑鍨ㄩ懕濠傘亯鐠佹澘缍嶇拠璇插絿鐠侯垳鍤庨妴?
閺傛媽鐭剧痪鍖＄窗

- 閻劍鍩涘鏌モ偓姘崇箖 WeFlow 瀹搞儱鍙跨€电厧鍤懕濠傘亯鐠佹澘缍嶉妴?- 缁変礁鐦戦弫鐗堝祦娴ｅ秳绨?`private/chat_history/`閿涘苯褰?`.gitignore` 娣囨繃濮㈤妴?- 娑撳绔撮梼鑸殿唽閻╁瓨甯撮崑姘ｂ偓婊冾嚠鐠囨繆顔囪ぐ鏇⑩攳閸斻劎娈戦梹鎸庢埂閸忓磭閮撮幇鐔虹叀 chat agent閳ユ縿鈧?- 瑜版挸澧犻惄顔界垼閺勵垳顬囩痪鑳崁妫?MVP閿涙SONL -> normalized events -> chunks -> memory facts -> ContactSkill -> review -> relationship-aware reply planner閵?- T100 worker 瀹歌弓楠囬崙?schema profile閵嗕苟ormalized event contract 閸滃苯鎮庨幋鎰姎閺?fixture閿涘苯鑻熼柅姘崇箖 reviewer `PASS`閵?- Captain 瀹告彃鐨?T100/T101/T102/T103/T110/T111/T112/T113/T114/T120/T121/T122/T123/T130/T131/T132 閺嶅洩顔囩€瑰本鍨氶敍瀛廰te M1 = `Conditional`閿涘瓔urrent Unique Task 閹恒劏绻橀崚?T133閵?- T101 worker 瀹歌弓楠囬崙娲缁変浇鍔氶弫蹇氼潐閸掓瑣鈧够ource_ref 鐟欏嫬鍨崪宀兯夐崗鍛啊 `source_ref/raw_ref` 妫板嫯顫嶈ぐ銏♀偓浣烘畱閸氬牊鍨?fixture閿涘苯鑻熼柅姘崇箖 reviewer `PASS`閵?- T102 worker 瀹歌弓楠囬崙鐑樻付鐏?normalize CLI閿涘苯鑻熺€瑰本鍨?dry-run 娑?limit 鐏忓繑鐗遍張顒勭崣鐠囦緤绱漴eviewer 閸掋倕鐣?`PASS`閵?- T103 milestone review 瀹稿弶甯撮崣?Gate M0 = `Conditional`閿涘苯鍘戠拋姝岀箻閸?M1閿涙笨110 conversation chunker v0閵嗕箑111 distillation schemas 閸?T112 summary/fact extraction 閸у洤鍑￠柅姘崇箖 reviewer `PASS`閿涘113 ContactSkill builder 瀹告煡鈧俺绻?reviewer `PASS_WITH_WARNINGS`閿涘114 绾喛顓?Gate M1 = `Conditional`閵?- T120 file store models 瀹告煡鈧俺绻?reviewer `PASS_WITH_WARNINGS`閿涘苯鍘戠拋姝岀箻閸?T121閵?- T121 evidence validator 瀹告煡鈧俺绻?reviewer `PASS_WITH_WARNINGS`閿涘苯鍘戠拋姝岀箻閸?T122閵?- T122 skill review CLI 瀹告煡鈧俺绻?reviewer `PASS_WITH_WARNINGS`閿涘苯鍘戠拋姝岀箻閸?T123閵?- T123 context integration 瀹告煡鈧俺绻?reviewer `PASS_WITH_WARNINGS`閿涘130 ReplyPlan schema 瀹告煡鈧俺绻?reviewer `PASS_WITH_WARNINGS`閿涘131 ReplyPlanner 瀹告煡鈧俺绻?reviewer `PASS_WITH_WARNINGS`閿涘132 Reply Policy 瀹告煡鈧俺绻?reviewer `PASS_WITH_WARNINGS`閿涘苯鍘戠拋姝岀箻閸?T133閵?
## 2. 瑜版挸澧犻崬顖欑娴犺濮?
T133: 閻劌宸婚崣?holdout 閸︾儤娅欑拠鍕強閸ョ偛顦查懛顏嗗姧鎼达箑鎷版潏鍦櫕闁潧鐣ч妴?
娴犺濮熼崠鍜冪窗`docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`

閻樿埖鈧緤绱癟132 瀹告煡鈧俺绻?`PASS_WITH_WARNINGS`閿涘eplyPlanner 瀹告彃鍙挎径?review-only contract wiring 閸?policy/boundary 妞嬪酣娅撶仦鍌樷偓淇?33 閸欘亜浠涢崠鍨倳 holdout eval 娑?Gate M3 閸掋倖鏌囬敍娑楃瑝娣囶喗鏁?planner 娴狅絿鐖滈敍灞肩瑝閹绘劒姘?holdout 閸樼喐鏋冮敍灞肩瑝閼奉亜濮╅崣鎴︹偓浣碘偓浣风瑝閹恒儲鏆熼幑顔肩氨閵嗕椒绗夊鏇炲弳閸氭垿鍣洪弫鐗堝祦鎼存挶鈧椒绗夐崶鐐额嚢閹存牗纭犻棁鎻掑斧婵浜版径鈺勵唶瑜版洏鈧?
## 3. T100 鐎瑰本鍨氱拋鏉跨秿

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- `examples/payloads/weflow_redacted_sample.jsonl`

worker 娓氀冪秼閸撳秴鍑＄涵顔款吇閻ㄥ嫰鐝穱鈥冲娇缂佹捁顔戦敍?
- 4 娑?WeFlow JSONL 閺傚洣娆㈤崗?38,289 鐞涘矉绱濋崗銊╁劥閸欘垵袙閺嬫劧绱濋弮鐘叉綎鐞涘被鈧?- 妞よ泛鐪扮悰宀€琚崹瀣旂€规艾鍨庢稉?`header`閵嗕梗member`閵嗕梗message` 娑撳琚妴?- 閻喐顒滈棁鈧憰浣界箻閸?normalized event 閻ㄥ嫭妲?`_type=message` 鐞涘矉绱濋崗?38,253 閺壜扳偓?- `timestamp` 缁嬪啿鐣炬稉?Unix epoch seconds閵?- `type` 閺勵垱绉烽幁顖滆閸ㄥ瀵岄崐娆撯偓澶婄摟濞堢绱濋崗鏈佃厬 `0`閵嗕梗7`閵嗕梗25`閵嗕梗80` 閸楃姷绮锋径褍顦块弫鑸偓?- `replyToMessageId` 閸欘垯缍旀稉鍝勭穿閻劑鎽肩捄顖氣偓娆撯偓澶涚幢`chatRecords` 閸欘垯缍旀稉楦挎祮閸欐垼浜版径鈺勵唶瑜版洖鈧瑩鈧鈧?- 閼磋鲸鏅?閸氬牊鍨氶弽铚傜伐瀹歌尙鏁撻幋鎰剁礉娑撳秴瀵橀崥顐ゆ埂鐎圭偛甯弬鍥モ偓浣烘埂鐎圭偠浠堢化璁虫眽婵挸鎮曢幋鏍埂鐎圭偞鏋冩禒璺烘倳閵?
Reviewer 缂佹捁顔戦敍?
- `docs/review/T100_review.md` verdict 娑?`PASS`閵?- N01 accepted閿涙瓐100/Q104 閸忔娊妫存笟婵囧祦閺囧瓨鏌婃稉?閳ユ翻100 worker draft + review PASS閳ユ縿鈧?- N02 deferred閿涙ype=80/chatRecords fixture 鐟曞棛娲婇悾娆戠舶 T102/T150閵?- N03 deferred閿涙瓱vent_id 閻?SHA-1/SHA-256 閸欐牞鍨楅悾娆戠舶 T102閵?
## 4. T101 鐎瑰本鍨氱拋鏉跨秿

- `docs/data_contracts/privacy_redaction_rules.md`
- `docs/data_contracts/source_ref_rules.md`
- `examples/payloads/weflow_redacted_sample.jsonl` 瀹告彃濮為崗?`eventIdPreview`閵嗕梗sourceRefPreview`閵嗕梗rawRefPreview`

Reviewer 缂佹捁顔戦敍?
- `docs/review/T101_review.md` verdict 娑?`PASS`閵?- N01 deferred閿涙ype=80/chatRecords fixture 鐟曞棛娲婄紒褏鐢婚悾娆戠舶 T102/T150閵?- N02 accepted閿涙瓲ixture preview hex 閸婄厧褰叉担婊€璐熷▔銊╁櫞閸楃姳缍呴敍灞肩瑝鐟曚焦鐪版潻鏂炬叏閵?- N03 deferred閿涙氨绮ㄩ弸鍕閺囨寧宕?token 娑撳骸鐤勯梽鍛板姎閺佸繘娓跺Ч鍌滄畱鐎靛綊缍堟禍銈囩舶 T102 鐎圭偟骞囬弮鑸电墡妤犲被鈧?
T102 韫囧懘銆忛柆闈涚暓閿?
- `docs/data_contracts/privacy_redaction_rules.md` 閻?Field Handling Matrix閵?- `docs/data_contracts/source_ref_rules.md` 閻?Allowed Public Shape閵?- normalize 鏉堟挸鍤崣顏囧厴鏉╂稑鍙?`private/distilled/`閵?- stdout 閸滃苯褰查幓鎰唉閻╊喖缍嶆稉宥呯繁閸戣櫣骞囬惇鐔风杽閼卞﹤銇夐崢鐔告瀮閵嗕胶婀＄€圭偞鏋冩禒璺烘倳閵嗕胶婀＄€圭偠浠堢化璁虫眽婵挸鎮曢幋鏍埂鐎圭偛閽╅崣?ID閵?
## 5. T102 鐎瑰本鍨氱拋鏉跨秿

- `src/practical_chat_agent/services/chatlog_ingestion.py`
- `src/practical_chat_agent/app/main.py`

Reviewer 缂佹捁顔戦敍?
- `docs/review/T102_review.md` verdict 娑?`PASS`閵?- N01 deferred閿涙碍妫ら弫?timezone 闂堟瑩绮梽宥囬獓 warning 閻ｆ瑧绮?T103/T150 閸掋倖鏌囬弰顖氭儊闂団偓鐟曚浇藟閵?- N02/N03 deferred閿涙艾寮诲▎陇顕伴崣鏍ф嫲閸忋劑鍣洪崘鍛摠缂傛挸鐡ㄩ悾娆戠舶 T110/T150 婢跺嫮鎮婇妴?- N04 accepted閿涙氨閮寸紒鐔哥Х閹垰鍙ч柨顔跨槤绾剛绱惍浣风稊娑?MVP 閸忔粌绨抽崣顖涘复閸欐ぜ鈧?- N05 deferred閿涙氨绮ㄩ弸鍕 PII token 閺囨寧宕查幒銊ㄧ箿閸?T112+ 閽傛悂顩撮梼鑸殿唽閵?- N06 deferred閿涙艾宕熼弬鍥︽ sender_role 缁嬪啿浠撮幀褏鏆€缂?T114/T150 妤犲矁鐦夐妴?
瀹告煡鐛欑拠渚婄窗

- `chatlog-normalize` 閺€顖涘瘮 `--input`閵嗕梗--output`閵嗕梗--limit`閵嗕梗--dry-run`閵嗕梗--timezone-name`閵?- 鏉堟挸鍙嗛梽鎰煑閸?`private/chat_history/**`閿涘矁绶崙娲閸掕泛婀?`private/distilled/**`閵?- stdout/report 娑撳秴瀵橀崥顐ゆ埂鐎圭偛甯弬鍥モ偓浣烘埂鐎圭偞鏋冩禒璺烘倳閵嗕胶婀＄€圭偠浠堢化璁虫眽婵挸鎮曢幋鏍埂鐎圭偛閽╅崣?ID閵?- normalized event 鐎涙顔屾稉?T100/T101 閸氬牏瀹崇€靛綊缍堥妴?
## 6. T103 鐎瑰本鍨氱拋鏉跨秿

- `docs/review/T103_milestone_review.md`
- `docs/review/T103_review.md`

Reviewer 缂佹捁顔戦敍?
- Gate M0 = `Conditional` accepted閵?- M0 娴滄梹娼涵顒佲偓褑顩﹀Ч鍌氬弿闁劍寮х搾鐐解偓?- 閸忎浇顔忔潻娑樺弳 M1閿涘奔绗呮稉鈧崬顖欑娴犺濮熸稉?T110閵?
M1 韫囧懘銆忛幍鎸庡复閻ㄥ嫭娼禒璁圭窗

- T110/T150 缂佈呯敾鐟曞棛娲?`type=80` / `chatRecords` 閻ㄥ嫪绻氱€瑰牆顦╅悶鍡曠瑢濞村鐦妴?- T110/T114/T150 娣囨繄鏆€楠炲爼鐛欑拠?`sender_role`閵嗕辜imezone fallback閵嗕焦鈧嗗厴/閸愬懎鐡ㄩ惄绋垮彠娑撳秶鈥樼€规碍鈧佲偓?- T112+ 娴犵粯鍓?LLM-facing 閽傛悂顩村銉╊€冪紒褏鐢婚柆闈涚暓 T101 闂呮劗顫嗘潏鍦櫕閿涘奔绗夐幎濠勵潌閺?normalize 閺傚洦婀伴幍鈺傛殠閸掓澘褰查幓鎰唉娴溠呭⒖閵?
## 7. T110 鐎瑰本鍨氱拋鏉跨秿

- 娴狅絿鐖滈弨鐟板З閿?  - `src/practical_chat_agent/services/conversation_chunking.py`
  - `src/practical_chat_agent/app/main.py`
- 瀹告彃鐤勯悳鏉垮敶鐎圭櫢绱?  - 閺傛澘顤?`ConversationChunkingService`閿涘本绉风拹?`private/distilled/**/normalized_events.jsonl`閵?  - 閺傛澘顤?`chatlog-chunk` CLI閿涘矂绮拋銈嗗Ω `chunks.jsonl` 閸滃本娲块弬鏉挎倵閻?`run_report.json` 閸愭瑥娲栭崥灞肩娑?`private/distilled/<run_id>/` 閻╊喖缍嶉妴?  - chunk v0 娴犲懍濞囬悽銊ょ箽鐎瑰牐绔熼悾宀嬬窗`conversation/contact` 閸欐ê瀵查妴浣规闂傛挳妫块梾鏃囩箖婢堆佲偓浣稿礋 chunk 濞戝牊浼呴弫棰佺瑐闂勬劑鈧浇绶崗銉х波閺夌喆鈧?  - 濮ｅ繋閲?chunk 娣囨繄鏆€ `chunk_id`閵嗕梗contact_id`閵嗕梗conversation_id`閵嗕梗event_ids`閵嗕梗time_range`閵嗕梗message_count`閵嗕梗chunking_reason`閵?  - chunk 缁狙傞獓閻椻晝鎴风紒顓濈炊闁?T102 閻ㄥ嫪绗夌涵顔肩暰閹備繆閸欏嚖绱癭source_message_type_codes` / `source_message_type_counts`閵嗕梗message_type_counts`閵嗕梗interaction_flag_counts`閵嗕梗risk_flag_counts`閵嗕梗events_with_interaction_flags`閵嗕梗events_with_risk_flags`閵?  - 閺堫亜绱╅崗?LLM閵嗕躬mbedding閵嗕竼ontactSkill閵嗕焦鏆熼幑顔肩氨閹存牕鐤勯弮璺洪挬閸欑増甯撮崗銉幢chunk 鏉堟挸鍤稉宥呭晸閼卞﹤銇夐崢鐔告瀮閵?- 瀹告彃鐣幋鎰扮崣鐠囦緤绱?  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/conversation_chunking.py src/practical_chat_agent/app/main.py`
  - `$env:PYTHONPATH='src'; & 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main chatlog-chunk --input private/distilled/t102_smoke --limit 12`
  - 缂佹挻鐏夐敍姘灇閸旂喎鍟撻崙?`private/distilled/t102_smoke/chunks.jsonl`閿涘苯鑻熼幎?chunking 閹躲儱鎲￠崘娆忓弳 `private/distilled/t102_smoke/run_report.json`閵?  - 鐠囥儱鐨弽閿嬫拱閸忚鲸绉风拹?12 閺?normalized events閿涘瞼鏁撻幋?1 娑?chunk閿涙矖chunking_reason=manual`閿涘畭boundary_flags=["end_of_input"]`閿涘奔绗栨穱婵堟殌娴?`type=7` / `type=80` 鐎电懓绨查惃?mixed/system 妞嬪酣娅撴稉搴濇唉娴滄帞绮虹拋掳鈧?- Reviewer 缂佹捁顔戦敍?  - `docs/review/T110_review.md` verdict 娑?`PASS`閵?  - 绾喛顓?T110 閸欘亜鐤勯悳?conversation chunker v0閿涘本婀搾濠勬櫕瀵洖鍙?LLM閵嗕躬mbedding閵嗕竼ontactSkill閵嗕焦鏆熼幑顔肩氨閹存牕鐤勯弮璺洪挬閸欒埇鈧?  - 绾喛顓?chunk 鏉堟挸鍤稉宥呭晸閼卞﹤銇夐崢鐔告瀮閿涘tdout/report 閺堫亜褰傞悳鎵埂鐎圭偠浜版径鈺佸敶鐎硅纭犻棁灞傗偓?  - 绾喛顓?T102 閻?`source_message_type_code`閵嗕梗risk_flags`閵嗕梗interaction_flags`閵嗕梗message_type`閵嗕梗sender_role` 缁涘绗夌涵顔肩暰閹備繆閸欏嘲鍑＄悮顐＄箽閻ｆ瑦鍨ㄥЧ鍥ㄢ偓璁崇炊闁帇鈧?- Non-blocking 婢跺嫮鎮婇敍?  - N01 accepted閿涙瓪chunking_reason="manual"` 鐎靛湱绮ㄩ弸鍕珶閻ｅ矁銆冩潏鎯т焊缁绱濇担鍡楃秼閸?`boundary_flags` 瀹歌弓绻氶悾娆戠矎閼哄偊绱遍崥搴ｇ敾 T112/T150 娴ｈ法鏁ら弮鏈电瑝鐟曚礁褰ф笟婵婄 reason閵?  - N02 accepted/deferred閿涙on-monotonic timestamp warning 瑜版挸澧犻崣顏囩箻閸?report閿涘奔绗夐梼璇差敚閿涙稖瀚㈤崥搴ｇ敾閺嶉攱婀伴崙铏瑰箛閹烘帒绨梻顕€顣介敍宀€鏁?T150 婢х偛濮炵拠濠冩焽鐟曞棛娲婇妴?  - N03 accepted/deferred閿涙瓪run_report.json` 閻?chunking 閹躲儱鎲¤ぐ銏♀偓浣藉喕婢?MVP 娴ｈ法鏁ら敍姹?14/T150 閸欘垱瀵滅€圭偤妾幎鑺ョ叀闂団偓濮瑰倹澧跨仦鏇樷偓?  - N04 deferred閿涙俺鍤滈崝銊ュ濞村鐦禒宥囨殌缂?T150閵?  - N05 accepted閿涙瓪topic_hint` 閺?optional閿涘110 娑撳秶鏁撻幋?topic hint 閸氬牏鎮婇敍灞芥倵缂侇厾鏁?T112+ 閹芥顩?鐠囶厺绠熼梼鑸殿唽鐞涖儴鍐婚妴?
## 8. T111 鐎瑰本鍨氱拋鏉跨秿

- 娴狅絿鐖?/ 閺傚洦銆傞弨鐟板З閿?  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/distillation_output_contract.md`
  - `docs/07_handoff.md`
- 瀹告彃鐤勯悳鏉垮敶鐎圭櫢绱?  - 閸?`core.models` 娑擃厽鏌婃晶鐐插讲婢跺秶鏁?schema閿?    - `DistillationClaim`
    - `ChunkSummaryObservation`
    - `ChunkSummary`
    - `MemoryFactCandidate`
    - `ContactSkillTopicPreference`
    - `ContactSkillPattern`
    - `ContactSkillImportantEvent`
    - `ContactSkillRelationshipState`
    - `ContactSkillCommunicationStyle`
    - `ContactSkillUserSidePreferences`
    - `ContactSkillReplyStrategy`
    - `ContactSkillUsageBoundary`
    - `ContactSkillCandidate`
  - 閹碘偓閺?fact / claim / skill 閻╃鍙х紒鎾寸€崸鍥ㄦ暜閹?`evidence_refs`閵嗕梗confidence`閵嗕梗sensitivity`閵嗕梗status`閵?  - `ContactSkillCandidate` 閺勫海鈥橀崝鐘插弳 `usage_boundary`閿涘矂绮拋銈囶洣濮?`persona_clone`閵嗕梗impersonation`閵嗕梗autonomous_contact_simulation`閵?  - 閺傛澘顤?`docs/data_contracts/distillation_output_contract.md`閿涘苯娴愮€?T112/T113 閹碘偓闂団偓 JSON contract閵嗕胶濮搁幀浣哄鐎规哎鈧焦鏅遍幇鐔峰缁撅箑鐣鹃崪灞藉冀 impersonation 鏉堝湱鏅妴?  - 閺堫亣鐨熼悽?LLM閵嗕焦婀悽鐔稿灇閻喎鐤勯拏鎼侇洿缂佹挻鐏夐妴浣规弓閸愭瑦鏆熼幑顔肩氨 migration閵?- 瀹告彃鐣幋鎰扮崣鐠囦緤绱?  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/core/models.py`
  - 缂佹挻鐏夐敍姘侀崹瀣瀮娴犲墎绱拠鎴︹偓姘崇箖閵?- Reviewer 缂佹捁顔戦敍?  - `docs/review/T111_review.md` verdict 娑?`PASS`閵?  - 绾喛顓?T111 鐎瑰本鏆ｇ€规矮绠?`ChunkSummary`閵嗕梗MemoryFactCandidate`閵嗕梗ContactSkillCandidate` 閸欏﹨绶熼崝鈺冪波閺嬪嫨鈧?  - 绾喛顓婚幍鈧張?fact/claim/skill 缂佹挻鐎鍝勫煑閹存牗鏁幐?`evidence_refs`閵嗕梗confidence`閵嗕梗sensitivity`閵嗕梗status`閵?  - 绾喛顓?`ContactSkillUsageBoundary` 姒涙顓荤粋浣诡剾 `persona_clone`閵嗕梗impersonation`閵嗕梗autonomous_contact_simulation`閵?  - 绾喛顓婚弮?LLM 鐠嬪啰鏁ら妴浣规￥閺佺増宓佹惔?migration閵嗕焦妫?`private/` 濞夊嫰婀堕妴?- Non-blocking 婢跺嫮鎮婇敍?  - N01 accepted閿涙瓪ContactSkillRelationshipState` / `ContactSkillCommunicationStyle` 閻ㄥ嫰鍎撮崚鍡楃摟濞堝吀绻氶悾娆掑殰閻㈠崬鐡х粭锔胯閿涘VP 闂冭埖顔岄崣顖涘复閸欐绱遍崥搴ｇ敾閸欘垱瀵滅€圭偤妾?LLM 鏉堟挸鍤弨鍓佹彛閵?  - N02 accepted/deferred閿涙瓪redaction_policy` 瑜版挸澧犳担璺ㄦ暏 `dict[str, Any]` 閸欘垱甯撮崣妤嬬幢T120/T150 閸欘垵顫?store/review 闂団偓鐟曚焦鏁兼稉铏圭波閺嬪嫬瀵?model閵?  - N03 deferred閿涙瓪DistillationMemoryType` 娑撳海骞囬張?`MemoryType` enum 閻ㄥ嫭妲х亸鍕唉缂?T120閵?  - N04 deferred閿涙瓪created_at` / `updated_at` 閻?T120 store 閹存牔楠囬悧鈺佸晸閸忋儱鐪扮悰銉ュ帠閵?  - N05 deferred閿涙瓍ydantic 缁撅附娼懛顏勫З閸栨牗绁寸拠鏇氭唉缂?T150閵?
## 9. T112 鐎瑰本鍨氱拋鏉跨秿

- 娴狅絿鐖?/ 閺傚洦銆傞弨鐟板З閿?  - `src/practical_chat_agent/services/chatlog_distillation.py`
  - `src/practical_chat_agent/services/contact_skill.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- 瀹告彃鐤勯悳鏉垮敶鐎圭櫢绱?  - 閺傛澘顤?`ChatlogDistillationService`閿涘本绉风拹?`private/distilled/**/chunks.jsonl` 娑撳骸鎮撻惄顔肩秿 `normalized_events.jsonl`閵?  - 閺傛澘顤?`chatlog-distill` CLI閿涘本鏁幐?`--input`閵嗕梗--output`閵嗕梗--limit`閵嗕梗--sample`閵嗕梗--dry-run`閵?  - LLM 鐠囬攱鐪版径宥囨暏 OpenAI-compatible `/chat/completions` 鐠嬪啰鏁ゆ搴㈢壐閵?  - distillation 鏉堟挸鍤崗鍫濅粵 provider 閸忕厧顔愯ぐ鎺嶇閸栨牭绱濋崘宥呭繁閸掕埖鐗庢灞艰礋 T111 `ChunkSummary` / `MemoryFactCandidate` schema閵?  - evidence refs 韫囧懘銆忛拃钘夋躬鐎电懓绨?chunk 閻?`chunk_id + event_ids` 閼煎啫娲块崘鍜冪幢鐡掑﹦鏅?refs 娴兼艾顕遍懛?chunk 鐞氼偅瀚嗙紒婵撶礉娑撳秴鍟撻崗?accepted 鏉堟挸鍤妴?  - 娴溠呭⒖閸欘亜鍟撻崗?`private/distilled/<run_id>/chunk_summaries.jsonl`閵嗕梗memory_facts.jsonl` 閸滃苯鎮庨獮璺烘倵閻?`run_report.json`閿涙稐绗夋穱婵嗙摠 LLM prompt 閹?raw response閵?  - `contact_skill.py` 瑜版挸澧犳禒鍛儓鏉炲鍣烘潏鍛И閸戣姤鏆熼敍灞艰礋 T113 閼辨艾鎮?refs 妫板嫮鏆€閿涘奔绗夐崠鍛儓 ContactSkill builder閵嗕购eview exporter 閹?store 闁槒绶妴?- 瀹告彃鐣幋鎰扮崣鐠囦緤绱?  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/chatlog_distillation.py src/practical_chat_agent/services/contact_skill.py src/practical_chat_agent/app/main.py`
  - `$env:PYTHONPATH='src'; & 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main chatlog-distill --input private/distilled/t102_smoke --limit 1`
  - 妫ｆ牗顐奸崶鐘崇煓缁犺京缍夌紒婊堟閸掓儼绻戦崶?`remote_request_failed`閿涘瘍orker 濞屸剝婀侀悽?mock 閸愭帒鍘栭幋鎰閿涙稒褰侀弶鍐槻鐠烘垵鎮?provider 閸欘垵鎻妴?  - 閸旂姴鍙?provider 鏉堟挸鍤崗鐓庮啇瑜版帊绔撮崠鏍ф倵閿涘苯鐨弽閿嬫拱閹存劕濮涢崘娆忓毉 `chunk_summaries.jsonl`閵嗕梗memory_facts.jsonl`閵嗕梗run_report.json`閵?  - 瑜版挸澧犵亸蹇旂壉閺堫剛绮ㄩ弸婊愮窗1 娑?selected chunk閿? 娑?successful chunk閿涘苯鍟撻崙?1 閺?chunk summary閵? 閺?memory facts閿涘畭distillation.failure_reasons` 娑撹櫣鈹栭妴?  - reviewer 绾喛顓绘禍鍝勪紣閹惰姤鐓?3+ 閺?fact 閻?evidence_refs閿涘苯娼庨懗钘夋礀閹稿洤缍嬮崜?chunk 娴滃娆㈤妴?- Reviewer 缂佹捁顔戦敍?  - `docs/review/T112_review.md` verdict 娑?`PASS`閵?  - 绾喛顓?LLM 鏉堟挸鍤紒蹇氱箖 provider 閸忕厧顔愯ぐ鎺嶇閸栨牓鈧箑111 schema 閺嶏繝鐛欓崪?evidence refs 閼煎啫娲块弽锟犵崣閸氬孩澧犻崘娆忓弳閵?  - 绾喛顓?prompt/raw response 娑撳秴鍟撻崗銉︽瀮娴犺绱漵tdout/report 閸欘亜鎯堢紒鐔活吀閸滃瞼濮搁幀浣虹垳閵?  - 绾喛顓绘禍褏澧块崣顏勫晸閸?`private/distilled/`閿涘本鐥呴張澶屾埂鐎圭偠浜版径鈺佸斧閺傚洩绻橀崗?docs/examples/tests/stdout閵?  - 绾喛顓婚張顏囩Ш閻ｅ苯浠?ContactSkill builder閵嗕够tore閵嗕焦鏆熼幑顔肩氨 migration閵嗕礁鐤勯弮璺洪挬閸欑増甯撮崗銉﹀灗閼奉亜濮╅崣鎴︹偓浣碘偓?- Non-blocking 婢跺嫮鎮婇敍?  - N01 deferred閿涙瓪chunk_id` fallback 閺勵垰鎮庡▔鏇犵煐缁帒瀹?evidence閿涘奔绲炬导姘舵娴ｅ氦鐦夐幑顔剧翱鎼达讣绱盩114 閸忋劑鍣?閺囨潙銇囬弽閿嬫拱閹惰姤鐓￠弮璺哄彠濞夈劋绮庨張?chunk_id 閻ㄥ嫭鐦笟瀣ㄢ偓?  - N02 deferred閿涙rovider shape drift 瀹歌尙鏁?R024 鐠佹澘缍嶉敍姹?14/T150 缂佈呯敾妤犲矁鐦夐妴?  - N03 accepted/deferred閿涙ensitivity 閸忔娊鏁拠宥呭幑鎼存洑缍旀稉?MVP 閸欘垱甯撮崣妤嬬幢T150 閸欘垵藟閸忓懏绁寸拠鏇熷灗閸氬海鐢婚弨鍓佹彛閵?  - N04 accepted/deferred閿涙emory_type fallback 娴ｆ粈璐?MVP 閸欘垱甯撮崣妤嬬幢T114/T150 鐟欏倸鐧傜拠顖氬瀻缁眹鈧?  - N05 accepted閿涙瓪contact_skill.py` 鏉炲鍣烘潏鍛И娑撳秷绉洪悾宀嬬礉T113 閸欘垱澧跨仦鏇熷灗闁插秴鍟撻妴?  - N06 deferred閿涙chema 閺嶏繝鐛欓妴涔獀idence refs閵嗕赋II 閼磋鲸鏅遍妴涔竢ovider 瑜版帊绔撮崠鏍畱閼奉亜濮╅崠鏍ㄧゴ鐠囨洜鏆€缂?T150閵?  - N07 accepted/deferred閿涙rompt 鐏?PII token 閺囨寧宕插鏌ュ劥閸掑棙寮х搾?T102 N05閿涙笨150 privacy leakage smoke test 缂佈呯敾鐟曞棛娲婇妴?
## 10. T113 鐎瑰本鍨氱拋鏉跨秿

- 娴狅絿鐖?/ 閺傚洦銆傞弨鐟板З閿?  - `src/practical_chat_agent/services/contact_skill.py`
  - `src/practical_chat_agent/exporters/contact_skill_markdown.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- 瀹告彃鐤勯悳鏉垮敶鐎圭櫢绱?  - `ContactSkillBuilderService` 濞戝牐鍨?T112 閻?`chunk_summaries.jsonl` 閸?`memory_facts.jsonl`閿涘矂鈧俺绻?Pydantic `model_validate` 鐠囪褰囨稉濠冪埗娴溠呭⒖閵?  - 閻㈢喐鍨?`ContactSkillCandidate`閿涘苯鑻熷鍝勫煑 `status="candidate"` 娑撳酣娼粚?`evidence_refs`閵?  - 鏉堟挸鍤?`private/distilled/<run_id>/contact_skill.candidate.json` 娑?`contact_skill.review.md`閵?  - Markdown review exporter 鐏炴洜銇?relationship state閵嗕恭ommunication style閵嗕辜opics閵嗕巩mportant events閵嗕够table preferences閵嗕躬motional patterns閵嗕购eply strategy閵嗕菇sage boundary閵嗕躬vidence refs 娑?anti-impersonation reminder閵?  - 閺傛澘顤?`chatlog-build-contact-skill` CLI閿涘本鏁幐?`--input`閵嗕梗--output`閵嗕梗--contact-id`閵嗕梗--dry-run`閵?  - 鏉堟挸鍤梽鎰煑閸?`private/distilled/`閿涙稒妫ら懛顏勫З approve閵嗕焦妫?DB migration閵嗕焦妫?realtime 楠炲啿褰撮妴浣规￥閼奉亜濮╅崣鎴︹偓浣碘偓?- 瀹告彃鐣幋鎰扮崣鐠囦緤绱?  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/contact_skill.py src/practical_chat_agent/exporters/contact_skill_markdown.py src/practical_chat_agent/app/main.py`
  - `$env:PYTHONPATH='src'; & 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main chatlog-build-contact-skill --input private/distilled/t102_smoke`
  - 閺嶉攱婀扮涵顔款吇閻㈢喐鍨?`contact_skill.candidate.json` 娑?`contact_skill.review.md`閿涘畱andidate 閻樿埖鈧椒绮涙稉?`candidate`閿涘eview artifact 閸欘垵顕伴獮璺虹敨 evidence refs / usage boundary閵?- Reviewer 缂佹捁顔戦敍?  - `docs/review/T113_review.md` verdict 娑?`PASS_WITH_WARNINGS`閵?  - 绾喛顓婚張顏囩Ш閻ｅ矁鍤滈崝?approve閵嗕椒绻氱€?raw chat text閵嗕胶鏁撻幋鎰ㄢ偓娓僶ntact speaking閳ユ繂鍞寸€瑰箍鈧礁鍟?DB migration閵嗕焦甯?realtime platform 閹?auto-send閵?  - 绾喛顓?evidence chain閵嗕恭andidate 閻樿埖鈧降鈧工nti-impersonation guardrails 閸?review artifact 閸у洦寮х搾?T113 娴犺濮熼惄顔界垼閵?- Warning 婢跺嫮鎮婇敍?  - N01 accepted閿涙瓪_build_report` 闁插秴顦茬拫鍐暏閺勵垯缍嗚ぐ鍗炴惙闁插秴顦插銉ょ稊閿涘奔绗夌憰浣圭湴鏉╂柧鎱ㄩ妴?  - N02 deferred閿涙艾鎯庨崣鎴濈础 tokens/topic/relationship 閹恒劍鏌囬崑蹇撶秼閸撳秴鐨弽閿嬫拱閿涘114 闂団偓閻劍娲挎径褎鍨ㄦ稉宥呮倱閺嶉攱婀伴弳鎾苟濞夋稑瀵茬紓鍝勫經閿涘120+ 閸欘垵鈧啳妾?LLM-assisted inference閵?  - N03 deferred閿涙瓭onfidence / closeness / trust 閸忣剙绱￠崠鏍︾瑬闂?evidence-weighted閿涘114 闂団偓娴滃搫浼愬Λ鈧弻銉︽Ц閸氾附妯夊妤勭箖鎼达妇绨跨涵顕嗙礉T120+ 闁插秵鏌婄拋鎹愵吀閵?  - N04 accepted閿涙瓪exporters/` 缂傚搫鐨?`__init__.py` 瑜版挸澧犳稉宥呭閸?Python 3 namespace package 鐎电厧鍙嗛妴?  - N05 accepted閿涙碍婀担璺ㄦ暏 helper 閺冪姴缍嬮崜宥夘棑闂勨晪绱濋崣顖氭躬 T114+ 缁夊娅庨幋鏍﹀▏閻劊鈧?
## 11. T114 / M1 鐎瑰本鍨氱拋鏉跨秿

- 閺傚洦銆傞弨鐟板З閿?  - `docs/review/T114_milestone_review.md`
  - `docs/review/T114_review.md`
  - `docs/review/M1_review.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Worker milestone sample:
  - sample run directory: `private/distilled/t102_smoke`
  - artifact chain present: `normalized_events.jsonl`閵嗕梗chunks.jsonl`閵嗕梗chunk_summaries.jsonl`閵嗕梗memory_facts.jsonl`閵嗕梗contact_skill.candidate.json`閵嗕梗contact_skill.review.md`閵嗕梗run_report.json`
  - sample summary: 12 normalized events, 1 chunk, 1 chunk summary, 7 memory facts, candidate ContactSkill.
  - worker audited 7/7 memory facts, exceeding the required 5 facts.
- Reviewer conclusion:
  - `docs/review/T114_review.md` verdict 娑?`PASS_WITH_WARNINGS`閵?  - Gate M1 verdict = `Conditional` confirmed.
  - Reviewer independently checked all 7 memory facts against normalized events.
  - All Gate M1 hard requirements passed.
- Captain milestone review:
  - `docs/review/M1_review.md` verdict = `Conditional`閵?  - M2 may proceed only with candidate-only / human-review-first semantics.
- Warning / condition handling:
  - T114 N01/N02 accepted閿涙inor semantic elevation/paraphrase in candidate-only facts, handled by human review and R030.
  - T114 N03 accepted閿涙ample too small for generalization, represented by Gate M1 `Conditional`.
  - T114 N04 accepted閿涙o report inconsistency found; no action.
- R028/R029/R030 remain active into M2.

## 12. T120 鐎瑰本鍨氱拋鏉跨秿

- 娴狅絿鐖?/ 閺傚洦銆傞弨鐟板З閿?  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/contact_skill.py`
  - `docs/07_handoff.md`
- 瀹告彃鐤勯悳鏉垮敶鐎圭櫢绱?  - 閸?`core.models` 娑擃厽鏌婃晶?T120 file-store 閻╃鍙уΟ鈥崇€烽敍?    - `ContactSkillRedactionPolicy`
    - `DistilledArtifactReviewDecision`
    - `DistilledArtifactReviewMetadata`
    - `DistilledArtifactSourceMetadata`
    - `MemoryFactStoreRecord`
    - `MemoryFactStoreFile`
    - `ContactSkillStoreRecord`
    - `ContactSkillStoreFile`
  - 娑?`MemoryFactCandidate` 婢х偛濮為弰鎯х础閺勭姴鐨?helper閿?    - `to_runtime_memory_type()`
    - `to_memory_fact(...)`
    - 娴犲懏褰佹笟娑樻倵缂?T123/T121 閸欘垰顦查悽銊︽Ё鐏忓嫸绱濇稉宥呮躬閺堫剝鐤嗛崑?runtime 濞夈劌鍙嗛妴?  - 鐏?`ContactSkillCandidate.redaction_policy` 娴犲骸顔旈弶?`dict[str, Any]` 閺€鍓佹彛娑撹櫣绮ㄩ弸鍕 `ContactSkillRedactionPolicy`閵?  - 閸?`contact_skill.py` 娑擃厽鏌婃晶?`ContactSkillFileStoreService`閿涘本鏁幐渚婄窗
    - 娴?legacy `memory_facts.jsonl` 閸栧懓顥婇獮璺哄鏉?`MemoryFactStoreFile`
    - 娴?legacy `contact_skill.candidate.json` 閸栧懓顥婇獮璺哄鏉?`ContactSkillStoreFile`
    - 娣囨繂鐡?`memory_fact_store.json` / `contact_skill_store.json`
    - 娣囨繄鏆€ `status`閵嗕梗evidence_refs`閵嗕梗source_run_id`閵嗕够ource artifact path閵嗕够ource chunk/memory/event ids閵嗕购eview metadata
  - `review_metadata.is_runtime_ready(...)` / record-level `is_runtime_ready()` 閸欘亜婀?`status="approved"` 娑?`reviewed_by_human=True` 閺冩儼绻戦崶?true閿涘奔绻氶幐?candidate-only / human-review-first 鐠囶厺绠熼妴?  - 閺堫亝鏌婃晶?CLI閵嗕焦婀弨瑙勬殶閹诡喖绨遍妴浣规弓瀵洖鍙嗛崥鎴﹀櫤鎼存挶鈧焦婀崑?runtime prompt 濞夈劌鍙嗛妴浣规弓閼奉亜濮?approve閵?- 瀹告彃鐣幋鎰扮崣鐠囦緤绱?  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/core/models.py src/practical_chat_agent/services/contact_skill.py`
  - 娴ｈ法鏁ら崥鍫熷灇閼磋鲸鏅遍弽铚傜伐鏉╂劘顢戦張鈧亸?load/save 闂傤厾骞嗘宀冪槈閿涘牊婀拠璇插絿閻喎鐤勯懕濠傘亯閸樼喐鏋冮敍澶涚窗
    - 閻㈢喐鍨?legacy fixture 娴?`private/distilled/t120_store_smoke/legacy/`
    - 閻?`ContactSkillFileStoreService` 閸旂姾娴?legacy `memory_facts.jsonl` / `contact_skill.candidate.json`
    - 閸愭瑥鍤?store 閺傚洣娆㈤崚?`private/distilled/t120_store_smoke/store/memory_fact_store.json`
    - 閸愭瑥鍤?store 閺傚洣娆㈤崚?`private/distilled/t120_store_smoke/store/contact_skill_store.json`
    - 閸愬秵顐奸崶鐐额嚢楠炶埖鏌囩懛鈧敍?      - memory statuses = `candidate`, `approved`
      - skill statuses = `approved`
      - `evidence_refs` 閺堫亙娑径?      - `source_memory_ids` / source event ids / source chunk ids 娣囨繄鏆€
      - approved record 閻?`review_metadata.reviewed_by_human`閵嗕梗last_decision`閵嗕弓istory 娣囨繄鏆€
      - `is_runtime_ready()` 娴犲懎顕?synthetic approved records 鏉╂柨娲?true
- Reviewer 缂佹捁顔戦敍?  - `docs/review/T120_review.md` verdict 娑?`PASS_WITH_WARNINGS`閵?  - 绾喛顓?T120 閸欘亜鐤勯悳?file store models 閸?service閿涘奔绗夐崑?CLI閵嗕笍B migration閵嗕箍ector DB閵嗕购untime prompt injection 閹?auto-approve閵?  - 绾喛顓?`is_runtime_ready()` 闂団偓鐟?`status="approved"`閵嗕梗reviewed_by_human=True`閵嗕梗last_decision="approved"` 娑撳鍣搁弶鈥叉閿涘奔绻氶幐?candidate-only / human-review-first閵?  - 绾喛顓?legacy T112/T113 artifacts 閸欘垰瀵樼憗鍛礋 store records閿涘奔绗?evidence refs閵嗕够ource ids閵嗕购eview metadata 閸?load/save round-trip 娣囨繄鏆€閵?- Warning 婢跺嫮鎮婇敍?  - N01 accepted閿涙瓪updated_at` no-op normalization 娴ｅ骸濂栭崫宥忕礉娑撳秷顩﹀Ч鍌濈箲娣囶噯绱盩122 閺囧瓨鏌?review 閻樿埖鈧焦妞傞崘宥嗘绾?timestamp 鐠囶厺绠熼妴?  - N02 accepted閿涙瓪ContactSkillBuilderService` 娑?`ContactSkillFileStoreService` 閻?path/helper duplication 鐎?MVP 閸欘垱甯撮崣妤嬬礉閺嗗倷绗夐幎钘夊彙娴滎偄鐔€缁眹鈧?  - N03 accepted閿涙ingle-record store shape 閸忕厧顔愰崗銉ュ經娓氬灝鍩勬潻浣盒╅敍瀛瓂dantic downstream validation 鐡掑啿顧勯崗婊冪俺閵?  - N04 accepted閿涙瓪DistillationMemoryType` 閸?runtime `MemoryType` 閻ㄥ嫮鐭栫划鎺戝閺勭姴鐨犵粭锕€鎮?MVP granularity閵?  - N05 deferred閿涙俺鍤滈崝銊ュ濞村鐦悾娆戠舶 T150閿涘本鏌婃晶?R031 鐠虹喕閲?store model validation閵嗕勾egacy wrapping閵嗕勾oad/save round-trip閵嗕购untime-ready gate 閸?path confinement 濞村鐦妴?- 瑜版挸澧犲▔銊﹀壈閻愮櫢绱?  - 閻喎鐤?approve / reject / freeze CLI 娴犲秶鏆€缂?T122閵?  - evidence existence/support 閺嶏繝鐛欓悽?T121 閹垫寧甯撮敍瀹甶ssing refs 韫囧懘銆忛梼缁橆剾 approval閵?
## 13. T121 鐎瑰本鍨氱拋鏉跨秿

- 娴狅絿鐖?/ 閺傚洦銆傞弨鐟板З閿?  - `src/practical_chat_agent/services/evidence_validation.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- 瀹告彃鐤勯悳鏉垮敶鐎圭櫢绱?  - 閺傛澘顤?`EvidenceValidationService`閿涘矂鈧俺绻?T120 `ContactSkillFileStoreService` 閸旂姾娴?memory/contact-skill store records閵?  - 娴?same-run artifacts 瀵よ櫣鐝?evidence id index閿?    - `normalized_events.jsonl`
    - `chunks.jsonl`
    - `chunk_summaries.jsonl`
    - `memory_facts.jsonl`
    - `contact_skill.candidate.json`
    - T120 store records 閼奉亣闊?  - 闁帒缍婇幍顐ｅ伎 serialized model payload 娑擃厽澧嶉張?nested `evidence_refs`閵?  - 鏉堟挸鍤В蹇庨嚋 record 閻?checked refs閵嗕沟issing refs閵嗕苟ested ref locations閵嗕垢rovenance snapshot閵嗕购eview metadata snapshot閵嗕工pproval/runtime block reasons閵?  - 閻樿埖鈧浇顫夐崚娆欑窗
    - `candidate` 姒涙顓?blocked from approval/runtime閵?    - `approved` 閼汇儱鐡ㄩ崷?missing refs閿涘苯鍨?blocked from approval/runtime閵?    - `rejected` / `frozen` / `archived` 娑撳秴褰?runtime-ready閵?    - `approved` 娑?refs OK 娴ｅ棙婀?human-reviewed閿涘苯褰ч懗?approval-ready閿涘奔绗夐懗?runtime-ready閵?  - 閺傛澘顤?`chatlog-validate-evidence` CLI閿涘本鏁幐?`--input`閵嗕梗--output`閵嗕梗--dry-run`閵?  - Validator 閸欘亝濮ら崨濠忕礉娑撳秴鍟撻崶?store metadata閿涘奔绗夐懛顏勫З approve閿涘奔绗夐崑?runtime integration閵?- 瀹告彃鐣幋鎰扮崣鐠囦緤绱?  - Compile passed閿?    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src\practical_chat_agent\services\evidence_validation.py src\practical_chat_agent\app\main.py`
  - Good case閿涙瓪private/distilled/t102_smoke` dry-run閵?    - `evidence_validation_status = passed`
    - `validated_record_count = 8`
    - `records_with_missing_refs = 0`
    - `missing_ref_count = 0`
    - `approval_blocked_records = 8`
    - `runtime_blocked_records = 8`
    - 鐟欙綁鍣撮敍姝砮fs 閸忋劑鍎寸€涙ê婀敍瀹篹cords 閸ョ姳绮涙稉?candidate 鐞氼偅顒滅涵顕€妯嗗顫偓?  - Bad case閿涙瓪private/distilled/t121_missing_ref_fixture/` synthetic fixture閵?    - `evidence_validation_status = failed`
    - `validated_record_count = 3`
    - `records_with_missing_refs = 1`
    - `missing_ref_count = 1`
    - approved memory record 閸?missing `evt_demo_2` 閸氬本妞?blocked from approval/runtime閵?  - Store-only case閿涙瓪private/distilled/t120_store_smoke/store` dry-run閵?    - `evidence_validation_status = failed`
    - `records_with_missing_refs = 3`
    - `missing_ref_count = 5`
    - 鐟欙綁鍣撮敍姝磘ore-only fixture without same-run evidence artifacts 鐞氼偅顒滅涵顔煎灲鐎?evidence-incomplete閵?- Reviewer 缂佹捁顔戦敍?  - `docs/review/T121_review.md` verdict 娑?`PASS_WITH_WARNINGS`閵?  - 绾喛顓?T121 閸欘亜鐤勯悳?read-only evidence validator 娑?CLI閿涘奔绗夐崑?auto-approve閵嗕工pprove/reject/freeze CLI閵嗕笍B migration閵嗕箍ector DB閵嗕购untime prompt injection閵嗕俯LM call 閹?`private/chat_history` 鐠囪褰囬妴?  - 绾喛顓?stdout/report 闂勬劕鍩楅崷?counts閵嗕够afe relative paths 閸?private `private/distilled/` report閿涘本婀崣鎴犲箛缁変礁鐦戦崘鍛啇鏉╂稑鍙?docs/examples/tests/stdout閵?- Warning 婢跺嫮鎮婇敍?  - N01 accepted閿涙艾缍嬮崜?`ContactSkillCandidate` 濞屸剝婀?stable skill artifact id閿涘畭_extract_contact_skill_ids` 鐎靛湱骞囬張?schema 娑撹櫣鈹栭敍娌燼llback 閸?`contact_id` 娑撳秴濂栭崫宥嗩劀绾喗鈧佲偓?  - N02 accepted/deferred閿涙SON/JSONL helper 瀹稿弶妲哥粭顑跨瑏娴犱粙鍣告径宥忕礉MVP 閸欘垱甯撮崣妤嬬幢T150 閹存牕鎮楃紒?refactor 閸欘垳绮烘稉鈧?file IO 楠炶泛娲栭弨?BOM handling閵?  - N03 accepted閿涙艾鍙?payload 闁帒缍婇幍?`evidence_refs` 閺?O(total dict nodes)閿涘苯缍嬮崜宥嗘殶閹诡噣鍣洪弮鐘斥偓褑鍏樻搴ㄦ珦閵?  - N04 accepted閿涙alidator read-only閵嗕椒绗夐崘娆忔礀 `review_metadata.evidence_validation_status` 閺勵垱顒滅涵顔款啎鐠佲槄绱盩122 閸愬啿鐣鹃弰顖氭儊閺嶈宓?report 閸愭瑥鍙?review metadata閵?  - N05 deferred閿涙俺鍤滈崝銊ュ濞村鐦悾娆戠舶 T150閿涘本鏌婃晶?R032 鐠虹喕閲?evidence index閵嗕苟ested refs閵嗕够tatus rules閵嗕沟issing refs blocking閵嗕弓uman review gate interaction 閸?path confinement 濞村鐦妴?- 瑜版挸澧犲▔銊﹀壈閻愮櫢绱?  - T122 approve 韫囧懘銆忕拠璇插絿閹存牞顩﹀Ч鍌炩偓姘崇箖 T121 evidence validation report閵?  - T122 娑撳秴绶遍崷?missing refs閵嗕焦婀?human review 閹?rejected/frozen/archived 閻樿埖鈧椒绗呯紒鏇＄箖 gate閵?
## 14. T122 鐎瑰本鍨氱拋鏉跨秿

- 娴狅絿鐖?/ 閺傚洦銆傞弨鐟板З閿?  - `src/practical_chat_agent/services/contact_skill.py`
  - `src/practical_chat_agent/exporters/contact_skill_markdown.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- 瀹告彃鐤勯悳鏉垮敶鐎圭櫢绱?  - 閺傛澘顤?`ContactSkillStoreReviewService`閿涘本鏁幐?list/apply decision/export review artifact閵?  - 閺傛澘顤?`chatlog-review-store` CLI with actions:
  - `list`
  - `approve`
  - `reject`
  - `freeze`
  - `archive`
  - `export`
  - T122 scope kept to private file-store review only:
    - no runtime integration
    - no DB migration
    - no vector DB
    - no LLM call
    - no auto-send
  - Review flow implemented:
    - input/output confined to `private/distilled/**`
    - safe record listing with record id, artifact type/id, status, review state, evidence validation status, approval/runtime-ready summary, and safe relative path
    - `approve` requires T121 `evidence_validation_report.json`
    - `approve` blocks on report status != `passed`
    - `approve` blocks on target-record missing refs
    - `approve` blocks for current status in `rejected` / `frozen` / `archived`
    - `reject` / `freeze` / `archive` update payload status plus review metadata/history and keep runtime-ready false
    - decision metadata writes reviewer id/name, reviewed timestamp, notes, and evidence validation status into `review_metadata`
    - export writes markdown safe summaries only under `private/distilled/**`
  - legacy wrapped records now get deterministic stable `record_id` values derived from run id + artifact id, so T121 report lookup and T122 CLI targeting stay stable across reloads.
  - store save preserves store-level `generated_at`.
- Private fixtures / safe samples used:
  - safe sample: `private/distilled/t102_smoke`
  - missing-ref sample: `private/distilled/t121_missing_ref_fixture`
  - T122 private verification fixtures:
    - `private/distilled/t122_pass_fixture`
    - `private/distilled/t122_reject_fixture`
    - `private/distilled/t122_freeze_fixture`

- 瀹告彃鐣幋鎰扮崣鐠囦緤绱?  - compile:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src\practical_chat_agent\app\main.py src\practical_chat_agent\services\contact_skill.py src\practical_chat_agent\exporters\contact_skill_markdown.py`
    - result: passed
  - safe list:
    - `chatlog-review-store --input private/distilled/t120_store_smoke/store --action list`
    - result: stdout only contains safe ids, status fields, counts, and private-relative paths
  - passed validation fixture:
    - `chatlog-validate-evidence --input private/distilled/t122_pass_fixture`
    - result: `evidence_validation_status = passed`
  - approve happy path:
    - `chatlog-review-store --input private/distilled/t122_pass_fixture --action approve --record-id skillstore_bae8944df32d64b2 --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Approved after passed evidence validation.'`
    - result: wrote `private/distilled/t122_pass_fixture/contact_skill_store.json`
    - confirmed `status = approved`, `reviewed_by_human = true`, `last_decision = approved`, reviewer fields set, `last_reviewed_at` populated, `evidence_validation_status = passed`, decision appended to `history`, and `updated_at` advanced
  - reject path:
    - `chatlog-validate-evidence --input private/distilled/t122_reject_fixture`
    - `chatlog-review-store --input private/distilled/t122_reject_fixture --action reject --record-id skillstore_0edb3e3030c16049 --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Rejected for narrower human rewrite before approval.'`
    - result: wrote `private/distilled/t122_reject_fixture/contact_skill_store.json`
    - confirmed `status = rejected`, decision appended, runtime-ready summary remained false
  - freeze path:
    - `chatlog-validate-evidence --input private/distilled/t122_freeze_fixture`
    - `chatlog-review-store --input private/distilled/t122_freeze_fixture --action freeze --record-id skillstore_4e33506d02e1e966 --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Frozen pending broader sample review.'`
    - result: wrote `private/distilled/t122_freeze_fixture/contact_skill_store.json`
    - confirmed `status = frozen`, decision appended, runtime-ready summary remained false
  - missing-ref approve block:
    - `chatlog-review-store --input private/distilled/t121_missing_ref_fixture --action approve --record-id memstore_37bae56b191844de --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Should be blocked by missing refs.'`
    - result: correctly blocked with `Approve is blocked because the target record still has missing evidence refs in the validation report.`
    - checked target fixture file stayed unchanged after the blocked command
  - export path:
    - `chatlog-review-store --input private/distilled/t122_pass_fixture --action export --output private/distilled/t122_pass_fixture/review_exports`
    - result: wrote `private/distilled/t122_pass_fixture/review_exports/store_review_export.md`
    - checked exported markdown contains safe review metadata only, not raw chat transcript output

- Reviewer 缂佹捁顔戦敍?  - `docs/review/T122_review.md` verdict 娑?`PASS_WITH_WARNINGS`閵?  - 绾喛顓?T122 閸欘亜鐤勯悳?private file-store review CLI閿涘奔绗夐崑?auto-approve閵嗕购untime integration閵嗕笍B migration閵嗕箍ector DB閵嗕俯LM閵嗕工uto-send 閹?`private/chat_history` 鐠囪褰囬妴?  - 绾喛顓?approve gate 鐎瑰本鏆ｉ敍姘舵付鐟?T121 validation report閵嗕购eport `passed`閵嗕辜arget record present閵? missing refs閵嗕恭hecked refs > 0閿涘苯鑻熼梼缁橆剾 rejected/frozen/archived re-approval閵?  - 绾喛顓?review metadata history閵嗕够afe export閵嗕垢ath confinement閵嗕够table record_id 閸?no private data stdout 閸у洦寮х搾鍏呮崲閸斺€冲瘶閵?- Warning 婢跺嫮鎮婇敍?  - N01 accepted閿涙瓪del current_status` 閺勵垯缍嗚ぐ鍗炴惙閹恒儱褰?妞嬪孩鐗搁梻顕€顣介敍灞肩瑝瑜板崬鎼?correctness閵?  - N02 accepted閿涙岸鈧帒缍婇弴瀛樻煀閹碘偓閺堝鎮庡▔?`status` 鐎涙顔岀粭锕€鎮庤ぐ鎾冲 schema閿涙稖瀚㈤張顏呮降 schema 閸戣櫣骞囨稉宥呮倱鐠囶厺绠熼惃?status 鐎涙顔岄崘宥夊櫢鐎孤扳偓?  - N03 accepted閿涙瓪store_runtime_ready` 閹绘劕澧犵拋锛勭暬閸欘亝妲告潪璇蹭簳 style note閵?  - N04 accepted/deferred閿涙eview service 鐠佸潡妫?file store private helpers 鐎?MVP 閸欘垱甯撮崣妤嬬幢閺堫亝娼甸崣顖涘▕ public file/path utility閵?  - N05 accepted閿涙utable `_StoreWorkspace` 瑜版挸澧犵仦鈧柈銊ュ讲閹貉佲偓?  - N06 deferred閿涙俺鍤滈崝銊ュ濞村鐦悾娆戠舶 T150閿涘本鏌婃晶?R033 鐠虹喕閲?approval gate閵嗕购eject/freeze/archive閵嗕购eview history閵嗕购ecursive status update閵嗕躬xport path confinement閵嗕够table record_id 閸?no-auto-approve 濞村鐦妴?- 瑜版挸澧犲▔銊﹀壈閻愮櫢绱?  - T123 韫囧懘銆忛崣顏囶嚢閸?approved + runtime-ready records閵?  - T123 娑撳秴绶卞▔銊ュ弳 candidate/rejected/frozen/archived閿涘奔绗夊妤€濮炴潪钘夌暚閺?skill 閹存牕鍙忛柈?memory 閸?prompt閵?  - T122 intentionally does not implement reopen; rejected/frozen/archived records remain non-approvable in this scope.

## 15. Worker 閸氼垰濮╅幓鎰仛

```text
娴ｇ姵妲?Codex worker閵?
鐠囧嘲鍘涢梼鍛邦嚢閿?- README.md
- AGENTS.md
- docs/02_experiment_plan.md
- docs/06_eval_protocol.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/review/T123_review.md
- docs/review/T130_review.md
- docs/review/T131_review.md
- docs/review/T132_review.md
- docs/data_contracts/reply_plan_contract.md
- docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md

閺堫剝鐤嗛崣顏勭暚閹存劧绱?- docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md

鐟欏嫬鍨敍?1. 閸欘亝鏁?Allowed files閵?2. 閸欘亜浠涢崠鍨倳 holdout eval 閸?Gate M3 閸掋倖鏌囬敍灞肩瑝娣囶喗鏁?planner 娴狅絿鐖滈妴?3. 鐠囧嫪鍙?T130-T132 鏉堟挸鍤惃鍕殰閻掕泛瀹抽妴浣界珶閻ｅ矂浼掔€瑰牄鈧浇鐦夐幑顔诲▏閻劊鈧购isk flags 閸欘垵袙闁插﹥鈧冩嫲闂呮劗顫嗙€瑰鍙忛妴?4. 閸欘垯浜掔拠璇插絿 private/distilled 娑撳娈戠粔浣规箒鐠囧嫪鍙婃潏鎾冲毉閿涘奔绲炬稉宥呯繁閹?holdout 閸樼喐鏋冮妴浣烘埂鐎圭偠浠堢化璁虫眽閸氬秲鈧胶婀＄€圭偛閽╅崣?ID 閹存牕褰茬拠鍡楀焼閸愬懎顔愰崘娆忓弳 docs閵?5. 娑撳秷鍤滈崝銊ュ絺闁緤绱濇稉宥嗗复閺佺増宓佹惔鎿勭礉娑撳秴绱╅崗銉ユ倻闁插繑鏆熼幑顔肩氨閿涘奔绗夌拠璇插絿 `private/chat_history/`閵?6. 娑撳秳鎱ㄦ径宥勫敩閻胶宸遍梽鍑ょ幢閼汇儱褰傞悳?blocking code issue閿涘苯褰ч崷?review 娑擃叀顔囪ぐ鏇炶嫙缂佹瑥鍤?Gate M3 `Block` 閹?`Conditional` 閻炲棛鏁遍妴?7. 鏉堟挸鍤?`docs/review/T133_milestone_review.md`閿涘苯鑻熼弴瀛樻煀 `docs/07_handoff.md`閵?8. 閺堚偓閸氬孩濮ら崨濠忕窗鐠囧嫪鍙婇弽閿嬫拱瑜般垺鈧降鈧礁灏堕崥宥嗗瘹閺嶅洢鈧笩ate M3 verdict閵嗕礁澧挎担娆擃棑闂勨斂鈧?```

## 16. Reviewer 閸氼垰濮╅幓鎰仛

```text
娴ｇ姵妲?Claude Code reviewer閵?
鐠囧嘲鍘涢梼鍛邦嚢閿?- docs/02_experiment_plan.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/06_eval_protocol.md
- docs/review/T123_review.md
- docs/review/T130_review.md
- docs/review/T131_review.md
- docs/review/T132_review.md
- docs/data_contracts/reply_plan_contract.md
- docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md

閸欘亣顕扮€光剝鐓￠張顒侇偧 diff閿涘奔绗夌憰浣锋叏閺€瑙勬瀮娴犺翰鈧?
闁插秶鍋ｅΛ鈧弻銉窗
1. T133 閺勵垰鎯侀崣顏勪粵 read-only / docs-only 閻?holdout eval閿涘奔绗夋穱顔芥暭 planner 娴狅絿鐖滈妴?2. 閺勵垰鎯侀崶鐐电摕 Gate M3 閸忔娊鏁梻顕€顣介敍姘冲殰閻掕泛瀹抽妴浣界珶閻ｅ矂浼掔€瑰牄鈧浇鐦夐幑顔诲▏閻劊鈧购isk flags 閸欘垵袙闁插﹥鈧佲偓渚€娈ｇ粔浣哥暔閸忋劊鈧?3. 閺勵垰鎯佸▽鈩冩箒 holdout 閸樼喐鏋冮妴浣烘埂鐎圭偠浠堢化璁虫眽閸氬秲鈧胶婀＄€圭偛閽╅崣?ID 閹存牕褰茬拠鍡楀焼 private content 鏉╂稑鍙?docs/examples/tests/stdout閵?4. 閺勵垰鎯佹俊鍌氱杽鐠佹澘缍?T131/T132 deterministic templates閵嗕共eyword false positives 閸滃瞼宸辩亸?committed tests 閻ㄥ嫰妾洪崚韬测偓?5. Gate M3 verdict 閺勵垰鎯佹稉?`Allow` / `Conditional` / `Block`閿涘苯鑻熺紒娆忓毉閸欘垱澧界悰灞炬蒋娴犺翰鈧?6. 閼?verdict 閸忎浇顔忔潻娑樺弳娑撳绔撮梼鑸殿唽閿涘本妲搁崥锔芥绾喚顩﹀銏ｅ殰閸斻劌褰傞柅浣告嫲鐎圭偞妞傞獮鍐插酱閹恒儱鍙嗙紒褏鐢荤搾濠勬櫕閵?
鏉堟挸鍤?Verdict: PASS / PASS_WITH_WARNINGS / BLOCK閿涘苯鑻熺€光剝鐓?`docs/review/T133_milestone_review.md`閵?```

## 17. 娑撳绔村銉┿€庢惔?
1. 閸欘垱褰佹禍銈呯秼閸?T132 worker/reviewer 娴狅絿鐖滄稉?Captain 閺€璺哄經閺傚洦銆傞崣妯绘纯閵?2. 娑撳绔存潪?worker 閸欘亝澧界悰?T133閿涘奔绗夌憰浣藉殰妫?M4閵?3. 閼?T133 review `BLOCK`閿涘瘍orker 閸欘亙鎱?blocking issue 閹存牞藟閸?blocking evaluation evidence閿涘苯鑻熼張鈧径姘冲殰閸斻劌顦茬€光€茬濞喡扳偓?4. 閼?T133 review `PASS` 閹?`PASS_WITH_WARNINGS`閿涘瓔aptain 閸愬秵娲块弬鐗堜笉閻炲棙鏋冨锝呰嫙閸愬啿鐣?Gate M3 閺勵垰鎯侀崗浣筋啅鏉╂稑鍙?M4閵?5. M3 娴犲秳绻氶幐?review-only閿涙稐绗夌憰浣哥杽閻滄媽鍤滈崝銊ュ絺闁焦鍨ㄧ€圭偞妞傞獮鍐插酱閹恒儱鍙嗛妴?
## 18. 閸樺棗褰舵い鍝勭碍

1. T100 review `PASS`閿涘苯鍑＄€瑰本鍨?schema profile 娑?normalized event contract閵?2. T101 review `PASS`閿涘苯鍑＄€瑰本鍨?privacy/source_ref rules閵?3. T102 review `PASS`閿涘苯鍑＄€瑰本鍨?`chatlog-normalize` 閺堚偓鐏?CLI閵?4. T103 Gate M0 = `Conditional` accepted閿涘苯鍘戠拋姝岀箻閸?M1閵?5. T110 review `PASS`閿涘苯鍑＄€瑰本鍨?`chatlog-chunk` conversation chunker v0閵?6. T111 review `PASS`閿涘苯鍑＄€瑰本鍨?distillation output schemas 閸?JSON contract閵?7. T112 review `PASS`閿涘苯鍑＄€瑰本鍨氱亸蹇旂壉閺?summary/fact extraction 娑?evidence refs 閺嶏繝鐛欑粻锛勫殠閵?8. T113 review `PASS_WITH_WARNINGS`閿涘苯鍑＄€瑰本鍨?ContactSkill candidate builder 閸?Markdown review exporter閵?9. T114 review `PASS_WITH_WARNINGS`閿涘瓘ate M1 = `Conditional`閿涘2 閸欘垱娼禒璺烘儙閸斻劊鈧?10. T120 review `PASS_WITH_WARNINGS`閿涘苯鍑＄€瑰本鍨?file store models 娑?human-review-first gate閵?11. T121 review `PASS_WITH_WARNINGS`閿涘苯鍑＄€瑰本鍨?evidence validator 娑?missing-ref/status gate閵?12. T122 review `PASS_WITH_WARNINGS`閿涘苯鍑＄€瑰本鍨?skill review CLI 娑?approval gate閵?13. T123 review `PASS_WITH_WARNINGS`閿涘苯鍑＄€瑰本鍨?approved-store compact `ChatContext` integration閵?14. T130 review `PASS_WITH_WARNINGS`閿涘苯鍑＄€瑰本鍨?ReplyPlan schema 娑?prompt contract閵?15. T131 review `PASS_WITH_WARNINGS`閿涘苯鍑＄€瑰本鍨?review-only ReplyPlanner 娑?`chat-reply-plan` CLI閿涙笨132 鏉╂稑鍙?policy/boundary validation閵?16. T132 review `PASS_WITH_WARNINGS`閿涘苯鍑＄€瑰本鍨?ReplyPlanner policy/boundary 妞嬪酣娅撶仦鍌︾幢T133 鏉╂稑鍙嗛崠鍨倳 holdout eval閵?
## 19. 濞夈劍鍓版禍瀣€?
- `.gitignore` 娑擃厼鍑￠張?`private/`閿涘奔绻氶悾娆掔箹娑擃亜鐣ㄩ崗銊﹀妇閺傚鈧?- 娑撳秷顩︽潻妯哄斧閻劍鍩涢幍瀣З鏉╀胶些 docs 閻╊喖缍嶇紒鎾寸€惃鍕惙娴ｆ嚎鈧?- 娑撳秷顩︾拠璇插絿閹存牞绶崙?`.env`閵?- 娑撳秷顩﹂幎?`private/chat_history` 閻ㄥ嫮婀＄€圭偞鏋冩禒璺烘倳閹存牞浜版径鈺佸敶鐎圭懓鍟撻崗?docs閵?- 瑜版挸澧犻梼鑸殿唽娑撳秴浠涘顔跨殶閵嗕椒绗夐崑姘冲殰閸斻劌褰傞柅浣碘偓浣风瑝閸嬫艾浜曟穱鈩冨閹诲繈鈧?- M2 閸欘垯浜掗幒銊ㄧ箻閿涘奔绲捐箛鍛淬€忕敮锔炬絻 Gate M1 Conditional 閺夆€叉缂佈呯敾妤犲矁鐦夐敍灞肩瑝鐟曚焦濡?M1 閸愭瑦鍨氶弮鐘虫蒋娴犺泛鐣幋鎰┾偓?
## 20. T123 Completion Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/chat_context.py`
  - `src/practical_chat_agent/app/container.py`
  - `docs/07_handoff.md`
- Implemented:
  - Added `approved_store_context` to `ChatContext`.
  - Added compact store brief models: `ApprovedStoreContext`, `ApprovedContactSkillBrief`, and `ApprovedMemoryFactBrief`.
  - Extended `ChatContextAssembler` with optional approved-store loading from `private/distilled/**`.
  - Context assembly now adds compact approved-store hints into `summary` and `memory_retrieval_notes`.
  - Filtering is conservative: only records that are approved, human-reviewed, evidence-valid, and `is_runtime_ready() == True` can enter runtime context.
  - Candidate, rejected, frozen, archived, missing-evidence, and not-human-reviewed records are excluded.
  - The brief stays compact: short relationship summary, short strategy / boundary reminders, record ids, and evidence refs only. No raw transcript, no full JSON dump, no runtime prompt injection.
  - `AppContainer` now supports optional injection through `PRACTICAL_CHAT_APPROVED_STORE_PATH` and `PRACTICAL_CHAT_APPROVED_MEMORY_LIMIT`.
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/chat_context.py src/practical_chat_agent/core/models.py src/practical_chat_agent/app/container.py`
  - Approved fixture:
    - fixture: `private/distilled/t123_approved_fixture`
    - result: `approved_store_context.status = loaded`
    - loaded one approved contact-skill brief with safe record id / evidence refs, and summary / retrieval notes included compact approved-store hints
  - Exclusion fixture:
    - fixture: `private/distilled/t123_exclusion_fixture`
    - result: `approved_store_context.status = no_runtime_ready_records`
    - rejected store record did not enter context
  - Compatibility fixture:
    - fixture: `private/distilled/t123_memory_only_fixture`
    - result: approved contact-skill brief loaded correctly; approved memory record with missing refs stayed excluded
  - No-store compatibility:
    - direct `ChatContextAssembler()` run with no store path
    - result: `approved_store_context.status = not_configured`, and existing context assembly behavior stayed unchanged
- Remaining risk / assumption:
  - Current private fixtures verify the positive contact-skill path and the exclusion path. They do not yet provide a runtime-ready approved memory-only sample, so the positive memory-brief branch remains unobserved and should be re-checked when such a safe fixture exists.

## 21. T130 Completion Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/reply_plan_contract.md`
  - `docs/07_handoff.md`
- Implemented:
  - Added strongly typed reply-planning models:
    - `ReplyPlanContextRef`
    - `ReplyPlanSourceContext`
    - `ReplyPlanCandidate`
    - `ReplyPlan`
  - Added `ReplyPlanMode = "candidate_review_only"` to make the review-only usage explicit.
  - Added `ReplyPlanContextRefType` so candidates can cite:
    - approved contact-skill record ids
    - approved memory-fact record ids
    - approved store evidence refs
    - recent event ids
    - runtime memory hit ids
    - policy-boundary refs
  - `ReplyPlan` requires:
    - `contact_id`
    - `source_context`
    - `policy_boundary_summary`
    - `notes_on_candidate_differences`
    - at least 3 `candidates`
  - Each `ReplyPlanCandidate` requires:
    - `draft_text`
    - `rationale`
    - at least 1 `supporting_context_ref`
    - at least 1 `boundary_reminder`
    - optional `risk_flags` and `confidence`
  - Added `docs/data_contracts/reply_plan_contract.md` to document:
    - review-only usage boundary
    - anti-impersonation rule
    - conservative handling for uncertain/sensitive cases
    - compatibility with T123 `approved_store_context`
    - JSON shape and field semantics for T131/T132
- How T130 ties back to T123:
  - `ReplyPlanSourceContext.approved_store_status` directly reuses T123 `ApprovedStoreContextStatus`.
  - `ReplyPlanSourceContext` accepts T123 compact ids and refs:
    - `approved_contact_skill_record_id`
    - `approved_memory_record_ids`
    - `approved_store_evidence_refs`
  - The contract therefore consumes the compact approved-store brief from `ChatContext` instead of requiring full store JSON or raw transcript text.
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/core/models.py`
  - Synthetic model validation passed with a safe inline sample:
    - validated one `ReplyPlan` containing 3 candidates
    - confirmed candidates can cite T123-style approved-store record ids / evidence refs
    - confirmed raw transcript text is not required by the schema
    - confirmed `approved_store_status="loaded"` is compatible with T123 context status values
- Remaining risk / assumption:
  - T130 defines the contract only. It does not yet prove that T131 generation logic will consistently populate distinct, high-quality candidates from real runtime context.
  - T123 reviewer warning about contact-id alignment still applies: T131 should verify that runtime `contact_id` routing stays aligned with approved-store records when the planner is wired in.

- Review decision:
  - `docs/review/T130_review.md` verdict = `PASS_WITH_WARNINGS`.
  - Warning handling:
    - N01 accepted: single-value `ReplyPlanMode` is correct for current review-only scope.
    - N02 deferred to R034: T131 must enforce stable unique `priority_rank` values.
    - N03 accepted: free-form `approach_label` is acceptable for MVP.
    - N04 deferred to R034: T131 must verify `contact_id` alignment during assembly.
  - Captain decision: T130 is complete; T131 is the next Current Unique Task.

## 22. T131 Kickoff Notes

- Task package:
  - `docs/tasks/M3_relationship_reply_planner/T131_reply_planner.md`
- Worker focus:
  - Implement a review-only ReplyPlanner service or CLI.
  - Consume only compact approved-store context from T123.
  - Output T130 `ReplyPlan` with at least 3 candidates.
  - Preserve safety: no raw transcript, no send logic, no DB, no vector DB.
- Reviewer focus:
  - Candidate distinctness.
  - Cited refs and boundary reminders.
  - Unique ranking and contact/source alignment.
  - No scope creep into automatic sending or platform integration.

## 23. T131 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/reply_planner.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- Implemented:
  - Added `ReplyPlanner` service with a review-only `generate(context=...) -> ReplyPlan` flow.
  - The planner consumes only `ChatContext` plus T123 compact `approved_store_context` fields already present at runtime.
  - Added hard checks for the two T130 warning items:
    - `ReplyPlan.contact_id` must match `ChatContext.user_id`.
    - `ApprovedStoreContext.contact_id` and approved contact-skill `contact_id` must align with the routed contact id.
    - `priority_rank` values must be unique and form a stable `1..N` sequence.
  - Added a safe `chat-reply-plan` CLI command that:
    - reads a redacted or synthetic `ChatContext` JSON file
    - generates a `ReplyPlan`
    - prints only the plan JSON or writes it to an output file
    - does not print the raw input context
  - Candidate generation stays offline and review-only:
    - exactly 3 distinct candidate shapes are generated
    - each candidate includes draft text, rationale, supporting refs, risk flags, boundary reminders, and confidence
    - refs are limited to approved compact ids, evidence refs, recent event ids, runtime memory ids, and policy-boundary ids
  - The planner ignores `source_record_ids` lists, so non-approved ids such as candidate/rejected/frozen/archived record ids do not leak into the plan surface.
  - `source_context.chat_context_summary` is rebuilt as a safe count/status summary instead of copying `ChatContext.summary`, so raw message text is not echoed back into the plan.
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/app/main.py`
  - Safe synthetic context validation passed with an inline fixture:
    - contact id: `contact_lin`
    - approved contact-skill record id: `approved_skill_001`
    - approved memory record id: `approved_mem_001`
    - recent event id: `evt_recent_1`
    - runtime memory hit id: `mem_runtime_1`
    - extra non-approved ids were injected into `source_record_ids` only as a negative check
  - Validation results:
    - service emitted 3 candidates
    - CLI emitted 3 candidates through `chat-reply-plan --input <tempfile>`
    - candidate refs stayed within approved-store ids, evidence refs, recent event ids, runtime memory ids, and policy-boundary ids
    - injected `candidate_record_999` / `rejected_record_888` ids did not appear in the output plan
    - raw synthetic inbound text did not appear in the output plan JSON
    - contact-id mismatch raised `ReplyPlannerError` as expected
- Remaining risk / assumption:
  - T131 is heuristic and deterministic; it proves the safe planning surface and contract wiring, but not yet the final quality ceiling of relationship-aware wording.
  - The current verification used a synthetic safe context, not a larger runtime sample set, so candidate quality across more relationship types still needs review in T132 or manual evaluation.

## 24. T131 Review Decision

- Review file: `docs/review/T131_review.md`
- Verdict: `PASS_WITH_WARNINGS`
- Captain decision:
  - T131 is complete within task scope.
  - M3 is not complete yet; do not enter M4.
  - Current Unique Task moves to T132 Reply Policy.
- Warning handling:
  - N01 accepted/deferred: hardcoded templates and shallow relationship-awareness are acknowledged; deferred to R035 and T132/T133.
  - N02 accepted: hardcoded confidence values are acceptable for contract-wiring MVP.
  - N03 accepted/deferred: unused `strategy_hints` and `relationship_summary` are acknowledged; deferred to R035 and T132/T133.
  - N04 deferred: no committed tests/fixtures; deferred to R036 and T150.
  - N05 accepted: `_dedupe(values)` missing type annotation is low-risk style debt.
  - N06 accepted: enum fallback is sufficient for current MVP.

## 25. T132 Kickoff Notes

- Task package:
  - `docs/tasks/M3_relationship_reply_planner/T132_reply_policy.md`
- Worker focus:
  - Add boundary / avoid-topic / over-proactivity / impersonation risk checks to the existing T131 planner path.
  - Preserve review-only output and T130 `ReplyPlan` contract.
  - Keep the existing T131 contact alignment and ranking validation.
  - Use safe synthetic or redacted fixtures only.
- Reviewer focus:
  - Confirm no auto-send, DB, vector DB, realtime integration, raw transcript read, or full store JSON injection.
  - Confirm sensitive or boundary scenarios produce conservative candidates and explicit risk flags.
  - Confirm T132 does not claim final relationship-quality completion.

## 26. T132 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/reply_planner.py`
  - `src/practical_chat_agent/services/policy.py`
  - `docs/07_handoff.md`
- Implemented:
  - Added a reply-planning policy layer in `policy.py`:
    - `ReplyPlanPolicyProfile`
    - `ReplyCandidatePolicyAssessment`
    - `ReplyPlanPolicyEngine`
  - The new policy engine evaluates compact runtime context and candidate drafts for:
    - `boundary_sensitive`
    - `over_proactive`
    - `impersonation_risk`
    - `thin_context`
  - `ReplyPlanner` now builds a context-level policy profile before composing the plan, then applies candidate-level policy review when assembling each `ReplyPlanCandidate`.
  - Sensitive or boundary-heavy context now changes planner behavior in two ways:
    - policy-level summaries and boundary reminders become more explicit
    - draft templates switch to a more conservative, no-pressure wording set instead of the baseline T131 wording
  - Thin-context handling is now explicit through the policy layer rather than only through a generic boundary string:
    - candidate `risk_flags` carry `thin_context`
    - `policy_boundary_summary` explains that relationship-specific assumptions should be avoided
    - candidate confidence is reduced conservatively
  - Over-proactivity is now candidate-specific:
    - optional follow-up or next-step language is only escalated into `over_proactive` when the context is thin or boundary-sensitive
    - clearly no-pressure wording such as 閳ユ粌鍘涙稉宥呯窔閸撳秵甯?/ 娑撳秶鏁ら悳鏉挎躬鐏炴洖绱戦垾?is exempted from false-positive `over_proactive` flags
  - Impersonation risk is now explicitly detectable at the candidate-text level, even though the current T131/T132 templates do not intentionally generate such text.
  - T131 checks remain intact:
    - `contact_id` alignment still enforced
    - `priority_rank` uniqueness and stable `1..N` ordering still enforced
    - output remains review-only `ReplyPlan`, not send logic
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/services/policy.py src/practical_chat_agent/app/main.py`
  - Safe synthetic verification passed with three inline contexts:
    - baseline context:
      - approved contact-skill present
      - 3 candidates emitted
      - no raw input text echoed
      - no accidental `boundary_sensitive` / `over_proactive` over-blocking
    - boundary / avoid-topic context:
      - approved contact-skill carried explicit 閳ユ笀ive space / do not push閳?style reminders
      - 3 candidates emitted
      - at least one candidate carried `boundary_sensitive`
      - at least one candidate carried `over_proactive`
      - boundary reminders included explicit caution language
      - wording shifted to more conservative no-pressure drafts
    - thin-context context:
      - `approved_store_status = not_configured`
      - 3 candidates emitted
      - all candidates carried `thin_context`
      - boundary reminders explicitly warned against over-claiming familiarity
      - confidence stayed below the safe baseline and wording shifted to the conservative template set
  - Privacy / safety checks from the synthetic verification:
    - raw synthetic inbound text did not appear in the emitted `ReplyPlan`
    - output remained limited to compact ids, evidence refs, runtime ids, policy summaries, and candidate text
    - no `private/chat_history/` reads, no DB/persistence expansion, no vector DB, no send automation
- Remaining risk / assumption:
  - T132 improves safety behavior, but it is still heuristic keyword-based policy logic rather than evidence-weighted semantic classification.
  - The current policy layer does not yet use committed automated tests or committed synthetic fixtures; that regression coverage remains deferred to T150.
  - Relationship-aware wording quality is still limited by T131/T132 deterministic templates; T133 holdout evaluation is still needed before claiming strong reply quality.

## 27. T132 Review Decision

- Review file: `docs/review/T132_review.md`
- Verdict: `PASS_WITH_WARNINGS`
- Captain decision:
  - T132 is complete within task scope.
  - M3 is not complete yet; do not enter M4.
  - Current Unique Task moves to T133 Holdout Eval.
- Warning handling:
  - N01 accepted: runtime text is consumed for keyword detection only and is not echoed.
  - N02 accepted: broad keyword risk is mitigated by compound trigger logic.
  - N03 accepted/deferred: substring false-positive risk is acknowledged; deferred to R037 and T133/T150.
  - N04 accepted: `_dedupe` duplication is low-risk refactor debt.
  - N05 deferred: no committed tests/fixtures; folded into R036 and T150.
  - N06 accepted: duplicate terminal branch has no correctness impact.
  - N07 accepted: approved memory claim text is bounded and used for detection only.

## 28. T133 Kickoff Notes

- Task package:
  - `docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`
- Worker focus:
  - Run an anonymized holdout evaluation of T130-T132 ReplyPlanner behavior.
  - Assess naturalness, boundary adherence, evidence/reference usage, policy risk flags, and privacy safety.
  - Produce `docs/review/T133_milestone_review.md` with Gate M3 verdict: `Allow`, `Conditional`, or `Block`.
  - Update `docs/07_handoff.md` with eval summary and remaining risks.
- Reviewer focus:
  - Confirm no private raw content or identifying details entered committed docs.
  - Confirm the eval did not modify planner code or advance M4.
  - Confirm Gate M3 verdict is supported by evidence rather than assertion.

## 29. T133 Eval Record

- Private eval artifacts produced under:
  - `private/distilled/t133_holdout_eval/contexts/*.context.json`
  - `private/distilled/t133_holdout_eval/plans/*.reply_plan.json`
  - `private/distilled/t133_holdout_eval/eval_summary.json`
- Eval coverage:
  - 6/6 synthetic anonymized scenarios produced valid 3-candidate ReplyPlans.
  - Baseline and work cases stayed low-pressure and review-only.
  - Sensitive and thin-context cases became more conservative, with explicit boundary flags.
  - False-positive probe showed the policy layer can still swing conservative on a normal-looking work prompt.
  - False-negative probe showed subtle pacing risk may still be under-detected when no explicit boundary cue is present.
- Gate M3 verdict:
  - `Conditional`
- Handoff note:
  - Keep T131/T132/T133 treated as review-only planning proof, not as final relationship-quality proof.
  - Next recommended action for Captain: review T133, carry the conditions into T150, and only then decide whether M4 can proceed.

## 30. T133 Review Decision

- Review file: `docs/review/T133_review.md`
- Verdict: `PASS_WITH_WARNINGS`
- Captain decision:
  - T133 is complete within task scope.
  - Gate M3 remains `Conditional`.
  - M4/T140 may proceed only under the conditions carried in `docs/review/M3_review.md`.
- Warning handling:
  - N01 accepted: self-reported ratings are acceptable for MVP milestone; T150 may add independent review.
  - N02 accepted: 6 synthetic scenarios are reasonable under task constraints.
  - N03 accepted: naturalness 3/5 is honestly reported; do not claim relationship-aware maturity.
  - N04 accepted: evidence usage 3/5 is honestly reported; structural wiring is correct.
  - N05 accepted: H01/H02 detail omission is minor because summary confirms all six scenarios produced valid plans.
  - No deferred warnings.
  - No rejected warnings.

## 31. M3 Review Decision

- Review file: `docs/review/M3_review.md`
- Verdict: `Conditional`
- Completion judgment:
  - M3 is structurally complete: T130 schema, T131 planner, T132 policy layer, and T133 holdout eval are all present.
  - M3 is not quality-mature: drafts remain deterministic/template-driven, naturalness is 3/5, and evidence usage is 3/5.
  - Clean-environment reproducibility is not fully proven because committed regression tests/fixtures are still missing.
- Conditions carried forward:
  - ReplyPlanner remains review-only; no auto-send, realtime platform integration, or LLM drafting expansion.
  - T150 must add committed regression tests for structure, boundary sensitivity, thin context, false positives, subtle false negatives, privacy leakage, contact alignment, and ranking.
  - Do not claim relationship-aware maturity until broader sample recalibration.

## 32. T140 Kickoff Notes

- Task package:
  - `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`
- Worker focus:
  - Define feedback log schema for accept/edit/reject/boundary feedback on `ReplyPlan` candidates.
  - Implement a minimal CLI that records feedback to a private log.
  - Validate candidate references against a supplied `ReplyPlan`.
  - Keep stdout safe and avoid printing full draft text, edited text, private notes, raw transcript, or private paths.
- Forbidden:
  - Do not auto-send.
  - Do not modify ContactSkill, MemoryFact, approved store records, or planner templates automatically.
  - Do not introduce DB/vector DB/realtime integration/LLM calls.
  - Do not read from `private/chat_history/`.
- Reviewer focus:
  - Confirm feedback is recorded but not applied.
  - Confirm all M3 conditional constraints remain intact.
  - Confirm invalid candidate references fail safely.
  - Confirm no private content enters committed docs.

## 33. Roadmap Alignment Decision

- Reference reviewed:
  - `docs/reference/gpt閻ㄥ嫬鎮楃紒顓☆啎鐠佲剝鈧繆鐭?閺囧瓨鏌婇悧?.md`
- Captain judgment:
  - The document matches the project direction: review-first, ContactSkill compatibility, delayed platform integration, delayed external memory, and no automatic sending.
  - The task board needed modification because old T141/T142 moved too quickly into proposal/versioning, while M3 is still conditional and T140 has not produced validated feedback yet.
- Changes made:
  - M4 now contains T140 feedback capture, T141 feedback log validator, and T142 feedback summary exporter.
  - M4.5 now contains T150 ReplyPlanner regression tests, T151 policy fixture suite, and T152 feedback CLI regression tests.
  - M5 now starts feedback-to-patch with T160-T164.
  - M6-M12 now describe staged ContactSkill decomposition, optional LLM planner, RelationshipState, MemoryRetriever, BehaviorPlanner, OutboundSendGate/Feishu, and WeChat adapter.
- Current Unique Task remains:
  - T140 Feedback Schema CLI.
- Important non-goals:
  - Do not implement Mem0, Feishu, WeChat, BehaviorPlanner, LLM drafting, or ContactSkill replacement before their gated milestones.

## 34. T140 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/feedback.py` (new)
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- Schema/service/CLI behavior:
  - Added `ReplyFeedbackAction` = Literal["accept", "edit", "reject", "boundary"].
  - Added `ReplyFeedbackRecord` with feedback_id, created_at, contact_id, reply_plan_id, candidate_id, priority_rank, action, user_note, edited_text, boundary_label, boundary_note, source_plan_path.
  - Added `ReplyFeedbackLog` with schema_version, generated_at, records list.
  - `FeedbackService.record_feedback()` loads a ReplyPlan JSON, validates the chosen candidate exists by priority_rank, appends a feedback record to a JSON log file under a private output path.
  - `chat-reply-feedback` CLI: `--plan`, `--candidate-rank`, `--action`, `--output`, `--note`, `--edited-text`, `--boundary-label`, `--boundary-note`.
  - Edit action requires `--edited-text`. Boundary action requires at least one of `--boundary-label` or `--boundary-note`.
  - Invalid candidate rank is rejected with a clear error listing valid ranks.
  - stdout emits only safe summaries: feedback_id, contact_id, candidate_id, priority_rank, action, total_records, output_path. No draft text, edited text, private notes, raw transcript, or private chat path contents are printed.
- Verification:
  - Compile passed for models.py, feedback.py, main.py.
  - Synthetic fixture at `private/distilled/t140_feedback_fixture/synthetic_reply_plan.json`.
  - Accept: feedback record appended, total_records=1.
  - Edit with edited-text: feedback record appended with edited_text field, total_records=2.
  - Reject with note: feedback record appended, total_records=3.
  - Boundary with label+note: feedback record appended with boundary_label and boundary_note, total_records=4.
  - Invalid candidate-rank=99: rejected with error listing valid ranks [1, 2, 3].
  - Edit without --edited-text: rejected with error.
  - stdout contains no draft text, edited text, private notes, or raw transcript content.
  - No ContactSkill, MemoryFact, approved store record, or planner template was modified.
  - Output confined to requested private output path.
- Remaining risks:
  - Feedback log append is not atomic; concurrent writes could corrupt the JSON file. This is acceptable for a private single-user offline tool.
  - No committed automated tests yet; deferred to T150/T152.
  - Feedback records store `source_plan_path` as a string; if the plan file is moved, the path reference becomes stale.
- Explicit non-actions:
  - No memory, ContactSkill, or approved store update was added.
  - No auto-send, realtime integration, DB, vector DB, LLM call, or `private/chat_history/` read was added.

## 35. T140 Review Decision

- Review file:
  - `docs/review/T140_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T140 is complete within task scope.
  - M4 may continue, but only into validation/summary work; no automatic learning or downstream mutation is authorized.
  - Current Unique Task moves to T141 Feedback Log Validator.
- Warning handling:
  - Accepted:
    - N03 `_count_records` re-reads the log after append. Low-impact inefficiency only.
    - N04 `reply_plan_id` currently stands in for a source-plan identifier. Acceptable until a dedicated `plan_id` exists.
    - N06 `ReplyFeedbackAction` as `Literal[...]` matches current codebase style.
  - Deferred:
    - N01 corrupted-log silent reset/data loss risk. Carry into T141 and R042.
    - N02 `source_plan_path` can become stale or vary by caller path style. Carry into T141-or-later and R043.
    - N05 output path is user-controlled but not enforced to remain private. Carry into T141/T152 and R043.
  - Rejected:
    - none

## 36. T141 Kickoff Notes

- Task package:
  - `docs/tasks/M4_feedback_loop/T141_feedback_log_validator.md`
- Worker focus:
  - implement a read-only validator for T140 feedback logs
  - validate record structure, action-specific required fields, source-plan existence, candidate existence, contact alignment, and safe/private path behavior
  - emit only aggregate/id-based summaries to stdout
  - surface corrupted-log or unreadable-log problems explicitly instead of silently normalizing them away
- Explicit non-goals:
  - no proposal generation
  - no memory or ContactSkill updates
  - no feedback-log mutation
  - no sending, DB/vector DB, LLM, or realtime integration
- Reviewer focus:
  - confirm the validator is read-only
  - confirm broken references and malformed records fail safely
  - confirm stdout/docs do not leak edited text, notes, draft text, or raw private content
  - confirm T141 does not drift into T142/T160/T162 behavior

## 37. T141 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- Validator behavior:
  - Added `FeedbackValidationService` with read-only `validate()` method.
  - Validates feedback log JSON existence, readability, JSON parse, and ReplyFeedbackLog schema.
  - Corrupted or unreadable input is reported explicitly via `corrupted_reason` and `corrupted_input_count`, not silently treated as empty-success.
  - Per-record checks:
    - `edit` action requires `edited_text` (otherwise `edit_without_text` issue).
    - `boundary` action requires at least one of `boundary_label` or `boundary_note` (otherwise `boundary_without_details` issue).
    - If `source_plan_path` is set, resolves the path (absolute, relative to CWD, then relative to log directory) and loads the referenced ReplyPlan.
    - Missing or unparseable plan is reported as `missing_plan`.
    - Candidate not found in plan (by `candidate_id` and `priority_rank`) is reported as `missing_candidate`.
    - `contact_id` mismatch between plan and feedback record is reported as `contact_mismatch`.
  - Privacy checks:
    - `W_PRIVACY_INPUT`: input log path is outside `private/` directory.
    - `W_PRIVACY_REF`: resolved `source_plan_path` is outside `private/` directory.
  - Output is safe: only ids, counts, booleans, warning codes, and safe paths. No draft text, edited text, user notes, boundary notes, or raw transcript content is emitted to stdout.
  - `--strict` flag causes non-zero exit code when any invalid records or privacy warnings exist.
- CLI command:
  - `chat-reply-feedback-validate --input <feedback-log.json> [--strict]`
- Verification:
  - Compile passed for feedback.py and main.py.
  - Good log (T140 fixture, 4 records accept/edit/reject/boundary): `valid_record_count=4`, `invalid_record_count=0`, no issues.
  - Bad log (edit without text, boundary without details): `edit_without_text_count=1`, `boundary_without_details_count=1`, `invalid_record_count=2`.
  - Missing plan reference: `missing_plan_count=1`, record reported invalid.
  - Corrupted JSON: `is_readable=false`, `corrupted_input_count=1`, `corrupted_reason="json_decode_error: ..."`, exit code 1.
  - Schema-invalid log (invalid action value): `corrupted_input_count=1`, `corrupted_reason="schema_error: 1 validation failure(s)"`, exit code 1.
  - Log outside `private/`: `W_PRIVACY_INPUT` warning surfaced. With `--strict`, exit code 1.
  - Log referencing plan outside `private/` (plan exists and is valid): `W_PRIVACY_REF` warning surfaced, record remains valid.
  - Read-only confirmed: md5sums of all fixture files unchanged after running all validations.
  - stdout privacy confirmed: grep for private text fields (edited_text, user_note, boundary_note, draft_text, fixture text content) returned 0 matches.
- Explicit non-actions:
  - No proposal, preference, boundary, memory, or ContactSkill update was added.
  - No feedback log, ReplyPlan, ContactSkill, MemoryFact, approved store, or planner template was mutated.
  - No LLM call, auto-send, realtime platform integration, DB, vector DB, or `private/chat_history/` read was added.

## 38. T141 Review Decision

- Review file:
  - `docs/review/T141_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T141 is complete within task scope.
  - M4 may continue only into aggregate feedback summary work; no proposal generation or downstream mutation is authorized.
  - Current Unique Task moves to T142 Feedback Summary Exporter.
- Warning handling:
  - Accepted:
    - N01 raw `input_path` in CLI output. Low-risk style inconsistency only.
    - N03 `_is_private_path` uses a coarse directory-name heuristic. Acceptable for MVP.
    - N04 `_resolve_plan_path` depends on CWD for relative paths. Acceptable with the current private/offline workflow.
    - N05 `strict_mode` is stored in the report but not read by the service. Minor dead data only.
  - Deferred:
    - N02 `reply_plan_id` coherence is not cross-checked against the loaded plan context. Carry into T142 if the summary needs to surface it.
    - N06 `record_results` may grow large on bigger logs. Carry into T142 as a compact-output concern.
  - Rejected:
    - none

## 39. T142 Kickoff Notes

- Task package:
  - `docs/tasks/M4_feedback_loop/T142_feedback_summary_exporter.md`
- Worker focus:
  - export aggregate, privacy-safe summaries over T140/T141 feedback logs
  - prefer validated inputs or internally validated summary paths
  - keep stdout concise and aggregate-only
  - surface invalid/skipped/warning counts without echoing per-record private text
- Explicit non-goals:
  - no proposal generation
  - no feedback-to-patch logic
  - no versioning, rollback, or freeze flow
  - no ContactSkill or Memory mutation
  - no LLM call, auto-send, realtime platform integration, DB, vector DB, or `private/chat_history/` read
- Reviewer focus:
  - confirm output is aggregate and privacy-safe
  - confirm T142 stays within M4 capture/validation/summary scope only
  - confirm any `reply_plan_id` coherence handling remains descriptive and non-mutating

## 40. T142 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- Summary service behavior:
  - Added `FeedbackSummaryService` with read-only `summarize()` method.
  - Reads a T140 feedback log JSON file and computes aggregate counts.
  - Aggregate fields in summary output:
    - `total_records`: total feedback record count
    - `counts_by_action`: count by action type (accept/edit/reject/boundary)
    - `distinct_contact_ids`: number of distinct contact ids
    - `distinct_candidate_ids`: number of distinct candidate ids
    - `distinct_reply_plan_ids`: number of distinct reply_plan_ids
    - `distinct_source_plan_paths`: number of distinct source_plan_path values
    - `records_with_boundary_label`: count of records with a boundary_label set
    - `records_with_edited_text`: count of records with edited_text set
    - `records_with_user_note`: count of records with user_note set
    - `counts_by_approach_label`: count by candidate approach_label (best-effort, loaded from referenced plans; empty when plans are not resolvable)
    - `time_range`: earliest and latest record timestamps
    - `validation_summary`: merged T141 validation report aggregates (optional)
  - Corrupted or unreadable input is reported via `is_readable: false` and `corrupted_reason`, consistent with T141 handling.
  - Optional `--validation-report` reads a T141 validation report and merges only aggregate counts (valid/invalid counts, missing_plan_count, missing_candidate_count, contact_mismatch_count, edit_without_text_count, boundary_without_details_count, privacy_warning_count). Raw record payloads are not printed.
  - Optional `--output` writes the full summary JSON to a private output path.
  - No draft text, edited text, user notes, boundary notes, or raw transcript content appears in stdout or output file.
- CLI command:
  - `chat-reply-feedback-summary --input <feedback.json> [--output <private summary.json>] [--validation-report <report.json>]`
- Verification:
  - Compile passed for feedback.py and main.py.
  - Good log (T140 fixture, 4 records accept/edit/reject/boundary): `total_records=4`, `counts_by_action={accept:1, edit:1, reject:1, boundary:1}`, `distinct_candidate_ids=3`, `counts_by_approach_label={conservative_acknowledgment:2, light_follow_up:1, warm_but_guarded:1}`, approach labels loaded from referenced plan.
  - Good log with validation report and output file: `validation_summary.status=merged`, `valid_record_count=4`, `invalid_record_count=0`, summary JSON written to output path.
  - Bad log (edit without text, boundary without details): `total_records=2`, `counts_by_action={edit:1, boundary:1}`, approach labels loaded from referenced plan.
  - Missing plan log: `total_records=1`, `counts_by_approach_label={}` (plan not resolvable, approach_label unavailable). With validation report: `validation_summary.missing_plan_count=1`, `invalid_record_count=1`.
  - Corrupted JSON: `is_readable=false`, `corrupted_reason="json_decode_error: ..."`, exit code 1.
  - Non-existent validation report: `validation_summary.status=report_not_found`.
  - Privacy confirmed: grep for private text field values (edited text content, user note content, boundary note content) in stdout and output file returned 0 matches.
  - Read-only confirmed: md5sums of all input fixture files unchanged after all summary runs.
  - No ContactSkill, MemoryFact, approved store record, or planner template was modified.
- Explicit non-actions:
  - No proposal, preference, boundary, memory, or ContactSkill update was added.
  - No feedback log, ReplyPlan, ContactSkill, MemoryFact, approved store, or planner template was mutated.
  - No LLM call, auto-send, realtime platform integration, DB, vector DB, or `private/chat_history/` read was added.

## 41. T142 Review Decision

- Review file:
  - `docs/review/T142_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T142 is complete within task scope.
  - M4 implementation scope is now complete: feedback can be recorded, validated, and summarized in a review-only flow.
  - No T142 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 duplicated `_resolve_plan_path` / `_load_plan_safe` helpers
    - N02 raw `input_path` in stdout
    - N03 low-risk aggregate existence-pattern counts
    - N04 unreadable input may still produce an output artifact
    - N05 untyped summary `dict`
    - N06 no `reason_tag` / `policy_risk_flag` aggregation because those fields do not yet exist
  - Deferred:
    - none
  - Rejected:
    - none

## 42. M4 Review Decision

- Review file:
  - `docs/review/M4_review.md`
- Verdict:
  - `Conditional`
- Completion judgment:
  - M4 is functionally complete for intended scope: T140/T141/T142 deliver feedback record, validation, and aggregate summary.
  - No blocking pseudo-completion was found.
  - Clean-environment reproducibility is still not proven from committed repo contents alone because committed tests and committed synthetic fixtures are still missing.
- Gate decision:
  - Do not proceed to M5 yet.
  - Proceed only to M4.5 regression hardening.

## 43. T150 Kickoff Notes

- Task package:
  - `docs/tasks/M4_5_regression_hardening/T150_replyplanner_regression_tests.md`
- Worker focus:
  - add committed deterministic tests for ReplyPlanner structure, privacy, ranking, contact alignment, thin-context behavior, and baseline policy behavior
  - use only synthetic or redacted fixtures
  - reduce the reproducibility gap that currently keeps M4 at `Conditional`
- Explicit non-goals:
  - no planner implementation changes unless Captain opens a bug-fix task
  - no T140-T142 feedback CLI regression work in this task
  - no LLM, auto-send, realtime integration, DB, vector DB, or UI work
- Reviewer focus:
  - confirm tests are committed, deterministic, and privacy-safe
  - confirm fixtures are synthetic/redacted
  - confirm M3/M4 gate obligations are actually encoded as tests rather than restated in docs

## 44. T150 Implementation Record

- Files changed:
  - `tests/__init__.py` (new)
  - `tests/helpers.py` (new)
  - `tests/conftest.py` (new)
  - `tests/test_reply_planner.py` (new)
  - `pyproject.toml` (added `[tool.pytest.ini_options]` with `pythonpath` and `testpaths`)
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Fixture shape:
  - All fixtures are synthetic Python objects constructed via `tests/helpers.py` helpers.
  - No JSON fixture files, no raw transcript text, no real names, real platform IDs, or private paths.
  - Seven reusable fixture contexts: baseline friend, colleague, thin, sensitive/boundary, false-positive probe, false-negative probe, privacy leakage probe.
  - Each fixture constructs `ChatContext` with appropriate `ApprovedStoreContext`, `ApprovedContactSkillBrief`, `ApprovedMemoryFactBrief`, events, and memory hits.
- Test command and result:
  - `PYTHONPATH='src' pytest tests -v`
  - 49 tests passed in 0.10s, 0 failures.
  - No LLM calls, no network access, no private file reads.
- Tests intentionally marking current limitations:
  - `TestFalseNegativeProbe`: documents that subtle inbound pacing pressure ("you should really call me sometime soon") is not detected by keyword-based policy. This is an accepted M3 Conditional limitation, not an xfail. The test asserts current expected behavior.
  - `TestFalsePositiveProbe`: documents that "money" in a work-budgeting context triggers `sensitive_topic=True` but does NOT escalate to `boundary_sensitive` because intent is GENERAL and no boundary cues exist. This is correct current behavior but documents the keyword proximity risk.
- Coverage of M3 Conditional obligations:
  - Candidate structure: `TestBaselineFriendContext`, `TestColleagueContext`, `TestStructureRegression::test_candidate_structure_regression_guard`
  - Privacy leakage: `TestPrivacyLeakage` (5 tests), `TestStructureRegression::test_privacy_regression_guard`
  - Contact alignment: `TestContactIdMismatch` (2 tests), `TestStructureRegression::test_contact_alignment_regression_guard`
  - Ranking invariants: `TestPriorityRank` (4 tests), `TestStructureRegression::test_ranking_invariant_regression_guard`
  - Thin-context behavior: `TestThinContext` (5 tests)
  - Boundary/sensitive behavior: `TestSensitiveContext` (4 tests)
  - False-positive boundedness: `TestFalsePositiveProbe` (4 tests)
  - False-negative documentation: `TestFalseNegativeProbe` (3 tests)
  - Not-configured path: `TestNotConfiguredPath` (5 tests)
  - Non-approved id isolation: `TestNonApprovedRecordIdIsolation` (2 tests)
- Which M3 risks were reduced:
  - R036 (no committed tests/fixtures): reduced. ReplyPlanner now has 49 committed deterministic tests and 7 synthetic fixture contexts.
  - R034 (priority_rank / contact alignment): regression-guarded. Both now have committed tests.
  - R037 (false-positive/false-negative keyword risk): documented with committed tests encoding current behavior.
- Which M3 risks remain open:
  - R035 (relationship-aware quality still template-driven): not addressed by T150. T150 tests the contract wiring and safety surface, not naturalness.
  - R037 (keyword-only policy): false-negative gap is documented but not fixed. A future semantic classifier could close this.
  - R046 (M3/M4 clean-environment reproducibility): partially reduced. T150 covers ReplyPlanner; T151/T152 must still cover policy fixtures and feedback CLI.

## 45. T150 Review Decision

- Review file:
  - `docs/review/T150_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T150 is complete within task scope.
  - The repo now has committed deterministic ReplyPlanner regression coverage and may move forward to T151.
  - No T150 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 `TestNotConfiguredPath` overlaps with `thin_context`, but still checks a distinct invariant.
    - N02 no direct `ReplyPlanPolicyEngine` unit tests yet; this is better treated as T151 follow-up scope than as a T150 defect.
    - N03 `practical` summary wording assertion is intentionally brittle as a regression guard.
    - N04 false-negative probes intentionally encode current missed-detection behavior.
    - N05 `tests/helpers.py` constructors are simple enough that missing isolated helper tests is low risk.
    - N06 `notes_on_candidate_differences` is not yet asserted and remains optional coverage expansion.
  - Deferred:
    - none
  - Rejected:
    - none

## 46. T151 Kickoff Notes

- Task package:
  - `docs/tasks/M4_5_regression_hardening/T151_policy_fixture_suite.md`
- Worker focus:
  - turn policy behavior into an explicit committed fixture suite on top of the new T150 base
  - add direct policy-layer assertions where they materially improve auditability
  - keep all fixtures synthetic/redacted and keep the task non-mutating
- Specific follow-ups from T150 review:
  - add direct `ReplyPlanPolicyEngine` coverage where planner-only coverage is too indirect
  - separate missing-store-path or loaded-without-skill coverage more clearly from generic thin-context coverage
  - consider assertions for `notes_on_candidate_differences` when policy state should surface there
- Explicit non-goals:
  - no planner or policy behavior changes unless Captain opens a bug-fix task
  - no feedback CLI regression work in this task
  - no LLM, auto-send, realtime integration, DB, vector DB, or UI work
- Reviewer focus:
  - confirm direct policy expectations are genuinely encoded in committed tests
  - confirm fixtures remain synthetic and privacy-safe
  - confirm T151 narrows reproducibility risk without overstating relationship-aware maturity

## 47. T151 Implementation Record

- Files changed:
  - `tests/conftest.py` (added 3 new fixtures: `loaded_no_skill_context`, `degraded_store_context`, `over_proactivity_probe_context`; fixed `baseline_friend_context` to remove accidental boundary cue keywords)
  - `tests/test_policy_engine.py` (new: 67 direct policy engine tests)
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Fixture shape:
  - All fixtures are synthetic Python objects constructed via `tests/helpers.py` helpers.
  - No JSON fixture files, no raw transcript text, no real names, real platform IDs, or private paths.
  - 10 reusable fixture contexts: baseline friend, colleague, thin, sensitive/boundary, false-positive probe, false-negative probe, privacy leakage probe, loaded-but-no-skill, degraded-store (store_path_missing), over-proactivity probe.
  - `baseline_friend_context` was corrected: previous `strategy_hints=["keep warm but low pressure"]` and `boundary_reminders=["do not push for details"]` inadvertently contained "low pressure" and "do not push" which are in `_BOUNDARY_CUE_KEYWORDS` and `_AVOID_FOLLOW_UP_KEYWORDS`, making the fixture not a clean baseline. Changed to `strategy_hints=["keep warm"]` and `boundary_reminders=["stay friendly and relaxed"]`.
- Test command and result:
  - `PYTHONPATH='src' pytest tests -v`
  - 116 tests passed in 0.17s (49 T150 + 67 T151), 0 failures.
  - No LLM calls, no network access, no private file reads.
- Direct `ReplyPlanPolicyEngine.build_profile()` coverage:
  - `TestBuildProfileBaselineFriend`: thin_context=False, boundary_sensitive=False, conservative_mode=False, practical_tone=False, context_risk_flags=[], avoid_follow_up=False
  - `TestBuildProfileColleague`: practical_tone=True, thin_context=False, conservative_mode=False
  - `TestBuildProfileThinContext`: thin_context=True, conservative_mode=True, context_risk_flags=["thin_context"]
  - `TestBuildProfileLoadedNoSkill`: thin_context=True despite status="loaded", conservative_mode=True, boundary_sensitive=False (no boundary cues)
  - `TestBuildProfileDegradedStore`: thin_context=True for status="store_path_missing", conservative_mode=True
  - `TestBuildProfileSensitive`: boundary_sensitive=True, conservative_mode=True, avoid_follow_up=True
  - `TestBuildProfileFalsePositive`: boundary_sensitive=False, conservative_mode=False ("money" in work context)
  - `TestBuildProfileFalseNegative`: boundary_sensitive=False, conservative_mode=False (documented limitation)
  - `TestBuildProfileOverProactivity`: avoid_follow_up=True, boundary_sensitive=True, conservative_mode=True, thin_context=False
- Direct `ReplyPlanPolicyEngine.assess_candidate()` coverage:
  - `TestAssessCandidateActionPush`: action push cues ("call", "meet", "閹垫挾鏁哥拠?, "schedule") always trigger over_proactive
  - `TestAssessCandidateOverProactiveConservativeMode`: optional_follow_up always triggers in conservative mode; paced_next_step with proactive cues triggers; conservative_acknowledgment without cues stays clean
  - `TestAssessCandidateNoPressureExemption`: "no rush" and Chinese "閸忓牅绗夊鈧崜宥嗗腹" exempt from over_proactive; action push overrides no-pressure
  - `TestAssessCandidateImpersonationRisk`: "he would say", "she would say", "鐎佃鏌熸导? all detected; clean text produces no impersonation_risk
  - `TestAssessCandidateConfidencePenalty`: thin_context 0.10, boundary_sensitive 0.06, combined 0.16, impersonation 0.15, clean 0.0
- `notes_on_candidate_differences` coverage:
  - Baseline: 3 default notes about each candidate
  - Conservative mode (sensitive context): notes shifted to no-pressure/avoiding language
  - Thin not-loaded (thin_context fixture): extra "thin" note appended
  - Loaded-no-skill: conservative notes but NO extra "thin" note (status IS "loaded")
  - Boundary-sensitive: extra note about sensitive/boundary context
- Over-proactivity planner integration:
  - `TestOverProactivityPlannerIntegration`: over_proactivity_probe_context produces plan with at least one over_proactive risk flag in candidates; all candidates remain valid
- Tests intentionally marking current limitations:
  - `TestBuildProfileFalseNegative`: documents that "you should really call me sometime soon" is not detected. Accepted M3 Conditional limitation.
  - `TestBuildProfileFalsePositive`: documents that "money" in work context triggers sensitive_topic=True at the keyword level but does NOT escalate to boundary_sensitive. This is correct behavior.
- Coverage of T151 task requirements:
  - baseline friend: `TestBuildProfileBaselineFriend` (6 tests)
  - practical colleague: `TestBuildProfileColleague` (5 tests)
  - explicit sensitive boundary: `TestBuildProfileSensitive` (5 tests)
  - thin context: `TestBuildProfileThinContext` (5 tests)
  - false-positive policy probe: `TestBuildProfileFalsePositive` (4 tests)
  - subtle false-negative probe: `TestBuildProfileFalseNegative` (3 tests)
  - impersonation-risk probe: `TestAssessCandidateImpersonationRisk` (5 tests)
  - over-proactivity probe: `TestBuildProfileOverProactivity` (4 tests) + `TestOverProactivityPlannerIntegration` (2 tests)
  - loaded-but-skill-missing: `TestBuildProfileLoadedNoSkill` (4 tests)
  - degraded store: `TestBuildProfileDegradedStore` (4 tests)
  - direct policy engine coverage: all build_profile + all assess_candidate tests
  - notes_on_candidate_differences: `TestNotesOnCandidateDifferences` (5 tests)
- Which M3/M4 risks were reduced:
  - R036 further narrowed: policy layer now has 67 committed direct tests on top of T150's 49 planner-through-policy tests.
  - R037 further documented: false-positive, false-negative, over-proactivity, and impersonation detection behavior all have direct policy engine tests encoding current expected behavior.
  - R046 further narrowed: clean-environment reproducibility now covers both ReplyPlanner surface and direct policy engine behavior. T152 must still cover feedback CLI.
- Which risks remain open:
  - R035 (relationship-aware quality still template-driven): not addressed by T151.
  - R037 (keyword-only policy): false-negative gap is documented but not fixed.
  - R046 (clean-environment reproducibility): T152 must still cover feedback CLI regression tests.

## 48. T151 Review Decision

- Review file:
  - `docs/review/T151_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T151 is complete within task scope.
  - The repo now has committed deterministic direct policy-engine coverage in addition to T150 planner regression coverage.
  - No T151 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 `_candidate_is_over_proactive` conservative fallback branch is not independently tested, but the uncovered branch is minor and functionally close to already-covered logic.
    - N02 confidence-penalty combinations are not exhaustively enumerated, but the penalty components and representative additive behavior are already covered.
    - N03 the baseline fixture contamination discovered during T151 is accepted as a useful correction uncovered by the new direct tests, not as a reason to reopen T150.
  - Deferred:
    - none
  - Rejected:
    - none

## 49. T152 Kickoff Notes

- Task package:
  - `docs/tasks/M4_5_regression_hardening/T152_feedback_cli_regression_tests.md`
- Worker focus:
  - add committed deterministic regression tests for the T140-T142 feedback capture, validation, and summary CLI loop
  - prove privacy-safe stdout behavior, explicit corrupted-log surfacing, compact validation/summary behavior, and non-mutation guarantees from committed repo contents alone
  - keep all fixtures synthetic/redacted and keep the task non-mutating
- Explicit non-goals:
  - no feedback-to-patch logic
  - no ContactSkill or Memory mutation
  - no planner, policy, or feedback implementation changes unless Captain opens a bug-fix task
  - no LLM, auto-send, realtime integration, DB, vector DB, or UI work
- Reviewer focus:
  - confirm tests prove M4 remains record/validate/summarize only
  - confirm stdout and artifacts do not leak draft text, edited text, notes, raw transcript content, or private chat paths
  - confirm the committed tests are sufficient to narrow or close the remaining clean-environment reproducibility gap for M4

## 50. T152 Implementation Record

- Files changed:
  - `tests/test_feedback_cli.py` (new: 60 feedback CLI regression tests)
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Fixture shape:
  - All fixtures are synthetic Python objects constructed via inline helpers in `tests/test_feedback_cli.py`.
  - No JSON fixture files, no raw transcript text, no real names, real platform IDs, or private paths.
  - `_synthetic_reply_plan()`: minimal 3-candidate ReplyPlan with safe ids and safe text.
  - `_write_plan()`: serializes a synthetic ReplyPlan to a temp file.
  - `_write_feedback_log()`: serializes synthetic feedback records to a temp file.
  - `_make_record()`: constructs a `ReplyFeedbackRecord` with sensible defaults.
  - Uses `pytest` `tmp_path` for all temp files; no committed filesystem artifacts.
- Test command and result:
  - `PYTHONPATH='src' pytest tests -v`
  - 176 tests passed in 1.30s (60 T152 + 67 T151 + 49 T150), 0 failures.
  - No LLM calls, no network access, no private file reads.
- Coverage of T152 task requirements:
  - `accept` feedback append: `TestFeedbackAppendAccept` (2 tests)
  - `edit` feedback append: `TestFeedbackAppendEdit` (3 tests)
  - `reject` feedback append: `TestFeedbackAppendReject` (2 tests)
  - `boundary` feedback append: `TestFeedbackAppendBoundary` (3 tests)
  - invalid candidate rank/id rejected: `TestFeedbackInvalidInputs` (4 tests)
  - invalid plan path rejected: `TestFeedbackInvalidInputs::test_missing_plan_file_rejected`, `test_invalid_plan_json_rejected`
  - validator catches invalid action-specific fields: `TestValidationActionSpecific` (3 tests)
  - summary exporter reports aggregate counts: `TestSummaryAggregateCounts` (5 tests)
  - validator report merge into summary: `TestSummaryValidationMerge` (3 tests)
  - stdout does not print private text: `TestPrivacySafety` (7 tests)
  - feedback flow does not mutate memory/ContactSkill/store: `TestNonMutation` (4 tests)
  - private output confinement: `TestPrivateOutputConfinement` (3 tests)
  - corrupted/unreadable input surfaced explicitly: `TestCorruptedInput` (7 tests)
  - compact validation/summary output: `TestCompactOutput` (4 tests)
  - end-to-end CLI regression: `TestCLIAppendRegression` (3 tests), `TestCLIValidateRegression` (2 tests), `TestCLISummarizeRegression` (3 tests)
- Coverage of T140/T141/T142 obligations:
  - T140 obligations tested: accept/edit/reject/boundary append, invalid rank rejection, invalid plan rejection, edit-without-text rejection, boundary-without-details rejection, output-only privacy, non-mutation of plan file.
  - T141 obligations tested: action-specific field validation (edit_without_text, boundary_without_details), missing-plan detection, missing-candidate detection, contact-mismatch detection, corrupted JSON/schema/missing-file surfacing, privacy warnings (W_PRIVACY_INPUT, W_PRIVACY_REF), read-only confirmation.
  - T142 obligations tested: aggregate counts (total, by action, distinct ids, boundary/edited/note counts, approach labels), validation report merge (aggregate-only, no raw record_results), corrupted input handling, output file writing, read-only confirmation.
- Which M4 risks were reduced:
  - R046 (clean-environment reproducibility): closed for M4.5. T150/T151/T152 together provide 176 committed deterministic tests covering ReplyPlanner, policy engine, and the full feedback CLI loop. Clean-environment reproducibility is now proven from committed repo contents alone.
  - R042 (corrupted-log silent reset): regression-guarded. Corrupted JSON, schema-invalid, and missing-file inputs are all tested to surface explicit errors rather than silent normalization.
  - R043 (path handling): regression-guarded. Privacy warnings for non-private input paths and non-private plan references are tested.
  - R044 (reply_plan_id coherence): remains active but is now regression-guarded for the paths T142 already covers (distinct counts in summary, reference tracking in validation).
  - R045 (verbose record_results): regression-guarded. Compact output tests verify that validation report and summary do not echo per-record private text.
- Which risks remain open:
  - R035 (relationship-aware quality still template-driven): not addressed by T152.
  - R037 (keyword-only policy): not addressed by T152; documented in T151 tests.
  - R038 (feedback log may be mistaken for automatic learning): not addressed by T152; M4 design constraint still applies.

## 51. T152 Review Decision

- Review file:
  - `docs/review/T152_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T152 is complete within task scope.
  - M4.5 regression hardening is now complete across T150/T151/T152.
  - No T152 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N03 `--validation-report` flag coverage is service-level rather than full CLI end-to-end, but the underlying merge behavior is directly regression-tested and adequate.
    - N04 there is no single append->validate->summarize integration test, but the service/CLI slices are covered strongly enough to accept the task.
    - N05 `test_approach_labels_loaded` is intentionally brittle as a regression guard and acceptable.
  - Deferred:
    - N01 validation `record_results` still has no explicit size bound on large logs.
    - N02 service-level output-path confinement is still warning/convention based rather than hard-enforced.
  - Rejected:
    - none

## 52. M4.5 Milestone Review

- Review file:
  - `docs/review/M4_5_review.md`
- Verdict:
  - `Allow`
- Captain conclusion:
  - M4.5 has satisfied its purpose: M3/M4 behavior is now reproducible from committed repo contents alone.
  - The project may now enter M5, but only at the schema-only candidate layer.
  - M5 remains review-only: no auto-apply, no runtime injection, no automatic ContactSkill/Memory mutation, and no outbound send behavior.

## 53. T160 Kickoff Notes

- Task package:
  - `docs/tasks/M5_feedback_to_patch/T160_preference_patch_schema.md`
- Worker focus:
  - define a review-only `PreferencePatchCandidate` contract and its supporting enums/metadata shape
  - keep the output candidate-only and evidence-backed via `supporting_feedback_ids`
  - prepare later clustering/review/runtime tasks without implementing them
- Explicit non-goals:
  - no clustering
  - no proposal generation
  - no review CLI
  - no runtime injection
  - no auto-approve or auto-apply behavior
  - no LLM, no outbound send behavior, no platform integration
- Reviewer focus:
  - confirm the schema is explicit enough for later M5 tasks without smuggling in runtime behavior
  - confirm candidate-only status and review metadata are encoded structurally
  - confirm empty or missing supporting feedback evidence is rejected or marked unsafe

## 54. T160 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/preference_patch_contract.md` (new)
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Model/enum names added:
  - `PreferencePatchType` (Literal with 8 values: tone_preference, length_preference, boundary_preference, topic_preference, question_style, humor_style, repair_style, proactivity_preference)
  - `PreferencePatchCandidate` (Pydantic BaseModel)
- Schema design:
  - `supporting_feedback_ids` has `min_length=1`, structurally requiring evidence. Empty list is rejected by Pydantic validation.
  - `status` defaults to `"candidate"` using existing `DistillationStatus` literal.
  - `review_metadata` reuses `DistilledArtifactReviewMetadata`, which defaults to `reviewed_by_human=False` and `last_decision=None`, so `is_runtime_ready()` returns `False` by default.
  - `is_runtime_ready()` on the model requires `status == "approved"` AND `reviewed_by_human == True` AND `last_decision == "approved"`.
  - No field stores raw transcript text, edited text, private notes, or raw feedback content.
  - `positive_examples` and `negative_examples` are free-form string lists for safe references or summaries only.
  - `supporting_cluster_ids` is optional for future T161 cluster output.
  - `affected_candidate_types` is a free-form string list for approach labels or candidate shapes this patch would influence.
- Synthetic validation example:
  - Created a `PreferencePatchCandidate` with `patch_type="tone_preference"`, `contact_id="contact_lin"`, `supporting_feedback_ids=["fb_abc123", "fb_def456"]`, `claim="Contact prefers concise replies"`, `behavior_instruction="Keep replies short and direct"`, `confidence=0.8`, `sensitivity="low"`.
  - Confirmed: `status == "candidate"`, `is_runtime_ready() == False`, `review_metadata.reviewed_by_human == False`.
  - Confirmed: creating with empty `supporting_feedback_ids=[]` raises Pydantic `ValidationError`.
- How the schema keeps M5 candidate-only:
  - Default status is `"candidate"`, not `"approved"`.
  - `is_runtime_ready()` is gated on human review, matching existing store/review pattern.
  - No field provides or implies a path to mutate ContactSkill, MemoryFact, or runtime prompts.
  - No auto-approve, auto-apply, or runtime injection capability is encoded in the model.
- Follow-up constraints for T161-T164:
  - T161 clustering must produce cluster IDs compatible with `supporting_cluster_ids`.
  - T162 proposal CLI must enforce `supporting_feedback_ids` non-empty; single-feedback patches without clustering are discouraged.
  - T163 review CLI must use the same approval gate as T122: status change requires human reviewer and valid evidence.
  - T164 compact context must only read patches where `is_runtime_ready() == True`, and must not inject `behavior_instruction` directly into runtime prompts without compact context layer.
  - None of T161-T164 may add a field that stores raw feedback text, edited text, or private note bodies.

## 55. T160 Review Decision

- Review file:
  - `docs/review/T160_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T160 is complete within task scope.
  - The repo now has an explicit candidate-only `PreferencePatchCandidate` contract for M5.
  - No T160 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 `instruction_scope` remains free-form at schema stage. This is acceptable while actual downstream usage is still unknown and later tightening remains available.
    - N04 `schema_version` remains a plain string for consistency with the project's existing model/store pattern.
    - N05 broader working-tree modifications are treated as repository hygiene noise rather than a T160 scope violation, because the task-specific change itself stays within allowed files.
  - Deferred:
    - N02 `positive_examples` and `negative_examples` are not structurally constrained to safe-only summaries/references.
    - N03 no committed automated tests yet cover `PreferencePatchCandidate` validation.
  - Rejected:
    - none

## 56. T161 Kickoff Notes

- Task package:
  - `docs/tasks/M5_feedback_to_patch/T161_feedback_clusterer.md`
- Worker focus:
  - add a deterministic, privacy-safe feedback clustering layer on top of validated T140-T142 records
  - emit stable cluster ids, aggregate labels, counts, and supporting feedback ids only
  - prepare clustered evidence for later T162 patch proposal work without generating patches yet
- Explicit non-goals:
  - no `PreferencePatchCandidate` generation
  - no review CLI
  - no runtime injection
  - no ContactSkill/Memory mutation
  - no outbound send behavior, no realtime integration, no LLM use
- Reviewer focus:
  - confirm clustering is deterministic and aggregate-only
  - confirm stdout/artifacts do not leak draft text, edited text, user notes, boundary notes, or raw feedback text
  - confirm cluster outputs are explicit enough for T162 without silently smuggling in patch-generation behavior

## 57. T161 Implementation Record

- 娴狅絿鐖?/ 閺傚洦銆傞弨鐟板З閿?  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/data_contracts/preference_patch_contract.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- 瀹告彃鐤勯悳鏉垮敶鐎圭櫢绱?  - 閺傛澘顤?`FeedbackClusterService`閿涘本绉风拹?T140 `ReplyFeedbackLog` 楠炴儼绶崙铏光€樼€规碍鈧佲偓渚€娈ｇ粔浣哥暔閸忋劎娈戦懕姘値閼辨氨琚妴?  - 閺傛澘顤?`chat-feedback-cluster` CLI閿涘本鏁幐?`--feedback-log`閵嗕梗--output`閵嗕梗--validation-report`閵?  - 閼辨氨琚弽鍥╊劮娴犲骸寮芥＃?action 缁鐎风涵顔肩暰閹勫腹鐎电》绱?    - `accept` 閳?`good_tone`
    - `reject` 閳?`not_like_me`
    - `boundary` 閳?`boundary_violation`閿涘牐瀚?`boundary_label` 瑜版帊绔撮崠鏍ф倵閸栧綊鍘ゅ鑼叀閺嶅洨顒烽崚娆庡▏閻劏顕氶弽鍥╊劮閿?    - `edit` 閳?瑜版挸澧犻弮鐘茬暔閸忋劎鈥樼€规碍鈧勭垼缁涙拝绱濋弽鍥唶娑?unlabeled
  - 閼辨氨琚柨顔昏礋 `(contact_id, cluster_label)`閿涘本瀵滈幒鎺戠碍妞ゅ搫绨潏鎾冲毉閵?  - `cluster_id` 閻?`sha256(contact_id:label)[:16]` 閻㈢喐鍨氶敍宀€鈥樻穱婵堟祲閸氬苯鍨庣紒鍕暛婵绮撴禍褏鏁撻惄绋挎倱 ID閵?  - 濮ｅ繋閲?cluster 鏉堟挸鍤崠鍛儓閿涙瓪cluster_id`閵嗕梗contact_id`閵嗕梗cluster_label`閵嗕梗supporting_feedback_ids`閵嗕梗record_count`閵嗕梗counts_by_action`閵嗕梗counts_by_approach_label`閵嗕梗counts_by_priority_rank`閵嗕梗time_range`閵嗕梗reason_tag_summary`閵?  - `--validation-report` 閸欘垶鈧寮弫鐗堟暜閹镐椒绮庨懕姘辫 T141 妤犲矁鐦夐柅姘崇箖閻ㄥ嫯顔囪ぐ鏇樷偓?  - stdout 娴犲懓绶崙楦夸粵閸氬牏绮虹拋鈥虫嫲 ID閿涘奔绗夋潏鎾冲毉閸樼喎顫愰崣宥夘洯閺傚洦婀伴妴浣虹椽鏉堟垶鏋冮張顑锯偓浣烘暏閹村嘲顦▔銊﹀灗鏉堝湱鏅径鍥ㄦ暈閵?  - 閺堫亞鏁撻幋?`PreferencePatchCandidate`閵嗕焦婀穱顔芥暭 ContactSkill/Memory/store records閵嗕焦婀拫鍐暏 LLM閵嗕焦婀懛顏勫З approve 閹?apply閵?- 閼辨氨琚潏鎾冲毉 shape閿?  - Schema: `feedback_cluster_v1`
  - CLI: `chat-feedback-cluster --feedback-log <path> --output <path> [--validation-report <path>]`
- 閸氬牊鍨氭宀冪槈缁€杞扮伐閿涘牆鐨㈤崷?verification 闂冭埖顔屾禍褍鍤敍澶涚窗
  - 鏉堟挸鍙嗛敍?0 閺夆€虫値閹存劕寮芥＃鍫ｎ唶瑜版洩绱檆ontact_test_001: 3 reject + 2 accept + 2 boundary + 1 edit, contact_test_002: 2 reject閿?  - 鏉堟挸鍤敍? 娑?cluster閿涘潌oundary_violation/2, good_tone/2, not_like_me/3 for contact_test_001, not_like_me/2 for contact_test_002閿?  - 1 閺?unlabeled閿涘潒dit 鐠佹澘缍嶉敍澶涚礉1 閺?unclustered
  - Cluster ID 缁嬪啿鐣鹃幀褔鐛欑拠渚€鈧俺绻冮敍姘辨祲閸氬矁绶崗銉よ⒈濞喡ょ箥鐞涘奔楠囬悽鐔烘祲閸氬瞼娈?cluster_id 闂嗗棗鎮?  - 闂呮劗顫嗙€瑰鍙忔宀冪槈闁俺绻冮敍姘崇翻閸?JSON 娑撳秴鎯?edited_text/user_note/boundary_note/draft_text
  - 娑撳秴鎮?contact_id 閻ㄥ嫮娴夐崥?label 娴溠呮晸娑撳秴鎮撻惃?cluster_id
  - 176 瀹稿弶婀佸ù瀣槸閸忋劑鍎撮柅姘崇箖閿涘矂娴傞崶鐐茬秺
  - CLI `chat-feedback-cluster --feedback-log <path>` 濮濓絽鐖舵潻鎰攽
- Cluster ID 娑?T160 閻ㄥ嫬鍙х化浼欑窗
  - `cluster_id` 娑?`cluster_<sha256_hex_16>` 閺嶇厧绱￠惃鍕摟缁楋缚瑕嗛敍灞肩瑢 `PreferencePatchCandidate.supporting_cluster_ids: list[str]` 閸忕厧顔?  - T162 閸欘垶鈧俺绻?`supporting_cluster_ids` 瀵洜鏁?T161 鏉堟挸鍤惃?cluster
- T162-T164 韫囧懘銆忔穱婵堟殌閻ㄥ嫮瀹抽弶鐕傜窗
  - `edit` action 鐠佹澘缍嶈ぐ鎾冲閺堫亣顫﹂懕姘辫閿涘牊妫ょ€瑰鍙忕涵顔肩暰閹勭垼缁涙拝绱氶敍瀛?62 娑撳秴褰查崑鍥啎 edit 鐠佹澘缍嶅鑼额潶閼辨氨琚憰鍡欐磰
  - cluster label 闂嗗棗鎮庤ぐ鎾冲娑?3 娑擃亞鈥樼€规碍鈧勭垼缁涙拝绱檂good_tone`閵嗕梗not_like_me`閵嗕梗boundary_violation`閿涘绱濋崝鐘辩瑐 boundary_label 瑜版帊绔撮崠鏍у爱闁板秶娈戝鑼叀閺嶅洨顒?  - `cluster_id` 娓氭繆绂嗛崚鍡欑矋闁款喖鍞寸€圭櫢绱濇稉宥呭讲閻劑娈㈤張?ID 閺囧じ鍞?  - 鏉堟挸鍤稉宥呮儓娴犺缍嶉崢鐔奉潗閺傚洦婀伴敍瀛?62 娑旂喍绗夊妞剧矤 cluster 鏉堟挸鍤崣宥嗙叀閸樼喎顫愰崣宥夘洯閸愬懎顔?
## 58. T161 Review Decision

- Review file:
  - `docs/review/T161_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T161 is complete within task scope.
  - The repo now has a deterministic, privacy-safe feedback clustering layer for M5.
  - No T161 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 `reason_tag_summary` is a mildly misleading name, but the field meaning is documented and no data is lost.
    - N03 `counts_by_approach_label` may silently degrade when referenced plan files are unavailable. This is acceptable because the field is optional enrichment.
    - N05 `.claude/settings.json` is a workspace artifact rather than a task-scope violation.
  - Deferred:
    - N02 no committed automated tests yet cover `FeedbackClusterService` / `chat-feedback-cluster`.
    - N04 raw `input_path` remains present in cluster stdout/output.
  - Rejected:
    - none

## 59. T162 Kickoff Notes

- Task package:
  - `docs/tasks/M5_feedback_to_patch/T162_patch_proposal_cli.md`
- Worker focus:
  - convert T161 cluster outputs into deterministic, review-only `PreferencePatchCandidate` proposals
  - preserve explicit evidence via non-empty `supporting_feedback_ids` and `supporting_cluster_ids`
  - skip ambiguous or unlabeled clusters rather than generating speculative patches
- Explicit non-goals:
  - no human review actions yet
  - no auto-approve, auto-apply, or runtime injection
  - no ContactSkill/Memory mutation
  - no outbound send behavior, no realtime integration, no LLM use
  - no raw feedback text, edited text, private notes, or draft text in candidate fields
- Reviewer focus:
  - confirm proposals are deterministic, candidate-only, and evidence-backed
  - confirm ambiguous or edit-only signals are skipped explicitly instead of being over-interpreted
  - confirm stdout/artifacts remain privacy-safe and no runtime mutation behavior is smuggled into the proposal layer

## 60. T162 Implementation Record

- 娴狅絿鐖?/ 閺傚洦銆傞弨鐟板З閿?  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/data_contracts/preference_patch_contract.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- 瀹告彃鐤勯悳鏉垮敶鐎圭櫢绱?  - 閺傛澘顤?`PatchProposalService`閿涘本绉风拹?T161 cluster report 楠炴儼绶崙铏光€樼€规碍鈧佲偓涔ndidate-only `PreferencePatchCandidate` 閹绘劖顢嶉妴?  - 閺傛澘顤?`chat-feedback-propose-patch` CLI閿涘本鏁幐?`--cluster-report`閿涘牆绻€闂団偓閿涘鎷?`--output`閿涘牆褰查柅澶涚礆閵?  - 绾喖鐣鹃幀褎鐖ｇ粵鐐Ё鐏忓嫸绱?    - `too_long` 閳?`length_preference` / sensitivity=low
    - `too_formal` 閳?`tone_preference` / sensitivity=low
    - `too_cold` 閳?`tone_preference` / sensitivity=low
    - `too_eager` 閳?`proactivity_preference` / sensitivity=medium
    - `too_intimate` 閳?`boundary_preference` / sensitivity=high
    - `boundary_violation` 閳?`boundary_preference` / sensitivity=high
  - 鐠哄疇绻冪憴鍕灟閿?    - `insufficient_support`: record_count < 2 閹?supporting_feedback_ids 娑撹櫣鈹?    - `unlabeled_cluster`: cluster_label 缂傚搫銇?    - `no_safe_mapping`: cluster_label 娑撳秴婀涵顔肩暰閹勬Ё鐏忓嫯銆冩稉顓ㄧ礄閸栧懏瀚?`good_tone`閵嗕梗not_like_me`閵嗕焦婀惌銉︾垼缁涙拝绱?  - `good_tone` 閸?`not_like_me` 鐞氼偉鐑︽潻鍥偓宀勬姜閻氭粍绁撮敍灞芥礈娑撳搫鍙鹃懕姘値娣団€冲娇娑撳秷鍐绘禒銉ф晸閹存劕鐣ㄩ崗銊ф畱 `behavior_instruction`閵?  - 缂冾喕淇婃惔锕€鍙曞蹇ョ窗`min(0.3 + 0.15 * (record_count - 1), 0.9)`閿涘奔绗岀拠浣瑰祦瀵搫瀹抽崡鏇＄殶闁帒顤冮敍灞肩瑝鐡掑懓绻?0.9閵?  - 閹碘偓閺堝鏁撻幋鎰畱 patch 閻樿埖鈧椒璐?`candidate`閿涘畭review_metadata.reviewed_by_human` 娑?`False`閿涘畭is_runtime_ready()` 鏉╂柨娲?`False`閵?  - `positive_examples` 閸?`negative_examples` 婵绮撴稉铏光敄閸掓銆冮敍鍧oposal 闂冭埖顔屾稉宥囨晸閹存劧绱氶妴?  - `affected_candidate_types` 娴?cluster 閻?`counts_by_approach_label` 濞插墽鏁撻妴?  - 閺堫亙鎱ㄩ弨?ContactSkill/Memory/store records閵嗕焦婀拫鍐暏 LLM閵嗕焦婀懛顏勫З approve 閹?apply閵嗕焦婀▔銊ュ弳 runtime context閵?- Proposal 鏉堟挸鍤?shape閿?  - Schema: `patch_proposal_v1`
  - CLI: `chat-feedback-propose-patch --cluster-report <path> --output <path>`
- 閸氬牊鍨氭宀冪槈缁€杞扮伐閿?  - 鏉堟挸鍙嗛敍姘儓 4 娑?cluster 閻ㄥ嫬鎮庨幋?cluster report閿涘澅oo_long/3閵嗕宫ood_tone/2閵嗕苟ot_like_me/2閵嗕攻oundary_violation/1閿?  - 鏉堟挸鍤敍? 娑?candidate閿涘澅oo_long/3 閳?length_preference, confidence=0.6閿?  - 鐠哄疇绻冮敍? 娑?cluster閿涘潛ood_tone 閳?no_safe_mapping, not_like_me 閳?no_safe_mapping, boundary_violation/1 閳?insufficient_support閿?  - 濮ｅ繋閲?candidate 閻?`supporting_feedback_ids` 闂堢偟鈹?  - `positive_examples` / `negative_examples` 娑撹櫣鈹栭崚妤勩€?  - 闁插秴顦叉潻鎰攽娴溠呮晸閻╃鎮撻惃?candidate閿涘牓娅庨弮鍫曟？閹村啿顦婚敍?  - 闂呮劗顫嗙€瑰鍙忛敍姘崇翻閸戣桨绗夐崥顐㈠斧婵寮芥＃鍫熸瀮閺堫兙鈧胶绱潏鎴炴瀮閺堫兙鈧胶鏁ら幋宄邦槵濞夈劍鍨ㄦ潏鍦櫕婢跺洦鏁?- T163-T164 韫囧懘銆忔穱婵堟殌閻ㄥ嫮瀹抽弶鐕傜窗
  - 閹绘劖顢嶉悩鑸碘偓浣割潗缂佸牅璐?`candidate`閿涘163 review CLI 閹靛秷鍏樼亸鍡楀従閺€閫涜礋 `approved`
  - `is_runtime_ready()` 娓氭繆绂?`status == "approved"` 娑?`review_metadata.reviewed_by_human == True` 娑?`review_metadata.last_decision == "approved"`
  - `positive_examples` / `negative_examples` 閸?proposal 闂冭埖顔屾稉铏光敄閿涘163 review 閹存牕鎮楃紒顓濇崲閸斺€冲讲鐞涖儱鍘栫€瑰鍙忛幗妯款洣
  - `patch_id` 娴ｈ法鏁?`new_id("patch")` 閻㈢喐鍨氶敍鍫ユ姜绾喖鐣鹃幀褝绱氶敍灞肩稻閸忔湹绮幍鈧張澶婄摟濞堢數鏁?cluster 鏉堟挸鍙嗙涵顔肩暰閹冨枀鐎?  - T164 閸欘亜褰插☉鍫ｅ瀭 `status == "approved"` 娑?`is_runtime_ready() == True` 閻?patch
## 61. T162 Review Decision

- Review file:
  - `docs/review/T162_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T162 is complete within task scope.
  - The repo now has a deterministic, candidate-only patch proposal layer for M5.
  - No T162 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N05 `.claude/settings.json` is a workspace artifact rather than a task-scope violation.
  - Deferred:
    - N01 the contract still overclaims deterministic `patch_id` behavior even though implementation uses UUID-based `new_id("patch")`.
    - N02 raw `input_path` remains present in proposal stdout/output.
    - N03 no committed automated tests yet cover `PatchProposalService` / `chat-feedback-propose-patch`.
    - N04 malformed cluster input with empty `contact_id` can still crash proposal generation instead of being skipped defensively.
  - Rejected:
    - none

## 62. T163 Kickoff Notes

- Task package:
  - `docs/tasks/M5_feedback_to_patch/T163_patch_review_cli.md`
- Worker focus:
  - add explicit human review actions for `PreferencePatchCandidate` proposal reports
  - preserve proposal evidence, review metadata, and decision history without mutating runtime state
  - keep approval semantics explicit and separate from runtime context wiring
- Explicit non-goals:
  - no auto-approve or auto-apply
  - no runtime injection or compact-context consumption yet
  - no ContactSkill/Memory mutation
  - no outbound send behavior, no realtime integration, no LLM use
  - no rewriting proposal content or inventing new evidence during review
- Reviewer focus:
  - confirm review actions are explicit, auditable, and human-gated
  - confirm rejected/frozen/archived patches do not become runtime-ready
  - confirm stdout/artifacts remain privacy-safe and no runtime mutation behavior is smuggled into the review layer

## 63. T163 Implementation Record

- 娴狅絿鐖?/ 閺傚洦銆傞弨鐟板З閿?  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/data_contracts/preference_patch_contract.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- 瀹告彃鐤勯悳鏉垮敶鐎圭櫢绱?  - 閺傛澘顤?`PatchReviewService`閿涘苯顕?T162 閹绘劖顢嶉幎銉ユ啞娑擃厾娈?`PreferencePatchCandidate` 閹笛嗩攽閺勬儳绱℃禍鍝勪紣 review 閸愬磭鐡ラ妴?  - 閺傛澘顤?`chat-feedback-review-patch` CLI閿涘本鏁幐?`--input`閿涘牆绻€闂団偓閿涘鈧梗--patch-id`閿涘牆绻€闂団偓閿涘鈧梗--decision`閿涘牆绻€闂団偓閿涘畮pprove/reject/freeze/archive閿涘鈧梗--reviewer`閿涘牆绻€闂団偓閿涘鈧梗--note`閿涘牆褰查柅澶涚礆閵嗕梗--output`閿涘牆褰查柅澶涚礆閵?  - Review CLI 閸氬秶袨閿涙瓪chat-feedback-review-patch`
  - 閸愬磭鐡ョ猾璇茬€锋稉搴ｅЦ閹焦妲х亸鍕剁窗
    - `approve` 閳?`approved`閿涘潉is_runtime_ready()` 鏉╂柨娲?`True`閿?    - `reject` 閳?`rejected`閿涘潉is_runtime_ready()` 鏉╂柨娲?`False`閿?    - `freeze` 閳?`frozen`閿涘潉is_runtime_ready()` 鏉╂柨娲?`False`閿?    - `archive` 閳?`archived`閿涘潉is_runtime_ready()` 鏉╂柨娲?`False`閿?  - 濮ｅ繑顐奸崘宕囩摜鏉╄棄濮?`DistilledArtifactReviewDecision` 閸?`review_metadata.history`閿涘苯宸婚崣韫瑝鐟曞棛娲婇妴?  - `review_metadata.reviewed_by_human`閵嗕梗last_decision`閵嗕梗last_reviewed_at`閵嗕梗last_reviewer_id` 闂呭繑娓堕弬鏉垮枀缁涙牗娲块弬鑸偓?  - Evidence 鐎涙顔岄敍鍧剆upporting_feedback_ids`閵嗕梗supporting_cluster_ids`閵嗕梗claim`閵嗕梗behavior_instruction`閵嗕梗confidence`閵嗕梗sensitivity`閿涘婀?review 鏉╁洨鈻兼稉顓濈瑝鐞氼偂鎱ㄩ弨骞库偓?  - 閺堫亙鎱ㄩ弨?ContactSkill/Memory/store records閵嗕焦婀拫鍐暏 LLM閵嗕焦婀懛顏勫З approve 閹?apply閵嗕焦婀▔銊ュ弳 runtime context閵?- 閸氬牊鍨氭宀冪槈缁€杞扮伐閿?  - 鏉堟挸鍙嗛敍姘儓 4 娑?candidate patch 閻ㄥ嫬鎮庨幋?T162 閹绘劖顢嶉幎銉ユ啞
  - Test 1: approve 閳?status=approved, is_runtime_ready=True, history_count=1, evidence preserved
  - Test 2: reject 閳?status=rejected, is_runtime_ready=False, evidence preserved
  - Test 3: freeze 閳?status=frozen, is_runtime_ready=False
  - Test 4: archive 閳?status=archived, is_runtime_ready=False
  - Test 5: re-approve after reject 閳?history_count=2, is_runtime_ready=True, last_reviewer_id updated
  - Test 6: invalid decision 閳?FeedbackError with expected message
  - Test 7: missing patch_id 閳?FeedbackError with list of available ids
  - Test 8: privacy safety 閳?no raw text, no extra fields in written-back file
  - Test 9: output to separate file 閳?input unchanged
  - Test 10: separate output preserves original input
  - 176 existing tests pass with zero regressions
- T164 韫囧懘銆忔穱婵堟殌閻ㄥ嫮瀹抽弶鐕傜窗
  - T164 閸欘亜褰插☉鍫ｅ瀭 `status == "approved"` 娑?`is_runtime_ready() == True` 閻?patch
  - review history 瀹告彃鍟撻崗銉﹀絹濡楀牊濮ら崨?JSON閿涘164 娑撳秴褰插〒鍛存珟閹存牞顩惄?history
  - review metadata 娴ｈ法鏁?`DistilledArtifactReviewMetadata` 娑?T122 鐎光剝鐓″Ο鈥崇础娑撯偓閼?  - stdout 閸滃矁绶崙杞扮瑝閸氼偄甯慨瀣冀妫ｅ牊鏋冮張顑锯偓浣虹椽鏉堟垶鏋冮張顑锯偓浣烘暏閹村嘲顦▔銊﹀灗鏉堝湱鏅径鍥ㄦ暈
## 64. T163 Review Decision

- Review file:
  - `docs/review/T163_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T163 is complete within task scope.
  - The repo now has explicit human review actions for patch candidates.
  - No T163 warning is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N05 `.claude/settings.json` is a workspace artifact rather than a task-scope violation.
  - Deferred:
    - N01 the contract still overclaims deterministic `patch_id` behavior even after T163 touched the contract file.
    - N02 no committed automated tests yet cover `PatchReviewService` / `chat-feedback-review-patch`.
    - N03 write-back to the input file by default when `--output` is not specified can risk in-place corruption on write failure.
    - N04 repeated review decisions can grow `review_metadata.history` without bound.
  - Rejected:
    - none

## 65. T164 Kickoff Notes

- Task package:
  - `docs/tasks/M5_feedback_to_patch/T164_approved_patch_context.md`
- Worker focus:
  - consume only approved, runtime-ready patches into `ChatContext`
  - preserve review history and evidence while exposing only compact communication hints
  - keep context integration approval-gated, privacy-safe, and non-mutating
- Explicit non-goals:
  - no candidate/rejected/frozen/archived injection
  - no auto-approve or auto-apply
  - no ContactSkill/Memory mutation
  - no outbound send behavior, no realtime integration, no LLM use
  - no raw feedback text, edited text, user notes, boundary notes, or draft text in context
- Reviewer focus:
  - confirm only approved/runtime-ready patches enter context
  - confirm review history survives untouched
  - confirm context output stays compact and privacy-safe

## 66. T164 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/services/chat_context.py`
  - `docs/data_contracts/preference_patch_contract.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Models added:
  - `ApprovedPatchBrief`: compact brief for a single approved, runtime-ready patch. Fields: `patch_id`, `patch_type`, `compact_instruction` (max 160 chars from `behavior_instruction`), `sensitivity`, `supporting_feedback_count`, `supporting_cluster_ids`.
  - `ApprovedPatchContext`: wrapper for approved patch briefs. Fields: `status` (reuses `ApprovedStoreContextStatus`), `source_path`, `contact_id`, `patches`, `notes`.
  - `ChatContext.approved_patch_context`: new field, defaults to `ApprovedPatchContext(status="not_configured")`.
- Service added in feedback.py:
  - `ApprovedPatchContextService.load_approved_patches(report_path, contact_id) -> ApprovedPatchContext`:
    - Reads a reviewed T162/T163 `patch_proposal_v1` report.
    - Validates each candidate patch via `PreferencePatchCandidate.model_validate`.
    - Filters: `status == "approved"` AND `is_runtime_ready() == True` AND `contact_id` match.
    - Candidate, rejected, frozen, and archived patches are excluded silently.
    - Builds compact `ApprovedPatchBrief` with truncated `behavior_instruction` and feedback count (not raw IDs).
    - Returns `not_configured`, `store_path_missing`, `no_runtime_ready_records`, or `loaded`.
- ChatContextAssembler changes:
  - New constructor parameter: `approved_patch_path: Path | None = None`.
  - `_load_approved_patch_context()`: resolves path via existing `_resolve_configured_store_path`, delegates to `ApprovedPatchContextService`.
  - `_build_approved_patch_notes()`: emits compact patch notes with patch_id, patch_type, compact_instruction, sensitivity, and feedback_count (max 4 patches in notes).
  - `_build_summary()`: appends compact patch hints (max 3 patches, 200 chars total) to context summary.
  - `assemble()`: wires approved_patch_context into returned `ChatContext`, appends patch notes to `memory_retrieval_notes`.
- Approved/runtime-ready filtering rules:
  - `patch.contact_id == contact_id`
  - `patch.status == "approved"`
  - `patch.is_runtime_ready() == True`
  - All three conditions must be satisfied simultaneously.
- Privacy safety:
  - NO raw feedback text, edited text, user notes, boundary notes, or draft text in context.
  - `supporting_feedback_ids` reduced to count; raw IDs not exposed.
  - `behavior_instruction` truncated to 160 chars in compact brief.
  - Review history stays in source report, never expanded into context.
  - Non-approved patches excluded entirely.
- Verification:
  - Compile passed for models.py, feedback.py, chat_context.py.
  - Existing 176 tests expected to pass with zero regressions.
  - Repo now includes `tests/test_t164_synthetic.py` with 13 synthetic tests covering `ApprovedPatchContextService` filtering and compact brief construction.
- Remaining risks:
  - Remaining committed-coverage gaps are frozen/archived exclusion cases, `ChatContextAssembler` approved-patch path integration, and empty/whitespace `behavior_instruction` handling.
  - `ChatContextAssembler` path validation reuses `_ensure_within_private_distilled` from T123, which guards against configured paths outside `private/distilled/`.
  - Patch briefs expose `supporting_cluster_ids` as-is; these are deterministic labels from T161 and contain no raw text.
- Follow-up constraints for later M5+ tasks:
  - Only `ApprovedPatchContextService` may load and filter patches for context; do not bypass the approval/runtime-ready gate.
  - If a future task adds LLM consumption of patch hints, it must preserve the existing compact/privacy-safe constraints.
  - `ApprovedPatchBrief` shape should remain stable as a context contract; adding fields is safer than removing or renaming.

## 67. T164 Review Decision

- Review file:
  - `docs/review/T164_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T164 is complete within task scope.
  - The repo now has an approved-only, compact patch-context path that stays review-only, privacy-safe, and non-mutating.
  - No T164 finding is blocking enough to require an automatic repair pass.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` is a workspace artifact rather than a task-scope violation.
    - N02 duplicated `_compact_text` is low-risk refactor debt.
    - N03 `ApprovedPatchContext.status` reuses a broader status enum than the patch-context path strictly needs.
    - N04 `_load_approved_patch_context()` instantiates a new `ApprovedPatchContextService()` per `assemble()` call, which is acceptable for the current offline workflow.
    - N05 the previous handoff wording understated existing synthetic test coverage and is corrected here.
    - N06 carrying deterministic `supporting_cluster_ids` in compact briefs is privacy-safe.
  - Deferred:
    - M01 no explicit frozen/archived exclusion test fixtures exist yet.
    - M02 no end-to-end `ChatContextAssembler` integration test covers the approved-patch load/build/summary path.
    - M03 no dedicated test covers empty or whitespace-only `behavior_instruction`.
  - Rejected:
    - none

## 68. T170 Implementation Record

- Files changed:
  - `docs/architecture/contactskill_decomposition.md` (new)
  - `docs/07_handoff.md`
- Design summary:
  - Proposed three derived briefs: `PartnerPersonaBrief`, `CommunicationPolicyBrief`, `BoundaryProfileBrief`.
  - Each brief is a projection from an approved `ContactSkillStoreRecord`, not a replacement.
  - Briefs are lazy (computed at assembly time), not separately stored or separately approved.
  - Fallback to existing `ApprovedContactSkillBrief` is guaranteed when derived briefs are absent.
  - Evidence refs are projected per-area from sub-model evidence; top-level refs remain on the parent aggregate.
  - Approval is inherited from the parent store record; no separate approval workflow for briefs.
  - Field ownership table maps all 20+ ContactSkill areas to specific briefs or to the fallback aggregate.
  - Three additive phases: schema definition (T171-T172), projection service (T173), context integration (T174).
- Compatibility guarantees preserved:
  - ContactSkill is not deleted, replaced, or deprecated.
  - T120-T164 pipeline is not modified.
  - Persona-clone / impersonation / autonomous-contact boundaries are unchanged.
  - No code changes, no data migration, no new storage format.
- Follow-up schema tasks now unblocked:
  - T171: `PartnerPersonaBrief` schema.
  - T172: `CommunicationPolicyBrief` + `BoundaryProfileBrief` schemas.
  - T173: `ContactSkillProjectionService` (lazy projection from approved store records).
  - T174: Derived-brief context integration in `ChatContextAssembler`.
- Open questions deferred:
  - Lazy vs. materialized briefs (performance question for later).
  - Cross-contact briefs (global policy brief deferred to M8+).
  - Brief versioning (may be needed if schemas evolve; deferred to T171-T172).
  - PartnerPersonaBrief + RelationshipState overlap (deferred to M8 design).
- Verification:
  - Document references T120-T123 (approved store, evidence validation, review CLI, context integration).
  - Document references T130-T133 (ReplyPlan schema, planner, policy, holdout eval).
  - Document references T160-T164 (PreferencePatch schema, clustering, proposal, review, compact context).
  - Document explicitly states existing approved ContactSkill data remains runnable.
  - Document makes clear decomposition is projection/addition, not replacement.
  - No code was edited, no migration was defined, no deprecation was claimed.

## 69. T170 Review Decision

- Review file:
  - `docs/review/T170_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T170 is complete within task scope.
  - The repo now has a documented compatibility-first decomposition contract for approved `ContactSkill`.
  - No automatic repair pass is needed because no blocking issue was found.
- Follow-up notes carried forward:
  - T171 must resolve whether `PartnerPersonaBrief.communication_style_snapshot` stays `dict[str, str]` or becomes a structured sub-model.
  - T172 must formalize `BoundaryProfileBrief.sensitivity_summary` reduction semantics.
  - T172/T174 may revisit `important_event_summaries` ownership only if runtime use proves the persona layer truly needs that context.
  - T172 or later may document how future boundary-signaling patch hints relate to `BoundaryProfileBrief` without broadening current patch semantics.
  - The handoff section-number churn noted by review is accepted as maintenance noise only.
- Next worker task:
  - T171 `PartnerPersonaBrief` Schema.
  - The task remains additive and schema-only; no runtime integration is authorized yet.

## 70. T171 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/contactskill_decomposition_contract.md` (new)
  - `tests/test_contactskill_persona_brief.py` (new)
  - `docs/07_handoff.md`
- Models added:
  - `CommunicationStyleSnapshot`: structured Pydantic model with four optional string fields (message_length, tone, response_latency, directness). Promoted from `dict[str, str]` as sketched in T170 because all keys are known and stable, and a named model provides type safety, self-documentation, and Pydantic validation.
  - `PartnerPersonaBrief`: derived brief for who this person is, how the relationship stands, and how they communicate. Fields: contact_id, relationship_type, relationship_state_summary, communication_style_snapshot, preferred_topics, emotional_pattern_labels, evidence_refs, source_skill_record_id.
- `communication_style_snapshot` typing decision:
  - Chose structured sub-model (`CommunicationStyleSnapshot`) over `dict[str, str]`.
  - Reason: the four dimensions are known upfront and map 1:1 from `ContactSkillCommunicationStyle`. A named model prevents typos, enables IDE support, and is consistent with the rest of the codebase. The T170 review note N02 is resolved.
- Evidence / `source_skill_record_id` traceability:
  - `evidence_refs` collects per-area evidence from relationship_state, communication_style, preferred_topics, and emotional_patterns sub-models. Top-level `ContactSkillCandidate.evidence_refs` are NOT projected into this brief.
  - `source_skill_record_id` is required and non-empty, providing a single traceability pointer to the parent `ContactSkillStoreRecord`.
  - The brief does not carry its own `status`, `review_metadata`, or approval fields. Approval is inherited from the parent record.
- Fallback relationship:
  - `PartnerPersonaBrief` is an optional overlay. `ApprovedContactSkillBrief` remains the minimum guaranteed output.
  - The brief does not replace or deprecate `ApprovedContactSkillBrief`.
- Verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py`: passed.
  - `pytest tests/test_contactskill_persona_brief.py -q`: 21 passed.
  - `pytest tests/ -q`: 210 passed (189 existing + 21 new), zero regressions.
- What T172 still needs to define:
  - `CommunicationPolicyBrief` schema (reply strategy + user-side preferences + stable preferences + approved patch hints).
  - `BoundaryProfileBrief` schema (avoid topics + boundary rules + disallowed uses + usage notes + important events + sensitivity_summary).
  - Formalize `BoundaryProfileBrief.sensitivity_summary` reduction semantics (T170 review N01).
  - Document how boundary-signaling patch hints relate to boundary ownership (T170 review N04).

## 71. T171 Review Decision

- Review file:
  - `docs/review/T171_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T171 is complete within task scope.
  - The repo now has the first committed derived-brief schema and contract for approved `ContactSkill`.
  - No automatic repair pass is needed because no blocking issue was found.
- Follow-up notes carried forward:
  - N01 `.claude/settings.json` is accepted as a workspace artifact rather than a task-scope defect.
  - N02 the `ContactSkillCommunicationStyle` `"unknown"` -> brief `None` conversion rule is deferred to T173 projection logic and documentation.
  - N03 `relationship_state_summary` stays free-form at schema stage; T173 must document how it is composed from `ContactSkillRelationshipState`.
  - N04 flat brief-level `evidence_refs` is accepted as the current contract; later tasks must preserve it unless a future schema change explicitly widens scope.
  - N05 missing brief-local `schema_version` is low risk now; T172 must explicitly decide whether later briefs add their own version marker or continue relying on parent-store versioning.
- Next worker task:
  - T172 `CommunicationPolicyBrief` + `BoundaryProfileBrief` Schemas.
  - The task remains additive and schema-only; no projection or runtime integration is authorized yet.

## 72. T172 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/contactskill_decomposition_contract.md`
  - `tests/test_contactskill_policy_briefs.py` (new)
  - `docs/07_handoff.md`
- Models added:
  - `CommunicationPolicyBrief`: how the system should draft replies. Fields: contact_id, default_approach, cold_contact_approach, topic_opener_approach, sensitive_topic_approach, user_goal, preferred_reply_style, stable_preference_hints, approved_patch_hints, evidence_refs, source_skill_record_id.
  - `BoundaryProfileBrief`: what to avoid, what is sensitive, and what the hard limits are. Fields: contact_id, avoid_topics, boundary_rules, disallowed_uses, usage_notes, important_event_summaries, sensitivity_summary, evidence_refs, source_skill_record_id.
- Fields belonging to CommunicationPolicyBrief vs BoundaryProfileBrief:
  - CommunicationPolicyBrief: reply_strategy (default, cold, topic_opener, sensitive), user_side_preferences (user_goal, preferred_reply_style), stable_preferences (pattern strings), approved_patch_hints.
  - BoundaryProfileBrief: avoid_topics (topic strings), user_side_preferences.boundaries (boundary_rules), usage_boundary (disallowed_uses, usage_notes), important_events (compact summaries), sensitivity_summary.
- Finalized sensitivity reduction rule (T170 N01):
  - `sensitivity_summary = max(avoid_topics sensitivities, important_events sensitivities, parent aggregate sensitivity)`.
  - Ordering: "low" < "medium" < "high".
  - Parent aggregate sensitivity serves as a floor; sub-model sensitivities can raise it.
  - If no avoid_topics and no important_events exist, the result is the parent aggregate sensitivity.
- Final ownership decision for important_event_summaries (T170 N03):
  - Stays in BoundaryProfileBrief because important events can be sensitive, and the boundary profile carries the sensitivity_summary needed to govern how aggressively to reference them.
- Versioning decision for derived briefs (T171 N05):
  - Derived briefs do NOT carry their own `schema_version`. Versioning is inherited through `source_skill_record_id` pointing to the parent `ContactSkillStoreRecord`, which carries `schema_version`.
- How approved patch hints are handled without broadening patch semantics (T170 N04):
  - `approved_patch_hints` lives on `CommunicationPolicyBrief` only. Patches are communication instructions, and the policy brief is the correct owner. BoundaryProfileBrief does NOT get its own patch-hints field. This avoids duplicating T164's single-source patch contract.
- Verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py`: passed.
  - `pytest tests/test_contactskill_policy_briefs.py -q`: 31 passed.
  - `pytest tests/ -q`: 241 passed (210 existing + 31 new), zero regressions.
- What T173 can now assume for projection logic:
  - All three brief schemas (PartnerPersonaBrief, CommunicationPolicyBrief, BoundaryProfileBrief) are defined.
  - Each brief has `contact_id`, `evidence_refs`, and `source_skill_record_id` for traceability.
  - The sensitivity reduction rule is specified (Section 7 of contract doc).
  - Patch enrichment for CommunicationPolicyBrief uses existing `ApprovedPatchBrief` from T164.
  - None of the briefs carry their own approval or status fields; T173 checks `record.is_runtime_ready()` before projecting.

## 73. T172 Review Decision

- Review file:
  - `docs/review/T172_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T172 is complete within task scope.
  - The repo now has committed policy and boundary derived-brief schemas and the corresponding contract notes.
  - No automatic repair pass is needed because no blocking issue was found.
- Follow-up notes carried forward:
  - N01 thin `CommunicationPolicyBrief.evidence_refs` is accepted as an upstream-model limitation; T173 must preserve it and must not invent synthetic evidence for reply strategy or user-side preference fields.
  - N02 `BoundaryProfileBrief.sensitivity_summary` default is a schema fallback only; T173 must compute the actual value explicitly.
  - N03 `important_event_summaries` format remains a projection concern; T173 must keep formatting deterministic and documented.
  - N04 `.claude/settings.json` is accepted as a workspace artifact rather than a task-scope defect.
- Next worker task:
  - T173 `ContactSkillProjectionService`.
  - The task remains additive and projection-only; no runtime context integration is authorized yet.

## 74. T173 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/contact_skill.py`
  - `tests/test_contactskill_projection.py` (new)
  - `docs/07_handoff.md`
- Entrypoint:
  - `ContactSkillProjectionService.project_all(record, approved_patch_hints=None) -> ContactSkillProjectionResult`
  - Returns a frozen dataclass with `record_id`, `contact_id`, `runtime_ready`, and optional `persona`, `policy`, `boundary` briefs.
- Runtime-ready gating:
  - `record.is_runtime_ready()` must return `True` (status=approved, reviewed_by_human=True, last_decision=approved).
  - Non-runtime-ready records produce a result with `runtime_ready=False` and all three briefs set to `None`.
  - Candidate, rejected, frozen, and archived records are excluded.
- How each brief is built:
  - **PartnerPersonaBrief**: `contact_id` from skill, `relationship_type` from skill, `relationship_state_summary` formatted as `"{current_status}, closeness={closeness:.2f}, trust={trust_level:.2f}, freq={interaction_frequency}, initiative={initiative_balance}"`, `communication_style_snapshot` projected with `"unknown"` 閳?`None` conversion, `preferred_topics` as topic strings, `emotional_pattern_labels` as pattern strings, `evidence_refs` as union of relationship_state + communication_style + preferred_topics + emotional_patterns refs, `source_skill_record_id` from record.
  - **CommunicationPolicyBrief**: reply strategy fields (default, cold, topic_opener, sensitive) projected from `ContactSkillReplyStrategy`, user-side preferences (user_goal, preferred_reply_style) projected from `ContactSkillUserSidePreferences`, `stable_preference_hints` as pattern strings from `ContactSkillPattern`, `approved_patch_hints` passed through from optional parameter (empty by default 閳?T174 wires the T164 patch loading), `evidence_refs` only from `stable_preferences` entries (faithfully thin 閳?no synthetic evidence for reply strategy or user-side preferences).
  - **BoundaryProfileBrief**: `avoid_topics` as topic strings, `boundary_rules` from `user_side_preferences.boundaries`, `disallowed_uses` and `usage_notes` from `usage_boundary`, `important_event_summaries` formatted as `"{event} ({date})"` when date exists or `"{event}"` when absent, `sensitivity_summary` computed as `max(avoid_topics sensitivities + important_events sensitivities + parent aggregate sensitivity)` with parent floor, `evidence_refs` as union of avoid_topics + important_events refs.
- Deterministic guarantees:
  - Same `ContactSkillStoreRecord` input always produces the same briefs.
  - Projection writes nothing to disk.
  - No LLM calls, no raw chat history reads, no ContactSkill mutation.
- Verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/contact_skill.py`: passed.
  - `pytest tests/test_contactskill_projection.py -v`: 47 passed.
  - `pytest tests/ -q`: 288 passed (241 existing + 47 new), zero regressions.
- What T174 can now consume safely:
  - `ContactSkillProjectionResult` with all three briefs available when the parent record is runtime-ready.
  - `approved_patch_hints` slot on `CommunicationPolicyBrief` ready for T164 patch wiring.
  - All briefs carry `contact_id`, `evidence_refs`, and `source_skill_record_id` for traceability and fallback alignment.
  - `BoundaryProfileBrief.sensitivity_summary` is explicitly computed (not the schema default).
  - `important_event_summaries` are deterministically formatted.
  - The projection is pure/additive: `ApprovedContactSkillBrief` fallback remains intact and untouched.

## 75. T173 Review Decision

- Review file:
  - `docs/review/T173_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T173 is complete within task scope.
  - The repo now has a committed lazy projection layer from approved store records into all three derived briefs.
  - No automatic repair pass is needed because no blocking issue was found.
- Follow-up notes carried forward:
  - N01 `.claude/settings.json` is accepted as a workspace artifact rather than a task-scope defect.
  - N02 trivial persona-field projection assertions are not required as a separate follow-up task; current coverage is sufficient.
  - N03 unreachable `_max_sensitivity` default handling is accepted as harmless redundancy.
  - N04 `relationship_state_summary` formatting is now a projection-owned contract; T174 must not reinterpret or silently reformat it in context assembly.
- Next worker task:
  - T174 `Derived Briefs Context Integration`.
  - The task remains additive and context-integration-only; no planner behavior change is authorized yet.

## 76. T174 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/chat_context.py`
  - `tests/test_chat_context_decomposition.py` (new)
  - `docs/07_handoff.md`
- Models added:
  - `DerivedBriefContext`: wrapper for the three T173-derived briefs. Fields: `status` (reuses `ApprovedStoreContextStatus`), `persona: PartnerPersonaBrief | None`, `policy: CommunicationPolicyBrief | None`, `boundary: BoundaryProfileBrief | None`, `source_skill_record_id: str | None`, `notes: list[str]`.
  - `ChatContext.derived_brief_context`: new field, defaults to `DerivedBriefContext(status="not_configured")`.
- ChatContextAssembler changes:
  - `_load_runtime_ready_contact_skill_brief` now returns `tuple[ApprovedContactSkillBrief | None, ContactSkillStoreRecord | None]` to expose the eligible record for projection.
  - `_load_approved_store_context` now returns `tuple[ApprovedStoreContext, ContactSkillStoreRecord | None]`.
  - New `_load_derived_brief_context(contact_id, skill_record, approved_patch_briefs)`: uses `ContactSkillProjectionService.project_all()` to produce derived briefs from the eligible record. Passes approved T164 patch briefs into the projection for `CommunicationPolicyBrief.approved_patch_hints`.
  - New `_build_derived_brief_notes(context)`: emits compact derived-brief notes including `source_skill_record_id`, `relationship_state_summary`, `stable_preference_hints`, and `sensitivity_summary`.
  - `_build_summary` extended with `derived_brief_context` parameter; appends derived persona and boundary-sensitivity lines to context summary when derived briefs are loaded.
  - `assemble()` wires the new derived-brief path: unpacks eligible record from store loading, passes approved patches to projection, adds derived-brief notes to `memory_retrieval_notes`, and includes `derived_brief_context` in returned `ChatContext`.
- Fallback behavior:
  - When `approved_store_path` is `None`, `derived_brief_context.status` is `"not_configured"` and all briefs are `None`. Existing `ApprovedContactSkillBrief` path is unchanged.
  - When store exists but no runtime-ready records match, `derived_brief_context.status` is `"not_configured"`. The `ApprovedStoreContext` reports `"no_runtime_ready_records"` independently.
  - When store is loaded with an eligible skill record, `derived_brief_context.status` is `"loaded"` and all three briefs are populated. `ApprovedContactSkillBrief` is also loaded alongside.
- Approved-patch context coexistence:
  - `ApprovedPatchContext` (T164) remains a separate compact context path. It is loaded independently of derived briefs.
  - Approved patches are passed to the projection service for `CommunicationPolicyBrief.approved_patch_hints`, so the policy brief carries the same patches as `ApprovedPatchContext`.
  - Both `ApprovedPatchContext` and `DerivedBriefContext` coexist on `ChatContext` without replacing each other.
- Projection output preservation:
  - `relationship_state_summary`, `important_event_summaries`, and `sensitivity_summary` are preserved as projection-owned outputs. The assembler does not reformat or reinterpret them.
  - Thin `CommunicationPolicyBrief.evidence_refs` (from `stable_preferences` only) is preserved without backfilling.
  - `"unknown"` 閳?`None` communication-style conversion is preserved from projection.
- Verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/chat_context.py`: passed.
  - `pytest tests/test_chat_context_decomposition.py -q`: 39 passed.
  - `pytest tests/ -q`: 327 passed (288 existing + 39 new), zero regressions.
- What remains unchanged:
  - The existing T123 `ApprovedContactSkillBrief` fallback path is fully preserved.
  - The T164 approved-patch compact context path is separate and unmodified.
  - ReplyPlanner, policy engine, and feedback CLI behavior are unchanged.
  - No new persistence, migration, or CLI commands were added.

## 77. T174 Review Decision

- Review file:
  - `docs/review/T174_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T174 is complete within task scope.
  - The repo now has additive derived-brief context integration with preserved fallback behavior.
  - No automatic repair pass is needed because no blocking issue was found.
- Follow-up notes carried forward:
  - N01 `.claude/settings.json` is accepted as a workspace artifact rather than a task-scope defect.
  - N02 per-assembly projection-service instantiation is accepted as low-impact offline overhead.
  - N03 `DerivedBriefContext.status` enum breadth is accepted as a benign consistency trade-off.
  - N04 unused `contact_id` parameter on `_load_derived_brief_context` is accepted as minor dead surface area.
  - N05 `stable_preference_hints[:2]` truncation is accepted as minor context-budget debt.
  - M01/M02/M03 are accepted as non-blocking residual synthetic-coverage gaps for the current stage.
- Next worker task:
  - none inside M6; proceed to milestone review.

## 78. M6 Review Decision

- Review file:
  - `docs/review/M6_review.md`
- Verdict:
  - `Allow`
- Captain decision:
  - M6 is complete and the project may enter M7.
  - The next recommended Current Unique Task is T180 `LLM Candidate Generator Contract`.
  - M7 opens only at the contract-definition layer; no model calls or hybrid planner behavior are authorized yet.

## 79. T170 Kickoff Notes

- Task package:
  - `docs/tasks/M6_contactskill_decomposition/T170_decomposition_design.md`
- Worker focus:
  - design a compatibility-first decomposition from approved `ContactSkill` into smaller derived briefs
  - keep evidence ownership, approval boundaries, and fallback behavior explicit
  - preserve the existing T120-T164 runtime and review contracts
- Explicit non-goals:
  - no code edits
  - no ContactSkill behavior change
  - no data migration
  - no deprecation or replacement claim for `ContactSkill`
  - no LLM behavior changes, runtime mutation, or platform work
- Reviewer focus:
  - confirm the design is additive and compatibility-first
  - confirm evidence refs and approval gates remain preserved across any derived-brief projection
  - confirm the document does not smuggle in a breaking migration plan or persona-clone scope creep

## 80. T180 Implementation Record

- Files changed:
  - `docs/data_contracts/llm_candidate_generator_contract.md` (new)
  - `docs/07_handoff.md`
- Contract shape:
  - Defines `LLMReplyPlan` as an extension of the T130 `ReplyPlan` contract with added `generator_type`, `generation_metadata`, and `refusal` fields.
  - Each candidate carries a `generator_type` literal (`"template_deterministic"` or `"llm_generated"`) for attributable routing.
  - Input contract limits LLM consumption to existing compact-context boundaries (T123/T164/T174). Raw chat transcripts, full store JSON dumps, and private/chat_history content are explicitly prohibited.
  - Output contract requires at least 1 `supporting_context_ref` and 1 `boundary_reminder` per candidate, matching T130 `ReplyPlanCandidate` requirements.
  - Structured refusal shape defined with codes: `PROVIDER_ERROR`, `INPUT_TOO_LARGE`, `MISSING_REQUIRED_CONTEXT`, `SAFETY_FILTER`, `INVALID_OUTPUT_SCHEMA`.
- Safety / privacy / no-impersonation constraints:
  - Input must use existing compact-context boundaries only; no new input-assembly path is authorized.
  - Privacy leakage detection (verbatim input echo) is a required deterministic validator check.
  - No first-person contact impersonation, no contact simulation, no relationship speculation without evidence refs.
  - `generator_type` field enables downstream attribution of LLM vs. deterministic output.
  - Deterministic validation boundary: generation may use LLM (non-deterministic), but acceptance before review must be fully deterministic (schema check, ref scope, rank uniqueness, privacy, impersonation).
- What T181 may implement next:
  - An offline CLI that consumes a `ChatContext` JSON and produces an `LLMReplyPlan`.
  - A generator service calling an LLM provider through an OpenAI-compatible adapter.
  - Deterministic post-generation validation of LLM output.
  - Structured refusal handling.
- What remains intentionally forbidden after T180:
  - Hybrid `ReplyPlanner` (merging deterministic + LLM candidates) 閳?deferred to T183.
  - Auto-approval or auto-injection of LLM candidates into any runtime path.
  - Changes to the existing deterministic `ReplyPlanner` or `ReplyPlanPolicyEngine`.
  - Storing or caching LLM outputs beyond the generator's output file.
  - Supplying raw chat transcript, full store JSON, or non-compact context as input.
  - Bypassing policy/boundary review or human approval for any LLM-generated candidate.
  - Any claim that LLM candidates are enabled, production-ready, or quality-proven.

## 81. T180 Review Decision

- Review file:
  - `docs/review/T180_review.md`
- Verdict:
  - `PASS`
- Captain decision:
  - T180 is complete within task scope.
  - The repo now has a committed additive contract for optional LLM-generated reply candidates.
  - No automatic repair pass is needed because no blocking issue was found.
- Next worker task:
  - T181 `LLM Candidate Offline CLI`.
  - The task must remain offline, opt-in, validated, and separate from the existing deterministic `ReplyPlanner`.


## 82. T181 Implementation Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/llm_reply_generator.py` (new)
  - `src/practical_chat_agent/app/main.py`
  - `tests/test_llm_reply_generator.py` (new)
  - `docs/07_handoff.md`
- CLI name: `chat-reply-generate-llm`
  - `--input` (required): safe ChatContext JSON file path.
  - `--output` (required): private output path for LLMReplyPlan JSON artifact.
  - `--dry-run` (optional): load context and print availability status without calling the LLM provider.
  - stdout emits only safe metadata (action, paths, contact_id, candidate_count, generator_type, generator_id, refusal_code/reason).
  - Output is always written to the specified path, even when the result is a structured refusal.
- Models added to `core/models.py`:
  - `LLMGeneratorType`: Literal `"template_deterministic"` | `"llm_generated"`.
  - `LLMGenerationMetadata`: provider, model, temperature, prompt_template_hash, generated_at, latency_ms.
  - `LLMReplyPlanRefusal`: refusal_code (PROVIDER_ERROR | INPUT_TOO_LARGE | MISSING_REQUIRED_CONTEXT | SAFETY_FILTER | INVALID_OUTPUT_SCHEMA), refusal_reason, is_retryable.
  - `LLMReplyPlanCandidate`: extends `ReplyPlanCandidate` with `generator_type` field.
  - `LLMReplyPlan`: schema_version v1, generator_type, generator_id, contact_id, source_context_snapshot, generation_metadata, candidates, refusal.
- Generator service (`services/llm_reply_generator.py`):
  - `LLMReplyGeneratorService`: offline generator that consumes safe `ChatContext` and calls an OpenAI-compatible provider. Uses the same `_post_json` / `_extract_message_content` / `_parse_json_content` pattern as `ChatlogDistillationService`.
  - Input is restricted to compact `ChatContext` fields only (approved_store_context briefs, derived_brief_context, approved_patch_context, recent_event/memory counts). No raw chat history, full store JSON, or non-compact context.
  - Provider errors and unavailable provider are captured as structured refusals, not raised exceptions.
  - Refusal shape follows the T180 contract: refusal_code, refusal_reason, is_retryable.
  - System prompt instructs no impersonation, evidence-grounded generation, conservative defaults.
- Deterministic post-generation validation:
  - `LLMReplyPlanValidator` performs 7 per-candidate checks: non-empty draft_text, >=1 supporting_context_ref, >=1 boundary_reminder, ref types in approved set, generator_type=="llm_generated", no privacy leakage (verbatim input echo), no impersonation patterns.
  - Invalid candidates are excluded silently per the T180 contract.
  - Ranks are re-assigned to a contiguous 1..N sequence after filtering.
  - Privacy leakage check: exact substring match of input context text against draft_text (minimum 8 chars).
  - Impersonation detection: first-person contact voice ("I would say", "he would say"), Chinese impersonation pattern ("鐎佃鏌熸导?), "娴ｆ粈璐?娴?..闊偂鍞?鐟欐帟澹? patterns.
- Verification:
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/llm_reply_generator.py src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/app/main.py`: passed.
  - `pytest tests/test_llm_reply_generator.py -q`: 26 passed.
  - `pytest tests/ -q`: 353 passed (327 existing + 26 new), zero regressions.
- Provider/runtime assumptions verified:
  - Without OPENAI_API_KEY / OPENAI_BASE_URL env vars, the CLI produces a structured refusal at the output path instead of crashing.
  - Dry-run (`--dry-run`) shows LLM availability status without calling the provider.
  - Deterministic validation works independently of provider availability.
  - Live provider access was not available during this task; smoke run with real provider was not executed.
- What T182 may extract or harden next:
  - Standalone `LLMReplyPlanValidator` extraction into its own module for reuse.
  - Hardened prompt template engineering for better candidate quality.
  - Expanded impersonation pattern detection.
  - Input-size budget enforcement (INPUT_TOO_LARGE refusal path).

## 83. T181 Review Decision

- Review file:
  - `docs/review/T181_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T181 is complete within task scope.
  - The repo now has a committed offline LLM candidate CLI that writes validated private artifacts or structured refusals without mutating the existing deterministic planner path.
  - No automatic repair pass is needed because no blocking issue was found.
- Warning disposition:
  - Accepted:
    - N01 allowed-files overrun for `.claude/settings.json` and `docs/reference/AI_coding_workflow.md` is treated as low-risk workspace/process noise rather than a blocker.
    - N02 default `policy_boundary` refs in `_build_candidates` are accepted for the MVP generator stage.
    - N03 redundant `validate_ranks` call is accepted as harmless dead work.
  - Deferred:
    - N04 substring-only privacy leak detection remains validator hardening debt.
    - N05 `INPUT_TOO_LARGE` refusal path remains unimplemented preflight debt.
    - M01 `_build_llm_input` output-shape coverage remains missing.
    - M02 `_parse_provider_response` error-path coverage remains missing.
    - M03 end-to-end generator-to-validator pipeline coverage remains missing.
    - M04 CLI stdout privacy regression coverage remains missing.
  - Rejected: none.
- Next worker task:
  - T182 `Candidate Validator`.
  - The task remains validator-only: extract/harden shared deterministic validation, add explicit budget/refusal handling, and close the missing regression coverage without adding new generation paths or hybrid planner wiring.

## 84. T182 Review Decision

- Review file:
  - `docs/review/T182_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T182 is complete within task scope.
  - The repo now has a committed shared deterministic validator layer and broader regression coverage for template and LLM candidate paths.
  - No automatic repair pass is needed because no blocking issue was found.
- Warning disposition:
  - Accepted:
    - N02 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a blocker.
  - Deferred:
    - N01 the `INPUT_TOO_LARGE` preflight call-site bug keeps the dedicated deterministic refusal path effectively dead.
    - M01 no regression test yet locks the `INPUT_TOO_LARGE` refusal path.
  - Rejected: none.
- Next worker task:
  - T183 `Hybrid ReplyPlanner`.
  - The task remains opt-in and review-only: integrate template and optional LLM candidate paths without making LLM the default, without bypassing validator/policy gating, and without changing compact-context boundaries.

## 85. T183 Review Decision

- Review file:
  - `docs/review/T183_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T183 is complete within task scope.
  - The repo now has a committed opt-in hybrid planner surface that can merge template and optional LLM candidates without making LLM behavior default.
  - No automatic repair pass is needed because no blocking issue was found.
- Warning disposition:
  - Accepted:
    - N01 allowed-files overrun for `.claude/settings.json` is treated as workspace-artifact noise rather than a blocker.
  - Deferred:
    - N02 no committed test exercises the valid LLM-candidate merge success path.
    - M01 no end-to-end hybrid success test exists.
    - M02 no explicit reranked-order assertion after merge exists.
  - Rejected: none.
- Next worker task:
  - T184 `Planner Holdout Eval`.
  - The task remains evaluation-only: compare template vs hybrid outputs on anonymized holdout scenarios, record evidence, and do not modify planner code.

## 86. T184 Review Decision

- Review file:
  - `docs/review/T184_review.md`
- Verdict:
  - `PASS_WITH_WARNINGS`
- Captain decision:
  - T184 is complete within task scope.
  - The repo now has holdout evidence showing the hybrid path improves naturalness and evidence usage, but this is not yet enough to close M7.
  - No automatic repair pass is needed because no blocking issue was found in the task review.
- Warning disposition:
  - Accepted:
    - N01 allowed-files overrun for `.claude/settings.json` is treated as workspace-artifact noise rather than a blocker.
    - N02 self-reported ratings without independent verification are acceptable for the milestone eval scope.
    - N03 candidate-diversity based on `approach_label` count only is an acceptable proxy for this eval.
  - Deferred: none from the task review itself.
  - Rejected: none.
- Next worker task:
  - T185 `Hybrid Planner Language and Safety Alignment`.
  - The task should remain narrow and repair the language/safety/label/merge gaps identified by T184.

## 87. T184 Milestone Review Decision

- Review file:
  - `docs/review/T184_milestone_review.md`
- Verdict:
  - `Conditional`
- Captain decision:
  - Gate M7 is not yet closed.
  - The holdout evidence is real and useful, but it also shows the hybrid path still needs a narrow alignment pass before M8 can be considered.
  - The project may continue to T185, but it should not treat M7 as complete.
- Gate conditions carried forward:
  - LLM output language should match template language (Chinese) or the mixed-language trade-off must be made explicit.
  - LLM draft text must honor thin_context and boundary_sensitive safety intent, not only the policy flag.
  - Hybrid LLM approach labels should follow the template naming convention.
  - A committed synthetic valid-candidate merge test must exist before relying on the hybrid path for broader evaluation claims.
- Next worker task:
  - T185 `Hybrid Planner Language and Safety Alignment`.
  - The task should remain narrow and should not expand planner scope, add provider integrations, or change template-only behavior.

## 84. T182 Implementation Record

- Files added:
  - `src/practical_chat_agent/services/reply_candidate_validator.py`
  - `tests/test_reply_candidate_validator.py`
- Files modified:
  - `src/practical_chat_agent/services/llm_reply_generator.py`
  - `src/practical_chat_agent/services/reply_planner.py`
  - `tests/test_llm_reply_generator.py`
  - `docs/07_handoff.md` (this entry)
- Shared validator module (`reply_candidate_validator.py`):
  - Module-level functions for deterministic validation, no class wrapper:
    - `check_text_non_empty()` 閳?candidate draft must be non-empty
    - `check_supporting_refs()` 閳?at least one supporting context ref
    - `check_boundary_reminders()` 閳?at least one boundary reminder
    - `check_ref_types()` 閳?all ref types in `VALID_REF_TYPES` frozenset
    - `has_privacy_leak()` 閳?two-tier check: full normalized substring (min 8 chars, existing) plus 4+ consecutive word sequence match (new, catches partial fragments)
    - `has_impersonation()` 閳?regex patterns from T181, now reusable
    - `normalize_ranks()` 閳?renumber priority_rank to 1..N (in-place)
    - `check_ranks_contiguous()` 閳?validate rank contiguity (non-mutating)
    - `check_input_size()` 閳?character-count proxy for token budget
  - Constants `VALID_REF_TYPES` (frozenset, 6 types), `MAX_INPUT_CHARS` (20,000), and `_IMPERSONATION_PATTERNS` are module-level and importable for inspection.
- LLMReplyPlanValidator now delegates to shared functions:
  - `_candidate_is_valid()` calls shared `check_text_non_empty`, `check_supporting_refs`, `check_boundary_reminders`, `check_ref_types`, `has_privacy_leak`, `has_impersonation`.
  - `validate()` still does deep-copy + filter + renumber via shared `normalize_ranks`.
  - Dead methods removed: `_IMPERSONATION_PATTERNS`, `_refs_are_valid`, `_ranks_are_contiguous`, `_has_privacy_leak`, `_has_impersonation`, `validate_ranks`.
- INPUT_TOO_LARGE preflight:
  - Added to `LLMReplyGeneratorService.generate()` between `_build_llm_input` and provider call.
  - Estimates total size (system prompt + serialized input dict).
  - Returns structured refusal with `INPUT_TOO_LARGE` code when exceeded.
  - Configurable via `max_input_chars` parameter (default 20,000).
- ReplyPlanner rank validation:
  - `_validate_plan()` now uses shared `check_ranks_contiguous()` instead of inline rank logic.
  - Uniqueness and contiguity are checked together with a single error message.
- Regression tests closing T181 deferred gaps:
  - **M01** (7 tests): `_build_llm_input` output-shape expectations 閳?minimal context, skill brief, memory facts, derived briefs, approved patches, empty contact id, event/memory counts.
  - **M02** (10 tests): `_parse_provider_response` error paths 閳?missing choices, empty choices, non-list choices, non-dict choice, missing message, non-dict message, empty content, invalid JSON, non-object JSON, valid response.
  - **M03** (2 tests): Generator-to-validator end-to-end synthetic pipeline 閳?mock provider 閳?parse 閳?build candidates 閳?construct plan 閳?validate; second test validates privacy leak filtering in the pipeline.
  - **M04** (2 tests): CLI stdout privacy regression 閳?dry-run and generate modes both assert `draft_text` and private text not in stdout.
- Shared validator test coverage (46 tests):
  - text non-empty (3), supporting refs (2), boundary reminders (2), ref types (5), privacy leak (8), impersonation (9), normalize ranks (5), check ranks contiguous (6), input size (4).
- LLMReplyPlanValidator now delegates 6 of 7 checks to the shared module, keeping only `generator_type` filtering as LLM-specific.
- The redundant second `validate_ranks` call in `generate()` (T181 N03) is now removed.
- Verification:
  - `python -m py_compile` passed for all modified files.
  - `pytest tests/test_reply_candidate_validator.py -q`: 46 passed.
  - `pytest tests/test_llm_reply_generator.py -q`: 47 passed.
  - `pytest tests/test_reply_planner.py -q`: existing tests pass unchanged.
  - `pytest tests/ -q`: **420 passed** (327 existing + 47 T181/T182 + 46 shared validator), zero regressions.
- Remaining risks:
  - Privacy-leak detection is improved but still deterministic (exact-match only). Paraphrased leaks remain undetected.
  - Input-size preflight uses character-count proxy, not token-count. May slightly over- or under-estimate actual provider token usage.
  - `ReplyCandidateValidator` impersonation patterns are module-level constants (not injectable). Extending requires modifying source.
  - No live provider smoke test was executed (same constraint as T181).

## 85. T183 Implementation Record

- Files added:
  - `tests/test_hybrid_reply_planner.py`
- Files modified:
  - `src/practical_chat_agent/services/reply_planner.py`
  - `src/practical_chat_agent/services/reply_candidate_validator.py` (T182 N01 fix)
  - `src/practical_chat_agent/services/llm_reply_generator.py` (T182 N01 fix)
  - `src/practical_chat_agent/app/main.py`
  - `tests/test_reply_candidate_validator.py` (T182 N01 test fix)
  - `docs/07_handoff.md` (this entry)
- Hybrid ReplyPlanner design:
  - `ReplyPlanner.__init__()` now accepts `llm_generator` (optional `LLMReplyGeneratorService`) and `hybrid_mode` (bool, default `False`).
  - `generate()` also accepts `force_template` (bool) to skip LLM even in hybrid mode.
  - When `hybrid_mode=True` and `llm_generator` is available:
    1. Template candidates are built as baseline (always).
    2. `_generate_llm_candidates()` calls `llm_generator.generate()` 閳?catches all exceptions, never raises.
    3. LLM candidates go through `_build_llm_candidate()` which applies `policy_engine.assess_candidate()` (same policy assessment as template candidates).
    4. `_merge_candidates()` merges deterministically: keep template candidate 1 as safety baseline, replace 2+ with up to 2 LLM candidates, pad to exactly 3 from remaining template candidates, renumber ranks to 1..3.
    5. If LLM generator is unavailable, refuses, or raises, hybrid mode falls back to clean template-only output (never crashes, never produces hybrid partial output).
    6. `_build_candidate_difference_notes()` updated to add LLM-specific notes when hybrid candidates are present.
  - The `force_template` parameter gives callers explicit control to bypass LLM even when hybrid mode is configured.
- T182 N01 INPUT_TOO_LARGE fix:
  - `check_input_size()` signature changed from `(serialized_json: str, ...)` to `(size: int, ...)` 閳?callers pass integer character count.
  - Call site in `LLMReplyGeneratorService.generate()` passes `estimated_size` (int) instead of `str(estimated_size)`.
  - Test values changed from string length checks to direct integer comparisons.
- CLI wiring:
  - `chat-reply-plan` now accepts `--hybrid` flag (default `False`).
  - When `--hybrid` is set, reads LLM provider settings via `get_settings()` and constructs an `LLMReplyGeneratorService`.
  - Template-only behavior is preserved when `--hybrid` is not set.
- Test coverage (18 tests in `test_hybrid_reply_planner.py`):
  - Backward compatibility: default planner has no LLM, produces valid 3-candidate plan.
  - Opt-in: hybrid_mode defaults to False; must be explicitly set.
  - LLM refusal fallback: when API key is unconfigured, hybrid mode returns template-only without crash.
  - LLM error fallback: when generator raises, hybrid mode returns template-only without crash.
  - `force_template` override: skips LLM even when hybrid mode is configured.
  - Policy assessment: all candidates carry risk_flags, boundary_reminders, confidence.
  - Output contract: always `candidate_review_only`, valid schema, review-ready candidates.
  - CLI: `--hybrid` flag accepted, produces valid ReplyPlan even when provider is unavailable.
- Verification:
  - `python -m py_compile` passed for all modified files.
  - `pytest tests/test_hybrid_reply_planner.py -q`: 18 passed.
  - `pytest tests/test_reply_planner.py -q`: existing tests pass unchanged.
  - `pytest tests/test_llm_reply_generator.py -q`: 47 passed.
  - `pytest tests/test_reply_candidate_validator.py -q`: 46 passed.
  - `pytest tests/ -q`: **438 passed** (420 existing + 18 new), zero regressions.
- Live provider smoke test:
  - Successfully executed with Deepseek (api.deepseek.com, model deepseek-chat).
  - Command: `chat-reply-plan --hybrid` with synthetic ChatContext.
  - Result: 3 candidates produced (1 template baseline + 2 LLM-generated).
    - Template candidate 1 (conservative_acknowledgment, 娑擃厽鏋? confidence 0.78).
    - LLM candidate 2 (enthusiastic follow-up, 閼昏鲸鏋? confidence 0.90).
    - LLM candidate 3 (casual support, 閼昏鲸鏋? confidence 0.85).
  - Merge rule verified: template[0] kept as safety baseline, LLM[0:2] replaced ranks 2 and 3.
  - Policy assessment applied: boundary_reminders carried through to LLM candidates.
  - Output written to `private/distilled/t183_smoke/hybrid_plan.json`.
  - Notable observation: LLM returned English drafts while template uses Chinese 閳?the prompt does not specify language preference.
- Remaining risks:
  - LLM candidate quality is not evaluated in T183 閳?T184 holdout eval remains the quality gate.
  - Merge rule (keep template[0], replace 2+) is deterministic but not validated against real LLM output diversity.
  - If LLM returns only 1 valid candidate, the merge pads with template candidates, which may produce a mixed-style output.

## 86. T184 Eval Record

### Goal

Evaluate template vs hybrid planner behavior on 6 anonymized holdout scenarios and record whether the hybrid path improves or regresses review-only quality without compromising safety.

### Eval Artifacts

All private outputs under `private/distilled/t184_holdout_eval/`:
- `contexts/*.context.json` 閳?6 synthetic anonymized ChatContext inputs
- `plans_template/*.plan.json` 閳?6 template-mode ReplyPlan outputs
- `plans_hybrid/*.plan.json` 閳?6 hybrid-mode ReplyPlan outputs
- `eval_analysis.json` 閳?structured comparison

### Eval Coverage

6 scenarios 鑴?2 modes = 12 ReplyPlans evaluated:

| Scenario | Type | Template diversity | Hybrid diversity | Baseline preserved |
|----------|------|-------------------|-----------------|--------------------|
| S1 new_job | warm baseline | 3 labels | 3 labels | Yes |
| S2 work | neutral task | 3 labels | 3 labels | Yes |
| S3 sensitive | boundary-heavy | 3 labels | 3 labels | Yes |
| S4 thin | no approved store | 3 labels | 3 labels | Yes |
| S5 memory | evidence-rich | 3 labels | 3 labels | Yes |
| S6 low_pressure | boundary-sensitive | 3 labels | 3 labels | Yes |

### Key Findings

- **Naturalness**: Hybrid +1 (4/5 vs 3/5). LLM candidates are consistently more natural and situation-appropriate.
- **Evidence usage**: Hybrid +0.5 (3.5/5 vs 3/5). S5 memory-rich scenario shows strong LLM evidence usage (references hiking trip directly); template stays generic.
- **Boundary adherence**: Hybrid -1 (3/5 vs 4/5). Policy flags are correctly applied but LLM draft text can contradict the flags (e.g., S4 thin_context LLM candidate asks engaging questions despite thin_context flag).
- **Mixed language**: Template candidates are Chinese; LLM candidates default to English. This creates a jarring UX when reviewing hybrid output.
- **LLM confidence inflation**: LLM candidates range 0.79-0.95 vs template 0.45-0.78. Not calibrated to actual quality variance.
- **Approach_label inconsistency**: Hybrid labels mix snake_case, title case, and sentence fragments.
- **Privacy safety**: 5/5 for both modes 閳?no leaks.
- **Merge stability**: 6/6 scenarios preserve template[0] as rank 1 baseline with contiguous ranks.

### Live Provider

All 6 hybrid scenarios used Deepseek (api.deepseek.com, deepseek-chat) via `chat-reply-plan --hybrid`.

### Gate M7 (Holdout Eval Stage) Verdict

**Conditional**

Conditions carried forward:
1. Language consistency 閳?LLM should generate in the same language as template (Chinese), or mixed-language output must be accepted as a design trade-off.
2. Safety constraint enforcement 閳?LLM draft text must respect thin_context and boundary_sensitive flags at the text level, not just at the policy-flag level.
3. Approach_label normalization 閳?hybrid labels should follow the same convention as template labels.
4. Merge success path regression coverage 閳?add a committed synthetic valid-candidate merge test.

### Remaining Risks

1. Mixed-language output is a real UX concern 閳?English LLM candidates alongside Chinese template candidates.
2. LLM safety constraint bypass 閳?draft text can contradict assigned risk flags.
3. LLM confidence is consistently high and uncalibrated, which may mislead human reviewers.
4. No committed regression test for hybrid valid-candidate merge path (carried from T183).
5. Approach_label naming inconsistency may affect downstream consumers (e.g., feedback clustering).

## 88. T185 Completion Record

### Goal

Fix the alignment gaps identified by T184 holdout evaluation: enforce LLM output language to match template language (Chinese), add explicit safety constraints for thin_context/boundary_sensitive scenarios, normalize approach_label naming, and add a committed regression test for the valid-candidate merge path.

### Files Changed

- `src/practical_chat_agent/services/llm_reply_generator.py`
- `tests/test_hybrid_reply_planner.py`

No changes to `reply_planner.py` or `app/main.py` were needed; all fixes are prompt/label/validation-level.

### Changes

1. **System prompt language enforcement**: Added rule 6 requiring all `draft_text` to be written in Chinese (娑擃厽鏋?. This aligns LLM output language with template output language, resolving the T184 mixed-language UX concern.

2. **Safety constraint enforcement**: Added rule 4 with explicit guidance for thin_context and boundary_sensitive scenarios. Also added automatic `safety_context` detection in `_build_llm_input()`: when `approved_store_context.status` is `not_configured` or `no_runtime_ready_records`, a `thin_context` flag is included; when `derived_brief_context.boundary.sensitivity_summary` contains `sensitive` or `high`, a `boundary_sensitive` flag is included. The system prompt instructs the LLM to obey these flags.

3. **Approach_label normalization**: Added `_normalize_label()` static method that converts arbitrary approach_label values to consistent `snake_case` (lowercase, non-alphanumeric characters replaced with underscores). Applied in `_build_candidates()` so all LLM approach labels follow the same convention as template labels.

4. **Merge success path regression test**: Added `TestHybridMergeSuccessPath` with 3 tests in `test_hybrid_reply_planner.py`. Uses `_MockSuccessGenerator` that returns pre-built valid LLM candidates without calling a real provider. Verifies: template[0] is preserved as safety baseline, LLM candidates replace template 2+, and final ranks are contiguous 1..3.

### Verification

- `python -m py_compile src/practical_chat_agent/services/llm_reply_generator.py src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/app/main.py` 閳?pass
- `pytest tests/test_hybrid_reply_planner.py -q` 閳?21 passed (3 new)
- `pytest tests/test_llm_reply_generator.py -q` 閳?47 passed
- `pytest tests/test_reply_candidate_validator.py -q` 閳?46 passed
- `pytest tests/ -q` 閳?441 passed (438 existing + 3 new), zero regressions

### Remaining Risks

1. **LLM behavior not fully deterministic**: The system prompt and safety context flags guide LLM behavior, but the LLM may still generate non-Chinese text or boundary-violating content in edge cases. The deterministic validator still catches impersonation and privacy leaks as a second line of defense.
2. **Safety context detection is heuristic**: The current detection uses `approved_store_context.status` and `boundary.sensitivity_summary` to infer thin/sensitive conditions. A more accurate approach would use the `ReplyPlanPolicyEngine` directly, which is outside the generator's scope.
3. **LLM confidence still uncalibrated**: This task did not address LLM confidence calibration; the uncalibrated 0.79-0.95 range noted in T184 remains.
4. **Label normalization may truncate some LLM labels**: Long or unusually formatted labels are collapsed to snake_case, which preserves consistency but may lose information.
5. **Template-only behavior unchanged**: Verified 閳?all 438 existing tests pass without modification.
## T210 Worker Completion Record

### Goal

Define the opening M10 behavior-planner contracts as schema-only, draft-only
artifacts before any planner execution, scheduler, outbound gate, platform
adapter, or send behavior exists.

### Files Changed

- `src/practical_chat_agent/core/models.py`
- `tests/test_behavior_schema.py`
- `docs/data_contracts/behavior_planner_contract.md`
- `docs/worker_summary/T210_worker_summary.md`
- `docs/07_handoff.md`

### Models Added

- `AgentSelfState`: compact review-safe assistant/user/contact state snapshot
  with identifiers, safe context refs, signal refs, and risk flags only.
- `BehaviorPolicy`: draft-only policy envelope with hard schema invariants:
  human review required, auto-send disallowed, platform execution disallowed,
  and scheduler use disallowed.
- `CandidateActionPayload`: non-executable payload with required
  `safe_summary`, optional `draft_text`, review notes, and metadata that rejects
  transport, scheduling, credential, and raw-transcript keys.
- `CandidateAction`: review-only proactive behavior candidate with stable id,
  contact/user scope, action type, rationale, supporting context refs, risk
  flags, review metadata, and hard no-send/no-platform/no-scheduler invariants.

### Contract Boundaries

- Allowed action types are limited to draft/review categories:
  `relationship_check_in_draft`, `reply_follow_up_draft`, `topic_suggestion`,
  `boundary_review_note`, `memory_review_prompt`, and `do_nothing`.
- `CandidateAction.is_runtime_visible()` requires approved human-review
  metadata, but runtime visibility remains non-executable.
- `platform_target` is always `null`; setting a platform target is rejected by
  schema validation.
- No raw transcript, private chat-history, platform transport, scheduling, or
  credential field is required or allowed in committed behavior payloads.

### Explicit Non-Actions

- No message sending.
- No real scheduler, background job, timer, reminder, or automation.
- No Feishu, WeChat, browser, desktop, notification, email, or other platform
  integration.
- No BehaviorPlanner execution logic, rule engine, ranking engine, or CLI.
- No mutation of `MemoryFact`, `ContactSkill`, relationship state, approved
  patches, stores, or private artifacts.
- No private chat-history reads or committed private content.
- No LLM calls, provider configuration, embeddings, vector DBs, Mem0/Zep
  production use, or fine-tuning.

### Verification

Commands were run with `TEMP` and `TMP` set to `.tmp/pytest`, and pytest cache
set to `.tmp/pytest_cache` to avoid the Windows default temp/cache permission
warnings observed in this sandbox.

- `python -m py_compile src/practical_chat_agent/core/models.py`: passed.
- `pytest tests/test_behavior_schema.py -q -o cache_dir=.tmp\pytest_cache`: 25 passed.
- `pytest tests/ -q -o cache_dir=.tmp\pytest_cache`: 747 passed.

### Remaining Risks

- T210 is schema-only. It does not define planner rules, candidate ranking,
  review CLI behavior, or outbound send-gate integration.
- The metadata forbidden-key guard currently applies to
  `CandidateActionPayload.metadata`; future payload fields must preserve the
  same no-platform/no-scheduler/no-raw boundary.
- Runtime visibility is intentionally separate from execution. Later tasks must
  not treat `approved` candidate actions as sendable or schedulable without an
  explicit OutboundSendGate task and review.

## T211 Worker Completion Record

### Goal

Add a deterministic, local rule engine that proposes review-only
`CandidateAction` artifacts from T210 behavior contracts without sending,
scheduling, platform integration, LLM calls, runtime wiring, or state mutation.

### Files Changed

- `src/practical_chat_agent/services/behavior_planner.py`
- `tests/test_behavior_rule_planner.py`
- `docs/data_contracts/behavior_planner_contract.md`
- `docs/worker_summary/T211_worker_summary.md`
- `docs/07_handoff.md`

### Service Added

- `BehaviorRulePlanner` in `src/practical_chat_agent/services/behavior_planner.py`
- Public method:
  - `plan(self_state, policy=None, safe_context_labels=None) -> list[CandidateAction]`

### Rule Behavior

- Deterministic rule order:
  1. `boundary_review_note`
  2. `memory_review_prompt`
  3. `relationship_check_in_draft`
  4. `do_nothing` fallback
- `boundary_review_note` fires for boundary-sensitive risk flags or safe labels.
- `memory_review_prompt` fires for recent safe signal refs or memory/relationship
  review labels.
- `relationship_check_in_draft` requires at least one approved context ref and
  no hard proactive-blocking risk flag.
- `do_nothing` is the fallback for empty/thin/blocked context when policy allows
  it.
- If no rule is allowed and `do_nothing` is disallowed, the result is an empty
  list.
- Candidate ids are stable hashes over safe identifiers and supporting refs.
- `BehaviorPolicy.allowed_action_types` is enforced before emission.
- `BehaviorPolicy.max_candidates` is enforced after rule filtering.

### Safety Boundaries

Every emitted `CandidateAction` preserves T210 invariants:

- `human_review_required=True`
- `auto_send_allowed=False`
- `platform_execution_allowed=False`
- `scheduler_allowed=False`
- `platform_target=None`
- `status="candidate"`
- at least one `supporting_context_ref`
- no forbidden payload metadata keys

The public planner API accepts compact safe labels only; it does not expose raw
transcript, message text, chat history, or private-message parameters.

### Explicit Non-Actions

- No message sending.
- No real scheduler, timer, reminder, background job, automation, or recurring task.
- No Feishu, WeChat, browser, desktop, notification, email, webhook, or platform adapter.
- No CLI commands, app-container wiring, runtime loops, or automatic execution hooks.
- No LLM calls, provider APIs, embeddings, vector DBs, Mem0/Zep, or external services.
- No final user-facing message draft generation; T212 owns that later layer.
- No mutation of `MemoryFact`, `ContactSkill`, `RelationshipState`,
  `PreferencePatchCandidate`, approved stores, private artifacts, or review metadata.
- No private chat-history reads or committed private content.

### Verification

Commands were run with `TEMP` and `TMP` set to `artifacts/pytest_tmp`, pytest
cache set to `artifacts/pytest_cache`, and full-suite `--basetemp` set to
`artifacts/pytest_basetemp`. An earlier full-suite attempt using `.tmp/pytest`
failed in fixture setup with Windows permission errors while enumerating the
pytest temp root; the `artifacts/pytest_*` rerun passed.

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py`: passed.
- `pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py -q -o cache_dir=artifacts\pytest_cache`: 40 passed.
- `pytest tests/ -q --basetemp=artifacts\pytest_basetemp -o cache_dir=artifacts\pytest_cache`: 762 passed.

### Remaining Risks

- T211 uses fixed conservative rule ordering only; no ranking or quality scoring
  exists yet.
- `safe_context_labels` are caller-supplied compact labels. The API avoids raw
  text parameters, but callers must still keep labels review-safe.
- `relationship_check_in_draft` produces a review-safe action summary only, not
  final user-facing wording. T212 remains responsible for draft generation.

## T220 Worker Completion Record

- T220 is the OutboundMessageRequest schema task for M11.
- Worker must not mark T220 as complete in `docs/04_task_board.md`; only the
  Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `tests/test_outbound_message_request_schema.py`
  - `docs/data_contracts/outbound_send_gate_contract.md`
  - `docs/worker_summary/T220_worker_summary.md`
  - `docs/07_handoff.md`
- Test-first evidence:
  - `tests/test_outbound_message_request_schema.py` was written before the new
    schema existed.
  - The first targeted pytest run failed during import because
    `OutboundMessagePayload` / `OutboundMessageRequest` were missing.
  - The schema and validators were then added minimally until the targeted test
    suite passed.
- Schema behavior added:
  - `OutboundMessagePayload` carries draft-only outbound text plus review-safe
    metadata and rejects scheduler, adapter, credential, transport, and
    raw/private-content keys.
  - `OutboundRequestHumanApproval` stores explicit outbound-request review state
    that is separate from `CandidateAction` review metadata.
  - `OutboundRequestSendGate` stores explicit gate-evaluation state that
    defaults to `not_evaluated`.
  - `OutboundMessageRequest` separates outbound draft intent from M10 behavior
    evidence through `source_type`, optional `source_candidate_action_id`, and
    optional `source_context_refs`.
  - `OutboundMessageRequest.is_sendable()` requires both explicit outbound human
    approval and an explicit gate state of `allowed`.
  - Reviewed or runtime-visible `CandidateAction` artifacts remain evidence
    only; they are not implicit send authorization.
- Verification status:
  - Commands were run with `TEMP` and `TMP` set to
    `artifacts\t220_pytest_tmp`, pytest cache set to
    `artifacts\t220_pytest_cache`, and `--basetemp` set to
    `artifacts\t220_pytest_basetemp` to keep pytest temp/cache inside the
    workspace-local sandbox path.
  - `python -m py_compile src/practical_chat_agent/core/models.py`: passed.
  - `pytest tests/test_outbound_message_request_schema.py -q -o cache_dir=artifacts\t220_pytest_cache --basetemp=artifacts\t220_pytest_basetemp`: passed, 11 tests.
  - `pytest tests/test_behavior_schema.py tests/test_outbound_message_request_schema.py -q -o cache_dir=artifacts\t220_pytest_cache --basetemp=artifacts\t220_pytest_basetemp`: passed, 36 tests.
  - `pytest tests -q -o cache_dir=artifacts\t220_pytest_cache --basetemp=artifacts\t220_pytest_basetemp`: passed, 791 tests.
- Explicit non-actions:
  - No message sending.
  - No scheduler, timer, reminder, background job, automation, or runtime loop.
  - No fake adapter, Feishu adapter, WeChat adapter, review card, or platform integration.
  - No CLI execution path or app-container wiring.
  - No LLM/provider calls, web services, vector DB, Mem0/Zep, or external systems.
  - No mutation of `CandidateAction`, memory records, ContactSkill,
    `RelationshipState`, approved stores, or private artifacts.
  - No `private/chat_history/` reads and no committed private content.
  - No task-board update.
- Remaining risks:
  - T220 defines the contract boundary only; T221 still needs to implement gate
    policy such as quiet hours, frequency limits, duplicate suppression, kill
    switch behavior, and audit decisions.
  - `source_context_refs` stay caller-supplied review-safe refs in T220; no
    store-backed evidence validation is performed here.
  - `channel_preference` is intentionally data-only and not a real adapter
    target; later platform tasks must keep that separation explicit.

## T221 Worker Completion Record

- T221 is the OutboundSendGate task for M11.
- Worker must not mark T221 as complete in `docs/04_task_board.md`; only the
  Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/services/outbound_send_gate.py`
  - `tests/test_outbound_send_gate.py`
  - `tests/test_outbound_message_request_schema.py`
  - `docs/data_contracts/outbound_send_gate_contract.md`
  - `docs/worker_summary/T221_worker_summary.md`
  - `docs/07_handoff.md`
- Test-first evidence:
  - `tests/test_outbound_send_gate.py` and the extra T220 coverage additions in
    `tests/test_outbound_message_request_schema.py` were written before the new
    service existed.
  - The first targeted pytest run failed during import because
    `practical_chat_agent.services.outbound_send_gate` did not exist.
  - The gate service and minimal supporting logic were then added until the
    targeted tests passed.
- Gate behavior added:
  - `OutboundSendGate.evaluate()` accepts a validated
    `OutboundMessageRequest` or a stable mapping.
  - Evaluation is pure and returns a new audited request copy inside
    `OutboundSendGateDecision`.
  - The service sets `send_gate.gate_state` to `allowed` only when all checks
    pass, and to `blocked` when any check fails.
  - Evaluated gate state always records `evaluator_id`, `evaluated_at`, and
    deterministic `gate_notes`.
  - Reviewed `CandidateAction` artifacts remain evidence only and are not send
    authorization.
- Policy rules implemented:
  - manual-only outbound approval
  - kill switch
  - quiet hours, including overnight windows
  - frequency limit using supplied synthetic/local request history
  - duplicate suppression using normalized draft text
  - self-echo prevention from supplied latest/reference text
  - defensive whitespace-only payload blocking
- Verification status:
  - Commands were run with `TEMP` and `TMP` set to
    `artifacts\t221_pytest_tmp`, pytest cache set to
    `artifacts\t221_pytest_cache`, and `--basetemp` set to
    `artifacts\t221_pytest_basetemp` to keep pytest temp/cache inside the
    workspace-local sandbox path.
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py`: passed.
  - `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q -o cache_dir=artifacts\t221_pytest_cache --basetemp=artifacts\t221_pytest_basetemp`: passed, 31 tests.
  - `pytest tests/test_behavior_schema.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q -o cache_dir=artifacts\t221_pytest_cache --basetemp=artifacts\t221_pytest_basetemp`: passed, 56 tests.
  - `pytest tests -q -o cache_dir=artifacts\t221_pytest_cache --basetemp=artifacts\t221_pytest_basetemp`: passed, 811 tests.
- Explicit non-actions:
  - No message sending.
  - No scheduler, timer, reminder, background job, automation, or runtime loop.
  - No fake adapter, Feishu adapter, WeChat adapter, review card, or platform integration.
  - No CLI send command, app-container wiring, or delivery execution path.
  - No LLM/provider calls, web services, vector DB, Mem0/Zep, or external systems.
  - No mutation of `CandidateAction`, memory records, ContactSkill,
    `RelationshipState`, approved stores, or private artifacts.
  - No `private/chat_history/` reads and no committed private content.
  - No task-board update.
- Remaining risks:
  - T221 is gate-only and records policy state, not delivery state; T222+ must
    keep `allowed` separate from `delivered`.
  - Frequency and duplicate checks currently treat prior gate-`allowed`
    requests as send-equivalent synthetic history because no delivery layer is
    in scope yet.
  - `manual_only_mode` remains intentionally fixed to the current conservative
    mainline and does not create any autonomous send path.

## T222 Worker Completion Record

- T222 is the local fake outbound adapter task for M11.
- Worker must not mark T222 as complete in `docs/04_task_board.md`; only the
  Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/services/outbound_fake_adapter.py`
  - `tests/test_outbound_fake_adapter.py`
  - `tests/test_outbound_send_gate.py`
  - `docs/data_contracts/outbound_send_gate_contract.md`
  - `docs/worker_summary/T222_worker_summary.md`
  - `docs/07_handoff.md`
- Test-first evidence:
  - `tests/test_outbound_fake_adapter.py` and the extra T221 clear-path /
    multi-blocking coverage in `tests/test_outbound_send_gate.py` were written
    before the adapter existed.
  - The first targeted pytest run failed during import because
    `practical_chat_agent.services.outbound_fake_adapter` did not exist.
  - The local fake adapter was then added minimally until the targeted tests
    passed.
- Fake adapter behavior added:
  - `LocalFakeOutboundAdapter.deliver()` accepts a validated
    `OutboundMessageRequest` or a stable mapping that validates to one.
  - Direct `CandidateAction` instances and mappings are rejected with
    `blocked_invalid_request`.
  - Requests where `is_sendable()` is false are rejected locally with
    `blocked_not_sendable`.
  - Sendable requests produce deterministic in-memory
    `FakeOutboundDeliveryResult` records with `fake_delivered`.
  - Result metadata records `request_id`, `contact_id`, `user_id`,
    `channel_preference`, adapter name, fake delivery timestamp, truncated
    payload preview, and safe audit notes.
  - The adapter does not mutate the input request and does not write to disk or
    contact any external platform.
- Additional T221 coverage added:
  - quiet-hours clear path
  - frequency-limit clear path
  - duplicate-suppression clear path
  - self-echo clear path
  - combined blocking reasons preserved for pending approval plus kill switch
  - fake-adapter blocking for missing explicit human approval
- Timezone portability decision:
  - T222 did not add `tzdata` to `pyproject.toml`.
  - New T222 test coverage was kept on UTC-based paths, and the earlier Windows
    named-timezone portability risk remains open as R097.
- Verification status:
  - Commands were run with `TEMP` and `TMP` set to
    `artifacts\t222_pytest_tmp`, pytest cache set to
    `artifacts\t222_pytest_cache`, and `--basetemp` set to
    `artifacts\t222_pytest_basetemp` to keep pytest temp/cache inside the
    workspace-local sandbox path.
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py`: passed.
  - `pytest tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py -q -o cache_dir=artifacts\t222_pytest_cache --basetemp=artifacts\t222_pytest_basetemp`: passed, 24 tests.
  - `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py -q -o cache_dir=artifacts\t222_pytest_cache --basetemp=artifacts\t222_pytest_basetemp`: passed, 43 tests.
  - `pytest tests/ -q -o cache_dir=artifacts\t222_pytest_cache --basetemp=artifacts\t222_pytest_basetemp`: passed, 823 tests.
- Explicit non-actions:
  - No real message sending.
  - No Feishu, WeChat, webhook, email, browser, desktop, or notification API
    calls.
  - No scheduler, timer, reminder, background job, automation, or runtime loop.
  - No CLI send path, app-container wiring, or delivery execution hook.
  - No LLM/provider calls, web services, vector DB, Mem0/Zep, or external systems.
  - No mutation of `CandidateAction`, memory records, ContactSkill,
    `RelationshipState`, approved stores, or private artifacts.
  - No `private/chat_history/` reads and no committed private content.
  - No task-board update.
- Remaining risks:
  - T222 proves only a local synthetic adapter boundary; there is still no real
    platform delivery, acknowledgement, or retry model.
  - `FakeOutboundDeliveryResult` stores a truncated preview only; any future
    adapter task must keep the same review-safe boundary and avoid raw
    transcript leakage.
  - The Windows named-timezone portability risk from T221 remains open because
    T222 intentionally did not add `tzdata`.

## T223 Worker Completion Record

- T223 is the Feishu sandbox outbound adapter task for M11.
- Worker must not mark T223 as complete in `docs/04_task_board.md`; only the
  Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/services/feishu_outbound_adapter.py`
  - `src/practical_chat_agent/core/models.py`
  - `tests/test_feishu_outbound_adapter.py`
  - `tests/test_outbound_fake_adapter.py`
  - `docs/data_contracts/outbound_send_gate_contract.md`
  - `docs/worker_summary/T223_worker_summary.md`
  - `docs/07_handoff.md`
- Test-first evidence:
  - `tests/test_feishu_outbound_adapter.py` and the T222 hardening additions in
    `tests/test_outbound_fake_adapter.py` were written before the Feishu
    adapter existed.
  - The first targeted pytest run failed during import because
    `practical_chat_agent.services.feishu_outbound_adapter` did not exist.
  - The sandbox adapter and minimal supporting metadata guardrails were then
    added until the targeted tests passed.
- Feishu sandbox behavior added:
  - `FeishuSandboxOutboundAdapter.deliver()` accepts a validated
    `OutboundMessageRequest` or a stable mapping that validates to one.
  - Direct `CandidateAction` instances and candidate-shaped mappings are
    rejected with `blocked_invalid_request`.
  - Non-sendable requests are blocked with `blocked_not_sendable`.
  - `channel_preference` must be explicitly `feishu`; `unspecified` and
    `wechat` are blocked with `blocked_wrong_channel`.
  - Recipient resolution uses explicit adapter config keyed by `contact_id`,
    outside `OutboundMessagePayload.metadata`.
  - The adapter builds a Feishu-compatible text payload from
    `request.payload.draft_text` only.
  - Dry-run is the default and returns `feishu_dry_run_ready` without invoking
    any transport.
  - When dry-run is explicitly disabled, an injected fake/sandbox transport may
    return `feishu_sandbox_sent`; transport failures return
    `blocked_transport_error`.
  - Result metadata records adapter name, request scope, recipient metadata,
    prepared payload, provider sandbox message id when present, aware-UTC
    `result_at`, and audit notes that preserve caller-provided audit entries.
  - Production Feishu delivery is still unclaimed.
- Additional hardening added:
  - outbound payload metadata now rejects Feishu recipient-smuggling keys such
    as `open_id`, `chat_id`, `receive_id`, `receive_id_type`,
    `feishu_open_id`, and `feishu_chat_id`
  - `FakeOutboundAdapterConfig` validation tests for empty adapter name and
    non-positive preview limit
  - fake adapter `existing_audit` preservation test
  - fake adapter preview exact-boundary and `preview_char_limit <= 3` tests
- Verification status:
  - Commands were run with `TEMP` and `TMP` set to
    `artifacts\t223_pytest_tmp`, pytest cache set to
    `artifacts\t223_pytest_cache`, and `--basetemp` set to
    `artifacts\t223_pytest_basetemp` to keep pytest temp/cache inside the
    workspace-local sandbox path.
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py src/practical_chat_agent/services/feishu_outbound_adapter.py`: passed.
  - `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py tests/test_feishu_outbound_adapter.py -q -o cache_dir=artifacts\t223_pytest_cache --basetemp=artifacts\t223_pytest_basetemp`: passed, 65 tests.
  - `pytest tests/ -q -o cache_dir=artifacts\t223_pytest_cache --basetemp=artifacts\t223_pytest_basetemp`: passed, 845 tests.
- Explicit non-actions:
  - No production Feishu sending.
  - No real Feishu, webhook, email, browser, desktop, notification, WeChat, or
    other external API calls in committed code/tests.
  - No production credentials, webhook registration, event callbacks, bot
    installation flow, or environment-secret reads.
  - No CLI send path, AppContainer wiring, scheduler, timer, background job,
    automation, or runtime delivery hook.
  - No mutation of `OutboundMessageRequest`, `CandidateAction`, memory records,
    ContactSkill, `RelationshipState`, approved stores, or private artifacts.
  - No `private/chat_history/` reads and no committed private content.
  - No task-board update.
- Remaining risks:
  - T223 proves only Feishu sandbox payload preparation and injected fake
    transport behavior; it does not prove production Feishu API compatibility,
    acknowledgement semantics, retries, or delivery recovery.
  - Recipient mapping is currently a simple explicit `contact_id` lookup in
    adapter config; future production work will need reviewed mapping ownership
    and operational secret handling outside this task.
  - The Windows named-timezone portability risk from T221 remains open because
    T223 did not introduce `tzdata`.

## T224 Worker Completion Record

- T224 is the Feishu review-card task for M11.
- Worker must not mark T224 as complete in `docs/04_task_board.md`; only the
  Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/services/feishu_review_card.py`
  - `tests/test_feishu_review_card.py`
  - `docs/data_contracts/outbound_send_gate_contract.md`
  - `docs/worker_summary/T224_worker_summary.md`
  - `docs/07_handoff.md`
- Test-first evidence:
  - `tests/test_feishu_review_card.py` was written before the new service
    existed.
  - The first targeted pytest run failed during import because
    `practical_chat_agent.services.feishu_review_card` did not exist.
  - The review-card builder/parser was then added minimally until the targeted
    tests passed.
- Review-card behavior added:
  - `FeishuReviewCardBuilder.render()` accepts a validated
    `OutboundMessageRequest` or stable mapping and renders a deterministic local
    Feishu-compatible interactive-card payload.
  - The builder rejects direct `CandidateAction` instances and candidate-shaped
    mappings with `blocked_invalid_request`.
  - Valid requests render whether sendable or not; the card presents approval
    state, gate state, sendability, risk flags, audit notes, draft preview, and
    optional T223 sandbox summary without implying delivery or approval.
  - Button action values encode inert review-intent payloads with
    `schema_version`, `request_id`, and `action` for `approve`,
    `request_edit`, `reject`, and `boundary_feedback`.
  - `FeishuReviewIntentParser.parse()` converts synthetic card-action mappings
    into validated inert review-intent data and deterministically rejects
    malformed, missing, unknown, and cross-request payloads.
  - No approval, edit, reject, or boundary-feedback action is applied in T224.
- Verification status:
  - Commands were run with `TEMP` and `TMP` set to
    `artifacts\t224_pytest_tmp`, pytest cache set to
    `artifacts\t224_pytest_cache`, and `--basetemp` set to
    `artifacts\t224_pytest_basetemp` to keep pytest temp/cache inside the
    workspace-local sandbox path.
  - `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py src/practical_chat_agent/services/feishu_outbound_adapter.py src/practical_chat_agent/services/feishu_review_card.py`: passed.
  - `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py tests/test_feishu_outbound_adapter.py tests/test_feishu_review_card.py -q -o cache_dir=artifacts\t224_pytest_cache --basetemp=artifacts\t224_pytest_basetemp`: passed, 84 tests.
  - `pytest tests/ -q -o cache_dir=artifacts\t224_pytest_cache --basetemp=artifacts\t224_pytest_basetemp`: passed, 864 tests.
- Explicit non-actions:
  - No real Feishu API calls.
  - No Feishu webhook/event callback server.
  - No OAuth, bot installation, tenant token, secret, or environment-variable handling.
  - No production Feishu delivery.
  - No CLI send path, AppContainer wiring, scheduler, timer, background job,
    automation, retry loop, or runtime hook.
  - No approval application, feedback-log write, memory write, or store
    mutation.
  - No `private/chat_history/` reads and no committed private content.
  - No task-board update.
- Remaining risks:
  - T224 proves only local review-card rendering and inert intent parsing; it
    does not prove callback payload compatibility against real Feishu event
    traffic.
  - Card draft preview truncation is display-only and must not be reused as a
    privacy boundary in later delivery or logging work.
  - The Windows named-timezone portability risk from T221 remains open because
    T224 did not introduce `tzdata`.

## T230 Worker Completion Record

- T230 is the WeChat adapter research spike task for M12.
- Worker must not mark T230 as complete in `docs/04_task_board.md`; only the
  Captain may do so after review.
- Files changed:
  - `docs/review/T230_wechat_adapter_research.md`
  - `docs/worker_summary/T230_worker_summary.md`
  - `docs/07_handoff.md`
- Research decision:
  - Recommended `Gate M12 Conditional`.
  - Personal WeChat automation, scan-login resurrection, realtime
    personal-account send/receive, desktop automation, and unofficial SDK
    vendoring remain blocked.
  - Official WeChat-family business surfaces are possible only as narrow,
    reviewed, synthetic-first adapter paths, not as a generic WeChat adapter.
- Official surfaces reviewed:
  - WeCom internal app messages and callbacks.
  - WeCom WeChat Customer Service send/receive/event surfaces.
  - Official Account customer-service messages and message callbacks.
  - Mini Program customer-service messages.
  - Manual-copy and Feishu/manual handoff alternatives.
- Recommended next-task disposition:
  - T231 should be rewritten as a synthetic inbound contract spike for exactly
    one official surface, with no live callback server, no API calls, no
    credentials, no polling, no private chat reads, and no store mutation.
  - T232 live outbound should remain blocked until T231 selects an official
    surface and a reviewed recipient mapping / tenant prerequisite model exists.
  - T233 should be rewritten as provider-constraint safety design, not delivery.
- Explicit non-actions:
  - No code implementation.
  - No package install, SDK clone, SDK vendoring, third-party code copy, login,
    QR scan, session validation, API call, callback registration, sending,
    receiving, polling, desktop automation, browser automation, or runtime loop.
  - No real credentials, tokens, cookies, tenant IDs, app IDs, OpenIDs, chat IDs,
    QR codes, or private recipients used.
  - No `private/chat_history/` reads and no committed private content.
  - No task-board update.
- Verification status:
  - External official documentation was consulted on 2026-05-28 and cited in
    `docs/review/T230_wechat_adapter_research.md`.
  - `git diff --check`: passed. Git reported line-ending conversion warnings
    for existing dirty files, but no whitespace errors.
  - `git diff --check -- docs\review\T230_wechat_adapter_research.md docs\worker_summary\T230_worker_summary.md docs\07_handoff.md`:
    passed. Git reported the same line-ending conversion warning for
    `docs/07_handoff.md`.
  - `git status --short`: ran successfully and showed pre-existing unrelated
    dirty workspace files plus the T230 allowed-file changes.
- Remaining risks:
  - No live account, tenant, app, credential flow, callback URL, recipient
    mapping, delivery callback, or provider failure handling was tested.
  - Official docs may change and must be rechecked before any future
    implementation task.
  - Official business/customer-service surfaces do not cleanly map to personal
    WeFlow chat contacts.

## T231 Worker Completion Record

- T231 is the WeCom Customer Service inbound contract spike for M12.
- Worker must not mark T231 as complete in `docs/04_task_board.md`; only the
  Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/connectors/inbound/wecom_customer_service.py`
  - `src/practical_chat_agent/connectors/inbound/__init__.py`
  - `tests/test_wecom_customer_service_inbound.py`
  - `tests/fixtures/wecom_customer_service_inbound/inbound_text_message.json`
  - `tests/fixtures/wecom_customer_service_inbound/non_text_message.json`
  - `tests/fixtures/wecom_customer_service_inbound/send_failure_event.json`
  - `tests/fixtures/wecom_customer_service_inbound/malformed_missing_identity.json`
  - `tests/fixtures/wecom_customer_service_inbound/personal_wechat_desktop_like.json`
  - `docs/data_contracts/wecom_customer_service_inbound_contract.md`
  - `docs/worker_summary/T231_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: `pytest tests/test_wecom_customer_service_inbound.py -q` failed during
    collection because `practical_chat_agent.connectors.inbound.wecom_customer_service`
    did not exist.
  - GREEN: the targeted T231 pytest command passed with 6 tests after adding
    the connector.
- Inbound contract behavior added:
  - `WeComCustomerServiceInboundConnector.connector_name` is
    `wecom_customer_service`.
  - The connector accepts synthetic wrapper payloads and documented-like WeCom
    Customer Service `msg_list` / `event` shapes.
  - Text customer messages normalize to `InboundEvent` with
    `platform=wechat`, `source_type=chat_message`, `direction=inbound`,
    `channel_type=dm`, `content_type=text`, deterministic event IDs,
    customer-service-scoped channel/account IDs, synthetic external-user alias
    actor IDs, and synthetic raw contract metadata.
  - Unsupported non-text messages normalize conservatively as
    `ContentType.SYSTEM` without media fetching.
  - Provider send-failure events normalize as inbound `SYSTEM_EVENT` evidence
    without mutating outbound state.
  - Malformed WeCom-shaped payloads are rejected deterministically.
  - Personal-WeChat/desktop-like payloads are not accepted.
- Official docs:
  - Rechecked official WeCom Customer Service receive/send docs on 2026-05-28:
    `https://developer.work.weixin.qq.com/document/path/94670` and
    `https://developer.work.weixin.qq.com/document/path/94677`.
- Explicit non-actions:
  - No live callback route, webhook server, polling/sync loop, scheduler,
    background job, runtime ingestion hook, or `AppContainer` wiring.
  - No platform API call, package install, SDK clone, SDK vendoring, or
    unofficial SDK snippet.
  - No real credentials, tokens, callback secrets, tenant IDs, app IDs, OpenIDs,
    external user IDs, `open_kfid`, chat IDs, cookies, QR codes, or private
    recipients.
  - No encryption/decryption, real signature verification, OAuth, credential
    loading, environment-variable handling, tenant setup, or IP allowlist.
  - No outbound payload preparation, sending, retry, delivery interpretation,
    memory write, ContactSkill mutation, RelationshipState mutation, feedback
    write, approved-store mutation, or outbound request/gate mutation.
  - No `private/chat_history/`, `private/distilled/`, or private artifact reads.
  - No task-board update.
- Verification status:
  - `python -m py_compile src/practical_chat_agent/connectors/inbound/wecom_customer_service.py src/practical_chat_agent/connectors/inbound/__init__.py`:
    passed.
  - `pytest tests/test_wecom_customer_service_inbound.py -q -o cache_dir=artifacts\t231_pytest_cache --basetemp=artifacts\t231_pytest_basetemp`:
    passed, 6 tests.
  - `git diff --check`: passed with line-ending conversion warnings only for
    `docs/07_handoff.md` and
    `src/practical_chat_agent/connectors/inbound/__init__.py`.
  - `git status --short`: ran successfully and showed only T231 allowed-file
    changes in this worker state.
- Remaining risks:
  - T231 proves only synthetic local normalization, not live WeCom callback or
    sync compatibility.
  - Official docs may drift before live work.
  - Parser batching remains undefined because the current inbound abstraction
    returns one event per parse.
  - Synthetic WeCom customer aliases are not repo contact mappings.
  - Credential flow, callback verification, encryption/decryption,
    service-window tracking, quota enforcement, recipient mapping, and
    failure-event outbound-state handling remain unresolved.

## T233 Worker Completion Record

- T233 is the WeCom Customer Service provider safety gate task for M12.
- Worker must not mark T233 as complete in `docs/04_task_board.md`; only the
  Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/services/wecom_customer_service_safety.py`
  - `tests/test_wecom_customer_service_safety_gate.py`
  - `docs/data_contracts/wecom_customer_service_safety_contract.md`
  - `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md`
  - `docs/worker_summary/T233_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: `pytest tests/test_wecom_customer_service_safety_gate.py -q` failed
    during collection because
    `practical_chat_agent.services.wecom_customer_service_safety` did not
    exist.
  - GREEN: the targeted T233 pytest command passed with 25 tests after adding
    the safety gate.
- Safety-gate behavior added:
  - `WeComCustomerServiceSafetyGate.evaluate()` accepts a validated
    `OutboundMessageRequest` or stable mapping that validates to one.
  - Non-sendable requests are blocked before provider checks.
  - Sendable requests must use `channel_preference="wechat"` and explicit
    `surface="wecom_customer_service"` config.
  - Recipient resolution uses explicit local alias mapping keyed by
    `contact_id`, outside `OutboundMessagePayload.metadata`.
  - Provider kill switch, manual-send disallow, missing/expired service window,
    and 5-message window limit all produce deterministic blocked decisions.
  - Provider identity, recipient, and credential metadata-smuggling keys are
    blocked.
  - Allowed decisions preserve caller audit notes, return aliases only, and
    record `provider_eligible_not_delivery` plus
    `provider_payload_not_prepared`.
  - The input `OutboundMessageRequest` is not mutated.
- T232 disposition:
  - Captain has now accepted T233 with `PASS` and rewritten T232.
  - T232 may now be assigned only as dry-run WeCom Customer Service payload
    preparation behind a matching allowed T233 safety decision, synthetic
    fixtures, explicit recipient aliases, and no live delivery.
- Verification status:
  - `python -m py_compile src/practical_chat_agent/services/wecom_customer_service_safety.py`:
    passed.
  - `pytest tests/test_wecom_customer_service_safety_gate.py -q`: passed,
    25 tests, with pytest cache-provider warnings because `.pytest_cache` was
    not writable in this environment.
  - `pytest tests/test_wecom_customer_service_safety_gate.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q`:
    passed, 61 tests, with the same pytest cache-provider warnings.
  - `git diff --check`: passed after final docs update, with line-ending
    conversion warnings for `docs/07_handoff.md` and
    `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md`.
  - `git status --short`: ran after final docs update and showed only the six
    T233 allowed-file changes. Git also reported global ignore permission
    warnings in this environment.
- Explicit non-actions:
  - No WeCom outbound adapter, API payload preparation, live API call,
    credential read, callback/webhook route, polling/sync loop, scheduler,
    background job, runtime wiring, CLI send path, retry loop, or delivery path.
  - No outbound request, memory, ContactSkill, RelationshipState, feedback-log,
    approved-store, inbound-store, or private-artifact mutation.
  - No `private/chat_history/`, `private/distilled/`, or private artifact reads.
  - No task-board update.
  - No production WeCom compatibility or live-delivery readiness claim.
- Remaining risks:
  - T233 proves only local deterministic provider eligibility, not live WeCom
    Customer Service API compatibility.
  - Official Tencent/WeCom docs were not refetched in T233 and may drift before
    live work.
  - Recipient aliases, service-window expiry, and sent-message counts are
    supplied local context, not live provider state.
  - Credential handling, tenant eligibility, callback verification,
    encryption/decryption, provider failure events, acknowledgement semantics,
    retries, and production recipient mapping remain unresolved.
  - `channel_preference="wechat"` is still broad and only narrows to WeCom
    Customer Service through explicit T233 safety config.

## T232 Worker Completion Record

- T232 is the WeCom Customer Service dry-run outbound adapter task for M12.
- Worker must not mark T232 as complete in `docs/04_task_board.md`; only the
  Captain may do so after review.
- Files changed:
  - `src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py`
  - `tests/test_wecom_customer_service_outbound_adapter.py`
  - `docs/data_contracts/wecom_customer_service_outbound_contract.md`
  - `docs/worker_summary/T232_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: `pytest tests/test_wecom_customer_service_outbound_adapter.py -q`
    failed during collection because
    `practical_chat_agent.services.wecom_customer_service_outbound_adapter`
    did not exist.
  - GREEN: the targeted T232 pytest command passed with 23 tests after adding
    the dry-run adapter.
- Dry-run adapter behavior added:
  - `WeComCustomerServiceDryRunOutboundAdapter.prepare_dry_run()` accepts a
    validated `OutboundMessageRequest` or stable mapping that validates to one.
  - The adapter requires a matching explicit T233
    `WeComCustomerServiceSafetyDecision(safety_state="allowed")`.
  - Direct `CandidateAction` inputs and candidate-shaped mappings are rejected.
  - Invalid mappings, non-sendable requests, non-`wechat` channel preferences,
    missing safety decisions, blocked safety decisions, mismatched
    request/contact/user identity, wrong safety surface, missing aliases, and
    missing T233 boundary audit notes all produce blocked dry-run results.
  - The allow path builds an in-memory dry-run payload with provider surface,
    `dry_run=true`, request/contact/user scope, recipient aliases only,
    approved draft text, optional safe summary, and source audit context.
  - Arbitrary `OutboundMessagePayload.metadata` is not copied into the prepared
    payload.
  - Caller and safety audit notes are preserved with deduplication.
  - The adapter exposes no `transport`, `send`, or `deliver` seam.
  - The input request and safety decision are not mutated.
- Verification status:
  - `python -m py_compile src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py`:
    passed.
  - `pytest tests/test_wecom_customer_service_outbound_adapter.py -q`: passed,
    23 tests, with pytest cache-provider warnings because `.pytest_cache` was
    not writable in this environment.
  - `pytest tests/test_wecom_customer_service_outbound_adapter.py tests/test_wecom_customer_service_safety_gate.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q`:
    passed, 84 tests, with the same pytest cache-provider warnings.
  - `git diff --check`: passed with a line-ending conversion warning for
    `docs/07_handoff.md`.
  - `git status --short`: ran and showed only T232 allowed-file changes. Git
    also reported global ignore permission warnings in this environment.
- Explicit non-actions:
  - No WeCom, WeChat, Tencent, Feishu, or external API calls.
  - No credential, environment-variable, token, cookie, tenant ID, app ID,
    OpenID, UnionID, external user ID, `open_kfid`, callback Token,
    EncodingAESKey, corpsecret, app secret, QR code, or real recipient read.
  - No live transport, fake transport, injected transport, retry logic,
    acknowledgement handling, failure-event mutation, callback route, webhook
    route, polling/sync loop, scheduler, background job, runtime wiring,
    `AppContainer` wiring, or CLI send path.
  - No message sending and no result represented as provider delivered,
    accepted, queued, retried, or acknowledged.
  - No outbound request, safety decision, memory, ContactSkill,
    RelationshipState, feedback-log, approved-store, inbound-store, or private
    artifact mutation.
  - No `private/chat_history/`, `private/distilled/`, or private artifact reads.
  - No task-board update.
  - No production WeCom compatibility or live-delivery readiness claim.
- Remaining risks:
  - T232 proves only local deterministic dry-run payload preparation, not live
    WeCom Customer Service API compatibility.
  - Official Tencent/WeCom docs were not refetched in T232 and may drift before
    live work.
  - The dry-run payload shape is synthetic and review-safe, not an official API
    contract.
  - T233 safety decisions are local snapshots, not live provider state.
  - Recipient aliases are not proven provider identifiers.
  - Credential handling, tenant eligibility, callback verification,
    encryption/decryption, provider failure events, acknowledgement semantics,
    retries, and production recipient mapping remain unresolved.

## T234 Worker Completion Record

- T234 is the M12 WeChat Adapter milestone review task.
- Worker must not mark T234 as complete in `docs/04_task_board.md`; only the
  Captain/Reviewer may advance task-board state after review.
- Files changed:
  - `docs/review/M12_review.md`
  - `docs/worker_summary/T234_worker_summary.md`
  - `docs/07_handoff.md`
- Gate recommendation:
  - `Gate M12 Conditional`.
  - M12 is accepted only as a local, synthetic, dry-run-only WeCom Customer
    Service slice.
  - M12 does not authorize live WeChat or WeCom delivery, credentials,
    callbacks, webhooks, polling, sync loops, transport, retries, provider
    acknowledgement, failure-event mutation, automatic sending, production
    recipient mapping, personal-WeChat automation, scan-login resurrection,
    desktop automation, or unofficial SDK use.
- Evidence reviewed:
  - T230 research/review/summary: unsafe paths remain blocked; WeCom Customer
    Service may be used only as a conditional official-surface candidate.
  - T231 connector/contract/tests/review/summary: synthetic inbound
    message/event normalization only; no live callback, polling, credential,
    store, or outbound behavior.
  - T233 safety gate/contract/tests/review/summary: local provider eligibility
    after `OutboundMessageRequest.is_sendable()` only; `allowed` is not payload
    preparation or delivery.
  - T232 dry-run adapter/contract/tests/review/summary: prepares local
    review-safe dry-run payloads only after a matching allowed T233 decision;
    no `transport`, `send`, or `deliver` seam.
- Verification status:
  - `python -m py_compile src/practical_chat_agent/connectors/inbound/wecom_customer_service.py src/practical_chat_agent/services/wecom_customer_service_safety.py src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py`:
    passed.
  - `pytest tests/test_wecom_customer_service_inbound.py tests/test_wecom_customer_service_safety_gate.py tests/test_wecom_customer_service_outbound_adapter.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q`:
    passed, 90 tests, with pytest cache-provider warnings because
    `.pytest_cache` was not writable in this environment.
  - `git diff --check`: passed with line-ending conversion warnings for
    pre-existing dirty files in this Windows working copy.
  - `git status --short`: ran; the worktree already had pre-existing
    modified/untracked files, and T234 touched only its allowed files. Git also
    reported global ignore permission warnings in this environment.
- Explicit non-actions:
  - No code, tests, schemas, CLI, config, package metadata, risk doc, decision
    log, task package, or task-board edits.
  - No WeCom, WeChat, Tencent, Feishu, or external API calls.
  - No credential, environment-variable, token, cookie, tenant ID, app ID,
    OpenID, UnionID, external user ID, `open_kfid`, callback Token,
    EncodingAESKey, corpsecret, app secret, QR code, or real recipient read.
  - No callback route, webhook route, polling/sync loop, scheduler, background
    job, runtime wiring, `AppContainer` wiring, CLI send path, transport, fake
    transport, retry loop, acknowledgement handling, failure-event mutation, or
    delivery path.
  - No outbound request, safety decision, memory, ContactSkill,
    RelationshipState, feedback-log, approved-store, inbound-store, or private
    artifact mutation.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    reads.
  - No production WeCom compatibility or live-delivery readiness claim.
- Remaining risks:
  - Official Tencent/WeCom docs may drift before live work.
  - WeCom Customer Service may remain a product mismatch for WeFlow personal
    chat exports and personal relationship workflows.
  - `channel_preference="wechat"` is broad and only narrows to WeCom Customer
    Service through explicit T233/T232 surfaces.
  - T231 synthetic fixtures cover only a narrow subset and do not define live
    batching or redaction.
  - T233 service-window and quota checks are supplied local context, not live
    provider state.
  - T232 dry-run payload shape is synthetic and review-safe, not an official
    API request contract.
  - Recipient aliases are not proven provider identifiers.
  - Credential handling, tenant eligibility, callback verification,
    encryption/decryption, provider failure events, acknowledgement semantics,
    retries, and production recipient mapping remain unresolved.

## T240 Worker Completion Record

- T240 is the M13 Commercial Companion Positioning And Safety Boundary Pack.
- Worker must not mark T240 as complete in `docs/04_task_board.md`; T240 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `docs/product/M13_commercial_companion_positioning.md`
  - `docs/product/M13_competitor_matrix.md`
  - `docs/safety/M13_clone_and_persona_risk_tiers.md`
  - `docs/safety/M13_proactive_companionship_redlines.md`
  - `docs/architecture/M13_persona_memory_relationship_architecture.md`
  - `docs/roadmap/M13_plus_milestone_plan.md`
  - `docs/tasks/M14_persona_compiler_schema/T250_persona_compiler_schema.md`
  - `docs/worker_summary/T240_worker_summary.md`
  - `docs/07_handoff.md`
- Product direction:
  - Reposition M13+ toward a transparent, controllable, text-first AI persona
    companion product.
  - Do not continue near-term work by piling on live WeChat/WeCom delivery.
  - Differentiate through persona compilation, trustworthy memory,
    relationship semantics, consented proactive behavior, virtual life streams,
    user controls, and safety/compliance governance.
- Safety outputs:
  - L1 original fictional persona is the near-term M14 target.
  - L2 de-identified style inspiration is future gated work.
  - L3 self-authorized digital self is future-only and consent-heavy.
  - L4 third-party/deceased/commemorative mode is research-only now.
  - L5 unauthorized real-person clone, public-figure clone, ex-partner/family
    clone, voice/face deepfake, and deceptive impersonation remain prohibited.
  - Proactive companionship must be opt-in, rate-limited, quiet-hours aware,
    no-response backed off, non-coercive, crisis-safe, and in-app/sandbox until
    later reviewed tasks change that boundary.
- Architecture and roadmap outputs:
  - Seven-engine architecture: Persona Compiler, Memory OS v2, Relationship
    Engine, Dialogue Engine, Proactive Engine, Virtual Life Engine, and Safety
    & Compliance Engine.
  - M13-M22 milestone plan with candidate task IDs T240 through T335.
  - First M14 task package: T250 `PersonaCard v1 Schema And Source / Consent
    Policy`.
- Public/source checks:
  - Product pages checked: TheOne, Replika, Character.AI calls/voice, Talkie,
    and MiniMax Xingye.
  - Official CAC pages checked: anthropomorphic interaction service rules,
    deep synthesis rules, and AIGC labeling rules.
- Verification status:
  - `git diff --check`: passed, with Windows line-ending conversion warnings
    for existing working-copy files.
  - `Test-Path` checks for all expected T240 docs: all returned `True`.
  - `rg` coverage check for `Gate M13`, `M14`, `M22`, `L1`, `L5`,
    `automatic sending`, `unauthorized clone`, and `imagined memory`: passed
    with expected matches.
- Explicit non-actions:
  - No implementation code, tests, package metadata, runtime config, CLI,
    connector, adapter, store, schema migration, or app UI changes.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No platform API calls, credentials, callbacks, polling, transport,
    scheduler, runtime send path, or automatic sending.
  - No real-person clone, deceased-person resurrection, voice clone,
    face/avatar deepfake, or deceptive impersonation path was authorized.
- Remaining risks:
  - Competitor, pricing, product, and legal facts may drift and need later
    validation.
  - Domestic report-only competitors still need hands-on/app-store/privacy
    review.
  - M14 must keep style inspiration from becoming identifiable real-person
    imitation.
  - Later Memory OS work must prove imagined/factual isolation.
  - Later proactive work must preserve consent and anti-manipulation redlines.

## T250 Worker Completion Record

- T250 is the PersonaCard v1 Schema And Source / Consent Policy task for M14.
- Worker must not mark T250 as complete in `docs/04_task_board.md`; T250 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `tests/test_persona_card_schema.py`
  - `docs/data_contracts/persona_card_v1_contract.md`
  - `docs/tasks/M14_persona_compiler_schema/T251_persona_compiler_local_prototype.md`
  - `docs/worker_summary/T250_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because `PersonaCard` did not exist.
  - GREEN: targeted pytest passed after adding the schema models.
- Schema behavior added:
  - `PersonaCard` with `persona_card_v1` version, generated `persona_` id,
    source policy, fictional identity, traits, speech style, emotion model,
    relationship model, imagined virtual history, growth policy, proactive
    preferences, safety policy, status, and review metadata.
  - `PersonaSourcePolicy` maps `original`/`deidentified_style`/
    `self_authorized`/`third_party_authorized`/`prohibited` to L1-L5 tiers.
  - Non-original non-prohibited sources require consent artifacts.
  - L5 prohibited cards never become runtime-ready.
  - `PersonaVirtualHistory` is explicitly imagined AI-generated content and
    rejects factual claims.
  - `PersonaCard.is_runtime_ready()` requires approved human review and blocks
    unsafe risk/source/identity/safety states.
- T251 next task package:
  - Created
    `docs/tasks/M14_persona_compiler_schema/T251_persona_compiler_local_prototype.md`.
  - T251 is scoped to deterministic local L1 persona compilation from synthetic
    descriptions; no private reads, LLM calls, clone behavior, proactive
    sending, or platform integration.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\core\models.py`: passed.
  - `pytest tests\test_persona_card_schema.py -q`: passed, 13 tests, with
    pytest cache-provider warnings because `.pytest_cache` was not writable.
  - `pytest tests\test_persona_card_schema.py tests\test_behavior_schema.py tests\test_contactskill_persona_brief.py tests\test_relationship_context.py tests\test_outbound_message_request_schema.py -q -o cache_dir=artifacts\t250_pytest_cache --basetemp=artifacts\t250_pytest_basetemp`:
    passed, 109 tests. A prior broader attempt failed only while creating
    `C:\Users\26410\AppData\Local\Temp\pytest-of-26410`.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No compiler service, LLM call, private chat-log read, runtime dialogue use,
    CLI command, storage repository, migration, proactive behavior, platform
    integration, voice/avatar/deepfake behavior, or automatic sending.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - The schema is not yet a compiler or UX.
  - L2 style inspiration still needs a deidentification guard and similarity
    tests.
  - Runtime dialogue consumption remains unopened and must stay behind future
    task packages.

## T251 Worker Completion Record

- T251 is the Local Prompt-To-Schema Persona Compiler Prototype task for M14.
- Worker must not mark T251 as complete in `docs/04_task_board.md`; T251 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/persona_compiler.py`
  - `tests/test_persona_compiler.py`
  - `docs/data_contracts/persona_compiler_contract.md`
  - `docs/tasks/M14_persona_compiler_schema/T252_deidentification_guard_tests.md`
  - `docs/worker_summary/T251_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.persona_compiler` did not exist.
  - GREEN: targeted pytest passed after adding `PersonaCompilerService`.
- Behavior added:
  - `PersonaCompilerService.compile(payload)` returns `PersonaCard v1`.
  - Safe synthetic fictional inputs produce L1 candidate PersonaCards.
  - `detailed_prompt`, `fuzzy_preference`, `template`, and `random_seed` are
    accepted by the local compiler.
  - Fuzzy/template/random inputs use safe fictional defaults.
  - Deterministic keyword mapping populates mood, speech, trait, relationship,
    virtual-history, growth-policy, proactive, and safety fields.
  - Real-person clone, voice/face/deepfake, hidden impersonation, and automatic
    sending signals return rejected L5 prohibited PersonaCards.
  - Compiler surface exposes only `compile()`; no send/schedule/delivery/runtime
    or private chat-history extraction methods were added.
- T252 next task package:
  - Created
    `docs/tasks/M14_persona_compiler_schema/T252_deidentification_guard_tests.md`.
  - T252 is scoped to synthetic deidentification guard tests only; no private
    chat-log reads or real style extraction.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\services\persona_compiler.py`:
    passed.
  - `pytest tests\test_persona_compiler.py -q -o cache_dir=artifacts\t251_pytest_cache --basetemp=artifacts\t251_pytest_basetemp`:
    passed, 10 tests.
  - `pytest tests\test_persona_card_schema.py tests\test_persona_compiler.py -q -o cache_dir=artifacts\t251_pytest_cache_final --basetemp=artifacts\t251_pytest_basetemp_final`:
    passed, 23 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No LLM call, model provider, external API, browser automation, network
    service, private chat-log read, style extraction, similarity scoring,
    runtime dialogue use, review UI, storage repository, migration, proactive
    candidate, platform integration, voice/avatar/deepfake behavior, or
    automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - Keyword mapping is intentionally shallow.
  - `style_inspiration` remains unsupported until T252 and later review gates.
  - L5 detection is not a complete policy engine.
  - Runtime dialogue and versioned storage remain unopened.

## T252 Worker Completion Record

- T252 is the Synthetic Deidentification Guard Tests task for M14.
- Worker must not mark T252 as complete in `docs/04_task_board.md`; T252 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/deidentification_guard.py`
  - `tests/test_deidentification_guard.py`
  - `docs/data_contracts/deidentification_guard_contract.md`
  - `docs/tasks/M14_persona_compiler_schema/T253_persona_review_card_contract.md`
  - `docs/worker_summary/T252_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.deidentification_guard` did not exist.
  - GREEN: targeted pytest passed after adding `DeidentificationGuard`.
- Behavior added:
  - `DeidentificationGuard.assess(text)` returns a machine-readable
    `DeidentificationGuardDecision`.
  - Generic abstract style signals such as concise, warm, delayed response,
    dry humor, practical, and gentle can pass.
  - Direct identifiers, contact identifiers, locations, organizations/schools,
    handles, biometric cues, real-person avatar cues, private events, exact
    biography, clone intent, and distinctive catchphrases are blocked.
  - Decisions never retain raw source text.
  - Guard surface exposes no private file/corpus, similarity, PersonaCard
    compiler, runtime, send, schedule, or delivery methods.
- T253 next task package:
  - Created
    `docs/tasks/M14_persona_compiler_schema/T253_persona_review_card_contract.md`.
  - T253 is scoped to local PersonaCard review-card and decision-contract work.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\services\deidentification_guard.py`:
    passed.
  - `pytest tests\test_deidentification_guard.py -q -o cache_dir=artifacts\t252_pytest_cache --basetemp=artifacts\t252_pytest_basetemp`:
    passed, 7 tests.
  - `pytest tests\test_deidentification_guard.py tests\test_persona_compiler.py -q -o cache_dir=artifacts\t252_pytest_cache_min --basetemp=artifacts\t252_pytest_basetemp_min`:
    passed, 17 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No private chat-log read, private corpus access, real deidentification
    quality claim, similarity scoring, LLM call, embedding, PersonaCard
    generation, runtime dialogue use, proactive behavior, platform integration,
    voice/avatar/deepfake processing, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T252 is synthetic and deterministic; it is not a production
    deidentification guarantee.
  - Future L2 work still needs broader adversarial evaluation before reading
    real private material.
  - PersonaCard review, versioning, and runtime consumption remain unopened.

## T253 Worker Completion Record

- T253 is the Persona Review Card Contract task for M14.
- Worker must not mark T253 as complete in `docs/04_task_board.md`; T253 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/persona_review.py`
  - `tests/test_persona_review.py`
  - `docs/data_contracts/persona_review_card_contract.md`
  - `docs/tasks/M14_persona_compiler_schema/T254_persona_version_store.md`
  - `docs/worker_summary/T253_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.persona_review` did not exist.
  - GREEN: targeted pytest passed after adding `PersonaReviewService`.
- Behavior added:
  - `PersonaReviewService.render(card)` returns a local review-card payload.
  - Payloads expose identity, disclosure, source/risk policy, traits, speech
    style, imagined virtual history, growth policy, proactive preferences,
    safety flags, warnings, and review decisions.
  - L5 prohibited cards render with redacted blocked-request background and
    remain non-runtime-ready.
  - `PersonaReviewService.review(...)` requires a reviewer id, returns a new
    PersonaCard, and updates review metadata history.
  - Approval is blocked for prohibited sources, unsafe tiers, real-person
    similarity blocks, non-fictional identity, real-person references, or
    disabled core safety flags.
  - Rejected and frozen cards remain non-runtime-ready.
  - Service surface exposes no send/schedule/delivery/runtime/memory retrieval
    methods.
- T254 next task package:
  - Created
    `docs/tasks/M14_persona_compiler_schema/T254_persona_version_store.md`.
  - T254 is scoped to local JSON version-store work only.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\services\persona_review.py`:
    passed.
  - `pytest tests\test_persona_review.py -q -o cache_dir=artifacts\t253_pytest_cache --basetemp=artifacts\t253_pytest_basetemp`:
    passed, 7 tests.
  - `pytest tests\test_persona_review.py tests\test_persona_compiler.py tests\test_deidentification_guard.py -q -o cache_dir=artifacts\t253_pytest_cache_min --basetemp=artifacts\t253_pytest_basetemp_min`:
    passed, 24 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No PersonaCard storage, version history, CLI, UI, LLM call, private
    chat-log read, runtime dialogue use, memory retrieval, proactive candidate,
    scheduler, outbound request, platform integration, voice/avatar/deepfake
    behavior, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T253 is not a product UI.
  - Version persistence, rollback, freeze/delete semantics, and export controls
    remain unopened until T254.
  - Runtime dialogue consumption remains unopened.

## T254 Worker Completion Record

- T254 is the Persona Version Store task for M14.
- Worker must not mark T254 as complete in `docs/04_task_board.md`; T254 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/persona_version_store.py`
  - `tests/test_persona_version_store.py`
  - `docs/data_contracts/persona_version_store_contract.md`
  - `docs/tasks/M14_persona_compiler_schema/T255_persona_compiler_m14_gate_review.md`
  - `docs/worker_summary/T254_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.persona_version_store` did not exist.
  - GREEN: targeted pytest passed after adding `PersonaVersionStore`.
- Behavior added:
  - `PersonaVersionStore` writes to a caller-provided local JSON path.
  - Saving a candidate creates version 1; saving an approved review copy
    creates a later version.
  - Latest lookup returns the latest non-deleted version.
  - Rollback appends a new version copied from a prior version without mutating
    history.
  - Freeze appends a frozen review copy; delete appends an archived tombstone.
  - Freeze/delete states are not runtime-ready.
  - Export returns JSON-compatible store data and omits raw private/delivery
    fields.
  - Store surface exposes no send/schedule/delivery/runtime/memory retrieval
    methods.
- T255 next task package:
  - Created
    `docs/tasks/M14_persona_compiler_schema/T255_persona_compiler_m14_gate_review.md`.
  - T255 is scoped to docs-only M14 gate review and M15 entry task creation.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\services\persona_version_store.py`:
    passed.
  - `pytest tests\test_persona_version_store.py -q -o cache_dir=artifacts\t254_pytest_cache --basetemp=artifacts\t254_pytest_basetemp`:
    passed, 7 tests.
  - `pytest tests\test_persona_version_store.py tests\test_persona_review.py tests\test_persona_compiler.py -q -o cache_dir=artifacts\t254_pytest_cache_min --basetemp=artifacts\t254_pytest_basetemp_min`:
    passed, 24 tests.
  - `pytest tests\test_persona_card_schema.py tests\test_persona_compiler.py tests\test_deidentification_guard.py tests\test_persona_review.py tests\test_persona_version_store.py -q -o cache_dir=artifacts\t254_pytest_cache_final --basetemp=artifacts\t254_pytest_basetemp_final`:
    passed, 44 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No database migration, global store discovery, CLI, UI, LLM call, private
    chat-log read, runtime dialogue use, memory retrieval, proactive candidate,
    scheduler, outbound request, platform integration, voice/avatar/deepfake
    behavior, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T254 is a local file store, not production persistence.
  - Concurrency, encryption, access control, cloud sync, and retention remain
    future work.
  - Runtime dialogue and Memory OS v2 remain unopened.

## T255 Worker Completion Record

- T255 is the Persona Compiler M14 Gate Review task.
- Worker must not mark T255 as complete in `docs/04_task_board.md`; T255 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `docs/review/M14_review.md`
  - `docs/tasks/M15_memory_os_v2/T260_memory_event_schema.md`
  - `docs/worker_summary/T255_worker_summary.md`
  - `docs/07_handoff.md`
- Gate result:
  - Recommended `PASS_WITH_WARNINGS` for entering M15 Memory OS v2.
  - M14 is documented as a local Persona Compiler foundation only.
- M15 next task package:
  - Created `docs/tasks/M15_memory_os_v2/T260_memory_event_schema.md`.
  - T260 is scoped to Memory OS v2 schema work only and must preserve factual,
    inferred, relational, procedural, and imagined memory separation.
- Verification status:
  - `pytest tests\test_persona_card_schema.py tests\test_persona_compiler.py tests\test_deidentification_guard.py tests\test_persona_review.py tests\test_persona_version_store.py -q -o cache_dir=artifacts\t255_pytest_cache --basetemp=artifacts\t255_pytest_basetemp`:
    passed, 44 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No code, tests, package metadata, runtime config, CLI, UI, private reads,
    LLM call, Memory OS implementation, retrieval, runtime dialogue, proactive
    behavior, outbound request, platform integration, voice/avatar/deepfake
    behavior, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - M14 remains local and API-level; no product UI or web demo exists yet.
  - Memory OS v2 has not started.
  - Runtime dialogue, proactive behavior, virtual-life stream, controls, and
    commercial UX remain future milestones.

## T260 Worker Completion Record

- T260 is the Memory Event Schema task for M15 Memory OS v2.
- Worker must not mark T260 as complete in `docs/04_task_board.md`; T260 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `tests/test_memory_event_schema.py`
  - `docs/data_contracts/memory_event_v2_contract.md`
  - `docs/tasks/M15_memory_os_v2/T261_memory_store_v2.md`
  - `docs/worker_summary/T260_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because `MemoryEvent` did not exist.
  - GREEN: targeted pytest passed after adding MemoryEvent v2 schema models.
- Behavior added:
  - `MemoryEvent`, `MemoryProvenance`, and `MemoryRetrievalPermission` schemas.
  - Explicit event/truth separation for factual, inferred, relational,
    procedural, and imagined memory.
  - Factual memory requires evidence refs.
  - Inferred memory requires confidence and rationale.
  - Relational memory requires relationship dimensions.
  - Procedural memory requires preference labels and does not become factual.
  - Imagined memory cannot be retrieved as factual evidence.
  - Frozen/deleted/archived memory is not retrieval-eligible.
  - Medium/high sensitivity memory defaults to review-required.
- T261 next task package:
  - Created `docs/tasks/M15_memory_os_v2/T261_memory_store_v2.md`.
  - T261 is scoped to local JSON MemoryEvent store work only.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\core\models.py`: passed.
  - `pytest tests\test_memory_event_schema.py -q -o cache_dir=artifacts\t260_pytest_cache --basetemp=artifacts\t260_pytest_basetemp`:
    passed, 10 tests.
  - `pytest tests\test_memory_event_schema.py tests\test_persona_card_schema.py -q -o cache_dir=artifacts\t260_pytest_cache_min --basetemp=artifacts\t260_pytest_basetemp_min`:
    passed, 23 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No memory store, retrieval ranking, vector search, private chat-log
    ingestion, LLM extraction, background consolidation, dream generation,
    dialogue runtime consumption, proactive candidate, outbound request,
    platform integration, voice/avatar/deepfake behavior, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T260 is schema-only.
  - Store, retrieval, consolidation, forgetting policy, and runtime memory
    consumption remain future work.

## T261 Worker Completion Record

- T261 is the Memory Store v2 task for M15 Memory OS v2.
- Worker must not mark T261 as complete in `docs/04_task_board.md`; T261 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/memory_event_store.py`
  - `tests/test_memory_event_store.py`
  - `docs/data_contracts/memory_event_store_v2_contract.md`
  - `docs/tasks/M15_memory_os_v2/T262_memory_lifecycle_policy.md`
  - `docs/worker_summary/T261_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.memory_event_store` did not exist.
  - GREEN: targeted pytest passed after adding `MemoryEventStore`.
- Behavior added:
  - Caller-path local JSON MemoryEvent store.
  - Append-only store records with `append` and `lifecycle_update`.
  - Latest-record list/query helpers and full-history access.
  - Type-aware helpers for user id, event type, and factual events.
  - Lifecycle updates preserve history and make frozen/deleted events
    retrieval-ineligible.
  - Imagined events are excluded from factual helpers.
  - Safe JSON export omits raw private/delivery fields.
  - Store surface exposes no send/schedule/delivery/runtime/dialogue methods.
- T262 next task package:
  - Created `docs/tasks/M15_memory_os_v2/T262_memory_lifecycle_policy.md`.
  - T262 is scoped to deterministic lifecycle/forgetting policy helpers only.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\services\memory_event_store.py`:
    passed.
  - `pytest tests\test_memory_event_store.py -q -o cache_dir=artifacts\t261_pytest_cache --basetemp=artifacts\t261_pytest_basetemp`:
    passed, 6 tests.
  - `pytest tests\test_memory_event_store.py tests\test_memory_event_schema.py -q -o cache_dir=artifacts\t261_pytest_cache_min --basetemp=artifacts\t261_pytest_basetemp_min`:
    passed, 16 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No vector search, retrieval ranking, semantic similarity, private chat-log
    ingestion, LLM extraction, background consolidation, forgetting/decay
    policy, dialogue runtime consumption, proactive candidate, outbound
    request, platform integration, voice/avatar/deepfake behavior, or automatic
    sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T261 is local JSON storage only.
  - Lifecycle/forgetting policy, retrieval bundle, consolidation, ranking, and
    runtime memory consumption remain unopened.

## T262 Worker Completion Record

- T262 is the Memory Lifecycle Policy task for M15 Memory OS v2.
- Worker must not mark T262 as complete in `docs/04_task_board.md`; T262 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/memory_lifecycle_v2.py`
  - `tests/test_memory_lifecycle_v2.py`
  - `docs/data_contracts/memory_lifecycle_v2_contract.md`
  - `docs/tasks/M15_memory_os_v2/T263_memory_retrieval_bundle_contract.md`
  - `docs/worker_summary/T262_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.memory_lifecycle_v2` did not exist.
  - GREEN: targeted pytest passed after adding
    `MemoryLifecyclePolicyService`.
- Behavior added:
  - Deterministic `MemoryLifecyclePolicyService.recommend(...)`.
  - Recommendation actions: keep, review_required, freeze, delete, archive,
    decay, and compress.
  - High-sensitivity/review-required memory is not retrieval-allowed.
  - Deleted/frozen/archived memory is not retrieval-allowed.
  - Imagined memory is kept only in imagined context.
  - Low-salience old memory can be recommended for decay/compression.
  - Explicit user-delete signal recommends delete.
  - Policy returns recommendations only and does not mutate stores.
- T263 next task package:
  - Created
    `docs/tasks/M15_memory_os_v2/T263_memory_retrieval_bundle_contract.md`.
  - T263 is scoped to retrieval bundle schemas only, not ranking/search.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\services\memory_lifecycle_v2.py`:
    passed.
  - `pytest tests\test_memory_lifecycle_v2.py -q -o cache_dir=artifacts\t262_pytest_cache --basetemp=artifacts\t262_pytest_basetemp`:
    passed, 7 tests.
  - `pytest tests\test_memory_lifecycle_v2.py tests\test_memory_event_store.py tests\test_memory_event_schema.py -q -o cache_dir=artifacts\t262_pytest_cache_min --basetemp=artifacts\t262_pytest_basetemp_min`:
    passed, 23 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No private chat-log read, memory extraction, store mutation, vector search,
    retrieval ranking, semantic similarity, background consolidation, dialogue
    runtime consumption, proactive candidate, outbound request, platform
    integration, voice/avatar/deepfake behavior, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T262 is deterministic policy only.
  - Retrieval bundle schema, consolidation, ranking, and runtime memory
    consumption remain unopened.

## T263 Worker Completion Record

- T263 is the Memory Retrieval Bundle Contract task for M15 Memory OS v2.
- Worker must not mark T263 as complete in `docs/04_task_board.md`; T263 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `tests/test_memory_retrieval_bundle_schema.py`
  - `docs/data_contracts/memory_retrieval_bundle_v2_contract.md`
  - `docs/tasks/M15_memory_os_v2/T264_memory_consolidation_stub.md`
  - `docs/worker_summary/T263_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because `MemoryRetrievalBundle` did not exist.
  - GREEN: targeted pytest passed after adding retrieval bundle schemas.
- Behavior added:
  - `MemoryRetrievalBundleItem.from_event(...)` packages selected MemoryEvent
    records without ranking or search.
  - `MemoryRetrievalBundle` records purpose, query summary, selected ids,
    exclusions, truth-status counts, imagined-memory count, safety warnings,
    and generated timestamp.
  - Factual-purpose bundles reject imagined memory as factual evidence.
  - Deleted/frozen/archived memory cannot be included.
  - Review-required memory requires `include_review_required=true`.
- T264 next task package:
  - Created `docs/tasks/M15_memory_os_v2/T264_memory_consolidation_stub.md`.
  - T264 is scoped to deterministic local consolidation candidates only.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\core\models.py`: passed.
  - `pytest tests\test_memory_retrieval_bundle_schema.py -q -o cache_dir=artifacts\t263_pytest_cache --basetemp=artifacts\t263_pytest_basetemp`:
    passed, 8 tests.
  - `pytest tests\test_memory_retrieval_bundle_schema.py tests\test_memory_event_schema.py -q -o cache_dir=artifacts\t263_pytest_cache_min --basetemp=artifacts\t263_pytest_basetemp_min`:
    passed, 18 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No memory selection, vector search, retrieval ranking, semantic similarity,
    query parsing, private chat-log read, LLM extraction, dialogue runtime
    consumption, proactive candidate, outbound request, platform integration,
    voice/avatar/deepfake behavior, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T263 is schema-only.
  - Actual retrieval selection, ranking, consolidation, and runtime memory
    consumption remain unopened.

## T264 Worker Completion Record

- T264 is the Memory Consolidation Stub task for M15 Memory OS v2.
- Worker must not mark T264 as complete in `docs/04_task_board.md`; T264 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/memory_consolidation_v2.py`
  - `tests/test_memory_consolidation_v2.py`
  - `docs/data_contracts/memory_consolidation_v2_contract.md`
  - `docs/tasks/M15_memory_os_v2/T265_memory_os_m15_gate_review.md`
  - `docs/worker_summary/T264_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.memory_consolidation_v2` did not exist.
  - GREEN: targeted pytest passed after adding `MemoryConsolidationService`.
- Behavior added:
  - `MemoryConsolidationService.propose(...)` returns deterministic
    consolidation candidate groups.
  - Active keep candidates group by event type.
  - Factual events group only with factual events.
  - Imagined events emit `separate_imagined` and stay out of factual groups.
  - Review-required/high-sensitivity events emit `review`.
  - Low-salience old events can emit `decay` or `compress`.
  - Service returns candidates only and does not mutate stores.
- T265 next task package:
  - Created `docs/tasks/M15_memory_os_v2/T265_memory_os_m15_gate_review.md`.
  - T265 is scoped to docs-only M15 gate review and M16 entry task creation.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\services\memory_consolidation_v2.py`:
    passed.
  - `pytest tests\test_memory_consolidation_v2.py -q -o cache_dir=artifacts\t264_pytest_cache --basetemp=artifacts\t264_pytest_basetemp`:
    passed, 6 tests.
  - `pytest tests\test_memory_consolidation_v2.py tests\test_memory_retrieval_bundle_schema.py tests\test_memory_lifecycle_v2.py tests\test_memory_event_schema.py -q -o cache_dir=artifacts\t264_pytest_cache_min --basetemp=artifacts\t264_pytest_basetemp_min`:
    passed, 31 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No LLM summarization, private chat-log read, vector search, retrieval
    ranking, semantic similarity, store mutation, dialogue runtime consumption,
    proactive candidate, outbound request, platform integration,
    voice/avatar/deepfake behavior, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T264 is deterministic grouping only.
  - No generated consolidated memories, LLM summaries, retrieval ranking, or
    runtime consumption exists yet.

## T265 Worker Completion Record

- T265 is the Memory OS M15 Gate Review task.
- Worker must not mark T265 as complete in `docs/04_task_board.md`; T265 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `docs/review/M15_review.md`
  - `docs/tasks/M16_relationship_dialogue_consumption/T270_relationship_context_bundle.md`
  - `docs/worker_summary/T265_worker_summary.md`
  - `docs/07_handoff.md`
- Gate result:
  - Recommended `PASS_WITH_WARNINGS` for entering M16 relationship/dialogue
    context work.
  - M15 is documented as a local Memory OS v2 foundation only.
- M16 next task package:
  - Created
    `docs/tasks/M16_relationship_dialogue_consumption/T270_relationship_context_bundle.md`.
  - T270 is scoped to relationship/dialogue context bundle schemas only.
- Verification status:
  - `pytest tests\test_memory_event_schema.py tests\test_memory_event_store.py tests\test_memory_lifecycle_v2.py tests\test_memory_retrieval_bundle_schema.py tests\test_memory_consolidation_v2.py -q -o cache_dir=artifacts\t265_pytest_cache --basetemp=artifacts\t265_pytest_basetemp`:
    passed, 37 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No code, tests, package metadata, runtime config, CLI, UI, private reads,
    LLM call, retrieval ranking, vector search, runtime dialogue, proactive
    behavior, outbound request, platform integration, voice/avatar/deepfake
    behavior, web demo, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - M15 remains local/API-level; no product UI or web demo exists yet.
  - Relationship/dialogue context consumption has not started.
  - Retrieval ranking, runtime dialogue, proactive behavior, virtual-life
    stream, controls, and commercial UX remain future milestones.

## T270 Worker Completion Record

- T270 is the Relationship Context Bundle task for M16.
- Worker must not mark T270 as complete in `docs/04_task_board.md`; T270 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `tests/test_relationship_context_bundle_schema.py`
  - `docs/data_contracts/relationship_context_bundle_contract.md`
  - `docs/tasks/M16_relationship_dialogue_consumption/T271_dialogue_context_planner.md`
  - `docs/worker_summary/T270_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because `RelationshipContextBundle` did not
    exist.
  - GREEN: targeted pytest passed after adding relationship context bundle
    schemas.
- Behavior added:
  - Persona, memory, and relationship context snapshots.
  - `RelationshipContextBundle.from_sources(...)`.
  - Runtime-ready PersonaCard is required.
  - Imagined memory cannot be packaged as factual context.
  - Retention/manipulation/engagement score dimensions are rejected.
  - Bundle contains no draft reply, send, schedule, delivery, platform, or
    webhook fields.
- T271 next task package:
  - Created
    `docs/tasks/M16_relationship_dialogue_consumption/T271_dialogue_context_planner.md`.
  - T271 is scoped to deterministic planning metadata only.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\core\models.py`: passed.
  - `pytest tests\test_relationship_context_bundle_schema.py -q -o cache_dir=artifacts\t270_pytest_cache --basetemp=artifacts\t270_pytest_basetemp`:
    passed, 5 tests.
  - `pytest tests\test_relationship_context_bundle_schema.py tests\test_persona_card_schema.py tests\test_memory_retrieval_bundle_schema.py -q -o cache_dir=artifacts\t270_pytest_cache_min --basetemp=artifacts\t270_pytest_basetemp_min`:
    passed, 26 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No LLM call, reply generation, dialogue planning, retrieval ranking,
    private reader, proactive candidate, outbound request, platform integration,
    voice/avatar/video behavior, web demo, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T270 is schema-only.
  - Dialogue planning, draft generation, runtime consumption, proactive
    behavior, UI, and web demo remain unopened.

## T271 Worker Completion Record

- T271 is the Dialogue Context Planner task for M16.
- Worker must not mark T271 as complete in `docs/04_task_board.md`; T271 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/dialogue_context_planner.py`
  - `tests/test_dialogue_context_planner.py`
  - `docs/data_contracts/dialogue_context_plan_contract.md`
  - `docs/tasks/M16_relationship_dialogue_consumption/T272_dialogue_draft_stub.md`
  - `docs/worker_summary/T271_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.dialogue_context_planner` did not exist.
  - GREEN: targeted pytest passed after adding `DialogueContextPlanner`.
- Behavior added:
  - Deterministic `DialogueContextPlan` metadata.
  - High boundary risk increases caution.
  - High trust/warmth allows warmer tone without dependency language.
  - Factual context gets factual-only notes.
  - Imagined context is labeled and not treated as factual evidence.
  - Planner emits no draft reply, send, schedule, delivery, platform, or runtime
    fields.
- T272 next task package:
  - Created
    `docs/tasks/M16_relationship_dialogue_consumption/T272_dialogue_draft_stub.md`.
  - T272 is scoped to deterministic review-only draft stub work.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\services\dialogue_context_planner.py`:
    passed.
  - `pytest tests\test_dialogue_context_planner.py -q -o cache_dir=artifacts\t271_pytest_cache --basetemp=artifacts\t271_pytest_basetemp`:
    passed, 6 tests.
  - `pytest tests\test_dialogue_context_planner.py tests\test_relationship_context_bundle_schema.py -q -o cache_dir=artifacts\t271_pytest_cache_min --basetemp=artifacts\t271_pytest_basetemp_min`:
    passed, 11 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No LLM call, final reply generation, retrieval ranking, memory selection,
    proactive candidate, outbound request, platform integration,
    voice/avatar/video behavior, web demo, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T271 is planning metadata only.
  - Draft generation, runtime dialogue, UI, proactive behavior, and web demo
    remain unopened.

## T272 Worker Completion Record

- T272 is the Dialogue Draft Stub task for M16.
- Worker must not mark T272 as complete in `docs/04_task_board.md`; T272 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/dialogue_draft_stub.py`
  - `tests/test_dialogue_draft_stub.py`
  - `docs/data_contracts/dialogue_draft_stub_contract.md`
  - `docs/tasks/M16_relationship_dialogue_consumption/T273_relationship_dialogue_m16_gate_review.md`
  - `docs/worker_summary/T272_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.dialogue_draft_stub` did not exist.
  - GREEN: targeted pytest passed after adding `DialogueDraftStubService`.
- Behavior added:
  - `DialogueDraftStubService.create(plan)` returns review-only
    `DialogueDraftStub`.
  - Draft text is deterministic from plan metadata.
  - Drafts require review.
  - Plan metadata and imagined-memory warnings remain visible.
  - Dependency/manipulation phrases are absent.
- T273 next task package:
  - Created
    `docs/tasks/M16_relationship_dialogue_consumption/T273_relationship_dialogue_m16_gate_review.md`.
  - T273 is scoped to docs-only M16 gate review and M17 entry task creation.
- Verification status:
  - `python -m py_compile src\practical_chat_agent\services\dialogue_draft_stub.py`:
    passed.
  - `pytest tests\test_dialogue_draft_stub.py -q -o cache_dir=artifacts\t272_pytest_cache --basetemp=artifacts\t272_pytest_basetemp`:
    passed, 5 tests.
  - `pytest tests\test_dialogue_draft_stub.py tests\test_dialogue_context_planner.py -q -o cache_dir=artifacts\t272_pytest_cache_min --basetemp=artifacts\t272_pytest_basetemp_min`:
    passed, 11 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No LLM call, final user-visible reply generation, runtime dialogue,
    proactive candidate, outbound request, scheduler, platform integration,
    voice/avatar/video behavior, web demo, or automatic sending.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
  - No real-person clone, public-figure clone, ex-partner/family clone,
    deceased-person mode, or deceptive impersonation path was authorized.
- Remaining risks:
  - T272 is a deterministic review-only stub, not production dialogue.
  - Runtime chat, UI, proactive behavior, platform integration, and web demo
    remain unopened.

## T273 Worker Completion Record

- T273 is the M16 Relationship Dialogue gate review task.
- Worker must not mark T273 as complete in `docs/04_task_board.md`; T273 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `docs/review/M16_review.md`
  - `docs/tasks/M17_proactive_engine_consent/T280_proactive_consent_schema.md`
  - `docs/worker_summary/T273_worker_summary.md`
  - `docs/07_handoff.md`
- Review evidence:
  - Read T270-T272 contracts, worker summaries, and tests.
  - Created the M16 gate review with PASS_WITH_WARNINGS recommendation.
  - Created the T280 M17 entry task package for proactive consent schema work.
- Verification status:
  - `pytest tests\test_relationship_context_bundle_schema.py tests\test_dialogue_context_planner.py tests\test_dialogue_draft_stub.py -q -o cache_dir=artifacts\t273_pytest_cache --basetemp=artifacts\t273_pytest_basetemp`:
    passed, 16 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No code implementation, test modification, task-board status change, LLM
    call, proactive candidate, scheduler, outbound request, delivery adapter,
    platform integration, voice/avatar/video behavior, web demo, or automatic
    sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - M16 is a local review-first foundation only.
  - M17 must still implement explicit consent and policy gates before any
    proactive UX can be safely prototyped.

## T280 Worker Completion Record

- T280 is the Proactive Consent schema task for M17.
- Worker must not mark T280 as complete in `docs/04_task_board.md`; T280 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `tests/test_proactive_consent_schema.py`
  - `docs/data_contracts/proactive_consent_contract.md`
  - `docs/tasks/M17_proactive_engine_consent/T281_proactive_policy_gate.md`
  - `docs/worker_summary/T280_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because `ProactiveConsent` did not exist.
  - GREEN: targeted pytest passed after adding `ProactiveConsent`.
- Behavior added:
  - Local review-only proactive consent schema.
  - Consent status, quiet hours, frequency cap, interval cap, pause/revocation,
    local surfaces, low-pressure intents, and safety notes.
  - Human review is mandatory.
  - Outbound/platform surfaces and disallowed intents are rejected.
- T281 next task package:
  - Created
    `docs/tasks/M17_proactive_engine_consent/T281_proactive_policy_gate.md`.
  - T281 is scoped to deterministic policy gate evaluation only.
- Verification status:
  - `pytest tests\test_proactive_consent_schema.py -q -o cache_dir=artifacts\t280_pytest_cache --basetemp=artifacts\t280_pytest_basetemp`:
    passed, 7 tests.
  - `python -m py_compile src\practical_chat_agent\core\models.py`: passed.
  - `pytest tests\test_proactive_consent_schema.py tests\test_relationship_context_bundle_schema.py -q -o cache_dir=artifacts\t280_pytest_cache_min --basetemp=artifacts\t280_pytest_basetemp_min`:
    passed, 12 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No proactive candidate, scheduler, outbound request, delivery adapter,
    platform integration, push notification, webhook, queue, LLM call,
    production reply generation, voice/avatar/video behavior, social feed, web
    demo, or automatic sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - T280 is schema-only.
  - Policy gate, review card, expanded scenario tests, UI, and web demo remain
    unopened.

## T281 Worker Completion Record

- T281 is the Proactive Policy Gate task for M17.
- Worker must not mark T281 as complete in `docs/04_task_board.md`; T281 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/proactive_policy_gate.py`
  - `tests/test_proactive_policy_gate.py`
  - `docs/data_contracts/proactive_policy_gate_contract.md`
  - `docs/tasks/M17_proactive_engine_consent/T282_quiet_hours_frequency_tests.md`
  - `docs/worker_summary/T281_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.proactive_policy_gate` did not exist.
  - GREEN: targeted pytest passed after adding `ProactivePolicyGate`.
- Behavior added:
  - Deterministic local proactive policy gate.
  - Consent status, surface, intent, quiet-hours, frequency-cap, and
    minimum-interval checks.
  - Review-only allow decision with mandatory human review.
  - Block/defer decisions with deterministic reason labels.
- T282 next task package:
  - Created
    `docs/tasks/M17_proactive_engine_consent/T282_quiet_hours_frequency_tests.md`.
  - T282 is scoped to expanded quiet-hours/frequency/no-response tests.
- Verification status:
  - `pytest tests\test_proactive_policy_gate.py -q -o cache_dir=artifacts\t281_pytest_cache --basetemp=artifacts\t281_pytest_basetemp`:
    passed, 6 tests.
  - `python -m py_compile src\practical_chat_agent\services\proactive_policy_gate.py`:
    passed.
  - `pytest tests\test_proactive_policy_gate.py tests\test_proactive_consent_schema.py -q -o cache_dir=artifacts\t281_pytest_cache_min --basetemp=artifacts\t281_pytest_basetemp_min`:
    passed, 13 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No proactive candidate generator, scheduler, outbound request, delivery
    adapter, platform integration, push notification, webhook, queue, LLM call,
    production reply generation, review UI, voice/avatar/video behavior, social
    feed, web demo, or automatic sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - T281 is policy-gate-only.
  - Expanded edge tests, review card, scenario policy, UI, and web demo remain
    unopened.

## T282 Worker Completion Record

- T282 is the Quiet-Hours And Frequency Edge Tests task for M17.
- Worker must not mark T282 as complete in `docs/04_task_board.md`; T282 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/proactive_policy_gate.py`
  - `tests/test_proactive_quiet_hours_frequency.py`
  - `docs/data_contracts/proactive_policy_gate_contract.md`
  - `docs/tasks/M17_proactive_engine_consent/T283_proactive_review_card.md`
  - `docs/worker_summary/T282_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `ProactivePolicyGate.evaluate(...)` did not accept
    `unanswered_follow_up_count`.
  - GREEN: targeted pytest passed after adding no-response pressure handling.
- Behavior added:
  - Quiet-hours, frequency-cap, minimum-interval, and no-response edge tests.
  - `no_response_pressure_risk` block reason for repeated follow-up after a
    prolonged no-response window.
- T283 next task package:
  - Created
    `docs/tasks/M17_proactive_engine_consent/T283_proactive_review_card.md`.
  - T283 is scoped to local review card rendering only.
- Verification status:
  - `pytest tests\test_proactive_quiet_hours_frequency.py -q -o cache_dir=artifacts\t282_pytest_cache --basetemp=artifacts\t282_pytest_basetemp`:
    passed, 5 tests.
  - `python -m py_compile src\practical_chat_agent\services\proactive_policy_gate.py`:
    passed.
  - `pytest tests\test_proactive_policy_gate.py tests\test_proactive_quiet_hours_frequency.py tests\test_proactive_consent_schema.py -q -o cache_dir=artifacts\t282_pytest_cache_min --basetemp=artifacts\t282_pytest_basetemp_min`:
    passed, 18 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No proactive candidate generator, scheduler, outbound request, delivery
    adapter, platform integration, push notification, webhook, queue, LLM call,
    production reply generation, review UI, voice/avatar/video behavior, social
    feed, web demo, or automatic sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - T282 is policy-test-focused.
  - Review cards, crisis/low-mood policy, M17 gate review, UI, and web demo
    remain unopened.

## T283 Worker Completion Record

- T283 is the Proactive Review Card task for M17.
- Worker must not mark T283 as complete in `docs/04_task_board.md`; T283 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/proactive_review_card.py`
  - `tests/test_proactive_review_card.py`
  - `docs/data_contracts/proactive_review_card_contract.md`
  - `docs/tasks/M17_proactive_engine_consent/T284_crisis_low_mood_policy.md`
  - `docs/worker_summary/T283_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.proactive_review_card` did not exist.
  - GREEN: targeted pytest passed after adding `ProactiveReviewCardService`.
- Behavior added:
  - Local proactive review card rendering.
  - Review actions for allow, block, and defer decisions.
  - Policy reasons, consent status, candidate summary, and safety notes are
    preserved.
  - All cards require review.
- T284 next task package:
  - Created
    `docs/tasks/M17_proactive_engine_consent/T284_crisis_low_mood_policy.md`.
  - T284 is scoped to deterministic crisis/low-mood policy handling only.
- Verification status:
  - `pytest tests\test_proactive_review_card.py -q -o cache_dir=artifacts\t283_pytest_cache --basetemp=artifacts\t283_pytest_basetemp`:
    passed, 5 tests.
  - `python -m py_compile src\practical_chat_agent\services\proactive_review_card.py`:
    passed.
  - `pytest tests\test_proactive_review_card.py tests\test_proactive_policy_gate.py tests\test_proactive_quiet_hours_frequency.py -q -o cache_dir=artifacts\t283_pytest_cache_min --basetemp=artifacts\t283_pytest_basetemp_min`:
    passed, 16 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No proactive candidate generator, scheduler, outbound request, delivery
    adapter, platform integration, push notification, webhook, queue, LLM call,
    production reply generation, review UI, voice/avatar/video behavior, social
    feed, web demo, or automatic sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - T283 creates review artifacts only.
  - Crisis/low-mood policy, M17 gate review, UI, and web demo remain unopened.

## T284 Worker Completion Record

- T284 is the Crisis And Low-Mood Proactive Policy task for M17.
- Worker must not mark T284 as complete in `docs/04_task_board.md`; T284 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/proactive_policy_gate.py`
  - `src/practical_chat_agent/services/proactive_review_card.py`
  - `tests/test_proactive_crisis_low_mood_policy.py`
  - `docs/data_contracts/proactive_policy_gate_contract.md`
  - `docs/data_contracts/proactive_review_card_contract.md`
  - `docs/tasks/M17_proactive_engine_consent/T285_m17_gate_review.md`
  - `docs/worker_summary/T284_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because high-risk safety flags were still
    allowed.
  - GREEN: targeted pytest passed after adding high-risk flag blocks and
    support-oriented review notes.
- Behavior added:
  - Crisis-like, low-mood, and dependency-pressure safety flags block normal
    proactive approval.
  - High-risk review cards expose support-oriented conservative review actions
    only.
  - High-risk card payloads avoid diagnosis, treatment, medical advice,
    emergency handling claims, and delivery/platform fields.
- T285 next task package:
  - Created `docs/tasks/M17_proactive_engine_consent/T285_m17_gate_review.md`.
  - T285 is scoped to docs-only M17 gate review and M18 entry task creation.
- Verification status:
  - `pytest tests\test_proactive_crisis_low_mood_policy.py -q -o cache_dir=artifacts\t284_pytest_cache --basetemp=artifacts\t284_pytest_basetemp`:
    passed, 4 tests.
  - `python -m py_compile src\practical_chat_agent\services\proactive_policy_gate.py src\practical_chat_agent\services\proactive_review_card.py`:
    passed.
  - `pytest tests\test_proactive_crisis_low_mood_policy.py tests\test_proactive_review_card.py tests\test_proactive_policy_gate.py -q -o cache_dir=artifacts\t284_pytest_cache_min --basetemp=artifacts\t284_pytest_basetemp_min`:
    passed, 15 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No diagnosis, treatment, medical advice, emergency handling, external
    escalation, proactive candidate generator, scheduler, outbound request,
    delivery adapter, platform integration, push notification, webhook, queue,
    LLM call, production reply generation, review UI, voice/avatar/video
    behavior, social feed, web demo, or automatic sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - T284 is deterministic high-risk policy only.
  - M17 gate review, virtual life stream, UI, and web demo remain unopened.

## T285 Worker Completion Record

- T285 is the M17 Gate Review task.
- Worker must not mark T285 as complete in `docs/04_task_board.md`; T285 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `docs/review/M17_review.md`
  - `docs/tasks/M18_virtual_life_stream/T290_role_dynamic_post_schema.md`
  - `docs/worker_summary/T285_worker_summary.md`
  - `docs/07_handoff.md`
- Review evidence:
  - Read M17 contracts, worker summaries, and proactive tests.
  - Created the M17 gate review with PASS_WITH_WARNINGS recommendation.
  - Created the T290 M18 entry task package for virtual life stream schema
    work.
- Verification status:
  - `pytest tests\test_proactive_consent_schema.py tests\test_proactive_policy_gate.py tests\test_proactive_quiet_hours_frequency.py tests\test_proactive_review_card.py tests\test_proactive_crisis_low_mood_policy.py -q -o cache_dir=artifacts\t285_pytest_cache --basetemp=artifacts\t285_pytest_basetemp`:
    passed, 27 tests.
  - `git diff --check`: passed.
- Explicit non-actions:
  - No code implementation, test modification, task-board status change, LLM
    call, proactive candidate generation, scheduler, outbound request, delivery
    adapter, platform integration, diagnosis, treatment, medical advice,
    emergency handling, external escalation, voice/avatar/video behavior,
    social feed publishing, web demo, or automatic sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - M17 is a local consented review-first foundation only.
  - M18 must still implement virtual life stream schemas and review-first
    generation stubs before UI/demo consumption.

## T290 Worker Completion Record

- T290 is the Role Dynamic Post Schema task for M18.
- Worker must not mark T290 as complete in `docs/04_task_board.md`; T290 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `tests/test_role_dynamic_post_schema.py`
  - `docs/data_contracts/role_dynamic_post_contract.md`
  - `docs/tasks/M18_virtual_life_stream/T291_virtual_life_engine_text_generator.md`
  - `docs/worker_summary/T290_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because `RoleDynamicPost` did not exist.
  - GREEN: targeted pytest passed after adding `RoleDynamicPost`.
- Behavior added:
  - Review-only virtual life stream draft schema.
  - Imagined AI-generated content status and explicit truth disclosure.
  - Local private review visibility.
  - Factual claims require review notes and remain imagined content.
- T291 next task package:
  - Created
    `docs/tasks/M18_virtual_life_stream/T291_virtual_life_engine_text_generator.md`.
  - T291 is scoped to deterministic local text stub generation only.
- Verification status:
  - `pytest tests\test_role_dynamic_post_schema.py -q -o cache_dir=artifacts\t290_pytest_cache --basetemp=artifacts\t290_pytest_basetemp`:
    passed, 5 tests.
  - `python -m py_compile src\practical_chat_agent\core\models.py`: passed.
  - `pytest tests\test_role_dynamic_post_schema.py tests\test_proactive_consent_schema.py -q -o cache_dir=artifacts\t290_pytest_cache_min --basetemp=artifacts\t290_pytest_basetemp_min`:
    passed, 12 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No post generator, LLM call, scheduler, publisher, outbound request,
    delivery adapter, platform integration, push notification, webhook, queue,
    review UI, voice/avatar/video behavior, Live2D, social feed publishing, web
    demo, or automatic sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - T290 is schema-only.
  - Text generation, AIGC metadata, contamination tests, review cards, UI, and
    web demo remain unopened.

## T291 Worker Completion Record

- T291 is the Virtual Life Engine Text Generator task for M18.
- Worker must not mark T291 as complete in `docs/04_task_board.md`; T291 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/services/virtual_life_engine.py`
  - `tests/test_virtual_life_engine_text_generator.py`
  - `docs/data_contracts/virtual_life_engine_contract.md`
  - `docs/tasks/M18_virtual_life_stream/T292_aigc_labeling_metadata.md`
  - `docs/worker_summary/T291_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because
    `practical_chat_agent.services.virtual_life_engine` did not exist.
  - GREEN: targeted pytest passed after adding `VirtualLifeEngine`.
- Behavior added:
  - Deterministic local virtual life stream draft stub.
  - Seed context captures mood/activity/topic labels and refs.
  - Generated posts preserve imagined labels, review status, and local private
    review visibility.
- T292 next task package:
  - Created `docs/tasks/M18_virtual_life_stream/T292_aigc_labeling_metadata.md`.
  - T292 is scoped to AIGC label/disclosure hardening only.
- Verification status:
  - `pytest tests\test_virtual_life_engine_text_generator.py -q -o cache_dir=artifacts\t291_pytest_cache --basetemp=artifacts\t291_pytest_basetemp`:
    passed, 5 tests.
  - `python -m py_compile src\practical_chat_agent\services\virtual_life_engine.py`:
    passed.
  - `pytest tests\test_virtual_life_engine_text_generator.py tests\test_role_dynamic_post_schema.py -q -o cache_dir=artifacts\t291_pytest_cache_min --basetemp=artifacts\t291_pytest_basetemp_min`:
    passed, 10 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No LLM call, scheduler, publisher, outbound request, delivery adapter,
    platform integration, push notification, webhook, queue, review UI,
    voice/avatar/video behavior, Live2D, social feed publishing, web demo, or
    automatic sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - T291 is deterministic stub generation only.
  - Label hardening, contamination tests, review cards, UI, and web demo remain
    unopened.

## T292 Worker Completion Record

- T292 is the AIGC Labeling Metadata task for M18.
- Worker must not mark T292 as complete in `docs/04_task_board.md`; T292 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/virtual_life_engine.py`
  - `tests/test_virtual_life_aigc_labeling.py`
  - `docs/data_contracts/role_dynamic_post_contract.md`
  - `docs/data_contracts/virtual_life_engine_contract.md`
  - `docs/tasks/M18_virtual_life_stream/T293_imagined_factual_contamination_tests.md`
  - `docs/worker_summary/T292_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because `RoleDynamicPost` did not expose
    `aigc_metadata`.
  - GREEN: targeted pytest passed after adding `AIGCDisclosureMetadata`.
- Behavior added:
  - Explicit AIGC disclosure metadata on RoleDynamicPost.
  - Required labels for AI-generated, imagined, review-required, and
    not-real-world-activity status.
  - Engine-created posts preserve disclosure metadata.
- T293 next task package:
  - Created
    `docs/tasks/M18_virtual_life_stream/T293_imagined_factual_contamination_tests.md`.
  - T293 is scoped to imagined/factual contamination tests only.
- Verification status:
  - `pytest tests\test_virtual_life_aigc_labeling.py -q -o cache_dir=artifacts\t292_pytest_cache --basetemp=artifacts\t292_pytest_basetemp`:
    passed, 4 tests.
  - `python -m py_compile src\practical_chat_agent\core\models.py src\practical_chat_agent\services\virtual_life_engine.py`:
    passed.
  - `pytest tests\test_virtual_life_aigc_labeling.py tests\test_virtual_life_engine_text_generator.py tests\test_role_dynamic_post_schema.py -q -o cache_dir=artifacts\t292_pytest_cache_min --basetemp=artifacts\t292_pytest_basetemp_min`:
    passed, 14 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No LLM call, scheduler, publisher, outbound request, delivery adapter,
    platform integration, push notification, webhook, queue, review UI,
    voice/avatar/video behavior, Live2D, social feed publishing, web demo, or
    automatic sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - T292 hardens labels only.
  - Contamination tests, review cards, UI, and web demo remain unopened.

## T293 Worker Completion Record

- T293 is the Imagined/Factual Contamination Tests task for M18.
- Worker must not mark T293 as complete in `docs/04_task_board.md`; T293 awaits
  adversarial review and Captain judgment.
- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `tests/test_virtual_life_contamination.py`
  - `docs/data_contracts/role_dynamic_post_contract.md`
  - `docs/data_contracts/virtual_life_engine_contract.md`
  - `docs/tasks/M18_virtual_life_stream/T294_dynamic_review_card.md`
  - `docs/worker_summary/T293_worker_summary.md`
  - `docs/07_handoff.md`
- TDD evidence:
  - RED: targeted pytest failed because factual memory could use
    `imagined_generation` provenance and `RoleDynamicPost` lacked
    `memory_ref_usage`.
  - GREEN: targeted pytest passed after adding the contamination guard and
    inspiration-only memory-ref usage.
- Behavior added:
  - Factual memory cannot use imagined-generation provenance.
  - Virtual life memory refs are explicitly inspiration-only.
  - Tests prevent imagined posts from becoming factual retrieval evidence.
- T294 next task package:
  - Created `docs/tasks/M18_virtual_life_stream/T294_dynamic_review_card.md`.
  - T294 is scoped to local virtual life review-card rendering only.
- Verification status:
  - `pytest tests\test_virtual_life_contamination.py -q -o cache_dir=artifacts\t293_pytest_cache --basetemp=artifacts\t293_pytest_basetemp`:
    passed, 5 tests.
  - `python -m py_compile src\practical_chat_agent\core\models.py src\practical_chat_agent\services\virtual_life_engine.py`:
    passed.
  - `pytest tests\test_virtual_life_contamination.py tests\test_virtual_life_aigc_labeling.py tests\test_memory_retrieval_bundle_schema.py -q -o cache_dir=artifacts\t293_pytest_cache_min --basetemp=artifacts\t293_pytest_basetemp_min`:
    passed, 17 tests.
  - `git diff --check`: passed with Windows line-ending conversion warnings.
- Explicit non-actions:
  - No LLM call, scheduler, publisher, outbound request, delivery adapter,
    platform integration, push notification, webhook, queue, review UI,
    voice/avatar/video behavior, Live2D, social feed publishing, web demo, or
    automatic sending was added.
  - No `private/chat_history/`, `private/distilled/`, or private artifact
    content was read, quoted, summarized, or committed.
- Remaining risks:
  - T293 adds contamination guards and tests only.
  - Dynamic review cards, M18 gate review, UI, and web demo remain unopened.
