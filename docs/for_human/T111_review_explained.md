# T111 Review Explained — Distillation Schemas

## 1. 这个 Task 在做什么？通俗解释

### 背景

在 T110 中，我们把聊天消息按时间间隔、联系人变化等规则切成了一个个"对话块"（chunk）。现在有了 chunk，下一步（T112）就是让 AI 来分析每个 chunk，从中提取摘要和记忆事实。

但这里有一个关键问题：**AI 的输出是不可控的。** 如果没有提前定好严格的格式规则，AI 可能会：
- 输出没有根据的"事实"（幻觉）
- 给出过度亲密的人格判断
- 做出无法追溯到原始消息的结论
- 甚至生成可以用来冒充联系人的信息

### T111 的核心目标

**T111 就是给后续所有 AI 分析步骤定规矩——在 AI 开始工作之前，先把输出格式用代码和文档固定下来。**

具体来说，T111 定义了三种"输出模板"：

1. **ChunkSummary（对话块摘要）**：对一个 chunk 的客观总结。比如"这段对话主要聊了最近的工作安排"，而不是"对方是一个很努力的人"。

2. **MemoryFactCandidate（记忆事实候选）**：从对话中提取的原子化事实。比如"对方提到最近在准备面试"，而不是"对方是一个焦虑的人"。每条事实必须能追溯到原始消息。

3. **ContactSkillCandidate（联系人沟通技能候选）**：关于"如何与此人沟通"的策略总结。比如"对方喜欢简短直接的回复风格"，而不是"对方的人格类型是 XXX"。

**"候选"（Candidate）** 这个词很重要——所有产物在通过人工审阅之前，都不能被视为可信的。

### 关键约束

- 每条结论必须有 **evidence_refs**（证据引用）：能追溯到具体的消息或对话块。
- 每条结论必须有 **confidence**（置信度）：AI 对这条结论有多确信，0 到 1 的分数。
- 每条结论必须有 **sensitivity**（敏感度）：这条结论涉及隐私的程度。
- 每条结论必须有 **status**（状态）：默认是"候选"，必须人工审阅后才能变成"已批准"。
- **ContactSkillCandidate 明确禁止被用来冒充或模拟联系人**——它只是帮助用户更好沟通的辅助工具，不是数字克隆。

## 2. 实现详解

### 2.1 任务目标

在 T112 的 LLM/JSON 抽取管线启动前，定义 `ChunkSummary`、`MemoryFactCandidate`、`ContactSkillCandidate` 的 Pydantic schema 和 JSON contract，确保所有蒸馏产物有强格式约束。

### 2.2 任务流程

```
T110 产物: chunks.jsonl（对话块）
       ↓
T111（本任务）: 定义严格的输出格式规则
       ↓ 固定了 schema 和 contract
T112（下一步）: AI 分析每个 chunk，生成摘要和事实
       ↓ 输出必须符合 T111 定义的格式
T113: 基于摘要和事实构建联系人沟通技能
       ↓
T114: 在真实样本上运行并人工抽查
```

### 2.3 代码变化

#### 修改文件：`core/models.py`

新增了 4 个类型别名和 13 个 Pydantic 模型。

**类型别名**（第 31-34 行）：用 Python 的 `Literal` 类型定义了受限的字符串值集合，防止下游代码使用不在约定范围内的值。

| 类型别名 | 允许值 | 用途 |
| --- | --- | --- |
| `DistillationStatus` | candidate / approved / rejected / frozen / archived | 所有蒸馏产物的生命周期状态 |
| `DistillationSensitivity` | low / medium / high | 所有蒸馏产物的隐私敏感度 |
| `DistillationMemoryType` | semantic / episodic / relationship / procedural / reflection | 记忆事实的五种类型 |
| `ContactRelationshipType` | friend / classmate / colleague / family / unknown | 联系人关系类别 |

**核心模型层次**：

```
DistillationClaim（基础断言）
├── ChunkSummaryObservation（chunk 级沟通观察）
├── ContactSkillTopicPreference（话题偏好断言）
├── ContactSkillPattern（行为模式断言）
└── ContactSkillImportantEvent（重要事件断言）

ChunkSummary（对话块摘要）
MemoryFactCandidate（记忆事实候选）

ContactSkillCandidate（联系人沟通技能候选）
├── ContactSkillRelationshipState（关系状态）
├── ContactSkillCommunicationStyle（沟通风格）
├── ContactSkillUserSidePreferences（用户侧偏好）
├── ContactSkillReplyStrategy（回复策略）
├── ContactSkillUsageBoundary（用途边界）
└── 以上 4 种 DistillationClaim 子类（偏好/模式/事件）
```

