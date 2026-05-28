# Decision Log

## D068: T230 PASS, accept Gate M12 Conditional, rewrite T231

- Date: 2026-05-28
- Status: Accepted
- Context: `docs/review/T230_review.md` gives `PASS` for the WeChat adapter research spike. No blocking issues were found. The review confirms T230 stayed docs-only and research-only, changed only allowed files, read no private chat content, installed or vendored no SDKs, called no platform APIs, used no credentials, and produced the required `Gate M12 Conditional` research report.
- Decision: T230 is complete. M12 may continue only through a narrowed official WeChat-family surface and only through synthetic contract work first. Captain selects WeCom WeChat Customer Service for T231 and rewrites T231 as `WeCom Customer Service Inbound Contract Spike`.
- Review observation handling:
  - Accepted:
    - N01 external documentation was cited with retrieval date but not independently refetched by the reviewer; future implementation tasks must recheck official docs before touching credentials, callbacks, or APIs.
    - N02 the option matrix is intentionally spike-depth; future implementation tasks need deeper API contract, error taxonomy, and session lifecycle analysis for the selected surface.
    - N03 the report did not choose between WeCom WeChat Customer Service and WeCom internal app; Captain chooses WeCom Customer Service for T231 because it is the best official WeChat-family customer-service candidate for an inbound/event contract spike.
    - N04 `channel_preference="wechat"` is too broad; T231 must not use it as production adapter selection, and any later outbound work needs an explicit surface/subchannel or adapter config.
  - Deferred: none from the T230 review decision.
  - Rejected: none.
- Conditions carried forward:
  - Personal WeChat friend-chat automation, scan-login resurrection, realtime personal-account send/receive, desktop automation, and unofficial SDK vendoring remain blocked.
  - T231 may add only a local deterministic parser/normalizer for synthetic WeCom Customer Service fixtures into `InboundEvent`.
  - T231 must not add live callback routes, webhook servers, polling/sync loops, platform API calls, credentials, SDKs, runtime ingestion hooks, `AppContainer` wiring, outbound payloads, sending, memory writes, private reads, or task-board updates.
  - T232 live outbound remains blocked until T231 passes review and Captain approves a provider-specific recipient mapping / tenant prerequisite model.
  - T233 remains provider-constraint safety design only until rewritten and must not implement delivery.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T230 to T231 and marks T230 complete.
  - `docs/07_handoff.md` records the T230 review decision and T231 task boundary.
  - `docs/08_risks_and_open_questions.md` closes Q203, opens Q204 for T231, and records M12 conditional risks.
  - `docs/tasks/M12_wechat_adapter/T231_wechat_inbound_adapter.md` is rewritten into a complete synthetic-only worker task package.
  - `docs/tasks/M12_wechat_adapter/T232_wechat_outbound_adapter.md` and `docs/tasks/M12_wechat_adapter/T233_wechat_safety_mode.md` are downgraded to blocked placeholders until Captain rewrites them after T231 review.

## D067: T224 PASS, close M11 local/sandbox slice, advance to T230

- Date: 2026-05-28
- Status: Accepted
- Context: `docs/review/T224_review.md` gives `PASS` for the Feishu review-card task. No blocking issues were found. The review confirms T224 renders deterministic local Feishu review-card payloads and parses synthetic inert review-intent actions without network calls, real Feishu API interaction, approval application, adapter calls, feedback-log writes, memory writes, mutation, callbacks, runtime wiring, or automatic sending.
- Decision: T224 is complete. M11 is complete at the task level with `Gate M11 Allow` for local/sandbox outbound safety only. The project may continue to T230 `WeChat Adapter Research Spike`.
- Review observation handling:
  - Accepted:
    - N01 `.claude/settings.json` allowed-permission change is established workspace-artifact convention noise and not functional code.
    - N02 duplicated candidate-shaped mapping detection is acceptable until shared extraction becomes justified.
    - N03 `FeishuSandboxDeliveryResult(**dict(...))` mapping coercion is acceptable for synthetic current scope.
    - N04 missing `FeishuReviewCardConfig` validation edge tests are minor coverage-strength debt.
    - N05 wide `render()` type signature is intentional so `CandidateAction` inputs can be rejected with a clear result.
    - M01-M04 missing positive mapping coercion, small preview-limit, frozen-intent immutability, and cosmetic `CandidateAction` blocked-result tests are useful hardening targets but non-blocking under the current `PASS` verdict.
  - Deferred: none from the T224 review decision.
  - Rejected: none.
- Conditions carried forward:
  - M11 does not authorize production Feishu delivery, real callback/event validation, WeChat implementation, scheduler/background jobs, runtime loops, or automatic outbound behavior.
  - Parsed review-card actions are inert review intents only; applying approval/edit/reject/boundary feedback remains a later explicit task.
  - T230 must be docs-only research and must not resume the old scan-login/realtime personal-WeChat SDK track.
  - T230 must not implement connectors, vendor SDK code, log in, scan QR codes, send/receive messages, call APIs, read secrets, or alter runtime behavior.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T224 to T230, marks T224 complete, and records M11 as task-level `Gate M11 Allow`.
  - `docs/07_handoff.md` records the T224 review decision, M11 close, and T230 task boundary.
  - `docs/08_risks_and_open_questions.md` records review-card callback-validation and M12 WeChat research risks, closes Q202, and opens Q203 for T230.
  - `docs/tasks/M12_wechat_adapter/T230_wechat_adapter_research_spike.md` is expanded into a complete docs-only worker task package.

## D066: T223 PASS, accept Feishu sandbox adapter, advance to T224

- Date: 2026-05-28
- Status: Accepted
- Context: `docs/review/T223_review.md` gives `PASS` for the Feishu sandbox adapter task. No blocking issues were found. The review confirms T223 consumes only already-sendable `OutboundMessageRequest` records, rejects direct `CandidateAction` inputs and candidate-shaped mappings, requires channel `feishu`, uses explicit sandbox recipient mapping outside payload metadata, defaults to dry-run, permits only injected fake/sandbox transport when dry-run is disabled, and introduces no production Feishu delivery, credentials, webhook/callback server, scheduler, runtime loop, CLI send path, external API call, private chat-history read, or store mutation.
- Decision: T223 is complete. The project may continue to T224 `Feishu Review Card`.
- Review observation handling:
  - Accepted:
    - N01 duplicated candidate-shaped mapping detection is acceptable for current adapter-safety scope; shared utility extraction can wait until duplication becomes material.
    - N02 redundant recipient runtime validation is harmless defensive code.
    - N03 recipient-map normalization by reassignment is functionally correct and low risk.
    - N04 Feishu payload shape is acceptable as sandbox approximation, but production delivery must verify current official Feishu API contract before claiming compatibility.
    - N05 mutable delivery-result dataclasses are acceptable for current service-layer scope.
    - M01-M06 missing validation, dry-run override, blocked-transport, blocked-no-transport, and dedupe tests are useful hardening targets but non-blocking under the current `PASS` verdict.
  - Deferred: none from the T223 review decision.
  - Rejected: none.
- Conditions carried forward:
  - T224 may implement only local Feishu review-card rendering and synthetic review-intent parsing over outbound request/gate/sandbox evidence.
  - T224 must not apply approve/edit/reject/boundary-feedback decisions, call adapters, send messages, write feedback logs, write memory, mutate stores, register callbacks/webhooks, read credentials, add CLI/runtime send paths, schedulers, background jobs, or automatic sending.
  - T224 must preserve the distinction between gate eligibility, fake simulation, Feishu sandbox evidence, rendered review card, parsed review intent, applied approval, and production delivery.
  - T224 must keep `CandidateAction` review state as evidence only and must not treat card actions as authorization to send.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T223 to T224 and marks T223 complete.
  - `docs/07_handoff.md` records the T223 review decision and T224 task boundary.
  - `docs/08_risks_and_open_questions.md` records the Feishu sandbox API-validation carry-forward risk and closes Q201.
  - `docs/tasks/M11_outbound_sendgate_feishu/T224_feishu_review_card.md` is expanded into a complete worker task package.

## D065: T222 PASS, accept local fake adapter, advance to T223

- Date: 2026-05-28
- Status: Accepted
- Context: `docs/review/T222_review.md` gives `PASS` for the local fake adapter task. No blocking issues were found. The review confirms T222 consumes only already-sendable `OutboundMessageRequest` records, rejects direct `CandidateAction` inputs, records deterministic synthetic fake-delivery results, and introduces no real platform delivery, scheduler, runtime loop, CLI send path, external service, private chat-history read, or store mutation.
- Decision: T222 is complete. The project may continue to T223 `Feishu Sandbox Adapter`.
- Review observation handling:
  - Accepted:
    - N01 candidate-shaped mapping detection is intentionally conservative for current adapter-safety scope.
    - N02 rejected direct `CandidateAction` model instances may report `contact_id=None` / `user_id=None`; this is cosmetic because the result is already `blocked_invalid_request`.
    - N03 `payload_preview` truncates and normalizes text but is not a privacy boundary for future real adapters.
    - M01 missing fake-adapter config validation tests are minor coverage-strength debt and should be covered in T223 if touching fake-adapter tests.
    - M02 missing explicit `existing_audit` fake-adapter test is minor coverage-strength debt and should be covered in T223 if touching fake-adapter tests.
    - M03 missing exact-boundary preview truncation tests are minor coverage-strength debt and should be covered in T223 if touching fake-adapter tests.
  - Deferred: none from the T222 review decision.
  - Rejected: none.
- Conditions carried forward:
  - T223 may implement only a Feishu sandbox/dry-run adapter boundary over already-sendable `OutboundMessageRequest` records.
  - T223 must not add production Feishu delivery, real platform credentials, webhook/event handling, runtime/CLI send paths, schedulers, background jobs, or automatic sending.
  - T223 must keep recipient mapping explicit and outside `OutboundMessagePayload.metadata`.
  - T223 must not treat gate `allowed`, fake `fake_delivered`, or candidate approval as production delivery.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T222 to T223 and marks T222 complete.
  - `docs/07_handoff.md` records the T222 review decision and T223 task boundary.
  - `docs/08_risks_and_open_questions.md` records the real-adapter privacy carry-forward risk and closes Q200.
  - `docs/tasks/M11_outbound_sendgate_feishu/T223_feishu_adapter.md` is expanded into a complete worker task package.

## D064: T221 PASS, accept OutboundSendGate, advance to T222

- Date: 2026-05-28
- Status: Accepted
- Context: `docs/review/T221_review.md` gives `PASS` for the deterministic outbound send-gate task. No blocking issues were found. The review confirms T221 implements all required gate rules, stays pure/non-mutating, and introduces no adapters, schedulers, CLI send paths, runtime loops, external services, private chat-history reads, or platform integration.
- Decision: T221 is complete. The project may continue to T222 `Local Fake Adapter`.
- Review observation handling:
  - Accepted:
    - N01 service-layer dataclasses and `ValueError` config validation are acceptable because these objects are not JSON round-trip schemas.
    - N02 repeated HH:MM parsing is harmless at current evaluate-per-request scale.
    - N03 `casefold()` normalization is sufficient for current Chinese/Latin duplicate/self-echo checks.
    - N04 Windows `zoneinfo` requires `tzdata` for named timezones; this is a portability/environment risk, not a T221 correctness blocker.
    - N05 `manual_only_mode=False` raising a clear error is appropriate defensive design for the conservative mainline.
    - N06 untested `existing_audit` merge support is harmless forward-compatible surface.
    - N07 `OutboundSendGateDecision` is acceptable even though audit self-containment requires reading `evaluated_request.send_gate`.
    - M01-M04 missing clear-path tests for quiet hours, frequency, duplicate, and self-echo are useful T222-adjacent hardening but non-blocking.
    - M05-M10 missing tests for existing audit, config edge validation, determinism, mapping context input, original `updated_at`, and combined blocking reasons are minor coverage-strength gaps.
  - Deferred: none from the T221 review decision.
  - Rejected: none.
- Conditions carried forward:
  - T222 may implement only a local fake adapter over already sendable `OutboundMessageRequest` records.
  - T222 must not call Feishu/WeChat/webhook/email/browser/desktop APIs, create schedulers/background jobs, or add runtime/CLI delivery paths.
  - T222 should preserve the distinction between gate `allowed`, local fake simulation, and real delivery.
  - T222 should add the most useful T221 pass-through tests before relying on the allow path end to end.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T221 to T222 and marks T221 complete.
  - `docs/07_handoff.md` records the T221 review decision and T222 task boundary.
  - `docs/08_risks_and_open_questions.md` records the T221 portability/carry-forward risks and closes Q199.
  - `docs/tasks/M11_outbound_sendgate_feishu/T222_local_fake_adapter.md` is expanded into a complete worker task package.

## D063: T220 PASS, accept outbound request schema, advance to T221

