# Risks And Open Questions

## Captain Update 2026-05-29 (T231 Review Decision)

Authoritative current risk state after the Captain review of T231:

- R040 remains active as a compact-context and privacy boundary rule: M12 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, behavior candidates, outbound requests, gate decisions, adapter results, review cards, parsed review intents, and inbound provider events remain review/gate artifacts unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved and orthogonal to M12 deterministic/synthetic adapter-contract work.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- R093 remains active but narrowed: M11 separated outbound requests/gates/adapters/cards from `CandidateAction`; M12 must still avoid consuming `CandidateAction` review state as inbound or outbound platform authorization.
- R096 remains active and narrowed: M11 review/gate/adapter/card states remain distinct; T233 must keep provider eligibility separate from payload preparation, API acceptance, delivery, and failure-event mutation.
- R097 remains active: T221 named-timezone verification on Windows requires `tzdata`, which is not currently declared in project dependencies.
- R098 remains active: display preview truncation is useful for local summaries/cards but is not a privacy boundary for future real, sandbox, card-rendered, or WeChat-family payloads.
- R099 remains active: T223 Feishu sandbox payload shape has not been validated against current official Feishu production API semantics.
- R100 remains active: T224 Feishu review-card payload and synthetic action parser are local approximations, not validation of real Feishu callback/event semantics.
- R101 remains active: personal-WeChat scan/login/realtime SDK work and unofficial SDK vendoring remain blocked; T233 must not add personal-WeChat, scan-login, desktop automation, or unofficial SDK behavior.
- R102 remains active: official WeChat-family documentation may drift; T233 and later tasks must recheck official docs before relying on provider semantics.
- R103 remains active: WeCom Customer Service does not cleanly map to personal WeFlow chat contacts; T233 must treat recipients as explicit synthetic aliases only.
- R104 remains active: `channel_preference="wechat"` is too broad for production adapter selection; T233 must require explicit selected surface/config rather than treating broad channel preference as sufficient.
- R105 remains active: no live WeCom account, tenant, app, callback URL, credential flow, recipient mapping, service window, delivery callback, or provider failure handling has been tested.
- R106 is active: T231 timestamp fallback uses Unix epoch for missing/unparseable values; future live inbound/sync work must distinguish invalid timestamps from real 1970 timestamps.
- R107 is active: T231 parses only the first `msg_list` item because the current inbound connector returns one event per call; future live `sync_msg` work needs explicit batching semantics.
- R108 is active: T231 carries synthetic raw payloads into `InboundEvent.raw`; future live adapter work must define redaction before storing real provider payloads or IDs.
- T231 opened no deferred task-review risks. Its non-blocking observations are accepted as synthetic-scope limitations or minor coverage-strength notes under a `PASS` verdict.
- M12 is still conditional only. This does not authorize live WeChat/WeCom callbacks, polling, credentials, outbound delivery, or automatic sending.

Closed question Q204: T231 is accepted with `PASS`, so the WeCom Customer Service synthetic inbound contract is complete and the project may proceed to T233 provider safety.

Open question Q205: Can T233 define a deterministic local WeCom Customer Service provider safety gate that blocks unsafe outbound eligibility before any payload preparation or delivery?

## Captain Update 2026-05-28 (T230 Review Decision / M12 Conditional)

Authoritative current risk state after the Captain review of T230:

- R040 remains active as a compact-context and privacy boundary rule: M12 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, behavior candidates, outbound requests, gate decisions, adapter results, review cards, parsed review intents, and inbound provider events remain review/gate artifacts unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved and orthogonal to M12 deterministic/synthetic adapter-contract work.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- R093 remains active but narrowed: M11 separated outbound requests/gates/adapters/cards from `CandidateAction`; M12 must still avoid consuming `CandidateAction` review state as inbound or outbound platform authorization.
- R096 remains active and narrowed: M11 review/gate/adapter/card states remain distinct; T231 must not introduce runtime ingestion or delivery state as a side effect of inbound parsing.
- R097 remains active: T221 named-timezone verification on Windows requires `tzdata`, which is not currently declared in project dependencies.
- R098 remains active: display preview truncation is useful for local summaries/cards but is not a privacy boundary for future real, sandbox, card-rendered, or WeChat-family payloads.
- R099 remains active: T223 Feishu sandbox payload shape has not been validated against current official Feishu production API semantics.
- R100 remains active: T224 Feishu review-card payload and synthetic action parser are local approximations, not validation of real Feishu callback/event semantics.
- R101 remains active but narrowed: T230 blocked paused personal-WeChat scan/login/realtime SDK work and unofficial SDK vendoring; T231 must preserve that block.
- R102 is active: official WeChat-family documentation may drift; T231 and later tasks must recheck official docs before relying on API, callback, credential, quota, or service-window facts.
- R103 is active: WeCom Customer Service does not cleanly map to personal WeFlow chat contacts; T231 must treat provider identities as synthetic contract aliases only, not contact mapping.
- R104 is active: `channel_preference="wechat"` is too broad for production adapter selection; future outbound work needs an explicit selected surface/subchannel or adapter config before any send path.
- R105 is active: no live WeCom account, tenant, app, callback URL, credential flow, recipient mapping, service window, delivery callback, or provider failure handling has been tested.
- T230 opened no deferred task-review risks. Its non-blocking observations are accepted as documentation freshness, research depth, surface-selection, and schema-overbreadth notes under a `PASS` verdict.
- M12 is conditional only. This does not authorize live WeChat/WeCom callbacks, polling, credentials, outbound delivery, or automatic sending.

Closed question Q203: T230 is accepted with `PASS`, M12 may proceed only as `Gate M12 Conditional`, and the next task is T231 as a WeCom Customer Service synthetic inbound contract spike.

Historical note: this T230 closeout opened Q204 for T231. Q204 is now closed by the T231 `PASS` Captain decision above.

## Captain Update 2026-05-28 (T224 Review Decision / M11 Close)

Authoritative current risk state after the Captain review of T224:

- R040 remains active as a compact-context and privacy boundary rule: M12 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, behavior candidates, outbound requests, gate decisions, adapter results, review cards, and parsed review intents remain review/gate artifacts unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved and orthogonal to M11/M12 deterministic outbound infrastructure.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- R093 remains active but narrowed: T220-T224 now separate outbound request, gate decision, fake adapter result, Feishu sandbox result, review-card payload, and review intent from `CandidateAction`, but M12 must still avoid consuming `CandidateAction` review state as send permission.
- R096 remains active and narrowed: T224 correctly keeps review intent separate from applied approval or delivery; M12 must preserve the distinction between gate eligibility, fake simulation, Feishu sandbox result, review-card rendering, parsed review intent, applied approval, and production delivery.
- R097 remains active: T221 named-timezone verification on Windows requires `tzdata`, which is not currently declared in project dependencies. T224 did not modify timezone dependency policy.
- R098 remains active: display preview truncation is useful for local summaries/cards but is not a privacy boundary for future real, sandbox, or card-rendered payloads.
- R099 remains active: T223 Feishu sandbox payload shape has not been validated against current official Feishu production API semantics.
- R100 is active: T224 Feishu review-card payload and synthetic action parser are local approximations, not validation of real Feishu callback/event semantics.
- R101 is active: M12 could accidentally revive the paused personal-WeChat scan/login/realtime SDK track or unofficial SDK vendoring; T230 has since blocked those paths, and T231 must preserve the synthetic-only WeCom Customer Service boundary.
- T224 opened no deferred task-review risks. Its non-blocking observations are accepted as workspace-artifact convention, duplication, synthetic mapping fragility, config-test coverage, or type-surface notes under a `PASS` verdict.
- M11 is complete at the task level with `Gate M11 Allow` for local/sandbox outbound safety only. This does not authorize real Feishu or WeChat delivery.

Closed question Q202: T224 is accepted with `PASS`, M11 may close at task level, and the project may proceed to T230 `WeChat Adapter Research Spike`.

Historical note: this T224 closeout opened Q203 for T230. Q203 is now closed by the T230 `PASS` / `Gate M12 Conditional` Captain decision above.

## Captain Update 2026-05-28 (T223 Review Decision)

Authoritative current risk state after the Captain review of T223:

- R040 remains active as a compact-context and privacy boundary rule: M11 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, behavior candidates, outbound requests, gate decisions, adapter results, review cards, and parsed review intents remain review/gate artifacts unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved and orthogonal to T223/T224 deterministic outbound infrastructure.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- R093 remains active but narrowed: T220-T223 now separate outbound request, gate decision, fake adapter result, and Feishu sandbox result from `CandidateAction`, but T224+ must still avoid consuming `CandidateAction` review state as send permission.
- R096 remains active and narrowed: T223 correctly keeps Feishu sandbox evidence separate from production delivery; T224 must preserve the distinction between gate eligibility, fake simulation, Feishu sandbox result, review-card rendering, parsed review intent, applied approval, and production delivery.
- R097 remains active: T221 named-timezone verification on Windows requires `tzdata`, which is not currently declared in project dependencies. T223 did not modify timezone dependency policy.
- R098 remains active: T222 `payload_preview` truncation is useful for local synthetic result summaries but is not a privacy boundary for future real, sandbox, or card-rendered payloads.
- R099 is active: T223 Feishu sandbox payload shape has not been validated against current official Feishu production API semantics.
- T223 opened no deferred task-review risks. Its non-blocking observations are accepted as duplication, defensive validation, mutability, API-validation, or coverage-strength notes under a `PASS` verdict.

Closed question Q201: T223 is accepted with `PASS`, so the project may proceed to T224 `Feishu Review Card`.

## Captain Update 2026-05-28 (T222 Review Decision)

Authoritative current risk state after the Captain review of T222:

- R040 remains active as a compact-context and privacy boundary rule: M11 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, behavior candidates, outbound requests, gate decisions, and adapter results remain review/gate artifacts unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved and orthogonal to T222/T223 deterministic outbound infrastructure.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- R093 remains active but narrowed: T220-T222 now separate outbound request, gate decision, and fake adapter result from `CandidateAction`, but T223+ must still avoid consuming `CandidateAction` review state as send permission.
- R096 remains active and narrowed: T222 correctly keeps fake delivery local and synthetic; T223 must preserve the distinction between gate eligibility, fake simulation, Feishu sandbox payload/result, and production delivery.
- R097 remains active: T221 named-timezone verification on Windows requires `tzdata`, which is not currently declared in project dependencies. T222 stayed UTC-only, so the risk remains open.
- R098 is active: T222 `payload_preview` truncation is useful for local synthetic result summaries but is not a privacy boundary for future real or sandbox adapters.
- T222 opened no deferred task-review risks. Its non-blocking observations are accepted as conservative heuristic, cosmetic metadata, privacy-boundary, or coverage-strength notes under a `PASS` verdict.

Closed question Q200: T222 is accepted with `PASS`, so the project may proceed to T223 `Feishu Sandbox Adapter`.

## Captain Update 2026-05-28 (T221 Review Decision)

Authoritative current risk state after the Captain review of T221:

- R040 remains active as a compact-context and privacy boundary rule: M11 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, behavior candidates, outbound requests, and gate decisions remain review/gate artifacts unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved and orthogonal to T221/T222 deterministic outbound infrastructure.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- R093 remains active but narrowed: T220/T221 now separate outbound request and gate decision from `CandidateAction`, but T222+ must still avoid consuming `CandidateAction` review state as send permission.
- R096 remains active and narrowed: T221 correctly keeps gate `allowed` separate from delivery; T222 must preserve this by making fake delivery explicitly local and synthetic.
- R097 is active: T221 named-timezone verification on Windows requires `tzdata`, which is not currently declared in project dependencies. Future tasks should either add the dependency explicitly or keep tests/config on UTC-only paths.
- T221 opened no deferred task-review risks. Its non-blocking observations are accepted as service-layer design, small optimization, portability, or minor coverage-strength notes under a `PASS` verdict.

Closed question Q199: T221 is accepted with `PASS`, so the project may proceed to T222 `Local Fake Adapter`.

## Captain Update 2026-05-27 (T220 Review Decision)

Authoritative current risk state after the Captain review of T220:

