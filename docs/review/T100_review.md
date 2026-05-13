# Review: T100 WeFlow Schema Profile

Review date: 2026-05-14
Reviewer: Claude Code
Task package: `docs/tasks/M0_weflow_data_contract/T100_schema_profile.md`

## Scope

只读审查 worker 针对 T100 的所有产出，对照任务包的 Allowed files、Forbidden scope 和 Verification 要求。

## Diff Summary

所有变更均为未提交状态（working tree），落在以下文件：

| 文件 | 变化类型 | 是否在 Allowed files 内 |
| --- | --- | --- |
| `docs/data_contracts/weflow_schema_profile.md` | 新增 | 是 |
| `docs/data_contracts/normalized_event_contract.md` | 新增 | 是 |
| `examples/payloads/weflow_redacted_sample.jsonl` | 新增 | 是 |
| `docs/07_handoff.md` | 修改 | 是 |
| `docs/08_risks_and_open_questions.md` | 修改 | 是 |

无任何 `src/practical_chat_agent/**` 变更。无 `docs/04_task_board.md` 变更。

## Task Completion Check

| 任务包要求 | 状态 | 证据 |
| --- | --- | --- |
| 文件数量、总行数、可解析行数、失败行数 | **完成** | profile 第 1 节：4 文件，38,289 行，全部可解析 |
| 字段名集合、类型统计、字段出现率 | **完成** | profile 第 3 节：完整的字段/类型/出现率表 |
| 消息类型字段候选 | **完成** | profile 第 4 节：`type` 字段 8 种编码的分布和候选归类 |
| 时间戳字段候选和格式观察 | **完成** | profile 第 5 节：epoch seconds 确认，无显式时区 |
| 发送者/接收者/方向字段候选 | **完成** | profile 第 6 节：跨文件复用身份的 user 判定规则 |
| 媒体/系统/撤回/引用字段候选 | **完成** | profile 第 7 节：replyToMessageId、chatRecords、type=80 |
| 隐私风险字段清单 | **完成** | profile 第 8 节：11 个字段的脱敏建议 |
| normalized event JSON schema 草案 | **完成** | contract 第 2 节：完整 schema + 字段说明表 |
| event_id 生成规则 | **完成** | contract 第 3 节：sha1 哈希方案 + 回退规则 |
| source_ref/raw_ref 规则 | **完成** | contract 第 4 节：结构化对象 + 紧凑串 |
| sender_role 判定规则 | **完成** | contract 第 5 节：5 步保守判定流程 |
| timestamp 解析规则 | **完成** | contract 第 6 节：epoch -> ISO 8601 + 配置时区 |
| message_type 映射规则 | **完成** | contract 第 7 节：保守映射表 |
| 脱敏原则 | **完成** | contract 第 8 节：5 条规则 |
| 当前未决问题 | **完成** | contract 第 9 节：5 个 open questions |
| 脱敏样例（2-5 行） | **完成** | sample 5 行，覆盖 header/member/message/reply |
| 不含真实内容 | **完成** | 见下方隐私审查 |
| 更新 handoff | **完成** | 状态更新为"worker 交付已出，待 review" |
| 更新 risks | **完成** | 新增 R010，关闭 Q100/Q104，更新 Q101-Q103 |
| 不修改 task board | **完成** | `docs/04_task_board.md` 无变更 |

## Privacy Audit

### 真实文件名泄露检查

`private/chat_history/` 中的真实文件名为：
- `私聊_qss.jsonl`
- `私聊_米文欣.jsonl`
- `私聊_赵雅萱.jsonl`
- `私聊_郑然.jsonl`

对全部 5 个交付文件执行 `grep` 扫描：**无命中**。交付文件一致使用 `file_01` 到 `file_04` 别名。

### 真实联系人姓名泄露检查

对全部交付文件搜索真实联系人姓名：**无命中**。

### 样例 fixture 安全性

- 5 行 JSONL 全部以 `[SYNTHETIC]` 标记或使用明确合成标识（`wxid_self_redacted`、`CONTACT_A`、`ACCOUNT_SELF`、`avatar_conversation_redacted.png`）。
- 无任何真实消息内容、真实 ID 或真实文件名片段。
- 逐行 `json.loads` 验证通过：`parsed_lines=5, all_valid_json=True`。

### 时间范围泄露

Profile 记录了时间范围 `2025-11-25` 至 `2026-05-13`。这是聚合级元数据，不泄露具体对话内容或联系人，可以接受。

## Compliance Check

| 检查项 | 结果 |
| --- | --- |
| 只改 Allowed files | **PASS** — 5 个文件全部在允许列表内 |
| 未修改 `src/practical_chat_agent/**` | **PASS** |
| 未复制真实聊天原文到 docs/examples/tests | **PASS** |
| 未写真实联系人姓名 | **PASS** |
| 未写真实原始文件名 | **PASS** |
| 未写手机号/地址/账号 ID | **PASS** |
| 未做 LLM 抽取 | **PASS** — 纯文档任务 |
| 未实现 chunker | **PASS** |
| 未新增数据库 | **PASS** |
| 未恢复 iLink/微信扫描任务 | **PASS** |
| 文档未把计划写成已完成事实 | **PASS** — 见下方详细检查 |

