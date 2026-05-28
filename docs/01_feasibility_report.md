# Feasibility Report

## Captain Update 2026-05-28 (T230 Review / M12 Conditional)

T230 confirms that M12 is feasible only as a narrowed official-surface research
and contract path, not as generic personal-WeChat integration.

The feasibility question has changed again:

- no longer blocked on whether WeChat-family options have been initially
  researched and separated into official vs prohibited paths
- now focused on whether a single official surface, selected as WeCom WeChat
  Customer Service for T231, can be represented through synthetic inbound
  fixtures and a pure `InboundEvent` normalizer
- still not ready for live WeChat/WeCom API calls, credentials, callback
  servers, polling/sync loops, personal-account automation, desktop automation,
  unofficial SDKs, outbound delivery, or automatic sending
- official documentation and provider constraints must be rechecked before any
  later implementation touches credentials or live APIs

So the project is ready to commit the T230 research slice and advance to T231,
but only as a synthetic inbound contract spike. T232 live outbound and T233
delivery behavior remain blocked until T231 is reviewed and Captain rewrites
their task packages.

## Captain Update 2026-05-28 (T224 Review / M11 Close)

T224 confirms that human-review presentation for outbound messages is feasible
without applying decisions or sending.

The feasibility question has changed again:

- no longer blocked on whether a local Feishu review-card payload and synthetic
  review-intent parser can be built over outbound request / gate / sandbox
  evidence
- now focused on whether M12 has any safe, official, thin WeChat adapter path
  that can preserve M11 boundaries without reviving the paused scan/login SDK
  track or adding unofficial realtime automation
- still not ready for WeChat implementation, production Feishu delivery,
  real callbacks/webhooks, credentials, scheduler/background jobs, runtime
  loops, or automatic outbound behavior
- Feishu review-card payloads and action parsing are local approximations; they
  are not validation of real Feishu callback/event semantics

So the project is ready to commit the T224 review-card slice, close M11 at the
task level, and advance to T230 as a docs-only WeChat adapter research spike.

## Captain Update 2026-05-28 (T223 Review)

T223 confirms that a Feishu-specific sandbox adapter boundary is feasible
without production delivery.

The feasibility question has changed again:

- no longer blocked on whether an already-sendable `OutboundMessageRequest` can
  be converted into a Feishu-shaped sandbox payload/result behind explicit
  recipient mapping
- now focused on whether T224 can render a local Feishu review card and parse
  synthetic review-intent actions while preserving the separation between
  display, review intent, approval application, send-gate state, adapter
  delivery, and feedback/memory writes
- still not ready for production Feishu delivery, callback/webhook handling,
  credentials, WeChat adapters, scheduler/background jobs, runtime loops, or
  automatic outbound behavior
- Feishu sandbox payload shape remains a sandbox approximation until a later
  production-delivery task validates current official Feishu API semantics

So the project is ready to commit the T223 Feishu sandbox slice and advance to
T224, with `feishu_dry_run_ready` / `feishu_sandbox_sent` treated as sandbox
evidence only, not production delivery.

## Captain Update 2026-05-28 (T222 Review)

T222 confirms that an outbound adapter boundary is feasible without external
delivery.

The feasibility question has changed again:

- no longer blocked on whether a sendable `OutboundMessageRequest` can cross an
  adapter boundary safely
- now focused on whether T223 can prepare a Feishu-specific sandbox payload /
  result while preserving send-gate, human approval, recipient mapping, audit,
  privacy, and dry-run defaults
- still not ready for production Feishu delivery, WeChat adapters, review-card
  UX, scheduler/background jobs, runtime loops, or automatic outbound behavior
- preview truncation from the fake adapter is not a privacy boundary for real
  adapters; T223 must construct platform payloads only from the approved
  outbound request payload and explicit sandbox recipient mapping

So the project is ready to commit the T222 local fake adapter slice and advance
to T223, with fake `fake_delivered` treated as synthetic evidence only, not
real delivery.

## Captain Update 2026-05-28 (T221 Review)

T221 confirms that send-gate policy is feasible without adding delivery infrastructure.

