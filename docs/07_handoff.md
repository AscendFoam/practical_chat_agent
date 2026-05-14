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
- Captain 已将 T100/T101/T102/T103/T110/T111 标记完成，Current Unique Task 推进到 T112。
- T101 worker 已产出隐私脱敏规则、source_ref 规则和补充了 `source_ref/raw_ref` 预览形态的合成 fixture，并通过 reviewer `PASS`。
- T102 worker 已产出最小 normalize CLI，并完成 dry-run 与 limit 小样本验证，reviewer 判定 `PASS`。
- T103 milestone review 已接受 Gate M0 = `Conditional`，允许进入 M1；T110 conversation chunker v0 与 T111 distillation schemas 均已通过 reviewer `PASS`。

## 2. 当前唯一任务

T112: 实现 chunk summary 与 fact extraction 的 LLM/JSON 校验管线。

任务包：`docs/tasks/M1_offline_distillation_mvp/T112_summary_fact_extraction.md`

状态：T111 review 已 `PASS`，下一步只推荐 T112，不自动执行。T112 可以开始小样本 LLM/JSON 抽取，但必须用 T111 schema 校验输出，拒绝无 `evidence_refs` 的 claim，并禁止把私密原文或 LLM 原始输入输出写入可提交目录。

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

## 6. T103 完成记录

- `docs/review/T103_milestone_review.md`
- `docs/review/T103_review.md`

Reviewer 结论：

- Gate M0 = `Conditional` accepted。
- M0 五条硬性要求全部满足。
- 允许进入 M1，下一唯一任务为 T110。

M1 必须承接的条件：

- T110/T150 继续覆盖 `type=80` / `chatRecords` 的保守处理与测试。
- T110/T114/T150 保留并验证 `sender_role`、timezone fallback、性能/内存相关不确定性。
- T112+ 任意 LLM-facing 蒸馏步骤继续遵守 T101 隐私边界，不把私有 normalize 文本扩散到可提交产物。

## 7. T110 完成记录

- 代码改动：
  - `src/practical_chat_agent/services/conversation_chunking.py`
  - `src/practical_chat_agent/app/main.py`
- 已实现内容：
  - 新增 `ConversationChunkingService`，消费 `private/distilled/**/normalized_events.jsonl`。
  - 新增 `chatlog-chunk` CLI，默认把 `chunks.jsonl` 和更新后的 `run_report.json` 写回同一个 `private/distilled/<run_id>/` 目录。
  - chunk v0 仅使用保守边界：`conversation/contact` 变化、时间间隔过大、单 chunk 消息数上限、输入结束。
  - 每个 chunk 保留 `chunk_id`、`contact_id`、`conversation_id`、`event_ids`、`time_range`、`message_count`、`chunking_reason`。
  - chunk 级产物继续传递 T102 的不确定性信号：`source_message_type_codes` / `source_message_type_counts`、`message_type_counts`、`interaction_flag_counts`、`risk_flag_counts`、`events_with_interaction_flags`、`events_with_risk_flags`。
  - 未引入 LLM、embedding、ContactSkill、数据库或实时平台接入；chunk 输出不写聊天原文。