- Date: 2026-05-27
- Status: Accepted
- Context: `docs/review/T220_review.md` gives `PASS` for the `OutboundMessageRequest` schema task. No blocking issues were found. The review confirms T220 stayed schema-only and introduced no sending, scheduling, platform adapter, runtime loop, CLI send path, LLM call, store mutation, private chat-history read, or `CandidateAction` send-authorization shortcut.
- Decision: T220 is complete. The project may continue to T221 `OutboundSendGate`.
- Review observation handling:
  - Accepted:
    - N01 `_OUTBOUND_MESSAGE_FORBIDDEN_METADATA_FIELDS` could use a cleaner frozenset union expression, but the current runtime behavior is harmless.
    - N02 the contract doc does not enumerate the entire outbound forbidden-key superset; the code remains authoritative and T221 may improve documentation if touching the contract.
    - N03 `OutboundMessagePayload.draft_text` has no max length; this is acceptable for the schema-only boundary.
    - N04 `source_candidate_action_id` is syntactically validated only; store-backed evidence existence remains outside T220.
    - N05 cross-field validators on human approval and send gate state use correct Pydantic v2 patterns and enforce useful defensive invariants.
    - N06 allowed-file compliance is satisfied; the mentioned docs are explicitly in T220's allowed list.
    - N07 untracked `artifacts/t220_pytest_basetemp/` contents are workspace temp noise from verification, not a T220 scope issue.
    - M01 standalone approval/gate validator edge tests are minor coverage-strength debt.
    - M02 `OutboundMessageRequest.is_sendable()` true-path coverage is valuable to add in T221 when the gate begins populating allowed state.
    - M03 outbound-specific forbidden metadata key coverage should be expanded when T221 hardens the boundary.
    - M04 timestamp round-trip coverage is minor schema-test debt.
    - M05 all-channel-preference coverage is minor schema-test debt.
  - Deferred: none from the T220 review decision.
  - Rejected: none.
- Conditions carried forward:
  - T221 must implement gate policy only: explicit outbound human approval requirement, quiet hours, frequency limits, duplicate suppression, kill switch, self-echo prevention, and audit notes.
  - T221 must not implement fake/Feishu/WeChat adapters, review cards, CLI/runtime send paths, schedulers, background jobs, or automatic delivery.
  - T221 must keep `CandidateAction` review status as evidence only and must not treat `OutboundMessageChannel` as a real adapter target.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T220 to T221 and marks T220 complete.
  - `docs/07_handoff.md` records the T220 review decision and T221 task boundary.
  - `docs/08_risks_and_open_questions.md` records T221 carry-forward risks and closes Q198.
  - `docs/tasks/M11_outbound_sendgate_feishu/T221_outbound_send_gate.md` is expanded into a complete worker task package.

## D062: T214 PASS, accept Gate M10 Allow, advance to T220

- Date: 2026-05-27
- Status: Accepted
- Context: `docs/review/T214_review.md` gives `PASS` for the behavior safety eval task, and `docs/review/T214_behavior_safety_eval.md` recommends `Gate M10 Allow`. No blocking issues were found. The review confirms T214 stayed within the allowed docs-only scope and did not modify code, tests, schemas, CLIs, services, config, task board, or private artifacts.
- Decision: T214 is complete. M10 is complete with `Gate M10 Allow`. The project may continue to M11/T220 `OutboundMessageRequest Schema`.
- Review observation handling:
  - Accepted:
    - N01 conflict-handling limitation is a conservative design choice: conflict-heavy inputs produce notes or `do_nothing`, not nuanced conflict-resolution drafts.
    - N02 repeated-review history-count repair was not proposed because T214 is evaluation-only; the issue remains minor test-strength debt.
    - N03 CLI path metadata remains an accepted project-wide offline CLI convention risk and is not repaired by an evaluation task.
    - N04 supplementary reading of `README.md` and `docs/02_experiment_plan.md` in the eval scope is harmless context gathering.
    - N05 temp/cache cleanup evidence is cosmetic; committed tests and reported command results are the trust anchor.
    - M01 missing explicit boundary-sensitive draft-enrichment scenario is a traceability-strength note covered implicitly by existing tests and eval question 3.
    - M02 policy-disallowed action-type scenario could trace the exact code path more explicitly, but the behavior is covered and non-blocking.
  - Deferred: none from the T214 review decision.
  - Rejected: none.
- M10 milestone review:
  - `docs/review/M10_review.md` records that current functionality is complete within review-only scope, can be run from a clean checkout with normal test dependencies, has committed tests and eval results, has no blocking pseudo-completion, and may enter M11.
- Conditions carried forward:
  - T220 must define `OutboundMessageRequest` separately from `CandidateAction`.
  - T220/T221 must not infer send permission from `CandidateAction.status`, `review_state`, or `is_runtime_visible()`.
  - No platform adapter, real sending, scheduler, background job, or automatic outbound behavior is authorized by M10.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T214 to T220 and marks T214 complete.
  - `docs/07_handoff.md` records the T214 review decision, M10 gate, and T220 task boundary.
  - `docs/08_risks_and_open_questions.md` records M10 residual risks and closes Q197.
  - `docs/tasks/M11_outbound_sendgate_feishu/T220_outbound_message_request_schema.md` is expanded into a complete worker task package.

## D061: T213 PASS, accept CandidateAction review CLI, advance to T214

- Date: 2026-05-25
- Status: Accepted
- Context: `docs/review/T213_review.md` gives `PASS` for the CandidateAction review CLI task. No blocking issues were found. The review confirms T213 is additive, manual-review-only, non-executing, and introduces no message sending, scheduling, platform integration, LLM calls, external services, memory mutation, approved-store mutation, or raw transcript paths.
- Decision: T213 is complete. The project may continue to T214 `Behavior Safety Eval`.
- Review observation handling:
  - Accepted:
    - N01 Captain-authored T212 close-out changes in governance docs are established convention noise and are not T213 worker scope leaks.
    - N02 CLI stdout includes safe `input_path` / `output_path` values through `_safe_cli_path()`; this follows prior project path-output convention and remains low risk for the offline single-user workflow.
    - N03 `docs/for_human/T212_review_explanation.md` in the working tree is a prior reviewer/Captain artifact, not a T213 worker leak.
    - N04 default in-place overwrite when `--output` is omitted follows existing review-CLI convention and is documented; low risk in the current offline workflow.
    - N05 `_apply_decision` type suppression is cosmetic typing debt because all status values are validated through the closed decision-to-status mapping.
    - M01 missing CLI-level `freeze` / `archive` / `reject` smoke tests are accepted as minor coverage-strength notes because service-level coverage covers all decisions and CLI approval coverage exists.
    - M02 missing repeated-review history-count test is accepted as a minor coverage-strength note.
    - M03 missing CLI-level reject/freeze/archive round-trip validation is accepted as a minor coverage-strength note because the approval path validates the CLI output shape and service-level tests cover the decisions.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T214 is evaluation-only and must not modify implementation code.
  - T214 must evaluate T210-T213 safety boundaries, especially that reviewed/approved candidates remain non-sendable and non-schedulable.
  - T214 must not authorize outbound behavior, platform adapters, schedulers, background jobs, or automatic sending.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T213 to T214 and marks T213 complete.
  - `docs/07_handoff.md` records the T213 review decision and T214 task boundary.
  - `docs/08_risks_and_open_questions.md` records that no new deferred T213 risks are opened.
  - `docs/tasks/M10_behavior_planner/T214_behavior_safety_eval.md` is expanded into a complete worker task package.

## D060: T212 PASS, accept proactive draft generator, advance to T213

- Date: 2026-05-25
- Status: Accepted
- Context: `docs/review/T212_review.md` gives `PASS` for the proactive draft generator task. No blocking issues were found. The review confirms T212 is additive, deterministic, draft-only, non-executing, and introduces no message sending, scheduling, platform integration, LLM calls, memory mutation, CLI commands, runtime wiring, or raw transcript paths.
- Decision: T212 is complete. The project may continue to T213 `CandidateAction Review CLI`.
- Review observation handling:
  - Accepted:
    - N01 `docs/for_human/T212_review_explanation.md` and `docs/worker_summary/T212_worker_summary.md` allowed-files overrun is treated as established convention noise.
    - N02 static draft text literals keyed by `BehaviorActionType` are acceptable for deterministic scope; forward-compatible `reply_follow_up_draft` and `topic_suggestion` draft entries are harmless even though T211 does not currently emit those action types.
    - N03 unreachable `_draft_text_for` fallback with `pragma: no cover` is accepted as cosmetic defensive code.
    - N04 `model_copy(update=...)` does not rerun validators, but is safe for current scope because the only update is optional `draft_text` on an already validated payload.
    - N05 overwriting existing `draft_text` is acceptable for current initial-enrichment scope; callers should treat the generator as deterministic replacement.
    - M01 missing mapping-with-existing-draft overwrite test is accepted as a minor coverage-strength note.
    - M02 missing planner+generator pipeline coverage for `reply_follow_up_draft` / `topic_suggestion` is accepted because current T211 rules do not emit those types.
    - M03 missing double-enrichment idempotence test is accepted as a minor coverage-strength note.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T213 may add manual review state changes for `CandidateAction` records only.
  - T213 must not treat approval as send/schedule/platform authorization.
  - T213 must preserve all T210/T211/T212 invariants and must not mutate unrelated stores or private artifacts.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T212 to T213 and marks T212 complete.
  - `docs/07_handoff.md` records the T212 review decision and T213 task boundary.
  - `docs/08_risks_and_open_questions.md` records that no new deferred T212 risks are opened.
  - `docs/tasks/M10_behavior_planner/T213_candidate_action_review_cli.md` is expanded into a complete worker task package.

## D059: T211 PASS, accept deterministic rule engine, advance to T212

- Date: 2026-05-25
- Status: Accepted
- Context: `docs/review/T211_review.md` gives `PASS` for the action-planner rule engine task. No blocking issues were found. The review confirms T211 is additive, deterministic, local, candidate-only, non-executing, and introduces no message sending, scheduling, platform integration, LLM calls, memory mutation, CLI commands, runtime wiring, or raw transcript paths.
- Decision: T211 is complete. The project may continue to T212 `Proactive Draft Generator`.
- Review observation handling:
  - Accepted:
    - N01 `docs/for_human/T211_review_explanation.md` allowed-files overrun is treated as established reviewer-convention noise; `docs/worker_summary/T211_worker_summary.md` is allowed by the task package and is also part of the established worker-summary convention.
    - N02 truncated SHA-1 deterministic action ids are accepted for the current offline single-user workflow because they follow existing project id patterns and collision risk is negligible at this scale.
    - N03 overlap between boundary-trigger flags and proactive-blocking flags is accepted and intentional: boundary-sensitive context should produce a review note while blocking optimistic proactive check-ins.
    - N04 `contact_id=None` fallback to `user_id` is accepted for current scope, with the documented meaning that the candidate is not targeted at a specific contact.
    - N05 `casefold()` normalization is accepted; contract flag values remain expected to be normalized safe labels.
    - M01 missing committed label-only `memory_review_prompt` test is accepted as a minor coverage-strength note.
    - M02 missing per-flag proactive-blocking parametrized tests are accepted as minor coverage-strength notes.
    - M03 missing committed `contact_id=None` fallback test is accepted as a minor coverage-strength note.
    - M04 missing multi-boundary-flag single-candidate test is accepted as a minor coverage-strength note.
    - M05 missing boundary-label-only trigger test is accepted as a minor coverage-strength note.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T212 may generate review-safe draft text for candidate actions only.
  - T212 must preserve all T210/T211 invariants: human review required, no auto-send, no platform execution, no scheduler, no platform target, no mutation, and no raw transcript inputs.
  - T212 must not add CLI/runtime wiring, platform adapters, outbound gate behavior, or LLM calls unless a future task explicitly authorizes them.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T211 to T212 and marks T211 complete.
  - `docs/07_handoff.md` records the T211 review decision and T212 task boundary.
  - `docs/08_risks_and_open_questions.md` records that no new deferred T211 risks are opened.
  - `docs/tasks/M10_behavior_planner/T212_proactive_draft_generator.md` is expanded into a complete worker task package.

## D058: T210 PASS, accept behavior schema, advance to T211

- Date: 2026-05-25
- Status: Accepted
- Context: `docs/review/T210_review.md` gives `PASS` for the behavior schema task. No blocking issues were found. The review confirms T210 is schema-only, draft-only, non-executable, and did not introduce planner logic, scheduling, platform integration, message sending, memory mutation, LLM calls, or raw transcript paths.
- Decision: T210 is complete. The project may continue to T211 `Action Planner Rule Engine`.
- Review observation handling:
  - Accepted:
    - N01 `docs/for_human/T210_review_explanation.md` allowed-files overrun is treated as established reviewer-convention noise.
    - N02 `docs/worker_summary/T210_worker_summary.md` allowed-files overrun is treated as established worker-summary convention noise.
    - N03 / M03 missing explicit `access_token` and `api_key` forbidden-key tests are accepted as low-risk test-strength observations because the full forbidden-key set is enforced by the shared metadata validator.
    - N04 reuse of `DistillationStatus` for `CandidateAction.status` is accepted for this schema-first stage and matches nearby lifecycle patterns.
    - N05 duplicated safety invariant fields on `BehaviorPolicy` and `CandidateAction` are accepted because each artifact remains independently safe when detached.
    - M01 no dedicated `BehaviorPolicy.max_candidates <= 0` test is accepted because the schema constraint is present and this is not blocking.
    - M02 no `AgentSelfState(contact_id=None)` round-trip test is accepted as minor boundary coverage debt.
    - M04 no explicit `CandidateActionPayload.review_notes` round-trip test is accepted as minor boundary coverage debt.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T211 may implement deterministic rule-based candidate generation only.
  - T211 must emit draft-only `CandidateAction` artifacts and preserve all T210 safety invariants.
  - T211 must not send messages, schedule actions, integrate platforms, call LLMs, mutate memory/ContactSkill/RelationshipState/approved stores, or bypass human review.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T210 to T211 and marks T210 complete.
  - `docs/07_handoff.md` records the T210 review decision and T211 task boundary.
  - `docs/08_risks_and_open_questions.md` records that no new deferred T210 risks are opened.
  - `docs/tasks/M10_behavior_planner/T211_action_planner_rule_engine.md` is expanded into a complete worker task package.

