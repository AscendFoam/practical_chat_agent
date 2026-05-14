# Feasibility Report

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
- 当前唯一任务切换为 T122，实现 contact-skill review/approve/reject/export CLI，并且 approve 必须受 T121 evidence validation gate 约束。
- M1 只选 1 个联系人或小样本做 distillation MVP。
- M1 不微调、不自动发送、不接实时平台。
- 所有可提交 fixture 必须脱敏。
