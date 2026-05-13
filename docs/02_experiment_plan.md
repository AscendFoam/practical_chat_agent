# 对话记录驱动的长期关系感知 Chat Agent 工程实验计划

更新日期：2026-05-13  
适用仓库：`D:\Codes\Social\practical_chat_agent`

## 1. 文档定位

本文档取代上一版“微信 iLink/桌面扫描优先”的实验计划，作为下一阶段工程主线。

路线变更原因：

- `docs/review/T01_review.md` 已确认 T01 被 BLOCK，核心原因是没有完成真实扫码登录与 session 验证。
- 用户已经通过 GitHub 上的 WeFlow 工具成功提取微信聊天记录，并存放在 `private/chat_history/`。
- 因此，下一阶段不再把“微信 SDK 登录、扫描、实时接入”作为主线，而是直接进入“基于已导出聊天记录的长期关系感知 chat agent 设计与实验”。

新的主线是：

```text
WeFlow JSONL 导出
  -> 本地隐私保护与 schema profiling
  -> normalized events
  -> conversation chunks
  -> chunk summaries
  -> evidence-backed memory facts
  -> ContactSkill / RelationshipSkill
  -> 人工 review
  -> 联系人感知回复 planner
  -> 反馈闭环与记忆生命周期
```

主要依据：

1. `docs/reference/gpt关于后续chat agent设计的思路.md`
2. `docs/deep_research_reports/对话记录驱动的长期关系感知chat agent.md`
3. `docs/review/T01_review.md`
4. 现有代码中的 `AgentRuntime`、`ChatMemoryExtractionService`、`ChatContextAssembler`、`PolicyEngine` 与 action/outbound 基础链路。

一句话结论：

> 当前最重要的不是继续打微信登录/扫描链路，而是验证“已导出的真实聊天记录能否被稳定、可审计、低幻觉地蒸馏为 ContactSkill、MemoryFacts 和关系感知回复策略”。核心资产不是模型权重，而是可追溯记忆库、可审计联系人 Skill 和有边界的回复策略。

## 2. 当前真实基线

### 2.1 已具备能力

仓库已有：

- Python package、Typer CLI、`AppContainer` 和统一 `AgentRuntime`。
- `InboundEvent`、`MemoryFact`、`ChatContext`、`ChatSuggestion`、`ActionExecutionRecord` 等核心模型。
- MySQL/SQLAlchemy 仓储和 `create_schema` 风格初始化。
- Telegram/飞书入站 payload replay。
- 微信桌面扫描和 OCR 兜底，但此路线暂不继续作为主线。
- 聊天上下文、记忆抽取、记忆检索、profile snapshot、受控 action/outbound 基础链路。
- `.gitignore` 已包含 `private/`，适合存放不可提交的 WeFlow 导出与蒸馏产物。

### 2.2 新数据基线

用户已通过 WeFlow 导出聊天记录，位于：

```text
private/chat_history/
```

这些文件属于私密数据：

- 不应提交到 git。
- 不应在治理文档中粘贴原文。
- worker 可以读取其 schema、字段、数量、时间范围等统计信息，但输出文档和测试 fixture 必须脱敏。

### 2.3 暂停或取消的旧主线

以下任务不再作为近期主线：

- 微信 iLink SDK 登录、session、收消息、reply 验证。
- 微信桌面扫描读取聊天记录。
- 自动实时消息接入。
- 微信真实发送。
- 主动触发。

旧 T00/T01 仅作为历史记录保留：

- T00：SDK 安装和二维码阶段探测通过。
- T01：因未扫码登录与未更新文档被 reviewer BLOCK。
- 用户已决定不修 T01，转向 WeFlow 导出数据路线。

## 3. 研发原则与边界

### 3.1 默认模式

- 本地优先：原始聊天记录只保留在 `private/`。
- 离线优先：先做单向蒸馏 MVP，不做实时平台接入。
- 可审计优先：每个事实、偏好、关系判断都必须有 `evidence_refs`。
- 人工 review 优先：ContactSkill 默认 candidate/review 状态，不能直接进入回复策略。
- 安全优先：不冒充联系人、不训练数字克隆、不自动发送。

### 3.2 不做什么

当前阶段明确不做：

- 不继续修 T01，也不继续微信 SDK 登录。
- 不写微信扫描或读取微信客户端记录的代码。
- 不破解微信数据库、不 hook、不注入、不绕过平台风控。
- 不微调/LoRA/DPO。
- 不把全部聊天原文一次性塞给 LLM。
- 不建立复杂前端 UI。
- 不安装或强依赖向量数据库，直到离线蒸馏 MVP 证明价值。
- 不提交 `private/` 中任何文件。

### 3.3 数据原则

- Raw JSONL 是冷备和证据来源，不直接作为 prompt 常驻上下文。
- Normalized event 必须有稳定 `event_id`、`source_ref`、联系人、时间、方向和内容类型。
- Chunk summary、memory fact、ContactSkill 都必须可反查到 event 或 chunk。
- 对外发给 LLM 的文本应经过最小脱敏或受控抽样。
- 所有产物区分：
  - 私密产物：`private/distilled/...`
  - 可提交 schema/说明：`docs/data_contracts/...`
  - 脱敏 fixture：`examples/payloads/...` 或 `tests/fixtures/...`

