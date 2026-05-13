# Decision Log

更新日期：2026-05-13

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

