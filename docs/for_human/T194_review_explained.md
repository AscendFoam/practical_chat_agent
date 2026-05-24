# T194 Review Explained

## 1. 这个 Task 在做什么？（通俗版）

想象一下，在 T190 我们定义了"关系状态"的 8 个维度（熟悉度、信任感等），T191 从反馈中提取"关系信号"，T192 根据信号生成"关系变更提案"（delta candidate），T193 让你（人类）审阅这些提案（批准/拒绝/冻结/归档）。

现在，批准的提案已经存在了。但问题来了：**怎么让 AI 回复助手知道这些批准的关系变更信息？**

**T194 的任务就是：把经过审批的关系变更信息，以一种**紧凑的、安全的**方式，注入到 AI 的回复上下文中。

想象一个场景：你批准了一个关系变更，认为某个联系人的"边界风险"从 0.3 上升到了 0.44。T194 会在 AI 组装回复上下文时，自动加入一条提示："注意：这个联系人的边界风险已从 0.30 上升到 0.44"。但 T194 **不会**把原始的审阅历史、信号详情或完整的提案内容塞进去——它只给你需要的"一句话摘要"。

## 2. 技术实现详解

### 任务目标

在 T193 能让人类审阅关系变更提案后，需要把审批通过的结果注入到 `ChatContext`（AI 回复上下文）中，以便后续的回复规划器能感知到关系变化。但必须保证：

1. **只读**：T194 只**读取**已审批的 delta，绝不修改真正的 `RelationshipState`
2. **紧凑**：只传递精炼的维度变化摘要，不暴露完整的审阅历史或信号详情
3. **安全**：未审批的（candidate/rejected/frozen/archived）delta 绝不进入上下文
4. **兼容**：不影响已有的上下文路径（approved_store_context、approved_patch_context、derived_brief_context）

### 任务流程

```
T193 审批通过的 RelationshipDeltaCandidate JSON 文件
  -> ChatContextAssembler (读取目录中的 *.json 文件)
  -> 过滤：只保留 status=approved + reviewed_by_human=True + last_decision=approved 的 delta
  -> 包装为 ApprovedRelationshipDeltaBrief (仅保留维度变化字符串、摘要、证据引用)
  -> 注入到 ChatContext.relationship_context
  -> 回复规划器可在不接触原始信号/审阅数据的前提下使用
```

### 代码变化

**1. `src/practical_chat_agent/core/models.py` — 新增 3 个模型**

- `ApprovedRelationshipDeltaBrief`：一个审批通过的 delta 的紧凑摘要。包含：
  - `dimension_changes`：格式化后的维度变化字符串（如 `"boundary_risk: 0.30->0.44 (increase)"`）
  - `delta_summary`：delta 原因摘要（最长 200 字符）
  - `evidence_refs`：证据引用（最多 6 条）
  - **不包含**：`signal_refs`（信号引用）、`review_metadata`（审阅元数据、审阅者身份、时间戳等）

- `ApprovedRelationshipContext`：容器模型，包含 `status`（使用 `ApprovedStoreContextStatus` 枚举值）、`source_path`、`contact_id`、`deltas` 列表和 `notes`。

- `ChatContext.relationship_context`：`ChatContext` 上的一个**新增可选字段**，与已有的 `approved_store_context`、`approved_patch_context`、`derived_brief_context` 平级共存。

**2. `src/practical_chat_agent/services/chat_context.py` — 扩展 ChatContextAssembler**

核心新增 4 个方法：

- `_load_approved_relationship_context(contact_id)`：入口方法，处理 4 种状态：
  - 路径未配置 → `not_configured`
  - 路径不存在或不是目录 → `store_path_missing`
  - 目录无 JSON 文件或无 runtime-ready delta → `no_runtime_ready_records`
  - 有有效的 delta → `loaded`

- `_try_load_runtime_ready_delta(path, contact_id)`：单个文件解析和过滤。读取 JSON → 校验为 `RelationshipDeltaCandidate` → 检查 `contact_id` 是否匹配 → 检查 `is_runtime_ready()` → 格式化为 `ApprovedRelationshipDeltaBrief`。

- `_build_relationship_context_notes(context)`：当关系上下文加载成功时，生成检索提示（如 `"relationship_delta_count=1"`、`"relationship_delta delta_test_001: boundary_risk: 0.30->0.44 (increase)"`）。

- `_build_summary()` 的扩展：在已有的 summary 后追加 `"Approved relationship guidance: boundary_risk: 0.30->0.44 (increase)."`。

新增的 `__init__` 参数：`approved_relationship_delta_path: Path | None = None`，可选指向 T193 输出的 delta JSON 文件目录。

**3. `tests/test_relationship_context.py` — 31 个测试**

覆盖范围：

- 加载成功 7 个：状态、维度变化、摘要、证据引用、delta_id、contact_id、多维 delta
- 降级行为 8 个：路径未配置（3 个）、路径不存在（1）、无 runtime-ready（5 个含候选态/空目录/混合过滤/错误联系人/未人工审核）
- 无原始泄露 4 个：无信号引用、无审阅历史、摘要截断、证据引用限制
- 与其他上下文共存 2 个
- 检索提示 4 个
- 摘要包含 3 个
- 确定性与无磁盘写入 2 个

