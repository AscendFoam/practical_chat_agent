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
- Captain 已将 T100/T101/T102/T103/T110/T111/T112/T113/T114 标记完成，Gate M1 = `Conditional`，Current Unique Task 推进到 T120。
- T101 worker 已产出隐私脱敏规则、source_ref 规则和补充了 `source_ref/raw_ref` 预览形态的合成 fixture，并通过 reviewer `PASS`。
- T102 worker 已产出最小 normalize CLI，并完成 dry-run 与 limit 小样本验证，reviewer 判定 `PASS`。
- T103 milestone review 已接受 Gate M0 = `Conditional`，允许进入 M1；T110 conversation chunker v0、T111 distillation schemas 和 T112 summary/fact extraction 均已通过 reviewer `PASS`，T113 ContactSkill builder 已通过 reviewer `PASS_WITH_WARNINGS`，T114 确认 Gate M1 = `Conditional`。

## 2. 当前唯一任务

T120: 新增离线 memory/skill Pydantic 模型和文件 store。

任务包：`docs/tasks/M2_memory_skill_store/T120_file_store_models.md`

状态：Gate M1 = `Conditional`，允许进入 M2，但不能把 M1 写成无条件成功。T120 只做 file store models，必须保留 status 与 evidence refs；不做 migration、不引入向量数据库、不把 candidate 直接接入 runtime。

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

## 9. T112 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/chatlog_distillation.py`
  - `src/practical_chat_agent/services/contact_skill.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- 已实现内容：
  - 新增 `ChatlogDistillationService`，消费 `private/distilled/**/chunks.jsonl` 与同目录 `normalized_events.jsonl`。
  - 新增 `chatlog-distill` CLI，支持 `--input`、`--output`、`--limit`、`--sample`、`--dry-run`。
  - LLM 请求复用 OpenAI-compatible `/chat/completions` 调用风格。
  - distillation 输出先做 provider 兼容归一化，再强制校验为 T111 `ChunkSummary` / `MemoryFactCandidate` schema。
  - evidence refs 必须落在对应 chunk 的 `chunk_id + event_ids` 范围内；越界 refs 会导致 chunk 被拒绝，不写入 accepted 输出。
  - 产物只写入 `private/distilled/<run_id>/chunk_summaries.jsonl`、`memory_facts.jsonl` 和合并后的 `run_report.json`；不保存 LLM prompt 或 raw response。
  - `contact_skill.py` 当前仅含轻量辅助函数，为 T113 聚合 refs 预留，不包含 ContactSkill builder、review exporter 或 store 逻辑。
- 已完成验证：
  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/chatlog_distillation.py src/practical_chat_agent/services/contact_skill.py src/practical_chat_agent/app/main.py`
  - `$env:PYTHONPATH='src'; & 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main chatlog-distill --input private/distilled/t102_smoke --limit 1`
  - 首次因沙箱网络限制返回 `remote_request_failed`，worker 没有用 mock 冒充成功；提权复跑后 provider 可达。
  - 加入 provider 输出兼容归一化后，小样本成功写出 `chunk_summaries.jsonl`、`memory_facts.jsonl`、`run_report.json`。
  - 当前小样本结果：1 个 selected chunk，1 个 successful chunk，写出 1 条 chunk summary、7 条 memory facts，`distillation.failure_reasons` 为空。
  - reviewer 确认人工抽查 3+ 条 fact 的 evidence_refs，均能回指当前 chunk 事件。
- Reviewer 结论：
  - `docs/review/T112_review.md` verdict 为 `PASS`。
  - 确认 LLM 输出经过 provider 兼容归一化、T111 schema 校验和 evidence refs 范围校验后才写入。
  - 确认 prompt/raw response 不写入文件，stdout/report 只含统计和状态码。
  - 确认产物只写入 `private/distilled/`，没有真实聊天原文进入 docs/examples/tests/stdout。
  - 确认未越界做 ContactSkill builder、store、数据库 migration、实时平台接入或自动发送。
