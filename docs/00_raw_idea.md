# Raw Idea

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