## D057: T203 PASS, accept optional Mem0 adapter spike, advance to T210

- Date: 2026-05-24
- Status: Accepted
- Context: `docs/review/T203_review.md` gives `PASS` for the optional Mem0 adapter spike. No blocking issues were found. The review confirms the adapter is additive, lazy-imported, optional/off-by-default, covered by 45 tests, and does not introduce a required dependency, raw transcript path, write path, store mutation, ChatContext wiring, planner changes, send behavior, or platform integration.
- Decision: T203 is complete. M9 is complete at the task level. The project may continue to T210 `Behavior Schema`.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` allowed-files overrun is treated as established workspace-artifact convention noise.
    - N02 `docs/worker_summary/T203_worker_summary.md` allowed-files overrun is treated as established worker-summary convention noise.
    - N03 T203 reuses the T202 eval case shape rather than importing the T202 runner directly; acceptable for a spike, but a production external adapter should use the T202 runner directly.
    - N04 documentation/test-count discrepancies are harmless documentation nits and do not affect safety or functionality.
    - N05 `_infer_memory_type` English keyword heuristics are acceptable for a spike but should not be treated as multilingual production classification.
    - M01 no dedicated `limit=0` test is acceptable for spike scope.
    - M02 no empty-string `contact_id` test is acceptable for spike scope.
    - M03 no direct `ImportError` simulation is acceptable because absent-config behavior covers the safe `not_configured` path and import is lazy.
    - M04 no non-`Exception` error test is acceptable because allowing `KeyboardInterrupt` / `SystemExit` to propagate is correct behavior.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - The Mem0 adapter remains optional and off-by-default; it is not production external-memory adoption.
  - Any future external-memory production task must add review enforcement, evidence mapping, SDK/dependency pinning, and operational error handling before runtime use.
  - T210 must stay schema-only and draft-only: no message sending, no scheduled real actions, no platform integration, no automatic memory mutation, and no autonomous behavior claims.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T203 to T210 and marks T203 complete.
  - `docs/07_handoff.md` records the T203 review decision and T210 task boundary.
  - `docs/08_risks_and_open_questions.md` records that no new T203 deferred risks are opened.
  - `docs/tasks/M10_behavior_planner/T210_behavior_schema.md` is expanded into a complete worker task package.

## D056: T202 PASS, accept retrieval eval set, advance to T203

- Date: 2026-05-24
- Status: Accepted
- Context: `docs/review/T202_review.md` gives `PASS` for the retrieval eval set task. No blocking issues were found. The review confirms T202 is additive and eval-only, uses synthetic data, exercises retrievers through the public `MemoryRetriever` protocol, and does not introduce raw transcript access, external dependencies, mutation, ChatContext wiring, planner changes, or outbound behavior changes.
- Decision: T202 is complete. The project may continue to T203 `Optional Mem0 Adapter Spike`.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` allowed-files overrun is treated as established workspace-artifact convention noise.
    - N02 `docs/worker_summary/T202_worker_summary.md` allowed-files overrun is treated as established worker-summary convention noise.
    - N03 eval coverage targets `LocalApprovedStoreRetriever` rather than the older context-bound `LocalMemoryRetriever`; this is acceptable because T202's goal is a reusable protocol eval set and the older adapter requires live `AgentProfile`, `InboundEvent`, and `MemoryFact` setup.
    - M01 lack of a dedicated empty-string query case is accepted because T201 already covers it and T202 covers `None`, whitespace, case-insensitive, substring, miss, and multi-token query behavior.
    - M02 excluded records use uniform importance/confidence values; this is acceptable because T202's exclusion assertions are about runtime-readiness boundaries, not ranking among excluded records.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T203 must remain a spike and must not make Mem0 or any external memory package a required runtime dependency.
  - T203 may add an optional adapter boundary only behind the `MemoryRetriever` protocol and should reuse the T202 eval set where feasible.
  - T203 must not read private chat history, index raw transcripts, auto-write memory, mutate approved stores, call external services in tests, wire into `ChatContext`, change `ReplyPlanner` / policy / send behavior, or claim production adoption.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T202 to T203 and marks T202 complete.
  - `docs/07_handoff.md` records the T202 review decision and T203 task boundary.
  - `docs/08_risks_and_open_questions.md` records that no new T202 deferred risks are opened.
  - `docs/tasks/M9_memory_retrieval_layer/T203_optional_mem0_adapter_spike.md` is expanded into a complete worker task package.

## D055: T201 PASS, accept local approved-store retriever, advance to T202

- Date: 2026-05-24
- Status: Accepted
- Context: `docs/review/T201_review.md` gives `PASS` for the local approved-store retriever task. No blocking issues were found. The review confirms `LocalApprovedStoreRetriever` is additive, implements the T200 protocol, filters conservatively to approved/runtime-ready/evidence-passed records, preserves evidence refs, and does not introduce raw transcript access, external dependencies, mutation, or planner/send behavior changes.
- Decision: T201 is complete. The project may continue to T202 `Retrieval Eval Set`.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` allowed-files overrun is treated as established workspace-artifact convention noise.
    - N02 `docs/worker_summary/T201_worker_summary.md` allowed-files overrun is treated as established worker-summary convention noise.
    - N03 per-call store-file reads without caching are acceptable for the current offline-first, single-user workflow.
    - M01 `limit=0` coverage is accepted as a harmless boundary guard.
    - M02 lack of explicit concurrent-read tests is accepted as outside current single-user offline scope.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T202 must build synthetic retrieval eval cases through the `MemoryRetriever` protocol and `MemoryRetrieverResult` shape.
  - T202 must use only committed synthetic/redacted fixtures and must not use private chat content.
  - T202 must remain eval-only: no vector DB, Mem0/Zep, embedding/provider calls, raw transcript reads, ChatContext wiring, planner/policy/send behavior changes, or external services.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T201 to T202 and marks T201 complete.
  - `docs/07_handoff.md` records the T201 review decision and T202 task boundary.
  - `docs/08_risks_and_open_questions.md` records that no new T201 deferred risks are opened.
  - `docs/tasks/M9_memory_retrieval_layer/T202_retrieval_eval_set.md` is expanded into a complete worker task package.

## D054: T200 PASS, accept MemoryRetriever contract, advance to T201

- Date: 2026-05-24
- Status: Accepted
- Context: `docs/review/T200_review.md` gives `PASS` for the MemoryRetriever interface task. No blocking issues were found. The review confirms the implementation is contract-first, additive, local-only, and does not introduce raw transcript access, external memory dependencies, auto-write behavior, or planner changes.
- Decision: T200 is complete. The project may continue to T201 `Local Approved-Store Retriever`.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` allowed-files overrun is treated as established workspace-artifact convention noise.
    - N02 `docs/worker_summary/T200_worker_summary.md` allowed-files overrun is treated as established worker-summary convention noise.
    - N03 `MemoryHit.source` remains a free-form string with documented convention values; this is acceptable for contract-first adapter extensibility.
    - M01 two adapter tests use guarded assertions, but the same setup is already covered by a direct hit-producing test, so this is accepted as a minor test-strength observation rather than deferred risk.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T201 must implement the T200 protocol against approved local store records only.
  - T201 must return `MemoryHit` items with `source="approved_store"` and preserve evidence refs.
  - T201 must not introduce vector DB, Mem0/Zep, embedding/provider calls, raw transcript reads, auto-write behavior, or planner/policy/send behavior changes.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T200 to T201 and marks T200 complete.
  - `docs/07_handoff.md` records the T200 review decision and T201 task boundary.
  - `docs/08_risks_and_open_questions.md` records that no new T200 deferred risks are opened.
  - `docs/tasks/M9_memory_retrieval_layer/T201_local_approved_store_retriever.md` is expanded into a complete worker task package.

## D053: T195 PASS_WITH_WARNINGS, close M8 as infrastructure/eval milestone, advance to T200

- Date: 2026-05-24
- Status: Accepted
- Context: `docs/review/T195_review.md` gives `PASS_WITH_WARNINGS` for the relationship-aware reply evaluation task. No blocking issues were found. The review confirms the task stayed evaluation-only, but it also shows that the worker's claimed keyword-match mechanism was factually wrong and that the current planner does not semantically consume relationship deltas.
- Decision: T195 is complete. M8 is closed as a relationship-state infrastructure/evaluation milestone, and the project may continue to T200 `MemoryRetriever Interface`.
- Warning handling:
  - Accepted:
    - W01 the worker's milestone-review/handoff mechanism claim was incorrect, but this is a documentation-accuracy issue and is corrected in the captain governance sync rather than requiring a repair pass.
    - W04 `docs/for_human/T195_review_explanation.md` allowed-files overrun is treated as low-risk convention noise.
  - Deferred:
    - W02 relationship dimension-change values are present in `ChatContext` but unused by `ReplyPlanner` / `ReplyPlanPolicyEngine`.
    - W03 relationship guidance reaching `ChatContext.summary` and retrieval notes is informational only and does not create semantic planner consumption.
  - Rejected: none.
- Conditions carried forward:
  - T200 must stay contract-first and local-only. No vector DB, no Mem0/Zep adapter, no auto-write, and no raw transcript retrieval are authorized.
  - M8 closure does not imply relationship-aware planner behavior already exists. Any future planner/policy consumption of relationship deltas requires its own scoped task.
  - T200 should not entangle retriever abstraction work with deferred planner-behavior gaps from T195.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T195 to T200 and marks T195 complete.
  - `docs/07_handoff.md` records the corrected T195 judgment and the next worker task boundary.
  - `docs/08_risks_and_open_questions.md` records the deferred "context present but behaviorally inert" risks from the T195 review.
  - `docs/tasks/M9_memory_retrieval_layer/T200_memory_retriever_interface.md` is rewritten into a stricter worker task package.

## D052: T194 PASS_WITH_WARNINGS, accept compact-context task, advance to T195

- Date: 2026-05-24
- Status: Accepted
- Context: `docs/review/T194_review.md` gives `PASS_WITH_WARNINGS` for the compact relationship-context task. No blocking issues were found, and the review confirms the task stayed context-only, approval-gated, and within the intended M8 boundary.
- Decision: T194 is complete. The project may continue to T195 `Relationship-Aware Reply Eval`.
- Warning handling:
  - Accepted:
    - N01 relationship context reads individual delta JSON files rather than a store-file abstraction, which is acceptable for the current scope.
    - N02 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a T194 scope defect.
    - S01 diagnostic notes entering retrieval notes are a project-wide convention.
    - S02 `ApprovedStoreContextStatus` reuse is acceptable cross-domain coupling for this compact context layer.
    - S03 lack of AppContainer wiring is outside current scope.
  - Deferred:
    - M01 summary truncation edge case is not directly tested.
    - M02 path-is-directory branch is not directly tested.
    - M03 empty `delta_rationale` input is not directly tested.
  - Rejected: none.
- Conditions carried forward:
  - T195 must stay evaluation-only. No code changes, no private artifacts committed, and no state application are authorized.
  - T195 should compare `ReplyPlan` behavior under different approved relationship contexts and capture evidence only.
  - T195 should treat relationship context as compact guidance, not as an automatic state mutation channel.
  - M8 remains open as an evaluation milestone, but no additional implementation task is authorized by T194 alone.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T194 to T195 and marks T194 complete.
  - `docs/07_handoff.md` records the T194 review decision and what T195 may assume next.
  - `docs/08_risks_and_open_questions.md` records the deferred context-loading and coverage risks from the T194 review.
  - `docs/tasks/M8_relationship_state/T195_relationship_aware_eval.md` is rewritten into a stricter worker task package.

## D051: T193 PASS_WITH_WARNINGS, accept relationship review task, advance to T194

- Date: 2026-05-24
- Status: Accepted
- Context: `docs/review/T193_review.md` gives `PASS_WITH_WARNINGS` for the relationship review CLI task. No blocking issues were found, and the review confirms the task stayed review-only, auditable, and within the intended M8 boundary.
- Decision: T193 is complete. The project may continue to T194 `RelationshipState Compact Context`.
- Warning handling:
  - Accepted:
    - N02 default input-file overwrite risk follows the same accepted review-CLI pattern seen in earlier tasks.
    - N04 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a T193 scope defect.
  - Deferred:
    - N01 no committed CLI-level integration tests yet exercise the Typer command path.
    - N03 no evidence pre-validation gate exists before approval, so later context/application tasks must not over-assume approval implies evidence freshness.
    - M01 no committed Typer-command regression tests yet exist for valid/invalid CLI flows.
    - M02 no explicit committed test yet covers the empty-string note path.
  - Rejected: none.
