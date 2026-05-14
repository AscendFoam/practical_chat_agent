# Eval Protocol

更新日期：2026-05-14

## 1. 评价目标

新的评价目标是验证：WeFlow 导出的聊天记录能否被安全、稳定、可审计地蒸馏为长期关系感知 chat agent 所需的结构化资产。

评价重点：

- 数据是否能稳定解析。
- 隐私是否被保护。
- 事实和关系判断是否有 evidence refs。
- ContactSkill 是否有用但不冒充联系人。
- 回复 planner 是否能有分寸地使用记忆。

## 2. Milestone Gate

### Gate M0: WeFlow 数据合约

必须满足：

- 能读取 `private/chat_history` 的 JSONL 文件并输出字段统计。
- 不把真实聊天原文写入 docs。
- 明确 normalized event schema。
- 至少生成一个脱敏 fixture。
- 明确 source_ref、event_id、sender_role、timestamp、message_type 的规则。

结论：`Allow`、`Conditional` 或 `Block`。

当前状态：

- T100 已通过 reviewer `PASS`，满足 schema profile、normalized event contract 和脱敏 fixture 的第一步要求。
- T101 已通过 reviewer `PASS`，满足隐私脱敏规则、source_ref/raw_ref 规则和红线样例要求。
- T102 已通过 reviewer `PASS`，最小 normalize CLI 已落地，输出只进入 `private/distilled/`，并遵守 T101 的字段处理矩阵和公开引用形态。
- T103 已接受 Gate M0 = `Conditional`，允许进入 M1；M0 条件需由 T110/T112+/T114/T150 继续跟踪。
- T110 已通过 reviewer `PASS`，conversation chunker v0 已落地。
- T111 已通过 reviewer `PASS`，蒸馏输出 schema 与 JSON contract 已落地；M1 继续由 T112 实现 summary/fact extraction。

### Gate M1: 离线蒸馏 MVP

必须满足：

- 对一个联系人或小样本生成 chunks。
- chunk summaries 输出 JSON 且可追溯。
- memory facts 全部带 evidence refs。
- ContactSkill candidate 有 review Markdown。
- 人工抽查至少 5 条 fact，证据能命中原始事件。
- 无私密原文进入可提交目录。

### Gate M2: Memory / Skill Store

必须满足：

- evidence validator 能拦截不存在或不支持 claim 的 refs。
- ContactSkill 有 candidate/approved/rejected/frozen/archived 状态。
- rejected/frozen 不进入 prompt。
- 能导出 JSON 和 Markdown review artifact。

### Gate M3: Relationship Reply Planner

必须满足：

- 输出结构化 ReplyPlan。
- 至少 3 个候选草稿。
- 每个草稿有 rationale、引用的 skill/memory 和 risk flags。
- 不冒充联系人，不生成“对方会怎么说”的角色扮演。
- 对敏感/边界场景给出保守选项。

### Gate M4: Feedback Loop

必须满足：

- accept/edit/reject/boundary feedback 可记录。
- edit diff 能生成可审阅的 preference/boundary proposal。
- 支持 skill/memory version diff、rollback、freeze。

### Gate M5: Hardening

必须满足：

- parser/chunker/evidence validator 有自动化测试。
- privacy leakage smoke test 通过。
- 文档、任务板、handoff 与代码状态一致。

## 3. 指标

### 数据层指标

- JSONL 行解析成功率。
- timestamp 可解析率。
- sender_role/direction 判定率。
- contact_id/conversation_id 稳定率。
- message_type 覆盖率。
- 脱敏 fixture 泄漏次数，目标为 0。

### 蒸馏层指标

- chunk 边界人工可接受率。
- MemoryFact evidence 命中率。
- Claim 支持率：证据是否真的支持 claim。
- 幻觉率：无证据或证据不支持的 claim 比例。
- ContactSkill 字段完整率。
- 人工 review 修改量。

### 回复层指标

- 回复自然度。
- 边界遵守率。
- 过度主动/过度亲密次数。
- 引用记忆解释质量。
- 用户二次编辑距离。

## 4. 不合格判据

任一情况视为失败或暂停：

- 私密聊天原文进入 `docs/`、`examples/`、`tests/` 或 git 可提交区域。
- LLM 输出没有 evidence refs。
- ContactSkill 出现无证据人格判断。
- 系统试图冒充联系人。
- 早期阶段引入微调、自动发送或实时社交平台接入。
- 用户人工 review 认为 ContactSkill 与真实关系认知严重不符。

## 5. T100 验证要求

T100 只做数据合约，不做语义蒸馏。

必须输出：

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- 一个脱敏 sample fixture 或明确说明为何暂不生成。

禁止输出：

- 真实联系人姓名。
- 完整聊天原文。
- 原始文件名中可识别的联系人信息。
- 手机号、地址、身份证、账号 token 等敏感信息。

T100 review 状态：`PASS`，见 `docs/review/T100_review.md`。

## 6. T101 验证要求

T101 只做规则与样例，不写代码。

必须输出：

- `docs/data_contracts/privacy_redaction_rules.md`
- `docs/data_contracts/source_ref_rules.md`
- 更新后的脱敏 sample fixture，覆盖 source_ref/raw_ref 形态。

