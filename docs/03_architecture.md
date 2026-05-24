# Architecture

## Captain Update 2026-05-25 (T210 Review)

T210 completes the schema-only opening of M10:

```text
approved compact context / memory / relationship signals
  -> AgentSelfState
  -> BehaviorPolicy
  -> CandidateActionPayload
  -> CandidateAction
  -> human review before visibility
  -> no sending, scheduling, platform execution, platform target, or mutation
```

The next architectural step is T211, which must add only deterministic candidate proposal rules:

```text
AgentSelfState + review-safe context signals
  -> BehaviorRulePlanner / equivalent service
  -> zero or more CandidateAction records
  -> stable rule rationale + supporting refs + risk flags
  -> still no LLM, CLI, scheduler, platform adapter, outbound gate, or store mutation
```

This keeps M10 on the safe side of the autonomy boundary: T211 may decide what to suggest for human review, but it must not decide to execute anything.

## Captain Update 2026-05-24 (T203 Review)

T203 completes the optional adapter spike for M9:

```text
MemoryRetriever contract
  -> LocalApprovedStoreRetriever (primary local path)
  -> optional Mem0AdapterRetriever spike
  -> graceful not_configured when dependency/config is absent
  -> no hard dependency, no auto-write, no ChatContext/planner/send behavior change
```

The next architectural step is M10/T210, which must stay schema-only and draft-only:

```text
approved compact context / memory / relationship signals
  -> future BehaviorPlanner inputs
  -> AgentSelfState / BehaviorPolicy / CandidateAction schemas
  -> human review before any action
  -> no scheduling, no platform integration, no outbound send
```

This moves the architecture from retrieval infrastructure to proactive-action modeling without crossing the send or autonomy boundary.

## Captain Update 2026-05-24 (T202 Review)

T202 completes the reusable eval layer of M9:

```text
synthetic retrieval eval cases
  -> MemoryRetriever protocol
  -> MemoryRetrieverResult contract checks
  -> reusable local/external retriever baseline
  -> no raw transcript, no external service, no runtime wiring
```

The next architectural step is T203, which must stay an optional adapter spike:

```text
optional Mem0 adapter boundary
  -> behind MemoryRetriever protocol
  -> reuse synthetic eval shape where possible
  -> graceful not_configured / unavailable behavior
  -> no required dependency, no auto-write, no ChatContext or planner behavior change
```

This keeps M9 from jumping from a retrieval contract directly into external-memory adoption without a reviewable adapter boundary.

## Captain Update 2026-05-24 (T201 Review)

T201 completes the local implementation layer of M9:

```text
approved local memory store
  -> LocalApprovedStoreRetriever
  -> MemoryRetrieverResult
  -> MemoryHit(source="approved_store")
  -> no ChatContext or planner behavior change yet
```

The next architectural step is T202, which must stay evaluation-only:

```text
synthetic approved-store cases
  -> MemoryRetriever protocol calls
  -> expected MemoryHit ids / exclusions / ordering
  -> reusable eval baseline for local and future retrievers
  -> no external adapter, no raw transcript, no runtime wiring
```

This keeps M9 evidence-driven: local behavior gets a committed eval baseline before optional external memory adapter work is considered.

## Captain Update 2026-05-24 (T200 Review)

T200 completes the contract-first opening of M9:

```text
existing local retrieval logic
  -> MemoryRetriever protocol
  -> MemoryHit contract
  -> MemoryRetrieverResult envelope
  -> LocalMemoryRetriever adapter
  -> no ChatContext or planner behavior change yet
```

The next architectural step is T201, which must stay local and approved-store-only:

```text
approved local memory store records
  -> LocalApprovedStoreRetriever
  -> MemoryHit(source="approved_store")
  -> deterministic query / limit behavior
  -> no raw transcript, no vector DB, no external adapter, no mutation
```

This keeps M9 on the safe path: prove the contract locally before evaluating retrieval quality or considering optional external adapter spikes.

## Captain Update 2026-05-24 (T195 Review)

T195 closes M8 by clarifying the current architecture, not by adding new runtime behavior:

```text
approved relationship deltas
  -> compact ApprovedRelationshipContext
  -> ChatContext.relationship_context
  -> review-visible summary / retrieval notes
  -> no planner or policy consumer for delta semantics
  -> no reply-behavior change today
```

