# Raw Idea

## Captain Update 2026-05-24 (T192 Review)

T192 has now passed review with `PASS_WITH_WARNINGS`, so the delta-generation step is accepted:

- the repo now has a conservative `RelationshipDeltaCandidate` generation layer on top of T191 signals
- the project still does not permit delta auto-approval, relationship-state mutation, or platform/send behavior
- the next safe step is T193 `Relationship Review CLI`, not compact-context injection or state application

The Current Unique Task therefore moves to T193 `Relationship Review CLI`.

## Captain Update 2026-05-24 (T191 Review)

T191 has now passed review with `PASS_WITH_WARNINGS`, so the signal-extraction step is accepted:

- the repo now has a conservative `RelationshipSignal` layer that turns specific boundary-labeled feedback into evidence-backed signals
- the project still does not permit raw chat-history reads, relationship-state auto-update, or delta generation from T191 alone
- the next safe step is T192 `RelationshipDeltaCandidate`, not review CLI or state mutation

The Current Unique Task therefore moves to T192 `RelationshipDeltaCandidate`.

## Captain Update 2026-05-24 (T190 Review)

T190 has now passed review with `PASS_WITH_WARNINGS`, so the first M8 step is accepted:

- the repo now has a conservative `RelationshipState` schema and `RelationshipDeltaCandidate` contract
- the project still does not permit signal extraction from raw chat history, automatic state mutation, delta auto-approval, or runtime send behavior
- the next safe step is T191 `Relationship Signal Extractor`, not delta application or context injection

The Current Unique Task therefore moves to T191 `Relationship Signal Extractor`.

## Captain Update 2026-05-23 (T185 / M7 Review)

T185 has now passed review with `PASS_WITH_WARNINGS`, and the M7 milestone review now allows M7 to close:

- the repo now has a committed, opt-in hybrid planner that remains review-only and template-compatible
- the project no longer needs to treat the holdout-stage gaps as open gate conditions, because language alignment, conservative safety prompting, label normalization, and merge-path regression coverage are now committed
- the remaining concerns are real but no longer blocking: heuristic safety-context detection, prompt-level language enforcement, and uncalibrated confidence remain future hardening work
- the next safe step is T190 `RelationshipState Schema`, not more M7 repair work

The Current Unique Task therefore moves to T190 `RelationshipState Schema`.

## Captain Update 2026-05-23 (T184 Review)

T184 has now passed review with `PASS_WITH_WARNINGS`, but the M7 holdout stage remains `Conditional`:

- the repo now has evidence that the hybrid planner improves naturalness and evidence usage on anonymized holdout scenarios
- the project still does not permit claiming M7 is complete, because language mismatch, thin-context safety drift, and merge-path test coverage remain open
- the next safe step is T185 `Hybrid Planner Language and Safety Alignment`, not entry into M8

The Current Unique Task therefore moves to T185 `Hybrid Planner Language and Safety Alignment`.

## Captain Update 2026-05-23 (T183 Review)

T183 has now passed review with `PASS_WITH_WARNINGS`, so the hybrid planner integration step is accepted:

- the repo now has an opt-in hybrid planner surface that can combine template and optional LLM candidates without making LLM behavior the default
- the project still does not permit quality claims without holdout evaluation, outbound behavior, or hidden state mutation
- the next safe step is T184 `LLM Planner Holdout Eval`, not more planner wiring

The Current Unique Task therefore moves to T184 `LLM Planner Holdout Eval`.

## Captain Update 2026-05-23 (T182 Review)

T182 has now passed review with `PASS_WITH_WARNINGS`, so the validator-hardening step is accepted:

- the repo now has a shared deterministic validator layer and broader regression coverage for template and LLM candidate paths
- the project still does not permit default LLM mode, outbound behavior, or hidden state mutation
- the next safe step is T183 `Hybrid ReplyPlanner`, but only as an opt-in, review-only integration step