**4. 文档更新**

- `docs/data_contracts/relationship_state_contract.md`：增加 T194 相关合约——Context Fields Added 表、Context Safety Constraints 6 条、Assembler Configuration
- `docs/07_handoff.md`：T194 Worker Completion Record
- `docs/worker_summary/T194_worker_summary.md`：Worker 自总结文档

### 对后续开发的意义

1. **T194 打通了"审批→上下文"链路**：批准的关系变更现在可以自然地出现在 AI 的回复上下文中，供 T195 评估使用。

2. **保持了多层安全防线**：
   - T193 的 human review gate
   - T194 只读不写（不修改 `RelationshipState`）
   - 只传递紧凑摘要（不泄露原始信号/审阅历史）

3. **与已有上下文路径独立**：`relationship_context` 独立于 `approved_store_context`、`approved_patch_context`、`derived_brief_context`，不影响已有功能。

4. **未解决的关键路径问题**：
   - **"审批通过 → 真正的 RelationshipState 更新"的路径仍然没有设计**。T194只是读取已审批的 delta 并注入上下文，但不会真正把 dimension 值更新到 `RelationshipState`。真正的状态更新需要未来的 task。
   - `approved_relationship_delta_path` 还没有通过 `AppContainer` 配置（没有环境变量支持），目前只能代码配置。

## 3. Review 结果：为什么是 PASS_WITH_WARNINGS

**任务目标达成情况**：Worker 完成了 T194 的所有要求——新增 3 个模型、`ChatContextAssembler` 的扩展逻辑、31 个测试覆盖全部场景、文档更新完整。没有越界行为。

**为什么不是 BLOCK**：没有阻塞性问题。代码正确、测试充分、没有伪实现、没有破坏已有功能、没有越界操作。所有安全约束得到满足（只读、紧凑、审批门控、不泄露原始数据）。

**为什么不是 PASS（而是有警告）**：存在 3 个非阻塞性问题和 3 个测试缺口：

1. **settings.json 有修改**（N01）：和所有 task 一样，属于工作区工件，不是 scope 违规。

2. **没有测试非法 JSON 的跳过路径**（N02）：`_try_load_runtime_ready_delta` 对解析失败的 JSON 文件会静默返回 `None`（这是正确的防御行为），但没有测试确认一个目录中的非 delta JSON 文件会被正确跳过。

3. **summary 截断路径未测试**（M01）：当维度变化字符串超过 200 字符时执行的截断逻辑没有直接测试。虽然实际触发概率极低，但属于无覆盖分支。

4. **路径是文件的边界情况未测试**（M02）：当配置路径指向一个文件而非目录时返回 `store_path_missing`，这个分支未测试。

5. **空的 delta_rationale 未测试**（M03）：如果 delta 的原因为空字符串，`delta_summary` 会为空，这个边缘情况未测试。

**总结**：T194 是一个高质量的完成，所有核心功能正确实现且有充分测试（31 个测试）。警告项都是边界情况的测试覆盖缺口，不影响功能正确性和安全性。

## 4. 对 Worker 文档的补充说明

Worker 的总结文档（`docs/worker_summary/T194_worker_summary.md`）准确且完整，没有发现错误或遗漏。

以下是补充说明（非修正，仅深化理解）：

1. **关于 `_build_relationship_context_notes` 的诊断信息传播**：Worker 没有提到当 `status != "loaded"` 时，`_build_relationship_context_notes` 返回 `list(context.notes)` 会导致诊断信息（如"Configured relationship delta path does not exist."）进入 `memory_retrieval_notes`。这个模式和 T123/T164 完全一致，属于项目级约定而非 T194 的问题。但如果未来清理整个检索提示机制，这个点值得注意。

2. **关于 `ApprovedStoreContextStatus` 的复用**：Worker 没有明确提到 T194 复用了 T123 的 `ApprovedStoreContextStatus` 枚举而非定义自己的状态枚举。这在语义上是合适的（值集合相同），但引入了跨域耦合。如果后续关系上下文需要独有的状态值，需要重构。

3. **关于已发布的 AppContainer 差距**：Worker 已记录"未配置 AppContainer"。需要补充的是：这不仅仅是配置便利性问题，也意味着在容器化部署中，T194 的关系上下文只能通过代码注入，不能通过环境变量配置。对于当前离线 MVP 来说是可接受的，但在进入运行时部署前需要解决。

4. **关于后续路径**：Worker 正确地指出 state application 被推迟。补充一点：T194 的任务描述说是"context-only"，T195 是"eval-only"。但"从 approved delta 到 RelationshipState update"的完整路径目前还没有被设计。这意味着 M8 存在一个 gap：T193 审批通过的 delta 在 T194 中被读取和使用，但永远不会被真正应用到 `RelationshipState` 本身。这个 gap 需要在 M8 收尾阶段或后续 task 中解决。
