# T191 Review Explained

## 1. 这个任务在做什么（通俗解释）

T191 要解决的问题是：**怎么从用户的反馈中提取出"关系信号"？**

想象一下这样的场景：你使用聊天助手生成了一条回复草稿，你看完觉得"这条回复太热情了，不符合我和这个联系人的关系距离"，于是你标记了一个"太热情"（too_eager）的边界反馈。这个反馈本身就包含了一个关于你们关系的重要信号——你在这个关系中不太希望主动过头。

T191 做的事情就是：设计一个**保守的、确定性的提取器**，从这类边界反馈中自动提取出"关系信号"（RelationshipSignal）。每个信号只描述一个关系维度的一个方向变化，比如"边界风险应该增加"或"主动性容许度应该降低"。

为什么需要这一层？因为 T190 定义的关系状态模型是多维度的，不能随便修改——任何修改都需要经过人工审查。而信号就是一个中间产物：它是"观察到的证据"，不是"状态的改变"。T192 后续会把这些信号汇总成正式的状态修改提案（delta candidate），再交给 T193 的人工审查流程。

## 2. 实现详细解释

### 2.1 任务目标

在 T190 的基础上，实现：
1. 一个 `RelationshipSignal` 数据模型——描述单个关系维度的单个观察
2. 一个 `RelationshipSignalExtractor` 服务——从反馈日志中提取信号
3. 覆盖正常和边界情况的自动化测试
4. 更新合约文档

### 2.2 代码变化

**`src/practical_chat_agent/core/models.py`** 新增 2 个类型：

1. `RelationshipSignalProvenance` = Literal["feedback_boundary", "feedback_action", "metadata_derived", "unknown"]
   - 描述信号是怎么产生的。目前只用 `feedback_boundary`（来自边界反馈），其余留给未来任务。

2. `RelationshipSignal`（Pydantic 模型）：
   - 每个信号针对**一个**关系维度（如 `boundary_risk`）
   - 有方向（increase/decrease/stable/unknown）和强度（0.0-1.0）
   - 必须有 `evidence_refs`（不能为空，指向源反馈记录的 `feedback_id`）
   - 默认状态是 `candidate`，需要人工审查后才可用
   - `is_runtime_ready()` 在人工批准后才返回 true
   - 不存储任何原始文本（不存反馈原文、编辑文本、用户备注或边界备注）

**`src/practical_chat_agent/services/feedback.py`** 新增 `RelationshipSignalExtractor` 类：

- 核心方法是 `extract_from_feedback(feedback_log, valid_record_ids=None)`
- 使用静态规则表 `_BOUNDARY_RULES`，规则如下：

| 边界标签 | 产生的信号维度 | 方向 | 强度 |
| --- | --- | --- | --- |
| `boundary_violation` | `boundary_risk` | 增加 | 0.7 |
| `too_intimate` | `boundary_risk` | 增加 | 0.5 |
| `too_intimate` | `intimacy_level` | 降低 | 0.4 |
| `too_eager` | `initiative_allowance` | 降低 | 0.5 |

- 只处理 `action="boundary"` 且有 `boundary_label` 的反馈记录
- 未知标签、非边界操作（accept/reject/edit）、无标签的边界反馈 → 不产生任何信号
- 可以传入 `valid_record_ids` 集合来过滤只处理特定记录
- 产出的信号中，`signal_description` 使用规则表中的固定描述文本，不使用用户的原始输入

**`tests/test_relationship_signals.py`** 新增 21 个测试，覆盖：

- 正面情况：3 种已知边界标签各产生正确信号
- 反面情况：accept/reject/edit/无标签/未知标签/空日志 → 不产生信号（6 个测试）
- 证据引用：验证 `evidence_refs` 包含源 `feedback_id`
- 记录过滤：`valid_record_ids` 过滤行为
- 隐私安全：不包含原始私密文本
- 多联系人：不同联系人的反馈产生正确的 `contact_id`
- 模型验证：空 evidence_refs、无效维度、越界强度值都被拒绝

