# T190 Review Explained

## 1. 这个任务在做什么（通俗解释）

T190 要解决的问题是：**怎么用数据结构来描述你和某个联系人之间的关系状态？**

之前的系统已经有一个简单的 `ContactSkillRelationshipState`，它用几个标量（比如 `closeness: 0.5`, `trust_level: 0.5`）来描述关系。但这种方法有个明显的问题：关系是多维度的。你可能很信任一个人（trust 高），但最近发生了争执（conflict 高），同时你还不太熟悉对方的私生活（intimacy 低）。用一个数字是说不清楚的。

T190 的目标是设计一个**多维度的关系状态结构**，用 8 个独立的维度来描述关系，而不是把关系压缩成一个分数。同时，任何对关系状态的修改都必须经过人工审查——系统不会自动改变关系评估。

## 2. 实现详细解释

### 2.1 任务目标

在 `models.py` 中定义两个核心数据结构和一些辅助类型：

1. `RelationshipState`：关系状态快照，包含 8 个独立的维度
2. `RelationshipDeltaCandidate`：对关系状态提出的修改建议，必须经过人工审查

### 2.2 代码变化

**新增 3 个 Literal 类型**（定义了允许值的枚举）：

- `InteractionTemperature`：最近的互动温度（warm/neutral/cold/mixed/unknown）
- `RelationshipDeltaDirection`：变化方向（increase/decrease/stable/unknown）
- `RELATIONSHIP_DIMENSION_NAMES`：8 个维度名称

**新增 3 个 Pydantic 模型**：

1. `RelationshipState`（关系状态快照）：
   - 8 个独立的 float 维度（0.0-1.0）：熟悉度、信任、热情、互惠、冲突水平、边界风险、主动性容许度、亲密度
   - 不确定性指标
   - 必须有证据引用（`evidence_refs` 不能为空）
   - 默认状态是 `candidate`，需要人工审查后才能使用
   - `is_runtime_ready()` 只有在人工批准后才返回 true

2. `RelationshipDeltaDimension`（单个维度的变化）：
   - 记录哪个维度变了、当前值、建议值、变化方向和幅度

3. `RelationshipDeltaCandidate`（修改建议）：
   - 至少包含一个维度的变化
   - 必须有证据引用
   - 可以引用 T191 的信号记录
   - 同样默认是 candidate，需要人工审查

### 2.3 文档变化

- `docs/data_contracts/relationship_state_contract.md`（新文件）：完整记录了维度语义、字段定义、安全约束和与后续任务的兼容性
- `docs/07_handoff.md`：新增 T190 完成记录

### 2.4 对后续开发的意义

这个任务属于 M8（RelationshipState）里程碑的第一个任务。它为后续任务打下了数据结构基础：

- **T191**（信号提取器）：从反馈和批准的元数据中提取关系信号，产出可被 `signal_refs` 引用的记录
- **T192**（delta 候选生成）：基于 T191 的信号，创建 `RelationshipDeltaCandidate` 实例
- **T193**（审查 CLI）：让人工审查和批准/拒绝 delta 候选
- **T194**（紧凑上下文集成）：将批准的关系状态集成到回复生成的上下文中
- **T195**（关系感知评估）：评估多维度关系模型是否比简单的 `ContactSkillRelationshipState` 更好地改善回复质量

重要的是，这些新模型与现有的 `ContactSkillRelationshipState` 完全独立，不替换也不合并。旧的模型继续作为 `ContactSkillCandidate` 内部的兼容性回退。

## 3. 为什么给出这个 review 结果

**Verdict: PASS_WITH_WARNINGS**

**通过的理由**：

1. 任务目标完全达成：定义了多维度的 `RelationshipState` 和审查制的 `RelationshipDeltaCandidate`
2. 严格遵守了 Allowed Files 约束：只修改了 `models.py`、`docs/data_contracts/` 和 `docs/07_handoff.md`
3. 没有任何 Forbidden Scope 的越界：没有信号提取、没有审查 CLI、没有自动更新、没有发送/平台集成、没有单分数压缩
4. 没有伪实现、mock、stub 或 hardcoded 行为——都是纯粹的数据结构定义
5. 编译通过，441 个现有测试全部通过，没有回归
6. 证据约束（`evidence_refs` 不能为空）正确实施
7. `is_runtime_ready()` 的三重门控（status + reviewed_by_human + last_decision）与现有项目模式一致
8. 文档没有把计划写成事实——合约文档明确标注了哪些是 T190 的工作，哪些是后续任务

**Warnings 的原因**：

- `magnitude` 字段默认为 0.0 但不会自动从 current/proposed 值计算，可能产生内部不一致的数据（但 T192 会负责正确计算）
- `source_type` 没有包含 `"delta_approved"` 选项，但后续应用 delta 时可能需要这个类型
- 与项目一贯的模式一致，没有提交自动化测试（留给后续 regression-hardening 任务）

这些都是可以在后续任务中自然解决的细节，不阻塞当前任务的完成。
