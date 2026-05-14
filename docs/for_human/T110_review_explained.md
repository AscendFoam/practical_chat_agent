# T110 Review Explained — Conversation Chunker v0

## 1. 这个 Task 在做什么？通俗解释

### 背景

在之前的任务中（T100-T102），我们做了这样一件事：把微信导出的聊天记录（WeFlow JSONL 文件）转换成了统一格式的"标准化事件"（normalized events）。你可以把这想象成——把各种格式混乱的聊天消息，整理成了一张张格式统一的卡片，每张卡片有事件 ID、时间戳、发送者角色、消息类型等信息。

但这些卡片是一条一条的单条消息，数量可能非常多（目前样本有 38,000 多条）。如果我们后续要让 AI 去分析这些消息、提取记忆事实、理解人际关系，不可能一条一条地处理——那样既慢又容易丢失上下文。

### T110 的核心目标

**T110 就是把这些单条消息"切块"（chunk）。**

想象你在读一本很厚的聊天记录书。你不会一个字一个字地读，而是会自然地按"话题段落"来理解。比如：

- 聊了一个话题，然后中间停了几个小时没说话——这中间就是一个自然的分界线。
- 今天和 A 聊的，明天和 B 聊的——A 和 B 的对话显然不应该混在一起。
- 连续聊了太多消息（比如超过 80 条）——太长了，需要拆开处理。

T110 的 chunker 就是用这些简单的、不需要 AI 的规则来把消息流切成一个个"对话块"（chunk）。每个 chunk 就是一个可以被后续步骤独立处理的基本单元。

### 关键约束

- **不用 AI**：不调用 LLM，不做语义分析，只用时间间隔、联系人变化、消息数这些确定性规则。
- **不用数据库**：纯文件读取和写入。
- **隐私安全**：chunker 不读取消息内容（text 字段），只看元数据。输出也不会包含任何原文。

## 2. 实现详解

### 2.1 任务目标

将 `private/distilled/<run_id>/normalized_events.jsonl`（T102 的产物）按保守启发式规则切成 chunks，输出 `chunks.jsonl`，供后续摘要、事实抽取和 ContactSkill 构建使用。

### 2.2 任务流程

```
T102 产物: normalized_events.jsonl
       ↓
ConversationChunkingService（流式读取）
       ↓ 逐条处理，检测边界
       ↓ 当检测到边界时，输出当前 chunk，开始新 chunk
       ↓
输出: chunks.jsonl + 更新 run_report.json
       ↓
后续消费者: T112（摘要/事实抽取）、T113（ContactSkill 构建）
```

### 2.3 代码变化

#### 新增文件：`conversation_chunking.py`

这是核心实现，包含以下关键组件：

**`_ChunkAccumulator`**（第 27-128 行）：一个"积攒器"，负责把属于同一个 chunk 的消息信息逐步收集起来。每收到一条消息，它就记录下：
- 消息 ID 列表（`event_ids`）
- 时间范围（`start_timestamp` / `end_timestamp`）
- 各种统计计数：消息类型分布、发送者角色分布、风险标记分布等

当检测到需要"切一刀"的时候，积攒器就把收集到的所有信息打包成一个 chunk 记录输出。

**`ConversationChunkingService`**（第 135-503 行）：主服务类，负责：
- 定位和验证输入文件（必须在 `private/distilled/` 下）
- 流式读取 JSONL，逐条处理
- 调用边界检测逻辑
- 写出 chunks 和更新报告

**边界检测规则 `_detect_boundary`**（第 471-495 行）：四条规则，按优先级排列：

| 优先级 | 规则 | 含义 | reason |
| --- | --- | --- | --- |
| 1 | conversation_id 变化 | 换了一个对话 | manual + conversation_change |
| 1 | contact_id 变化 | 换了一个联系人 | manual + contact_change |
| 2 | 消息数 >= 80（可配置） | 单个 chunk 太长 | message_limit |
| 3 | 时间间隔 >= 4 小时（可配置） | 对话中间有长时间停顿 | time_gap |

最后，输入结束时（`end_of_input`），剩余的消息也会被关闭成一个 chunk。

**`build_chunk_id`**（第 498-502 行）：用 SHA-1 哈希生成 chunk 的唯一 ID，格式为 `chk_<sha1_hex>[:16]`，确保同一个 chunk 的 ID 在多次运行中保持一致。

#### 修改文件：`main.py`

