# Handoff

更新日期：2026-05-13

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

## 2. 当前唯一任务

T100: WeFlow JSONL schema profiling 与 normalized event 合约。

任务包：`docs/tasks/M0_weflow_data_contract/T100_schema_profile.md`

状态：ready for worker，不要由 Captain 直接执行。

## 3. 为什么现在做 T100

在实现任何 parser、chunker 或 LLM 抽取前，必须先知道 WeFlow JSONL 的真实字段结构、消息类型、时间戳格式、联系人/方向映射和隐私风险。

T100 的目标不是提取关系知识，而是建立后续所有任务依赖的数据合约，并确保不泄露私密聊天内容。

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
- docs/tasks/M0_weflow_data_contract/T100_schema_profile.md

规则：
1. 只改 Allowed files。
2. 可以读取 private/chat_history 做字段统计，但不要把真实原文、真实姓名、原始文件名写进可提交文件。
3. 不做 LLM 抽取，不做 chunker，不做数据库，不做实时微信接入。
4. 完成后运行 Verification。
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

输出 Verdict: PASS / PASS_WITH_WARNINGS / BLOCK，并写入 docs/review/T100_review.md。
```

## 6. 下一步顺序

1. Worker 执行 T100。
2. Reviewer 审查 T100。
3. Captain 根据 review 更新 `04_task_board`、`05_decision_log`、`07_handoff`、`08_risks_and_open_questions`。
4. T100 通过后推进 T101 或 T102。

## 7. 注意事项

- `.gitignore` 中已有 `private/`，保留这个安全措施。
- 不要还原用户手动迁移 docs 目录结构的操作。
- 不要读取或输出 `.env`。
- 不要把 `private/chat_history` 的真实文件名或聊天内容写入 docs。
- 当前阶段不做微调、不做自动发送、不做微信扫描。