- R040 remains active as a compact-context and privacy boundary rule: M11 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, behavior candidates, and outbound requests remain review/gate artifacts unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T220/T221 deterministic send-gate work.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- R093 remains active but narrowed: T220 now separates `OutboundMessageRequest` from `CandidateAction`, but T221 and later tasks must still prevent `CandidateAction.status`, `review_state`, or `is_runtime_visible()` from becoming send authorization.
- R094 remains active: CLI path metadata and default in-place overwrite remain accepted offline CLI conventions; M11 operational paths should prefer explicit outputs and avoid private names in paths.
- R095 remains active: T220 has not evaluated real platform delivery, notification UX, send audit UX, adapter failure recovery, or scheduler behavior. These belong to later M11+ tasks and must not be claimed as completed by T220.
- R096 is active: T221 could accidentally blur "gate allowed" with "delivered". Gate allowance must only update/audit the request state; fake and real adapters remain later tasks.
- T220 opened no deferred task-review risks. Its non-blocking observations are accepted as cleanup, schema-only scope, documentation clarity, or minor coverage-strength notes under a `PASS` verdict.

Closed question Q198: T220 is accepted with `PASS`, so the project may proceed to T221 `OutboundSendGate`.

## Captain Update 2026-05-27 (T214 Review / M10 Review)

Authoritative current risk state after the Captain review of T214 and M10:

- R040 remains active as a compact-context and privacy boundary rule: M11 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, and behavior candidates remain review-only guidance unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to M10 review-only BehaviorPlanner completion.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- R093 is active: future M11 code could accidentally interpret `CandidateAction.status="approved"`, `review_state="reviewed"`, or `is_runtime_visible()` as outbound authorization. T220/T221 must prevent this with a separate outbound request model and explicit send-gate decision.
- R094 is active: CLI path metadata and default in-place overwrite remain accepted offline CLI conventions, but future operational workflows should avoid private names in paths and prefer explicit output paths.
- R095 is active: M10 has not evaluated real platform delivery, notification UX, send audit UX, adapter failure recovery, or scheduler behavior. These belong to M11+ and must not be claimed as completed by M10.
- T214 opened no deferred task-review risks. Its non-blocking observations are accepted as conservative design, harmless eval-scope context, current convention risk, cosmetic evidence detail, or minor traceability-strength notes under a `PASS` verdict.
- M10 is complete with `Gate M10 Allow` only for review-only behavior-planner infrastructure.

Closed question Q197: T214 is accepted with `PASS`, so M10 may close with `Gate M10 Allow` and the project may proceed to T220.

## Captain Update 2026-05-25 (T213 Review Decision)

Authoritative current risk state after the Captain review of T213:

- R040 remains active as a compact-context and privacy boundary rule: M10 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, and behavior candidates remain review-only guidance unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T213 and does not block deterministic/manual M10 review work.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- T213 opened no new deferred risks. Its non-blocking review observations are accepted as convention noise, current offline workflow trade-offs, cosmetic typing debt, or minor test-strength notes under a `PASS` verdict.
- M10 remains non-executable: reviewed or approved `CandidateAction` output must not be treated as authorization to send, schedule, execute, call platforms, or mutate state.

Closed question Q196: T213 is accepted with `PASS`, so the project may proceed to T214 as an evaluation-only behavior safety task.

## Captain Update 2026-05-25 (T212 Review Decision)

Authoritative current risk state after the Captain review of T212:

- R040 remains active as a compact-context and privacy boundary rule: M10 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, and behavior candidates remain review-only guidance unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T212 and does not block deterministic M10 draft enrichment work.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- T212 opened no new deferred risks. Its non-blocking review observations are accepted as convention noise, deterministic design choices, or minor test-strength notes under a `PASS` verdict.
- M10 remains non-executable: `ProactiveDraftGenerator` output is review text only and must not be treated as authorization to send, schedule, execute, or mutate state.

Closed question Q195: T212 is accepted with `PASS`, so the project may proceed to T213 as a manual review workflow task.

## Captain Update 2026-05-25 (T211 Review Decision)

Authoritative current risk state after the Captain review of T211:

- R040 remains active as a compact-context and privacy boundary rule: M10 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, and behavior candidates remain review-only guidance unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T211 and does not block deterministic M10 draft enrichment work.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- T211 opened no new deferred risks. Its non-blocking review observations are accepted as convention noise, intentional conservative design, or minor test-strength notes under a `PASS` verdict.
- M10 remains non-executable: `BehaviorRulePlanner` output, `CandidateAction` approval, or runtime visibility must not be treated as authorization to send, schedule, execute, or mutate state.

Closed question Q194: T211 is accepted with `PASS`, so the project may proceed to T212 as a deterministic, review-only draft-text enrichment task.

## Captain Update 2026-05-25 (T210 Review Decision)

Authoritative current risk state after the Captain review of T210:

- R040 remains active as a compact-context and privacy boundary rule: M10 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, and behavior candidates remain review-only guidance unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T210 and does not block deterministic M10 rule work.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- T210 opened no new deferred risks. Its non-blocking review observations are accepted as convention noise, schema-style choices, or minor test-strength notes under a `PASS` verdict.
- M10 remains non-executable: `CandidateAction` approval or runtime visibility must not be treated as authorization to send, schedule, execute, or mutate state.

Closed question Q193: T210 is accepted with `PASS`, so the project may proceed to T211 as a deterministic, review-only rule-engine task.

## Captain Update 2026-05-24 (T203 Review Decision)

Authoritative current risk state after the Captain review of T203:

- R040 remains active as a compact-context and privacy boundary rule: M10 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, relationship-state artifacts, and future behavior candidates remain review-only guidance unless a later task explicitly authorizes mutation or execution.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T203 and does not block M9 retrieval infrastructure completion.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- T203 opened no new deferred risks. Its non-blocking review observations are accepted as convention noise, spike-scope limitations, or harmless documentation/test-strength notes.
- Mem0 remains optional/off-by-default and is not production external-memory adoption. Future production use would need explicit review enforcement, evidence mapping, SDK/dependency pinning, and operational error recovery.

Closed question Q192: T203 is accepted with `PASS`, so M9 is complete at task level and the project may proceed to M10/T210.

## Captain Update 2026-05-24 (T202 Review Decision)

Authoritative current risk state after the Captain review of T202:

- R040 remains active as a compact-context and privacy boundary rule: M9 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, and relationship-state artifacts remain review-only guidance unless a later task explicitly authorizes mutation.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T202 and does not block M9 retrieval evaluation work.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- T202 opened no new deferred risks. Its non-blocking review observations are accepted as convention noise, acceptable scope boundaries, or low-risk eval-strength notes.

Closed question Q191: T202 is accepted with `PASS`, so the project may proceed to T203 as an optional Mem0 adapter spike behind the existing `MemoryRetriever` contract.

## Captain Update 2026-05-24 (T201 Review Decision)

Authoritative current risk state after the Captain review of T201:

- R040 remains active as a compact-context and privacy boundary rule: M9 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, and relationship-state artifacts remain review-only guidance unless a later task explicitly authorizes mutation.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T201 and does not block M9 local retrieval work.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- T201 opened no new deferred risks. Its non-blocking review observations are accepted as convention noise or acceptable current-scope operational trade-offs.

Closed question Q190: T201 is accepted with `PASS`, so the project may proceed to T202 and create a synthetic retrieval eval set against the `MemoryRetriever` contract.

## Captain Update 2026-05-24 (T200 Review Decision)

Authoritative current risk state after the Captain review of T200:

- R040 remains active as a compact-context and privacy boundary rule: M9 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: approved memories, approved patches, derived briefs, and relationship-state artifacts remain review-only guidance unless a later task explicitly authorizes mutation.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T200 and does not block M9 retrieval-contract work.
- R091 remains active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics.
- R092 remains active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.
- T200 opened no new deferred risks. Its non-blocking review observations are accepted as convention noise or intentional contract flexibility.

Closed question Q189: T200 is accepted with `PASS`, so the project may proceed to T201 and implement a local approved-store retriever against the new `MemoryRetriever` contract.

## Captain Update 2026-05-24 (T195 Review Decision)

Authoritative current risk state after the Captain review of T195:

- R040 remains active as a compact-context and privacy boundary rule: M9 and later work must continue to use approved metadata / review-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: relationship-state work remains review-only guidance and must not turn into hidden state mutation.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T195 and does not block M8 closure.
- R084 remains active and deferred: T193 approvals still do not run an evidence pre-validation gate, so later work must not over-read approval as evidence freshness.
- R086 through R090 remain active as deferred T194 hardening debt.
- R091 is active and deferred: approved relationship context exists in `ChatContext`, but no planner or policy code path consumes relationship delta semantics, so reply behavior is unchanged.
- R092 is active and deferred: relationship guidance that surfaces through summary/retrieval notes is informational only and must not be mistaken for semantic runtime consumption.

Closed question Q188: T195 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T200 and close M8 as an infrastructure/evaluation milestone without claiming relationship-aware planner behavior is already implemented.

## Captain Update 2026-05-24 (T194 Review Decision)

Authoritative current risk state after the Captain review of T194:

- R040 remains active as a compact-context and privacy boundary rule: T195 must continue to use approved metadata / anonymized-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: relationship-state work must stay review-only and must not turn compact context into hidden state mutation.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T194 and does not block M8 context acceptance.
- R083 remains active and deferred: T193 still has no committed CLI-level integration tests.
- R084 remains active and deferred: T193 approvals do not run an evidence pre-validation gate, so T194/T195 must not treat approval as evidence freshness.
- R085 remains active and deferred: the empty-string review-note path is untested and could regress silently.
- R086 is active and deferred: T194 summary truncation is not directly tested.
- R087 is active and deferred: T194 path-is-directory branch is not directly tested.
- R088 is active and deferred: T194 empty `delta_rationale` input is not directly tested.
- R089 is active and deferred: T194 uses a directory-of-JSON-files relationship context path rather than a store-file abstraction, which is acceptable for scope but may become awkward if delta volume grows.
- R090 is active and deferred: T194 has no AppContainer wiring, so runtime configuration remains programmatic only.

Closed question Q187: T194 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T195 rather than reopening the compact-context task.

## Captain Update 2026-05-24 (T193 Review Decision)

Authoritative current risk state after the Captain review of T193:

- R040 remains active as a compact-context and privacy boundary rule: T194 and later M8 work must continue to use approved metadata / anonymized-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: relationship-state work must stay review-only and must not turn approved deltas into hidden state mutation without an explicit later task.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T193 and does not block M8 review acceptance.
- R078 remains active and deferred: T192 still lacks an explicit unknown-dimension safe-skip regression test.
- R079 remains active and deferred: T192 still lacks a mixed known+unknown/stable direction regression test.
- R080 remains active and deferred: T192 still lacks the state-evidence-only deduplication edge-case test.
- R081 remains active and deferred: T192 aggregation/calibration remains heuristic and uncalibrated.
- R082 is now narrowed but still active: T193 chose an all-or-nothing review model, but later tasks must preserve that choice explicitly unless they deliberately redesign it.
- R083 is active and deferred: T193 has no committed CLI-level integration tests, so Typer wiring, file I/O, and safe-path output remain regression-prone.
- R084 is active and deferred: T193 approvals do not run an evidence pre-validation gate, so later context/application tasks must not assume approved deltas automatically have fresh, resolvable evidence.
- R085 is active and deferred: the empty-string review-note path is untested and could regress silently.

Closed question Q186: T193 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T194 rather than reopening the relationship review task.

## Captain Update 2026-05-24 (T192 Review Decision)

Authoritative current risk state after the Captain review of T192:

- R040 remains active as a compact-context and privacy boundary rule: T193 and later M8 work must continue to use approved metadata / anonymized-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: relationship-state work must stay review-only and must not turn deltas into automatic learning or hidden state mutation.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T192 and does not block M8 delta acceptance.
- R072 remains active and narrowed: T192 now recomputes/validates magnitude programmatically, but the schema itself still does not enforce the invariant.
- R073 remains active: `RelationshipDeltaDirection="stable"` still lacks a fully explicit contract meaning across later review/application flows.
- R074 remains active: no committed automated tests yet cover `RelationshipState` / `RelationshipDeltaCandidate` validation helpers at the model boundary.
- R075 remains active and deferred: `RelationshipSignal` lacks an `updated_at` field, so later review/update flows will not have an explicit mutation timestamp unless T193 or a follow-up adds one.
- R076 remains active and deferred: `RelationshipSignal` runtime-ready approval path is not yet committed-test covered.
- R077 remains active and deferred: `RelationshipSignal.signal_id` format and non-emptiness are not yet covered by a dedicated committed test.
- R078 is active and deferred: no committed test yet confirms that unknown dimension names are skipped safely by T192.
- R079 is active and deferred: no committed test yet covers mixed known-direction plus unknown/stable companion signals on the same dimension.
- R080 is active and deferred: no committed test yet covers the state-evidence-only deduplication edge case that could leave delta `evidence_refs` empty.
- R081 is active and deferred: T192 uses heuristic `_MAGNITUDE_SCALE` / `_MIN_STRENGTH` defaults and max-strength aggregation, which are explicit and reviewable but uncalibrated.
- R082 is active and deferred: T193 still needs a clear decision on whether relationship-delta review is all-or-nothing or can support dimension-level partial approval.