The feasibility question has changed again:

- no longer blocked on whether an outbound request can be evaluated by deterministic local policy
- now focused on whether T222 can consume only gate-allowed `OutboundMessageRequest` records and simulate delivery locally without external side effects
- still not ready for Feishu/WeChat adapters, review-card UX, scheduler/background jobs, runtime loops, or automatic outbound behavior
- Windows `zoneinfo` reproducibility now has a small portability note: T221 timezone tests require `tzdata` on Windows unless future tasks avoid named timezones or add the dependency explicitly

So the project is ready to commit the T221 gate slice and advance to T222, with gate `allowed` still treated as eligibility for later adapter consideration, not as delivery completion.

## Captain Update 2026-05-27 (T220 Review)

T220 confirms that an outbound request contract is feasible without turning review artifacts into executable actions.

The feasibility question has changed again:

- no longer blocked on whether M11 can define a separate outbound request shape
- now focused on whether T221 can make a deterministic `OutboundSendGate` that blocks by default, requires explicit outbound human approval, applies quiet-hours/frequency/duplicate/kill-switch/self-echo rules, and records audit evidence
- still not ready for fake adapters, Feishu/WeChat adapters, review cards, runtime loops, background scheduling, or automatic sending until later reviewed tasks

So the project is ready to commit the T220 schema slice and advance to T221, with `CandidateAction` remaining evidence and `OutboundMessageRequest` remaining inert unless the send gate explicitly allows it.

## Captain Update 2026-05-27 (T214 Review / M10 Review)

T214 confirms that M10 is feasible and complete as a review-only behavior-planner milestone.

The feasibility question has changed again:

- no longer blocked on whether T210-T213 preserve non-execution invariants end to end
- now focused on whether M11 can define an explicit outbound request contract and send gate without smuggling execution semantics into `CandidateAction`
- still not ready for platform sending, Feishu/WeChat adapters, background scheduling, or automatic outbound behavior until later M11 tasks pass review

So the project is ready to commit the T214/M10 review slice and advance to T220, with `CandidateAction` remaining review-only evidence rather than a send request.

## Captain Update 2026-05-25 (T213 Review)

T213 confirms that manual review of proactive behavior candidates is feasible without turning candidate approval into outbound authorization.

The feasibility question has changed again:

- no longer blocked on whether enriched `CandidateAction` records can be manually approved, rejected, frozen, or archived while preserving review metadata and non-mutation
- now focused on whether T214 can evaluate the complete T210-T213 behavior-planner slice for boundary, frequency, quiet-hours, conflict, privacy, and no-execution safety
- still explicitly not ready for automatic sending, reminders, platform adapters, outbound delivery, or runtime autonomy; those remain behind later OutboundSendGate milestones

So the project is ready to commit the T213 slice and advance to T214, while keeping M10 review-only and non-executable.

## Captain Update 2026-05-25 (T212 Review)

T212 confirms that review-only proactive candidates can be enriched with deterministic draft text without crossing the outbound boundary.

The feasibility question has changed again:

- no longer blocked on whether candidate actions can carry short, conservative, review-safe draft text while preserving no-send/no-scheduler/no-platform invariants
- now focused on whether T213 can add an explicit human review flow for candidate actions without treating approval as send authorization
- still explicitly not ready for automatic sending, reminders, platform adapters, or outbound delivery; those remain behind later review and send-gate milestones

So the project is ready to commit the T212 slice and advance to T213, while keeping proactive behavior review-first and non-executable.

## Captain Update 2026-05-25 (T211 Review)

T211 confirms that deterministic proactive-action proposal is feasible in the current repository shape without crossing the autonomy boundary.

The feasibility question has changed again:

- no longer blocked on whether safe context signals can be turned into review-only `CandidateAction` records while preserving T210 no-send/no-scheduler/no-platform invariants
- now focused on whether T212 can enrich those candidate actions with short review-safe draft text, deterministically and without platform execution, scheduling, LLM calls, or final-send semantics
- still explicitly not ready for automatic sending, reminders, platform adapters, or outbound delivery; those remain behind later review and send-gate milestones