The next architectural step is T200, which must stay contract-first:

```text
existing local memory sources
  -> MemoryRetriever interface
  -> MemoryHit contract
  -> approved-only / review-safe retrieval boundary
  -> no external adapter and no auto-write
```

This keeps M9 separate from the still-deferred question of explicit relationship-aware planner consumption.

## Captain Update 2026-05-24 (T194 Review)

T194 completes the runtime-context half of M8:

```text
approved relationship delta context
  -> compact ChatContext guidance
  -> approved/runtime-ready only
  -> no raw signal or review-history leakage
  -> no state mutation
```

The next architectural step is T195, which must stay evaluation-only:

```text
different approved relationship states
  -> compare ReplyPlan behavior
  -> no code changes
  -> no state application
  -> no private artifact commits
```

This keeps M8 additive and finishes the architecture with an evaluation gate rather than a new runtime mutation path.

## Captain Update 2026-05-24 (T193 Review)

T193 adds the review layer on top of candidate deltas:

```text
RelationshipDeltaCandidate
  -> RelationshipDeltaReviewService
  -> approve / reject / freeze / archive
  -> review metadata + runtime-ready gate
  -> still no RelationshipState mutation
```

The next architectural step is T194, which must stay context-only:

```text
approved relationship state and/or approved review artifacts
  -> compact ChatContext summary
  -> no raw signal history
  -> no state mutation
  -> no send behavior change
```

This keeps M8 additive and preserves the line between review, context, and future application semantics.

## Captain Update 2026-05-24 (T192 Review)

T192 completes the second executable layer in M8:

```text
RelationshipSignal
  -> RelationshipDeltaGenerator
  -> RelationshipDeltaCandidate
  -> explicit dimension changes
  -> evidence refs + signal refs
  -> no state mutation
```

The next architectural step is T193, which must stay review-only:

```text
RelationshipDeltaCandidate
  -> manual review CLI
  -> approve / reject / freeze / archive
  -> review metadata update
  -> no auto-apply to RelationshipState
```

This keeps M8 additive and preserves the review-first boundary from schema -> signal -> delta.

## Captain Update 2026-05-24 (T191 Review)

T191 adds the first executable layer on top of the M8 schema:

```text
boundary-labeled feedback
  -> conservative RelationshipSignal
  -> evidence refs + provenance
  -> no raw-text storage
  -> no state mutation
```

The next architectural step is T192, which must stay delta-only:

```text
RelationshipSignal records
  -> RelationshipDeltaCandidate
  -> explicit dimension changes
  -> review-only output
  -> no auto-approval
  -> no RelationshipState update
```

This keeps M8 additive and preserves the review-first boundary established by T190 and T191.

## Captain Update 2026-05-24 (T190 Review)

T190 completes the contract-first opening for M8:

```text
RelationshipState schema
  -> multidimensional fields
  -> evidence refs + timestamps
  -> review-only delta contract
  -> no scalar collapse
  -> no auto-update
```

The next architectural step is T191, which must stay extractor-only:

```text
approved feedback / approved metadata
  -> conservative relationship signals
  -> explicit dimension refs + evidence refs
  -> no state mutation
  -> no delta generation
  -> no raw transcript dependency
```

This keeps M8 additive and preserves the review-first boundary established by T190.

## Captain Update 2026-05-23 (T185 / M7 Review)

M7 architecture is now closed as an opt-in, review-only, regression-hardened hybrid path:

```text
template ReplyPlan
  -> opt-in hybrid ReplyPlan
  -> holdout evaluation evidence
  -> narrow alignment hardening
  -> Gate M7 closes with Allow
```

The next architectural step is M8 / T190, which must stay conservative:

```text
RelationshipState schema
  -> multidimensional fields
  -> evidence refs + timestamps
  -> no scalar collapse
  -> no auto-update
```

This keeps the next milestone additive and preserves the review-first boundary established by M7.

## Captain Update 2026-05-23 (T184 Review)

T184 shows the current M7 architecture is usable, but not yet final:

```text
template ReplyPlan
  -> opt-in hybrid ReplyPlan
  -> holdout evaluation evidence
  -> quality judgment
  -> Gate M7 stays Conditional until alignment gaps are fixed
```

