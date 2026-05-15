# Architecture

更新日期：2026-05-15

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

T100/T101/T102 已通过 review `PASS`，T103 已接受 Gate M0 = `Conditional`，T110/T111/T112 已通过 review `PASS`，T113/T120/T121/T122 已通过 review `PASS_WITH_WARNINGS`，T114 已确认 Gate M1 = `Conditional`。当前完成的是数据合约、隐私规则、脱敏样例、最小 normalize CLI、conversation chunker v0、蒸馏输出 schema、小样本 summary/fact extraction、ContactSkill review artifact、M1 milestone sample review，以及 M2 的离线 memory/skill file store、evidence validator 和人工 review CLI：

- `docs/data_contracts/weflow_schema_profile.md`
- `docs/data_contracts/normalized_event_contract.md`
- `docs/data_contracts/privacy_redaction_rules.md`
- `docs/data_contracts/source_ref_rules.md`
- `examples/payloads/weflow_redacted_sample.jsonl`
- `src/practical_chat_agent/services/chatlog_ingestion.py`
- `src/practical_chat_agent/services/conversation_chunking.py`
- `src/practical_chat_agent/services/chatlog_distillation.py`
- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/exporters/contact_skill_markdown.py`
- `src/practical_chat_agent/core/models.py` 中的 distillation candidate schema
- `docs/data_contracts/distillation_output_contract.md`
- `chatlog-normalize` CLI in `src/practical_chat_agent/app/main.py`
- `chatlog-chunk` CLI in `src/practical_chat_agent/app/main.py`
- `chatlog-distill` CLI in `src/practical_chat_agent/app/main.py`
- `chatlog-build-contact-skill` CLI in `src/practical_chat_agent/app/main.py`
- `chatlog-validate-evidence` CLI in `src/practical_chat_agent/app/main.py`
- `chatlog-review-store` CLI in `src/practical_chat_agent/app/main.py`

T120 已新增离线 memory/skill 文件 store 和 Pydantic 模型，保留 candidate/approved/rejected/frozen/archived 状态、evidence refs、source metadata 与 review metadata；T121 已新增 read-only evidence validator，校验 refs 存在性、状态规则和 human-review gate 交互；T122 已新增人工 review/approve/reject/freeze/archive/export CLI，approval 受 evidence validation report 约束；仍未接数据库或向量库。下一步 T123 将 approved + runtime-ready store records 以 compact brief 形式接入 `ChatContext`，不接 ReplyPlanner，不自动发送。

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