**关键设计决策**：

1. **`DistillationClaim` 作为基类**：所有"原子断言"（claim）都继承它，自动获得 `claim`、`evidence_refs`（至少 1 条）、`confidence`（0-1）、`sensitivity`、`status`、`rationale`。这避免了在每个子结构中重复定义这些字段。

2. **`evidence_refs` 强制非空**：用 `Field(..., min_length=1)` 确保每个断言至少有一条证据引用。这意味着 AI 输出如果没附带证据，Pydantic 校验会直接拒绝——不可能出现"无证据的结论"。

3. **`ContactSkillUsageBoundary`**：这是一个专门的安全守卫模型，默认值就明确禁止了三种用途：
   - `persona_clone`（人格克隆）
   - `impersonation`（冒充）
   - `autonomous_contact_simulation`（自动模拟联系人）
   
   同时默认只允许三种用途：`reply_assistance`（回复辅助）、`context_retrieval`（上下文检索）、`human_review`（人工审阅）。

4. **不继承 vs 继承的选择**：`ChunkSummary`、`MemoryFactCandidate`、`ContactSkillCandidate` 不继承 `DistillationClaim`，而是独立组合相同的字段。这是因为它们是"复合结构"，不是单条断言——继承会引入语义上的不恰当。

#### 新增文件：`distillation_output_contract.md`

这是一个完整的 JSON contract 文档，包含：

- **状态约定**（第 1 节）：定义了 5 种 status 和 3 种 sensitivity 的含义
- **ChunkSummary JSON 形状**（第 2 节）：含完整 JSON 示例和字段约束表
- **MemoryFactCandidate JSON 形状**（第 3 节）：含 3 条规则（claim 必须可审计、evidence_refs 不能为空、单次现象不直接升格为稳定结论）
- **ContactSkillCandidate JSON 形状**（第 4 节）：含完整 JSON 示例和字段约束表
- **Anti-Impersonation 边界**（第 5 节）：4 条硬边界 + 一句话原则
- **T112/T113 接口约束**（第 6 节）：明确下游任务必须遵守的规则

#### 修改文件：`07_handoff.md`

- 状态更新为"worker draft 已完成，待 reviewer 审查"
- 新增第 8 节 T111 worker draft 记录
- 章节编号顺延

### 2.4 对后续开发的意义

**T111 产出的 schema 是 T112-T114 所有蒸馏步骤的"格式闸门"：**

- **T112（摘要与事实抽取）**：LLM 的输出必须能被这些 Pydantic model 校验通过。如果 AI 输出没有 evidence_refs、confidence 超出 0-1 范围、或者 status 不在 5 种候选值中，校验会直接失败。这从技术上防止了"无证据结论"进入系统。

- **T113（ContactSkill 构建）**：只能消费通过 schema 校验的 `ChunkSummary` 和 `MemoryFactCandidate`。review artifact 必须展示 evidence_refs 和 usage_boundary。approve 前的 skill 不能进入 reply planner。

- **T114（样本运行）**：人工抽查时可以直接检查每个字段的值是否合理——evidence_refs 是否指向真实消息、confidence 是否与证据强度匹配、sensitivity 是否合适。

- **T120（Store 与证据校验）**：需要处理 `MemoryFactCandidate.approved` → 现有 `MemoryFact` 的映射，以及 `DistillationMemoryType`（5 种字面值）与现有 `MemoryType` 枚举的对应。

**对项目整体架构的影响**：

1. **可审计性**：每条结论都有 evidence_refs，可以追溯到具体的消息或 chunk。这是整个项目的核心原则——"所有事实、偏好、关系判断都必须有 evidence_refs"。

2. **安全性**：ContactSkillUsageBoundary 从模型层面阻止了 persona clone / impersonation 的技术可能性。即使代码有 bug，模型默认值也不允许这些用途。

