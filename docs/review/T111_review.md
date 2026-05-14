# Review: T111 Distillation Schemas

Review date: 2026-05-14
Reviewer: Claude Code (adversarial)
Task package: `docs/tasks/M1_offline_distillation_mvp/T111_distillation_schemas.md`

## Scope

只读审查 worker 针对 T111 的所有产出，对照任务包的 Allowed files、Forbidden scope 和 Verification 要求。T111 是 schema 定义任务——在 T112 LLM/JSON 抽取管线启动前，为 `ChunkSummary`、`MemoryFactCandidate`、`ContactSkillCandidate` 固定字段边界、evidence_refs 约束和 anti-impersonation 边界。重点检查 schema 完整性、与实验计划数据合约的对齐、以及是否有越界行为。

## Diff Summary

所有变更均为未提交状态（working tree），落在以下文件：

| 文件 | 变化类型 | 是否在 Allowed files 内 |
| --- | --- | --- |
| `src/practical_chat_agent/core/models.py` | 修改 | 是 |
| `docs/data_contracts/distillation_output_contract.md` | 新增 | 是 |
| `docs/07_handoff.md` | 修改 | 是 |

零 `src/` 下非 Allowed files 变更。零 LLM 调用。零数据库 migration。零 `private/` 读取或输出泄露。

## Task Completion Check

| 任务包要求 | 状态 | 证据 |
| --- | --- | --- |
| 定义 `ChunkSummary` Pydantic schema | **完成** | `models.py:304-323` |
| 定义 `MemoryFactCandidate` Pydantic schema | **完成** | `models.py:326-338` |
| 定义 `ContactSkillCandidate` Pydantic schema | **完成** | `models.py:415-443` |
| Schema 包含 `evidence_refs` | **完成** | 所有 claim/skill 结构均用 `Field(..., min_length=1)` 强制非空 |
| Schema 包含 `confidence` | **完成** | 所有候选结构均有 `confidence: float = Field(..., ge=0.0, le=1.0)` |
| Schema 包含 `sensitivity` | **完成** | 受限字面值 `Literal["low", "medium", "high"]` |
| Schema 包含 `status` | **完成** | 受限字面值 `Literal["candidate", "approved", "rejected", "frozen", "archived"]` |
| `ContactSkillCandidate` 禁止 persona clone / impersonation | **完成** | `ContactSkillUsageBoundary.disallowed_uses` 默认包含 `"persona_clone"`、`"impersonation"`、`"autonomous_contact_simulation"` |
| JSON contract 文档 | **完成** | `distillation_output_contract.md` 覆盖全部三类 schema + 状态约定 + anti-impersonation 边界 |
| 更新 `docs/07_handoff.md` | **完成** | 新增 T111 worker draft 记录、状态更新 |
| 不调用 LLM | **完成** | 零 LLM/API 调用 |
| 不写数据库 migration | **完成** | 零 migration 代码 |

## Experiment Plan Alignment

逐项核对 `docs/02_experiment_plan.md` 6.3 节 Memory Fact schema 与 `MemoryFactCandidate` 的字段映射：

| 实验计划字段 | `MemoryFactCandidate` 字段 | 对齐 |
| --- | --- | --- |
| `memory_id` | `memory_id: str` | **对齐** |
| `memory_type` (5 种) | `memory_type: DistillationMemoryType` (相同 5 种) | **对齐** |
| `subject_id` | `subject_id: str` | **对齐** |
| `claim` | `claim: str` | **对齐** |
| `status` (5 种) | `status: DistillationStatus` (相同 5 种) | **对齐** |
| `confidence` | `confidence: float` (0-1) | **对齐** |
| `importance` | `importance: float` (0-1) | **对齐** |
| `sensitivity` (3 级) | `sensitivity: DistillationSensitivity` (相同 3 级) | **对齐** |
| `evidence_refs` | `evidence_refs: list[str]` (min_length=1) | **对齐且更严格** |
| `conflicts_with` | `conflicts_with: list[str]` | **对齐** |

逐项核对 `docs/02_experiment_plan.md` 6.4 节 ContactSkill schema 与 `ContactSkillCandidate` 的字段映射：

