# T130 Review Explained: ReplyPlan Schema

## 一、通俗解释：T130 在做什么？

想象你有一个智能助手，帮你"想想要怎么回复朋友的消息"。

T130 做的事情很简单：**给这个"回复规划"设计一张标准表格**。

这张表格长什么样？它规定：
- 一次规划至少要给出 **3 个不同的回复选项**（比如保守的、中等的、稍微热情一点的）。
- 每个选项都要说清楚：
  - 回复的文本是什么
  - 为什么建议这样回
  - 这条建议参考了哪些之前审批过的人际关系资料
  - 有什么风险需要注意
  - 有什么边界提醒（比如"不要显得太亲密"）
- 整张表格还要附带元信息：是跟谁回复、参考了哪些上下文、整体的政策边界是什么、这几个选项之间有什么区别。

**关键点：T130 只设计表格，不填表。** 它不调用 AI、不生成回复、不发送消息。它只是在代码里定义好了数据结构，让后面的任务（T131）有地方放生成的结果。

打个比方：T130 相当于设计了一张"处方笺模板"，T131 才是真正写处方的医生。

## 二、实现详解

### 2.1 任务目标

T130 的正式目标是：定义 `ReplyPlan` schema（数据结构）和 prompt contract（使用契约），用于表达多候选回复草稿、推荐理由、边界检查和引用证据。

它属于 **Milestone 3: 联系人感知 Reply Planner** 的第一个任务（T130），在 T123（将审批过的记忆/技能接入 ChatContext）之后。

### 2.2 任务流程

T130 的流程很直接，因为它是一个"定义数据结构"的任务：

1. **阅读 T123 的成果**：理解 `ChatContext` 中的 `ApprovedStoreContext` 结构，确保新 schema 能消费 T123 的 compact brief。
2. **设计 Pydantic 模型**：在 `core/models.py` 中新增 4 个模型类和 2 个 Literal 类型。
3. **编写使用契约文档**：创建 `docs/data_contracts/reply_plan_contract.md`。
4. **编译验证**：确保新代码不破坏已有模型。
5. **合成样例验证**：用虚构数据测试 `ReplyPlan` 是否能承载 3 个候选。

### 2.3 代码变化

#### `src/practical_chat_agent/core/models.py`

新增了以下内容：

**2 个 Literal 类型**（行 44-52）：

```python
ReplyPlanMode = Literal["candidate_review_only"]
ReplyPlanContextRefType = Literal[
    "approved_contact_skill_record",
    "approved_memory_fact_record",
    "approved_store_evidence_ref",
    "recent_event",
    "memory_hit",
    "policy_boundary",
]
```

- `ReplyPlanMode`：当前只有 `"candidate_review_only"` 这一个模式，明确表达"仅供审阅"。
- `ReplyPlanContextRefType`：定义了候选回复可以引用哪些类型的证据来源，包括已审批的联系人技能、已审批的记忆事实、证据引用、最近事件、运行时记忆命中、策略边界。

**4 个 Pydantic 模型**（行 665-700）：

1. **`ReplyPlanContextRef`**：单个上下文引用，包含引用类型、引用 ID 和可选的说明。
2. **`ReplyPlanSourceContext`**：本次规划依赖的上下文来源，直接复用 T123 的 `ApprovedStoreContextStatus`，并携带 T123 的 compact ids。
3. **`ReplyPlanCandidate`**：单个候选回复，包含草稿文本、推荐理由、支持引用（至少1条）、风险标签、边界提醒（至少1条）和可选置信度。
4. **`ReplyPlan`**：整体回复规划，要求至少 3 个候选，并包含策略边界摘要和候选差异说明。

**关键设计决策**：

- `candidates` 的 `min_length=3` 确保至少有 3 个候选——这是任务包的硬性要求。
- `supporting_context_refs` 的 `min_length=1` 确保每个候选必须有引用依据，不允许"无中生有"的回复。
- `boundary_reminders` 的 `min_length=1` 确保每个候选必须带有边界提醒，防止规划者忘记安全约束。
- `approved_store_status` 直接复用 T123 的 `ApprovedStoreContextStatus` Literal 类型，保证了类型层面的兼容性。

#### `docs/data_contracts/reply_plan_contract.md`

新建了完整的 ReplyPlan 使用契约文档，包含 8 个章节：

