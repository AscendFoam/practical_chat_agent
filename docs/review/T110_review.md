# Review: T110 Conversation Chunker v0

Review date: 2026-05-14
Reviewer: Claude Code (normal)
Task package: `docs/tasks/M1_offline_distillation_mvp/T110_chunker_v0.md`

## Scope

只读审查 worker 针对 T110 的所有产出，对照任务包的 Allowed files、Forbidden scope 和 Verification 要求。重点检查 chunk 边界逻辑是否保守、隐私合规、不确定性信号传递、以及是否越界引入 LLM/embedding/ContactSkill/数据库。

## Diff Summary

所有变更均为未提交状态（working tree），落在以下文件：

| 文件 | 变化类型 | 是否在 Allowed files 内 |
| --- | --- | --- |
| `src/practical_chat_agent/services/conversation_chunking.py` | 新增 | 是 |
| `src/practical_chat_agent/app/main.py` | 修改 | 是 |
| `docs/07_handoff.md` | 修改 | 是 |

零 `private/` 读取或输出泄露。零 `docs/` 下文档声称计划为已完成事实。

## Task Completion Check

| 任务包要求 | 状态 | 证据 |
| --- | --- | --- |
| 消费 T102 `normalized_events.jsonl` | **完成** | `_resolve_input_file` 定位并读取 `private/distilled/**/normalized_events.jsonl` |
| 生成 `chunks.jsonl` | **完成** | `chunk_normalized_events` 流式写入 `chunks.jsonl` |
| 每个 chunk 有 `event_ids`、`time_range`、`chunking_reason` | **完成** | `to_chunk_record` 输出 `event_ids`、`time_range`、`message_count`、`chunking_reason` |
| 不做 LLM 调用 | **完成** | 全文零 LLM/API 调用 |
| 不做 embedding 语义切分 | **完成** | 边界仅基于 conversation/contact 变化、时间间隔、消息数 |
| 不输出私密内容到可提交目录 | **完成** | 所有输出限制在 `private/distilled/` |
| CLI 可运行 | **完成** | `chatlog-chunk` 命令注册到 Typer app |
| 输出 `run_report.json` 更新 | **完成** | `_write_run_report` 追加 `chunking` 字段 |
| 更新 `docs/07_handoff.md` | **完成** | 新增 T110 worker draft 记录、状态更新 |

## Privacy Audit

### 真实聊天原文泄露检查

`_coerce_event` 方法（第 420-457 行）不读取 `text` 字段。chunker 只消费事件元数据（event_id、conversation_id、contact_id、timestamp、message_type、sender_role、interaction_flags、risk_flags），不接触消息内容。**不构成泄露。**

### Report / stdout 安全性

`result.report` 通过 `typer.echo` 输出。逐字段检查：

| report 字段 | 安全性 |
| --- | --- |
| `tool` | 字面常量 `"chatlog-chunk"` |
| `line_stats` | 纯计数统计 |
| `chunk_stats` | 纯计数统计 + 参数值 |
| `chunking_reason_counts` / `boundary_flag_counts` | 枚举型字符串 |
| `source_message_type_counts` / `message_type_counts` | 类型计数，无原文 |
| `sender_role_counts` / `status_counts` | 角色统计 |
| `interaction_flag_counts` / `risk_flag_counts` | 标记计数 |
| `warnings` | 枚举型字符串 |
| `input_file` | 使用 `_safe_relative_path` 输出相对路径，不暴露绝对路径 |
| `output_dir` | 同上 |

**结论：stdout/report 不包含真实聊天原文、真实文件名、真实联系人姓名或真实平台 ID。**

### Chunk 输出安全性

`to_chunk_record` 的输出字段：`chunk_id`（SHA-1 哈希）、`contact_id`（T102 已脱敏的哈希别名）、`conversation_id`（同上）、`event_ids`（SHA-1 哈希）、`time_range`（ISO 时间戳）、`message_count`（整数）、`chunking_reason`（枚举字符串）、`boundary_flags`（枚举）、聚合统计计数。

**chunk 输出不含任何原文、真实标识或敏感内容。**

## Compliance Check

| 检查项 | 结果 |
| --- | --- |
| 只改 Allowed files | **PASS** — 3 个文件全部在允许列表内 |
| 不做 LLM 调用 | **PASS** — 无任何 LLM/API 调用 |
| 不做 embedding 语义切分 | **PASS** — 边界仅用时间间隔、消息数、contact/conversation 变化 |
| 不做 ContactSkill | **PASS** — 无 ContactSkill 代码 |
| 不接数据库 | **PASS** — 无 DB import |
| 不输出私密内容到可提交目录 | **PASS** — 输出限制在 `private/distilled/` |
| 每个 chunk 有 event_ids、time_range、chunking_reason | **PASS** |
| 保留 T102 不确定性信号 | **PASS** — 详见下方 |