So the project is ready to commit the T211 slice and advance to T212, while keeping proactive behavior candidate-only, local, and human-review-first.

## Captain Update 2026-05-25 (T210 Review)

T210 confirms that proactive behavior can be represented safely in the current repository shape, but only as reviewable draft artifacts.

The feasibility question has changed again:

- no longer blocked on whether M10 can define schema-level proactive action boundaries without crossing into sending, scheduling, platform execution, or hidden memory mutation
- now focused on whether T211 can implement a deterministic rule engine that proposes `CandidateAction` records from safe approved context and `AgentSelfState`, while keeping output candidate-only and review-only
- still explicitly not ready for autonomous behavior, reminders, platform adapters, or outbound delivery; those remain behind later review and send-gate milestones

So the project is ready to commit the T210 slice and advance to T211, while keeping BehaviorPlanner work deterministic, local, non-sending, and human-review-first.

## Captain Update 2026-05-24 (T203 Review)

T203 confirms that an optional external-memory adapter boundary is feasible in the current repository shape, but only as an off-by-default spike.

The feasibility question has changed again:

- no longer blocked on whether Mem0 can be wrapped behind the `MemoryRetriever` protocol without becoming a required dependency
- now explicitly aware that external adapter adoption still needs review enforcement, real evidence mapping, SDK version pinning, error recovery, and operational configuration before production use
- now focused on whether M10 can define draft-only proactive behavior schemas without sending messages, scheduling real actions, mutating memory, or integrating platforms

So the project is ready to commit the T203 slice, close M9 at task level, and advance to T210 while keeping proactive behavior strictly review-only and non-sending.

## Captain Update 2026-05-24 (T202 Review)

T202 confirms that retrieval behavior can be evaluated from committed synthetic cases in the current repository shape.

The feasibility question has changed again:

- no longer blocked on whether the T200/T201 retriever surface can be measured through a reusable eval baseline
- now focused on whether T203 can evaluate an optional Mem0 adapter boundary without making Mem0 a required dependency, reading private/raw transcripts, auto-writing memory, or wiring external retrieval into runtime behavior
- still explicitly not ready for production external-memory integration; T203 is a spike, not an adoption decision

So the project is ready to commit the T202 slice and advance to T203, while keeping M9 contract-bound, synthetic-testable, optional, and review-safe.

## Captain Update 2026-05-24 (T201 Review)

T201 confirms that local approved-store retrieval is feasible in the current repository shape.

The feasibility question has changed again:

- no longer blocked on whether the T200 retriever contract can be implemented over approved local store records
- now focused on whether T202 can create a committed synthetic eval set that measures retrieval relevance and boundary behavior through the unified `MemoryRetrieverResult` shape
- still explicitly not ready for external memory adapter work until local retrieval behavior has a reusable eval baseline

So the project is ready to commit the T201 slice and advance to T202, while keeping M9 local, deterministic, approved-only, and review-safe.

## Captain Update 2026-05-24 (T200 Review)

T200 confirms that a retrieval abstraction is feasible in the current repository shape.

The feasibility question has changed again:

- no longer blocked on whether the repo can define a clean `MemoryRetriever` / `MemoryHit` contract above existing local retrieval logic
- now focused on whether T201 can implement that contract over approved local store records without broadening into raw transcript search, external memory systems, auto-write, or planner behavior changes
- still explicitly aware that relationship-aware planner behavior remains a separate deferred gap, not something M9 retrieval should smuggle in

So the project is ready to commit the T200 slice and advance to T201, while keeping M9 local, deterministic, approved-only, and review-safe.

## Captain Update 2026-05-24 (T195 Review)

T195 confirms that M8 is feasible within its intended scope, but it also sharpens the remaining gap.

The feasibility question has changed again:

- no longer blocked on whether the repo can model, review, expose, and evaluate approved relationship-state guidance safely
- now explicitly aware that the current planner does not consume that guidance semantically, so M8 closes as infrastructure/evaluation rather than behavior completion
- now focused on whether T200 can define a retriever abstraction cleanly, without external memory systems or hidden runtime coupling

