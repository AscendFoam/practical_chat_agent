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
- Captain 已将 T100/T101/T102 标记完成，Current Unique Task 推进到 T103。
- T101 worker 已产出隐私脱敏规则、source_ref 规则和补充了 `source_ref/raw_ref` 预览形态的合成 fixture，并通过 reviewer `PASS`。
- T102 worker 已产出最小 normalize CLI，并完成 dry-run 与 limit 小样本验证，reviewer 判定 `PASS`。

## 2. 当前唯一任务

T103: M0 review，确认能进入离线蒸馏 MVP。

任务包：`docs/tasks/M0_weflow_data_contract/T103_m0_review.md`

状态：可交给 milestone reviewer 执行。T102 已 review `PASS`，不需要 worker 返修。

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

## 4. T101 完成记录

- `docs/data_contracts/privacy_redaction_rules.md`
- `docs/data_contracts/source_ref_rules.md`
- `examples/payloads/weflow_redacted_sample.jsonl` 已加入 `eventIdPreview`、`sourceRefPreview`、`rawRefPreview`

Reviewer 结论：

- `docs/review/T101_review.md` verdict 为 `PASS`。
- N01 deferred：type=80/chatRecords fixture 覆盖继续留给 T102/T150。
- N02 accepted：fixture preview hex 值可作为注释占位，不要求返修。
- N03 deferred：结构化替换 token 与实际脱敏需求的对齐交给 T102 实现时校验。

T102 必须遵守：

- `docs/data_contracts/privacy_redaction_rules.md` 的 Field Handling Matrix。
- `docs/data_contracts/source_ref_rules.md` 的 Allowed Public Shape。
- normalize 输出只能进入 `private/distilled/`。
- stdout 和可提交目录不得出现真实聊天原文、真实文件名、真实联系人姓名或真实平台 ID。

## 5. T102 完成记录

- `src/practical_chat_agent/services/chatlog_ingestion.py`
- `src/practical_chat_agent/app/main.py`

Reviewer 结论：

- `docs/review/T102_review.md` verdict 为 `PASS`。
- N01 deferred：无效 timezone 静默降级 warning 留给 T103/T150 判断是否需要补。
- N02/N03 deferred：双次读取和全量内存缓存留给 T110/T150 处理。
- N04 accepted：系统消息关键词硬编码作为 MVP 兜底可接受。
- N05 deferred：结构化 PII token 替换推迟到 T112+ 蒸馏阶段。
- N06 deferred：单文件 sender_role 稳健性留给 T114/T150 验证。

已验证：

- `chatlog-normalize` 支持 `--input`、`--output`、`--limit`、`--dry-run`、`--timezone-name`。
- 输入限制在 `private/chat_history/**`，输出限制在 `private/distilled/**`。
- stdout/report 不包含真实原文、真实文件名、真实联系人姓名或真实平台 ID。
- normalized event 字段与 T100/T101 合约对齐。

## 6. Milestone Reviewer 启动提示

```text
你是 milestone reviewer。

请先阅读：
- README.md
- AGENTS.md
- docs/02_experiment_plan.md
- docs/06_eval_protocol.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/review/T100_review.md
- docs/review/T101_review.md
- docs/review/T102_review.md

本轮只完成：
- docs/tasks/M0_weflow_data_contract/T103_m0_review.md

规则：
1. 不写代码。
2. 不读取或输出 private/chat_history 原文。
3. 综合 T100-T102 产物和 review，给出 Gate M0 verdict: Allow / Conditional / Block。
4. 明确是否可以进入 M1。
5. 若 verdict 不是 Block，推荐下一唯一任务但不要执行。
6. 写入 docs/review/T103_milestone_review.md，并按任务包更新治理文档。
```

## 7. Reviewer 启动提示

```text
你是 Claude Code reviewer / milestone reviewer。

请先阅读：
- docs/02_experiment_plan.md
- docs/04_task_board.md
- docs/07_handoff.md

只读审查本次 diff，不要修改文件。

重点检查：
1. T100-T102 是否满足 M0 Gate。
2. 是否有真实聊天原文、真实联系人姓名、真实文件名或真实平台 ID 进入可提交目录。
3. T102 CLI 是否足以支撑 M1 chunker 输入。
4. T102 non-blocking issues 是否需要作为 M1 进入条件。
5. 文档与 task board 是否一致。

输出 Gate M0 verdict: Allow / Conditional / Block，并写入 docs/review/T103_milestone_review.md。
```

## 8. 下一步顺序

1. Milestone reviewer 执行 T103。
2. Captain 根据 review 更新 `04_task_board`、`05_decision_log`、`07_handoff`，并按需要处理风险文档。
3. 若 Gate M0 `Allow` 或 `Conditional`，推荐 M1 下一任务但不执行。
4. 若 Gate M0 `Block`，停止并交给用户裁决或创建修复任务包。

## 9. 历史顺序

1. T100 review `PASS`，已完成 schema profile 与 normalized event contract。
2. T101 review `PASS`，已完成 privacy/source_ref rules。
3. T102 review `PASS`，已完成 `chatlog-normalize` 最小 CLI。

## 10. 注意事项

- `.gitignore` 中已有 `private/`，保留这个安全措施。
- 不要还原用户手动迁移 docs 目录结构的操作。
- 不要读取或输出 `.env`。
- 不要把 `private/chat_history` 的真实文件名或聊天内容写入 docs。
- 当前阶段不做微调、不做自动发送、不做微信扫描。
