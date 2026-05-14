# Review: T101 Privacy Rules And Source Refs

Review date: 2026-05-14
Reviewer: Claude Code
Task package: `docs/tasks/M0_weflow_data_contract/T101_privacy_source_refs.md`

## Scope

只读审查 worker 针对 T101 的所有产出，对照任务包的 Allowed files、Forbidden scope 和 Verification 要求。

## Diff Summary

所有变更均为未提交状态（working tree），落在以下文件：

| 文件 | 变化类型 | 是否在 Allowed files 内 |
| --- | --- | --- |
| `docs/data_contracts/privacy_redaction_rules.md` | 新增 | 是 |
| `docs/data_contracts/source_ref_rules.md` | 新增 | 是 |
| `examples/payloads/weflow_redacted_sample.jsonl` | 修改 | 是 |
| `docs/07_handoff.md` | 修改 | 是 |

无任何 `src/**` 变更。无 `docs/04_task_board.md` 变更。无 `docs/08_risks_and_open_questions.md` 变更（该文件在 Allowed files 内但不在 Docs to update 内，worker 未改是正确的）。

## Task Completion Check

| 任务包要求 | 状态 | 证据 |
| --- | --- | --- |
| 明确 PII 类型和替换策略 | **完成** | privacy_redaction_rules.md 第 3 节（4 类 PII）+ 第 5 节（3 种替换策略） |
| 明确哪些字段可进入 docs/examples/tests，哪些只能留在 private | **完成** | privacy_redaction_rules.md 第 2 节（Data Zone Rules）+ 第 4 节（Field Handling Matrix） |
| 明确 event_id/source_ref 不泄露真实文件名的规则 | **完成** | source_ref_rules.md 全文 11 节系统覆盖 |
| 更新 redacted sample 以覆盖 source_ref | **完成** | 两条 message 行已加入 `eventIdPreview`、`sourceRefPreview`、`rawRefPreview` |
| 更新 handoff | **完成** | 状态更新为"worker 交付已出，待 review"，新增 6.1 节记录 T101 产物 |

## Privacy Audit

### 真实联系人姓名泄露检查

`private/chat_history/` 中的真实文件名为 `私聊_qss.jsonl`、`私聊_米文欣.jsonl`、`私聊_赵雅萱.jsonl`、`私聊_郑然.jsonl`。

对全部 4 个交付文件执行 grep 扫描：**无命中**。

### 真实文件路径泄露检查

- `source_ref_rules.md:167` 出现 `private/chat_history/真实文件名.jsonl` — 这是"禁止"列表中的占位描述（`真实文件名` 是中文直述"真实的文件名"，不是某个真实文件的名字），不构成泄露。
- 其余位置：**无命中**。

### 样例 fixture 安全性

- 5 行 JSONL 逐行 `json.loads` 验证通过：`parsed_lines=5, all_valid_json=True`。
- 新增的 preview 字段使用合成值：`evt_a1b2c3d4e5f60718`、`pmid_a1b2c3d4`、`weflow:file_01:4`。全部符合 source_ref_rules 定义的安全形态。
- 回复消息的 `reply_to_platform_message_id_hash: pmid_a1c2d3e4` 正确关联到第一条消息的 `platform_message_id_hash`，结构一致。
- 无真实消息内容、真实 ID 或真实文件名片段。

### 规则与 T100 隐私风险字段的对应

T100 schema profile 第 8 节列出了 11 个隐私风险字段。privacy_redaction_rules.md 第 4 节 Field Handling Matrix 全部覆盖：

| T100 隐私风险字段 | privacy_redaction_rules 覆盖 |
| --- | --- |
| `content` | 第 4 节 + 第 3.2 节 |
| `sender` | 第 3.1 节 + 第 4 节 |
| `accountName` | 第 3.1 节 + 第 4 节 |
| `platformId` | 第 3.1 节 + 第 4 节 |
| `platformMessageId` | 第 3.1 节 + 第 4 节 |
| `replyToMessageId` | 第 3.1 节 + 第 6.1 节 |
| `avatar` | 第 3.3 节 + 第 4 节 |
| `meta.name` | 第 3.3 节 + 第 4 节 |
| `meta.groupAvatar` | 第 3.3 节 + 第 4 节 |
| `chatRecords[*].content` | 第 3.2 节 + 第 6.2 节 |
| `chatRecords[*].sender/accountName/avatar` | 第 3.1 节 + 第 6.2 节 |

## Compliance Check