So the project is ready to commit the T195 slice and advance to T200, while keeping relationship-aware planner behavior as later scoped work rather than smuggling it into M9.

## Captain Update 2026-05-24 (T194 Review)

T194 confirms that compact, approval-gated relationship context can be exposed to `ChatContext` in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether approved relationship guidance can be injected into runtime context without raw signal or review-history leakage
- now focused on whether T195 can evaluate planner behavior under different approved relationship states without modifying code or treating the context path as a state-application mechanism

So the project is ready to commit the T194 slice and advance to T195, while keeping the final M8 step evaluation-only.

## Captain Update 2026-05-24 (T193 Review)

T193 confirms that explicit human review over relationship deltas is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether relationship deltas can be approved/rejected/frozen/archived without mutating state
- now focused on whether T194 can expose only approved relationship state information into compact context without leaking raw signal/delta internals or changing send behavior

So the project is ready to commit the T193 slice and advance to T194, while keeping M8 context work compact, approval-gated, and non-mutating.

## Captain Update 2026-05-24 (T192 Review)

T192 confirms that reviewable relationship-delta generation is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether sparse relationship signals can be turned into explicit, evidence-backed delta candidates without mutating state
- now focused on whether T193 can add human review actions over those deltas without silently applying them or broadening scope into state mutation

So the project is ready to commit the T192 slice and advance to T193, while keeping M8 review work explicit, auditable, and non-mutating.

## Captain Update 2026-05-24 (T191 Review)

T191 confirms that conservative relationship-signal extraction is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether boundary-labeled feedback can be converted into sparse, evidence-backed relationship signals without raw-text leakage
- now focused on whether T192 can turn those signals into reviewable `RelationshipDeltaCandidate` records with explicit dimension semantics and no auto-approval

So the project is ready to commit the T191 slice and advance to T192, while keeping M8 delta work review-first and non-mutating.

## Captain Update 2026-05-24 (T190 Review)

T190 confirms that conservative relationship-state modeling is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether M8 can define a multidimensional relationship-state contract without collapsing to a scalar score
- now focused on whether T191 can extract conservative, evidence-backed relationship signals from approved metadata and feedback artifacts without reading raw chat history or mutating state

So the project is ready to commit the T190 slice and advance to T191, while keeping M8 extraction work review-first, additive, and non-mutating.

## Captain Update 2026-05-23 (T185 / M7 Review)

M7 is now feasible and complete within its intended scope.

The final feasibility question for M7 changed again:

- no longer blocked on whether an opt-in hybrid planner surface can be wired safely
- no longer blocked on whether holdout evaluation can produce useful evidence
- no longer blocked on whether the observed language/safety/label/merge gaps can be repaired within the existing architecture
- now focused on whether M8 can define a conservative multidimensional relationship-state model without collapsing back into a scalar score or auto-update behavior

So the project is ready to commit the T185 slice, close M7 with `Allow`, and advance to T190 while keeping relationship-state work review-first and non-mutating.

## Captain Update 2026-05-23 (T184 Review)

T184 confirms that the hybrid planner path is viable on anonymized holdout scenarios, but the milestone is not yet fully closed.

The feasibility gap has changed again:

- no longer blocked on whether the hybrid path can be evaluated on real anonymized scenarios with evidence-backed results
- now focused on whether T185 can remove the language/safety/merge coverage gaps that keep Gate M7 at `Conditional`

So the project is ready to commit the T184 slice and advance to T185, while keeping the M7 gate open until the narrow alignment work is complete.

## Captain Update 2026-05-23 (T183 Review)

T183 confirms that an opt-in hybrid planner surface is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether template and LLM candidates can be composed into a single review-only planner surface without making LLM behavior the default
- now focused on whether T184 can evaluate the resulting hybrid planner on holdout scenarios and separate quality evidence from implementation success

So the project is ready to commit the T183 slice and advance to T184, while keeping quality judgment separate from integration success.

## Captain Update 2026-05-23 (T182 Review)