The next architectural step is T185, which must stay narrow:

```text
hybrid planner
  -> Chinese language alignment
  -> explicit thin-context / boundary-sensitive safety constraints
  -> normalized approach labels
  -> committed merge-path regression coverage
```

This keeps M7 evidence-backed without overstating readiness.

## Captain Update 2026-05-23 (T183 Review)

T183 completes the opt-in hybrid planner wiring without claiming quality completion:

```text
ReplyPlanner
  -> template-only mode (default)
  -> opt-in hybrid mode
     - template candidates
     - optional LLM candidates
     - shared deterministic validator
     - policy/boundary assessment
     - review-only ReplyPlan output
```

The next architectural step is T184, which must stay holdout-eval-only:

```text
hybrid ReplyPlanner
  -> anonymized holdout scenarios
  -> compare template vs hybrid outputs
  -> score naturalness / evidence / boundary / privacy / diversity
  -> no planner code changes
```

This keeps M7 additive and separates implementation success from quality judgment.

## Captain Update 2026-05-23 (T182 Review)

T182 completes the shared validation layer without changing planner selection behavior:

```text
template candidates / LLM candidates
  -> shared deterministic validator helpers
  -> privacy + impersonation + ref checks
  -> rank normalization
  -> stronger regression coverage
  -> existing planner/runtime behavior unchanged
```

The next architectural step is T183, which must stay opt-in and review-only:

```text
ReplyPlanner
  -> template-only mode (existing default)
  -> optional hybrid mode
     - template candidates
     - optional LLM candidates
     - shared deterministic validation
     - policy/boundary review before final output
  -> ReplyPlan output only
```

This keeps M7 additive, non-default, and compatible with the committed deterministic planner flow.

## Captain Update 2026-05-23 (T181 Review)

T181 completes the first executable M7 path without changing the existing planner runtime:

```text
safe ChatContext JSON
  -> offline LLM candidate generator CLI
  -> OpenAI-compatible provider call
  -> deterministic post-generation validation
  -> validated LLMReplyPlan or structured refusal
  -> private output artifact only
  -> existing ReplyPlanner unchanged
```

The next architectural step is T182, which must stay validator-only:

```text
template candidates / LLM candidates
  -> shared deterministic validator layer
  -> stronger privacy + impersonation + ref checks
  -> explicit input-budget refusal path
  -> regression coverage
  -> still no hybrid planner default path
```

This keeps M7 additive, review-first, and isolated from the committed deterministic planner flow.

## Captain Update 2026-05-23 (T180 Review)

T180 completes the contract-only M7 opening without changing runtime behavior:

```text
existing review-only planner path
  -> optional LLMReplyPlan contract
  -> separate offline LLM generator surface
  -> deterministic post-generation validation boundary
  -> private output artifact only
  -> no hybrid planner or runtime mutation yet
```

The next architectural step is T181, which must stay offline and opt-in:

```text
safe ChatContext JSON
  -> offline LLM candidate generator CLI
  -> validated LLMReplyPlan or structured refusal
  -> private output path
  -> no change to chat-reply-plan / ReplyPlanner
```

This keeps M7 additive, review-first, and isolated from the committed deterministic planner flow.

## Captain Update 2026-05-23 (M6 Review)

M6 is now complete. The architecture includes a full compatibility-first decomposition path:

```text
Approved ContactSkillStoreRecord
  -> ContactSkillProjectionService
  -> DerivedBriefContext
     - PartnerPersonaBrief
     - CommunicationPolicyBrief
     - BoundaryProfileBrief
  -> existing ApprovedContactSkillBrief fallback
  -> separate ApprovedPatchContext path
```

The next architectural step is T180, which must stay contract-only:

```text
existing review-only planner path
  -> optional LLM candidate contract
  -> no LLM calls yet
  -> no planner behavior change yet
  -> no send/platform/runtime mutation
```

This keeps M7 narrow, review-first, and compatible with the committed M6 context structure.

## Captain Update 2026-05-23 (T174 Review)

T174 completes the M6 runtime-side wiring without changing planner behavior:

```text
ContactSkillProjectionService
  -> DerivedBriefContext on ChatContext
  -> additive overlay only
  -> coexistence with ApprovedContactSkillBrief fallback
  -> coexistence with ApprovedPatchContext
```