- Non-blocking 处理：
  - N01 deferred：`chunk_id` fallback 是合法粗粒度 evidence，但会降低证据精度；T114 全量/更大样本抽查时关注仅有 chunk_id 的比例。
  - N02 deferred：provider shape drift 已由 R024 记录；T114/T150 继续验证。
  - N03 accepted/deferred：sensitivity 关键词兜底作为 MVP 可接受；T150 可补充测试或后续收紧。
  - N04 accepted/deferred：memory_type fallback 作为 MVP 可接受；T114/T150 观察误分类。
  - N05 accepted：`contact_skill.py` 轻量辅助不越界，T113 可扩展或重写。
  - N06 deferred：schema 校验、evidence refs、PII 脱敏、provider 归一化的自动化测试留给 T150。
  - N07 accepted/deferred：prompt 层 PII token 替换已部分满足 T102 N05；T150 privacy leakage smoke test 继续覆盖。

## 10. T113 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/contact_skill.py`
  - `src/practical_chat_agent/exporters/contact_skill_markdown.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- 已实现内容：
  - `ContactSkillBuilderService` 消费 T112 的 `chunk_summaries.jsonl` 和 `memory_facts.jsonl`，通过 Pydantic `model_validate` 读取上游产物。
  - 生成 `ContactSkillCandidate`，并强制 `status="candidate"` 与非空 `evidence_refs`。
  - 输出 `private/distilled/<run_id>/contact_skill.candidate.json` 与 `contact_skill.review.md`。
  - Markdown review exporter 展示 relationship state、communication style、topics、important events、stable preferences、emotional patterns、reply strategy、usage boundary、evidence refs 与 anti-impersonation reminder。
  - 新增 `chatlog-build-contact-skill` CLI，支持 `--input`、`--output`、`--contact-id`、`--dry-run`。
  - 输出限制在 `private/distilled/`；无自动 approve、无 DB migration、无 realtime 平台、无自动发送。
- 已完成验证：
  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/contact_skill.py src/practical_chat_agent/exporters/contact_skill_markdown.py src/practical_chat_agent/app/main.py`
  - `$env:PYTHONPATH='src'; & 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main chatlog-build-contact-skill --input private/distilled/t102_smoke`
  - 样本确认生成 `contact_skill.candidate.json` 与 `contact_skill.review.md`，candidate 状态仍为 `candidate`，review artifact 可读并带 evidence refs / usage boundary。
- Reviewer 结论：
  - `docs/review/T113_review.md` verdict 为 `PASS_WITH_WARNINGS`。
  - 确认未越界自动 approve、保存 raw chat text、生成“contact speaking”内容、写 DB migration、接 realtime platform 或 auto-send。
  - 确认 evidence chain、candidate 状态、anti-impersonation guardrails 和 review artifact 均满足 T113 任务目标。
- Warning 处理：
  - N01 accepted：`_build_report` 重复调用是低影响重复工作，不要求返修。
  - N02 deferred：启发式 tokens/topic/relationship 推断偏当前小样本，T114 需用更大或不同样本暴露泛化缺口，T120+ 可考虑 LLM-assisted inference。
  - N03 deferred：confidence / closeness / trust 公式化且非 evidence-weighted，T114 需人工检查是否显得过度精确，T120+ 重新设计。
  - N04 accepted：`exporters/` 缺少 `__init__.py` 当前不影响 Python 3 namespace package 导入。
  - N05 accepted：未使用 helper 无当前风险，可在 T114+ 移除或使用。

## 11. T114 / M1 完成记录

- 文档改动：
  - `docs/review/T114_milestone_review.md`
  - `docs/review/T114_review.md`
  - `docs/review/M1_review.md`
  - `docs/07_handoff.md`
  - `docs/08_risks_and_open_questions.md`
- Worker milestone sample:
  - sample run directory: `private/distilled/t102_smoke`
  - artifact chain present: `normalized_events.jsonl`、`chunks.jsonl`、`chunk_summaries.jsonl`、`memory_facts.jsonl`、`contact_skill.candidate.json`、`contact_skill.review.md`、`run_report.json`
  - sample summary: 12 normalized events, 1 chunk, 1 chunk summary, 7 memory facts, candidate ContactSkill.
  - worker audited 7/7 memory facts, exceeding the required 5 facts.
- Reviewer conclusion:
  - `docs/review/T114_review.md` verdict 为 `PASS_WITH_WARNINGS`。
  - Gate M1 verdict = `Conditional` confirmed.
  - Reviewer independently checked all 7 memory facts against normalized events.
  - All Gate M1 hard requirements passed.