T182 confirms that shared deterministic candidate validation is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether template and LLM candidate paths can share reusable deterministic validation and stronger regression coverage
- now focused on whether T183 can add an opt-in hybrid planner mode without regressing template-mode compatibility, review-only policy enforcement, or compact-context boundaries

So the project is ready to commit the T182 slice and advance to T183, while keeping hybrid integration opt-in, non-default, and policy-gated.

## Captain Update 2026-05-23 (T181 Review)

T181 confirms that an optional offline LLM generation path is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether M7 can call an OpenAI-compatible provider through a separate offline CLI while preserving private-output-only discipline
- now focused on whether T182 can extract and harden deterministic candidate validation so both template and LLM candidates share stronger privacy, boundary, and refusal enforcement

So the project is ready to commit the T181 slice and advance to T182, while keeping M7 validator work deterministic, additive, and separate from hybrid planner wiring.

## Captain Update 2026-05-23 (T180 Review)

T180 confirms that an optional LLM candidate path can be introduced contract-first in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether M7 can define an additive LLM candidate contract without breaking the existing deterministic planner path
- now focused on whether T181 can implement an opt-in offline CLI that stays within compact-context boundaries, writes only private artifacts, and preserves deterministic post-generation validation

So the project is ready to commit the T180 slice and advance to T181, while keeping LLM work offline, opt-in, and separate from the existing `ReplyPlanner`.

## Captain Update 2026-05-23 (M6 Review)

M6 confirms that ContactSkill-compatible decomposition is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether the repo can decompose approved `ContactSkill` into narrower briefs while preserving compatibility, evidence ownership, and fallback behavior
- now focused on whether M7 can introduce LLM-related contracts and later execution paths without regressing privacy, boundary adherence, review-only mode, or the newly committed context structure

So the project is ready to commit the T174 slice, close M6 with `Allow`, and advance to T180, while keeping the first M7 step contract-only.

## Captain Update 2026-05-23 (T174 Review)

T174 confirms that derived-brief context integration is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether projected briefs can coexist with the existing `ApprovedContactSkillBrief` fallback and T164 approved-patch compact context
- now focused on whether the next milestone can stay contract-first before any LLM execution path is introduced

## Captain Update 2026-05-23 (T173 Review)

T173 confirms that lazy derived-brief projection is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether all three derived briefs can be projected deterministically from approved store records without mutation or side effects
- now focused on whether T174 can integrate those derived briefs into `ChatContext` while preserving the existing `ApprovedContactSkillBrief` fallback and the separate T164 approved-patch compact-context path

So the project is ready to commit the T173 slice and advance to T174, while keeping context integration additive, fallback-safe, and non-mutating.

## Captain Update 2026-05-23 (T172 Review)

T172 confirms that the remaining policy and boundary brief schemas are feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether M6 can formalize policy and boundary semantics without mutating runtime behavior
- now focused on whether T173 can project those schemas faithfully from approved store records without inventing synthetic evidence, relying on schema defaults, or weakening fallback behavior

So the project is ready to commit the T172 slice and advance to T173, while keeping projection work lazy, deterministic, and non-mutating.

## Captain Update 2026-05-23 (T171 Review)

T171 confirms that additive derived-brief schema work is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether the first focused derived brief can be represented cleanly and tested without runtime wiring
- now focused on whether policy and boundary semantics can be formalized with explicit sensitivity, ownership, and versioning decisions before projection starts

So the project is ready to commit the T171 slice and advance to T172, while keeping M6 schema work additive, reviewable, and non-breaking.

## Captain Update 2026-05-22 (T170 Review)

T170 confirms that a compatibility-first `ContactSkill` decomposition path is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on whether M6 needs a breaking replacement design
- now focused on whether additive brief schemas can be formalized cleanly, with explicit evidence ownership and no runtime behavior change

So the project is ready to commit the T170 slice and advance to T171, while keeping M6 schema work additive, reviewable, and non-breaking.

## Captain Update 2026-05-22 (T164 Review)