## Captain Update 2026-05-23 (T173 Review)

T173 is now complete, so the M6 architecture has a committed projection layer between approved store records and runtime context:

```text
Approved ContactSkillStoreRecord
  -> ContactSkillProjectionService
  -> PartnerPersonaBrief
  -> CommunicationPolicyBrief
  -> BoundaryProfileBrief
  -> later ChatContext integration
  -> fallback to existing ApprovedContactSkillBrief
```

The next architectural step is T174, which must stay context-integration-only:

```text
projection layer committed
  -> ChatContext / approved-store context wiring
  -> partial overlay support
  -> coexistence with approved patch compact context
  -> no planner behavior change
  -> no new persistence or migration
```

This keeps M6 additive, fallback-safe, and runtime-stable.

## Captain Update 2026-05-23 (T172 Review)

T172 is now complete, so the M6 architecture has all three derived-brief schemas committed:

```text
Approved ContactSkill
  -> PartnerPersonaBrief
  -> CommunicationPolicyBrief
  -> BoundaryProfileBrief
  -> lazy projection later
  -> fallback to existing ApprovedContactSkillBrief
```

The next architectural step is T173, which must stay projection-only:

```text
brief schemas committed
  -> lazy projection service
  -> explicit conversion rules
  -> runtime-ready gating
  -> no ChatContext integration yet
  -> no new persistence or migration
```

This keeps M6 additive, deterministic, and runtime-stable until T174.

## Captain Update 2026-05-23 (T171 Review)

T171 is now complete, so the M6 architecture has its first committed derived-brief model:

```text
Approved ContactSkill
  -> PartnerPersonaBrief schema
  -> later CommunicationPolicyBrief
  -> later BoundaryProfileBrief
  -> lazy projection later
  -> fallback to existing ApprovedContactSkillBrief
```

The next architectural step is T172, which must stay schema-only:

```text
persona brief committed
  -> policy + boundary brief models + contract rules
  -> sensitivity reduction semantics
  -> important-event ownership decision
  -> no projection service yet
  -> no ChatContext/runtime integration yet
```

This keeps M6 additive, typed, and runtime-stable until T173-T174.

## Captain Update 2026-05-22 (T170 Review)

T170 is now complete, so the M6 architecture has an explicit compatibility-first decomposition contract:

```text
Approved ContactSkill
  -> documented decomposition contract
  -> PartnerPersonaBrief
  -> CommunicationPolicyBrief
  -> BoundaryProfileBrief
  -> lazy projection later
  -> fallback to existing ApprovedContactSkillBrief
```

The next architectural step is T171, which must stay schema-only:

```text
decomposition design
  -> additive brief models + contract doc
  -> no projection service yet
  -> no ChatContext/runtime integration yet
  -> no ContactSkill mutation or migration
```

This keeps M6 additive, evidence-first, and runtime-stable until T173-T174.

## Captain Update 2026-05-22 (T164 Review)

T164 is now complete, so the M5 architecture has reached its intended review-only compact-context endpoint:

```text
Reproducible feedback loop
  -> PreferencePatchCandidate schema
  -> deterministic privacy-safe feedback clusters
  -> conservative deterministic patch proposals
  -> manual approve/reject/freeze/archive review
  -> approved patch compact context in ChatContext
```

The next architectural step is T170, which must add design only:

```text
Approved ContactSkill
  -> decomposition design
  -> compatible derived briefs
  -> fallback to existing ContactSkill
  -> no runtime breakage or data migration yet
```

This keeps the mainline non-breaking, evidence-first, and review-oriented.

## Captain Update 2026-05-22 (T163 Review)

T163 is now complete, so the M5 architecture has advanced from candidate proposals to explicit human-reviewed patch state:

```text
Reproducible feedback loop
  -> PreferencePatchCandidate schema
  -> deterministic privacy-safe feedback clusters
  -> conservative deterministic patch proposals
  -> manual approve/reject/freeze/archive review
  -> later approved patch compact context
```

The next architectural step is T164, which must add compact-context consumption only:

```text
approved runtime-ready patches
  -> compact patch briefs in ChatContext
  -> planner-readable communication hints
  -> no raw feedback text and no direct runtime prompt injection shortcuts
```

