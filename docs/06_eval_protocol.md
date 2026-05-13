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
- T101 必须补齐隐私脱敏规则、source_ref/raw_ref 规则和红线样例。
- T102 必须把合约落到只输出 `private/distilled/` 的 normalize CLI。
- T103 才能给出 M0 总体 Gate 结论。

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