- Conditions carried forward:
  - T194 must stay context-only. No RelationshipState mutation, no send/platform integration, and no raw signal-history injection are authorized.
  - T194 should expose compact approved relationship-state guidance, not raw delta-review internals.
  - T194/T195 should remember that T193 approval is a human decision layer, not a substitute for evidence-prevalidation.
  - M8 remains open; T193 closes review wiring, not state application.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T193 to T194 and marks T193 complete.
  - `docs/07_handoff.md` records the T193 review decision and what T194 may assume next.
  - `docs/08_risks_and_open_questions.md` records the deferred CLI/evidence-gate risks from the T193 review.
  - `docs/tasks/M8_relationship_state/T194_relationship_state_context.md` is rewritten into a stricter worker task package.

## D050: T192 PASS_WITH_WARNINGS, accept delta-generation task, advance to T193

- Date: 2026-05-24
- Status: Accepted
- Context: `docs/review/T192_review.md` gives `PASS_WITH_WARNINGS` for the RelationshipDeltaCandidate generation task. No blocking issues were found, and the review confirms the task stayed conservative, reviewable, and within the intended M8 boundary.
- Decision: T192 is complete. The project may continue to T193 `Relationship Review CLI`.
- Warning handling:
  - Accepted:
    - N01 heuristic `_MAGNITUDE_SCALE=0.2` and `_MIN_STRENGTH=0.3` are acceptable for candidate-only scope.
    - N02 max-strength aggregation is acceptable for current conservative scope even though it loses signal-count information.
    - N03 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a T192 scope defect.
    - N04 `dimension_name` type-ignore suppression is acceptable cosmetic typing debt for the current deterministic generator.
    - N05 `_DIRECTION_SIGN` string-key typing is acceptable and does not create a correctness issue.
  - Deferred:
    - M01 no committed test yet confirms that a signal for an unknown dimension name is skipped safely.
    - M02 no committed test yet covers mixed known-direction plus unknown/stable companion signals on the same dimension.
    - M04 no committed test yet covers the state-evidence-only deduplication edge case that could leave `evidence_refs` empty.
  - Rejected: none.
- Conditions carried forward:
  - T193 must stay review-only. No auto-apply to `RelationshipState`, no send/platform integration, and no hidden mutation are authorized.
  - T193 should preserve the T192 candidate surface as an auditable artifact with explicit approve/reject/freeze/archive decisions.
  - Partial dimension-level approval remains an open design question; T193 should either stay all-or-nothing or document any finer-grained semantics explicitly before implementing them.
  - M8 remains open; T192 is candidate generation, not approved-state application.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T192 to T193 and marks T192 complete.
  - `docs/07_handoff.md` records the T192 review decision and what T193 may assume next.
  - `docs/08_risks_and_open_questions.md` records the deferred delta-generation test gaps from the T192 review.
  - `docs/tasks/M8_relationship_state/T193_relationship_review_cli.md` is rewritten into a stricter worker task package.

## D049: T191 PASS_WITH_WARNINGS, accept signal-extraction task, advance to T192

- Date: 2026-05-24
- Status: Accepted
- Context: `docs/review/T191_review.md` gives `PASS_WITH_WARNINGS` for the RelationshipSignal extractor task. No blocking issues were found, and the review confirms the task stayed conservative, evidence-backed, and within the intended M8 boundary.
- Decision: T191 is complete. The project may continue to T192 `RelationshipDeltaCandidate`.
- Warning handling:
  - Accepted:
    - N01 the handoff test-count mismatch is a documentation accuracy issue, not a code defect.
    - N02 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a T191 scope defect.
    - N04 the static rule-table `# type: ignore[arg-type]` is acceptable for the current deterministic extractor scope.
    - N05 sparse signal coverage across only three dimensions is intentional and conservative for this task.
  - Deferred:
    - N03 `RelationshipSignal` lacks an `updated_at` field, so T193 should make update timing explicit or accept the asymmetry knowingly.
    - M01 no committed test yet exercises an approved `RelationshipSignal` runtime-ready path.
    - M02 no committed test yet covers `signal_id` format or non-emptiness.
  - Rejected: none.
- Conditions carried forward:
  - T192 must stay delta-only. No auto-approval, no state mutation, no send/platform integration, and no scalar-collapse are authorized.
  - T192 should consume T191 signals and make dimension-change semantics explicit, including magnitude and direction handling.
  - T193 should later use the same review/lifecycle pattern already established for other M8 reviewable artifacts.
  - M8 remains open; T191 is executable signal extraction, not milestone closure.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T191 to T192 and marks T191 complete.
  - `docs/07_handoff.md` records the T191 review decision and what T192 may assume next.
  - `docs/08_risks_and_open_questions.md` records the deferred signal-model and coverage risks from the T191 review.
  - `docs/tasks/M8_relationship_state/T192_relationship_delta_candidate.md` is rewritten into a stricter worker task package.

## D048: T190 PASS_WITH_WARNINGS, accept schema task, advance to T191

- Date: 2026-05-24
- Status: Accepted
- Context: `docs/review/T190_review.md` gives `PASS_WITH_WARNINGS` for the RelationshipState schema task. No blocking issues were found, and the review confirms the task stayed schema-only, conservative, and within the intended M8 boundary.
- Decision: T190 is complete. The project may continue to T191 `Relationship Signal Extractor`.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a T190 scope defect.
    - N04 `RelationshipState.source_type` not yet including an approved-delta variant is acceptable forward-compatibility debt for the schema-opening step.
  - Deferred:
    - N02 `RelationshipDeltaDimension.magnitude` is not enforced to match `abs(proposed_value - current_value)`, so downstream consumers must not treat it as schema-guaranteed until T192 or later hardening constrains it.
    - N03 `RelationshipDeltaDirection="stable"` is available but not yet contract-guided, so T191/T192 must avoid inventing contradictory stable-delta semantics.
    - M01 no committed automated tests yet exercise `RelationshipState` / `RelationshipDeltaCandidate` validation, helper behavior, or boundary enforcement.
  - Rejected: none.
- Conditions carried forward:
  - T191 must stay extraction-only. No raw chat-history reads, no state mutation, no delta generation, no review CLI, and no LLM dependency are authorized.
  - T191 should emit evidence-backed relationship signals that later T192 delta generation can reference.
  - T192 must either enforce or explicitly compute `magnitude` / direction semantics so later reviewers are not left with ambiguous delta interpretation.
  - M8 remains open; T190 is contract completion, not milestone closure.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T190 to T191 and marks T190 complete.
  - `docs/07_handoff.md` records the T190 review decision and what T191 may assume next.
  - `docs/08_risks_and_open_questions.md` records the deferred schema-consistency and test-coverage risks from the T190 review.
  - `docs/tasks/M8_relationship_state/T191_relationship_signal_extractor.md` is rewritten into a stricter worker task package.

## D047: T185 PASS_WITH_WARNINGS, close M7 with Allow, advance to T190

- Date: 2026-05-23
- Status: Accepted
- Context: `docs/review/T185_review.md` gives `PASS_WITH_WARNINGS` for the narrow hybrid alignment task. The review confirms that the four M7 gate conditions from `docs/review/T184_milestone_review.md` are now resolved. The Captain milestone review in `docs/review/M7_review.md` therefore revisits Gate M7 positively.
- Decision: T185 is complete. M7 is closed with `Allow`. The project may proceed to M8 beginning with T190 `RelationshipState Schema`.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a blocker.
    - N02 heuristic safety-context detection is acceptable for the current prompt-level alignment scope.
    - N03 language enforcement remaining prompt-level is acceptable for current scope and does not justify reopening M7.
  - Deferred: none from the T185 task review itself.
  - Rejected: none.
- Milestone judgment:
  - M7 now has a complete additive chain from contract -> offline generation -> shared validation -> hybrid integration -> holdout evidence -> narrow alignment repair.
  - M7 is allowed to close because hybrid mode remains opt-in and review-only, the committed merge-path regression gap is closed, and no blocking pseudo-completion was found.
  - M7 closure does not mean calibrated confidence, perfect safety-context detection, or automatic-send readiness.
- Impact:
  - `docs/review/M7_review.md` is created as the milestone-level authorization review.
  - `docs/04_task_board.md` moves the Current Unique Task from T185 to T190 and marks Gate M7 `Allow`.
  - `docs/07_handoff.md` records the T185 review decision and the M7 milestone review decision.
  - `docs/08_risks_and_open_questions.md` closes the M7 gate questions and carries forward only the residual heuristic/prompt-level/calibration risks.
  - `docs/tasks/M8_relationship_state/T190_relationship_state_schema.md` is tightened so the first M8 worker step is explicit and schema-only.

## D046: T184 PASS_WITH_WARNINGS, Gate M7 Conditional, advance to T185

- Date: 2026-05-23
- Status: Accepted
- Context: `docs/review/T184_review.md` gives `PASS_WITH_WARNINGS` for the holdout evaluation task, and `docs/review/T184_milestone_review.md` sets Gate M7 to `Conditional`. The eval produced evidence, but the milestone is not yet fully closed.
- Decision: T184 is complete. The project may continue to T185 `Hybrid Planner Language and Safety Alignment`, but M7 remains open.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a blocker.
    - N02 self-reported ratings without independent verification are acceptable for this MVP milestone eval.
    - N03 candidate-diversity measured by `approach_label` count only is acceptable as a first proxy.
  - Deferred: none from the task review itself.
- Conditions carried forward from Gate M7:
  - T185 must fix the language mismatch, prompt-level safety gap, approach_label normalization gap, and committed merge-path regression gap.
  - T185 must stay narrow and must not expand planner scope or make hybrid mode default.
  - T184 evidence remains evidence, not final readiness proof; M7 stays `Conditional` until the narrow follow-up is resolved.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T184 to T185 and marks T184 complete with Gate M7 `Conditional`.
  - `docs/07_handoff.md` records the T184 review decision and the Gate M7 conditions.
  - `docs/08_risks_and_open_questions.md` records the language/safety/label/merge gaps as active risks.
  - `docs/tasks/M7_llm_reply_planner/T185_hybrid_planner_language_and_safety_alignment.md` is created as the next narrow worker task.

## D045: T183 PASS_WITH_WARNINGS, accept task, advance to T184

- Date: 2026-05-23
- Status: Accepted
- Context: `docs/review/T183_review.md` gives `PASS_WITH_WARNINGS` for the hybrid planner integration task. No blocking issues were found, and the review confirms the hybrid surface is additive, opt-in, and review-only.
- Decision: T183 is complete. The project may continue to T184 `Planner Holdout Eval`.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a task-scope defect, consistent with prior precedent.
  - Deferred:
    - N02 no committed test exercises the valid LLM-candidate merge success path.
    - M01 no end-to-end hybrid success test exists.
    - M02 no explicit reranked-order assertion after merge exists.
  - Rejected: none.
- Conditions carried forward:
  - T184 must remain evaluation-only. No planner code changes, no send/platform integration, and no raw private content in committed artifacts.
  - T184 must distinguish private smoke evidence from committed tests and must not overclaim quality without holdout data.
  - T184 should assess template vs hybrid behavior on anonymized scenarios and record the result as evidence, not as a code change request.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T183 to T184 and marks T183 complete.
  - `docs/07_handoff.md` records the T183 review decision and what T184 may assume next.
  - `docs/08_risks_and_open_questions.md` records the missing committed coverage for hybrid merge success.
  - `docs/tasks/M7_llm_reply_planner/T184_llm_planner_holdout_eval.md` is tightened into a formal worker task package.

## D044: T182 PASS_WITH_WARNINGS, accept task, advance to T183

- Date: 2026-05-23
- Status: Accepted
- Context: `docs/review/T182_review.md` gives `PASS_WITH_WARNINGS` for the shared validator-hardening task. No blocking issues were found, and the review confirms the extraction/reuse/regression-hardening work is solid overall.
- Decision: T182 is complete. The project may continue to T183 `Hybrid ReplyPlanner`.
- Warning handling:
  - Accepted:
    - N02 `.claude/settings.json` modification is treated as workspace-artifact noise rather than a task-scope defect, consistent with prior precedent.
  - Deferred:
    - N01 the `INPUT_TOO_LARGE` preflight call-site bug means the dedicated deterministic refusal path is still non-functional in practice.
    - M01 no committed regression test yet covers the `INPUT_TOO_LARGE` refusal path, so the preflight bug could regress silently.
  - Rejected: none.
- Conditions carried forward:
  - T183 must keep template mode backward-compatible and must not make hybrid/LLM behavior the default path.
  - T183 must preserve shared deterministic validation, policy/boundary review, compact-context boundaries, and review-only output semantics.
  - T183 may integrate optional LLM candidates only behind explicit opt-in controls and must not bypass refusal handling or validator gates.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T182 to T183 and marks T182 complete.
  - `docs/07_handoff.md` records the T182 review decision and what T183 may assume next.
  - `docs/08_risks_and_open_questions.md` records the still-open `INPUT_TOO_LARGE` preflight/test debt.
  - `docs/tasks/M7_llm_reply_planner/T183_hybrid_reply_planner.md` is tightened into a formal worker task package.

