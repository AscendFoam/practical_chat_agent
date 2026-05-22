# T170 Review Explained — ContactSkill Decomposition Design

## 1. 这个任务在做什么（通俗解释）

想象你有一个巨大的档案夹，里面装着关于某个联系人的所有信息：关系状态、沟通风格、怎么回复对方、哪些话题不能碰……这就是当前的 `ContactSkill`。

问题是，不同场景只需要这个档案夹的一部分内容：

- 写回复草稿时，主要看"怎么回复"和"哪些不能说"。
- 检查安全边界时，主要看"哪些不能说"和"这个人的关系状态"。
- 理解对方是谁时，主要看"关系类型"和"沟通风格"。

但现在不管什么场景，都要把整个档案夹搬过来。这不仅效率低，还导致：

- 修改某个部分的逻辑时，可能意外影响其他部分。
- 证据（evidence refs）归属不清晰——所有证据都堆在一起，分不清哪条证据支持哪个判断。

T170 要做的就是**设计**（只写文档，不写代码）如何把这个大档案夹拆成几个更小、更聚焦的"简报"（brief），同时**保证原有的档案夹完全不受影响**——它仍然存在、仍然可用、仍然是被审批通过的权威来源。

## 2. 实现细节

### 任务目标

设计三个"派生简报"（derived brief），每个聚焦一个方面：

| 简报 | 聚焦点 | 通俗理解 |
|---|---|---|
| `PartnerPersonaBrief` | 对方是谁、关系如何、怎么沟通 | "这个人是什么样的" |
| `CommunicationPolicyBrief` | 怎么回复对方 | "我该怎么说话" |
| `BoundaryProfileBrief` | 哪些话题要避免、哪些是底线 | "什么不能说" |

### 任务流程

1. 分析当前 `ContactSkill` 的痛点（4 类职责混杂、消费者无法按需取用、证据归属模糊）。
2. 定义三个派生简报的字段和职责。
3. 制作字段归属表——把 ContactSkill 的 20+ 字段逐一映射到对应的简报或保留在原始档案中。
4. 设计回退策略——如果派生简报不存在，仍然可以用现有的 `ApprovedContactSkillBrief`。
5. 设计证据保留规则——每个简报只携带自己领域的证据，跨领域证据留在原始档案。
6. 设计审批边界——简报不独立审批，继承原始 ContactSkill 的审批状态。
7. 规划三阶段迁移路径（全部是加法，不做减法）。

### 文件变化

| 文件 | 变化类型 | 内容 |
|---|---|---|
| `docs/architecture/contactskill_decomposition.md` | 新建 | 完整的分解设计文档（12 个章节，约 220 行） |
| `docs/07_handoff.md` | 修改 | 新增 Section 68（T170 Implementation Record），将原 Section 68 Kickoff Notes 后移为 Section 69 |

**没有修改任何代码文件。** `src/` 和 `tests/` 目录没有任何变化。

### 对后续开发的意义

这个设计文档是 M6 里程碑（ContactSkill-Compatible Decomposition）的地基。它解锁了四个后续任务：

- **T171**：定义 `PartnerPersonaBrief` 的 Pydantic 模型（纯 schema，不接入运行时）。
- **T172**：定义 `CommunicationPolicyBrief` 和 `BoundaryProfileBrief` 的 Pydantic 模型。
- **T173**：实现 `ContactSkillProjectionService`——从已审批的 ContactSkill 投射出派生简报。
- **T174**：在 `ChatContextAssembler` 中接入派生简报，让 ReplyPlanner 和 PolicyEngine 可以消费更结构化的上下文。

关键设计决策是"懒投射"（lazy projection）：简报不单独存储，而是在组装上下文时实时计算。这避免了新的存储格式和新的审批流程。

这个设计还与之前的 M5 管线（T160-T164 PreferencePatch）衔接：已审批的偏好补丁（approved patch hints）被归入 `CommunicationPolicyBrief`，作为回复策略的补充信号。

### 与项目整体路线的关系

从 `docs/04_task_board.md` 可以看到，项目当前处于 M5 完成后、M6 开始的阶段。M5 完成了"反馈到补丁"管线（从用户反馈中提取可审阅的偏好补丁）。M6 是在不破坏已有管线的前提下，让 ContactSkill 的结构更清晰，为后续 M7（LLM 辅助回复）和 M8（多轴关系状态）铺路。