Closed question Q185: T192 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T193 rather than reopening the delta-generation task.

## Captain Update 2026-05-24 (T191 Review Decision)

Authoritative current risk state after the Captain review of T191:

- R040 remains active as a compact-context and privacy boundary rule: T192 and later M8 work must continue to use approved metadata / anonymized-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: relationship-state work must stay review-only and must not turn feedback, derived briefs, or future signals into automatic learning or hidden state mutation.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T191 and does not block M8 signal acceptance.
- R072 is active and deferred: `RelationshipDeltaDimension.magnitude` is still not schema-enforced against `current_value` / `proposed_value`, so T192 must validate or recompute it explicitly.
- R073 is active and deferred: `RelationshipDeltaDirection="stable"` still lacks contract guidance, so T192/T193 could diverge unless the delta semantics are narrowed explicitly.
- R074 remains active: no committed automated tests yet cover `RelationshipState` / `RelationshipDeltaCandidate` validation, helper behavior, or runtime-ready gating.
- R075 is active and deferred: `RelationshipSignal` lacks an `updated_at` field, so later review/update flows will not have an explicit mutation timestamp unless T193 or a follow-up adds one.
- R076 is active and deferred: `RelationshipSignal` runtime-ready approval path is not yet committed-test covered.
- R077 is active and deferred: `RelationshipSignal.signal_id` format and non-emptiness are not yet covered by a dedicated committed test.

Closed question Q184: T191 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T192 rather than reopening the signal-extraction task.

## Captain Update 2026-05-24 (T190 Review Decision)

Authoritative current risk state after the Captain review of T190:

- R040 remains active as a compact-context and privacy boundary rule: T191 and later M8 work must continue to use approved metadata / anonymized-safe artifacts only and must not reopen raw-transcript ingestion.
- R041 remains active: relationship-state work must stay review-only and must not turn feedback, derived briefs, or future signals into automatic learning or hidden state mutation.
- R071 remains active: LLM confidence calibration is still unresolved, but it is orthogonal to T190 and does not block M8 schema acceptance.
- R072 is active and deferred: `RelationshipDeltaDimension.magnitude` is not schema-enforced against `current_value` / `proposed_value`, so downstream code cannot yet assume that magnitude is internally consistent.
- R073 is active and deferred: `RelationshipDeltaDirection="stable"` exists without contract guidance, so later M8 tasks could diverge on what a no-change delta means unless T192/T193 narrow the semantics explicitly.
- R074 is active and deferred: no committed automated tests yet cover `RelationshipState` / `RelationshipDeltaCandidate` validation, helper behavior, or runtime-ready gating.

Closed question Q183: T190 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T191 rather than reopening the schema-only M8 opening step.

## Captain Update 2026-05-23 (T185 Review Decision + M7 Review)

Authoritative current risk state after the Captain review of T185 and the M7 milestone review:

- R039 remains active: M7 is closed, but LLM quality and confidence can still be over-read as readiness for unmonitored use.
- R040 remains active as a compact-context boundary rule: M8 and later work must continue to use anonymized/safe inputs only.
- R041 remains active: approved patches, derived briefs, and future relationship state must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R069 is active and deferred: safety-context detection remains heuristic rather than policy-engine-native.
- R070 is active and deferred: Chinese output alignment is still prompt-level rather than hard post-generation enforcement.
- R071 is active and deferred: LLM confidence calibration remains unresolved and should not be treated as a probability.

Closed question Q181: T185 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T190 rather than reopening M7 repair work.
Closed question Q182: Gate M7 is `Allow`, so the project may enter M8 beginning with T190.

## Captain Update 2026-05-23 (T184 Review Decision)

Authoritative current risk state after the Captain review of T184:

- R039 remains active: the holdout evidence supports improvement, but not readiness for unmonitored use or broad quality claims.
- R040 remains active as a compact-context boundary rule: T185 and later work must continue to use anonymized/safe holdout inputs only.
- R041 remains active: approved patches and derived briefs must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R065 remains active and now is clearly exposed by holdout eval: the hybrid merge success path still lacks a committed regression test.
- R066 is active and deferred: hybrid LLM candidates default to English while template candidates are Chinese, creating a mixed-language review UX gap.
- R067 is active and deferred: LLM draft text can contradict thin_context / boundary_sensitive safety intent even when policy flags are present.
- R068 is active and deferred: hybrid LLM `approach_label` values are not normalized to the same naming convention as template labels.

Closed question Q179: T184 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T185 rather than reopening holdout evaluation for a blocking repair pass.
Closed question Q180: Gate M7 is `Conditional`, so the project may continue within M7 but may not claim the milestone is fully closed until T185 resolves the remaining conditions.

## Captain Update 2026-05-23 (T183 Review Decision)

Authoritative current risk state after the Captain review of T183:

- R039 remains active: entering T184 can still overstate LLM quality if holdout evidence is treated as proof of general readiness rather than a bounded evaluation.
- R040 remains active as a compact-context boundary rule: T184 must evaluate only anonymized/safe holdout inputs and must not reopen raw-transcript or full-store paths.
- R041 remains active: approved patches and derived briefs must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R065 is active and deferred: the hybrid merge success path does not have a committed regression test, so future refactors could break valid-candidate merging without immediate detection.

Closed question Q178: T183 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T184 rather than reopening hybrid integration work for a blocking repair pass.

## Captain Update 2026-05-23 (T182 Review Decision)

Authoritative current risk state after the Captain review of T182:

- R039 remains active: entering T183/T184 can still reintroduce LLM scope creep if hybrid work drifts into default runtime LLM behavior.
- R040 remains active as a compact-context boundary rule: T183 may integrate planner paths, but it must not invent a new raw-transcript or full-store input surface.
- R041 remains active: approved patches and derived briefs must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R063 remains active and deferred in a narrower, concrete form: the new `INPUT_TOO_LARGE` preflight exists but is called incorrectly, so the deterministic refusal path is still non-functional.
- R064 remains active but narrowed: most T181 regression gaps are now closed, but the `INPUT_TOO_LARGE` refusal path still lacks committed regression coverage.

Closed question Q177: T182 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T183 rather than reopening validator extraction work for a blocking repair pass.

## Captain Update 2026-05-23 (T181 Review Decision)

Authoritative current risk state after the Captain review of T181:

- R039 remains active: entering T182/T183 can still reintroduce LLM scope creep if validator work drifts into hybrid planner behavior or default runtime LLM mode.
- R040 remains active as a compact-context boundary rule: T182 may harden validation, but it must not invent a new raw-transcript or full-store input path.
- R041 remains active: approved patches and derived briefs must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R062 is active and deferred: T181 privacy leak detection is substring-based and misses paraphrase/key-detail leakage.
- R063 is active and deferred: `INPUT_TOO_LARGE` exists in the refusal contract but has no explicit preflight budget enforcement, so oversize input currently collapses into provider-error handling.
- R064 is active and deferred: T181 lacks committed regression coverage for `_build_llm_input`, provider parse errors, generator-to-validator end-to-end flow, and CLI stdout privacy.

Closed question Q176: T181 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T182 rather than reopening offline generator work for a blocking repair pass.

## Captain Update 2026-05-23 (T180 Review Decision)

Authoritative current risk state after the Captain review of T180:

- R039 remains active: entering T181 can still reintroduce LLM scope creep if the offline CLI crosses into default planner behavior, non-private outputs, or hybrid planner work.
- R040 remains active but is now a hard M7 boundary: future LLM work must consume the existing compact-context structure instead of inventing a parallel raw-transcript path that bypasses the committed fallback-safe context design.
- R041 remains active: approved patches and derived briefs must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R061 remains closed for M6 scope: T180 does not reopen the accepted decomposition/fallback question.

Closed question Q175: T180 is accepted with `PASS`, so the project may proceed to T181 rather than reopening contract-definition work for a blocking repair pass.

## Captain Update 2026-05-23 (M6 Review)

Authoritative current risk state after the Captain milestone review of M6:

- R039 remains active: entering M7 can reintroduce LLM scope creep if contract-only work is not kept narrow.
- R040 remains active but is now regression-guarded by committed M6 tests; future planner/context changes must not break additive fallback behavior.
- R041 remains active: approved patches and future derived briefs must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R061 is now closed for M6 scope: committed T174 tests show derived briefs remain additive, preserve `ApprovedContactSkillBrief` fallback, and coexist with the T164 approved-patch compact-context path.

Closed question Q173: T174 is accepted with `PASS`, so the project may proceed to milestone review rather than reopening context integration work for a blocking repair pass.
Closed question Q174: Gate M6 is `Allow`, so the project may enter M7 beginning with T180 contract-only work.

## Captain Update 2026-05-23 (T174 Review Decision)

Authoritative current risk state after the Captain review of T174:

- R040 remains active but is further narrowed: context integration is now committed alongside schema and projection, reducing the chance of accidental `ContactSkill` replacement inside M6.
- R041 remains active: derived briefs and approved patch hints must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R061 remains active but is narrowed pending milestone review: the remaining question is whether committed T174 tests are sufficient to close the M6 integration risk for the milestone gate.

## Captain Update 2026-05-23 (T173 Review Decision)

Authoritative current risk state after the Captain review of T173:

- R040 remains active but is further narrowed: the decomposition path now has not only committed schemas but also a committed projection layer, reducing the chance of accidental `ContactSkill` replacement during T174.
- R041 remains active: future derived briefs and approved patch hints must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R061 remains active but is further narrowed: projection fidelity is now committed; the remaining M6 risk is integration discipline, especially preserving fallback behavior and keeping derived-brief context separate from approved-patch compact context.

Closed question Q172: T173 is accepted with `PASS`, so the project may proceed to T174 rather than reopening projection work for a blocking repair pass.

## Captain Update 2026-05-23 (T172 Review Decision)

Authoritative current risk state after the Captain review of T172:

- R040 remains active but is further narrowed: the decomposition path now has all three additive schemas committed, reducing the chance of accidental `ContactSkill` replacement during later M6 work.
- R041 remains active: future derived briefs and approved patch hints must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R061 remains active but is further narrowed: schema semantics are now committed; the remaining M6 risk is projection fidelity, especially explicit conversion/computation rules and preservation of the existing evidence contract.

Closed question Q171: T172 is accepted with `PASS`, so the project may proceed to T173 rather than reopening policy/boundary schema work for a blocking repair pass.

## Captain Update 2026-05-23 (T171 Review Decision)

Authoritative current risk state after the Captain review of T171:

- R040 remains active but is further narrowed: the decomposition path is now not only documented, but also partially encoded as additive schema rather than as a breaking replacement.
- R041 remains active: future derived briefs and approved patch hints must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R061 remains active but is narrowed: persona-brief typing is now resolved; the remaining M6 contract work is boundary sensitivity reduction, important-event ownership, derived-brief versioning strategy, and projection-layer conversion rules.

Closed question Q170: T171 is accepted with `PASS`, so the project may proceed to T172 rather than reopening persona-brief schema work for a blocking repair pass.

## Captain Update 2026-05-22 (T170 Review Decision)

Authoritative current risk state after the Captain review of T170:

- R040 remains active but is narrowed: the decomposition path is now explicitly documented as projection plus fallback, reducing the chance of accidental `ContactSkill` replacement.
- R041 remains active: future derived briefs and approved patch hints must still be interpreted as review-only guidance rather than automatic learning or hidden state mutation.
- R061 is active and deferred: T171-T172 must formalize persona-brief typing, boundary sensitivity reduction, important-event ownership, and any future patch-to-boundary semantics so T173-T174 do not drift from the T170 contract.

Closed question Q169: T170 is accepted with `PASS`, so the project may proceed to T171 rather than reopening M6 design work for a blocking repair pass.

## Captain Update 2026-05-22 (T164 Review Decision)

Authoritative current risk state after the Captain review of T164:

- R041 remains active: approved patches in context must still be interpreted as review-only communication hints rather than automatic learning.
- R053 remains active and deferred: `patch_id` non-determinism across repeated T162 runs persists but is now consumed only at T164 load time.
- R054 remains active and deferred: repo coverage now exists for `ApprovedPatchContextService`, but gaps remain for frozen/archived exclusion fixtures, end-to-end `ChatContextAssembler` approved-patch integration, and empty/whitespace `behavior_instruction` handling.
- R057 remains active: T163 write-back corruption risk is bounded since T164 reads the report read-only; a corrupted report would surface as `store_path_missing` or invalid JSON.
- R058 remains active: review history unbounded growth is a storage concern only; T164 does not expand history into context.
- R059 remains active: `ApprovedPatchContextService` loads the full proposal report into memory. For large reports with many candidates this may become a memory concern, but is acceptable for current single-user offline scale.
- R060 remains active: `ChatContextAssembler` path validation for patch reports reuses `_ensure_within_private_distilled` which constrains paths under `private/distilled/`. This guards against accidental exposure but is not a hard security boundary.

Closed question Q168: T164 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T170 rather than sending T164 back for a blocking repair pass.

## Captain Update 2026-05-22 (T164)

Authoritative current risk state after T164 Approved Patch Compact Context:

- R041 remains active: approved patches now have a compact context path but must still be interpreted as review-only communication hints rather than automatic learning.
- R053 remains active and deferred: `patch_id` non-determinism across repeated T162 runs persists but is now consumed only at T164 load time.
- R054 remains active and deferred: repo coverage now exists for `ApprovedPatchContextService`, but gaps remain for frozen/archived exclusion fixtures, end-to-end `ChatContextAssembler` approved-patch integration, and empty/whitespace `behavior_instruction` handling.
- R057 remains active: T163 write-back corruption risk is bounded since T164 reads the report read-only; a corrupted report would surface as `store_path_missing` or invalid JSON.
- R058 remains active: review history unbounded growth is a storage concern only; T164 does not expand history into context.
- R059 is active: `ApprovedPatchContextService` loads the full proposal report into memory. For large reports with many candidates this may become a memory concern, but is acceptable for current single-user offline scale.
- R060 is active: `ChatContextAssembler` path validation for patch reports reuses `_ensure_within_private_distilled` which constrains paths under `private/distilled/`. This guards against accidental exposure but is not a hard security boundary.

Closed question Q167: T164 provides compact approved-patch context integration that consumes reviewed T162/T163 proposal reports, filters to only approved + runtime-ready patches, and exposes safe, compressed patch briefs through `ChatContext` without raw feedback text, review history expansion, or non-approved patch leakage.

## Captain Update 2026-05-22 (T163 Review Decision)

Authoritative current risk state after the Captain review of T163:

- R041 remains active: T164 must preserve the interpretation of feedback-to-patch as review-only proposal work rather than automatic learning.
- R053 remains active and deferred from T163 review: `patch_id` is UUID-based and non-deterministic across repeated T162 runs.
- R054 remains active and deferred: no committed automated tests yet cover `PatchProposalService`, `chat-feedback-propose-patch`, `PatchReviewService`, or `chat-feedback-review-patch`.
- R057 is active: `PatchReviewService` writes back to the input file by default when `--output` is not specified. If the write fails mid-operation, the input file may be corrupted.
- R058 is active: repeated review decisions on the same patch accumulate in `review_metadata.history` without a bound.

Closed question Q166: T163 provides explicit human review actions (approve/reject/freeze/archive) for `PreferencePatchCandidate` proposals, preserving evidence fields and accumulating review history. Approved patches become runtime-ready; rejected/frozen/archived patches remain non-runtime-ready.

## Captain Update 2026-05-19 (T163)

Authoritative current risk state after T163 Patch Review CLI:

- R041 remains active: T163 adds human review decisions but does not inject approved patches into runtime context. T164 must preserve the review-only-to-compact-context boundary.
- R053 remains active and deferred from T162 review: `patch_id` is UUID-based and non-deterministic across repeated T162 runs.
- R054 remains active and deferred: no committed automated tests yet cover `PatchProposalService`, `chat-feedback-propose-patch`, `PatchReviewService`, or `chat-feedback-review-patch`.
- R057 is active: `PatchReviewService` writes back to the input file by default when `--output` is not specified. If the write fails mid-operation, the input file may be corrupted. The current implementation writes the full JSON on each review decision, which is safe for single-review use but may not be atomic under concurrent access.
- R058 is active: repeated review decisions on the same patch accumulate in `review_metadata.history` without a bound. Over many review cycles the history list could grow unboundedly.

Closed question Q166: T163 provides explicit human review actions (approve/reject/freeze/archive) for `PreferencePatchCandidate` proposals, preserving evidence fields and accumulating review history. Approved patches become runtime-ready; rejected/frozen/archived patches remain non-runtime-ready.

## Captain Update 2026-05-18 (T162 Review Decision)

Authoritative current risk state after the Captain review of T162:

- R041 remains active: T163-T164 must preserve the interpretation of feedback-to-patch as review-only proposal work rather than automatic learning.
- R043 remains active and deferred from T162 review: raw `input_path` is still present in proposal stdout/output and remains project-wide path-handling/privacy debt.
- R053 remains active and deferred from T162 review: the contract still overclaims deterministic `patch_id` behavior even though `patch_id` is UUID-based and non-deterministic across repeated runs.
- R054 is active and deferred: no committed automated tests yet cover `PatchProposalService` or `chat-feedback-propose-patch`.
- R056 is active and deferred: malformed cluster input with empty `contact_id` can still crash proposal generation instead of being skipped defensively.

Closed question Q165: T162 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T163 rather than sending T162 back for a blocking repair pass.

## Captain Update 2026-05-18 (T162)

Authoritative current risk state after T162 Patch Proposal CLI:

- R041 remains active: T162 generates candidate-only patches but does not review, approve, or apply them. T163/T164 must preserve the review-only, candidate-only interpretation.
- R048 is addressed at the proposal layer: `positive_examples` and `negative_examples` are always empty lists at T162 proposal time. T163 review CLI or future tasks may populate these with safe summaries.
- R053 is active: `patch_id` uses `new_id("patch")` (UUID-based, non-deterministic) while all other proposal fields are deterministic from cluster input. Repeated runs on the same cluster report produce identical content but different `patch_id` values.
- R054 is active: no committed automated tests yet cover `PatchProposalService` / `chat-feedback-propose-patch`.
- R055 is active: confidence formula `min(0.3 + 0.15 * (record_count - 1), 0.9)` is monotonic but not calibrated. Confidence values should not be interpreted as probabilities.

Closed question Q164: T162 produces deterministic, candidate-only PreferencePatch proposals from T161 cluster outputs, skipping ambiguous or low-support clusters with explicit skip reasons.

## Captain Update 2026-05-18 (T161 Review Decision)

Authoritative current risk state after the Captain review of T161:

- R041 remains active: T162-T164 must preserve the interpretation of feedback-to-patch as review-only proposal work rather than automatic learning.
- R043 remains active and deferred from T161 review: raw `input_path` is still present in cluster stdout/output and remains project-wide path-handling/privacy debt.
- R050 remains active: edit actions still produce no safe deterministic cluster label, so T162 must not assume edit-driven preferences are already captured by T161.
- R051 remains active: cluster IDs are stable by grouping key rather than by record content, so downstream consumers must not rely on `cluster_id` alone to understand evidence changes.
- R052 is active and deferred: no committed automated tests yet cover `FeedbackClusterService` or `chat-feedback-cluster`.

Closed question Q163: T161 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T162 rather than sending T161 back for a blocking repair pass.

## Captain Update 2026-05-18 (T161)

Authoritative current risk state after T161 Feedback Clusterer:

- R041 remains active: T161 clusters feedback but does not generate patches, review them, or apply them. Downstream tasks must preserve the aggregate-only, review-only interpretation.
- R050 is active: edit actions produce no cluster label because no safe deterministic signal exists to distinguish edit reasons. T161 marks edit records as unlabeled. T162 may need a different strategy for edit-based patch proposals, or a later hardening task may derive edit-specific labels from approach_label patterns or boundary_label signals.
- R051 is active: cluster_id stability depends on the grouping key content, not on the actual records. Two runs with different records for the same (contact_id, label) produce the same cluster_id. This is by design for accumulation but may confuse consumers that expect cluster_id to reflect record content.
- R052 is active: no committed automated tests yet cover cluster output validation.

Closed question Q162: T161 produces deterministic, privacy-safe feedback clusters with stable cluster_ids, supporting_feedback_ids, and aggregate counts. The clustering is action-type-based and does not generate PreferencePatchCandidate records.

## Captain Update 2026-05-18 (T160 Review)

Authoritative current risk state after the Captain review of T160:

- R041 remains active: T160 is accepted, but M5 must still preserve the candidate-only, review-only interpretation of feedback-to-patch work.
- R047 remains active but is accepted for now: `instruction_scope` and `affected_candidate_types` remain free-form strings until actual T161/T162 usage clarifies whether enum tightening is worth the compatibility cost.
- R048 remains active and deferred: `positive_examples` and `negative_examples` still rely on convention rather than structure to stay privacy-safe. T162 must enforce safe-summary-only content.
- R049 is active: `PreferencePatchCandidate` has no committed automated validation tests yet. This is acceptable for T160 scope, but a later hardening slice should add model-level regression coverage before broader M5 runtime consumption.

Closed question Q161: T160 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T161 rather than sending T160 back for a blocking repair pass.

## Captain Update 2026-05-18 (T160)

Authoritative current risk state after T160 PreferencePatch Schema:

- R041 remains active: T160 defines the candidate-only schema but does not implement clustering, review, or application. The `PreferencePatchCandidate` schema structurally enforces evidence via `supporting_feedback_ids` (min_length=1) and candidate-only defaults, but downstream tasks must preserve these constraints.
- R047 is active: T160 introduces `PreferencePatchType` with 8 values, but `instruction_scope` and `affected_candidate_types` remain free-form strings. Later tasks should validate actual usage patterns before deciding whether to constrain these to enums.
- R048 is active: `positive_examples` and `negative_examples` are free-form string lists with no structural enforcement that they contain only safe references rather than raw feedback text. T162 proposal generation must enforce safe-summary-only content.

Closed question Q160: T160 defines the PreferencePatch candidate schema with all required fields. The schema is candidate-only, evidence-backed, and compatible with later M5 tasks without requiring schema breakage.

## Captain Update 2026-05-18 (M4.5 Review)

Authoritative current risk state after the Captain milestone review of M4.5:

- R046 is closed: clean-environment reproducibility for the reviewed M3/M4 surface is now proven from committed repo contents via T150/T151/T152.
- R043 remains active and deferred from T152 review: service-level output-path confinement is still not hard-enforced.
- R045 remains active and deferred from T152 review: validation `record_results` can still become verbose on large logs.
- R044 remains active: `reply_plan_id` coherence is still not fully cross-checked against loaded plan context.
- R038 remains active: M5 must continue to avoid any automatic learning interpretation of feedback.
- R035 remains active: relationship-aware quality is still template-driven.
- R037 remains active but well-instrumented by committed tests.

Closed question Q133: M4.5 is complete and the project may now enter M5, beginning with T160 PreferencePatch Schema under candidate-only, review-only constraints.

## Captain Update 2026-05-18 (T152)

Authoritative current risk state after T152 Feedback CLI Regression Tests:

- R046 is now closed for M4.5: T150 (49 tests), T151 (67 tests), and T152 (60 tests) together provide 176 committed deterministic tests covering ReplyPlanner, policy engine, and the full feedback CLI loop. Clean-environment reproducibility is now proven from committed repo contents alone. M5 may be reconsidered after Captain review.
- R042 is regression-guarded: corrupted JSON, schema-invalid, and missing-file inputs are all tested to surface explicit errors rather than silent normalization, in both the validator and the summary exporter.
- R043 is regression-guarded: privacy warnings for non-private input paths (W_PRIVACY_INPUT) and non-private plan references (W_PRIVACY_REF) are tested. Service-level output-path freedom is documented as by-design for the single-user offline workflow.
- R044 remains active but is regression-guarded for the paths T142 already covers.
- R045 is regression-guarded: compact output tests verify that validation report and summary do not echo per-record private text.
- R035 remains active: T152 does not address relationship-aware quality.
- R037 remains active but is well-instrumented by T151 tests.

Closed question Q132: T152 is complete as a feedback CLI regression test task. M4.5 regression hardening is now structurally complete (T150/T151/T152). The clean-environment reproducibility gap that kept M4 at Conditional is now closed from committed repo contents.

## Captain Update 2026-05-18 (T151 Review Decision)

Authoritative current risk state after the Captain review of T151:

- R036 can now be closed for the planner/policy slice: T150 and T151 together provide committed deterministic regression coverage for both ReplyPlanner output behavior and direct policy-engine behavior.
- R037 remains active but is now well-instrumented: false-positive, false-negative, over-proactivity, impersonation-risk, no-pressure exemption, and confidence-penalty behavior are all encoded in committed tests, but the keyword-only limitation is still real.
- R046 remains active but is now narrowly scoped to the feedback CLI loop: T152 is the last required M4.5 hardening task before M5 can be reconsidered.
- R035 remains active: T151 improves safety-surface auditability, not relationship-aware naturalness.

Closed question Q131: T151 is accepted with `PASS_WITH_WARNINGS`, so the project may move directly to T152 rather than sending T151 back for a blocking fix pass.

## Captain Update 2026-05-18 (T151)

Authoritative current risk state after T151 Policy Fixture Suite:

- R036 is further narrowed but remains active: T151 adds 67 direct policy engine tests and 3 new fixture contexts on top of T150's 49 planner-through-policy tests. Policy layer behavior is now directly regression-guarded from committed repo contents. T152 must still cover feedback CLI.
- R037 is further documented: false-positive, false-negative, over-proactivity, impersonation-risk, action-push, no-pressure exemption, and confidence penalty behavior all have direct `ReplyPlanPolicyEngine` tests encoding current expected behavior. The keyword-only limitation remains, but all detection paths are now auditable.
- R046 is further narrowed: clean-environment reproducibility now covers both the ReplyPlanner surface (T150) and direct policy engine behavior (T151). T152 must still add feedback CLI regression tests.
- R035 remains active: T151 tests policy detection wiring and safety surface, not naturalness.
- T151 also corrected `baseline_friend_context` fixture which inadvertently contained boundary cue keywords ("low pressure", "do not push"), making it not a clean baseline. This is a fixture correction, not a planner behavior change.

Closed question Q130: T151 is complete as a policy fixture suite task. Direct `ReplyPlanPolicyEngine` behavior now has committed deterministic test coverage including build_profile, assess_candidate, over-proactivity, impersonation risk, no-pressure exemption, confidence penalties, loaded-but-no-skill vs not_configured thin context, degraded store, and notes_on_candidate_differences.

## Captain Update 2026-05-18 (T150 Review Decision)

Authoritative current risk state after the Captain review of T150:

- R034 can now be closed: priority-rank uniqueness/stability and contact alignment are no longer open regressibility risks because they are now covered by committed deterministic tests.
- R036 is narrowed but remains active: ReplyPlanner regression coverage is now committed, but the full M3/M4 hardening target still depends on T151 and T152.
- R037 remains active but is narrower: current keyword-policy false-positive and false-negative behavior is now documented and reproducible, but not yet improved.
- R046 remains active but is narrower: clean-environment reproducibility now exists for the ReplyPlanner slice, but not yet for the full policy-fixture and feedback-CLI surface.

## Captain Update 2026-05-17 (T150)

Authoritative current risk state after T150 ReplyPlanner regression tests:

- R036 is narrowed: T150 adds 49 committed deterministic tests and 7 synthetic fixture contexts covering candidate structure, privacy leakage, contact alignment, ranking invariants, thin-context behavior, boundary/sensitive behavior, false-positive boundedness, false-negative documentation, not-configured path, and non-approved id isolation. ReplyPlanner contract wiring is now regression-guarded from committed repo contents alone.
- R034 is narrowed: priority_rank uniqueness/stability and contact_id alignment now have committed regression tests. Can be closed after T150 review confirms coverage is adequate.
- R037 is narrowed: false-positive and false-negative keyword policy behavior is now documented in committed tests that encode current expected behavior. The keyword-only limitation remains, but the behavior is reproducible and auditable.
- R046 is narrowed: ReplyPlanner is now reproducible from committed tests. T151 (policy fixture suite) and T152 (feedback CLI regression tests) must still add corresponding committed coverage before M5 is authorized.
- R035 remains active: T150 tests contract wiring and safety surface, not naturalness. Relationship-aware quality is still template-driven. Naturalness claims remain prohibited.

Closed question Q129: T150 is complete as a regression hardening task. ReplyPlanner M3 Conditional obligations now have committed deterministic test coverage.

## Captain Update 2026-05-17

Authoritative current risk state after T142 review and the Captain M4 review:

- R044 remains active: `reply_plan_id` coherence is still not cross-checked against loaded plan context. T142 stayed descriptive and aggregate-only, but did not remove this gap.
- R045 remains active: T141 validation `record_results` can still become verbose on large logs. T142 avoided re-printing raw per-record payloads, but T152 should still regression-test compact behavior.
- R046 is active: M3/M4 clean-environment reproducibility is still not proven from committed repo contents alone. T150-T152 must add committed synthetic fixtures and deterministic regression tests before M5 is allowed.

Closed question Q127: T142 is accepted with `PASS_WITH_WARNINGS`, so the project may treat M4 implementation scope as complete rather than sending T142 back for a blocking fix pass.

Closed question Q128: the Captain M4 review is `Conditional`, so the next step is M4.5/T150 regression hardening, not M5 feedback-to-patch work.

## Captain Update 2026-05-17

Authoritative current risk state after T140 review:

- R042 is active: a corrupted T140 feedback log can currently be silently replaced during append, creating a data-loss risk. T141 should surface this explicitly and T152 should eventually regression-test it.
- R043 is active: T140 path handling is still too loose for long-term trust. `source_plan_path` can become stale and `--output` is not yet enforced to remain private. T141 should validate and warn; T152 can harden with committed regression coverage.

Closed question Q125: T140 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T141 rather than sending the task back to worker for a blocking fix pass.

- R044 is active: `reply_plan_id` coherence is still not cross-checked against the loaded plan context. T142 may summarize it, but should not overstate it.
- R045 is active: T141 `record_results` can become verbose on large logs. T142 should keep summary output compact and aggregate-only.

Closed question Q126: T141 is accepted with `PASS_WITH_WARNINGS`, so the project may proceed to T142 rather than sending the task back to worker for blocking repair.

## Captain Update 2026-05-16

Authoritative current risk state after T133/M3 review:

- R035 remains active but is narrowed: T133 holdout partially verifies structure and safety behavior, not relationship-aware maturity. Naturalness is 3/5 and evidence usage is 3/5, so maturity claims remain prohibited.
- R036 remains active: T131-T133 still lack committed regression tests/fixtures. T150 must cover ReplyPlanner contract, policy detection, privacy leakage, contact alignment, ranking, boundary sensitivity, thin context, false positives, and subtle false negatives.
- R037 remains active: T133 observed both false-positive and subtle false-negative probes, so keyword/substr policy risk must be carried into T150 or later refactor.
- R038 is active: M4 feedback logs may be mistaken for automatic learning. T140 must record feedback only and must not mutate ContactSkill/Memory, planner templates, or outbound behavior.

Closed question Q123: Gate M3 is `Conditional`; T140 may proceed only under review-only constraints and with T150 regression tests carried forward.

## Captain Update 2026-05-16: Roadmap Risks

- R039 is active: adopting the updated GPT roadmap too aggressively could reintroduce platform/external-memory scope creep. Mitigation: task board now delays Mem0, Feishu, WeChat, BehaviorPlanner, and LLM drafting behind explicit gates.
- R040 is active: ContactSkill decomposition could accidentally become a breaking replacement. Mitigation: M6 is defined as compatible projection with fallback, not deletion.
- R041 is active: feedback-to-patch could be mistaken for automatic learning. Mitigation: M5 patches remain candidate/review-only and require supporting feedback ids.

Closed question Q124: the updated GPT roadmap is directionally aligned, but M4/M5+ tasks needed revision to preserve feedback-first and regression-first sequencing.

更新日期：2026-05-16

## Active Risks