## D043: T181 PASS_WITH_WARNINGS, accept task, advance to T182

- Date: 2026-05-23
- Status: Accepted
- Context: `docs/review/T181_review.md` gives `PASS_WITH_WARNINGS` for the offline LLM candidate CLI task. No blocking issues were found, and the review confirms the task stayed offline, opt-in, additive, and separate from the existing deterministic planner path.
- Decision: T181 is complete. The project may continue to T182 `Candidate Validator`.
- Warning handling:
  - Accepted:
    - N01 allowed-files overrun for `.claude/settings.json` and `docs/reference/AI_coding_workflow.md` is treated as low-risk workspace/process noise rather than a T181 implementation blocker.
    - N02 default `policy_boundary` refs in `_build_candidates` are accepted for the MVP generator stage; evidence-grounded LLM-provided refs remain later work.
    - N03 redundant `validate_ranks` call is accepted as dead work with no correctness impact.
  - Deferred:
    - N04 substring-only privacy leak detection remains too narrow for paraphrase/key-detail leakage and is carried forward as validator hardening debt.
    - N05 `INPUT_TOO_LARGE` refusal code exists without explicit budget enforcement and is carried forward as validator/preflight debt.
    - M01 `_build_llm_input` output-shape coverage is still missing.
    - M02 `_parse_provider_response` error-path coverage is still missing.
    - M03 no committed end-to-end generator-to-validator pipeline test yet exists.
    - M04 no committed CLI stdout privacy regression test yet exists.
  - Rejected: none.
- Conditions carried forward:
  - T182 must stay validator-only. No new candidate generation mode, hybrid planner wiring, or default runtime LLM path is authorized yet.
  - T182 may harden deterministic validation, privacy checks, impersonation checks, shared candidate validation reuse, and explicit input-budget refusal handling.
  - T182 must preserve compact-context boundaries, review-only mode, approved-store semantics, and human-approved outbound policy.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T181 to T182 and marks T181 complete.
  - `docs/07_handoff.md` records the T181 review decision and what T182 may assume next.
  - `docs/08_risks_and_open_questions.md` records deferred validator/privacy/test hardening debt.
  - `docs/tasks/M7_llm_reply_planner/T182_candidate_validator.md` is rewritten into a stricter worker task package.

## D042: T180 PASS, accept task, advance to T181

- Date: 2026-05-23
- Status: Accepted
- Context: `docs/review/T180_review.md` gives `PASS` for the LLM candidate contract task. No blocking or non-blocking issues were found, and the review confirms the task stayed contract-only, additive, and within the allowed documentation scope.
- Decision: T180 is complete. The project may continue to T181 `LLM Candidate Offline CLI`.
- Conditions carried forward:
  - T181 must stay offline and opt-in. It may not make LLM generation the default planner path.
  - T181 must consume only safe synthetic/redacted `ChatContext` JSON that already respects T123/T164/T174 compact-context boundaries; no new raw-transcript input path is authorized.
  - T181 must produce a private `LLMReplyPlan` artifact or structured refusal with deterministic post-generation validation before output is written.
  - T181 must not modify the existing deterministic `ReplyPlanner`, `ReplyPlanPolicyEngine`, approved-store semantics, or review-only gating.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T180 to T181 and marks T180 complete.
  - `docs/07_handoff.md` records the T180 review decision and what T181 may assume next.
  - `docs/tasks/M7_llm_reply_planner/T181_llm_candidate_offline_cli.md` is tightened so the next worker task is explicit, private-output-only, and non-hybrid.

## D041: T174 PASS, complete M6, authorize T180

- Date: 2026-05-23
- Status: Accepted
- Context:
  - `docs/review/T174_review.md` gives `PASS` for the derived-brief context integration task.
  - `docs/review/M6_review.md` now concludes Gate M6 = `Allow`.
- Decision:
  - T174 is complete.
  - M6 is complete.
  - The project may enter M7, beginning with T180 `LLM Candidate Generator Contract`.
- Follow-up notes carried forward:
  - N01 `.claude/settings.json` modification is treated as workspace noise rather than a T174 scope violation.
  - N02 per-assembly instantiation of `ContactSkillProjectionService()` is accepted as low-impact offline overhead, not a blocker.
  - N03 reuse of `ApprovedStoreContextStatus` on `DerivedBriefContext` is accepted as a benign enum-breadth trade-off.
  - N04 unused `_load_derived_brief_context(contact_id=...)` parameter is accepted as minor dead surface area.
  - N05 `stable_preference_hints[:2]` compact-note truncation is accepted as small context-budget debt.
  - M01/M02/M03 from T174 review are accepted as non-blocking residual coverage gaps for the current synthetic-test phase; they do not block M6 closure.
- Conditions carried forward:
  - T180 must remain contract-only. No LLM call path, hybrid planner behavior, or runtime mutation is authorized yet.
  - Any M7 work must preserve T123/T164/T174 compact-context contracts, review-only mode, privacy boundaries, and anti-impersonation rules.
  - Future planner work must not reinterpret derived briefs or approved patches as automatic learning.
- Impact:
  - `docs/04_task_board.md` moves the Current Unique Task from T174 to T180.
  - `docs/review/M6_review.md` is created as the milestone-level authorization review.
  - M7 is now opened only at the contract-definition layer.

## D040: T173 PASS, accept task, advance to T174

- Date: 2026-05-23
- Status: Accepted
- Context: `docs/review/T173_review.md` gives `PASS` for the projection service task. No blocking issues were found, and the review confirms the task stayed pure, additive, deterministic, and within the allowed file scope.
- Decision: T173 is complete. The project may continue to T174 `Derived Briefs Context Integration`.
- Follow-up notes carried forward:
  - N01 `.claude/settings.json` modification is treated as workspace noise rather than a T173 scope violation.
  - N02 missing direct assertions for trivial persona field projections is accepted; the risk is negligible and existing tests already exercise those paths sufficiently.
  - N03 unreachable `_max_sensitivity(default=...)` fallback is accepted as harmless defensive redundancy.
  - N04 `relationship_state_summary` format is accepted as a T173-local projection convention; T174 must consume it as projection-owned output rather than re-deriving or reformatting it in context assembly.
- Conditions carried forward:
  - T174 remains context-integration-only. No planner behavior change, migration, or deprecation is authorized yet.
  - T174 must preserve the separate `ApprovedContactSkillBrief` fallback path and the separate T164 approved-patch compact-context path.
  - T174 must treat projected briefs as additive overlays over existing approved-store context, not as a replacement for it.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T173 to T174, `docs/07_handoff.md` records the PASS decision, and the T174 task package is tightened around fallback preservation and coexistence with approved-patch context.

## D039: T172 PASS, accept task, advance to T173

- Date: 2026-05-23
- Status: Accepted
- Context: `docs/review/T172_review.md` gives `PASS` for the `CommunicationPolicyBrief` + `BoundaryProfileBrief` schema task. No blocking issues were found, and the review confirms the task stayed additive, schema-only, and within the allowed file scope.
- Decision: T172 is complete. The project may continue to T173 `ContactSkillProjectionService`.
- Follow-up notes carried forward:
  - N01 `CommunicationPolicyBrief.evidence_refs` remains structurally thin because upstream `reply_strategy` and `user_side_preferences` models do not carry direct evidence refs. This is accepted as an inherited model limitation; T173 must preserve it faithfully and must not invent synthetic evidence.
  - N02 `BoundaryProfileBrief.sensitivity_summary` model default is a schema fallback only. T173 must compute the value explicitly from the documented reduction rule rather than relying on the default.
  - N03 `important_event_summaries` remains free-form at schema level. T173 must own the formatting rule explicitly and keep it deterministic.
  - N04 `.claude/settings.json` modification is treated as workspace noise rather than a T172 scope violation.
- Conditions carried forward:
  - T173 remains a pure, lazy projection layer only. No `ChatContext` integration, ReplyPlanner behavior change, migration, or deprecation is authorized yet.
  - T173 must project only from approved, runtime-ready `ContactSkillStoreRecord` inputs.
  - T174 must preserve the existing `ApprovedContactSkillBrief` fallback and the separate T164 approved-patch compact-context path.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T172 to T173, `docs/07_handoff.md` records the PASS decision, and the T173 task package is tightened around evidence fidelity, sensitivity computation, and event-summary formatting.

## D038: T171 PASS, accept task, advance to T172

- Date: 2026-05-23
- Status: Accepted
- Context: `docs/review/T171_review.md` gives `PASS` for the `PartnerPersonaBrief` schema task. No blocking issues were found, and the review confirms the task stayed additive, schema-only, and within the allowed file scope.
- Decision: T171 is complete. The project may continue to T172 `CommunicationPolicyBrief` + `BoundaryProfileBrief` Schemas.
- Follow-up notes carried forward:
  - N01 `.claude/settings.json` modification is treated as workspace noise rather than a T171 scope violation.
  - N02 the `ContactSkillCommunicationStyle` `"unknown"` -> brief `None` conversion rule is accepted as a projection-layer concern and must be made explicit in T173.
  - N03 `relationship_state_summary` remains structurally valid at schema stage; T173 must define and document how `ContactSkillRelationshipState` fields project into that summary.
  - N04 flat brief-level `evidence_refs` is an accepted design trade-off; T173/T174 must preserve this contract and not invent per-area attribution unless a later task explicitly changes the model.
  - N05 lack of a brief-local `schema_version` field is acceptable for T171 scope, but T172 must explicitly decide whether later derived briefs add version markers or continue relying on parent store versioning.
- Conditions carried forward:
  - T172 remains model/contract work only. No projection service, `ChatContext` integration, ReplyPlanner behavior change, migration, or deprecation is authorized yet.
  - T173 must remain a pure, lazy projection layer over approved, runtime-ready `ContactSkillStoreRecord` inputs.
  - T174 must preserve the existing `ApprovedContactSkillBrief` fallback and the separate T164 approved-patch compact-context path.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T171 to T172, `docs/07_handoff.md` records the PASS decision, and the T172/T173 task packages are tightened around the remaining M6 schema/projection semantics.

## D037: T170 PASS, accept task, advance to T171

- Date: 2026-05-22
- Status: Accepted
- Context: `docs/review/T170_review.md` gives `PASS` for the ContactSkill decomposition design task. No blocking issues were found, and the review confirms the task stayed design-only and within the allowed documentation scope.
- Decision: T170 is complete. The project may continue to T171 `PartnerPersonaBrief` Schema.
- Follow-up notes carried forward:
  - N01 `BoundaryProfileBrief.sensitivity_summary` reduction semantics remain to be formalized during T172 schema work.
  - N02 `PartnerPersonaBrief.communication_style_snapshot` typing must be resolved during T171 schema definition.
  - N03 `important_event_summaries` ownership may be revisited during T172/T174 if the runtime truly needs persona-layer event context.
  - N04 boundary-signaling patch hints remain a future boundary/schema concern for T172 or later, not a T170 blocker.
  - N05 handoff section-number churn is accepted as documentation maintenance noise rather than an implementation defect.
- Conditions carried forward:
  - T171 and T172 remain model/contract tasks only. No projection service, `ChatContext` integration, ReplyPlanner behavior change, migration, or deprecation is authorized yet.
  - T173 must project lazily from approved, runtime-ready `ContactSkillStoreRecord` inputs only.
  - T174 must preserve the existing `ApprovedContactSkillBrief` fallback and may not break the T123/T164 compact-context path.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T170 to T171, `docs/07_handoff.md` records the PASS decision, and the M6 task packages are tightened so schema/projection/context work stays separated.

## D036: T164 PASS_WITH_WARNINGS, accept task, advance to T170

- Date: 2026-05-22
- Status: Accepted
- Context: `docs/review/T164_review.md` gives `PASS_WITH_WARNINGS` for the approved patch compact context task. No blocking issues were found.
- Decision: T164 is complete. The project may continue to T170 ContactSkill Decomposition Design.
- Warning handling:
  - Accepted:
    - N01 `.claude/settings.json` modification is treated as workspace noise rather than a T164 scope violation.
    - N02 `_compact_text` duplication between `ChatContextAssembler` and `ApprovedPatchContextService` is low-risk refactor debt only.
    - N03 `ApprovedPatchContext.status` reuses a broader existing status type than strictly necessary. This is imprecise but harmless in current scope.
    - N04 per-call `ApprovedPatchContextService()` instantiation inside `assemble()` is low-impact for the current offline workflow.
    - N05 handoff wording about missing committed tests was inaccurate; Captain governance sync corrects that record rather than treating it as an implementation defect.
    - N06 carrying `supporting_cluster_ids` through compact briefs is safe because they are deterministic labels and not raw feedback content.
  - Deferred:
    - M01 explicit frozen/archived exclusion coverage is still missing. Carry forward under R054 as a remaining T164 coverage gap.
    - M02 no end-to-end `ChatContextAssembler` integration test yet exercises the approved-patch path. Carry forward under R054 as a remaining T164 coverage gap.
    - M03 no committed test yet covers empty or whitespace-only `behavior_instruction` through the full approved-patch load flow. Carry forward under R054 as a remaining T164 coverage gap.
  - Rejected: none.