`docs/08_risks_and_open_questions.md` 中的 R040（ContactSkill decomposition 可能被误执行成 breaking replacement）正是这个任务要防范的风险。T170 的设计通过"projection, not replacement"原则和显式的 fallback 策略来应对这个风险。

## 3. 为什么给出了 PASS 的 review 结果

### 任务完成度

T170 的任务要求列出了 8 项设计要素（痛点分析、派生简报集、字段归属表、回退策略、证据规则、兼容阶段、非目标、人格冒充边界），全部覆盖：

1. Section 2 覆盖痛点分析。
2. Section 3 定义了三个派生简报及各自职责。
3. Section 4 提供了 20+ 字段的归属表。
4. Section 5 设计了四级回退策略（简报 → 部分简报 → fallback aggregate → 兜底）。
5. Sections 6-7 定义了证据保留和审批边界规则。
6. Section 8 规划了三阶段 additive 路径。
7. Section 10 列出了 8 条显式非目标。
8. Section 11 声明了人格冒充/冒充/自主联系边界不变。

### 验证标准全部通过

| 验证项 | 结果 |
|---|---|
| 引用 T120-T123 | Section 9 专门章节 |
| 引用 T130-T133 | Section 9 专门章节 |
| 引用 T160-T164 | Section 9 专门章节 + `approved_patch_hints` 字段 |
| 已有数据保持可运行 | Section 1 + Section 5 明确声明 |
| 分解是投射/加法 | 多处明确声明（Section 1, 5, 8, 10） |
| Handoff 更新 | Section 68 记录完整 |
| 只改 Allowed files | 仅 `docs/architecture/` 和 `docs/07_handoff.md` |
| 未改代码 | 确认无 `src/` 变更 |
| 未声明 deprecated | 确认无 deprecation 声明 |

### 没有伪实现、mock、stub 或 hardcode

T170 是纯设计任务，不涉及代码实现。文档中的所有内容都是设计描述和架构分析，没有需要验证的运行行为。

### 没有破坏已有功能

没有任何代码被修改。`ContactSkill` 的存储、审批、运行时路径完全不受影响。

### 没有过度工程

设计保持在最小必要范围：

- 只定义了 3 个简报（不是 5 个或 10 个）。
- 简报是懒投射（不引入新存储格式）。
- 不独立审批（继承父记录状态）。
- 没有引入 LLM、平台集成、向量数据库等超出任务范围的内容。

### 没有把计划写成事实

文档通篇使用设计性语言（"proposed", "would", "may"），不声称已完成实现。Handoff Section 68 也清楚标注了这是一个 design record。

### 几个非阻塞性观察

这些不足以影响 PASS 判定，但值得后续任务注意：

1. `sensitivity_summary` 的聚合规则（取各区域最大值还是继承父级）在 T171 定义 schema 时需明确。
2. `communication_style_snapshot` 用 `dict[str, str]` 是否足够类型安全，T171 可评估是否改为结构化模型。
3. `important_event_summaries` 放在 `BoundaryProfileBrief` 而非 `PartnerPersonaBrief`，是一个可讨论的设计选择。
4. `PartnerPersonaBrief` 与 M8 的 `RelationshipState` 存在字段重叠，设计文档已正确标注为延迟到 M8 解决。

## 4. 关于 Worker 自述的验证

Worker 提供的自验证结果与实际文件内容一致：

- "引用 T120-T123 5 处" — 实际确认 Section 9 有专门段落 + Field Ownership Table 中引用。
- "引用 T130-T133 2 处" — 实际确认 Section 9 有专门段落。
- "引用 T160-T164 5 处" — 实际确认 Section 9 有专门段落 + `approved_patch_hints` 字段引用。
- "已有 approved 数据保持可运行" — 实际确认 Section 5 明确声明。
- "分解是 projection/addition" — 实际确认多处声明。
- "Handoff 已更新" — 实际确认 Section 68 存在且内容完整。
- "只改 Allowed files" — 实际确认无其他文件变更。
- "未改代码" — 实际确认 `src/` 无变更。
- "未声明 deprecated" — 实际确认无 deprecation/replacement 声明。

Worker 自述的剩余风险也与设计文档 Section 12 一致：PartnerPersonaBrief 与 M8 RelationshipState 重叠、Lazy vs. materialized briefs、Cross-contact briefs 均已正确标注为延迟问题。

无补充或纠正。