新增 `chatlog-chunk` CLI 命令（第 1569-1619 行），支持以下参数：

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--input` | `private/distilled` | 输入文件或目录 |
| `--output` | 与输入同目录 | 输出目录 |
| `--limit` | 无限制 | 只处理前 N 条消息 |
| `--dry-run` | false | 只输出报告，不写文件 |
| `--max-gap-minutes` | 240（4 小时） | 时间间隔阈值 |
| `--max-messages-per_chunk` | 80 | 单 chunk 消息数上限 |

#### 修改文件：`docs/07_handoff.md`

- 状态从"可交给 worker 执行"更新为"worker draft 已完成，待 reviewer 审查"
- 新增第 7 节记录 T110 worker draft 的详细产物、验证结果和待确认事项
- 章节编号顺延（7→8, 8→9, ...）

### 2.4 对后续开发的意义

**T110 产出的 `chunks.jsonl` 是 M1 后续所有任务的基础输入：**

- **T112（摘要与事实抽取）**：会逐 chunk 调用 LLM 生成摘要和提取记忆事实。chunk 的粒度直接影响摘要的质量——太大则信息丢失，太小则上下文不足。
- **T113（ContactSkill 构建）**：会基于多个 chunk 的摘要和事实来构建联系人画像。
- **T114（样本运行）**：会在真实数据上运行完整蒸馏管线，验证 chunk 边界是否合理。

**关键设计决策的影响：**

1. **保守启发式而非语义切分**：T110 的边界规则不需要 AI，计算成本为零，可复现。语义切分（按话题变化切分）留给后续引入 embedding 后的 v1 版本。这意味着 v0 的 chunk 可能会在某些"话题切换但没有时间间隔"的地方把不同话题的消息混在一起，但不会把不同联系人的消息混在一起。

2. **不确定性信号传递**：每个 chunk 保留了 `risk_flags`、`interaction_flags`、`source_message_type_codes` 等聚合统计。这意味着下游任务可以知道某个 chunk 里有"多少条不确定类型的消息"、"哪些 event 有风险标记"，从而在处理时更加谨慎。

3. **流式单次读取**：解决了 T102 遗留的"双次读取"问题。chunker 只需要把文件从头到尾读一遍，边读边切，内存占用与 chunk 数量而非 event 数量成正比。

## 3. 为什么给出 PASS 的 review 结果

### Review 总体判断

**Verdict: PASS** — 任务完整完成，没有阻塞性问题。

### 通过的核心原因

1. **任务要求全部满足**：
   - chunker 正确消费了 T102 的 `normalized_events.jsonl`
   - 每个 chunk 包含了所有必需字段（`event_ids`、`time_range`、`message_count`、`chunking_reason`）
   - 没有使用 LLM、embedding、ContactSkill 或数据库
   - 输出严格限制在 `private/distilled/` 目录

2. **隐私保护到位**：
   - chunker 根本不读取消息内容（text 字段），只处理元数据
   - stdout 报告只有统计计数，没有原文
   - chunk_id 使用哈希生成，不暴露原始信息

3. **不确定性信号完整保留**：
   - T102 产出的 `risk_flags`、`interaction_flags`、`source_message_type_code` 等不确定性信号在 chunk 级别被完整聚合和传递
   - 没有抹平或忽略 T103 Conditional 条件要求追踪的信号

4. **实现质量高**：
   - 零伪实现、零 mock、零硬编码
   - 流式单次读取解决了 T102 遗留的性能问题
   - 边界检测逻辑保守且优先级合理（联系人变化 > 消息数 > 时间间隔）
   - 路径校验使用 `resolve()` + `relative_to()` 防止路径穿越

5. **文档诚实**：
   - `07_handoff.md` 准确描述了当前状态（"worker draft 已完成，待 reviewer 审查"）
   - 没有提前把 T110 标记为完成
   - 没有把计划写成已完成事实

### 提出的 5 个非阻塞性问题

这些问题不阻碍 T110 通过，但值得后续关注：

1. **`chunking_reason="manual"` 语义不精确**：conversation/contact 变化是自动规则触发的，用 "manual" 描述可能造成误解。但 `boundary_flags` 已区分了具体原因，所以功能正确性不受影响。

2. **时间戳倒流只设了聚合警告**：没有记录具体哪些 event 出现了时间倒流。但这不影响 chunk 的正确性，只是调试信息可以更丰富。

3. **重跑会覆盖之前的报告**：对 MVP 来说完全可以接受，后续可以版本化。

4. **没有自动化测试**：这是有意为之——任务包的 Allowed files 不包含测试目录，测试留给 T150。

5. **没有 `topic_hint` 字段**：这需要 LLM 才能生成，超出了 T110（"不做 LLM 调用"）的范围。数据合约标注该字段为 optional，所以不包含也合规。

### 与之前 review 的一致性

T102 review 留下了 6 个 non-blocking issues，T103 review 基于此给出了 5 个 Conditional 条件。T110 的实现：

- 承接了 N02（双次读取）→ 改为单次流式读取，已解决
- 承接了 N03（全量内存缓存）→ chunk 级缓存对 MVP 可接受
- 传递了所有不确定性信号（source_message_type_code、risk_flags 等）
- 没有引入新的越界行为

整体而言，T110 是一个干净、保守、合规的实现，完全符合任务包的要求和项目的研发原则。