## 4. 目标 MVP

### 4.1 MVP 目标

输入：一个或多个 WeFlow JSONL 聊天记录文件。  
输出：

```text
private/distilled/<run_id>/
  normalized_events.jsonl
  chunks.jsonl
  chunk_summaries.jsonl
  memory_facts.jsonl
  contact_skill.candidate.json
  contact_skill.review.md
  run_report.json
```

MVP 要证明：

- WeFlow JSONL 可以被解析为统一事件格式。
- 对话可以按联系人、时间间隔、消息数和后续语义特征切块。
- chunk summary 与 memory fact 能带 evidence refs。
- ContactSkill 能表达关系状态、沟通风格、边界、偏好和回复策略。
- 人工可以审阅、修改和拒绝 skill。
- 回复 planner 可以在不冒充联系人、不自动发送的前提下利用 ContactSkill 生成候选草稿。

### 4.2 MVP 不做

- 不训练模型。
- 不自动发送。
- 不做实时平台接入。
- 不做多 agent 系统。
- 不把 `private/chat_history` 原文复制到 repo 可提交目录。
- 不追求一次性处理所有联系人，先选 1 个高价值联系人或一个小样本。

## 5. 总体架构

### 5.1 离线蒸馏管线

```text
ChatHistoryProfiler
  -> WeFlowJsonlAdapter
  -> ConversationNormalizer
  -> PrivacyRedactor
  -> ConversationChunker
  -> ChunkSummarizer
  -> FactExtractor
  -> ContactSkillBuilder
  -> SkillReviewExporter
```

### 5.2 运行时回复管线

```text
latest user draft/context
  -> recent conversation window
  -> approved ContactSkill brief
  -> relevant MemoryFacts
  -> ReplyPlanner
  -> Policy/Boundary check
  -> 3 candidate drafts + rationale + risk flags
  -> user feedback
  -> memory/skill update proposal
```

### 5.3 模块职责

- `ChatHistoryProfiler`：读取 `private/chat_history`，输出字段统计、样本 schema、文件规模，不输出原文。
- `WeFlowJsonlAdapter`：把 WeFlow JSONL 行映射为 normalized event。
- `ConversationNormalizer`：统一时间、方向、联系人、文本、媒体元数据和 source ref。
- `PrivacyRedactor`：识别手机号、地址、身份证、真实姓名等敏感片段并掩码。
- `ConversationChunker`：先做时间/消息数/联系人维度切块，后续再加入 embedding 语义边界。
- `ChunkSummarizer`：对 chunk 做客观摘要和观察，不做稳定人格判断。
- `FactExtractor`：抽取原子事实、偏好、边界、关系变化，强制 evidence refs。
- `ContactSkillBuilder`：把 summaries/facts 合成 candidate skill。
- `SkillReviewService`：导出 review Markdown，支持 approve/reject/edit。
- `ReplyPlanner`：基于 approved skill 和 memory 生成候选回复。

## 6. 数据合约

### 6.1 Normalized Event

最小字段：

```json
{
  "event_id": "evt_xxx",
  "platform": "wechat",
  "source": "weflow_jsonl",
  "source_file": "private/chat_history/<redacted>.jsonl",
  "source_line": 123,
  "conversation_id": "conv_xxx",
  "contact_id": "contact_xxx",
  "sender_role": "user|contact|system|unknown",
  "sender_id": "sender_xxx",
  "sender_name": "redacted_or_alias",
  "timestamp": "2026-05-13T10:20:00+08:00",
  "text": "message text or redacted text",
  "message_type": "text|image|voice|file|sticker|system|mixed|unknown",
  "media_refs": [],
  "status": "normal|recalled|deleted|unknown",
  "raw_ref": "weflow:<file_hash>:<line_no>"
}
```

### 6.2 Conversation Chunk

```json
{
  "chunk_id": "chk_xxx",
  "contact_id": "contact_xxx",
  "conversation_id": "conv_xxx",
  "start_event_id": "evt_a",
  "end_event_id": "evt_b",
  "event_ids": ["evt_a", "evt_b"],
  "time_range": ["start", "end"],
  "topic_hint": "optional",
  "message_count": 42,
  "chunking_reason": "time_gap|message_limit|semantic_shift|manual"
}
```

### 6.3 Memory Fact

```json
{
  "memory_id": "mem_xxx",
  "memory_type": "semantic|episodic|relationship|procedural|reflection",
  "subject_id": "contact_xxx|user|relationship_xxx",
  "claim": "可审计的事实或关系判断",
  "status": "candidate|approved|rejected|frozen|archived",
  "confidence": 0.72,
  "importance": 0.8,
  "sensitivity": "low|medium|high",
  "evidence_refs": ["evt_xxx", "chk_xxx"],
  "conflicts_with": [],
  "created_at": "..."
}
```