- 已完成验证：
  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/conversation_chunking.py src/practical_chat_agent/app/main.py`
  - `$env:PYTHONPATH='src'; & 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main chatlog-chunk --input private/distilled/t102_smoke --limit 12`
  - 结果：成功写出 `private/distilled/t102_smoke/chunks.jsonl`，并把 chunking 报告写入 `private/distilled/t102_smoke/run_report.json`。
  - 该小样本共消费 12 条 normalized events，生成 1 个 chunk；`chunking_reason=manual`，`boundary_flags=["end_of_input"]`，且保留了 `type=7` / `type=80` 对应的 mixed/system 风险与交互统计。
- Reviewer 结论：
  - `docs/review/T110_review.md` verdict 为 `PASS`。
  - 确认 T110 只实现 conversation chunker v0，未越界引入 LLM、embedding、ContactSkill、数据库或实时平台。
  - 确认 chunk 输出不写聊天原文，stdout/report 未发现真实聊天内容泄露。
  - 确认 T102 的 `source_message_type_code`、`risk_flags`、`interaction_flags`、`message_type`、`sender_role` 等不确定性信号已被保留或汇总传递。
- Non-blocking 处理：
  - N01 accepted：`chunking_reason="manual"` 对结构边界表达偏粗，但当前 `boundary_flags` 已保留细节；后续 T112/T150 使用时不要只依赖 reason。
  - N02 accepted/deferred：non-monotonic timestamp warning 当前只进入 report，不阻塞；若后续样本出现排序问题，由 T150 增加诊断覆盖。
  - N03 accepted/deferred：`run_report.json` 的 chunking 报告形态足够 MVP 使用；T114/T150 可按实际抽查需求扩展。
  - N04 deferred：自动化测试仍留给 T150。
  - N05 accepted：`topic_hint` 是 optional，T110 不生成 topic hint 合理，后续由 T112+ 摘要/语义阶段补足。

## 8. T111 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/distillation_output_contract.md`
  - `docs/07_handoff.md`
- 已实现内容：
  - 在 `core.models` 中新增可复用 schema：
    - `DistillationClaim`
    - `ChunkSummaryObservation`
    - `ChunkSummary`
    - `MemoryFactCandidate`
    - `ContactSkillTopicPreference`
    - `ContactSkillPattern`
    - `ContactSkillImportantEvent`
    - `ContactSkillRelationshipState`
    - `ContactSkillCommunicationStyle`
    - `ContactSkillUserSidePreferences`
    - `ContactSkillReplyStrategy`
    - `ContactSkillUsageBoundary`
    - `ContactSkillCandidate`
  - 所有 fact / claim / skill 相关结构均支持 `evidence_refs`、`confidence`、`sensitivity`、`status`。
  - `ContactSkillCandidate` 明确加入 `usage_boundary`，默认禁止 `persona_clone`、`impersonation`、`autonomous_contact_simulation`。
  - 新增 `docs/data_contracts/distillation_output_contract.md`，固定 T112/T113 所需 JSON contract、状态约定、敏感度约定和反 impersonation 边界。
  - 未调用 LLM、未生成真实蒸馏结果、未写数据库 migration。
- 已完成验证：
  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/core/models.py`
  - 结果：模型文件编译通过。
- Reviewer 结论：
  - `docs/review/T111_review.md` verdict 为 `PASS`。
  - 确认 T111 完整定义 `ChunkSummary`、`MemoryFactCandidate`、`ContactSkillCandidate` 及辅助结构。
  - 确认所有 fact/claim/skill 结构强制或支持 `evidence_refs`、`confidence`、`sensitivity`、`status`。
  - 确认 `ContactSkillUsageBoundary` 默认禁止 `persona_clone`、`impersonation`、`autonomous_contact_simulation`。
  - 确认无 LLM 调用、无数据库 migration、无 `private/` 泄露。
- Non-blocking 处理：
  - N01 accepted：`ContactSkillRelationshipState` / `ContactSkillCommunicationStyle` 的部分字段保留自由字符串，MVP 阶段可接受；后续可按实际 LLM 输出收紧。
  - N02 accepted/deferred：`redaction_policy` 当前使用 `dict[str, Any]` 可接受；T120/T150 可视 store/review 需要改为结构化 model。
  - N03 deferred：`DistillationMemoryType` 与现有 `MemoryType` enum 的映射交给 T120。
  - N04 deferred：`created_at` / `updated_at` 由 T120 store 或产物写入层补充。
  - N05 deferred：Pydantic 约束自动化测试交给 T150。

## 9. Worker 启动提示

```text
你是 Codex worker。