- Captain milestone review:
  - `docs/review/M1_review.md` verdict = `Conditional`。
  - M2 may proceed only with candidate-only / human-review-first semantics.
- Warning / condition handling:
  - T114 N01/N02 accepted：minor semantic elevation/paraphrase in candidate-only facts, handled by human review and R030.
  - T114 N03 accepted：sample too small for generalization, represented by Gate M1 `Conditional`.
  - T114 N04 accepted：no report inconsistency found; no action.
  - R028/R029/R030 remain active into M2.

## 12. Worker 启动提示

```text
你是 Codex worker。

请先阅读：
- README.md
- AGENTS.md
- docs/02_experiment_plan.md
- docs/06_eval_protocol.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/review/T114_review.md
- docs/review/M1_review.md
- docs/tasks/M2_memory_skill_store/T120_file_store_models.md

本轮只完成：
- docs/tasks/M2_memory_skill_store/T120_file_store_models.md

规则：
1. 只改 Allowed files。
2. 新增离线 memory/skill Pydantic 模型和文件 store，先不强制接数据库。
3. 必须保留 `status`、`evidence_refs`、source ids 和 review metadata。
4. 支持 load/save candidate 和 approved skill/memory 文件。
5. 不做 database migration，不引入向量数据库，不做 runtime prompt 注入。
6. 不自动 approve，不绕过 human review。
7. 用脱敏 fixture 或安全样例运行最小 load/save 验证。
8. 最后报告：改了什么、如何验证、剩余风险。
```

## 13. Reviewer 启动提示

```text
你是 Claude Code reviewer。

请先阅读：
- docs/02_experiment_plan.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/06_eval_protocol.md
- docs/review/M1_review.md

只读审查本次 diff，不要修改文件。

重点检查：
1. T120 是否只实现 file store models，不做 migration、向量库或 runtime integration。
2. Candidate / approved / rejected / frozen / archived 状态是否保留。
3. Evidence refs、source ids、review metadata 是否不丢失。
4. 是否有真实聊天原文或 private output 进入 docs/examples/tests。
5. Load/save 验证是否真实运行。
6. 是否遵守 Gate M1 Conditional 的 candidate-only / human-review-first 条件。

输出 Verdict: PASS / PASS_WITH_WARNINGS / BLOCK，并写入 docs/review/T120_review.md。
```

## 14. 下一步顺序

1. 可提交当前 T114 + M1 review + Captain 收口文档变更。
2. 下一轮 worker 只执行 T120，不要自领 T121。
3. 若 T120 review `BLOCK`，worker 只修 blocking issue，并最多自动复审一次。
4. 若 T120 review `PASS` 或 `PASS_WITH_WARNINGS`，Captain 再更新治理文档并推进 T121。
5. M2 仍为 Conditional；不要把 candidate 产物直接接入 runtime。

## 15. 历史顺序

1. T100 review `PASS`，已完成 schema profile 与 normalized event contract。
2. T101 review `PASS`，已完成 privacy/source_ref rules。
3. T102 review `PASS`，已完成 `chatlog-normalize` 最小 CLI。
4. T103 Gate M0 = `Conditional` accepted，允许进入 M1。
5. T110 review `PASS`，已完成 `chatlog-chunk` conversation chunker v0。
6. T111 review `PASS`，已完成 distillation output schemas 和 JSON contract。
7. T112 review `PASS`，已完成小样本 summary/fact extraction 与 evidence refs 校验管线。
8. T113 review `PASS_WITH_WARNINGS`，已完成 ContactSkill candidate builder 和 Markdown review exporter。
9. T114 review `PASS_WITH_WARNINGS`，Gate M1 = `Conditional`，M2 可条件启动。

## 16. 注意事项

- `.gitignore` 中已有 `private/`，保留这个安全措施。
- 不要还原用户手动迁移 docs 目录结构的操作。
- 不要读取或输出 `.env`。
- 不要把 `private/chat_history` 的真实文件名或聊天内容写入 docs。
- 当前阶段不做微调、不做自动发送、不做微信扫描。
- M2 可以推进，但必须带着 Gate M1 Conditional 条件继续验证，不要把 M1 写成无条件完成。