### 2.3 文档变化

- `docs/data_contracts/relationship_state_contract.md`：新增 "RelationshipSignal (T191)" 部分，记录信号与状态/增量的区别、提取规则表、字段定义、安全约束。
- `docs/07_handoff.md`：新增 T191 Worker Completion Record。

### 2.4 对后续开发的意义

T191 是 M8 里程碑的第二个任务（T190 之后），它建立了**信号层**——从反馈到状态变更之间的中间产物。

后续任务的依赖关系：

- **T192**（delta 候选生成）：消费 T191 的信号，把多个信号聚合成 `RelationshipDeltaCandidate`（状态修改提案），用 `signal_refs` 引用信号 ID
- **T193**（审查 CLI）：让人工审查和批准/拒绝 delta 候选
- **T194**（紧凑上下文集成）：将批准后的关系状态集成到回复生成的上下文中
- **T195**（关系感知评估）：评估多维度关系模型是否比旧的 `ContactSkillRelationshipState` 更好

值得注意的是，当前提取器只覆盖了 8 个维度中的 3 个（`boundary_risk`、`intimacy_level`、`initiative_allowance`）。另外 5 个维度（熟悉度、信任、热情、互惠、冲突水平）没有对应的提取规则，因为从当前的边界反馈标签无法直接推断。这意味着信号在初期会比较稀疏，但这正是"宁可漏掉也不要过度推断"的保守设计意图。

## 3. 为什么给出这个 review 结果

**Verdict: PASS_WITH_WARNINGS**

**通过的理由**：

1. 任务目标完全达成：实现了保守的信号提取器，从边界反馈中提取证据支持的关系信号
2. 严格遵守了 Allowed Files 约束：只修改了 `models.py`、`feedback.py`、`relationship_state_contract.md`、`tests/test_relationship_signals.py` 和 `07_handoff.md`
3. 没有任何 Forbidden Scope 的越界：没有读取原始聊天记录、没有修改关系状态、没有生成 delta candidate、没有 LLM 调用、没有发送/平台集成、没有把维度压缩成单分数
4. 没有伪实现、mock、stub 或 hardcoded 行为——提取器使用确定性的规则表，不依赖任何外部服务
5. 编译通过，21 个新测试全部通过，441 个现有测试全部通过，没有回归
6. 证据约束正确实施：每个信号都有 `evidence_refs` 指向源反馈 ID
7. 隐私保护到位：不存储原始反馈文本、用户备注、编辑文本或边界备注
8. 文档准确区分了已完成工作（T191）和后续任务（T192-T195）

**Warnings 的原因**：

- Worker handoff 文档中测试计数写成了 22 但实际是 21（`worker_summary` 文件中的计数是正确的 21）
- `.claude/settings.json` 新增了编译/测试命令——与项目一贯模式一致的工作区权限变更
- `RelationshipSignal` 没有 `updated_at` 字段，与 `RelationshipState` 和 `RelationshipDeltaCandidate` 不对称——后续 T193 审查流程更新信号状态时没有时间戳跟踪
- 提取器的规则表使用 `# type: ignore[arg-type]` 绕过 Literal 类型检查——运行时正确但静态类型安全性较弱
- 只覆盖 8 个维度中的 3 个——设计如此（宁可少提取也不要过度推断），但信号会比较稀疏

这些都是可以在后续任务中自然解决的细节，不阻塞当前任务的完成。

## 4. Worker 文档补充

Worker 的 `docs/worker_summary/T191_worker_summary.md` 内容基本准确。需要注意：

1. Worker summary 写 "21 committed tests"，这是正确的；但 handoff 中的 T191 Worker Completion Record 写了 "22 tests"，两者不一致。Handoff 中的计数应更正为 21。
2. Worker summary 的 "Remaining Risks" 准确描述了当前覆盖范围的限制和强度值未校准的问题。
3. Worker 没有提到 `RelationshipSignal` 缺少 `updated_at` 字段这一点——这是一个与后续 T193 相关的前向兼容性细节。