This keeps the mainline review-only, approval-gated, and non-mutating.

## Captain Update 2026-05-18 (T162 Review)

T162 is now complete, so the M5 architecture has advanced from aggregate evidence to explicit candidate proposals:

```text
Reproducible feedback loop
  -> PreferencePatchCandidate schema
  -> deterministic privacy-safe feedback clusters
  -> conservative deterministic patch proposals
  -> later manual patch review
  -> only then approved patch compact context
```

The next architectural step is T163, which must add review actions only:

```text
patch proposal report
  -> manual approve/reject/freeze/archive decisions
  -> preserved review metadata/history
  -> no runtime injection yet
```

This keeps the mainline review-only and non-mutating.

## Captain Update 2026-05-18 (T161 Review)

T161 is now complete, so the M5 architecture has advanced from schema-only candidates to explicit aggregate evidence:

```text
Reproducible feedback loop
  -> PreferencePatchCandidate schema
  -> deterministic privacy-safe feedback clusters
  -> later patch proposal CLI
  -> later manual patch review
  -> only then approved patch compact context
```

The next architectural step is T162, which must add proposal generation only:

```text
feedback clusters
  -> conservative deterministic patch proposals
  -> candidate-only PreferencePatchCandidate records
  -> no review/apply/runtime injection yet
```

This keeps the mainline review-only and non-mutating.

## Captain Update 2026-05-18 (T160 Review)

T160 is now complete, so the M5 architecture has an explicit candidate-contract layer:

```text
Reproducible feedback loop
  -> PreferencePatchCandidate schema
  -> later deterministic feedback clusters
  -> later patch proposal CLI
  -> later manual patch review
  -> only then approved patch compact context
```

The next architectural step is T161, which must add clustering only:

```text
validated feedback records
  -> deterministic privacy-safe clusters
  -> cluster ids + aggregate labels + supporting feedback ids
  -> no patch generation yet
```

This keeps the mainline review-only and non-mutating.

## Captain Update 2026-05-18 (M4.5 Review)

M4.5 is now complete. The architecture now has a committed reproducibility layer around both planning and feedback handling:

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlanPolicyEngine
  -> human review
  -> private feedback log
  -> read-only validation report
  -> aggregate safe summary
  -> committed synthetic regression suite
```

The next architectural step may now begin, but only at the candidate-contract layer:

```text
Reproducible feedback loop
  -> PreferencePatchCandidate schema
  -> later clustering
  -> later proposal CLI
  -> later review CLI
  -> only then approved patch runtime context
```

This preserves the mainline contract: no auto-apply, no automatic ContactSkill/Memory mutation, no outbound send behavior, and no platform integration.

## Captain Update 2026-05-18 (T151 Review)

T151 extends the committed architectural safety net from planner-through-policy behavior to direct policy-engine behavior:

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlanPolicyEngine
  -> committed synthetic planner tests
  -> committed synthetic policy-engine tests
  -> reviewable safety baseline
```

The next architectural step is still hardening rather than feature growth:

```text
Planner + policy regression coverage
  -> feedback CLI regression coverage
  -> only then M5 feedback-to-patch candidates
```

## Captain Update 2026-05-18

T150 adds a committed architectural safety net around the existing review-only planner path:

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlan candidates
  -> committed synthetic regression tests
  -> reviewable safety baseline
```

The next architectural step remains inside hardening, not feature expansion:

```text
ReplyPlanner regression coverage
  -> policy fixture suite and direct policy assertions
  -> feedback CLI regression coverage
  -> only then M5 feedback-to-patch candidates
```

## Captain Update 2026-05-17

T142 is now complete, so the architecture has a full review-only M4 feedback loop:

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlan candidates
  -> human review
  -> private feedback log
  -> read-only validation report
  -> aggregate safe summary
```

The next architectural step is not patch generation. The next step is regression hardening:

```text
M4 review-only feedback loop
  -> M4.5 committed regression tests and fixtures
  -> only then M5 feedback-to-patch candidates
```

This preserves the current contract: no auto-send, no realtime integration, no ContactSkill/Memory mutation, and no feedback-to-learning jump before reproducible tests exist.

## Captain Update 2026-05-17