请先阅读：
- README.md
- AGENTS.md
- docs/02_experiment_plan.md
- docs/06_eval_protocol.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/data_contracts/normalized_event_contract.md
- docs/data_contracts/distillation_output_contract.md
- docs/review/T111_review.md
- docs/tasks/M1_offline_distillation_mvp/T112_summary_fact_extraction.md

本轮只完成：
- docs/tasks/M1_offline_distillation_mvp/T112_summary_fact_extraction.md

规则：
1. 只改 Allowed files。
2. 只实现 chunk summary 与 fact extraction 的 LLM/JSON 校验管线，先支持 limit/sample。
3. 输出只能写入 `private/distilled/<run_id>/chunk_summaries.jsonl`、`memory_facts.jsonl` 和 `run_report.json`。
4. LLM 输出必须校验为 T111 schema；缺失 evidence_refs/confidence/sensitivity/status 的输出视为无效。
5. Evidence refs 必须能回指 T110 chunk/event 范围。
6. 不保存 LLM 输入/输出原文到可提交目录，不把 private/distilled 内容复制到 docs/examples/tests。
7. 不做 ContactSkill builder、Markdown review exporter、数据库 migration、实时平台接入或自动发送。
8. 如果模型不可用，不要用 mock 假装完成；记录阻塞或降级验证结果。
9. 最后报告：改了什么、如何验证、人工抽查至少 3 条 facts 的结果、剩余风险。
```

## 10. Reviewer 启动提示

```text
你是 Claude Code reviewer。

请先阅读：
- docs/02_experiment_plan.md
- docs/04_task_board.md
- docs/07_handoff.md

只读审查本次 diff，不要修改文件。

重点检查：
1. T112 是否只实现 summary/fact extraction 管线，不越界做 ContactSkill builder 或 store。
2. LLM 输出是否必须校验为 T111 schema。
3. 无 evidence_refs/confidence/sensitivity/status 的输出是否会被拒绝。
4. evidence refs 是否能回指 T110 chunk/event 范围。
5. 是否有真实聊天原文、LLM 输入原文或 LLM 原始输出进入 docs/examples/tests/stdout。
6. 是否越界写数据库 migration、实时平台接入或自动发送。
7. 若模型不可用，worker 是否明确记录而不是用 mock 冒充真实完成。

输出 Verdict: PASS / PASS_WITH_WARNINGS / BLOCK，并写入 docs/review/T112_review.md。
```

## 11. 下一步顺序

1. 可提交当前 T111 + Captain 收口文档变更。
2. 下一轮 worker 只执行 T112，不要自领 T113。
3. 若 T112 review `BLOCK`，worker 只修 blocking issue，并最多自动复审一次。
4. 若 T112 review `PASS` 或 `PASS_WITH_WARNINGS`，Captain 再更新 `04_task_board`、`05_decision_log`、`07_handoff`、`08_risks_and_open_questions`。
5. T113 只有在 T112 review 通过后才能启动。

## 12. 历史顺序

1. T100 review `PASS`，已完成 schema profile 与 normalized event contract。
2. T101 review `PASS`，已完成 privacy/source_ref rules。
3. T102 review `PASS`，已完成 `chatlog-normalize` 最小 CLI。
4. T103 Gate M0 = `Conditional` accepted，允许进入 M1。
5. T110 review `PASS`，已完成 `chatlog-chunk` conversation chunker v0。
6. T111 review `PASS`，已完成 distillation output schemas 和 JSON contract。

## 13. 注意事项

- `.gitignore` 中已有 `private/`，保留这个安全措施。
- 不要还原用户手动迁移 docs 目录结构的操作。
- 不要读取或输出 `.env`。
- 不要把 `private/chat_history` 的真实文件名或聊天内容写入 docs。
- 当前阶段不做微调、不做自动发送、不做微信扫描。
- M1 可以推进，但必须带着 T103 的 Conditional 条件继续验证，不要把 conditional 误写成无条件完成。
