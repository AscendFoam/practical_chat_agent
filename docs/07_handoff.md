# Handoff

更新日期：2026-05-16

## Captain Current State 2026-05-16

- T133 review decision: `PASS_WITH_WARNINGS`.
- T133 warning disposition: N01/N02/N03/N04/N05 all accepted; no deferred or rejected warnings.
- Gate M3: `Conditional`, documented in `docs/review/M3_review.md`.
- Current Unique Task: T140 Feedback Schema CLI.
- Current task package: `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`.
- M4/T140 may proceed only under review-only constraints: no auto-send, no realtime platform integration, no LLM drafting expansion, no automatic ContactSkill/Memory mutation, and no relationship-aware maturity claim.
- T150 must add committed regression tests covering ReplyPlanner structure, boundary sensitivity, thin context, false positives, subtle false negatives, privacy leakage, contact alignment, and ranking.

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
- Captain 已将 T100/T101/T102/T103/T110/T111/T112/T113/T114/T120/T121/T122/T123/T130/T131/T132 标记完成，Gate M1 = `Conditional`，Current Unique Task 推进到 T133。
- T101 worker 已产出隐私脱敏规则、source_ref 规则和补充了 `source_ref/raw_ref` 预览形态的合成 fixture，并通过 reviewer `PASS`。
- T102 worker 已产出最小 normalize CLI，并完成 dry-run 与 limit 小样本验证，reviewer 判定 `PASS`。
- T103 milestone review 已接受 Gate M0 = `Conditional`，允许进入 M1；T110 conversation chunker v0、T111 distillation schemas 和 T112 summary/fact extraction 均已通过 reviewer `PASS`，T113 ContactSkill builder 已通过 reviewer `PASS_WITH_WARNINGS`，T114 确认 Gate M1 = `Conditional`。
- T120 file store models 已通过 reviewer `PASS_WITH_WARNINGS`，允许进入 T121。
- T121 evidence validator 已通过 reviewer `PASS_WITH_WARNINGS`，允许进入 T122。
- T122 skill review CLI 已通过 reviewer `PASS_WITH_WARNINGS`，允许进入 T123。
- T123 context integration 已通过 reviewer `PASS_WITH_WARNINGS`，T130 ReplyPlan schema 已通过 reviewer `PASS_WITH_WARNINGS`，T131 ReplyPlanner 已通过 reviewer `PASS_WITH_WARNINGS`，T132 Reply Policy 已通过 reviewer `PASS_WITH_WARNINGS`，允许进入 T133。

## 2. 当前唯一任务

T133: 用历史 holdout 场景评估回复自然度和边界遵守。

任务包：`docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`

状态：T132 已通过 `PASS_WITH_WARNINGS`，ReplyPlanner 已具备 review-only contract wiring 和 policy/boundary 风险层。T133 只做匿名 holdout eval 与 Gate M3 判断；不修改 planner 代码，不提交 holdout 原文，不自动发送、不接数据库、不引入向量数据库、不回读或泄露原始聊天记录。

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

## 12. T120 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/contact_skill.py`
  - `docs/07_handoff.md`
- 已实现内容：
  - 在 `core.models` 中新增 T120 file-store 相关模型：
    - `ContactSkillRedactionPolicy`
    - `DistilledArtifactReviewDecision`
    - `DistilledArtifactReviewMetadata`
    - `DistilledArtifactSourceMetadata`
    - `MemoryFactStoreRecord`
    - `MemoryFactStoreFile`
    - `ContactSkillStoreRecord`
    - `ContactSkillStoreFile`
  - 为 `MemoryFactCandidate` 增加显式映射 helper：
    - `to_runtime_memory_type()`
    - `to_memory_fact(...)`
    - 仅提供后续 T123/T121 可复用映射，不在本轮做 runtime 注入。
  - 将 `ContactSkillCandidate.redaction_policy` 从宽松 `dict[str, Any]` 收紧为结构化 `ContactSkillRedactionPolicy`。
  - 在 `contact_skill.py` 中新增 `ContactSkillFileStoreService`，支持：
    - 从 legacy `memory_facts.jsonl` 包装并加载 `MemoryFactStoreFile`
    - 从 legacy `contact_skill.candidate.json` 包装并加载 `ContactSkillStoreFile`
    - 保存 `memory_fact_store.json` / `contact_skill_store.json`
    - 保留 `status`、`evidence_refs`、`source_run_id`、source artifact path、source chunk/memory/event ids、review metadata
  - `review_metadata.is_runtime_ready(...)` / record-level `is_runtime_ready()` 只在 `status="approved"` 且 `reviewed_by_human=True` 时返回 true，保持 candidate-only / human-review-first 语义。
  - 未新增 CLI、未改数据库、未引入向量库、未做 runtime prompt 注入、未自动 approve。