T140 is now complete. The architecture has advanced from "reply planning only" to "reply planning plus private human feedback capture":

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlan candidates
  -> policy/boundary risk flags
  -> human review
  -> private feedback log
```

The next architectural step is T141, which adds a read-only validation layer in front of any future feedback summaries or patch proposals:

```text
private feedback log
  -> feedback validator
  -> safe validation report
  -> later safe summary / later reviewable patch candidates
```

This validator layer must stay non-mutating: it may inspect feedback records and referenced `ReplyPlan` files, but it must not rewrite feedback logs, mutate ContactSkill or MemoryFact stores, or trigger any outbound behavior.

## Captain Update 2026-05-16

M3 is now conditionally closed. The architecture includes a review-only ReplyPlanner path:

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlan candidates
  -> policy/boundary risk flags
  -> human review
```

M4 begins with feedback capture, not autonomous learning:

```text
ReplyPlan candidate
  -> human accept/edit/reject/boundary feedback
  -> private feedback log
  -> later reviewable proposal/versioning tasks
```

Feedback records must not directly mutate ContactSkill, MemoryFact, approved store records, planner templates, or outbound delivery. No auto-send, realtime integration, DB/vector DB expansion, or LLM drafting expansion is allowed in T140.

## Captain Update 2026-05-16: Roadmap Architecture

The architecture is extended as a staged ladder:

```text
M4 Feedback Capture
  -> M4.5 Regression Hardening
  -> M5 PreferencePatch candidates
  -> M6 ContactSkill-compatible derived briefs
  -> M7 optional LLM-assisted ReplyPlanner
  -> M8 RelationshipState
  -> M9 MemoryRetriever abstraction
  -> M10 draft-only BehaviorPlanner
  -> M11 OutboundSendGate + Feishu sandbox
  -> M12 thin WeChat adapter
```

Key architecture decision: platform adapters and external memory systems stay outside the core until send gate, regression tests, approved records, and review metadata are in place.

更新日期：2026-05-15

## 1. 新架构定位

项目主线切换为：

```text
WeFlow JSONL export
  -> offline distillation
  -> evidence-backed memory and contact skill
  -> relationship-aware reply planning
```

旧的 iLink/微信扫描代码与任务不删除，但暂不作为当前主线。

## 2. 数据流

```text
private/chat_history/*.jsonl
  -> ChatHistoryProfiler
  -> WeFlowJsonlAdapter
  -> NormalizedEvent
  -> ConversationChunk
  -> ChunkSummary
  -> MemoryFactCandidate
  -> ContactSkillCandidate
  -> Review artifact
  -> Approved skill/memory store
  -> ReplyPlanner
```

## 3. 计划模块

```text
src/practical_chat_agent/services/chatlog_profile.py
src/practical_chat_agent/services/chatlog_ingestion.py
src/practical_chat_agent/services/conversation_chunking.py
src/practical_chat_agent/services/contact_skill.py
src/practical_chat_agent/services/reply_planner.py
src/practical_chat_agent/exporters/contact_skill_markdown.py
```

第一阶段也可以先用 CLI + service，不必立即新增数据库表。

## 3.1 当前实现状态

