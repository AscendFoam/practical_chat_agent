# Review: T102 Minimal Normalize CLI

Review date: 2026-05-14
Reviewer: Claude Code (adversarial)
Task package: `docs/tasks/M0_weflow_data_contract/T102_minimal_normalize_cli.md`

## Scope

只读审查 worker 针对 T102 的所有产出，对照任务包的 Allowed files、Forbidden scope 和 Verification 要求。重点检查隐私合规、伪实现、越界和文档准确性。

## Diff Summary

所有变更均为未提交状态（working tree），落在以下文件：

| 文件 | 变化类型 | 是否在 Allowed files 内 |
| --- | --- | --- |
| `src/practical_chat_agent/services/chatlog_ingestion.py` | 新增 | 是 |
| `src/practical_chat_agent/app/main.py` | 修改 | 是 |
| `docs/07_handoff.md` | 修改 | 是 |
| `docs/08_risks_and_open_questions.md` | 修改 | 是 |

无 `docs/04_task_board.md` 变更（worker 未修改任务板，符合预期）。

## Task Completion Check

| 任务包要求 | 状态 | 证据 |
| --- | --- | --- |
| CLI `chatlog-normalize --input --output --limit --dry-run` | **完成** | `main.py:1516-1562`，5 个选项全部实现 |
| 输出 `normalized_events.jsonl` 和 `run_report.json` 到 `private/distilled/<run_id>` | **完成** | `chatlog_ingestion.py:80-91` |
| 支持 `--limit` | **完成** | `main.py:1529`，`chatlog_ingestion.py:344` 截断逻辑 |
| 支持 `--dry-run` | **完成** | `main.py:1533`，dry-run 不写文件，仅输出安全 report |
| 不在 stdout 打印原文 | **完成** | stdout 仅输出 `result.report`，report 不含 text 字段 |
| 输入路径边界限制在 `private/chat_history/` | **完成** | `chatlog_ingestion.py:55-59`，`resolve` + `relative_to` 校验 |
| 输出路径边界限制在 `private/distilled/` | **完成** | `chatlog_ingestion.py:117-122`，同上 |
| 更新 `docs/07_handoff.md` | **完成** | 新增 8.1 节、状态更新 |
| 更新 `docs/08_risks_and_open_questions.md` if needed | **完成** | R011/R012 更新、Q102/Q103 关闭 |

## Privacy Audit

### 真实聊天原文泄露检查

`chatlog_ingestion.py:531` 中 `"text": content` 直接使用原始 content，但此字段仅写入 `private/distilled/` 下的 `normalized_events.jsonl`，受 `.gitignore` 保护。**不构成泄露。**

`chatlog_ingestion.py:649` 中 `forwarded_records` 的 `content` 同理，仅在私有输出中。

### 真实联系人姓名 / 文件名泄露检查

对全部 4 个交付文件执行 grep 扫描，检查是否存在 `private/chat_history/` 中的真实文件名或真实联系人名：**无命中。**

- `chatlog_ingestion.py` 全文不出现任何真实文件名。文件别名统一使用 `file_{index:02d}` 格式（第 153 行）。
- `main.py` 的新增代码不包含任何真实标识。
- `07_handoff.md` 使用"真实私聊文件名"作为描述性文字，不是具体值。
- `08_risks_and_open_questions.md` 无真实标识。

### Report / stdout 安全性

`result.report` 通过 `typer.echo` 输出到 stdout。逐字段检查：

| report 字段 | 安全性 |
| --- | --- |
| `tool` / `source` | 字面常量，安全 |
| `file_count` / `files` | `files` 使用 `file_alias` + `size_bytes` + 统计计数，无真实文件名 |
| `line_stats` | 纯计数统计 |
| `message_type_counts` | 原始 type code 的计数，安全 |
| `identity_summary` | `self_identity_hash` 使用 SHA-1 哈希别名（12 字符截断），不暴露原始值 |
| `warnings` | 枚举型字符串，安全 |
| `input_root` | 硬编码为 `"private/chat_history"`，安全 |