- Conditions carried forward:
  - M5 remains review-only and approval-gated in meaning even though compact patch hints now exist in `ChatContext`.
  - Future work must not reinterpret approved patch context as automatic learning or hidden state mutation.
  - T170 must be design-only and must preserve compatibility with the current ContactSkill-centered pipeline.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T164 to T170, and the T170 task package is tightened so the next worker step is explicit and non-breaking.

## D035: T163 PASS_WITH_WARNINGS, accept task, advance to T164

- Date: 2026-05-22
- Status: Accepted
- Context: `docs/review/T163_review.md` gives `PASS_WITH_WARNINGS` for the manual patch review CLI. No blocking issues were found.
- Decision: T163 is complete. The project may continue to T164 Approved Patch Compact Context.
- Warning handling:
  - Accepted:
    - N05 `.claude/settings.json` modification is treated as workspace noise rather than a T163 scope violation.
  - Deferred:
    - N01 `docs/data_contracts/preference_patch_contract.md` still overclaims deterministic `patch_id` behavior even though `patch_id` is UUID-based. Carry forward under R053 until a later task corrects the contract or changes the id strategy.
    - N02 no committed automated tests yet cover `PatchReviewService` or `chat-feedback-review-patch`. Carry forward under R054 until a later hardening task adds deterministic review-layer regression coverage.
    - N03 review writes back to the input file by default when `--output` is not specified. Carry forward as R057 until a later task adds safer non-destructive write behavior or explicit atomic write handling.
    - N04 `review_metadata.history` grows without a cap across repeated review cycles. Carry forward as R058 until a later task defines retention or compaction behavior.
  - Rejected: none.
- Conditions carried forward:
  - T164 must remain approved-only, privacy-safe, compact, and non-mutating.
  - T164 must consume only patches where `status == "approved"` and `is_runtime_ready() == True`.
  - T164 must preserve review history and review metadata without clearing, rewriting, or flattening them into raw runtime text.
  - No automatic ContactSkill/Memory mutation, outbound sending, realtime integration, or LLM use is authorized by this decision.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T163 to T164, and the T164 task package is tightened so the next worker step is explicit and review-safe.

## D034: T162 PASS_WITH_WARNINGS, accept task, advance to T163

- Date: 2026-05-18
- Status: Accepted
- Context: `docs/review/T162_review.md` gives `PASS_WITH_WARNINGS` for the deterministic patch proposal CLI. No blocking issues were found.
- Decision: T162 is complete. The project may continue to T163 Patch Review CLI.
- Warning handling:
  - Accepted:
    - N05 `.claude/settings.json` modification is treated as workspace noise rather than a T162 scope violation.
  - Deferred:
    - N01 `docs/data_contracts/preference_patch_contract.md` still overclaims deterministic `patch_id` behavior even though `patch_id` is UUID-based. Carry forward under R053 until a later task corrects the contract or changes the id strategy.
    - N02 raw `input_path` still appears in proposal stdout/output. Carry forward under the already-active project-wide path-handling/privacy risk R043.
    - N03 no committed automated tests yet cover `PatchProposalService` or `chat-feedback-propose-patch`. Carry forward as R054 until a later hardening task adds deterministic proposal regression coverage.
    - N04 malformed cluster input with empty `contact_id` can still crash proposal generation instead of being skipped defensively. Carry forward as R056 until a later task adds an explicit guard.
  - Rejected: none.
- Conditions carried forward:
  - T163 must remain manual-review-only, candidate-only, privacy-safe, and non-mutating.
  - T163 must not reinterpret approved review status as runtime injection; T164 remains the first task allowed to read approved patches into compact context.
  - T163 must preserve `supporting_feedback_ids`, `supporting_cluster_ids`, and review metadata/history without editing proposal semantics or inventing new evidence.
  - No automatic ContactSkill/Memory mutation, outbound sending, realtime integration, or LLM use is authorized by this decision.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T162 to T163, and the T163 task package is tightened so the next worker step is explicit and review-safe.

## D033: T161 PASS_WITH_WARNINGS, accept task, advance to T162

- Date: 2026-05-18
- Status: Accepted
- Context: `docs/review/T161_review.md` gives `PASS_WITH_WARNINGS` for the deterministic feedback clusterer. No blocking issues were found.
- Decision: T161 is complete. The project may continue to T162 Patch Proposal CLI.
- Warning handling:
  - Accepted:
    - N01 `reason_tag_summary` is a slightly misleading field name because it aggregates `boundary_label` values, but the contract and implementation remain explicit enough for current scope and no data is lost.
    - N03 `counts_by_approach_label` may silently degrade to empty when plan files are unavailable. This is acceptable because the field is optional enrichment rather than required evidence.
    - N05 `.claude/settings.json` modification is treated as workspace noise rather than a T161 scope violation.
  - Deferred:
    - N02 no committed automated tests yet cover `FeedbackClusterService` or `chat-feedback-cluster`. Carry forward as R052 until a later hardening task adds deterministic cluster regression coverage.
    - N04 raw `input_path` still appears in cluster stdout/output. Carry forward under the already-active project-wide path-handling/privacy risk R043.
  - Rejected: none.
- Conditions carried forward:
  - T162 must remain deterministic, candidate-only, privacy-safe, and non-mutating.
  - T162 must consume cluster outputs conservatively and skip ambiguous or unlabeled clusters rather than speculating.
  - T162 must enforce non-empty `supporting_feedback_ids`, preserve `supporting_cluster_ids`, and keep `positive_examples` / `negative_examples` limited to safe summaries or references only.
  - No automatic ContactSkill/Memory mutation, outbound sending, realtime integration, or LLM use is authorized by this decision.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T161 to T162, and the T162 task package is tightened so the next worker step is explicit and review-safe.

## D032: T160 PASS_WITH_WARNINGS, accept task, advance to T161

- Date: 2026-05-18
- Status: Accepted
- Context: `docs/review/T160_review.md` gives `PASS_WITH_WARNINGS` for the schema-only PreferencePatch candidate contract. No blocking issues were found.
- Decision: T160 is complete. The project may continue to T161 Feedback Clusterer.
- Warning handling:
  - Accepted:
    - N01 `instruction_scope` remains a free-form string at schema stage. This is acceptable while actual clustering/proposal usage is still unknown and R047 already tracks possible later tightening.
    - N04 `schema_version` remains a plain string. This matches existing model/store conventions and is not worth special-case validation in T160 alone.
    - N05 broader working-tree modifications are treated as a repository hygiene note rather than a T160 scope violation, because the task-specific implementation change stays within the allowed model/contract surface.
  - Deferred:
    - N02 `positive_examples` and `negative_examples` are not structurally constrained to safe-only summaries/references. Carry forward as R048 until T162 enforces safe content generation.
    - N03 no committed automated tests yet cover `PreferencePatchCandidate` validation. Carry forward as R049 until a later hardening task adds model-level regression coverage.
  - Rejected: none.
- Conditions carried forward:
  - T161 must remain deterministic, aggregate-only, privacy-safe, and non-mutating.
  - T161 must not generate `PreferencePatchCandidate` records yet; it only prepares stable clustered evidence for T162.
  - No automatic ContactSkill/Memory mutation, outbound sending, realtime integration, or LLM use is authorized by this decision.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T160 to T161, and the T161 task package is tightened to preserve the candidate-only M5 sequencing.

## D031: T152 PASS_WITH_WARNINGS, complete M4.5, authorize T160

- Date: 2026-05-18
- Status: Accepted
- Context: `docs/review/T152_review.md` gives `PASS_WITH_WARNINGS` for the committed feedback CLI regression suite. No blocking issues were found. T150/T151/T152 now cover planner, direct policy, and feedback CLI behavior from committed synthetic tests.
- Decision: T152 is complete. M4.5 regression hardening is complete. The project may enter M5, beginning with T160 PreferencePatch Schema.
- Warning handling:
  - Accepted:
    - N03 `--validation-report` CLI wiring is not covered by a dedicated Typer end-to-end test, but the service-level merge behavior is directly regression-tested and adequate for this task scope.
    - N04 there is no single append->validate->summarize pipeline test yet, but the three services and CLI entry points are all covered directly enough to accept the task.
    - N05 `test_approach_labels_loaded` is intentionally brittle as a regression guard and acceptable.
  - Deferred:
    - N01 validation `record_results` still has no bounded-size guarantee on large logs. Carry forward as R045 until a future task either bounds it or formally accepts the verbosity envelope.
    - N02 service-level output-path confinement is still convention/warning-based rather than hard-enforced. Carry forward as R043.
  - Rejected: none.
- Conditions carried forward:
  - M5 remains review-only and candidate-only.
  - T160 must define schema/contracts only; it must not generate, approve, apply, or inject patches.
  - No automatic ContactSkill/Memory mutation, outbound sending, realtime integration, or LLM use is authorized by this decision.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T152 to T160. `docs/review/M4_5_review.md` is created as the milestone-level authorization review.

## D030: T151 PASS_WITH_WARNINGS, accept task, advance to T152

- Date: 2026-05-18
- Status: Accepted
- Context: `docs/review/T151_review.md` gives `PASS_WITH_WARNINGS` for the committed policy fixture suite. No blocking issues were found.
- Decision: T151 is complete. The project may continue to T152 Feedback CLI Regression Tests.
- Warning handling:
  - Accepted:
    - N01 the final conservative fallback branch in `_candidate_is_over_proactive` is not independently covered, but the branch is behaviorally redundant with already-tested proactive detection logic.
    - N02 confidence-penalty coverage is not exhaustive across every additive combination, but the component penalties and a representative combined case are already deterministic and sufficient for this task scope.
    - N03 the baseline fixture contamination found by T151 is a positive correction, not a remaining defect; direct policy-engine tests successfully exposed and fixed the issue.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T152 remains required before M5 because the feedback CLI loop is still not regression-hardened from committed repo contents alone.
  - T152 should emphasize privacy-safe stdout, corrupted-log surfacing, compact validation behavior, non-mutation guarantees, and aggregate summary behavior.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T151 to T152.

## D029: T150 PASS_WITH_WARNINGS, accept task, advance to T151

- Date: 2026-05-18
- Status: Accepted
- Context: `docs/review/T150_review.md` gives `PASS_WITH_WARNINGS` for the committed ReplyPlanner regression test task. No blocking issues were found.
- Decision: T150 is complete. The project may continue to T151 Policy Fixture Suite.
- Warning handling:
  - Accepted:
    - N01 `TestNotConfiguredPath` overlaps with the `thin_context` fixture but still asserts a distinct invariant.
    - N02 policy-layer behavior is still exercised indirectly through `ReplyPlanner`; direct `ReplyPlanPolicyEngine` unit coverage is better treated as T151 scope.
    - N03 `practical` summary wording assertion is intentionally fragile as a regression guard.
    - N04 false-negative probes intentionally assert current missed-detection behavior as a documented limitation.
    - N05 helper constructors are simple enough that missing isolated unit tests is low risk.
    - N06 `notes_on_candidate_differences` is not yet asserted, but this is informational rather than safety-critical.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - T151 should add more explicit policy-fixture coverage, including direct `ReplyPlanPolicyEngine` expectations where helpful.
  - T151 should consider separating missing-store-path coverage more clearly from thin-context coverage.
  - T151 should consider adding assertions for `notes_on_candidate_differences`.
  - T152 remains required before M5 because the feedback CLI loop is not yet regression-hardened.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T150 to T151.

## D028: Gate M4 Conditional, enter T150 instead of M5

- Date: 2026-05-17
- Status: Accepted
- Context: `docs/review/M4_review.md` judges M4 feedback capture as functionally complete but not yet clean-environment reproducible.
- Decision: Gate M4 is `Conditional`. The project may proceed only to M4.5 regression hardening, beginning with T150 ReplyPlanner Regression Tests.
- Reasoning:
  - T140/T141/T142 provide the intended M4 read-only flow: record, validate, and summarize feedback.
  - No blocking pseudo-completion was found.
  - Clean-environment proof is still missing because committed tests and committed synthetic fixtures do not yet cover M3/M4 behavior.
  - M5 feedback-to-patch remains unauthorized until T150-T152 reduce this reproducibility gap.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T142 to T150.

## D027: T142 PASS_WITH_WARNINGS, accept task, complete M4 functional scope

- Date: 2026-05-17
- Status: Accepted
- Context: `docs/review/T142_review.md` gives `PASS_WITH_WARNINGS` for the feedback summary exporter task. No blocking issues were found.
- Decision: T142 is complete. M4 functional scope is now present: feedback can be recorded, validated, and summarized in a review-only, privacy-safe flow.
- Warning handling:
  - Accepted:
    - N01 duplicated `_resolve_plan_path` / `_load_plan_safe` helpers. Low-risk refactor debt only.
    - N02 raw `input_path` appears in stdout. Style inconsistency only.
    - N03 aggregate presence counts may reveal low-risk existence patterns. Acceptable for the current offline single-user tool.
    - N04 unreadable input can still produce an output artifact describing the failure. Acceptable current behavior.
    - N05 summary returns an untyped `dict`. Consistent with current M4 style.
    - N06 no `reason_tag` / `policy_risk_flag` aggregation because those fields do not exist in the current record schema.
  - Deferred: none.
  - Rejected: none.
- Conditions carried forward:
  - M4 remains review-only and non-mutating.
  - M4 is complete for scope, not yet sufficient for M5.
  - T150-T152 remain responsible for committed reproducibility coverage.