T100/T101/T102 已通过 review `PASS`，T103 已接受 Gate M0 = `Conditional`，T110/T111/T112 已通过 review `PASS`，T113/T120/T121/T122 已通过 review `PASS_WITH_WARNINGS`，T114 已确认 Gate M1 = `Conditional`。当前完成的是数据合约、隐私规则、脱敏样例、最小 normalize CLI、conversation chunker v0、蒸馏输出 schema、小样本 summary/fact extraction、ContactSkill review artifact、M1 milestone sample review，以及 M2 的离线 memory/skill file store、evidence validator 和人工 review CLI：

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- `docs/data_contracts/privacy_redaction_rules.md`
- `docs/data_contracts/source_ref_rules.md`
- `examples/payloads/weflow_redacted_sample.jsonl`
- `src/practical_chat_agent/services/chatlog_ingestion.py`
- `src/practical_chat_agent/services/conversation_chunking.py`
- `src/practical_chat_agent/services/chatlog_distillation.py`
- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/exporters/contact_skill_markdown.py`
- `src/practical_chat_agent/core/models.py` 中的 distillation candidate schema
- `docs/data_contracts/distillation_output_contract.md`
- `chatlog-normalize` CLI in `src/practical_chat_agent/app/main.py`
- `chatlog-chunk` CLI in `src/practical_chat_agent/app/main.py`
- `chatlog-distill` CLI in `src/practical_chat_agent/app/main.py`
- `chatlog-build-contact-skill` CLI in `src/practical_chat_agent/app/main.py`
- `chatlog-validate-evidence` CLI in `src/practical_chat_agent/app/main.py`
- `chatlog-review-store` CLI in `src/practical_chat_agent/app/main.py`

T120 已新增离线 memory/skill 文件 store 和 Pydantic 模型，保留 candidate/approved/rejected/frozen/archived 状态、evidence refs、source metadata 与 review metadata；T121 已新增 read-only evidence validator，校验 refs 存在性、状态规则和 human-review gate 交互；T122 已新增人工 review/approve/reject/freeze/archive/export CLI，approval 受 evidence validation report 约束；仍未接数据库或向量库。下一步 T123 将 approved + runtime-ready store records 以 compact brief 形式接入 `ChatContext`，不接 ReplyPlanner，不自动发送。

## 4. 复用现有能力

可复用：

- `core.models.InboundEvent` 的思想，但离线 normalized event 需要更明确的 `source_ref`、`sender_role` 和 `contact_id`。
- `MemoryFact` 作为后续入库目标，但离线 MVP 可先输出 JSONL。
- `ChatMemoryExtractionService` 的 JSON schema/prompt 风格。
- `ChatContextAssembler` 的上下文压缩思想。
- `PolicyEngine` 对 outbound 的保守边界，后续迁移到 reply planner。

暂不复用或不作为主线：

- `WeChatDesktopConnector`
- iLink SDK sandbox
- 微信 delivery connector
- trigger/scheduled actions

## 5. 存储策略

### 私密产物

```text
private/chat_history/
private/distilled/
private/review_workbench/
```

这些路径不提交。

### 可提交合约与脱敏样例

```text
docs/data_contracts/
examples/payloads/weflow_redacted_sample.jsonl
tests/fixtures/weflow_redacted_sample.jsonl
```

这些文件不得包含真实姓名、手机号、地址、完整原文或可识别联系人。

## 6. ContactSkill 与记忆关系

ContactSkill 是面向“如何与此人沟通”的关系技能，不是联系人人格模拟。

```text
ContactSkill
  relationship_state
  communication_style
  boundaries
  preferred_topics
  avoid_topics
  reply_strategy
  evidence_refs
  review status
```

MemoryFacts 是更原子化的事实：

```text
MemoryFact
  semantic / episodic / relationship / procedural / reflection
  claim
  evidence_refs
  status
  conflicts_with
```

运行时应只注入：

- 当前联系人 approved ContactSkill brief。
- 最近对话窗口。
- 与当前话题相关的少量 approved memory facts。
- policy/boundary constraints。

## 7. 安全架构

- 原文不进 git。
- 可提交 fixture 必须人工脱敏。
- LLM 输出必须通过 JSON schema 与 evidence refs 校验。
- 无 evidence 的 claim 直接 rejected 或要求重试。
- ContactSkill 默认 candidate，需要人工 approve。
- 回复 planner 只产草稿，不发送。
- 禁止生成“对方会怎么说”的角色扮演输出。

T130 完成后，M3 的结构边界也已固定：ReplyPlan 只消费 compact `ChatContext` 和 approved-store brief，不回读原始聊天记录，不把 reply generation 和 send 混在一起。

T131 完成后，架构新增 `ReplyPlanner` 作为 review-only 组装层：它从 compact `ChatContext` 生成 T130 `ReplyPlan`，并显式校验 `priority_rank` 与 `contact_id` 对齐。当前仍是 deterministic heuristic baseline；T132 需要把 policy/boundary 风险作为独立控制层补上，而不是把自动发送或实时平台接入并入 planner。

T132 完成后，架构新增 `ReplyPlanPolicyEngine` 作为 planner 内部的 policy/boundary 分类层：它只做检测、风险标记、边界提醒和 confidence penalty，不做发送、不做持久化、不读取私密原文目录。该层仍是 keyword heuristic，T133 需要用匿名 holdout 验证是否足以作为 M3 gate 输入。