- 已完成验证：
  - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/core/models.py src/practical_chat_agent/services/contact_skill.py`
  - 使用合成脱敏样例运行最小 load/save 闭环验证（未读取真实聊天原文）：
    - 生成 legacy fixture 于 `private/distilled/t120_store_smoke/legacy/`
    - 用 `ContactSkillFileStoreService` 加载 legacy `memory_facts.jsonl` / `contact_skill.candidate.json`
    - 写出 store 文件到 `private/distilled/t120_store_smoke/store/memory_fact_store.json`
    - 写出 store 文件到 `private/distilled/t120_store_smoke/store/contact_skill_store.json`
    - 再次回读并断言：
      - memory statuses = `candidate`, `approved`
      - skill statuses = `approved`
      - `evidence_refs` 未丢失
      - `source_memory_ids` / source event ids / source chunk ids 保留
      - approved record 的 `review_metadata.reviewed_by_human`、`last_decision`、history 保留
      - `is_runtime_ready()` 仅对 synthetic approved records 返回 true
- Reviewer 结论：
  - `docs/review/T120_review.md` verdict 为 `PASS_WITH_WARNINGS`。
  - 确认 T120 只实现 file store models 和 service，不做 CLI、DB migration、vector DB、runtime prompt injection 或 auto-approve。
  - 确认 `is_runtime_ready()` 需要 `status="approved"`、`reviewed_by_human=True`、`last_decision="approved"` 三重条件，保持 candidate-only / human-review-first。
  - 确认 legacy T112/T113 artifacts 可包装为 store records，且 evidence refs、source ids、review metadata 可 load/save round-trip 保留。
- Warning 处理：
  - N01 accepted：`updated_at` no-op normalization 低影响，不要求返修；T122 更新 review 状态时再明确 timestamp 语义。
  - N02 accepted：`ContactSkillBuilderService` 与 `ContactSkillFileStoreService` 的 path/helper duplication 对 MVP 可接受，暂不抽共享基类。
  - N03 accepted：single-record store shape 兼容入口便利迁移，Pydantic downstream validation 足够兜底。
  - N04 accepted：`DistillationMemoryType` 到 runtime `MemoryType` 的粗粒度映射符合 MVP granularity。
  - N05 deferred：自动化测试留给 T150，新增 R031 跟踪 store model validation、legacy wrapping、load/save round-trip、runtime-ready gate 和 path confinement 测试。
- 当前注意点：
  - 真实 approve / reject / freeze CLI 仍留给 T122。
  - evidence existence/support 校验由 T121 承接，missing refs 必须阻止 approval。

## 13. T121 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/evidence_validation.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- 已实现内容：
  - 新增 `EvidenceValidationService`，通过 T120 `ContactSkillFileStoreService` 加载 memory/contact-skill store records。
  - 从 same-run artifacts 建立 evidence id index：
    - `normalized_events.jsonl`
    - `chunks.jsonl`
    - `chunk_summaries.jsonl`
    - `memory_facts.jsonl`
    - `contact_skill.candidate.json`
    - T120 store records 自身
  - 递归扫描 serialized model payload 中所有 nested `evidence_refs`。
  - 输出每个 record 的 checked refs、missing refs、nested ref locations、provenance snapshot、review metadata snapshot、approval/runtime block reasons。
  - 状态规则：
    - `candidate` 默认 blocked from approval/runtime。
    - `approved` 若存在 missing refs，则 blocked from approval/runtime。
    - `rejected` / `frozen` / `archived` 不可 runtime-ready。
    - `approved` 且 refs OK 但未 human-reviewed，只能 approval-ready，不能 runtime-ready。
  - 新增 `chatlog-validate-evidence` CLI，支持 `--input`、`--output`、`--dry-run`。
  - Validator 只报告，不写回 store metadata，不自动 approve，不做 runtime integration。
- 已完成验证：
  - Compile passed：
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src\practical_chat_agent\services\evidence_validation.py src\practical_chat_agent\app\main.py`
  - Good case：`private/distilled/t102_smoke` dry-run。
    - `evidence_validation_status = passed`
    - `validated_record_count = 8`
    - `records_with_missing_refs = 0`
    - `missing_ref_count = 0`
    - `approval_blocked_records = 8`
    - `runtime_blocked_records = 8`
    - 解释：refs 全部存在，records 因仍为 candidate 被正确阻止。
  - Bad case：`private/distilled/t121_missing_ref_fixture/` synthetic fixture。
    - `evidence_validation_status = failed`
    - `validated_record_count = 3`
    - `records_with_missing_refs = 1`
    - `missing_ref_count = 1`
    - approved memory record 因 missing `evt_demo_2` 同时 blocked from approval/runtime。
  - Store-only case：`private/distilled/t120_store_smoke/store` dry-run。
    - `evidence_validation_status = failed`
    - `records_with_missing_refs = 3`
    - `missing_ref_count = 5`
    - 解释：store-only fixture without same-run evidence artifacts 被正确判定 evidence-incomplete。
- Reviewer 结论：
  - `docs/review/T121_review.md` verdict 为 `PASS_WITH_WARNINGS`。
  - 确认 T121 只实现 read-only evidence validator 与 CLI，不做 auto-approve、approve/reject/freeze CLI、DB migration、vector DB、runtime prompt injection、LLM call 或 `private/chat_history` 读取。
  - 确认 stdout/report 限制在 counts、safe relative paths 和 private `private/distilled/` report，未发现私密内容进入 docs/examples/tests/stdout。