The Current Unique Task therefore moves to T183 `Hybrid ReplyPlanner`.

## Captain Update 2026-05-23 (T181 Review)

T181 has now passed review with `PASS_WITH_WARNINGS`, so the offline LLM generator step is accepted:

- the repo now has an opt-in offline CLI that can turn safe `ChatContext` JSON into a validated private `LLMReplyPlan` artifact or structured refusal
- the project still does not permit hybrid planner behavior, default LLM mode, outbound behavior, or hidden state mutation
- the next safe step is T182 `Candidate Validator`, not immediate planner integration

The Current Unique Task therefore moves to T182 `Candidate Validator`.

## Captain Update 2026-05-23 (T180 Review)

T180 has now passed review with `PASS`, so the contract-only M7 opening step is accepted:

- the repo now has an explicit additive contract for optional LLM-generated reply candidates
- the project still does not permit hybrid planner behavior, default LLM mode, outbound behavior, or hidden state mutation
- the next safe step is T181 `LLM Candidate Offline CLI`, not immediate planner integration

The Current Unique Task therefore moves to T181 `LLM Candidate Offline CLI`.

## Captain Update 2026-05-23 (M6 Review)

M6 has now passed milestone review with `Allow`:

- the repo now has a complete compatibility-first decomposition path for approved `ContactSkill`
- the project still does not permit immediate LLM calls, planner-behavior changes, outbound behavior, or hidden state mutation
- the next safe step is the narrow M7 opening task T180 `LLM Candidate Generator Contract`, not runtime LLM integration

The Current Unique Task therefore moves to T180 `LLM Candidate Generator Contract`.

## Captain Update 2026-05-23 (T174 Review)

T174 has now passed review with `PASS`, so the fifth M6 step is accepted:

- the repo now has derived-brief context integration with preserved `ApprovedContactSkillBrief` fallback
- the project still does not permit planner behavior changes, migration, or replacement of the existing compact-context path
- the next step is milestone review for M6, not additional M6 worker implementation

## Captain Update 2026-05-23 (T173 Review)

T173 has now passed review with `PASS`, so the fourth M6 step is accepted:

- the repo now has a pure lazy projection layer from approved `ContactSkill` store records into all three derived briefs
- the project still does not permit `ChatContext` integration changes to bypass the existing fallback path or approved-patch compact-context path
- the next safe step is T174 derived-brief context integration, not planner behavior changes

The Current Unique Task therefore moves to T174 `Derived Briefs Context Integration`.

## Captain Update 2026-05-23 (T172 Review)

T172 has now passed review with `PASS`, so the third M6 step is accepted:

- the repo now has committed policy and boundary derived-brief schemas for approved `ContactSkill`
- the project still does not permit runtime integration, migration, deprecation of `ContactSkill`, or persisted derived-brief storage
- the next safe step is T173 projection service work, not `ChatContext` integration

The Current Unique Task therefore moves to T173 `ContactSkillProjectionService`.

## Captain Update 2026-05-23 (T171 Review)

T171 has now passed review with `PASS`, so the second M6 step is accepted:

- the repo now has the first additive derived-brief schema for approved `ContactSkill`
- the project still does not permit projection service logic, runtime integration, migration, or deprecation of `ContactSkill`
- the next safe step is schema-only T172 `CommunicationPolicyBrief` + `BoundaryProfileBrief`, not projection or context wiring

The Current Unique Task therefore moves to T172 `CommunicationPolicyBrief` Schema.

## Captain Update 2026-05-22 (T170 Review)

T170 has now passed review with `PASS`, so the first M6 step is accepted:

- the repo now has a documented compatibility-first decomposition design for approved `ContactSkill`
- the project still does not permit runtime mutation, data migration, deprecation of `ContactSkill`, or derived-brief persistence
- the next safe step is schema-only T171 `PartnerPersonaBrief`, not projection or runtime integration

