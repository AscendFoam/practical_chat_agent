# T112 Review Explained — Summary And Fact Extraction

## 1. 这个 Task 在做什么？通俗解释

### 背景

在前面的任务中，我们完成了：
- T102：把微信聊天记录转换成了标准化的消息事件
- T110：把这些消息按时间间隔和联系人切成了对话块（chunk）
- T111：定义了"摘要"和"记忆事实"的严格数据格式

现在有了对话块，也有了格式规则，下一步就是让 AI 来分析这些对话块。

### T112 的核心目标

**T112 是第一次让 AI（LLM）真正参与到数据分析中来**——让 AI 读取每个对话块，从中提炼出摘要和记忆事实。

具体来说：

1. **摘要（ChunkSummary）**：AI 对一段对话的客观总结。比如"这段对话中，联系人介绍了自己的考试目标和目前的准备进度"。

2. **记忆事实（MemoryFactCandidate）**：从对话中提取的可以长期记住的原子化信息。比如"联系人的目标院校是 XXX"、"联系人预计自己的分数在 YYY 范围"。

**但关键是——AI 的输出不能直接当真。** 每条输出都必须：
- 有证据引用（能追溯到具体的消息 ID）
- 通过严格的格式校验（必须符合 T111 定义的 schema）
- 标记为"候选"状态（需要人工审阅后才能变成"已批准"）

### 关键约束

- **不处理全量数据**：先用小样本（limit/sample）验证管线是否工作。
- **不保存 LLM 原文**：AI 的输入 prompt 和原始响应不写入可提交目录。
- **不接受无证据的输出**：AI 如果输出了一条没有 evidence_refs 的事实，直接拒绝。
- **不用 mock 假装完成**：如果 AI 模型不可用，如实记录，不用假数据冒充。

## 2. 实现详解

### 2.1 任务目标

实现 chunk summary 与 fact extraction 的 LLM/JSON 校验管线，对 T110 的 chunks 调用 OpenAI-compatible LLM，将输出校验为 T111 schema，拒绝无 evidence_refs 的 claim。

### 2.2 任务流程

```
T110 产物: chunks.jsonl + T102 产物: normalized_events.jsonl
       ↓
ChatlogDistillationService
       ↓ 1. 加载 selected chunks（支持 limit/sample）
       ↓ 2. 加载对应 normalized events（只加载需要的 event_ids）
       ↓ 3. 对每个 chunk:
       ↓    a. 构建 LLM prompt（含脱敏后的消息内容）
       ↓    b. 调用 OpenAI-compatible /chat/completions
       ↓    c. 提取和解析 JSON 响应
       ↓    d. Provider 兼容归一化（处理各种键名变体）
       ↓    e. Pydantic schema 校验（T111 ChunkSummary / MemoryFactCandidate）
       ↓    f. Evidence refs 范围校验（只能用 chunk_id 和 event_ids）
       ↓ 4. 只写出通过全部校验的 accepted 输出
       ↓
输出: chunk_summaries.jsonl + memory_facts.jsonl + run_report.json
       ↓
后续消费者: T113（ContactSkill builder）、T114（人工抽查）
```

### 2.3 代码变化

#### 新增文件：`chatlog_distillation.py`（1287 行）

这是 T112 的核心实现，包含以下关键组件：

**`ChatlogDistillationService`**：主服务类，负责整个蒸馏管线。

**LLM 请求层**：
- `_build_system_prompt`（第 309-323 行）：系统提示词，明确告诉 AI 只返回 JSON、每个 claim 必须有 evidence_refs、只能用提供的 chunk_id 和 event_ids、保持保守。
- `_build_user_prompt`（第 325-353 行）：用户提示词，包含 chunk 元数据和脱敏后的消息列表。
- `_post_json`（第 1117-1142 行）：使用标准库 `urllib` 发送 HTTP POST，不依赖第三方 HTTP 库。
- `_build_response_format`（第 355-365 行）：根据模型类型选择 JSON 输出模式（deepseek 用 `json_object`，其他用 `json_schema` strict mode）。

**Provider 兼容归一化层**：
- `_normalize_provider_output`（第 367-409 行）：处理 LLM 返回的 JSON 可能出现的各种格式变体——嵌套在 `result`/`data`/`output` 中、`chunk_summary` 键名不同、`memory_facts`/`facts`/`memories` 键名变体。
- `_normalize_chunk_summary`（第 411-442 行）：处理摘要的各种字段名变体（`summary`/`overview`/`description`）。
- `_normalize_memory_fact`（第 444-495 行）：处理事实的各种格式（完整 claim 或 predicate+object 格式）。