**结论：stdout/report 不包含真实原文、真实文件名、真实联系人姓名或真实平台 ID。**

### normalized_events.jsonl 字段合规性

与 `normalized_event_contract.md` 的字段逐一比对：

| 合约字段 | 实现字段 | 合规 |
| --- | --- | --- |
| `event_id` | `evt_<sha1_hex>[:16]` | 合规 — 使用 namespaced SHA-1，不暴露 `platformMessageId` |
| `source_ref.file_alias` | `file_XX` | 合规 — 不含真实文件名 |
| `source_ref.platform_message_id_hash` | `pmid_<sha1_hex>[:8]` | 合规 |
| `source_ref.reply_to_platform_message_id_hash` | 条件出现 | 合规 |
| `raw_ref` | `weflow:{file_alias}:{line_no}` | 合规 — 与 source_ref_rules 格式一致 |
| `sender_id` | `sender_<sha1_hex>[:12]` | 合规 — 哈希别名 |
| `contact_id` | `contact_<sha1_hex>[:12]` | 合规 |
| `conversation_id` | `conv_<sha1_hex>[:12]` | 合规 |
| `sender_role` | user/contact/system/unknown | 合规 |
| `timestamp` | ISO 8601 + 时区偏移 | 合规 |
| `timestamp_epoch_s` | 原始值保留 | 合规 |
| `timezone_assumption` | 配置项显式提供 | 合规 |
| `message_type` | text/system/mixed/unknown | 合规 — 保守映射 |
| `status` | normal/recalled | 合规 |
| `interaction_flags` | reply/forwarded_records/system_notice/recalled_notice | 合规 |
| `risk_flags` | 详细不确定性标记 | 合规 |

**normalized event 合约合规性：全部通过。**

## Compliance Check

| 检查项 | 结果 |
| --- | --- |
| 只改 Allowed files | **PASS** — 4 个文件全部在允许列表内 |
| 遵守 privacy_redaction_rules Field Handling Matrix | **PASS** — 可提交目录零真实标识 |
| 遵守 source_ref_rules Allowed Public Shape | **PASS** — source_ref/raw_ref 格式完全一致 |
| normalize 输出只进 private/distilled/ | **PASS** — `_ensure_within_root` 校验 |
| stdout 和可提交目录不出现真实原文 | **PASS** — report 仅含统计和别名 |
| 不做 LLM 抽取 | **PASS** |
| 不做 chunker | **PASS** |
| 不做 ContactSkill | **PASS** |
| 不接数据库 | **PASS** — 无 DB import |
| 不做实时微信接入 | **PASS** |
| 文档未把计划写成已完成事实 | **PASS** — 见下方检查 |

## Plans vs Facts Check

| 文档 | 结论 |
| --- | --- |
| `07_handoff.md` | "T102 worker 已产出最小 normalize CLI，并完成 dry-run 与 limit 小样本验证；当前待 adversarial review，尚未由 Captain 标记完成。" — **合规**，状态准确 |
| `07_handoff.md` 8.1 节 | Worker 产物清单和高信号结论均基于实际运行的验证结果 — **合规** |
| `08_risks_and_open_questions.md` R011 | "T102 CLI 已对 type=80 与 chatRecords 做保守处理" — 代码可验证，`_map_message_type` 将 type=80 映射为 system — **合规** |
| `08_risks_and_open_questions.md` R012 | "T102 已落地最小可运行版本" — CLI 可运行 — **合规** |
| `08_risks_and_open_questions.md` Q102/Q103 | 描述的是 T102 实际实现行为 — **合规** |

## Pseudo-implementation / Mock / Stub / Hardcode Check

逐功能检查：