The Current Unique Task therefore moves to T171 `PartnerPersonaBrief` Schema.

## Captain Update 2026-05-22 (T164 Review)

T164 has now passed review with `PASS_WITH_WARNINGS`, so the fifth M5 step is accepted:

- the repo now has compact approved-patch context integration behind explicit approval gates
- the project still does not permit automatic learning, hidden state mutation, or non-approved patch influence on runtime context
- the next safe step is no longer patch-context wiring but M6-compatible decomposition design work

The Current Unique Task therefore moves to T170 ContactSkill Decomposition Design.

## Captain Update 2026-05-22 (T163 Review)

T163 has now passed review with `PASS_WITH_WARNINGS`, so the fourth M5 step is accepted:

- the repo now has explicit human review actions for patch candidates
- the project still does not permit automatic learning, auto-apply, runtime injection without a dedicated context layer, or hidden ContactSkill/Memory mutation
- the next safe step is no longer patch review but approved-patch compact context integration

The Current Unique Task therefore moves to T164 Approved Patch Compact Context.

## Captain Update 2026-05-18 (T162 Review)

T162 has now passed review with `PASS_WITH_WARNINGS`, so the third M5 step is accepted:

- the repo now has deterministic, candidate-only patch proposal generation from aggregate feedback clusters
- the project still does not permit automatic learning, auto-approve, auto-apply, runtime injection, or hidden ContactSkill/Memory mutation
- the next safe step is no longer proposal generation but manual patch review with explicit human decisions

The Current Unique Task therefore moves to T163 Patch Review CLI.

## Captain Update 2026-05-18 (T161 Review)

T161 has now passed review with `PASS_WITH_WARNINGS`, so the second M5 step is accepted:

- the repo now has a deterministic, privacy-safe feedback clustering layer
- the project still does not permit automatic learning, auto-approve, auto-apply, runtime injection, or hidden ContactSkill/Memory mutation
- the next safe step is no longer clustering but candidate-only patch proposal generation from aggregate evidence

The Current Unique Task therefore moves to T162 Patch Proposal CLI.

## Captain Update 2026-05-18 (T160 Review)

T160 has now passed review with `PASS_WITH_WARNINGS`, so the first M5 step is accepted:

- the repo now has a candidate-only `PreferencePatchCandidate` contract with evidence via `supporting_feedback_ids`
- the project still does not permit automatic learning, auto-apply, runtime injection, or hidden ContactSkill/Memory mutation
- the next safe step is no longer schema definition but deterministic clustering of repeated feedback patterns

The Current Unique Task therefore moves to T161 Feedback Clusterer.

## Captain Update 2026-05-18 (M4.5 Review)

`docs/review/M4_5_review.md` now allows the project to leave regression hardening and enter the first M5 task.

- the repo can now prove planner, policy, and feedback-loop behavior from committed synthetic tests
- the next safe step is no longer "more hardening" but "define a candidate-only patch contract"
- the project is still explicitly not doing automatic learning, automatic sending, or hidden state mutation

The Current Unique Task therefore moves to T160 PreferencePatch Schema.

## Captain Update 2026-05-18 (T151 Review)

T151 has now passed review with `PASS_WITH_WARNINGS`, so the policy-fixture half of M4.5 is accepted and committed.

- direct `ReplyPlanPolicyEngine` behavior is now reproducible from committed tests
- synthetic fixture coverage now distinguishes thin-context, loaded-but-no-skill, degraded-store, and boundary-sensitive cases more explicitly
- the remaining hardening gap before M5 is now concentrated in T152 feedback CLI regression coverage

The Current Unique Task therefore moves to T152 Feedback CLI Regression Tests. The project is ready to commit the T151 slice and continue, but not yet ready to open M5 feedback-to-patch work.

## Captain Update 2026-05-18

T150 has now passed review with `PASS_WITH_WARNINGS`, and the project has its first committed regression-hardening slice for M4.5:

- ReplyPlanner structure is now reproducible from committed tests
- privacy leakage, contact alignment, ranking, thin-context, and baseline policy behavior now have deterministic coverage
- the project still does not have enough clean-environment coverage to enter M5

The Current Unique Task therefore moves to T151 Policy Fixture Suite, not to feedback-to-patch work. The next step is to make policy-layer false-positive, false-negative, over-proactivity, and direct policy-engine expectations more explicit and reviewable.

## Captain Update 2026-05-17

T142 has now passed review with `PASS_WITH_WARNINGS`, so the intended M4 loop is functionally complete:

- private feedback can be recorded
- feedback logs can be validated read-only
- aggregate feedback summaries can be exported without leaking private text

This does not yet justify moving into M5 feedback-to-patch work. The Captain M4 review is `Conditional`: the remaining gap is clean-environment reproducibility, because committed regression tests and committed synthetic fixtures are still missing. The Current Unique Task therefore moves to T150 ReplyPlanner Regression Tests rather than to patch generation.

## Captain Update 2026-05-17

T140 has now passed review with `PASS_WITH_WARNINGS`.

The project can continue into T141, but M4 still remains strictly review-only:

- feedback may be recorded and validated
- feedback may not automatically update ContactSkill, MemoryFact, planner templates, or outbound behavior
- no auto-send, realtime integration, DB/vector DB expansion, or LLM drafting expansion is allowed

The immediate next need is not "learning from feedback" but making sure the feedback log itself is trustworthy, reference-valid, privacy-safe, and read-only to downstream state. That is why the Current Unique Task moves to T141 Feedback Log Validator rather than directly to proposal generation.

## Captain Update 2026-05-16

T133 has passed review with `PASS_WITH_WARNINGS`, and the Captain M3 review sets Gate M3 to `Conditional`.

The project may proceed to M4/T140, but only as a review-only feedback capture loop. The ReplyPlanner is structurally complete for M3, not quality-mature: current drafts remain template-driven, T133 naturalness is 3/5, evidence usage is 3/5, and no committed regression tests exist yet.

Current mainline remains offline-first WeFlow distillation and review-only reply planning. T140 must record accept/edit/reject/boundary feedback without auto-sending, realtime platform integration, automatic ContactSkill/Memory mutation, fine-tuning, or relationship-aware maturity claims.

## Captain Update 2026-05-16: Design Roadmap Alignment

`docs/reference/gpt的后续设计思路(更新版).md` is accepted as directionally aligned with the project, with one operational refinement: near-term work must be even more staged.

Adopted:

- Keep ContactSkill as a compatibility/evidence aggregate; decompose later through derived briefs, not deletion.
- Keep M4 as feedback capture/validation/summary only.
- Add M4.5 regression hardening before feedback-to-patch, LLM-assisted drafting, RelationshipState, MemoryRetriever, BehaviorPlanner, or platform adapters.
- Put Feishu/WeChat behind OutboundSendGate and after local fake adapter.

Not adopted for immediate execution:

- No immediate Mem0 integration.
- No immediate Feishu/WebSocket/platform work.
- No immediate ContactSkill replacement.
- No automatic learning, automatic sending, or proactive behavior.

更新日期：2026-05-15

## 1. 解决什么问题

用户已经通过 WeFlow 导出了微信聊天记录。现在项目要解决的问题是：如何把这些私密、杂乱、长期积累的对话记录，转化为一个本地可控、可审计、具有长期关系感知能力的 chat agent。

这个 agent 的目标不是复刻某个联系人，也不是训练一个数字克隆，而是帮助用户：

- 回忆与某个联系人相关的长期上下文。
- 理解关系状态、沟通风格和边界。
- 生成更有分寸、更符合用户意图的回复草稿。
- 在用户纠错后更新记忆与 ContactSkill。

## 2. 为什么现在值得做