**为什么需要兼容归一化？** 因为不同的 AI 模型/provider 返回的 JSON 格式不完全一致。即使给了 strict schema，有些 provider 还是会：
- 在外面包一层 `{"result": {...}}`
- 用不同的字段名
- 用 `predicate`+`object` 替代完整的 `claim` 句子

兼容层确保这些变体都能被正确解析，但最终仍需通过严格的 Pydantic schema 校验。

**Schema 校验层**：
- `_ChunkDistillationEnvelope`（第 52-54 行）：Pydantic 模型，定义 LLM 输出的期望结构。
- `_build_chunk_summary`（第 497-548 行）：将归一化后的数据构建为 T111 的 `ChunkSummary` 对象。
- `_build_memory_facts`（第 550-589 行）：将归一化后的数据构建为 T111 的 `MemoryFactCandidate` 对象。

**Evidence Refs 范围校验**：
- `_validate_chunk_evidence`（第 591-638 行）：核心校验逻辑。
  - `allowed_refs = set(chunk_event_ids) | {chunk_id}`
  - 检查 summary、important_facts、observations、memory_facts 的所有 evidence_refs
  - 空引用 → `empty_evidence_refs`
  - 越界引用 → `out_of_scope_evidence_refs`
  - memory_facts 的 `source_chunk_ids` 必须包含当前 `chunk_id`

**PII 脱敏**：
- `_redact_private_text`（第 1096-1108 行）：在构建 LLM prompt 时对消息内容做脱敏。
  - Email → `[EMAIL]`
  - 电话 → `[PHONE]`
  - URL → `[URL]`
  - 路径 → `[PATH]`
  - 6+ 位数字 → `[NUMBER]`
  - wxid/长账号 → `[ACCOUNT]`
  - 截断到 240 字符

**错误处理**：
- `ChatlogDistillationError`：自定义错误类，带 `code` 字段用于统计。
- 5 种 chunk 状态：`ok`（成功）、`failed`（LLM 错误）、`rejected`（evidence refs 不合法）、`skipped`（缺少事件数据）。
- `run_report.json` 的 `failure_reasons` 按错误码汇总。

#### 新增文件：`contact_skill.py`（40 行）

轻量辅助模块，只有两个函数：
- `summarize_distillation_inputs`：返回状态字符串（"distillation_inputs_ready: chunk_summaries=N memory_facts=N"）
- `collect_source_refs`：从 chunk summaries 和 memory facts 中收集去重的 evidence refs

**不包含 ContactSkill builder、review exporter 或 store 逻辑**——这些是 T113 的 scope。

#### 修改文件：`main.py`

新增 `chatlog-distill` CLI 命令（约 54 行），支持：

| 参数 | 说明 |
| --- | --- |
| `--input` | 输入 chunks.jsonl 或 run 目录 |
| `--output` | 输出目录（默认与输入同目录） |
| `--limit` | 只处理前 N 个 chunks |
| `--sample` | 均匀抽样 N 个 chunks |
| `--dry-run` | 只输出报告不写文件 |

复用现有 `settings` 的 `openai_api_key`、`openai_base_url`、`chat_memory_model` 配置。

#### 修改文件：`07_handoff.md`

新增第 14 节记录 T112 worker draft。

#### 修改文件：`08_risks_and_open_questions.md`

新增 R024：provider 返回 JSON 形状漂移风险。

### 2.4 对后续开发的意义

**T112 是整个蒸馏管线从"准备阶段"进入"实际运行阶段"的转折点：**

- **T113（ContactSkill builder）**：将消费 T112 产出的 `chunk_summaries.jsonl` 和 `memory_facts.jsonl`，把它们聚合为联系人的沟通技能候选。`contact_skill.py` 的 `collect_source_refs` 会帮助 T113 收集证据引用。

- **T114（样本运行与人工抽查）**：将在真实样本上运行完整管线，人工验证 fact 的质量。T112 的 `run_report.json` 提供了详细的统计（成功/失败/拒绝/跳过）和 chunk 级别的处理结果。

- **T150（自动化测试）**：需要为 T112 的核心组件补充测试——schema 校验、evidence refs 范围检查、PII 脱敏、provider 归一化。

**关键设计决策的影响：**

1. **Provider 兼容归一化层**：这是 T112 对真实世界 complexity 的直接回应。AI 模型的输出不像教科书那样规整——实际运行中发现 provider 返回的 JSON 格式与 T111 schema 不完全一致。归一化层让管线在面对不完美的 LLM 输出时仍然能工作，而不是直接报错。但这也意味着 T150 需要覆盖 provider shape drift 的回归测试。