1. **Usage Boundary**：明确 "review-first, not autonomous" 的原则。
2. **Compatibility With T123**：解释如何消费 T123 的 compact brief，不重新读取 store 文件。
3. **Schema Overview**：列出新增的模型和类型。
4. **JSON Shape**：给出完整的 JSON 示例（使用虚构数据，非真实聊天内容）。
5. **Field Semantics**：逐字段表格说明。
6. **Prompt Contract Expectations**：给 T131 的 LLM prompt 约束（不冒充、不无证据声称、不确定时保守）。
7. **Validation Expectations**：T130 的验证重点。
8. **Non-Goals**：明确声明本 contract 不负责什么。

#### `docs/07_handoff.md`

在末尾追加了 T130 Completion Record（Section 21），记录了改了什么、如何验证、剩余风险。

### 2.4 对后续开发的意义

T130 为整个 M3 里程碑打下了数据结构基础：

- **T131（ReplyPlanner 实现）**：将使用 `ReplyPlan` 作为输出格式，基于 T123 的 approved-store context 和 LLM 生成候选回复。T131 的 prompt 设计应遵循 Section 6 的 8 条规则。
- **T132（Policy/Boundary 校验）**：将检查 `ReplyPlan` 的 `policy_boundary_summary` 和 `boundary_reminders`，确保没有冒充、过度主动或越界内容。`ReplyPlanContextRefType` 中的 `"policy_boundary"` 就是为 T132 预留的引用类型。
- **T133（Holdout 评估）**：将用历史 holdout 场景验证候选回复的自然度和边界遵守程度。
- **M4 反馈闭环**：用户对候选的 accept/edit/reject 反馈将关联到 `ReplyPlanCandidate.candidate_id`，形成可追溯的偏好修正链路。

从项目整体看，T130 把 M2 的"已审批记忆/技能"连接到了 M3 的"回复生成"。它是从"理解关系"到"利用关系辅助回复"的关键桥梁——但桥梁只搭了结构，还没通车（T131 才是通车）。

## 三、为什么给出 PASS_WITH_WARNINGS 的 review 结果？

### 核心判断

**PASS（通过）的部分**：

1. **任务完成度**：T130 的所有硬性要求都满足了。schema 支持 3+ 候选、per-candidate 字段齐全、元信息完整、与 T123 兼容、prompt contract 覆盖了反冒充/保守处理/审阅优先等所有要求。
2. **无越界**：没有调用 LLM、没有生成回复逻辑、没有发送消息、没有接触数据库或原始聊天记录。改动严格限制在 schema 定义和文档。
3. **无伪实现**：所有 4 个 Pydantic 模型都是真实的数据结构，有完整的字段约束，不是空壳或 placeholder。
4. **隐私安全**：文档中的示例全部使用虚构数据（`contact_xxx`、`skillstore_001`），没有真实聊天内容、真实联系人姓名或平台 ID 泄露。
5. **不破坏现有功能**：所有已有模型（ChatContext、ApprovedStoreContext、ChatSuggestion 等）完全未被修改。
6. **文档诚实**：没有把计划写成事实，明确声明了"不负责真正调用 LLM"和"T130 只定义 contract"。

**WITH_WARNINGS（带警告）的原因**：

我记录了 4 个非阻塞性观察点，它们不影响当前任务的正确性，但值得后续任务注意：

1. **N01**：`ReplyPlanMode` 当前只有一个值 `"candidate_review_only"`。这本身不是问题，但如果未来需要新模式（如自动选择），需要扩展这个 Literal。当前无需行动。
2. **N02**：`priority_rank` 没有唯一性约束——理论上两个候选可以有相同的排序号。这是 Pydantic 的自然限制，T131 在生成时应确保分配唯一 rank。
3. **N03**：`approach_label` 是自由字符串，没有枚举约束。MVP 阶段可接受，后续可视情况收紧。
4. **N04**：`ReplyPlanSourceContext` 不携带 `contact_id`，这个信息在父级 `ReplyPlan` 上。理论上 source context 可以被错误地填充为不同联系人的数据。低风险，T131 在组装时应做一致性校验。

这些 warning 和之前 T111/T120/T121/T122/T123 的 review 模式一致——记录观察但不阻塞流程。按照项目治理惯例，由 Captain 决定每个 warning 是 accept、defer 还是要求后续修复。

### 总结

T130 干净利落地完成了 schema 定义工作。它做了该做的（定义结构、写契约文档），没做不该做的（调用 LLM、生成回复、碰隐私数据）。4 个 warning 都是面向未来的建模观察，不影响当前交付。给 PASS_WITH_WARNINGS 是因为这符合项目此前一贯的 review 标准（T120-T123 均为 PASS_WITH_WARNINGS），同时保留了对后续任务的提醒。