### 6.4 ContactSkill

ContactSkill 不是联系人数字克隆，而是用户回复辅助策略：

```json
{
  "schema_version": "contact_skill_v1",
  "contact_id": "contact_xxx",
  "relationship_type": "friend|classmate|colleague|family|unknown",
  "relationship_state": {
    "current_status": "low_frequency_but_continuing",
    "closeness": 0.45,
    "trust_level": 0.5,
    "interaction_frequency": "low",
    "initiative_balance": "user_leads_more",
    "confidence": 0.7
  },
  "communication_style": {
    "message_length": "short|medium|long|mixed",
    "tone": "polite|casual|reserved|warm|mixed",
    "response_latency": "fast|slow|unstable|unknown",
    "directness": "low|medium|high"
  },
  "preferred_topics": [],
  "avoid_topics": [],
  "important_events": [],
  "stable_preferences": [],
  "emotional_patterns": [],
  "user_side_preferences": {
    "user_goal": "",
    "boundaries": [],
    "preferred_reply_style": ""
  },
  "reply_strategy": {
    "default": "",
    "when_contact_is_cold": "",
    "when_contact_opens_topic": "",
    "for_sensitive_topics": ""
  },
  "confidence": 0.0,
  "evidence_refs": [],
  "status": "candidate|approved|rejected|archived",
  "redaction_policy": {
    "store_raw_quotes": false,
    "max_quote_length": 30,
    "mask_names": true,
    "mask_phone_numbers": true
  }
}
```

## 7. 分阶段路线图

### Milestone 0：WeFlow 数据合约与安全画像

目标：不生成 skill，先搞清楚导出数据结构、隐私边界和 normalized schema。

验收：

- 不泄露原文。
- 有 WeFlow schema profile。
- 有 normalized event 合约。
- 有小型脱敏 fixture。

### Milestone 1：离线蒸馏 MVP

目标：对一个选定联系人或小样本完成 JSONL -> chunks -> summaries -> memory facts -> candidate ContactSkill。

验收：

- 每条 memory/skill claim 都有 evidence refs。
- review.md 可人工审阅。
- 私密产物在 `private/distilled/`。

### Milestone 2：Memory/Skill Store 与证据校验

目标：把离线产物接入本项目现有模型和仓储，支持 review/approve/version。

验收：

- evidence refs 可校验。
- rejected/frozen 不进入 prompt。
- skill 可导出 JSON/Markdown。

### Milestone 3：联系人感知回复 Planner

目标：基于 approved ContactSkill、recent context 和相关 memory 生成 3 个候选回复草稿。

验收：

- 输出 JSON，含 rationale 和 risk flags。
- 不冒充联系人。
- 可解释为什么这么回复。

### Milestone 4：反馈闭环与记忆修正

目标：记录用户对草稿的 accept/edit/reject/boundary violation，并生成 memory/skill 更新提案。

验收：

- 用户修改能转化为可审阅的偏好/边界提案。
- 支持 diff、rollback、冻结。

### Milestone 5：评估与工程硬化

目标：建立自动化测试、隐私泄露检查、evidence accuracy 抽查和最终 handoff。

验收：

- 有脱敏 fixture 测试。
- 有 evidence validation。
- 有 privacy leakage smoke test。
- 文档与代码状态一致。

## 8. 推荐第一步

当前唯一任务应切换为：

```text
T100: WeFlow JSONL schema profiling 与 normalized event 合约
```

目标：

- 只读取 `private/chat_history` 的文件级统计和 JSONL 字段结构。
- 不把聊天原文写入 docs。
- 输出 `docs/data_contracts/weflow_schema_profile.md` 和 `docs/data_contracts/normalized_event_contract.md`。
- 生成一个最小脱敏 fixture，用于后续 adapter 测试。

为什么：

- 这是后续离线蒸馏管线的地基。
- 在不碰 LLM、不建数据库、不扫描微信的情况下，能最快验证数据可解析性。

## 9. 评价指标

### 数据层

- JSONL 行解析成功率。
- 时间戳可解析率。
- sender/contact/direction 可判定率。
- message_type 覆盖率。
- 脱敏 fixture 不含真实敏感内容。

### 蒸馏层

- chunk 边界人工可接受率。
- memory fact evidence 命中率。
- 幻觉率：claim 没有证据或证据不支持 claim 的比例。
- 敏感信息泄露率。
- ContactSkill 字段完整率。

### 回复层

- 候选草稿自然度。
- 是否符合 ContactSkill 边界。
- 是否过度主动/过度亲密。
- 是否能解释引用了哪些记忆。
- 用户二次编辑距离。

## 10. 停止条件

任一情况出现，应暂停当前路线并重新设计：

- WeFlow JSONL 无法稳定解析出时间、方向或联系人。
- 生成的 memory facts 大量缺 evidence refs。
- ContactSkill 出现明显人格冒充或无证据判断。
- 私密原文进入可提交目录。
- LLM 输出无法通过 JSON/evidence 校验。
- 用户人工 review 认为 skill 与真实认知严重不符。