## Uncertainty Signal Preservation

T103 的 Conditional 条件要求 T110 保留 T102 的不确定性信号。逐项检查：

| T102 不确定性信号 | T110 是否保留 | 证据 |
| --- | --- | --- |
| `source_message_type_code` | **保留** | `_coerce_event` 提取，`_ChunkAccumulator` 聚合 `source_message_type_counts` |
| `risk_flags` | **保留** | `_coerce_event` 提取，`_ChunkAccumulator` 聚合 `risk_flag_counts` + `events_with_risk_flags` |
| `interaction_flags` | **保留** | 同上，聚合 `interaction_flag_counts` + `events_with_interaction_flags` |
| `message_type` (mixed/unknown) | **保留** | 聚合 `message_type_counts` |
| `sender_role` (unknown) | **保留** | 聚合 `sender_role_counts` |

额外新增的 `boundary_flags` 提供了 chunk 边界触发原因的细粒度信息。`events_with_interaction_flags` 和 `events_with_risk_flags` 列出了有问题的 event ID，方便下游精确定位。

**不确定性信号传递完整，未抹平任何 T102 遗留信号。**

## Chunk Boundary Logic Review

`_detect_boundary`（第 471-495 行）使用四条保守规则：

1. **conversation_id 变化** → 新 chunk。标记 `conversation_change`。
2. **contact_id 变化** → 新 chunk。标记 `contact_change`。
3. **message_count >= max_messages_per_chunk**（默认 80）→ 新 chunk，`reason=message_limit`。
4. **时间间隔 >= max_gap_seconds**（默认 240 分钟 = 4 小时）→ 新 chunk，`reason=time_gap`。
5. **输入结束** → 关闭最后 chunk，`reason=manual`，标记 `end_of_input`。

边界检测优先级：conversation/contact 变化 > 消息数上限 > 时间间隔。这确保了不同联系人/对话的 event 永远不会被混入同一个 chunk。**优先级合理。**

时间间隔使用 `timestamp_epoch_s` 做整数差值比较，当任一端缺失时跳过检测（不崩溃）。**安全。**

`_timestamps_non_monotonic`（第 460-468 行）检测时间戳倒流，但只在 report 的 `warnings` 集合中添加 `non_monotonic_timestamp_order`，不改变行为。这是合理的保守策略——MVP 阶段只报告、不修正。

## Performance: Single-pass Streaming

T102 N02（双次读取）和 N03（全量内存缓存）是 T103 Conditional 追踪项。

T110 的 `_chunk_file` 使用单次流式读取（`with normalized_events_path.open(...) as handle: for line_no, raw_line in enumerate(handle)`），逐行处理。chunk_lines 虽然暂存在内存中的 `list[str]`，但这是 chunk 级别（每行是序列化的 chunk JSON），不是 event 级别。对于正常对话数据量，这是可接受的。

**T102 N02 在 chunker 侧已通过单次读取解决。N03 的 chunk 级缓存对 MVP 规模可接受。**

## Pseudo-implementation / Mock / Stub / Hardcode Check

| 功能 | 是否真实实现 | 证据 |
| --- | --- | --- |
| JSONL 流式读取与解析 | 真实 | `path.open("r")` + `json.loads` 逐行处理 |
| 边界检测 | 真实 | 4 条启发式规则，基于实际字段值判断 |
| chunk_id 生成 | 真实 | `sha1("chunk|{conv_id}|{start_id}|{end_id}")[:16]`，有命名空间前缀 |
| 路径边界校验 | 真实 | `resolve()` + `relative_to()` 防穿越，与 T102 一致 |
| run_report.json 合并 | 真实 | 读取已有报告，合并 `chunking` 字段，处理异常情况 |
| 不确定性信号聚合 | 真实 | `Counter` 统计，`events_with_*` 列表记录具体 event |
| event 校验 | 真实 | `_coerce_event` 验证必填字段，缺失时抛异常而非静默跳过 |

**结论：零伪实现、零 mock、零 stub。所有核心逻辑都是真实实现。**

## Missing Verification

Worker 已运行以下验证：

1. `python -m compileall` — 编译检查通过
2. `chatlog-chunk --input private/distilled/t102_smoke --limit 12` — 小样本验证通过
3. 产出 `chunks.jsonl` 和更新 `run_report.json`
4. 12 条 events → 1 个 chunk，字段完整

**验证充分，满足任务包 Verification 要求。**

补充说明：任务包 Allowed files 不含 `tests/` 路径，自动化测试留给 T150。

## Over-engineering Check

实现规模评估：

- `conversation_chunking.py`：503 行，包含 1 个 service 类、1 个 accumulator dataclass、1 个 boundary decision dataclass、1 个 result dataclass
- `main.py` 新增：约 54 行（1 个 CLI 命令 + 2 行 import）