T164 confirms that approved-only patch context integration is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on exposing approved, runtime-ready patch hints through `ChatContext`
- now focused on whether ContactSkill can be decomposed into narrower derived briefs without breaking the current evidence-first, compatibility-first pipeline

So the project is ready to commit the T164 slice and advance to T170, while keeping M6 design work non-breaking and documentation-first.

## Captain Update 2026-05-22 (T163 Review)

T163 confirms that explicit human review over patch proposals is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on recording manual approve/reject/freeze/archive decisions while preserving evidence and review history
- now focused on whether only approved, runtime-ready patches can be integrated into `ChatContext` as compact guidance without leaking proposal internals or skipping existing approval boundaries

So the project is ready to commit the T163 slice and advance to T164, but still only within approved-only, compact-context, non-mutating M5 constraints.

## Captain Update 2026-05-18 (T162 Review)

T162 confirms that deterministic, candidate-only patch proposal generation is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on converting deterministic feedback clusters into conservative `PreferencePatchCandidate` proposals
- now focused on whether human review decisions can be recorded safely without auto-approval, runtime injection, or evidence drift

So the project is ready to commit the T162 slice and advance to T163, but still only within manual-review, non-mutating M5 constraints.

## Captain Update 2026-05-18 (T161 Review)

T161 confirms that deterministic, privacy-safe feedback clustering is feasible in the current repository shape.

The feasibility gap has changed again:

- no longer blocked on turning validated feedback into stable aggregate clusters
- now focused on whether those clusters can be converted into conservative `PreferencePatchCandidate` records without leaking raw text, over-interpreting ambiguous labels, or bypassing review

So the project is ready to commit the T161 slice and advance to T162, but still only within deterministic, candidate-only, review-first M5 constraints.

## Captain Update 2026-05-18 (T160 Review)

T160 confirms that M5 can stay within the current safety envelope while introducing patch-shaped artifacts.

The feasibility gap has changed again:

- no longer blocked on defining a review-only patch contract
- now focused on whether repeated feedback can be clustered deterministically and privately before any patch proposal is generated

So the project is ready to commit the T160 slice and advance to T161, but still only within review-only, candidate-only M5 constraints.

## Captain Update 2026-05-18 (M4.5 Review)

M4.5 confirms that clean-environment reproducibility is now feasible in the current repository shape for the entire reviewed M3/M4 surface.

The feasibility gap has changed:

- no longer blocked on proving planner/policy/feedback behavior from committed contents
- now focused on whether M5 can stay candidate-only and review-first while introducing patch-shaped artifacts

So the project is now ready to commit T152 and advance to T160, but only within schema-only, non-mutating M5 constraints.

## Captain Update 2026-05-18 (T151 Review)

T151 confirms that committed deterministic policy-engine regression testing is feasible in the current repository shape. The repo can now prove both the ReplyPlanner surface and the direct policy layer from committed synthetic fixtures alone.

The remaining feasibility gap is now narrower:

- T152 must prove that the T140-T142 feedback CLI flow is equally reproducible from committed contents
- until that happens, M5 remains premature even though T151 itself is accepted

So the project is ready to commit T151 and advance the worker to T152, but not yet ready to claim full M4.5 completion.

## Captain Update 2026-05-18

T150 confirms that committed deterministic ReplyPlanner regression testing is feasible in the current repository shape. The repo can now prove a meaningful subset of M3 behavior from committed contents alone, without private fixtures or manual-only verification.

The remaining feasibility gap is narrower and more specific:

- T151 must make policy-layer fixture coverage and direct policy expectations more explicit
- T152 must do the same for the feedback CLI capture/validate/summary loop

So the project is still not ready for M5, but it is ready to commit T150 and advance the next worker to T151.

## Captain Update 2026-05-17

T142 confirms that privacy-safe aggregate feedback summary export is feasible in the current architecture. The project can now record, validate, and summarize feedback without mutating ContactSkill, MemoryFact, approved stores, or outbound behavior.

The remaining feasibility gap is reproducibility, not feature reach. M4 is therefore judged `Conditional`: a clean environment still cannot prove the M3/M4 behavior from committed repo contents alone, because committed regression tests and committed synthetic fixtures are still missing. T150-T152 remain the required bridge before M5.