| 实验计划字段 | `ContactSkillCandidate` 字段 | 对齐 |
| --- | --- | --- |
| `schema_version` | `schema_version: str = "contact_skill_candidate_v1"` | **对齐** |
| `contact_id` | `contact_id: str` | **对齐** |
| `relationship_type` (5 种) | `relationship_type: ContactRelationshipType` (相同 5 种) | **对齐** |
| `relationship_state` (6 字段) | `ContactSkillRelationshipState` (6 字段 + evidence/confidence/sensitivity/status) | **对齐且增强** |
| `communication_style` (4 字段) | `ContactSkillCommunicationStyle` (4 字段 + evidence/confidence/sensitivity/status) | **对齐且增强** |
| `preferred_topics` | `list[ContactSkillTopicPreference]` | **对齐** |
| `avoid_topics` | `list[ContactSkillTopicPreference]` | **对齐** |
| `important_events` | `list[ContactSkillImportantEvent]` | **对齐** |
| `stable_preferences` | `list[ContactSkillPattern]` | **对齐** |
| `emotional_patterns` | `list[ContactSkillPattern]` | **对齐** |
| `user_side_preferences` | `ContactSkillUserSidePreferences` | **对齐** |
| `reply_strategy` (4 场景) | `ContactSkillReplyStrategy` (相同 4 场景) | **对齐** |
| `confidence` | `confidence: float` (0-1) | **对齐** |
| `evidence_refs` | `evidence_refs: list[str]` (min_length=1) | **对齐且更严格** |
| `status` | `status: DistillationStatus` | **对齐** |
| `redaction_policy` | `redaction_policy: dict[str, Any]` | **对齐** |

**新增超出实验计划的字段**：`source_chunk_ids`、`source_memory_ids`、`review_notes`、`usage_boundary`。这些是合理的增强——`usage_boundary` 满足任务包的 anti-impersonation 要求，`source_chunk_ids` / `source_memory_ids` 支持可审计追溯，`review_notes` 支持 T113 人工审阅。

**结论：与实验计划数据合约完全对齐，所有新增字段有合理依据。**

## Schema Design Quality

### 继承策略

`DistillationClaim` 作为原子断言的基类，提供 `claim` + `evidence_refs` + `confidence` + `sensitivity` + `status` + `rationale`。继承它的子类：

- `ChunkSummaryObservation` — chunk 级沟通观察
- `ContactSkillTopicPreference` — 话题偏好断言
- `ContactSkillPattern` — 行为模式断言
- `ContactSkillImportantEvent` — 重要事件断言

`ChunkSummary`、`MemoryFactCandidate`、`ContactSkillCandidate` 不继承 `DistillationClaim`，而是独立组合 `evidence_refs` / `confidence` / `sensitivity` / `status`。这避免了不恰当的继承（复合结构不是单条 claim），同时保持了字段命名和约束的一致性。

**设计合理，继承深度为 1，无过度抽象。**

### evidence_refs 强制非空

所有 claim 结构和 skill 的 `evidence_refs` 使用 `Field(..., min_length=1)` 强制至少一个引用。这意味着：

1. T112 的 LLM 输出如果没有附带 evidence_refs，Pydantic 校验会直接失败。
2. 任何无证据的 claim 都不可能通过 schema 校验进入下游。

**这是任务包核心要求的正确实现。**

### Anti-impersonation 边界

`ContactSkillUsageBoundary` 模型（第 392-412 行）：

- `allowed_uses` 默认值：`["reply_assistance", "context_retrieval", "human_review"]`
- `disallowed_uses` 默认值：`["persona_clone", "impersonation", "autonomous_contact_simulation"]`
- `notes` 明确声明 "must not be used to imitate, replace, or autonomously speak as the real contact"

`distillation_output_contract.md` 第 5 节进一步用 4 条硬边界 + 一句话原则强化。

代码和文档双重约束。**满足任务包对 anti-impersonation 的要求。**

## Relationship with Existing Models

### 与 `MemoryFact` 的关系

现有 `MemoryFact`（第 277-288 行）服务于在线 agent 运行时：`agent_id`、`user_id`、`MemoryType` 枚举、`scope`、`salience` 等。

新增 `MemoryFactCandidate` 服务于离线蒸馏管线：`subject_id`、`claim`、`DistillationMemoryType` 字面值、`importance`、`source_chunk_ids` 等。

两者职责不同、字段不同、不冲突。T120 可能需要处理 `MemoryFactCandidate.approved` → `MemoryFact` 的映射，但这是 T120 的 scope，不在 T111 范围内。

### 与 `core/enums.py` 的关系