对于一个需要流式读取、边界检测、不确定性信号聚合和 run_report 合并的 chunker，这个规模合理。没有过早抽象、没有引入不必要依赖、没有实现禁止的功能。

唯一可讨论的设计选择：`_ChunkAccumulator` 跟踪了大量聚合统计（sender_role_counts、status_counts 等），这些在 v0 可能不是严格必需的。但考虑到下游 T112（fact extraction）和 T113（ContactSkill builder）会需要这些统计，提前收集是合理的，不算过度工程。

## Regression Risk

| 检查项 | 结论 |
| --- | --- |
| 对已有 CLI 命令的影响 | **无风险** — 新增命令不影响已有命令 |
| 对 `AppContainer` / 数据库模型的影响 | **无风险** — 新增 service 不依赖 AppContainer 或数据库 |
| 对 Telegram/飞书/meeting/memory/delivery 链路的影响 | **无风险** — 无共享代码修改 |
| 对 T102 normalize CLI 的影响 | **无风险** — chunker 独立读取 T102 产物，不修改它 |

## Plans vs Facts Check

| 文档 | 结论 |
| --- | --- |
| `07_handoff.md` 状态 | "worker draft 已完成，待 reviewer 审查" — **合规** |
| `07_handoff.md` T110 记录 | 产物清单、验证命令和剩余风险基于实际运行结果 — **合规** |
| `07_handoff.md` "不要提前标记 task 完成" | **合规** — `04_task_board.md` 未修改，T110 未标完成 |

## Blocking Issues

无。

## Non-blocking Issues

1. **N01 — `chunking_reason="manual"` 语义不精确**：`_detect_boundary` 对 conversation/contact 变化返回 `reason="manual"`，但这些是自动规则决策而非人工触发。建议使用 `structural` 或 `contact_change` 等更精确的 reason。当前 `boundary_flags` 已区分具体触发原因，所以功能不受影响。**严重度：低。**

2. **N02 — `_timestamps_non_monotonic` 只设聚合警告**：时间戳倒流检测只在整个 report 的 `warnings` 集合中加 `non_monotonic_timestamp_order`，不记录哪些具体 event 出现了倒流。建议在 `events_with_risk_flags` 或新字段中追踪。**严重度：低，不影响 chunk 正确性。**

3. **N03 — `run_report.json` 重跑覆盖**：多次运行 chunk 会覆盖之前的 `chunking` 报告。对 MVP 可接受，后续可考虑版本化或追加。**严重度：低。**

4. **N04 — 无自动化测试**：chunk 边界逻辑、event 校验、run_report 合并等缺少单元测试。任务包未要求（Allowed files 不含 tests/），留给 T150。**严重度：低，已知 deferred。**

5. **N05 — `topic_hint` 未包含**：实验计划 6.2 节的 Conversation Chunk schema 有 `topic_hint` 字段。worker 选择不包含，因为生成 topic hint 需要 LLM，超出 T110 范围。数据合约标注该字段为 `optional`，所以可接受。**严重度：极低。**

## Suspicious Implementation Details

无。所有实现逻辑清晰、边界保守、无安全漏洞。

## Verdict

**PASS**

Worker 完整完成了 T110 任务包的所有要求：

1. `ConversationChunkingService` 从 `private/distilled/**/normalized_events.jsonl` 流式读取，输出 `chunks.jsonl`。
2. 边界规则仅使用保守启发式：conversation/contact 变化、时间间隔、消息数上限、输入结束。
3. 每个 chunk 包含 `event_ids`、`time_range`、`message_count`、`chunking_reason`。
4. 完整保留 T102 不确定性信号：`source_message_type_code`、`risk_flags`、`interaction_flags`、`message_type`、`sender_role`。
5. 零 LLM、零 embedding、零 ContactSkill、零数据库、零实时平台接入。
6. 所有输出限制在 `private/distilled/`，stdout/report 不含真实原文或真实标识。
7. `chatlog-chunk` CLI 支持 `--input`、`--output`、`--limit`、`--dry-run`、`--max-gap-minutes`、`--max-messages-per-chunk`。
8. `run_report.json` 追加 `chunking` 字段，与 T102 产物共存。
9. 单次流式读取，解决了 T102 N02（双次读取）问题。
10. 无伪实现、无 mock、无 stub、无越界功能。
11. 文档状态准确，未把计划写成已完成事实。

5 个 non-blocking issues 均不阻碍 T110 通过，可在后续任务中处理。

## Recommended Next Action

1. Captain 将 T110 在 `04_task_board.md` 标记为完成。
2. 推进 T111（定义 ChunkSummary、MemoryFactCandidate、ContactSkillCandidate schema）或按项目优先级调整。
3. T112 阶段注意 N01（考虑是否需要更精确的 chunking_reason 枚举）。
4. T150 阶段补 chunker 单元测试：边界逻辑、空输入、单 event、时间戳缺失、run_report 合并。