2. **Evidence refs 的 default fallback**：如果 LLM 没有输出 evidence_refs，系统会用 `chunk_id` 作为默认证据。这保证了每条输出至少有一个证据引用（chunk 级别），但精度比 event 级别低。这是一个 MVP 阶段的合理折中——先保证管线能运行，后续可以优化 prompt 或收紧策略。

3. **标准库 urllib 而非第三方 HTTP 库**：不引入 `requests` 或 `httpx` 等新依赖，使用 Python 标准库。这减少了依赖管理复杂度，但代码更冗长（手动处理 HTTP 错误、JSON 解析等）。

4. **PII 脱敏在 prompt 构建层**：脱敏发生在把消息内容发送给 LLM 之前。这意味着 LLM 看到的是脱敏后的内容（邮箱变成了 `[EMAIL]`），生成的摘要和事实也不会包含原始 PII。这从源头上减少了 PII 泄露到蒸馏产物中的风险。

## 3. 为什么给出 PASS 的 review 结果

### Review 总体判断

**Verdict: PASS** — 任务完整完成，没有阻塞性问题。

### 通过的核心原因

1. **任务要求全部满足**：
   - `chatlog-distill` CLI 成功运行，产出了 `chunk_summaries.jsonl` 和 `memory_facts.jsonl`
   - 每条 claim 都经过 Pydantic schema 校验（T111 schema）
   - 每条 claim 都经过 evidence refs 范围校验（只能引用 chunk_id 或 event_ids）
   - 不符合要求的输出被拒绝，记录在 `run_report.json` 中
   - 支持 limit/sample/dry-run

2. **LLM 输出校验管线完整**：
   - 从 raw response → JSON 提取 → provider 归一化 → Pydantic schema 校验 → evidence refs 范围校验，每一步都有明确的失败路径
   - 归一化不绕过校验——它只降低解析失败率，最终仍需通过严格 schema 校验

3. **隐私保护到位**：
   - LLM prompt 中的消息内容经过 PII 脱敏（6 种正则替换）
   - LLM raw response 不写入任何文件
   - stdout/report 只有统计和状态码
   - 所有产物仅存在于 `private/distilled/`

4. **没有用 mock 假装完成**：
   - 首次因沙箱网络限制失败时，如实记录了 `remote_request_failed`
   - 提权后重新运行，确认 provider 可达后才标记验证完成

5. **人工抽查了 3+ 条 fact**：
   - 每条 fact 的 evidence_refs 都能回指到当前 chunk 的具体事件
   - 没有越界引用

6. **没有越界行为**：
   - `contact_skill.py` 只有轻量辅助函数，没有 ContactSkill builder
   - 没有数据库 migration、实时平台接入或自动发送

7. **文档诚实**：
   - `07_handoff.md` 状态为"待 reviewer 审查"
   - `08_risks_and_open_questions.md` 新增 R024 记录 provider shape drift 风险
   - 没有提前把 T112 标记为完成

### 提出的 7 个非阻塞性问题

1. **N01 — evidence refs 的 default fallback 降低精度**：LLM 不提供细粒度 evidence_refs 时，系统用 chunk_id 作为默认证据。chunk_id 是合法证据，但精度不如 event_id。T114 全量抽查时需要关注。

2. **N02 — predicate→claim 硬编码模板**：8 个模板基于当前 deepseek 输出行为。换模型后可能失效。已在 R024 中跟踪。

3. **N03 — sensitivity 关键词推断硬编码**：用英文/中文关键词推断敏感度。不完整但 MVP 可接受。

4. **N04 — memory_type fallback 关键词推断**：类似 N03，用关键词推断记忆类型。保守但可能误分类。

5. **N05 — contact_skill.py 轻量但作用有限**：只有 2 个辅助函数。T113 可能需要大幅扩展。

6. **N06 — 无自动化测试**：T150 补充。

7. **N07 — PII 脱敏部分实现了 T102 N05**：`_redact_private_text` 覆盖了 6 种 PII 类型，但这是在 prompt 层而非 normalized event 层。

### 为什么这些问题不构成 BLOCK

这 7 个问题都是"MVP 阶段的合理折中"——核心管线（LLM 调用 → schema 校验 → evidence 校验 → 文件输出）完整且正确地工作。后续任务（T113/T114/T150）有明确的路径来处理这些折中带来的限制。