- Impact: T142 closes the implementation side of M4 and hands off to Captain milestone review.

## D025: T140 PASS_WITH_WARNINGS, accept task, advance to T141

- Date: 2026-05-17
- Status: Accepted
- Context: `docs/review/T140_review.md` gives `PASS_WITH_WARNINGS` for the feedback schema + CLI task. No blocking issues were found.
- Decision: T140 is complete. The project may continue to T141 Feedback Log Validator.
- Warning handling:
  - Accepted:
    - N03 `_count_records` re-reads the whole log after append. Low-impact inefficiency only.
    - N04 `reply_plan_id` currently proxies `approved_contact_skill_record_id`. Acceptable because `ReplyPlan` has no dedicated stable `plan_id` yet.
    - N06 `ReplyFeedbackAction` uses `Literal[...]` rather than an enum. Consistent with current project patterns.
  - Deferred:
    - N01 corrupted log file can be silently replaced, causing possible data loss. Carry into T141/R042.
    - N02 `source_plan_path` may be absolute or relative and can become stale after moves. Carry into T141-or-later/R043.
    - N05 CLI/service do not enforce private path confinement on `--output`. Carry into T141/T152/R043.
  - Rejected: none.
- Conditions carried forward:
  - M4 stays capture/validate/summary only.
  - T141 must remain read-only and must not mutate feedback logs, ContactSkill, MemoryFact, approved stores, planner templates, or outbound behavior.
  - T150/T152 remain responsible for committed regression coverage.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T140 to T141.

## D026: T141 PASS_WITH_WARNINGS, accept task, advance to T142

- Date: 2026-05-17
- Status: Accepted
- Context: `docs/review/T141_review.md` gives `PASS_WITH_WARNINGS` for the feedback log validator task. No blocking issues were found.
- Decision: T141 is complete. The project may continue to T142 Feedback Summary Exporter.
- Warning handling:
  - Accepted:
    - N01 raw `input_path` appears in CLI output. Low-risk style inconsistency only.
    - N03 `_is_private_path` uses a coarse directory-name heuristic. Acceptable for MVP.
    - N04 `_resolve_plan_path` depends on CWD for relative paths. Acceptable with the current private/offline workflow.
    - N05 `strict_mode` is stored in the report but not read by the service. Minor dead data only.
  - Deferred:
    - N02 `reply_plan_id` coherence is not cross-checked against the loaded plan context. Carry into T142 if the summary needs to surface it.
    - N06 `record_results` may grow large on bigger logs. Carry into T142 as a compact-output concern.
  - Rejected: none.
- Conditions carried forward:
  - M4 stays capture/validation/summary only.
  - T142 must remain aggregate-only and privacy-safe.
  - T150/T152 remain responsible for committed regression coverage.
- Impact: `docs/04_task_board.md` moves the Current Unique Task from T141 to T142.

## D023: T133 PASS_WITH_WARNINGS, Gate M3 Conditional, enter T140

- Date: 2026-05-16
- Status: Accepted
- Context: `docs/review/T133_review.md` gives `PASS_WITH_WARNINGS` for the T133 holdout eval. `docs/review/M3_review.md` confirms Gate M3 = `Conditional`.
- Decision: T133 is complete. M3 may proceed to M4/T140 only under review-only constraints.
- Warning handling: T133 N01/N02/N03/N04/N05 are all accepted. No T133 warnings are deferred or rejected.
- Conditions:
  - ReplyPlanner remains review-only. No auto-send, realtime platform integration, or LLM drafting expansion.
  - T150 must add committed regression tests for structure, boundary sensitivity, thin context, false positives, subtle false negatives, privacy leakage, contact alignment, and ranking.
  - Do not claim relationship-aware maturity until broader sample recalibration.
- Impact: Current Unique Task becomes T140 Feedback Schema CLI. T140 records human feedback only; it must not automatically update ContactSkill/Memory or send messages.

## D024: Adopt updated GPT roadmap as staged backlog, revise M4+

- Date: 2026-05-16
- Status: Accepted
- Context: `docs/reference/gpt的后续设计思路(更新版).md` was reviewed against current project state: M3 is `Conditional`, T140 is current, and the project remains offline-first/review-only.
- Decision: Adopt the roadmap's strategic direction but revise milestone/task ordering to preserve the current safety architecture.
- Adopted changes:
  - M4 is narrowed to feedback capture, validation, and safe summary only.
  - M4.5 is added for committed ReplyPlanner/policy/feedback regression tests.
  - Feedback-to-patch moves after regression hardening.
  - ContactSkill decomposition becomes compatible projection, not replacement.
  - LLM-assisted ReplyPlanner, RelationshipState, MemoryRetriever, BehaviorPlanner, Feishu, and WeChat are delayed behind tests and review gates.
- Rejected for immediate execution:
  - Direct Mem0 integration.
  - Direct Feishu/WebSocket/platform integration.
  - Direct ContactSkill deletion/replacement.
  - Automatic learning, automatic sending, or proactive behavior.
- Impact: `docs/04_task_board.md` and task packages under `docs/tasks/` were updated to reflect the staged roadmap. Current Unique Task remains T140.

更新日期：2026-05-15

## D001: 下一阶段以微信主线为优先

- 日期：2026-05-13
- 状态：Superseded
- 背景：上一版计划认为应优先验证 WeChatBot/iLink，再接入微信主流程。
- 原决策：按 `Sprint 0 -> Sprint 7` 推进微信 iLink/扫描/投递路线。
- 被取代原因：T01 登录/session 验证被 BLOCK，且用户已通过 WeFlow 成功导出聊天记录，不再需要扫描或实时接入作为当前主线。

## D002: WeChatBot/iLink SDK 先做仓库外隔离 POC

- 日期：2026-05-13
- 状态：Paused
- 背景：非官方或半官方 SDK 可能有稳定性、账号和接口风险。
- 原决策：Sprint 0 不修改主仓库业务代码，先仓库外验证登录、收消息、reply、媒体和 `context_token`。
- 当前结果：T00 安装和二维码阶段 review `PASS`；T01 登录/session review `BLOCK`。
- 新决策：不修 T01，不继续 iLink 登录验证。相关记录保留为历史，不作为当前开发阻塞项。

## D003: 出站消息默认 human-in-the-loop

- 日期：2026-05-13
- 状态：Accepted
- 背景：聊天 agent 涉及真实社交关系，误发送和越界回复风险高。
- 决策：当前阶段只生成草稿和 review artifact，不自动发送。未来若恢复投递功能，必须经过 `PolicyEngine` 和人工审批。
- 影响：新路线的 ReplyPlanner 只输出候选草稿、rationale 和 risk flags。

## D004: 治理文档采用 AI coding workflow

- 日期：2026-05-13
- 状态：Accepted
- 背景：用户要求像新项目一样建立 00-08 文档，并给出可指导 worker 的 `04_task_board.md`。
- 决策：所有开发以 `Current Unique Task` 和 `docs/tasks/` 任务包为准。
- 影响：路线切换后，旧任务保留为 paused legacy，新任务从 T100 开始。

## D005: T00 review 通过，曾推进到 T01

- 日期：2026-05-13
- 状态：Historical
- 背景：`docs/review/T00_review.md` 给出 `PASS`，确认 SDK 安装、导入、构造和二维码阶段探测真实有效。
- 决策：T00 标记完成。
- 当前影响：仅作为旧 iLink 路线历史证据，不再驱动主线。

## D006: 路线切换到 WeFlow 离线蒸馏 MVP

- 日期：2026-05-13
- 状态：Accepted
- 背景：用户已通过 WeFlow 工具提取聊天记录并存放在 `private/chat_history/`。`docs/review/T01_review.md` 的 BLOCK 主要来自未完成扫码登录，但用户明确希望跳过整个微信聊天记录扫描/SDK路线。
- 决策：暂停 iLink/扫描主线，直接进入基于 WeFlow JSONL 的长期关系感知 chat agent 设计与实验。
- 当前唯一任务：T100 WeFlow JSONL schema profiling 与 normalized event 合约。
- 影响：`02_experiment_plan.md`、`04_task_board.md` 和 00-08 治理文档已按新路线更新。

## D007: 当前阶段不做微调、实时接入、自动发送

- 日期：2026-05-13
- 状态：Accepted
- 背景：两份新设计文档都强调 Memory + ContactSkill + RAG/Skill 的解耦架构，而不是把隐私事实写进模型权重。
- 决策：M0-M1 只做离线解析、切块、摘要、事实抽取、ContactSkill candidate 和人工 review。
- 影响：不引入 LoRA/DPO/微调，不恢复微信 SDK，不建立自动投递功能。

## D008: T100 review PASS，进入 T101 隐私与 source_ref 规则

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T100_review.md` 给出 `PASS`，确认 T100 已完成 WeFlow schema profile、normalized event contract 和安全脱敏 fixture，且未越界实现 chunker、LLM、数据库或实时微信接入。
- 决策：T100 标记完成；当前唯一任务切换为 T101。
- Warning 处理：N01 accepted，Q100/Q104 关闭依据更新为 “T100 worker draft + review PASS”；N02 deferred 到 T102/T150 处理 type=80/chatRecords fixture 覆盖；N03 deferred 到 T102 决定 `event_id` 是否从 SHA-1 升级或补充 SHA-256。
- 影响：下一步先固定隐私脱敏规则和 source_ref/raw_ref 规则，再允许实现最小 normalize CLI。

## D009: T101 review PASS，进入 T102 最小 normalize CLI

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T101_review.md` 给出 `PASS`，确认隐私脱敏规则、source_ref/raw_ref 规则和补充 source_ref 预览形态的合成 fixture 均满足任务要求，且未修改 `src/**`、未复制真实原文、未实现脱敏器或 LLM 流程。
- 决策：T101 标记完成；当前唯一任务切换为 T102。
- Warning 处理：N01 deferred，继续由 T102/T150 补充 `type=80` 和 `chatRecords` 合成 fixture；N02 accepted，preview hex 值作为 fixture 注释可接受，不要求返修；N03 deferred，T102 实现时校验结构化替换 token 与实际脱敏需求是否对齐。
- 影响：T102 worker 必须遵守 `privacy_redaction_rules.md` 的 Field Handling Matrix 和 `source_ref_rules.md` 的 Allowed Public Shape，且所有 normalize 输出只能落入 `private/distilled/`。

## D010: T102 review PASS，进入 T103 M0 review

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T102_review.md` 给出 `PASS`，确认 `chatlog-normalize` CLI 可运行，输入限制在 `private/chat_history/`，输出限制在 `private/distilled/`，stdout/report 不泄露真实原文、真实文件名、真实联系人或真实平台 ID。
- 决策：T102 标记完成；当前唯一任务切换为 T103 M0 review。
- Warning 处理：N01 deferred 到 T103/T150 评估 timezone fallback warning；N02/N03 deferred 到 T110/T150 考虑流式处理与内存写入；N04 accepted，系统消息关键词作为 MVP 兜底可接受；N05 deferred 到 T112+ 蒸馏阶段处理 PII token 替换；N06 deferred 到 T114/T150 验证单文件 sender_role 稳健性。
- 影响：下一步不直接进入 M1 worker 实现，而是先做 T103 gate review，决定 M0 是否 `Allow`、`Conditional` 或 `Block`。

## D011: T103 Gate M0 Conditional，进入 T110

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T103_milestone_review.md` 已汇总 T100-T102 的产物与 review 结论；`docs/review/T103_review.md` 接受 worker 草案，确认 Gate M0 = `Conditional`。T100/T101/T102 均已 reviewer `PASS`，M0 硬性条件已满足，但仍有若干明确记录的非阻塞问题需要带入 M1。
- 决策：Gate M0 = `Conditional`；允许进入 M1，当前唯一任务切换为 T110 conversation chunker v0。
- 条件：
  - T110/T150 继续覆盖 `type=80` / `chatRecords` 的保守处理与测试。
  - T110/T114/T150 保留并验证 `sender_role`、timezone fallback、性能/内存相关不确定性。
  - T112+ 任意 LLM-facing 蒸馏步骤继续遵守 T101 的隐私边界，不把私有 normalize 文本直接扩散到可提交产物。
- 影响：T110 worker 可以启动，但必须承接 M0 条件，尤其是保留不确定性信号、避免私密内容进入可提交目录，并为 T112+/T114/T150 留出验证路径。