- Warning 处理：
  - N01 accepted：当前 `ContactSkillCandidate` 没有 stable skill artifact id，`_extract_contact_skill_ids` 对现有 schema 为空；fallback 到 `contact_id` 不影响正确性。
  - N02 accepted/deferred：JSON/JSONL helper 已是第三份重复，MVP 可接受；T150 或后续 refactor 可统一 file IO 并回收 BOM handling。
  - N03 accepted：全 payload 递归找 `evidence_refs` 是 O(total dict nodes)，当前数据量无性能风险。
  - N04 accepted：validator read-only、不写回 `review_metadata.evidence_validation_status` 是正确设计；T122 决定是否根据 report 写入 review metadata。
  - N05 deferred：自动化测试留给 T150，新增 R032 跟踪 evidence index、nested refs、status rules、missing refs blocking、human review gate interaction 和 path confinement 测试。
- 当前注意点：
  - T122 approve 必须读取或要求通过 T121 evidence validation report。
  - T122 不得在 missing refs、未 human review 或 rejected/frozen/archived 状态下绕过 gate。

## 14. T122 完成记录

- 代码 / 文档改动：
  - `src/practical_chat_agent/services/contact_skill.py`
  - `src/practical_chat_agent/exporters/contact_skill_markdown.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- 已实现内容：
  - 新增 `ContactSkillStoreReviewService`，支持 list/apply decision/export review artifact。
  - 新增 `chatlog-review-store` CLI with actions:
  - `list`
  - `approve`
  - `reject`
  - `freeze`
  - `archive`
  - `export`
  - T122 scope kept to private file-store review only:
    - no runtime integration
    - no DB migration
    - no vector DB
    - no LLM call
    - no auto-send
  - Review flow implemented:
    - input/output confined to `private/distilled/**`
    - safe record listing with record id, artifact type/id, status, review state, evidence validation status, approval/runtime-ready summary, and safe relative path
    - `approve` requires T121 `evidence_validation_report.json`
    - `approve` blocks on report status != `passed`
    - `approve` blocks on target-record missing refs
    - `approve` blocks for current status in `rejected` / `frozen` / `archived`
    - `reject` / `freeze` / `archive` update payload status plus review metadata/history and keep runtime-ready false
    - decision metadata writes reviewer id/name, reviewed timestamp, notes, and evidence validation status into `review_metadata`
    - export writes markdown safe summaries only under `private/distilled/**`
  - legacy wrapped records now get deterministic stable `record_id` values derived from run id + artifact id, so T121 report lookup and T122 CLI targeting stay stable across reloads.
  - store save preserves store-level `generated_at`.
- Private fixtures / safe samples used:
  - safe sample: `private/distilled/t102_smoke`
  - missing-ref sample: `private/distilled/t121_missing_ref_fixture`
  - T122 private verification fixtures:
    - `private/distilled/t122_pass_fixture`
    - `private/distilled/t122_reject_fixture`
    - `private/distilled/t122_freeze_fixture`

- 已完成验证：
  - compile:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src\practical_chat_agent\app\main.py src\practical_chat_agent\services\contact_skill.py src\practical_chat_agent\exporters\contact_skill_markdown.py`
    - result: passed
  - safe list:
    - `chatlog-review-store --input private/distilled/t120_store_smoke/store --action list`
    - result: stdout only contains safe ids, status fields, counts, and private-relative paths
  - passed validation fixture:
    - `chatlog-validate-evidence --input private/distilled/t122_pass_fixture`
    - result: `evidence_validation_status = passed`
  - approve happy path:
    - `chatlog-review-store --input private/distilled/t122_pass_fixture --action approve --record-id skillstore_bae8944df32d64b2 --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Approved after passed evidence validation.'`
    - result: wrote `private/distilled/t122_pass_fixture/contact_skill_store.json`
    - confirmed `status = approved`, `reviewed_by_human = true`, `last_decision = approved`, reviewer fields set, `last_reviewed_at` populated, `evidence_validation_status = passed`, decision appended to `history`, and `updated_at` advanced
  - reject path:
    - `chatlog-validate-evidence --input private/distilled/t122_reject_fixture`
    - `chatlog-review-store --input private/distilled/t122_reject_fixture --action reject --record-id skillstore_0edb3e3030c16049 --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Rejected for narrower human rewrite before approval.'`
    - result: wrote `private/distilled/t122_reject_fixture/contact_skill_store.json`
    - confirmed `status = rejected`, decision appended, runtime-ready summary remained false
  - freeze path:
    - `chatlog-validate-evidence --input private/distilled/t122_freeze_fixture`
    - `chatlog-review-store --input private/distilled/t122_freeze_fixture --action freeze --record-id skillstore_4e33506d02e1e966 --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Frozen pending broader sample review.'`
    - result: wrote `private/distilled/t122_freeze_fixture/contact_skill_store.json`
    - confirmed `status = frozen`, decision appended, runtime-ready summary remained false
  - missing-ref approve block:
    - `chatlog-review-store --input private/distilled/t121_missing_ref_fixture --action approve --record-id memstore_37bae56b191844de --reviewer-id worker_t122 --reviewer-name 'T122 Reviewer' --note 'Should be blocked by missing refs.'`
    - result: correctly blocked with `Approve is blocked because the target record still has missing evidence refs in the validation report.`
    - checked target fixture file stayed unchanged after the blocked command
  - export path:
    - `chatlog-review-store --input private/distilled/t122_pass_fixture --action export --output private/distilled/t122_pass_fixture/review_exports`
    - result: wrote `private/distilled/t122_pass_fixture/review_exports/store_review_export.md`
    - checked exported markdown contains safe review metadata only, not raw chat transcript output

- Reviewer 结论：
  - `docs/review/T122_review.md` verdict 为 `PASS_WITH_WARNINGS`。
  - 确认 T122 只实现 private file-store review CLI，不做 auto-approve、runtime integration、DB migration、vector DB、LLM、auto-send 或 `private/chat_history` 读取。
  - 确认 approve gate 完整：需要 T121 validation report、report `passed`、target record present、0 missing refs、checked refs > 0，并阻止 rejected/frozen/archived re-approval。
  - 确认 review metadata history、safe export、path confinement、stable record_id 和 no private data stdout 均满足任务包。
- Warning 处理：
  - N01 accepted：`del current_status` 是低影响接口/风格问题，不影响 correctness。
  - N02 accepted：递归更新所有合法 `status` 字段符合当前 schema；若未来 schema 出现不同语义的 status 字段再重审。
  - N03 accepted：`store_runtime_ready` 提前计算只是轻微 style note。
  - N04 accepted/deferred：review service 访问 file store private helpers 对 MVP 可接受；未来可抽 public file/path utility。
  - N05 accepted：mutable `_StoreWorkspace` 当前局部可控。
  - N06 deferred：自动化测试留给 T150，新增 R033 跟踪 approval gate、reject/freeze/archive、review history、recursive status update、export path confinement、stable record_id 和 no-auto-approve 测试。
- 当前注意点：
  - T123 必须只读取 approved + runtime-ready records。
  - T123 不得注入 candidate/rejected/frozen/archived，不得加载完整 skill 或全部 memory 到 prompt。
  - T122 intentionally does not implement reopen; rejected/frozen/archived records remain non-approvable in this scope.

## 15. Worker 启动提示

```text
你是 Codex worker。

请先阅读：
- README.md
- AGENTS.md
- docs/02_experiment_plan.md
- docs/06_eval_protocol.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/review/T123_review.md
- docs/review/T130_review.md
- docs/review/T131_review.md
- docs/review/T132_review.md
- docs/data_contracts/reply_plan_contract.md
- docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md

本轮只完成：
- docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md

规则：
1. 只改 Allowed files。
2. 只做匿名 holdout eval 和 Gate M3 判断，不修改 planner 代码。
3. 评估 T130-T132 输出的自然度、边界遵守、证据使用、risk flags 可解释性和隐私安全。
4. 可以读取 private/distilled 下的私有评估输出，但不得把 holdout 原文、真实联系人名、真实平台 ID 或可识别内容写入 docs。
5. 不自动发送，不接数据库，不引入向量数据库，不读取 `private/chat_history/`。
6. 不修复代码缺陷；若发现 blocking code issue，只在 review 中记录并给出 Gate M3 `Block` 或 `Conditional` 理由。
7. 输出 `docs/review/T133_milestone_review.md`，并更新 `docs/07_handoff.md`。
8. 最后报告：评估样本形态、匿名指标、Gate M3 verdict、剩余风险。
```

## 16. Reviewer 启动提示

```text
你是 Claude Code reviewer。

请先阅读：
- docs/02_experiment_plan.md
- docs/04_task_board.md
- docs/07_handoff.md
- docs/06_eval_protocol.md
- docs/review/T123_review.md
- docs/review/T130_review.md
- docs/review/T131_review.md
- docs/review/T132_review.md
- docs/data_contracts/reply_plan_contract.md
- docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md

只读审查本次 diff，不要修改文件。

重点检查：
1. T133 是否只做 read-only / docs-only 的 holdout eval，不修改 planner 代码。
2. 是否回答 Gate M3 关键问题：自然度、边界遵守、证据使用、risk flags 可解释性、隐私安全。
3. 是否没有 holdout 原文、真实联系人名、真实平台 ID 或可识别 private content 进入 docs/examples/tests/stdout。
4. 是否如实记录 T131/T132 deterministic templates、keyword false positives 和缺少 committed tests 的限制。
5. Gate M3 verdict 是否为 `Allow` / `Conditional` / `Block`，并给出可执行条件。
6. 若 verdict 允许进入下一阶段，是否明确禁止自动发送和实时平台接入继续越界。

输出 Verdict: PASS / PASS_WITH_WARNINGS / BLOCK，并审查 `docs/review/T133_milestone_review.md`。
```

## 17. 下一步顺序

1. 可提交当前 T132 worker/reviewer 代码与 Captain 收口文档变更。
2. 下一轮 worker 只执行 T133，不要自领 M4。
3. 若 T133 review `BLOCK`，worker 只修 blocking issue 或补充 blocking evaluation evidence，并最多自动复审一次。
4. 若 T133 review `PASS` 或 `PASS_WITH_WARNINGS`，Captain 再更新治理文档并决定 Gate M3 是否允许进入 M4。
5. M3 仍保持 review-only；不要实现自动发送或实时平台接入。

## 18. 历史顺序

1. T100 review `PASS`，已完成 schema profile 与 normalized event contract。
2. T101 review `PASS`，已完成 privacy/source_ref rules。
3. T102 review `PASS`，已完成 `chatlog-normalize` 最小 CLI。
4. T103 Gate M0 = `Conditional` accepted，允许进入 M1。
5. T110 review `PASS`，已完成 `chatlog-chunk` conversation chunker v0。
6. T111 review `PASS`，已完成 distillation output schemas 和 JSON contract。
7. T112 review `PASS`，已完成小样本 summary/fact extraction 与 evidence refs 校验管线。
8. T113 review `PASS_WITH_WARNINGS`，已完成 ContactSkill candidate builder 和 Markdown review exporter。
9. T114 review `PASS_WITH_WARNINGS`，Gate M1 = `Conditional`，M2 可条件启动。
10. T120 review `PASS_WITH_WARNINGS`，已完成 file store models 与 human-review-first gate。
11. T121 review `PASS_WITH_WARNINGS`，已完成 evidence validator 与 missing-ref/status gate。
12. T122 review `PASS_WITH_WARNINGS`，已完成 skill review CLI 与 approval gate。
13. T123 review `PASS_WITH_WARNINGS`，已完成 approved-store compact `ChatContext` integration。
14. T130 review `PASS_WITH_WARNINGS`，已完成 ReplyPlan schema 与 prompt contract。
15. T131 review `PASS_WITH_WARNINGS`，已完成 review-only ReplyPlanner 与 `chat-reply-plan` CLI；T132 进入 policy/boundary validation。
16. T132 review `PASS_WITH_WARNINGS`，已完成 ReplyPlanner policy/boundary 风险层；T133 进入匿名 holdout eval。

## 19. 注意事项

- `.gitignore` 中已有 `private/`，保留这个安全措施。
- 不要还原用户手动迁移 docs 目录结构的操作。
- 不要读取或输出 `.env`。
- 不要把 `private/chat_history` 的真实文件名或聊天内容写入 docs。
- 当前阶段不做微调、不做自动发送、不做微信扫描。
- M2 可以推进，但必须带着 Gate M1 Conditional 条件继续验证，不要把 M1 写成无条件完成。

## 20. T123 Completion Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/chat_context.py`
  - `src/practical_chat_agent/app/container.py`
  - `docs/07_handoff.md`
- Implemented:
  - Added `approved_store_context` to `ChatContext`.
  - Added compact store brief models: `ApprovedStoreContext`, `ApprovedContactSkillBrief`, and `ApprovedMemoryFactBrief`.
  - Extended `ChatContextAssembler` with optional approved-store loading from `private/distilled/**`.
  - Context assembly now adds compact approved-store hints into `summary` and `memory_retrieval_notes`.
  - Filtering is conservative: only records that are approved, human-reviewed, evidence-valid, and `is_runtime_ready() == True` can enter runtime context.
  - Candidate, rejected, frozen, archived, missing-evidence, and not-human-reviewed records are excluded.
  - The brief stays compact: short relationship summary, short strategy / boundary reminders, record ids, and evidence refs only. No raw transcript, no full JSON dump, no runtime prompt injection.
  - `AppContainer` now supports optional injection through `PRACTICAL_CHAT_APPROVED_STORE_PATH` and `PRACTICAL_CHAT_APPROVED_MEMORY_LIMIT`.
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/chat_context.py src/practical_chat_agent/core/models.py src/practical_chat_agent/app/container.py`
  - Approved fixture:
    - fixture: `private/distilled/t123_approved_fixture`
    - result: `approved_store_context.status = loaded`
    - loaded one approved contact-skill brief with safe record id / evidence refs, and summary / retrieval notes included compact approved-store hints
  - Exclusion fixture:
    - fixture: `private/distilled/t123_exclusion_fixture`
    - result: `approved_store_context.status = no_runtime_ready_records`
    - rejected store record did not enter context
  - Compatibility fixture:
    - fixture: `private/distilled/t123_memory_only_fixture`
    - result: approved contact-skill brief loaded correctly; approved memory record with missing refs stayed excluded
  - No-store compatibility:
    - direct `ChatContextAssembler()` run with no store path
    - result: `approved_store_context.status = not_configured`, and existing context assembly behavior stayed unchanged
- Remaining risk / assumption:
  - Current private fixtures verify the positive contact-skill path and the exclusion path. They do not yet provide a runtime-ready approved memory-only sample, so the positive memory-brief branch remains unobserved and should be re-checked when such a safe fixture exists.

## 21. T130 Completion Record

- Files changed:
  - `src/practical_chat_agent/core/models.py`
  - `docs/data_contracts/reply_plan_contract.md`
  - `docs/07_handoff.md`
- Implemented:
  - Added strongly typed reply-planning models:
    - `ReplyPlanContextRef`
    - `ReplyPlanSourceContext`
    - `ReplyPlanCandidate`
    - `ReplyPlan`
  - Added `ReplyPlanMode = "candidate_review_only"` to make the review-only usage explicit.
  - Added `ReplyPlanContextRefType` so candidates can cite:
    - approved contact-skill record ids
    - approved memory-fact record ids
    - approved store evidence refs
    - recent event ids
    - runtime memory hit ids
    - policy-boundary refs
  - `ReplyPlan` requires:
    - `contact_id`
    - `source_context`
    - `policy_boundary_summary`
    - `notes_on_candidate_differences`
    - at least 3 `candidates`
  - Each `ReplyPlanCandidate` requires:
    - `draft_text`
    - `rationale`
    - at least 1 `supporting_context_ref`
    - at least 1 `boundary_reminder`
    - optional `risk_flags` and `confidence`
  - Added `docs/data_contracts/reply_plan_contract.md` to document:
    - review-only usage boundary
    - anti-impersonation rule
    - conservative handling for uncertain/sensitive cases
    - compatibility with T123 `approved_store_context`
    - JSON shape and field semantics for T131/T132
- How T130 ties back to T123:
  - `ReplyPlanSourceContext.approved_store_status` directly reuses T123 `ApprovedStoreContextStatus`.
  - `ReplyPlanSourceContext` accepts T123 compact ids and refs:
    - `approved_contact_skill_record_id`
    - `approved_memory_record_ids`
    - `approved_store_evidence_refs`
  - The contract therefore consumes the compact approved-store brief from `ChatContext` instead of requiring full store JSON or raw transcript text.
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/core/models.py`
  - Synthetic model validation passed with a safe inline sample:
    - validated one `ReplyPlan` containing 3 candidates
    - confirmed candidates can cite T123-style approved-store record ids / evidence refs
    - confirmed raw transcript text is not required by the schema
    - confirmed `approved_store_status="loaded"` is compatible with T123 context status values
- Remaining risk / assumption:
  - T130 defines the contract only. It does not yet prove that T131 generation logic will consistently populate distinct, high-quality candidates from real runtime context.
  - T123 reviewer warning about contact-id alignment still applies: T131 should verify that runtime `contact_id` routing stays aligned with approved-store records when the planner is wired in.

- Review decision:
  - `docs/review/T130_review.md` verdict = `PASS_WITH_WARNINGS`.
  - Warning handling:
    - N01 accepted: single-value `ReplyPlanMode` is correct for current review-only scope.
    - N02 deferred to R034: T131 must enforce stable unique `priority_rank` values.
    - N03 accepted: free-form `approach_label` is acceptable for MVP.
    - N04 deferred to R034: T131 must verify `contact_id` alignment during assembly.
  - Captain decision: T130 is complete; T131 is the next Current Unique Task.

## 22. T131 Kickoff Notes

- Task package:
  - `docs/tasks/M3_relationship_reply_planner/T131_reply_planner.md`
- Worker focus:
  - Implement a review-only ReplyPlanner service or CLI.
  - Consume only compact approved-store context from T123.
  - Output T130 `ReplyPlan` with at least 3 candidates.
  - Preserve safety: no raw transcript, no send logic, no DB, no vector DB.
- Reviewer focus:
  - Candidate distinctness.
  - Cited refs and boundary reminders.
  - Unique ranking and contact/source alignment.
  - No scope creep into automatic sending or platform integration.

## 23. T131 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/reply_planner.py`
  - `src/practical_chat_agent/app/main.py`
  - `docs/07_handoff.md`
- Implemented:
  - Added `ReplyPlanner` service with a review-only `generate(context=...) -> ReplyPlan` flow.
  - The planner consumes only `ChatContext` plus T123 compact `approved_store_context` fields already present at runtime.
  - Added hard checks for the two T130 warning items:
    - `ReplyPlan.contact_id` must match `ChatContext.user_id`.
    - `ApprovedStoreContext.contact_id` and approved contact-skill `contact_id` must align with the routed contact id.
    - `priority_rank` values must be unique and form a stable `1..N` sequence.
  - Added a safe `chat-reply-plan` CLI command that:
    - reads a redacted or synthetic `ChatContext` JSON file
    - generates a `ReplyPlan`
    - prints only the plan JSON or writes it to an output file
    - does not print the raw input context
  - Candidate generation stays offline and review-only:
    - exactly 3 distinct candidate shapes are generated
    - each candidate includes draft text, rationale, supporting refs, risk flags, boundary reminders, and confidence
    - refs are limited to approved compact ids, evidence refs, recent event ids, runtime memory ids, and policy-boundary ids
  - The planner ignores `source_record_ids` lists, so non-approved ids such as candidate/rejected/frozen/archived record ids do not leak into the plan surface.
  - `source_context.chat_context_summary` is rebuilt as a safe count/status summary instead of copying `ChatContext.summary`, so raw message text is not echoed back into the plan.
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/app/main.py`
  - Safe synthetic context validation passed with an inline fixture:
    - contact id: `contact_lin`
    - approved contact-skill record id: `approved_skill_001`
    - approved memory record id: `approved_mem_001`
    - recent event id: `evt_recent_1`
    - runtime memory hit id: `mem_runtime_1`
    - extra non-approved ids were injected into `source_record_ids` only as a negative check
  - Validation results:
    - service emitted 3 candidates
    - CLI emitted 3 candidates through `chat-reply-plan --input <tempfile>`
    - candidate refs stayed within approved-store ids, evidence refs, recent event ids, runtime memory ids, and policy-boundary ids
    - injected `candidate_record_999` / `rejected_record_888` ids did not appear in the output plan
    - raw synthetic inbound text did not appear in the output plan JSON
    - contact-id mismatch raised `ReplyPlannerError` as expected
- Remaining risk / assumption:
  - T131 is heuristic and deterministic; it proves the safe planning surface and contract wiring, but not yet the final quality ceiling of relationship-aware wording.
  - The current verification used a synthetic safe context, not a larger runtime sample set, so candidate quality across more relationship types still needs review in T132 or manual evaluation.

## 24. T131 Review Decision

- Review file: `docs/review/T131_review.md`
- Verdict: `PASS_WITH_WARNINGS`
- Captain decision:
  - T131 is complete within task scope.
  - M3 is not complete yet; do not enter M4.
  - Current Unique Task moves to T132 Reply Policy.
- Warning handling:
  - N01 accepted/deferred: hardcoded templates and shallow relationship-awareness are acknowledged; deferred to R035 and T132/T133.
  - N02 accepted: hardcoded confidence values are acceptable for contract-wiring MVP.
  - N03 accepted/deferred: unused `strategy_hints` and `relationship_summary` are acknowledged; deferred to R035 and T132/T133.
  - N04 deferred: no committed tests/fixtures; deferred to R036 and T150.
  - N05 accepted: `_dedupe(values)` missing type annotation is low-risk style debt.
  - N06 accepted: enum fallback is sufficient for current MVP.

## 25. T132 Kickoff Notes

- Task package:
  - `docs/tasks/M3_relationship_reply_planner/T132_reply_policy.md`
- Worker focus:
  - Add boundary / avoid-topic / over-proactivity / impersonation risk checks to the existing T131 planner path.
  - Preserve review-only output and T130 `ReplyPlan` contract.
  - Keep the existing T131 contact alignment and ranking validation.
  - Use safe synthetic or redacted fixtures only.
- Reviewer focus:
  - Confirm no auto-send, DB, vector DB, realtime integration, raw transcript read, or full store JSON injection.
  - Confirm sensitive or boundary scenarios produce conservative candidates and explicit risk flags.
  - Confirm T132 does not claim final relationship-quality completion.

## 26. T132 Implementation Record

- Files changed:
  - `src/practical_chat_agent/services/reply_planner.py`
  - `src/practical_chat_agent/services/policy.py`
  - `docs/07_handoff.md`
- Implemented:
  - Added a reply-planning policy layer in `policy.py`:
    - `ReplyPlanPolicyProfile`
    - `ReplyCandidatePolicyAssessment`
    - `ReplyPlanPolicyEngine`
  - The new policy engine evaluates compact runtime context and candidate drafts for:
    - `boundary_sensitive`
    - `over_proactive`
    - `impersonation_risk`
    - `thin_context`
  - `ReplyPlanner` now builds a context-level policy profile before composing the plan, then applies candidate-level policy review when assembling each `ReplyPlanCandidate`.
  - Sensitive or boundary-heavy context now changes planner behavior in two ways:
    - policy-level summaries and boundary reminders become more explicit
    - draft templates switch to a more conservative, no-pressure wording set instead of the baseline T131 wording
  - Thin-context handling is now explicit through the policy layer rather than only through a generic boundary string:
    - candidate `risk_flags` carry `thin_context`
    - `policy_boundary_summary` explains that relationship-specific assumptions should be avoided
    - candidate confidence is reduced conservatively
  - Over-proactivity is now candidate-specific:
    - optional follow-up or next-step language is only escalated into `over_proactive` when the context is thin or boundary-sensitive
    - clearly no-pressure wording such as “先不往前推 / 不用现在展开” is exempted from false-positive `over_proactive` flags
  - Impersonation risk is now explicitly detectable at the candidate-text level, even though the current T131/T132 templates do not intentionally generate such text.
  - T131 checks remain intact:
    - `contact_id` alignment still enforced
    - `priority_rank` uniqueness and stable `1..N` ordering still enforced
    - output remains review-only `ReplyPlan`, not send logic
- Verification:
  - Compile passed:
    - `& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/services/policy.py src/practical_chat_agent/app/main.py`
  - Safe synthetic verification passed with three inline contexts:
    - baseline context:
      - approved contact-skill present
      - 3 candidates emitted
      - no raw input text echoed
      - no accidental `boundary_sensitive` / `over_proactive` over-blocking
    - boundary / avoid-topic context:
      - approved contact-skill carried explicit “give space / do not push” style reminders
      - 3 candidates emitted
      - at least one candidate carried `boundary_sensitive`
      - at least one candidate carried `over_proactive`
      - boundary reminders included explicit caution language
      - wording shifted to more conservative no-pressure drafts
    - thin-context context:
      - `approved_store_status = not_configured`
      - 3 candidates emitted
      - all candidates carried `thin_context`
      - boundary reminders explicitly warned against over-claiming familiarity
      - confidence stayed below the safe baseline and wording shifted to the conservative template set
  - Privacy / safety checks from the synthetic verification:
    - raw synthetic inbound text did not appear in the emitted `ReplyPlan`
    - output remained limited to compact ids, evidence refs, runtime ids, policy summaries, and candidate text
    - no `private/chat_history/` reads, no DB/persistence expansion, no vector DB, no send automation
- Remaining risk / assumption:
  - T132 improves safety behavior, but it is still heuristic keyword-based policy logic rather than evidence-weighted semantic classification.
  - The current policy layer does not yet use committed automated tests or committed synthetic fixtures; that regression coverage remains deferred to T150.
  - Relationship-aware wording quality is still limited by T131/T132 deterministic templates; T133 holdout evaluation is still needed before claiming strong reply quality.

## 27. T132 Review Decision

- Review file: `docs/review/T132_review.md`
- Verdict: `PASS_WITH_WARNINGS`
- Captain decision:
  - T132 is complete within task scope.
  - M3 is not complete yet; do not enter M4.
  - Current Unique Task moves to T133 Holdout Eval.
- Warning handling:
  - N01 accepted: runtime text is consumed for keyword detection only and is not echoed.
  - N02 accepted: broad keyword risk is mitigated by compound trigger logic.
  - N03 accepted/deferred: substring false-positive risk is acknowledged; deferred to R037 and T133/T150.
  - N04 accepted: `_dedupe` duplication is low-risk refactor debt.
  - N05 deferred: no committed tests/fixtures; folded into R036 and T150.
  - N06 accepted: duplicate terminal branch has no correctness impact.
  - N07 accepted: approved memory claim text is bounded and used for detection only.

## 28. T133 Kickoff Notes

- Task package:
  - `docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`
- Worker focus:
  - Run an anonymized holdout evaluation of T130-T132 ReplyPlanner behavior.
  - Assess naturalness, boundary adherence, evidence/reference usage, policy risk flags, and privacy safety.
  - Produce `docs/review/T133_milestone_review.md` with Gate M3 verdict: `Allow`, `Conditional`, or `Block`.
  - Update `docs/07_handoff.md` with eval summary and remaining risks.
- Reviewer focus:
  - Confirm no private raw content or identifying details entered committed docs.
  - Confirm the eval did not modify planner code or advance M4.
  - Confirm Gate M3 verdict is supported by evidence rather than assertion.

## 29. T133 Eval Record

- Private eval artifacts produced under:
  - `private/distilled/t133_holdout_eval/contexts/*.context.json`
  - `private/distilled/t133_holdout_eval/plans/*.reply_plan.json`
  - `private/distilled/t133_holdout_eval/eval_summary.json`
- Eval coverage:
  - 6/6 synthetic anonymized scenarios produced valid 3-candidate ReplyPlans.
  - Baseline and work cases stayed low-pressure and review-only.
  - Sensitive and thin-context cases became more conservative, with explicit boundary flags.
  - False-positive probe showed the policy layer can still swing conservative on a normal-looking work prompt.
  - False-negative probe showed subtle pacing risk may still be under-detected when no explicit boundary cue is present.
- Gate M3 verdict:
  - `Conditional`
- Handoff note:
  - Keep T131/T132/T133 treated as review-only planning proof, not as final relationship-quality proof.
  - Next recommended action for Captain: review T133, carry the conditions into T150, and only then decide whether M4 can proceed.

## 30. T133 Review Decision

- Review file: `docs/review/T133_review.md`
- Verdict: `PASS_WITH_WARNINGS`
- Captain decision:
  - T133 is complete within task scope.
  - Gate M3 remains `Conditional`.
  - M4/T140 may proceed only under the conditions carried in `docs/review/M3_review.md`.
- Warning handling:
  - N01 accepted: self-reported ratings are acceptable for MVP milestone; T150 may add independent review.
  - N02 accepted: 6 synthetic scenarios are reasonable under task constraints.
  - N03 accepted: naturalness 3/5 is honestly reported; do not claim relationship-aware maturity.
  - N04 accepted: evidence usage 3/5 is honestly reported; structural wiring is correct.
  - N05 accepted: H01/H02 detail omission is minor because summary confirms all six scenarios produced valid plans.
  - No deferred warnings.
  - No rejected warnings.

## 31. M3 Review Decision

- Review file: `docs/review/M3_review.md`
- Verdict: `Conditional`
- Completion judgment:
  - M3 is structurally complete: T130 schema, T131 planner, T132 policy layer, and T133 holdout eval are all present.
  - M3 is not quality-mature: drafts remain deterministic/template-driven, naturalness is 3/5, and evidence usage is 3/5.
  - Clean-environment reproducibility is not fully proven because committed regression tests/fixtures are still missing.
- Conditions carried forward:
  - ReplyPlanner remains review-only; no auto-send, realtime platform integration, or LLM drafting expansion.
  - T150 must add committed regression tests for structure, boundary sensitivity, thin context, false positives, subtle false negatives, privacy leakage, contact alignment, and ranking.
  - Do not claim relationship-aware maturity until broader sample recalibration.

## 32. T140 Kickoff Notes

- Task package:
  - `docs/tasks/M4_feedback_loop/T140_feedback_schema_cli.md`
- Worker focus:
  - Define feedback log schema for accept/edit/reject/boundary feedback on `ReplyPlan` candidates.
  - Implement a minimal CLI that records feedback to a private log.
  - Validate candidate references against a supplied `ReplyPlan`.
  - Keep stdout safe and avoid printing full draft text, edited text, private notes, raw transcript, or private paths.
- Forbidden:
  - Do not auto-send.
  - Do not modify ContactSkill, MemoryFact, approved store records, or planner templates automatically.
  - Do not introduce DB/vector DB/realtime integration/LLM calls.
  - Do not read from `private/chat_history/`.
- Reviewer focus:
  - Confirm feedback is recorded but not applied.
  - Confirm all M3 conditional constraints remain intact.
  - Confirm invalid candidate references fail safely.
  - Confirm no private content enters committed docs.
