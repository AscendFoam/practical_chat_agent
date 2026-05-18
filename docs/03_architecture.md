# Architecture

## Captain Update 2026-05-18 (T151 Review)

T151 extends the committed architectural safety net from planner-through-policy behavior to direct policy-engine behavior:

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlanPolicyEngine
  -> committed synthetic planner tests
  -> committed synthetic policy-engine tests
  -> reviewable safety baseline
```

The next architectural step is still hardening rather than feature growth:

```text
Planner + policy regression coverage
  -> feedback CLI regression coverage
  -> only then M5 feedback-to-patch candidates
```

## Captain Update 2026-05-18

T150 adds a committed architectural safety net around the existing review-only planner path:

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlan candidates
  -> committed synthetic regression tests
  -> reviewable safety baseline
```

The next architectural step remains inside hardening, not feature expansion:

```text
ReplyPlanner regression coverage
  -> policy fixture suite and direct policy assertions
  -> feedback CLI regression coverage
  -> only then M5 feedback-to-patch candidates
```

## Captain Update 2026-05-17

T142 is now complete, so the architecture has a full review-only M4 feedback loop:

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlan candidates
  -> human review
  -> private feedback log
  -> read-only validation report
  -> aggregate safe summary
```

The next architectural step is not patch generation. The next step is regression hardening:

```text
M4 review-only feedback loop
  -> M4.5 committed regression tests and fixtures
  -> only then M5 feedback-to-patch candidates
```

This preserves the current contract: no auto-send, no realtime integration, no ContactSkill/Memory mutation, and no feedback-to-learning jump before reproducible tests exist.

## Captain Update 2026-05-17

T140 is now complete. The architecture has advanced from "reply planning only" to "reply planning plus private human feedback capture":

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlan candidates
  -> policy/boundary risk flags
  -> human review
  -> private feedback log
```

The next architectural step is T141, which adds a read-only validation layer in front of any future feedback summaries or patch proposals:

```text
private feedback log
  -> feedback validator
  -> safe validation report
  -> later safe summary / later reviewable patch candidates
```

This validator layer must stay non-mutating: it may inspect feedback records and referenced `ReplyPlan` files, but it must not rewrite feedback logs, mutate ContactSkill or MemoryFact stores, or trigger any outbound behavior.

## Captain Update 2026-05-16

M3 is now conditionally closed. The architecture includes a review-only ReplyPlanner path:

```text
Approved compact ChatContext
  -> ReplyPlanner
  -> ReplyPlan candidates
  -> policy/boundary risk flags
  -> human review
```

M4 begins with feedback capture, not autonomous learning:

```text
ReplyPlan candidate
  -> human accept/edit/reject/boundary feedback
  -> private feedback log
  -> later reviewable proposal/versioning tasks
```

Feedback records must not directly mutate ContactSkill, MemoryFact, approved store records, planner templates, or outbound delivery. No auto-send, realtime integration, DB/vector DB expansion, or LLM drafting expansion is allowed in T140.

## Captain Update 2026-05-16: Roadmap Architecture

The architecture is extended as a staged ladder:

```text
M4 Feedback Capture
  -> M4.5 Regression Hardening
  -> M5 PreferencePatch candidates
  -> M6 ContactSkill-compatible derived briefs
  -> M7 optional LLM-assisted ReplyPlanner
  -> M8 RelationshipState
  -> M9 MemoryRetriever abstraction
  -> M10 draft-only BehaviorPlanner
  -> M11 OutboundSendGate + Feishu sandbox
  -> M12 thin WeChat adapter
```

Key architecture decision: platform adapters and external memory systems stay outside the core until send gate, regression tests, approved records, and review metadata are in place.

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

T130 完成后，M3 的结构边界也已固定：ReplyPlan 只消费 compact `ChatContext` 和 approved-store brief，不回读原始聊天记录，不把 reply generation 和 send 混在一起。

T131 完成后，架构新增 `ReplyPlanner` 作为 review-only 组装层：它从 compact `ChatContext` 生成 T130 `ReplyPlan`，并显式校验 `priority_rank` 与 `contact_id` 对齐。当前仍是 deterministic heuristic baseline；T132 需要把 policy/boundary 风险作为独立控制层补上，而不是把自动发送或实时平台接入并入 planner。

T132 完成后，架构新增 `ReplyPlanPolicyEngine` 作为 planner 内部的 policy/boundary 分类层：它只做检测、风险标记、边界提醒和 confidence penalty，不做发送、不做持久化、不读取私密原文目录。该层仍是 keyword heuristic，T133 需要用匿名 holdout 验证是否足以作为 M3 gate 输入。
