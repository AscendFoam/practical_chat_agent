# Decision Log

更新日期：2026-05-14

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