| 检查项 | 结果 |
| --- | --- |
| 只改 Allowed files | **PASS** — 4 个文件全部在允许列表内 |
| 未修改 `src/**` | **PASS** |
| 未复制真实原文 | **PASS** |
| 未实现脱敏器 | **PASS** — 纯规则文档，无代码 |
| 未做 LLM 抽取 | **PASS** |
| 未做 chunker / 数据库 / 实时接入 | **PASS** |
| 文档未把计划写成已完成事实 | **PASS** — 见下方检查 |

## Plans vs Facts Check

| 文档 | 结论 |
| --- | --- |
| privacy_redaction_rules.md | 第 8 节明确写"本轮只定义规则，不实现脱敏器"。替换策略中的结构化 token（`[PHONE]` 等）是"未来蒸馏流程中保留"的建议，未声称已实现。**合规** |
| source_ref_rules.md | 第 8 节注明"T102 会最终确认底层 digest"，未声称算法已定板。**合规** |
| sample fixture | preview 字段是"fixture 注释字段"，handoff 已说明"不应被误当成 WeFlow 官方原始字段"。**合规** |
| handoff | 状态写"worker 交付已出，等待 reviewer 判定"。**合规** |

## Pseudo-implementation / Mock / Stub / Hardcode Check

本次任务为纯文档任务，无代码实现。所有规则是设计定义而非可执行代码。样例 fixture 中的 preview 值是手工合成的可读占位（`a1b2c3d4`），不是从真实数据计算出的哈希。这符合"合成值"要求。

不存在伪实现、mock、stub 或硬编码问题。

## Missing Verification

任务包要求：

1. **人工检查 sample 无真实标识** — Worker 用 `rg` 检查了新文档和样例，未命中真实文件名或联系人名。Reviewer 独立验证确认。
2. **规则能解释 T100 中发现的隐私风险字段** — Reviewer 逐条比对，11 个 T100 隐私字段全部被 privacy_redaction_rules 覆盖（见上方对应表）。

验证充分。

## Over-engineering Check

无过度工程。privacy_redaction_rules 约 180 行覆盖 8 个章节，source_ref_rules 约 210 行覆盖 11 个章节。两份文档各自聚焦一个主题，没有交叉冗余或提前设计脱敏器实现。

## Regression Risk

无。`src/` 目录零代码变更。对 T100 交付的 sample fixture 只做了追加字段（3 个 preview），未删除或修改已有字段。

## Blocking Issues

无。

## Non-blocking Issues

1. **N01 — 样例仍未覆盖 type=80 和 chatRecords**：这是 T100 N02 的延续。T101 的任务范围是脱敏规则和 source_ref，不要求补充消息类型覆盖，但后续 T102/T150 仍需解决。

2. **N02 — preview 字段的 hex 值过于规整**：`a1b2c3d4`、`b1c2d3e4` 是手工挑选的可读序列，不是真实哈希输出。这作为 fixture 注释是完全可以的，但如果有人把它当成"正确哈希格式"来复制，可能产生困惑。风险很低，不影响通过。

3. **N03 — privacy_redaction_rules 第 3.4 节的结构化替换 token 是前瞻性设计**：`[PHONE]`、`[EMAIL]` 等 token 是未来脱敏器的占位规范，当前阶段不实现。文档用词是"若未来需要"和"应至少支持"，没有声称已实现。合规，但建议 T102 实现时校验这些 token 是否与实际需求对齐。

## Suspicious Implementation Details

无。所有规则定义合理，样例内容安全。

## Verdict

**PASS**

Worker 完整完成了 T101 任务包的所有要求：隐私脱敏规则明确了 PII 分类、数据区域边界和替换策略；source_ref 规则系统覆盖了别名、行号、消息 ID、event_id 的公共形态与红线；样例 fixture 正确追加了 source_ref/raw_ref 预览字段；handoff 更新为"待 review"状态。

隐私审查通过：真实联系人姓名和真实文件名在交付文件中零出现。规则完整覆盖了 T100 发现的全部 11 个隐私风险字段。文档没有把计划写成已完成事实。

3 个 non-blocking issues 均不阻碍 T101 通过，可在后续任务中顺带处理。

## Recommended Next Action

1. Captain 将 T101 在 `04_task_board.md` 标记为完成。
2. 推进 T102（WeFlow adapter 的最小 normalize CLI），T102 必须遵守本任务定义的隐私脱敏规则和 source_ref 规则。
3. T102 worker 参考源码实现时：
   - 遵守 privacy_redaction_rules 的 Field Handling Matrix。
   - 遵守 source_ref_rules 的 Allowed Public Shape。
   - 考虑 N01，补充 type=80 和 chatRecords 的合成 fixture。
   - 确认 event_id 底层 digest 算法（SHA-1 / SHA-256）。