## Plans vs Facts Check

逐文件检查是否存在"把计划写成已完成事实"的情况：

| 文档 | 结论 |
| --- | --- |
| schema profile | 所有统计是观察结果而非计划。映射建议明确标注"候选"。适配说明标注"后续 T102"。**合规** |
| normalized contract | schema 标注为"草案"。映射规则标注为"建议"。open questions 明确列出。**合规** |
| sample fixture | 纯合成数据，无事实声明。**合规** |
| handoff | 状态写为"worker 交付已出，等待 reviewer 判定"，未标 T100 为完成。**合规** |
| risks | Q100/Q104 关闭依据标注为"T100 worker draft"，未标为已通过 review。**合规** |

## Pseudo-implementation / Mock / Stub / Hardcode Check

本次任务为纯文档任务，无代码实现。所有统计数据来自对真实 JSONL 文件的实际分析（38,289 行全部可解析），非 mock。normalized event schema 是合约草案而非实现。样例 fixture 是手工合成而非从真实数据截取。

不存在伪实现、mock、stub 或硬编码问题。

## Missing Verification

任务包要求"至少运行一个只输出统计、不输出原文的本地检查命令"。Worker 报告已执行：

1. 本地统计脚本：确认 4 文件、38,289 行，全部可解析。
2. 样例逐行 JSON 解析：`parsed_lines=5`。
3. `rg` 检查新文档和样例，未命中真实文件名或联系人名。
4. `git status` 确认变更范围。

Reviewer 独立验证了 #2（逐行 JSON 解析通过）和 #3（grep 扫描无真实文件名泄露）。验证充分。

## Over-engineering Check

无过度工程。文档长度与任务复杂度匹配：schema profile 约 230 行覆盖 9 个必需要求，normalized contract 约 210 行覆盖 8 个必需要求。样例 fixture 5 行，满足"2 到 5 行"要求。

没有提前实现 adapter 代码、chunker 逻辑或数据库 schema。

## Regression Risk

无。`src/` 目录零代码变更，`docs/04_task_board.md` 未修改。

## Blocking Issues

无。

## Non-blocking Issues

1. **N01 — Q100/Q104 关闭依据为 "worker draft"**：`08_risks_and_open_questions.md` 中 Q100 和 Q104 的关闭依据写的是 "T100 worker draft"，这意味着它们尚未通过 adversarial review 就被移到了 Closed Questions。本 review 确认这两条结论是准确的，因此不构成阻断。但建议 Captain 在关闭时将依据更新为 "T100 worker draft + review PASS"。

2. **N02 — 样例 fixture 缺少 `type=80`（系统消息）和 `chatRecords`（转发记录）的覆盖**：当前 5 行覆盖了 header、member、普通文本消息（type=0）和回复消息（type=25）。type=80 和 chatRecords 只在 schema profile 中有统计描述，但样例里没有对应的合成行。这不违反任务包要求（"能代表主要字段结构"），但后续 T102/T150 可能需要补充这些类型的 fixture。

3. **N03 — `event_id` 方案使用 SHA-1**：SHA-1 存在碰撞风险，但当前用途是生成稳定别名而非密码学安全哈希，且输入空间极小（文件别名 + 行号 + 平台 ID），碰撞概率可忽略。可接受，无需更改。若后续对安全性有更高要求可升级为 SHA-256。

## Suspicious Implementation Details

无。所有观察与实际数据一致。

## Verdict

**PASS**

Worker 完整完成了 T100 任务包的所有要求：schema profile 覆盖了字段结构、消息类型、时间戳、方向和隐私风险；normalized event contract 提供了稳健的合约草案；样例 fixture 是纯合成内容且通过 JSON 解析验证；handoff 和 risks 文档更新为"待 review"状态，未越界标完成。

隐私审查通过：真实文件名（含联系人姓名）、真实消息内容、真实平台 ID 均未出现在任何交付文件中。文档中没有把计划写成已完成事实的情况。

3 个 non-blocking issues 均不阻碍 T100 通过，可由 Captain 决定是否在后续任务中处理。

## Recommended Next Action

1. Captain 将 T100 在 `04_task_board.md` 标记为完成。
2. 将 N01 的 Q100/Q104 关闭依据更新为 "T100 worker draft + review PASS"。
3. 推进 T101（脱敏规则和红线测试样例）或 T102（最小 normalize CLI），两者可并行。
4. T102 worker 在实现 adapter 时参考 N02，考虑补充 type=80 和 chatRecords 的合成 fixture。