| 功能 | 是否真实实现 | 证据 |
| --- | --- | --- |
| JSONL 文件读取和解析 | 真实 | `path.open("r", encoding="utf-8")` + `json.loads` |
| 文件别名映射 | 真实 | `file_aliases = {path: f"file_{index:02d}" ...}` |
| 本地用户身份推断 | 真实 | `_resolve_self_pair` 基于跨文件 member 对复用 + message 高频对，非硬编码 |
| 联系人推断 | 真实 | `_resolve_file_contact_pairs` 基于排除 self_pair 后的最高频消息对 |
| sender_role 判定 | 真实 | 基于推断出的 self_pair/contact_pair + type=80 系统消息检测 |
| event_id 生成 | 真实 | `sha1("weflow|{file_alias}|{line_no}|{platformMessageId}")[:16]`，符合合约 |
| 消息类型映射 | 真实 | 基于 WeFlow 原始 type code 的保守映射表 |
| reply 链路解析 | 真实 | 使用 `event_ids_by_file_and_message_id` 字典查找 |
| forwarded_records 处理 | 真实 | 递归遍历 `chatRecords` 数组，对每个嵌套记录应用同样的身份推断 |
| 路径边界校验 | 真实 | `Path.resolve()` + `relative_to()` 防路径穿越 |
| 路径遍历保护 | 真实 | `resolve()` 后做 `relative_to` 检查，能阻止 `../../etc/passwd` 类攻击 |

**结论：零伪实现、零 mock、零 stub、零硬编码值。所有核心逻辑都是真实实现。**

## Missing Verification

Worker 已运行以下验证：

1. `python -m py_compile` — 编译检查通过
2. `chatlog-normalize --help` — CLI 注册成功
3. `--dry-run --limit 10` — dry-run 安全 report 输出
4. `--output private/distilled/t102_smoke --limit 12` — 产物生成
5. `normalized_events.jsonl` 12 行 JSON 解析验证
6. `run_report.json` 无真实文件名/联系人名检查

**验证覆盖充分，满足任务包 Verification 要求。**

补充说明：任务包未要求编写自动化测试（Allowed files 不含 `tests/` 路径），单元测试留给 T150。

## Over-engineering Check

实现规模评估：

- `chatlog_ingestion.py`：711 行，包含 1 个 service 类、2 个 dataclass、约 20 个方法
- `main.py` 新增：约 55 行（1 个 CLI 命令 + 1 个辅助函数 + 2 行 import）

对于一个需要处理多文件 JSONL、身份推断、reply 链路、类型映射和隐私边界的 CLI 工具，这个规模是合理的。没有过早抽象、没有引入不必要的依赖、没有实现任务包禁止的功能。

唯一值得讨论的设计选择：`_ScanResult` 和 `_scan_inputs` 会先完整扫描所有文件再逐文件 normalize，导致每个文件被读取两次。这在当前数据规模（~38k 行）下不是问题，但对未来全量处理会有性能影响。作为 MVP 实现，可以接受。

## Regression Risk

| 检查项 | 结论 |
| --- | --- |
| 对已有 CLI 命令的影响 | **无风险** — 新增命令不影响已有命令 |
| 对 `AppContainer` / 数据库模型的影响 | **无风险** — 新增 service 不依赖 AppContainer 或数据库 |
| 对 Telegram/飞书/meeting/memory/delivery 链路的影响 | **无风险** — 无共享代码修改 |
| 对 T100/T101 文档的影响 | **无风险** — 文档只做追加更新 |

## Blocking Issues

无。

## Non-blocking Issues

1. **N01 — `_resolve_timezone` 无效时区静默降级**：传入无效 timezone_name 时静默降级到 UTC，不在 report 中记录此降级行为。建议在 report 的 `warnings` 中增加一条 timezone fallback 提示。**严重度：低。**

2. **N02 — 双次文件读取**：`_scan_inputs` 和 `_normalize_messages` 各读一次完整文件。当前 ~38k 行可接受，但全量处理时建议合并为单次流式处理。**严重度：低，可推迟到 T110 或 T150。**

3. **N03 — 全量内存缓存**：所有 `normalized_lines` 存入 `list[str]` 后一次性写入。对当前规模无害，但对百万级数据可能成为瓶颈。**严重度：低，可推迟。**