## Captain Update 2026-05-17

T140 confirms that private human feedback capture is feasible in the current architecture: a `ReplyPlan` can be loaded, a chosen candidate can be referenced safely, and accept/edit/reject/boundary feedback can be written without touching memory, ContactSkill, sending, or platform adapters.

The remaining feasibility gap inside M4 is log trustworthiness rather than feature reach. Before any summary or patch-proposal work, T141 must prove that feedback logs can be validated read-only, that broken references fail safely, and that corrupted or non-private path behavior is surfaced instead of silently passing through.

## Captain Update 2026-05-16

Gate M3 is `Conditional` after T133 review. The M3 structure is feasible: `ReplyPlan`, `ReplyPlanner`, policy/boundary checks, and anonymized holdout evaluation all exist and run in the current environment.

The remaining feasibility gap is reproducibility and quality maturity. A clean environment run is not fully proven because committed regression fixtures/tests are still missing, and T133 rates naturalness/evidence usage at 3/5. Proceeding to T140 is feasible only because T140 records human feedback privately and does not apply it automatically.

T150 remains mandatory for committed regression tests before any stronger quality or maturity claim.

## Captain Update 2026-05-16: Roadmap Feasibility

The updated GPT roadmap is feasible if treated as a staged backlog rather than immediate implementation.

Feasible now:

- T140 feedback capture.
- T141 feedback validation.
- T142 safe feedback summary.
- T150-T152 committed regression tests and fixtures.

Feasible later, after tests:

- PreferencePatch candidates and review flow.
- Compatible ContactSkill decomposition.
- Optional LLM-assisted ReplyPlanner.

Not feasible/safe now:

- Direct Mem0/Zep integration.
- Feishu or WeChat adapter work.
- BehaviorPlanner/proactive behavior.
- Automatic memory or ContactSkill mutation from feedback.

更新日期：2026-05-15

## 1. 问题定义

目标是基于 WeFlow 已导出的私密聊天记录，构建长期关系感知 chat agent 的离线蒸馏与运行时基础。

核心挑战：

- 原始 JSONL 字段和消息类型是否可稳定解析。
- 如何避免把一次性聊天误判为长期关系规律。
- 如何让每条记忆和 ContactSkill 结论都有证据链。
- 如何保护 `private/chat_history` 中的敏感内容。
- 如何在回复生成时利用关系记忆而不冒充联系人。

## 2. 技术路线对比

| 方案 | 优点 | 问题 | 当前判断 |
| --- | --- | --- | --- |
| 继续 iLink/扫码/实时接入 | 可实时收发 | T01 BLOCK，平台风险高，用户已不需要 | 暂停 |
| 微信桌面扫描/OCR | 已有部分代码 | 读取记录稳定性差，用户已有 WeFlow 导出 | 暂停 |
| 微调/LoRA | 可学语气 | 难审计、难删除、易泄露隐私 | 不做 |
| RAG 直接检索原文 | 证据强 | 容易把大量原文塞入上下文，缺关系抽象 | 后续作为组件 |
| Memory + ContactSkill | 可解释、可审计、可回滚 | 需要设计抽取和 review 流程 | 当前主线 |
| 离线蒸馏 MVP | 风险低、最快验证核心假设 | 初期不是实时 agent | 当前第一阶段 |

## 3. 可差异化点

- 本地优先处理 WeFlow 导出，不依赖社交平台实时接口。
- 用 evidence refs 约束所有事实和关系判断。
- ContactSkill 用于辅助用户沟通，不用于复刻或冒充联系人。
- 先做审阅版 JSON/Markdown，再接数据库和运行时。
- 用户反馈进入记忆生命周期，而不是训练模型权重。

## 4. MVP 实验

输入：

- `private/chat_history/` 中的 WeFlow JSONL。

输出：

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- `private/distilled/<run_id>/normalized_events.jsonl`
- `private/distilled/<run_id>/chunks.jsonl`
- `private/distilled/<run_id>/memory_facts.jsonl`
- `private/distilled/<run_id>/contact_skill.candidate.json`
- `private/distilled/<run_id>/contact_skill.review.md`

