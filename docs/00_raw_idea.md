# Raw Idea

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
