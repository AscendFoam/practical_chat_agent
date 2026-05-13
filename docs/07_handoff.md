# Handoff

更新日期：2026-05-14

## 1. 当前状态

项目路线已切换。

旧路线：

- T00：WeChatBot/iLink SDK 安装和二维码阶段探测，review `PASS`。
- T01：登录/session 验证，review `BLOCK`。
- 用户已决定不修 T01，不再推进微信 SDK 登录、扫描或聊天记录读取路线。

新路线：

- 用户已通过 WeFlow 工具导出聊天记录。
- 私密数据位于 `private/chat_history/`，受 `.gitignore` 保护。
- 下一阶段直接做“对话记录驱动的长期关系感知 chat agent”。
- 当前目标是离线蒸馏 MVP：JSONL -> normalized events -> chunks -> memory facts -> ContactSkill -> review -> relationship-aware reply planner。
- T100 worker 已产出 schema profile、normalized event contract 和合成脱敏 fixture，并通过 reviewer `PASS`。
- Captain 已将 T100 标记完成，Current Unique Task 推进到 T101。

## 2. 当前唯一任务

T101: 设计脱敏规则、source_ref 规则和最小红线测试样例。

任务包：`docs/tasks/M0_weflow_data_contract/T101_privacy_source_refs.md`

状态：可交给 worker 执行。T100 已 review `PASS`，不需要 worker 返修。

## 3. T100 完成记录

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- `examples/payloads/weflow_redacted_sample.jsonl`

worker 侧当前已确认的高信号结论：

- 4 个 WeFlow JSONL 文件共 38,289 行，全部可解析，无坏行。
- 顶层行类型稳定分为 `header`、`member`、`message` 三类。
- 真正需要进入 normalized event 的是 `_type=message` 行，共 38,253 条。
- `timestamp` 稳定为 Unix epoch seconds。
- `type` 是消息类型主候选字段，其中 `0`、`7`、`25`、`80` 占绝大多数。
- `replyToMessageId` 可作为引用链路候选；`chatRecords` 可作为转发聊天记录候选。
- 脱敏/合成样例已生成，不包含真实原文、真实联系人姓名或真实文件名。

Reviewer 结论：

- `docs/review/T100_review.md` verdict 为 `PASS`。
- N01 accepted：Q100/Q104 关闭依据更新为 “T100 worker draft + review PASS”。
- N02 deferred：type=80/chatRecords fixture 覆盖留给 T102/T150。
- N03 deferred：event_id 的 SHA-1/SHA-256 取舍留给 T102。

## 4. Worker 启动提示

```text
你是 Codex worker。

请先阅读：
- README.md
- AGENTS.md
- docs/02_experiment_plan.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/reference/gpt关于后续chat agent设计的思路.md
- docs/deep_research_reports/对话记录驱动的长期关系感知chat agent.md

本轮只完成：
- docs/tasks/M0_weflow_data_contract/T101_privacy_source_refs.md

规则：
1. 只改 Allowed files。
2. 读取 T100 outputs，必要时只用统计结论解释隐私风险；不要把真实原文、真实姓名、原始文件名写进可提交文件。
3. 不实现脱敏器，不做 LLM 抽取，不做 chunker，不做数据库，不做实时微信接入。
4. 更新 redacted sample 以覆盖 source_ref/raw_ref。
5. 最后报告：改了什么、如何验证、剩余风险。
```

## 5. Reviewer 启动提示

```text
你是 Claude Code reviewer。

请先阅读：
- docs/02_experiment_plan.md
- docs/04_task_board.md
- docs/07_handoff.md

只读审查本次 diff，不要修改文件。

重点检查：
1. 是否泄露 private/chat_history 的真实聊天原文、真实联系人姓名或可识别文件名。
2. 是否真的建立了 WeFlow schema profile 和 normalized event contract。
3. 是否越界实现了 LLM 抽取、chunker、数据库或实时微信接入。
4. 脱敏 fixture 是否安全。
5. 文档是否把计划写成已完成事实。

输出 Verdict: PASS / PASS_WITH_WARNINGS / BLOCK，并写入 docs/review/T101_review.md。
```

## 6. 下一步顺序

1. Worker 执行 T101。
2. Reviewer 审查 T101 worker 交付。
3. Captain 根据 review 更新 `04_task_board`、`05_decision_log`、`07_handoff`、`08_risks_and_open_questions`。
4. 若 T101 review `PASS` 或 `PASS_WITH_WARNINGS`，推进 T102。
5. 若 T101 review `BLOCK`，只修 blocking issue，并最多自动复审一次。

## 7. 注意事项

- `.gitignore` 中已有 `private/`，保留这个安全措施。
- 不要还原用户手动迁移 docs 目录结构的操作。
- 不要读取或输出 `.env`。
- 不要把 `private/chat_history` 的真实文件名或聊天内容写入 docs。
- 当前阶段不做微调、不做自动发送、不做微信扫描。