## D012: T110 review PASS，进入 T111 蒸馏 schema

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T110_review.md` 给出 `PASS`，确认 `ConversationChunkingService` 和 `chatlog-chunk` CLI 已完成 conversation chunker v0，输出限制在 `private/distilled/`，未引入 LLM、embedding、ContactSkill、数据库或实时平台接入。
- 决策：T110 标记完成；当前唯一任务切换为 T111 Distillation Schemas。
- Reviewer non-blocking issues 处理：因 verdict 为 `PASS`，不要求 worker 返修；N01/N02/N03 作为 accepted observations 进入后续实现注意事项；N04 deferred 到 T150 自动化测试；N05 accepted，`topic_hint` 保持 optional，不阻塞 T111。
- 影响：T111 必须在 T112 引入 LLM-facing 抽取前定义 ChunkSummary、MemoryFactCandidate、ContactSkillCandidate 的强 schema、JSON contract、evidence_refs 和反 impersonation/数字克隆边界。

## D013: T111 review PASS，进入 T112 摘要与事实抽取

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T111_review.md` 给出 `PASS`，确认 `ChunkSummary`、`MemoryFactCandidate`、`ContactSkillCandidate` 及辅助 schema 已在 `core.models` 中定义，`docs/data_contracts/distillation_output_contract.md` 已固定 JSON contract、状态/敏感度约定和 anti-impersonation 边界。
- 决策：T111 标记完成；当前唯一任务切换为 T112 Summary And Fact Extraction。
- Reviewer non-blocking issues 处理：N01 accepted，关系/沟通风格字段保留自由字符串以适配 MVP LLM 输出；N02 accepted/deferred，`redaction_policy` 字典形态当前可接受，后续可在 T120/T150 收紧；N03 deferred 到 T120 处理 `DistillationMemoryType` 与现有 `MemoryType` 映射；N04 deferred 到 T120 store 补充 `created_at` / `updated_at`；N05 deferred 到 T150 增加 Pydantic 约束测试。
- 影响：T112 可以启动，但必须把 LLM 输出校验为 T111 schema，缺失 `evidence_refs`、`confidence`、`sensitivity` 或 `status` 的输出一律视为无效；不得把私密原文或 LLM 原始输入输出写入可提交目录。

## D014: T112 review PASS，进入 T113 ContactSkill builder

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T112_review.md` 给出 `PASS`，确认 `ChatlogDistillationService` 和 `chatlog-distill` CLI 已能在小样本上消费 T110 chunks/T102 normalized events，调用 OpenAI-compatible LLM，并在写入前完成 provider 输出归一化、T111 schema 校验和 evidence refs 范围校验。
- 决策：T112 标记完成；当前唯一任务切换为 T113 ContactSkill builder 与 Markdown review exporter。
- Reviewer non-blocking issues 处理：N01 deferred 到 T114 关注 evidence refs 粒度；N02 deferred 到 T114/T150 关注 provider shape drift；N03 accepted/deferred，MVP sensitivity 关键词兜底可接受，后续 T150 可补测试；N04 accepted/deferred，memory_type fallback 可接受，T114/T150 观察误分类；N05 accepted，`contact_skill.py` 轻量辅助不越界；N06 deferred 到 T150 自动化测试；N07 accepted/deferred，T112 已在 prompt 层部分实现 PII token 替换，后续隐私测试继续覆盖。
- 影响：T113 可以消费 `chunk_summaries.jsonl` 和 `memory_facts.jsonl` 生成 `contact_skill.candidate.json` 与 `contact_skill.review.md`；仍不得自动 approve、不得保存大段原文、不得生成“模拟联系人说话”的内容。

## D015: T113 review PASS_WITH_WARNINGS，进入 T114 MVP sample run

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T113_review.md` 给出 `PASS_WITH_WARNINGS`，确认 `ContactSkillBuilderService` 和 Markdown exporter 已能消费 T112 outputs，生成 `contact_skill.candidate.json` 与 `contact_skill.review.md`，candidate 保持 `status="candidate"`，保留 evidence refs，且没有自动 approve、冒充联系人、数据库 migration、实时平台接入或自动发送。
- 决策：T113 标记完成；当前唯一任务切换为 T114 Run MVP Sample。
- Warning 处理：N01 accepted，重复 `_build_report()` 仅为低影响重复工作；N02 deferred 到 T114/T120+，小样本启发式 token/topic/relationship 推断需要在不同或更大样本上验证；N03 deferred 到 T114/T120+，formulaic confidence/relationship 数值需要人工检查是否显得过度精确；N04 accepted，缺少 `exporters/__init__.py` 不影响当前运行；N05 accepted，未使用 helper 无当前风险。
- 影响：T114 必须抽查至少 5 条 memory facts 的 evidence 支持度，并额外关注 T113 启发式泛化、confidence 数值可信度、topic 提取覆盖率和 review artifact 是否仍适合人工审阅。

## D016: Gate M1 Conditional，进入 M2/T120

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T114_review.md` 给出 `PASS_WITH_WARNINGS`，确认 worker 的 Gate M1 verdict = `Conditional`；`docs/review/M1_review.md` 作为 Captain 综合审查，同样确认 M1 可条件进入 M2。
- 决策：T114 标记完成；Gate M1 = `Conditional`；当前唯一任务切换为 T120 File Store Models。
- Warning 处理：T114 N01/N02 accepted，candidate-only fact 的轻微语义上提由 human review 兜底；T114 N03 accepted，样本过小是结构限制并由 `Conditional` verdict 表达；T114 N04 accepted，不要求补查 report 字段。新增 R030 继续跟踪 paraphrase compression。
- 条件：
  - M2 必须保持 candidate-only / human-review-first，不得把 candidate 或 rejected/frozen 内容直接注入 runtime prompt。
  - T120 必须保留 status 与 evidence refs，并不得引入数据库 migration 或向量库。
  - R028/R029/R030 必须继续活跃到更广样本或后续 store/review 机制能缓解为止。
- 影响：允许进入 M2，但不得把 M1 写成无条件成功；T120 是文件 store 与模型稳定化任务，不是 runtime integration。

## D017: T120 review PASS_WITH_WARNINGS，进入 T121

- 日期：2026-05-14
- 状态：Accepted
- 背景：`docs/review/T120_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T120 已完成离线 memory/skill 文件 store、review metadata、source metadata、legacy artifact wrapping 和 human-review-first `is_runtime_ready()` gate；未引入 CLI、数据库 migration、向量库、runtime prompt 注入或自动 approve。
- 决策：T120 标记完成；当前唯一任务切换为 T121 Evidence Validator。
- Warning 处理：N01 accepted，`updated_at` no-op normalization 不影响正确性，T122 更新 review 状态时再明确 timestamp 语义；N02 accepted，两个 service 间 path/helper duplication 对 MVP 可接受，暂不抽基类；N03 accepted，single-record store shape 兼容入口由 Pydantic 校验兜底；N04 accepted，`DistillationMemoryType` 到 runtime `MemoryType` 的粗粒度映射符合 MVP；N05 deferred 到 T150，需补 store model validation、legacy wrapping、load/save round-trip、runtime-ready gate 和 path confinement 自动化测试。
- 影响：T121 必须只做 evidence validator 与 rejected/frozen 状态规则，不做 approve CLI、runtime integration、数据库或向量库；missing refs 必须阻止 approval。

## D018: T121 review PASS_WITH_WARNINGS，进入 T122

- 日期：2026-05-15
- 状态：Accepted
- 背景：`docs/review/T121_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T121 已完成 read-only evidence validator、`chatlog-validate-evidence` CLI、same-run evidence index、nested `evidence_refs` collection、status gate 和 missing-ref approval/runtime blocking；未自动 approve、未做 review/approve CLI、未接数据库、向量库或 runtime prompt。
- 决策：T121 标记完成；当前唯一任务切换为 T122 Skill Review CLI。
- Warning 处理：N01 accepted，当前 schema 没有 stable contact skill artifact id，fallback 到 `contact_id` 不影响正确性；N02 accepted/deferred，JSON/JSONL helper 第三次重复对 MVP 可接受，若 T150 或后续重构统一文件 IO 可一并处理；N03 accepted，递归扫描全 payload 的性能对当前数据量无风险；N04 accepted，validator read-only 不写回 store 是正确设计，T122 决定是否写入 `review_metadata.evidence_validation_status`；N05 deferred 到 T150，需补 evidence index、nested refs、status rules、missing refs blocking、human review gate interaction 和 path confinement 自动化测试。
- 影响：T122 必须把 T121 validation report 作为 approve gate；不得在 missing refs、candidate-only 或未人工审阅情况下绕过 approval/runtime 安全边界。

## D019: T122 review PASS_WITH_WARNINGS，进入 T123

- 日期：2026-05-15
- 状态：Accepted
- 背景：`docs/review/T122_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T122 已完成 `chatlog-review-store` CLI、`ContactSkillStoreReviewService`、approval gate、review metadata history、safe export 和 stable record_id；approve 需要 T121 report passed、目标 record present、0 missing refs、checked refs > 0，且拒绝 rejected/frozen/archived re-approval；未做 runtime integration、数据库、向量库、LLM 或自动发送。
- 决策：T122 标记完成；当前唯一任务切换为 T123 Context Integration。
- Warning 处理：N01 accepted，`del current_status` 是低影响接口/风格问题；N02 accepted，递归更新所有合法 `status` 字段符合当前 schema，未来 schema 若出现不同语义再重审；N03 accepted，`store_runtime_ready` 提前计算只是轻微 style note；N04 accepted/deferred，review service 访问 file store private helpers 对 MVP 可接受，未来可抽公共 file IO/path utility；N05 accepted，mutable `_StoreWorkspace` 当前局部可控；N06 deferred 到 T150，需补 approval gate、reject/freeze/archive flow、review metadata history、recursive status update、export path confinement、stable record_id 和 no-auto-approve 测试。
- 影响：T123 必须只读取 approved + runtime-ready store records，生成 compact `ChatContext` brief；不得注入 candidate/rejected/frozen/archived，不得把大段原文放入 prompt，不得实现 ReplyPlanner 或自动发送。

## D020: T130 review PASS_WITH_WARNINGS，进入 T131

- 日期：2026-05-15
- 状态：Accepted
- 背景：`docs/review/T130_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T130 已完成 ReplyPlan schema 与 prompt contract：支持 3+ candidates、per-candidate rationale / refs / risk flags / boundary reminders，兼容 T123 compact approved-store context，且没有引入 LLM 调用、发送逻辑、数据库、向量库或私密原文泄露。
- 决策：T130 标记完成；当前唯一任务切换为 T131 Relationship-Aware Reply Planner。
- Warning 处理：N01 accepted，单值 `ReplyPlanMode` 当前符合 review-only scope；N02 deferred 到 R034，T131 必须保证候选 `priority_rank` 稳定且不冲突；N03 accepted，`approach_label` 自由字符串对 MVP 可接受；N04 deferred 到 R034，T131 必须校验 `ReplyPlan.contact_id` 与 source context / T123 approved-store context 对齐。
- 影响：T131 可以实现 planner service/CLI，但必须继续保持 review-only、人类确认优先、只消费 approved + runtime-ready compact context，不得自动发送或绕过 T123/T130 的安全边界。

## D021: T131 review PASS_WITH_WARNINGS，进入 T132

- 日期：2026-05-16
- 状态：Accepted
- 背景：`docs/review/T131_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T131 已完成 review-only `ReplyPlanner` service 与 `chat-reply-plan` CLI：只消费 T123 compact approved-store context，输出 T130 `ReplyPlan`，包含 3 个结构可区分候选，并校验 `priority_rank` 唯一性与 `contact_id` 对齐；未引入自动发送、数据库、向量库、实时平台接入或私密原文读取。
- 决策：T131 标记完成；当前唯一任务切换为 T132 Reply Policy。M3 尚未完成，不能进入 M4。
- Warning 处理：N01 accepted/deferred，硬编码模板和浅层 relationship-awareness 进入 R035，由 T132/T133 继续约束和评估；N02 accepted，硬编码 confidence 在 contract-wiring MVP 可接受；N03 accepted/deferred，`strategy_hints` / `relationship_summary` 未参与草稿生成进入 R035；N04 deferred 到 R036，committed tests/fixtures 留给 T150，并由 T133 提供匿名化评估记录；N05 accepted，`_dedupe(values)` 类型注解缺失为低风险风格问题；N06 accepted，当前 enum fallback 足够支撑 MVP。
- 影响：T132 worker 只应补 policy/boundary 风险层，不重写 T131 planner 主流程，不进入 M4/T140，不实现自动发送或平台集成。

## D022: T132 review PASS_WITH_WARNINGS，进入 T133

- 日期：2026-05-16
- 状态：Accepted
- 背景：`docs/review/T132_review.md` 给出 `PASS_WITH_WARNINGS`，确认 T132 已在 `ReplyPlanner` 前后加入 policy/boundary 风险层：覆盖 `boundary_sensitive`、`over_proactive`、`impersonation_risk`、`thin_context`，保留 T131 的 review-only `ReplyPlan` contract、`priority_rank` 校验和 `contact_id` 对齐；未引入自动发送、数据库、向量库、实时平台接入或私密原文输出。
- 决策：T132 标记完成；当前唯一任务切换为 T133 Holdout Eval。M3 尚未完成，不能进入 M4。
- Warning 处理：N01 accepted，runtime text 仅用于 detection 且不 echo；N02 accepted，宽泛关键词已有 compound trigger 缓解；N03 accepted/deferred，substring matching false-positive 风险进入 R037，由 T133/T150 继续观察和测试；N04 accepted，`_dedupe` 重复是低风险重复；N05 deferred，T132 无 committed tests/fixtures 并入 R036；N06 accepted，重复分支无 correctness 影响；N07 accepted，approved memory claim 仅限量用于 detection，不进入输出 surface。
- 影响：T133 只做匿名 holdout eval 和 Gate M3 判断，不修改 planner 代码，不提交 holdout 原文，不进入 M4/T140。