| ID | 风险 | 影响 | 当前缓解 |
| --- | --- | --- | --- |
| R001 | WeFlow JSONL 字段结构与预期不一致 | parser 和 normalized event 合约不稳定 | T100 先做 schema profiling，不直接实现蒸馏 |
| R002 | 私密聊天内容泄露到可提交目录 | 严重隐私风险 | `private/` 受 `.gitignore` 保护；T100 禁止输出原文和真实标识 |
| R003 | sender_role/direction 判断错误 | 事实归因错位，ContactSkill 失真 | T100 明确方向规则；M1 人工抽查 evidence |
| R004 | LLM 编造关系判断 | 产生错误记忆和越界回复 | 所有 claim 必须有 evidence refs，validator 拦截无证据输出 |
| R005 | 单次情绪/聊天被误判为长期模式 | 关系状态过拟合 | M1 区分单次现象与稳定模式，M2 引入 status/review |
| R006 | 过早引入向量库、UI、实时接入或微调 | 拖慢核心验证 | M0-M1 只做离线 MVP |
| R007 | ContactSkill 被误用为联系人模拟器 | 冒充/数字克隆风险 | 文档和 planner 明确只辅助用户回复，不模拟联系人 |
| R008 | 用户手动迁移 docs 后 git 状态复杂 | 误删或覆盖用户文件 | 不 revert 未确认变更，只基于现有路径更新 |
| R009 | T01 review BLOCK 未修复 | 旧 iLink 路线 Gate 0 不通过 | 用户已决定暂停旧路线，不作为当前阻塞项 |
| R010 | `meta.type=private` 的导出里仍可能出现大量 `member` 行 | 若简单按成员数判断方向，会导致 `sender_role` 判错 | T100 contract 已要求用跨文件复用身份和 message 高频对来判定 user/contact |
| R011 | 当前脱敏 fixture 仍未覆盖 `type=80`/`chatRecords` 的合成输入样例 | T150 前的测试覆盖仍可能不足 | T103 worker draft 认为这不阻塞 M1；T110/T150 必须延续保守处理并补 fixture / 测试 |
| R012 | `event_id` 当前最小实现继续采用 SHA-1 命名空间输入 | 长期可追溯 ID 规则可能需要更强或更明确的稳定性/隐私说明 | T103 worker draft 认为 M1 可先继续使用该规则；若 reviewer 或 T150 测试要求更强摘要，再统一升级 |
| R013 | T101 的结构化替换 token 未在 normalize 阶段实现 | 若后续 LLM 蒸馏直接使用原文，可能出现 PII 泄露风险 | T102 review 认为 normalize 私有输出保留原文合理；PII token 替换 deferred 到 T112+ 蒸馏阶段 |
| R014 | T102 normalize 当前双次读取文件并全量缓存 normalized lines | 大规模聊天记录可能出现性能或内存瓶颈 | T103 worker draft 认为对当前 38k 行样本可接受；T110/T150 继续评估是否需要流式化 |
| R015 | 单文件数据场景下 `sender_role` 推断可能退化 | 其他用户或单联系人样本可能出现 user/contact 归因不稳 | T103 worker draft 认为这不阻塞进入 T110；T114/T150 需用实际样本验证并保留 `risk_flags` 兜底 |
| R016 | T112+ 若不消费 T110 保留的不确定性信号，仍可能在摘要/事实抽取中抹平风险 | 后续摘要/事实抽取可能忽略 `risk_flags`、`interaction_flags` 或原始 message type 的不确定性 | T110 review 已确认 chunker 保留/汇总传递相关信号；T112 schema 与抽取逻辑必须显式承接这些字段 |
| R017 | T110 chunker 尚缺自动化测试覆盖 | 边界切分、异常 timestamp、report 形态或隐私泄漏可能在后续改动中回归 | T110 reviewer 判定不阻塞；T150 必须补 chunker fixture/unit tests 与 privacy leakage smoke test |
| R018 | `chunking_reason` 对 conversation/contact 结构边界表达偏粗 | 后续模块若只看 reason 而忽略 `boundary_flags`，可能误解 chunk 边界含义 | T110 reviewer 判定不阻塞；T112/T113/T150 使用 chunk 时应优先读取 `boundary_flags` 和统计字段 |
| R019 | T111 schema 的部分 ContactSkill 风格字段仍是自由字符串 | 后续 LLM 输出可能出现枚举漂移，影响 review 和统计一致性 | T111 reviewer 判定 MVP 可接受；T112/T113 记录实际输出形态，T150 或后续 schema 收紧为 `Literal` |
| R020 | `redaction_policy` 当前为 `dict[str, Any]` | 缺少字段级校验，后续 store/review 可能出现策略键不一致 | T111 reviewer 判定不阻塞；T120/T150 可改为结构化 Pydantic model |
| R021 | `DistillationMemoryType` 与现有运行时 `MemoryType` 未统一 | approved memory candidate 入库时可能需要映射，若未处理会造成类型不一致 | T120 负责定义 `MemoryFactCandidate` -> `MemoryFact` 映射 |
| R022 | T111 candidate schema 暂无 `created_at` / `updated_at` | 文件 store、审阅和版本追踪可能缺少生成/更新时间 | T120 store 或产物写入层补充时间戳 |
| R023 | T111 Pydantic 约束尚缺自动化测试 | `evidence_refs` 非空、`confidence` 范围等约束未来可能回归 | T150 补合法/非法 JSON 的 Pydantic 校验测试 |
| R024 | T112 实测发现 provider 返回 JSON 形状会漂移，可能使用 `predicate/object/high` 一类字段，而不是直接命中 T111 schema | 若没有兼容归一化层，真实小样本会在 schema 校验前失败，导致 distillation 无法写出 | T112 已加入 provider 输出归一化层并在 `private/distilled/t102_smoke` 小样本验证通过；T150 仍应补充 provider shape drift 回归测试 |
| R025 | T112 evidence refs fallback 允许使用 `chunk_id` 作为粗粒度证据 | claim 可能缺少 event_id 级证据，后续人工审阅时证据精度不足 | T112 reviewer 判定不阻塞；T114 统计仅 chunk_id 级 evidence 的比例并人工抽查 |
| R026 | T112 sensitivity 与 memory_type fallback 使用关键词兜底 | 可能出现敏感度低估或 memory type 误分类 | MVP 可接受；T114/T150 观察误分类并补充测试或收紧规则 |
| R027 | T112 LLM 管线缺少自动化测试 | schema 校验、evidence refs 范围、PII 脱敏、provider 归一化未来可能回归 | T150 必须补充自动化测试 |
| R028 | T113 ContactSkill builder 的启发式 tokens/topic/relationship 推断偏当前小样本 | 换联系人或更大样本时，preferred topics、avoid topics、relationship_type 等可能为空或误导 | T113 reviewer 判定不阻塞；T114 必须用样本 run 观察泛化，T120+ 可考虑 LLM-assisted inference |
| R029 | T113 confidence/closeness/trust 数值由公式生成，未按 evidence quality 加权 | 人工 reviewer 可能误读为精确关系量化，导致过度信任 candidate | T113 reviewer 判定 candidate-only 可接受；T114 检查数字是否显得过度精确，T120+ 重设评分策略 |
| R030 | T114 样例虽然 evidence chain 完整，但 reflection / reply-strategy 类 claim 已出现“短证据 -> 平滑 paraphrase”压缩 | 若后续样例更复杂，reviewer 可能高估 claim 的稳健度，进而放大 ContactSkill 中的策略推断 | T114 记录为 `Conditional`；M2 前保持 candidate-only / human-review-first，并在更广样例上继续抽查 |
| R031 | T120 file store 缺少已提交自动化测试 | store model validation、legacy wrapping、load/save round-trip、runtime-ready gate 或 path confinement 未来可能回归 | T120 reviewer 判定不阻塞；T150 必须补对应单测和 path confinement 测试 |
| R032 | T121 evidence validator 缺少已提交自动化测试 | evidence index、nested `evidence_refs` collection、status gate 或 path confinement 未来可能回归 | T121 reviewer 判定不阻塞；T150 必须补 validator 单测与 good/bad fixture 覆盖 |
| R033 | T122 review CLI 缺少已提交自动化测试 | approval gate、reject/freeze/archive、review history、stable record_id 或 export confinement 未来可能回归 | T122 reviewer 判定不阻塞；T150 必须补 full approval lifecycle 与 no-auto-approve 测试 |
| R034 | T130 ReplyPlan 可能出现重复 `priority_rank`，且 `ReplyPlanSourceContext` 可能与 `ReplyPlan.contact_id` 在组装时错位 | 候选排序会歧义，或出现跨联系人上下文串线 | T131 已实现唯一排序与 contact 对齐校验；T150 仍需补回归测试，确认后可关闭 |
| R035 | T131/T132 候选草稿仍主要由 deterministic templates 驱动，relationship-aware 质量尚未通过 holdout 验证 | “relationship-aware” 质量可能被高估，候选可能显得泛化或不够贴合真实关系边界 | T132 已把 boundary / avoid topics / over-proactivity 转成风险控制；T133 必须用匿名 holdout 评估自然度、边界遵守和证据使用 |
| R036 | T131/T132 只有 inline synthetic verification，尚无 committed test/fixture | 干净环境和后续重构存在回归风险 | T150 必须补 ReplyPlanner contract、policy detection、privacy leakage、contact alignment 和 ranking tests；T133 可先记录匿名化人工评估结果 |
| R037 | T132 policy layer 使用 substring keyword matching，可能出现 false positives | 某些普通文本可能被误判为敏感、过度主动或边界场景，导致候选过度保守 | T133 holdout eval 记录 false-positive / false-negative 样例；T150 或后续 refactor 可引入更精确的匹配规则 |
| R038 | M4 feedback log 可能被误解为自动学习或自动记忆更新 | 用户反馈若被直接应用，可能绕过 human-review-first 和 evidence/versioning 约束 | T140 只允许记录 private feedback，不得自动修改 ContactSkill/Memory、planner templates 或 outbound behavior；T141/T142 才能在 reviewable proposal/versioning 范围内继续 |
| R039 | 更新版路线图若被过度提前执行，可能重新引入平台接入、外部 memory 或 LLM scope creep | 破坏当前 offline-first / review-only / evidence-first 安全骨架 | Task board 已把 Mem0、Feishu、WeChat、BehaviorPlanner、LLM drafting 延后到 M7-M12，并要求先通过 M4/M4.5/M5/M6 gates |
| R040 | ContactSkill decomposition 可能被误执行成 breaking replacement | 现有 T113/T120-T123/T130-T133 evidence pipeline 和 runtime context 可能失效 | M6 明确定义为 compatible projection；保留 ContactSkill 作为 legacy aggregate / evidence bundle，并要求 fallback |
| R041 | Feedback-to-Patch 可能被误解为自动学习 | 单条反馈可能被过度泛化并污染长期回复策略 | M5 patches 必须保持 candidate/review-only，包含 supporting_feedback_ids，不自动 approve、不自动 runtime injection |
| R047 | `instruction_scope` 和 `affected_candidate_types` 仍为自由字符串 | T162+ 可能出现拼写漂移或语义不一致 | T160 schema-only 阶段可接受；T162/T163 使用后观察实际值再决定是否收紧 |
| R048 | `positive_examples` / `negative_examples` 无结构化安全约束 | 可能被后续实现误用于存储原始反馈文本 | T162 提案生成必须只写入安全摘要或引用，不得写入原始反馈、编辑文本或私密备注 |
| R049 | `PreferencePatchCandidate` 尚无已提交的自动化验证测试 | 后续 schema 演进或 review/runtime 接入时，字段约束可能无声回归 | T160 review 接受其当前 scope，但后续 hardening task 应补 valid/invalid construction、runtime-ready gate、confidence range、JSON round-trip 等回归测试 |
| R050 | `edit` action 反馈记录当前无安全确定性聚类标签 | edit 记录不参与聚类，可能遗漏重要的用户偏好信号 | T161 仅对 accept/reject/boundary 生成标签；T162 或后续 hardening task 需决定是否为 edit 派生标签或采用不同策略 |
| R051 | cluster_id 仅反映分组键不反映记录内容 | 不同记录集可能共享同一 cluster_id | T161 设计为累积分组，T162 使用时应同时检查 supporting_feedback_ids 而非仅依赖 cluster_id |
| R052 | `FeedbackClusterService` / `chat-feedback-cluster` 尚无已提交的自动化回归测试 | 聚类标签、cluster_id 稳定性、过滤规则或隐私输出约束未来可能无声回归 | T161 review 接受当前 scope；后续 hardening task 应补有效/无效聚类、cluster_id 稳定性、validation-report 过滤、隐私字段缺失、JSON round-trip 与单记录边界情况测试 |
| R053 | `patch_id` 使用 UUID 生成，同一 cluster 输入重复运行产生不同 patch_id | patch_id 不稳定可能导致重复生成时无法去重或追踪 | T162 scope 内可接受；T163 review CLI 或后续 hardening task 可改为基于 cluster_id 的确定性 ID |
| R054 | M5 patch pipeline 自动化覆盖仍不完整：T162/T163/T164 已有实现，但 proposal/review/context 路径仍存在回归覆盖缺口 | 提案映射规则、review 写回行为、approved-patch context 过滤与组装路径可能在未来无声回归 | T162-T164 review 均接受当前 scope；后续 hardening task 应补 proposal/review 端到端覆盖、frozen/archived exclusion、assembler integration、empty/whitespace `behavior_instruction`、隐私字段与 JSON round-trip 测试 |
| R055 | 置信度公式 `min(0.3 + 0.15 * (record_count - 1), 0.9)` 单调但未校准 | 置信度值可能被误解为概率 | T162 文档已明确说明不 claim 校准概率；T163 review CLI 展示时需避免过度解读 |
| R056 | 提案生成对 malformed cluster report 缺少空 `contact_id` 防御 | 手工编辑或损坏的 cluster report 可能触发未处理异常并中断 proposal 生成 | T162 review 接受当前 scope；后续任务应在 proposal 层显式跳过 `contact_id` 为空的 cluster，给出 `missing_contact` 或等价 skip reason |
| R059 | `ApprovedPatchContextService` loads the full proposal report into memory | 对于包含大量候选的 proposal report 可能产生内存压力 | 当前单用户离线规模可接受；未来若 report 过大，可改为 streaming 或分页加载 |
| R060 | `ChatContextAssembler` patch path 校验复用 `_ensure_within_private_distilled` | 该方法约束路径在 `private/distilled/` 下，提供约定级隔离而非硬安全边界 | 当前 offline-only 工作流可接受；若未来引入多用户或网络暴露场景，需采用更严格的路径沙箱 |
| R062 | T181 privacy leak detection only checks normalized substring overlap | Verbatim echo can be caught, but paraphrased or partial-detail leakage may still pass validation and reach private review artifacts | T182 should harden deterministic leak detection and add regression coverage that proves safe rejection on richer leak patterns |
| R063 | `INPUT_TOO_LARGE` preflight exists but the T182 call site passes `str(estimated_size)` instead of the serialized payload | Oversize compact-context input still falls through to provider-error handling, so the dedicated deterministic refusal path remains non-functional despite appearing implemented | T183 or a narrow follow-up should fix the call site and add a regression test that proves `INPUT_TOO_LARGE` is returned before provider call |
| R064 | Candidate-path regression coverage is much stronger after T182, but the `INPUT_TOO_LARGE` refusal path still lacks committed coverage | The current preflight bug could persist or regress silently even though most validator/generator branches are now protected | Add a dedicated refusal-path regression test before or during T183 so hybrid integration does not build on an unverified preflight |
| R065 | T183 hybrid merge success path is only smoke-validated, not committed-test validated | A refactor could break valid LLM candidate merging, reranking, or policy assessment without immediate regression signal | Add a committed synthetic valid-candidate merge test before relying on the hybrid path for broader evaluation claims |
| R066 | T184 holdout showed hybrid LLM candidates defaulted to English while template candidates remained Chinese | This was a real UX gap during T184 and was addressed by T185 language alignment | Closed by T185 |
| R067 | T184 holdout showed thin_context / boundary_sensitive policy flags did not always constrain LLM draft text | This was a real safety-gap exposure during T184 and was addressed by T185 prompt-level constraints | Closed by T185 |
| R068 | T184 holdout showed hybrid `approach_label` values were not normalized to the template naming convention | This was a real downstream-consistency gap during T184 and was addressed by T185 label normalization | Closed by T185 |
| R069 | T185 safety-context detection remains heuristic rather than policy-engine-native | Hybrid LLM safety alignment could drift if prompt-side heuristics and planner-side policy semantics diverge | Track as deferred hardening; do not treat T185 prompt behavior as a substitute for policy-engine-native enforcement |
| R070 | T185 Chinese output alignment is prompt-level rather than hard post-generation enforcement | A provider could still return non-Chinese text in edge cases, creating review UX inconsistency | Track as deferred hardening; current scope accepts prompt alignment but does not claim hard language enforcement |
| R071 | LLM candidate confidence remains uncalibrated | Reviewers could over-read high confidence values as probabilities or production readiness | Keep documented as non-probabilistic confidence; revisit only if later milestones rely on calibration-sensitive ranking |
| R072 | `RelationshipDeltaDimension.magnitude` defaults to a free value and is not enforced to match `abs(proposed_value - current_value)` | Future delta-generation or review code could consume internally inconsistent deltas unless it recomputes or validates magnitude explicitly | T192 or later hardening should compute/validate magnitude explicitly before downstream consumers rely on it |
| R073 | `RelationshipDeltaDirection=\"stable\"` exists without contract guidance | T192/T193 could disagree on whether a "stable" entry is a real delta, a no-op, or an invalid review artifact | T192 should either avoid generating stable deltas or document exact semantics before T193 review flow depends on them |
| R074 | No committed automated tests yet cover `RelationshipState` / `RelationshipDeltaCandidate` validation or helpers | Schema regressions in bounds, required evidence, runtime-ready gating, or helper behavior could slip in silently | Add committed schema validation tests in a later M8 hardening slice or when T191/T192 introduce executable signal/delta flows |
| R075 | `RelationshipSignal` lacks an `updated_at` field | Later approval/update flows for signals will not have an explicit mutation timestamp unless another task adds one | T193 or a follow-up can add `updated_at` if mutation timing becomes important |
| R076 | No committed automated test exercises an approved `RelationshipSignal` runtime-ready path | The approval→runtime-ready transition on signals could regress without a direct test | Add a committed lifecycle test when T193 makes signal review/update behavior executable |
| R077 | No committed automated test covers `RelationshipSignal.signal_id` format or non-emptiness | Signal id generation would remain untested at the model boundary | Add a dedicated model test when signal schema hardening is revisited |
| R078 | No committed test confirms that unknown dimension names are skipped safely by T192 | A malformed or future signal dimension could regress from safe-skip behavior without direct test coverage | Add a dedicated T192 regression test for unknown dimensions before or during later M8 hardening |
| R079 | No committed test covers mixed known-direction plus unknown/stable companion signals on the same dimension | Future refactors could unintentionally change the tolerance for unknown/stable companions in an otherwise valid signal group | Add a dedicated aggregation test when T192/T193 hardening is revisited |
| R080 | No committed test covers the state-evidence-only deduplication edge case for T192 | A future change could allow empty `evidence_refs` to emerge after deduplication, violating the delta contract | Add a defensive test and, if needed, guard logic before relying on broader signal sources |
| R081 | T192 uses heuristic `_MAGNITUDE_SCALE` / `_MIN_STRENGTH` defaults and max-strength aggregation | Delta magnitudes may be reviewable and conservative, but they are not empirically calibrated and may underuse corroborating signals | Keep candidate-only and human-reviewed for now; revisit calibration/aggregation only if later milestones need denser signal use |
| R082 | T193 has an open design question around dimension-level partial approval | If a delta changes multiple dimensions, review semantics could become ambiguous unless the CLI enforces all-or-nothing or explicitly supports partial approval | T193 should document and implement one review model explicitly rather than leaving this implicit |
| R083 | T193 has no committed CLI-level integration tests | Typer wiring, file I/O, JSON error handling, and safe-path output could regress even though the service layer is covered | Add committed CLI regression tests before or during later M8 hardening if the command becomes a relied-on operational path |
| R084 | T193 approvals do not run an evidence pre-validation gate | Later tasks could over-assume that an approved delta also has fresh, resolvable evidence refs | T194/T195 and any future state-application task should treat approval as human review only, not as evidence validation |
| R085 | T193 has no explicit empty-string note regression test | The note-normalization edge path could change silently without direct coverage | Add a narrow test when CLI/service hardening is revisited |
| R086 | T194 summary truncation is not directly tested | Very long multi-dimension summaries could change formatting without regression signal | Add a narrow truncation test if context verbosity grows |
| R087 | T194 path-is-directory branch is not directly tested | File-vs-directory misconfiguration could regress silently | Add a branch test if runtime configuration for relationship context becomes relied upon |
| R088 | T194 empty `delta_rationale` input is not directly tested | An empty rationale could change summary behavior without direct coverage | Add a narrow test when context hardening is revisited |
| R089 | T194 reads a directory of relationship delta JSON files rather than a store-file abstraction | The current design is fine for scope but may become awkward if delta volume or lifecycle complexity grows | Revisit abstraction only if later milestones need a richer relationship-delta store model |
| R090 | T194 lacks AppContainer wiring | Relationship context is only configurable programmatically, not via central app configuration | Add wiring later if runtime configuration becomes a real operational need |
| R091 | Approved relationship context is present in `ChatContext` but not consumed by `ReplyPlanner` or `ReplyPlanPolicyEngine` | M8 can be over-read as relationship-aware reply behavior even though approved deltas currently have zero behavioral effect | Keep documented as a functional gap; only a later scoped planner/policy task may claim to close it |
| R092 | Relationship guidance reaching summary and retrieval-note surfaces is informational only | Future readers may mistake visible context text for active runtime semantics and overstate current capability | Do not treat summary or retrieval notes as semantic consumption; add explicit planner integration only in a later scoped task |
| R093 | Future M11 code could accidentally interpret `CandidateAction.status`, `review_state`, or `is_runtime_visible()` as outbound authorization | T220 separated `OutboundMessageRequest` from `CandidateAction`, but later gate/adapter code could still accidentally consume candidate review state as send permission | T221 and later tasks must require explicit `OutboundMessageRequest.human_approval` and `send_gate` state; `CandidateAction` remains evidence only |
| R094 | Offline CLI path metadata and default in-place overwrite remain accepted conventions | Future operational workflows could expose private names in paths or increase overwrite risk if reused outside local offline review | Prefer explicit output paths and safe path metadata in future M11 operational tasks |
| R095 | M10/T220 do not evaluate platform delivery, notification UX, send audit UX, adapter failure recovery, or scheduler behavior | The project could overstate readiness for real delivery after defining request/gate contracts | Keep adapter, scheduler, and delivery claims behind T222+ reviewed tasks and later milestone gates |
| R096 | T221 could blur "gate allowed" with "message delivered" | A gate decision should be an audit/policy state only; treating it as delivery would bypass T222/T223/T224 review boundaries | T221 must not create adapters, send paths, schedulers, background jobs, or runtime delivery side effects |
| R097 | T221 named-timezone verification on Windows depends on `tzdata`, but `tzdata` is not declared in project dependencies | Fresh Windows environments may fail timezone tests or runtime named-zone evaluation even though the worker environment had `tzdata` installed | Future tasks should either add `tzdata` explicitly or keep new tests/config on UTC-only paths and document the choice |
| R098 | T222 fake-adapter `payload_preview` truncation is not a privacy boundary | Future real or sandbox adapters could incorrectly treat truncated previews as sufficient redaction or safe payload handling | T223+ must build platform payloads only from approved outbound request text and explicit recipient mapping; preview fields are for audit summaries only |
| R099 | T223 Feishu sandbox payload shape is not production API validation | The sandbox adapter builds a Feishu-shaped payload for dry-run / injected fake transport, but production API compatibility, acknowledgement semantics, retries, and recovery were not validated | Future production Feishu delivery work must verify current official Feishu API contract, auth, callback, ack/error, retry, and recovery semantics before claiming real delivery |
| R100 | T224 Feishu review-card payload/action parser is not real callback validation | Local card payloads and synthetic action mappings can diverge from current Feishu interactive-card callback/event payloads | Future real Feishu callback or approval-application work must validate official event schemas, signatures, auth, idempotency, replay handling, and audit behavior before claiming production integration |
| R101 | M12 could accidentally revive paused personal-WeChat scan/login/realtime SDK work | The repository rules prohibit resuming the old scan/login SDK track, vendoring unofficial SDK code, or adding realtime platform integration without explicit scoped approval | T230 blocked unsafe paths; T231 must stay synthetic WeCom Customer Service contract-only and must not add personal-WeChat, scan-login, desktop automation, or unofficial SDK behavior |
| R102 | Official WeChat-family documentation may drift after T230 retrieval | A future implementation could rely on stale API, callback, credential, quota, or service-window facts | T231 and later tasks must recheck official docs before touching provider semantics; if docs cannot be checked, mark those facts unresolved |
| R103 | WeCom Customer Service does not cleanly map to personal WeFlow chat contacts | M12 could overclaim that official customer-service identity equals arbitrary personal WeChat contact identity | T231 uses only synthetic provider aliases and does not create contact/recipient mapping; mapping requires a later reviewed task |
| R104 | `channel_preference="wechat"` is too broad for production adapter selection | A later outbound adapter could accidentally route to the wrong WeChat-family surface | Future outbound work needs explicit selected surface/subchannel or adapter config before any payload preparation or send path |
| R105 | No live WeCom account, tenant, app, callback URL, credential flow, recipient mapping, service window, delivery callback, or provider failure handling has been tested | M12 cannot claim operational readiness or delivery semantics | Keep T233 provider-safety-only; keep T232 live outbound blocked until provider-safety, tenant, credential, and recipient prerequisites are reviewed |
| R106 | T231 timestamp fallback uses Unix epoch for missing or unparseable provider timestamps | Future live inbound/sync work could confuse invalid timestamp data with a real 1970 timestamp | T233 is unaffected; any future live inbound task must require valid timestamps or use an explicit invalid-timestamp sentinel |
| R107 | T231 parses only the first `msg_list` item | Future live `sync_msg` responses may carry multiple messages and would be under-processed if reused as-is | Define batching semantics before any live callback/sync integration |
| R108 | T231 stores synthetic source payloads in `InboundEvent.raw` | A future live adapter could leak real provider IDs or callback bodies if it reuses raw storage without redaction | Keep current raw storage synthetic-only; define redaction before live provider payload storage |