新增的 `DistillationMemoryType` 是 `Literal` 类型别名，而现有 `MemoryType` 是 `core/enums.py` 中的 `StrEnum`。两者值集不同（蒸馏有 `reflection`，在线运行时有其他值）。

**这种分离是合理的**——蒸馏管线的类型系统暂时不需要与在线运行时的 enum 统一，避免了跨模块耦合。T120 可能需要映射，但 T111 不做映射是正确的。

### 与 `T110` chunks 的关系

`ChunkSummary` 的前 7 个字段（`chunk_id`、`contact_id`、`conversation_id`、`time_range`、`event_ids`、`message_count`、`chunking_reason`）直接映射 T110 输出的 chunk 字段。`source_message_type_codes`、`interaction_flags`、`risk_flags` 延续 T102/T110 的不确定性信号。

**与上游 chunk 格式对齐良好。**

## Pseudo-implementation / Mock / Stub / Hardcode Check

| 功能 | 是否真实实现 | 证据 |
| --- | --- | --- |
| Pydantic schema 定义 | 真实 | 13 个 `BaseModel` 子类 + 4 个 `Literal` 类型别名 |
| `evidence_refs` 非空约束 | 真实 | `Field(..., min_length=1)` |
| `confidence` 范围约束 | 真实 | `Field(..., ge=0.0, le=1.0)` |
| Anti-impersonation 边界 | 真实 | `ContactSkillUsageBoundary` 默认值 + contract 文档第 5 节 |
| 状态约定 | 真实 | `DistillationStatus` Literal 约束 5 种值 |
| 敏感度约定 | 真实 | `DistillationSensitivity` Literal 约束 3 种值 |

**结论：零伪实现、零 mock、零 stub。所有约束都是真实的 Pydantic 验证规则。**

## Missing Verification

Worker 已运行：
1. `python -m compileall src/practical_chat_agent/core/models.py` — 编译通过

对于纯 schema 定义任务，编译检查是必要的最小验证。Pydantic 模型的字段约束（`min_length`、`ge`、`le`）会在运行时自动校验，不需要额外代码。

补充建议（不阻碍通过）：可以在 T150 补充 Pydantic 校验测试——构造合法/非法 JSON，验证 `min_length=1` 和范围约束是否生效。

## Over-engineering Check

实现规模：

- `models.py` 新增约 155 行（13 个 model + 4 个 type alias + 1 行 import）
- `distillation_output_contract.md` 约 287 行（4 个主要章节 + JSON 示例 + 字段表）
- `07_handoff.md` 增量约 40 行

对于一个需要定义 3 个核心 schema + 10 个辅助子结构 + 完整 JSON contract 文档的任务，这个规模合理。`DistillationClaim` 基类避免了 claim 相关字段的重复定义。没有引入不必要的抽象层、没有引入外部依赖、没有定义运行时逻辑。

唯一可讨论的设计选择：`ContactSkillRelationshipState` 和 `ContactSkillCommunicationStyle` 的字符串字段（如 `message_length`、`tone`、`interaction_frequency`）使用自由字符串而非受限字面值。实验计划建议了受限值（如 `"short|medium|long|mixed"`），但 worker 选择自由字符串。这在 MVP 阶段是合理的——LLM 输出的枚举值可能不完全匹配预设，先留灵活度，后续可收紧。

## Regression Risk

| 检查项 | 结论 |
| --- | --- |
| 对已有 model 的影响 | **无风险** — 新增 model 插入在 `MemoryFact` 和 `MemoryProfileFacet` 之间，不修改任何已有 model |
| 新 import 的影响 | **极低风险** — 仅新增 `Literal` from `typing`，无副作用 |
| `ChatContext.model_rebuild()` | **无影响** — 新增 model 不参与 `ChatContext` 的前向引用链 |
| 对已有 service 的影响 | **无风险** — grep 确认新 model 未被任何 service 引用 |
| 对已有 CLI 的影响 | **无风险** — 无 CLI 代码变更 |

## Plans vs Facts Check

| 文档 | 结论 |
| --- | --- |
| `07_handoff.md` 状态 | "worker draft 已完成，待 reviewer 审查" — **合规** |
| `07_handoff.md` T111 记录 | 列出了所有新增 schema 名称、验证命令和 reviewer 关注点 — **合规** |
| `07_handoff.md` "不要提前标记 task 完成" | **合规** — `04_task_board.md` 未修改 |
| `distillation_output_contract.md` JSON 示例 | 使用脱敏占位符（`contact_xxx`、`evt_xxx`），无真实数据 — **合规** |