此前 iLink/扫码路线在 T01 被 BLOCK，且用户已明确不再需要微信扫描读取记录。项目现在有更低风险、更直接的数据来源：`private/chat_history/` 下的 WeFlow JSONL 导出。

这使得下一阶段可以绕开平台接入风险，直接验证核心假设：

> 历史对话记录能否被稳定蒸馏为可追溯的 MemoryFacts、ContactSkill 和关系感知回复策略。

## 3. 最小可验证实验

MVP：

```text
WeFlow JSONL
  -> normalized_events.jsonl
  -> chunks.jsonl
  -> chunk_summaries.jsonl
  -> memory_facts.jsonl
  -> contact_skill.candidate.json
  -> contact_skill.review.md
```

T100 已完成 schema profiling 与 normalized event 合约，并通过 reviewer `PASS`。T101 已完成隐私脱敏规则、source_ref 规则和红线样例，并通过 reviewer `PASS`。T102 已完成最小 normalize CLI，并通过 reviewer `PASS`。T103 已接受 Gate M0 = `Conditional`，允许进入 M1 离线蒸馏 MVP。T110 已完成 conversation chunker v0，并通过 reviewer `PASS`。T111 已完成蒸馏输出 schema 和 JSON contract，并通过 reviewer `PASS`。T112 已完成小样本 chunk summary 与 fact extraction 的 LLM/JSON 校验管线，并通过 reviewer `PASS`。T113 已完成 ContactSkill candidate 与 Markdown review artifact，并通过 reviewer `PASS_WITH_WARNINGS`。T114 已确认 Gate M1 = `Conditional`。T120 已完成离线 memory/skill 文件 store 与 review metadata，并通过 reviewer `PASS_WITH_WARNINGS`。T121 已完成 evidence validator 与状态规则，并通过 reviewer `PASS_WITH_WARNINGS`。T122 已完成人工 review/approve/reject/freeze/export CLI，并通过 reviewer `PASS_WITH_WARNINGS`。

## 4. 最相似已有工作

- RAG/长期记忆助手：可检索历史，但常缺少关系状态和边界建模。
- Personal CRM：联系人模型成熟，但多为人工维护。
- Mem0/Letta/MemoryBank 类记忆系统：记忆层思想可借鉴，但不应早期引入复杂框架。
- 微调/数字克隆项目：能学风格，但事实不可控、难删除，不适合本项目当前阶段。

## 5. 失败标准

- 无法从 WeFlow JSONL 稳定解析联系人、时间和方向。
- 生成的事实没有 evidence refs。
- ContactSkill 出现无证据的人格判断或冒充倾向。
- 私密聊天原文被写入可提交目录。
- 用户 review 后认为 skill 与真实关系认知偏差过大。

## 当前决策

`Go to offline distillation MVP`。

暂停 iLink/微信扫描主线，M0 已条件通过，M1 已条件通过。当前唯一任务切到 T123：Context Integration。

2026-05-15 之后，T123 和 T130 已完成，当前唯一任务转入 T131 ReplyPlanner。核心约束不变：offline-first、review-only、只消费 approved + runtime-ready 的 compact context。

2026-05-16：T131 已通过 `PASS_WITH_WARNINGS` 并关闭为安全 wiring baseline；它能生成 review-only `ReplyPlan`，但关系感知仍偏模板化。当前唯一任务转入 T132 Reply Policy，先补边界、禁忌话题、过度主动和冒充风险控制；M3 尚未完成，不能进入 M4。

2026-05-16：T132 已通过 `PASS_WITH_WARNINGS` 并关闭为 policy/boundary baseline；它增强了边界、禁忌话题、过度主动和冒充风险的显式标记，但仍是 heuristic template-based planner。当前唯一任务转入 T133 Holdout Eval，用匿名场景判断 M3 是否可条件进入下一阶段；仍不自动发送、不接实时平台。