## Open Questions

| ID | 问题 | 需要谁回答 | 最晚解决点 |
| --- | --- | --- | --- |
| Q205 | Can T233 define a deterministic local WeCom Customer Service provider safety gate that blocks unsafe outbound eligibility before any payload preparation or delivery? | T233 worker + reviewer + Captain review | Before T232 can be rewritten as dry-run outbound payload preparation |

## Closed Questions

| ID | 结论 | 关闭依据 |
| --- | --- | --- |
| Q204 | T231 can be accepted as complete. It normalizes synthetic WeCom Customer Service message/event fixtures into `InboundEvent` without live platform behavior, private reads, store mutation, runtime wiring, outbound payloads, or sending. | `docs/review/T231_review.md` + Captain decision |
| Q203 | T230 can be accepted as complete and M12 may proceed only as `Gate M12 Conditional`. Generic personal-WeChat adapter work remains blocked; Captain selects WeCom Customer Service for T231 synthetic inbound contract work. | `docs/review/T230_review.md`, `docs/review/T230_wechat_adapter_research.md` + Captain decision |
| Q202 | T224 can be accepted as complete, M11 can close at task level with `Gate M11 Allow` for local/sandbox outbound safety only, and the project may proceed to T230. It is accepted with `PASS`; all review observations are accepted, with no deferred risks or repair pass. | `docs/review/T224_review.md` + Captain decision |
| Q201 | T223 can be accepted as complete and the project may proceed to T224. It is accepted with `PASS`; all review observations are accepted, with no deferred risks or repair pass. | `docs/review/T223_review.md` + Captain decision |
| Q200 | T222 can be accepted as complete and the project may proceed to T223. It is accepted with `PASS`; all review observations are accepted, with no deferred risks or repair pass. | `docs/review/T222_review.md` + Captain decision |
| Q199 | T221 can be accepted as complete and the project may proceed to T222. It is accepted with `PASS`; all review observations are accepted, with no deferred risks or repair pass. | `docs/review/T221_review.md` + Captain decision |
| Q198 | T220 can be accepted as complete and the project may proceed to T221. It is accepted with `PASS`; all review observations are accepted, with no deferred risks or repair pass. | `docs/review/T220_review.md` + Captain decision |
| Q197 | T214 can be accepted as complete, M10 may close with `Gate M10 Allow`, and the project may proceed to T220. | `docs/review/T214_review.md`, `docs/review/M10_review.md` + Captain decision |
| Q195 | T212 can be accepted as complete and the project may proceed to T213. It is accepted with `PASS`; all review observations are accepted, with no deferred risks or repair pass. | `docs/review/T212_review.md` + Captain decision |
| Q194 | T211 can be accepted as complete and the project may proceed to T212. It is accepted with `PASS`; all review observations are accepted, with no deferred risks or repair pass. | `docs/review/T211_review.md` + Captain decision |
| Q193 | T210 can be accepted as complete and the project may proceed to T211. It is accepted with `PASS`; all review observations are accepted, with no deferred risks or repair pass. | `docs/review/T210_review.md` + Captain decision |
| Q192 | T203 can be accepted as complete and M9 can close at task level. It is accepted with `PASS`; all review observations are accepted, with no deferred risks or repair pass. The next task is T210. | `docs/review/T203_review.md` + Captain decision |
| Q191 | T202 can be accepted as complete and the project may proceed to T203. It is accepted with `PASS`; all review observations are accepted, with no deferred risks or repair pass. | `docs/review/T202_review.md` + Captain decision |
| Q190 | T201 是否可以作为已完成任务接受并推进到 T202？可以；以 `PASS` 接受，所有 review observations 均为 accepted，无 deferred 风险或 repair pass。 | `docs/review/T201_review.md` + Captain decision |
| Q189 | T200 是否可以作为已完成任务接受并推进到 T201？可以；以 `PASS` 接受，所有 review observations 均为 accepted，无 deferred 风险或 repair pass。 | `docs/review/T200_review.md` + Captain decision |
| Q183 | T190 是否可以作为已完成任务接受并推进到 T191？可以；以 `PASS_WITH_WARNINGS` 接受，deferred 项转入 M8 风险台账并由 T191/T192+ 承接。 | `docs/review/T190_review.md` + Captain decision |
| Q184 | T191 是否可以作为已完成任务接受并推进到 T192？可以；以 `PASS_WITH_WARNINGS` 接受，deferred 项转入 M8 风险台账并由 T192/T193+ 承接。 | `docs/review/T191_review.md` + Captain decision |
| Q185 | T192 是否可以作为已完成任务接受并推进到 T193？可以；以 `PASS_WITH_WARNINGS` 接受，deferred 项转入 M8 风险台账并由 T193+ 承接。 | `docs/review/T192_review.md` + Captain decision |
| Q186 | T193 是否可以作为已完成任务接受并推进到 T194？可以；以 `PASS_WITH_WARNINGS` 接受，deferred 项转入 M8 风险台账并由 T194+ 承接。 | `docs/review/T193_review.md` + Captain decision |
| Q187 | T194 是否可以作为已完成任务接受并推进到 T195？可以；以 `PASS_WITH_WARNINGS` 接受，deferred 项转入 M8 风险台账并由 T195+ 承接。 | `docs/review/T194_review.md` + Captain decision |
| Q180 | Gate M7 是否已经可以关闭并进入 M8？还不可以；它仍是 `Conditional`，必须先完成 T185 的窄范围对齐修复。 | `docs/review/T184_milestone_review.md` + Captain decision |
| Q179 | T184 是否可以作为已完成任务接受并推进到 T185？可以；以 `PASS_WITH_WARNINGS` 接受，holdout 证据有效但 gate 仍 `Conditional`。 | `docs/review/T184_review.md` + Captain decision |
| Q178 | T183 是否可以作为已完成任务接受并推进到 T184？可以；以 `PASS_WITH_WARNINGS` 接受，deferred 项收敛到 hybrid merge success test 缺口。 | `docs/review/T183_review.md` + Captain decision |
| Q177 | T182 是否可以作为已完成任务接受并推进到 T183？可以；以 `PASS_WITH_WARNINGS` 接受，deferred 项收敛到 `INPUT_TOO_LARGE` 预检 bug 及其测试缺口。 | `docs/review/T182_review.md` + Captain decision |
| Q176 | T181 是否可以作为已完成任务接受并推进到 T182？可以；以 `PASS_WITH_WARNINGS` 接受，deferred 项转入 validator/privacy/test hardening 风险。 | `docs/review/T181_review.md` + Captain decision |
| Q001 | SDK 包名为 `wechatbot-sdk`，验证版本 `0.2.1`，导入路径为 `from wechatbot import WeChatBot`。 | T00 notes + T00 review |
| Q002 | 是否继续修微信扫码登录？不继续。 | 用户本轮明确跳过微信聊天记录扫描/SDK路线 |
| Q100 | WeFlow 顶层行类型稳定分为 `header`、`member`、`message`；normalized event 只需要消费 `_type=message`。 | T100 worker draft + `docs/review/T100_review.md` PASS |
| Q104 | 可以生成安全脱敏 fixture，且最小样例不包含真实内容。 | T100 worker draft + `docs/review/T100_review.md` PASS |
| Q101 | T102 使用跨文件 member 对复用、message 高频对、type=80 系统检测、unknown 兜底和 risk_flags 来判定 `sender_role`。 | `docs/review/T102_review.md` PASS |
| Q102 | T102 最小实现默认使用 `Asia/Shanghai` 渲染 normalized timestamp，并保留 `timestamp_epoch_s`。 | `docs/review/T102_review.md` PASS |
| Q103 | T102 最小实现将 `type=7` 保守映射为 `mixed`，将 `type=4/23/24/99` 保守映射为 `unknown`。 | `docs/review/T102_review.md` PASS |
| Q108 | `event_id` 在 T102 保留 SHA-1，但加入 `weflow` 命名空间输入；MVP 可接受，未来可升级。 | `docs/review/T102_review.md` PASS |
| Q109 | T101 的 `[PHONE]`、`[EMAIL]` 等结构化替换 token 不在 normalize 阶段实现，推迟到 T112+ 蒸馏阶段。 | `docs/review/T102_review.md` PASS |
| Q110 | 是否已有隐私脱敏规则和 source_ref/raw_ref 公开形态？已有，T101 已定义 PII 分类、数据区域边界、字段处理矩阵和 allowed public shape。 | `docs/review/T101_review.md` PASS |
| Q111 | T101 fixture preview hex 是否需要返修为真实哈希形态？不需要；作为合成 fixture 注释占位可接受。 | `docs/review/T101_review.md` PASS，N02 accepted |
| Q112 | Gate M0 verdict 为 `Conditional`；允许进入 M1，但 T110/T112+/T114/T150 必须承接条件。 | `docs/review/T103_review.md` accepted worker draft |
| Q113 | T110 conversation chunker v0 是否足以作为 M1 后续输入？足以作为 MVP 输入。 | `docs/review/T110_review.md` PASS |
| Q114 | T111 distillation schemas 是否足以作为 T112 JSON 校验边界？足以作为 MVP schema。 | `docs/review/T111_review.md` PASS |
| Q115 | T112 summary/fact extraction 是否足以支撑 ContactSkill builder？足以作为 T113 的 MVP 输入。 | `docs/review/T112_review.md` PASS |
| Q116 | T113 ContactSkill builder 是否足以支撑 M1 sample review？足以作为 T114 MVP 输入，但带启发式和 confidence warning。 | `docs/review/T113_review.md` PASS_WITH_WARNINGS |
| Q105 | 第一轮 distillation MVP 选哪个联系人或样本？已使用 `private/distilled/t102_smoke` 作为 T114 milestone sample。 | `docs/review/T114_milestone_review.md` worker draft |
| Q106 | LLM 抽取模型、预算和脱敏策略如何处理？T112 已使用配置化 OpenAI-compatible provider/model 路径，并在 prompt 层执行最小 PII token 替换；更完整的 privacy leakage 测试留给 T150。 | `docs/review/T112_review.md` PASS |
| Q107 | ContactSkill review 采用什么形态？M1 采用 Markdown review artifact，CLI review/approve/export 延后到 T122。 | `docs/review/T113_review.md` PASS_WITH_WARNINGS |
| Q117 | Gate M1 是否允许进入下一里程碑？允许以 `Conditional` 进入 M2；必须保持 candidate-only / human-review-first，保留 evidence refs/status，并继续跟踪 R028/R029/R030。 | `docs/review/T114_review.md` + `docs/review/M1_review.md` |
| Q118 | T120 file store 是否足以作为 T121/T122 的基础？足以作为 MVP 基础，但带自动化测试 deferred warning。 | `docs/review/T120_review.md` PASS_WITH_WARNINGS |
| Q119 | T121 evidence validator 是否足以作为 T122 approval gate 的基础？足以作为 MVP 基础；T122 必须读取 validation report 并禁止 missing refs approval。 | `docs/review/T121_review.md` PASS_WITH_WARNINGS |
| Q120 | T122 review CLI 是否足以作为 T123 context integration 的准入基础？足以作为 MVP 基础；T123 必须只读取 approved + runtime-ready records。 | `docs/review/T122_review.md` PASS_WITH_WARNINGS |
| Q121 | T131 是否足以作为 T132 的输入基础？足以作为安全 wiring baseline，但不是质量完成版；T132 必须补 policy/boundary 风险层，M3 仍未完成。 | `docs/review/T131_review.md` PASS_WITH_WARNINGS |
| Q122 | T132 是否足以作为 T133 的输入基础？足以作为 policy/boundary baseline，但不是最终质量证明；T133 必须做匿名 holdout eval 和 Gate M3 判断。 | `docs/review/T132_review.md` PASS_WITH_WARNINGS |
| Q123 | Gate M3 是否允许进入下一里程碑？允许以 `Conditional` 进入 M4/T140，但仅限 review-only feedback capture，并必须把 T150 regression tests 条件带入后续。 | `docs/review/T133_review.md` PASS_WITH_WARNINGS + `docs/review/M3_review.md` |
| Q124 | `gpt的后续设计思路(更新版).md` 是否符合当前项目？方向符合，但必须收敛执行顺序；已将 M4 改为 feedback capture/validate/summary，新增 M4.5 regression hardening，并把 feedback-to-patch、ContactSkill decomposition、LLM planner、RelationshipState、MemoryRetriever、BehaviorPlanner、Feishu、WeChat 延后到 gated milestones。 | Captain roadmap alignment decision + `docs/04_task_board.md` update |
| Q125 | T140 feedback schema CLI 是否可以继续？可以，以 `PASS_WITH_WARNINGS` 接受。 | `docs/review/T140_review.md` PASS_WITH_WARNINGS |
| Q126 | T141 feedback log validator 是否可以继续？可以，以 `PASS_WITH_WARNINGS` 接受。 | `docs/review/T141_review.md` PASS_WITH_WARNINGS |
| Q127 | T142 feedback summary exporter 是否可以继续？可以，以 `PASS_WITH_WARNINGS` 接受。 | `docs/review/T142_review.md` PASS_WITH_WARNINGS |
| Q128 | M4 是否可以进入 M5？不可以，M4 为 `Conditional`，必须先完成 M4.5 regression hardening (T150/T151/T152)。 | `docs/review/M4_review.md` Conditional |
| Q129 | T150 ReplyPlanner regression tests 是否足以减少 R036/R034/R037/R046？足以部分减少：ReplyPlanner contract wiring、privacy、contact alignment、ranking、thin-context、boundary/sensitive、false-positive/false-negative 行为现在有 49 个已提交确定性测试覆盖。T151/T152 仍需补充 policy fixture suite 和 feedback CLI 回归测试。 | T150 implementation record in `docs/07_handoff.md` |
| Q161 | T160 PreferencePatch schema 是否可以接受并推进到 T161？可以；以 `PASS_WITH_WARNINGS` 接受，warning 中的示例字段安全约束和缺少 committed model tests 继续留在风险台账中。 | `docs/review/T160_review.md` + Captain decision |
| Q162 | T161 feedback clusterer 是否产出确定性的、隐私安全的聚类结果？是；聚类由 action type 确定性推导，cluster_id 稳定，输出不含原始文本，不生成 patch candidate。 | T161 implementation record in `docs/07_handoff.md` |
| Q163 | T161 是否可以作为已完成任务接受并推进到 T162？可以；以 `PASS_WITH_WARNINGS` 接受，缺少 committed cluster tests 和 `input_path` 暴露模式继续保留在风险台账中。 | `docs/review/T161_review.md` + Captain decision |
| Q164 | T162 是否产出确定性的、candidate-only 的 PreferencePatch 提案？是；提案从 cluster label 确定性映射到 patch type，跳过不支持或模糊的 cluster，输出不含原始文本，不自动 approve。 | T162 implementation record in `docs/07_handoff.md` |
| Q165 | T162 是否可以作为已完成任务接受并推进到 T163？可以；以 `PASS_WITH_WARNINGS` 接受，`patch_id` 确定性文档偏差、proposal `input_path` 暴露、缺少 committed proposal tests 和 malformed cluster defensive guard 继续保留在风险台账中。 | `docs/review/T162_review.md` + Captain decision |
| Q167 | T164 是否提供 compact approved-patch context integration？是；T164 consumes reviewed T162/T163 proposal reports, filters to only approved + runtime-ready patches, and exposes safe compressed patch briefs through `ChatContext` without raw feedback text, review history expansion, or non-approved patch leakage. | T164 implementation record in `docs/07_handoff.md` |

## Deferred Items

- iLink 登录、收消息、reply、媒体和 `context_token` 验证。
- 微信桌面扫描记录读取。
- 实时平台接入。
- 自动发送。
- 向量数据库和 pgvector。
- DPO/微调/LoRA。
- 前端 review UI。