4. **N04 — `_looks_like_system_notice` 标记列表硬编码**：当前使用 7 个中文关键词匹配系统消息，可能漏判非常规系统消息。但 `type=80` 整体已被映射为 `system`，此函数只在 `sender_role` 层做进一步区分，且有 `unknown` 兜底和 `risk_flags` 标记。**严重度：低。**

5. **N05 — T101 的结构化替换 token（`[PHONE]`、`[EMAIL]` 等）未在 CLI 中实现**：normalized events 的 `text` 字段在 `private/distilled/` 中保留原文，未做 PII 替换。这符合任务包"不做 LLM 抽取"的约束——结构化替换应在蒸馏管线（T112+）而非 normalize 阶段实现。但建议在 Q109 中明确标注"token 替换推迟到 T112+蒸馏阶段"。**严重度：低。**

6. **N06 — `sender_role` 推断对单文件场景可能不稳定**：如果用户只有一个聊天文件（只有一个联系人），`_resolve_self_pair` 的跨文件复用策略无法命中 member 对候选，会退化为 message pair 策略或 `None`。这不是 bug（有 warning 和 risk_flags 兜底），但在后续面向其他用户数据时需要考虑更稳健的 fallback。**严重度：低。**

## Suspicious Implementation Details

无。所有实现逻辑清晰、有合理 fallback、无安全漏洞。

## Open Questions Resolution

| Q ID | 问题 | T102 回答 | Reviewer 判断 |
| --- | --- | --- | --- |
| Q101 | sender_role 判定稳健性 | 使用跨文件 member 对复用 + message 高频对 + type=80 系统检测 + unknown 兜底 + risk_flags | 可接受，MVP 级别 |
| Q102 | 时区默认值 | 默认 `Asia/Shanghai`，保留 `timestamp_epoch_s` | 已关闭 |
| Q103 | type=7/4/23/24/99 映射 | type=7 → mixed, type=4/23/24/99 → unknown | 保守可接受 |
| Q108 | SHA-1 vs SHA-256 | 保留 SHA-1，带 `weflow` 命名空间前缀 | 可接受，未来可升级 |
| Q109 | 结构化替换 token 对齐 | 未在 normalize 阶段实现 PII 替换 | 合理，推迟到 T112+ |

## Verdict

**PASS**

Worker 完整完成了 T102 任务包的所有要求：

1. `chatlog-normalize` CLI 实现了 `--input`、`--output`、`--limit`、`--dry-run`、`--timezone-name` 五个选项。
2. 输出严格限制在 `private/distilled/`，路径边界校验使用 `resolve()` + `relative_to()` 防穿越。
3. stdout 仅输出安全 report（统计、别名、哈希），不包含真实原文、真实文件名或真实联系人。
4. normalized event 字段与 T100 合约和 T101 规则完全对齐：`file_XX` 别名、`pmid_<hex>` 哈希、`weflow:{alias}:{line}` raw_ref。
5. 消息类型映射保守（type=7 → mixed, type=80 → system, 稀有类型 → unknown），有 risk_flags 兜底。
6. 身份推断使用跨文件复用策略，有 warning 和 unknown 兜底。
7. 无伪实现、无 mock、无 stub、无越界功能。
8. 文档状态准确，未把计划写成已完成事实。
9. Worker 验证覆盖充分（编译检查 + dry-run + limit 小样本 + JSON 解析验证 + 隐私 grep）。

6 个 non-blocking issues 均不阻碍 T102 通过，可在后续任务中顺带处理。

## Recommended Next Action

1. Captain 将 T102 在 `04_task_board.md` 标记为完成。
2. 推进 T103（M0 review），确认整个 Milestone 0 可以进入 M1 离线蒸馏 MVP。
3. T103/M1 阶段建议关注：
   - N02（双次读取）在 T110 chunker 设计时考虑流式处理。
   - N05（PII token）在 T112 蒸馏管线中实现对齐。
   - N06（单文件 sender_role）在 T114 实际样本运行时验证。
