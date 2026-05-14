# Architecture

更新日期：2026-05-14

## 1. 新架构定位

项目主线切换为：

```text
WeFlow JSONL export
  -> offline distillation
  -> evidence-backed memory and contact skill
  -> relationship-aware reply planning
```

旧的 iLink/微信扫描代码与任务不删除，但暂不作为当前主线。

## 2. 数据流

```text
private/chat_history/*.jsonl
  -> ChatHistoryProfiler
  -> WeFlowJsonlAdapter
  -> NormalizedEvent
  -> ConversationChunk
  -> ChunkSummary
  -> MemoryFactCandidate
  -> ContactSkillCandidate
  -> Review artifact
  -> Approved skill/memory store
  -> ReplyPlanner
```

## 3. 计划模块

```text
src/practical_chat_agent/services/chatlog_profile.py
src/practical_chat_agent/services/chatlog_ingestion.py
src/practical_chat_agent/services/conversation_chunking.py
src/practical_chat_agent/services/contact_skill.py
src/practical_chat_agent/services/reply_planner.py
src/practical_chat_agent/exporters/contact_skill_markdown.py
```

第一阶段也可以先用 CLI + service，不必立即新增数据库表。

## 3.1 当前实现状态

T100/T101 已通过 review `PASS`，当前完成的是数据合约、隐私规则和脱敏样例：

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- `docs/data_contracts/privacy_redaction_rules.md`
- `docs/data_contracts/source_ref_rules.md`
- `examples/payloads/weflow_redacted_sample.jsonl`

下一步 T102 开始实现最小 normalize CLI；仍不得做 chunking、LLM、ContactSkill 或数据库接入。

## 4. 复用现有能力

可复用：

- `core.models.InboundEvent` 的思想，但离线 normalized event 需要更明确的 `source_ref`、`sender_role` 和 `contact_id`。
- `MemoryFact` 作为后续入库目标，但离线 MVP 可先输出 JSONL。
- `ChatMemoryExtractionService` 的 JSON schema/prompt 风格。
- `ChatContextAssembler` 的上下文压缩思想。
- `PolicyEngine` 对 outbound 的保守边界，后续迁移到 reply planner。

暂不复用或不作为主线：

- `WeChatDesktopConnector`
- iLink SDK sandbox
- 微信 delivery connector
- trigger/scheduled actions

## 5. 存储策略

### 私密产物

```text
private/chat_history/
private/distilled/
private/review_workbench/
```

这些路径不提交。

### 可提交合约与脱敏样例

```text
docs/data_contracts/
examples/payloads/weflow_redacted_sample.jsonl
tests/fixtures/weflow_redacted_sample.jsonl
```

这些文件不得包含真实姓名、手机号、地址、完整原文或可识别联系人。

## 6. ContactSkill 与记忆关系

ContactSkill 是面向“如何与此人沟通”的关系技能，不是联系人人格模拟。

```text
ContactSkill
  relationship_state
  communication_style
  boundaries
  preferred_topics
  avoid_topics
  reply_strategy
  evidence_refs
  review status
```

MemoryFacts 是更原子化的事实：

```text
MemoryFact
  semantic / episodic / relationship / procedural / reflection
  claim
  evidence_refs
  status
  conflicts_with
```

运行时应只注入：

- 当前联系人 approved ContactSkill brief。
- 最近对话窗口。
- 与当前话题相关的少量 approved memory facts。
- policy/boundary constraints。

## 7. 安全架构

- 原文不进 git。
- 可提交 fixture 必须人工脱敏。
- LLM 输出必须通过 JSON schema 与 evidence refs 校验。
- 无 evidence 的 claim 直接 rejected 或要求重试。
- ContactSkill 默认 candidate，需要人工 approve。
- 回复 planner 只产草稿，不发送。
- 禁止生成“对方会怎么说”的角色扮演输出。