## Privacy Audit

`distillation_output_contract.md` 的 JSON 示例全部使用脱敏占位符（`chk_xxx`、`contact_xxx`、`evt_xxx`）。无真实聊天原文、真实联系人姓名或真实文件名。`models.py` 的 schema 定义是纯结构描述，不含任何数据。

**零隐私泄露。**

## Blocking Issues

无。

## Non-blocking Issues

1. **N01 — `ContactSkillRelationshipState` 和 `ContactSkillCommunicationStyle` 字符串字段未约束**：`message_length`、`tone`、`interaction_frequency` 等字段使用自由字符串，而实验计划 6.4 建议了受限值（如 `"short|medium|long|mixed"`）。MVP 阶段自由字符串可接受（LLM 输出值可能不完全匹配），但后续可收紧为 `Literal`。**严重度：低。**

2. **N02 — `redaction_policy` 使用 `dict[str, Any]` 而非结构化 model**：当前用字典存储 `store_raw_quotes`、`max_quote_length` 等策略，失去了 Pydantic 的字段级校验。建议后续定义为独立 `BaseModel`。**严重度：低。**

3. **N03 — `DistillationMemoryType` 与现有 `MemoryType` enum 值集不统一**：蒸馏管线的 5 种类型（`semantic|episodic|relationship|procedural|reflection`）与在线运行时 `MemoryType` 枚举不完全对应。T120 需要处理从 `MemoryFactCandidate` 到 `MemoryFact` 的映射。当前分离是合理的，但需要明确跟踪。**严重度：低，T120 负责。**

4. **N04 — 新 schema 无 `created_at` / `updated_at` 时间戳**：与现有 `MemoryFact`（有 `created_at` + `updated_at`）不同，新 schema 没有时间字段。对于离线批处理产物，时间戳可由文件写入时间替代，但 T120 store 可能需要补上。**严重度：低。**

5. **N05 — 无自动化 Pydantic 校验测试**：`evidence_refs` 的 `min_length=1` 约束、`confidence` 的范围约束等没有测试覆盖。T150 应补充。**严重度：低，已知 deferred。**

## Suspicious Implementation Details

无。所有实现逻辑清晰、约束正确、无安全漏洞。

## Verdict

**PASS**

Worker 完整完成了 T111 任务包的所有要求：

1. 在 `core/models.py` 定义了 `ChunkSummary`、`MemoryFactCandidate`、`ContactSkillCandidate` 及 10 个辅助子结构。
2. 所有 fact/claim/skill 结构强制 `evidence_refs` 非空（`min_length=1`），包含 `confidence`（0-1 范围）、`sensitivity`（3 级字面值）、`status`（5 种候选状态）。
3. `ContactSkillCandidate` 通过 `ContactSkillUsageBoundary` 明确禁止 `persona_clone`、`impersonation`、`autonomous_contact_simulation`。
4. `distillation_output_contract.md` 固定了 JSON contract、状态约定、敏感度约定和 anti-impersonation 边界。
5. 与实验计划 6.3/6.4 数据合约完全对齐，新增字段（`usage_boundary`、`source_chunk_ids`、`source_memory_ids`、`review_notes`）有合理依据。
6. 零 LLM 调用、零数据库 migration、零 `private/` 泄露。
7. 新增 schema 不修改任何已有 model，回归风险极低。
8. 文档状态准确，未把计划写成已完成事实。

5 个 non-blocking issues 均不阻碍 T111 通过，可在后续任务中处理。

## Recommended Next Action

1. Captain 将 T111 在 `04_task_board.md` 标记为完成。
2. 推进 T112（chunk summary 与 fact extraction 的 LLM/JSON 校验管线）。
3. T112 必须遵守 `distillation_output_contract.md` 第 6 节的接口约束：
   - LLM 输出必须能校验为上述 schema
   - 缺失 `evidence_refs`/`confidence`/`sensitivity`/`status` 的输出视为无效
   - 不得把私密原文复制进可提交目录
4. T150 补充 Pydantic 校验测试（构造合法/非法 JSON 验证约束生效）。
5. T120 注意 N03（`DistillationMemoryType` 与 `MemoryType` 的映射）和 N04（时间戳补充）。