禁止输出：

- 真实联系人姓名、真实原始文件名或完整聊天原文。
- 可反推联系人身份的账号 ID、手机号、地址、token 或媒体路径。

T101 review 状态：`PASS`，见 `docs/review/T101_review.md`。

## 7. T102 验证要求

T102 开始写最小 normalize CLI，但仍不做语义蒸馏。

必须输出：

- `private/distilled/<run_id>/normalized_events.jsonl`
- `private/distilled/<run_id>/run_report.json`
- CLI dry-run 或 limit 小样本验证记录。

禁止输出：

- 任何 normalized event 到 `docs/`、`examples/` 或 `tests/`。
- stdout 中打印真实聊天原文、真实文件名、真实联系人姓名或真实平台 ID。
- LLM 调用、chunker、ContactSkill、数据库接入或实时平台接入。

必须额外检查：

- 遵守 `docs/data_contracts/privacy_redaction_rules.md` 的 Field Handling Matrix。
- 遵守 `docs/data_contracts/source_ref_rules.md` 的 Allowed Public Shape。
- 对 `type=80` / `chatRecords` 至少形成保守处理或明确 report 中的 skipped/unsupported 记录。
- 明确 `event_id` 底层 digest 选择，并与 `normalized_event_contract.md`、`source_ref_rules.md` 保持一致。

T102 review 状态：`PASS`，见 `docs/review/T102_review.md`。

## 8. T103 验证要求

T103 是 M0 milestone review，不写代码。

必须输出：

- `docs/review/T103_milestone_review.md`
- Gate M0 verdict: `Allow` / `Conditional` / `Block`
- 若进入 M1，明确下一唯一任务。

必须检查：

- T100-T102 的 review 结论和遗留风险。
- 是否有真实聊天原文、真实文件名、真实联系人或真实平台 ID 进入可提交目录。
- normalize CLI 是否足够支持 M1 chunking 的输入。
- T102 non-blocking issues 是否需要在进入 M1 前设置条件。

T103 review 状态：Gate M0 = `Conditional` accepted，见 `docs/review/T103_review.md`。

## 9. T110 验证要求

T110 只做 conversation chunker v0，不使用 LLM。

必须输出：

- `private/distilled/<run_id>/chunks.jsonl`
- chunk run report 或等价统计。
- 每个 chunk 至少有 `chunk_id`、`contact_id`、`conversation_id`、`event_ids`、`time_range`、`message_count`、`chunking_reason`。

禁止输出：

- 私密聊天原文到 `docs/`、`examples/`、`tests/` 或 stdout。
- LLM 调用、embedding 语义切分、ContactSkill、数据库或实时平台接入。

必须额外检查：

- 保留或传递 `source_message_type_code`、`risk_flags`、`interaction_flags` 等不确定性信号，避免 chunker 抹平 T102 的保守处理。
- 对 `type=7`/`type=80` 等 mixed/system 事件采用保守 chunking 策略。
- 评估是否需要流式处理，避免放大全量内存缓存风险。

T110 review 状态：`PASS`，见 `docs/review/T110_review.md`。

## 10. T111 验证要求

T111 只定义 ChunkSummary、MemoryFactCandidate、ContactSkillCandidate 的 Pydantic schema 和 JSON contract，不调用 LLM。

必须输出：

- `docs/data_contracts/distillation_output_contract.md`
- `src/practical_chat_agent/core/models.py` 中可复用的 schema 或与现有模型兼容的候选模型定义。
- ContactSkillCandidate 的用途边界，明确禁止 persona clone / impersonation。

禁止输出：

- LLM 调用、prompt 执行或真实蒸馏结果。
- 数据库 migration。
- 私密聊天原文到 `docs/`、`examples/`、`tests/` 或 stdout。

必须额外检查：

- 所有 claim/fact/skill 相关结构都必须支持 `evidence_refs`、`confidence`、`sensitivity`、`status`。
- schema 应为 T112 的 JSON 校验和 T113 的 review artifact 留出稳定字段。
- 若修改 Python 模型，必须运行 compile 验证。

T111 review 状态：`PASS`，见 `docs/review/T111_review.md`。

## 11. T112 验证要求

T112 实现 chunk summary 与 fact extraction 的 LLM/JSON 校验管线，只支持 limit/sample，不处理全量数据。

必须输出：

- `private/distilled/<run_id>/chunk_summaries.jsonl`
- `private/distilled/<run_id>/memory_facts.jsonl`
- `run_report.json` 中记录成功、失败、校验拒绝和 skipped chunks。

禁止输出：

- 私密聊天原文、LLM 输入原文或 LLM 原始输出到 `docs/`、`examples/`、`tests/` 或 stdout。
- 无 `evidence_refs` 的 fact/claim。
- ContactSkill builder、review exporter、数据库 migration、实时平台接入或自动发送。

必须额外检查：

- LLM 输出必须校验为 T111 schema；缺失 `evidence_refs`、`confidence`、`sensitivity`、`status` 视为无效。
- evidence refs 必须能回指 T110 chunk/event 范围。
- 小样本运行后人工抽查至少 3 条 facts。
- 若模型不可用，必须在 handoff/risks 中明确记录，并不要把 mock 输出当成真实完成。