## 5. 风险

- 原始导出格式不稳定或字段含义不明。
- sender_role/direction 判断错误导致事实归因错位。
- LLM 对关系状态过度推断。
- 私密内容泄露到 docs/examples/tests。
- 初期过早引入向量库、UI 或复杂 agent 框架，拖慢验证。

## 6. Go / No-Go 判断

当前判断：`Go with offline-first constraints`。

约束：

- T100 已通过 review `PASS`，确认 WeFlow schema profile、normalized event contract 和脱敏 fixture 可以作为 M0 后续输入。
- T101 已通过 review `PASS`，确认隐私脱敏规则、source_ref/raw_ref 规则和红线样例可以约束 T102。
- T102 已通过 review `PASS`，确认最小 normalize CLI 可运行，输出限定在 `private/distilled/`，且未做 chunking、LLM、ContactSkill 或数据库接入。
- T103 milestone review 已接受 Gate M0 = `Conditional`，允许进入 M1，但 T110/T150/T112+/T114 必须承接 M0 条件。
- T110 已通过 reviewer `PASS`，conversation chunker v0 可生成 `chunks.jsonl` 并保留 T102 的不确定性信号。
- T111 已通过 reviewer `PASS`，ChunkSummary、MemoryFactCandidate、ContactSkillCandidate schema 和 JSON contract 已可作为 T112 校验边界。
- T112 已通过 reviewer `PASS`，小样本可生成 `chunk_summaries.jsonl` 和 `memory_facts.jsonl`，并在写入前执行 schema/evidence refs 校验。
- T113 已通过 reviewer `PASS_WITH_WARNINGS`，可生成 candidate 状态的 `contact_skill.candidate.json` 和人工审阅用 `contact_skill.review.md`。
- T114 已确认 Gate M1 = `Conditional`，M1 artifact chain 能在一个真实小样本上端到端运行，但启发式泛化、confidence 数字和 paraphrase compression 风险必须带入 M2。
- T120 已通过 reviewer `PASS_WITH_WARNINGS`，离线 memory/skill 文件 store、review metadata、source metadata 和 human-review-first gate 已落地；未接数据库、未引入向量库、未做 runtime prompt 注入。
- T121 已通过 reviewer `PASS_WITH_WARNINGS`，evidence validator、missing-ref approval block、candidate/rejected/frozen/archived 状态规则和 validator report 已落地；未自动 approve、未做 runtime integration。
- T122 已通过 reviewer `PASS_WITH_WARNINGS`，人工 review/approve/reject/freeze/archive/export CLI 已落地，approve 必须受 T121 validation report 约束；仍未做 runtime integration、数据库或自动发送。
- 当前唯一任务切换为 T123，将 approved + runtime-ready memory/skill 以 compact brief 接入 `ChatContext`，不得注入 candidate/rejected/frozen/archived 或大段原文。
- M1 只选 1 个联系人或小样本做 distillation MVP。
- M1 不微调、不自动发送、不接实时平台。
- 所有可提交 fixture 必须脱敏。

补充判断：T130 已完成并通过 `PASS_WITH_WARNINGS`，ReplyPlan schema 与 prompt contract 已经可行；后续风险主要转移到 T131 的组装质量与候选差异化，而不是结构本身。

补充判断：T131 已完成并通过 `PASS_WITH_WARNINGS`，证明从 T123 compact approved-store context 到 T130 `ReplyPlan` 的 review-only wiring 可行；但 clean-env/committed fixture 尚未覆盖，且候选文本仍偏硬编码。当前可进入 T132 policy/boundary validation，但不能进入 M4。

补充判断：T132 已完成并通过 `PASS_WITH_WARNINGS`，证明 ReplyPlanner 可以在不扩大 scope 的情况下加入 policy/boundary 风险层；但匹配逻辑仍是关键词/substring heuristic，且缺少 committed tests。当前可进入 T133 匿名 holdout eval，但仍不能进入 M4。