3. **渐进信任**：status 字段实现了从 candidate → approved 的渐进式信任链。所有产物默认是 candidate，只有人工审阅后才能变成 approved。rejected/frozen/archived 提供了完整的生命周期管理。

## 3. 为什么给出 PASS 的 review 结果

### Review 总体判断

**Verdict: PASS** — 任务完整完成，没有阻塞性问题。

### 通过的核心原因

1. **任务要求全部满足**：
   - `ChunkSummary`、`MemoryFactCandidate`、`ContactSkillCandidate` 三个核心 schema 已定义
   - 所有 schema 包含 `evidence_refs`（强制非空）、`confidence`（0-1 范围）、`sensitivity`（3 级）、`status`（5 种）
   - `ContactSkillCandidate` 通过 `ContactSkillUsageBoundary` 明确禁止了 persona clone / impersonation

2. **与实验计划完全对齐**：
   - `MemoryFactCandidate` 与实验计划 6.3 节 Memory Fact schema 的每个字段一一对应
   - `ContactSkillCandidate` 与实验计划 6.4 节 ContactSkill schema 的每个字段一一对应
   - 新增字段（`usage_boundary`、`source_chunk_ids` 等）都有合理依据

3. **schema 设计质量高**：
   - `DistillationClaim` 基类避免了 claim 字段的重复定义
   - 继承关系合理（只有原子断言继承基类，复合结构独立组合）
   - Pydantic 的 `Field` 约束（`min_length=1`、`ge=0.0`、`le=1.0`）提供了运行时校验

4. **anti-impersonation 边界到位**：
   - 代码层面：`ContactSkillUsageBoundary.disallowed_uses` 默认禁止三种用途
   - 文档层面：`distillation_output_contract.md` 第 5 节 4 条硬边界 + 一句话原则
   - 双重约束，既防代码误用，也防文档理解偏差

5. **零越界行为**：
   - 没有调用 LLM、没有生成真实蒸馏结果、没有写数据库 migration
   - 没有读取或输出 `private/` 中的任何内容
   - 没有修改任何已有 model（新增 model 插入在 `MemoryFact` 和 `MemoryProfileFacet` 之间）

6. **回归风险极低**：
   - 新增 model 未被任何 service 或 CLI 引用（grep 确认）
   - 不影响 `ChatContext.model_rebuild()` 等前向引用链
   - 唯一的新 import 是 `Literal` from `typing`

### 提出的 5 个非阻塞性问题

这些问题不阻碍 T111 通过，但值得后续关注：

1. **沟通风格的字符串字段未约束**（N01）：`message_length`、`tone` 等字段目前是自由字符串，实验计划建议了受限值。但在 MVP 阶段，给 LLM 留一些灵活度是合理的——AI 输出的枚举值可能不完全匹配预设。后续可以收紧。

2. **`redaction_policy` 用字典而非结构化 model**（N02）：当前用 `dict[str, Any]` 存储脱敏策略，失去了 Pydantic 校验。但功能上不影响，后续可以改为独立 model。

3. **蒸馏管线与在线运行时的类型系统不统一**（N03）：`DistillationMemoryType`（5 种字面值）与 `MemoryType`（现有枚举）不完全对应。当前分离避免了跨模块耦合，但 T120 需要处理映射。

4. **新 schema 没有时间戳**（N04）：与现有 `MemoryFact` 不同，新 schema 没有 `created_at`/`updated_at`。对离线批处理来说可以接受（文件写入时间可替代），T120 store 可能需要补上。

5. **没有 Pydantic 校验测试**（N05）：`evidence_refs` 非空约束和范围约束没有测试覆盖。留给 T150。

### 与之前 review 的一致性

- T110 review 的 N01（`chunking_reason` 语义）和 N05（`topic_hint` 缺失）在 T111 的 schema 中得到了呼应——`ChunkSummary` 有 `topics` 字段（T112 可填充），`chunking_reason` 从 chunk 原样继承。
- T103 Conditional 条件中的"T112+ 必须遵守 T101 隐私边界"在 `distillation_output_contract.md` 第 6 节 T112 接口约束中得到了明确："不得把私密原文复制进可提交目录的示例或日志"。
- 整体而言，T111 在 T112 之前建立了一个坚实的格式闸门，从技术上防止了无证据结论、幻觉和不安全用途进入系统。
