# Decision Log

更新日期：2026-05-13

## D001: 下一阶段以微信主线为优先

- 日期：2026-05-13
- 状态：Accepted
- 背景：会议子系统已经较成熟，聊天 agent 主线需要回到微信数据、记忆、联系人 Skill 和受控回复。
- 决策：下一阶段 roadmap 采用 `Sprint 0 -> Sprint 7` 的微信优先路线。
- 影响：后续任务板优先推进 WeChatBot/iLink POC 和微信 ingestion，不继续扩展会议子系统，除非用户重新指定。

## D002: WeChatBot/iLink SDK 先做仓库外隔离 POC

- 日期：2026-05-13
- 状态：Accepted
- 背景：非官方或半官方 SDK 可能有稳定性、账号和接口风险。
- 决策：Sprint 0 不修改主仓库业务代码，不 vendor SDK，不添加 submodule。先在仓库外 sandbox 验证登录、收消息、reply、媒体和 `context_token`。
- 影响：`Current Unique Task` 设置为 T00；主仓库只新增治理文档和 POC notes。

## D003: 出站消息默认 human-in-the-loop

- 日期：2026-05-13
- 状态：Accepted
- 背景：项目已有 action/policy/delivery 基础，但微信误发送风险高。
- 决策：真实发送必须经过 `PolicyEngine` 和人工审批；群聊默认草稿；主动触发只生成审批草稿。
- 影响：M5 前不得实现微信真实发送，M6 前不得做主动触发。

## D004: 治理文档采用 AI coding workflow

- 日期：2026-05-13
- 状态：Accepted
- 背景：用户要求像新项目一样建立 00-08 文档，并给出可指导 worker 的 `04_task_board.md`。
- 决策：补齐 `docs/00_raw_idea.md`、`01_feasibility_report.md`、`03_architecture.md`、`04_task_board.md`、`05_decision_log.md`、`06_eval_protocol.md`、`07_handoff.md`、`08_risks_and_open_questions.md`，并创建 `docs/tasks/` 任务包目录。
- 影响：后续 worker 以任务包为准，不直接从 roadmap 自由发挥。

## D005: T00 review 通过，推进 T01

- 日期：2026-05-13
- 状态：Accepted
- 背景：`docs/review/T00_review.md` 给出 `PASS`，确认 worker 未越界、未修改主仓库业务代码、未 vendor SDK，并执行了真实安装/导入/二维码阶段探测。
- 决策：T00 标记完成。两个 non-blocking issue 不阻塞任务，均分类为 accepted，并作为 T01 输入项处理。
- Accepted warning N01：T01 需要确认 `Python 3.12.7` sandbox 与项目常用 Python 3.11 环境的兼容边界。
- Accepted warning N02：T01 需要确认官方文档 URL 与本地 `wechatbot-sdk 0.2.1` 行为是否对应。
- Deferred warnings：无。
- Rejected warnings：无。
- 影响：`Current Unique Task` 推进到 T01，但 Gate 0 仍未通过。
