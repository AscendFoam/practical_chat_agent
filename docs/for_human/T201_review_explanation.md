# T201 Review Explanation

## 这个任务在做什么？

T201 是 M9（Memory Retrieval Layer）的第二个任务，目标是基于 T200 定义的 `MemoryRetriever` 协议，实现一个**本地已审批记忆仓库检索器**。

在 T201 之前，项目中有两种获取记忆的方式：
1. `MemoryRetrievalService` —— 从传入的候选记忆中按显著度排序和过滤（T200 的 `LocalMemoryRetriever` 包装了它）。
2. 人工审批的 `memory_fact_store.json` 文件 —— 存放着经过证据验证、人工审批的已就绪记忆记录。

但第二种方式没有一个统一的检索接口。如果想要从已审批的仓库中查找"关于某个联系人的咖啡偏好"，就需要直接读 JSON 文件、手动解析和过滤。

T201 的目标就是：实现一个 `LocalApprovedStoreRetriever`，让它满足 T200 的 `MemoryRetriever` 协议，直接从 `memory_fact_store.json` 中检索已审批记忆，返回标准化的 `MemoryHit` 结果。

## 实现做了什么？

### 1. 新增类（`services/memory_retrieval.py`）

**`LocalApprovedStoreRetriever`** —— 一个从磁盘上的已审批记忆仓库文件检索记忆的类。

构造函数接受一个路径参数（可以是 `memory_fact_store.json` 文件本身，也可以是包含该文件的目录）。

`retrieve()` 方法的完整流程：

1. **解析文件路径**：如果传入的是目录，自动查找目录下的 `memory_fact_store.json`。如果文件不存在，返回 `not_configured`。
2. **加载并解析**：读取文件内容，尝试解析为 `MemoryFactStoreFile`（Pydantic 模型）。如果解析失败（JSON 格式错误、schema 不匹配），返回 `error`。
3. **筛选合格记录**：只保留满足三个条件的记录：
   - `subject_id` 等于请求的 `contact_id`（联系人匹配）
   - `is_runtime_ready() == True`（status 为 approved、已人工审核、最后决策为 approved）
   - `evidence_validation_status == "passed"`（证据验证已通过）
4. **查询过滤**（可选）：如果提供了 query，对 claim 文本做大小写不敏感的子串匹配。
5. **排序**：按重要性降序、置信度降序、memory_id 升序排列，保证结果确定性。
6. **截断**：应用 limit 参数。
7. **构建 MemoryHit**：每条合格记录转换为 `MemoryHit`，`source` 固定为 `"approved_store"`，`score` 来自记录的 `importance` 字段，`memory_type` 通过 `to_runtime_memory_type()` 映射。

### 2. 三重门禁设计

这个实现最关键的设计决策是**三重门禁**：

| 门禁 | 检查内容 | 目的 |
|------|---------|------|
| 联系人匹配 | `subject_id == contact_id` | 防止跨联系人串线 |
| 运行时就绪 | `is_runtime_ready()` = approved + 人工审核 + 最后决策 approved | 确保只有完全审批的记录被检索 |
| 证据验证 | `evidence_validation_status == "passed"` | 确保证据引用有效 |

candidate、rejected、frozen、archived、未人工审核、证据验证未通过或失败的记录永远不会出现在检索结果中。

### 3. 测试（63 个）

覆盖了：
- 协议一致性（`isinstance` 检查）
- 已审批记录检索（字段正确性）
- 排除记录（candidate/rejected/frozen/archived/未审核/证据验证失败/错误联系人）
- 查询过滤（匹配、大小写不敏感、不匹配、None、空串、空白）
- Limit 执行（正常、0、超大）
- 来源标记（`"approved_store"`）
- 分数派生（来自 importance）
- 记忆类型映射（5 种蒸馏类型全部覆盖）
- 证据引用保持
- 确定性排序（importance/confidence/memory_id 三级排序）
- 存储路径解析（文件路径 vs 目录路径）
- 边界情况（文件不存在、目录不存在、空目录、无效 JSON、错误 schema、空仓库、目录无存储文件）
- 备注内容
- 合约边界断言（无 raw/embedding/write/file/review 字段）
- 存储文件不被修改
- JSON 往返
- candidate_count 准确性

### 4. 合约文档更新

`docs/data_contracts/memory_retriever_contract.md` 中原来的"T201 Implementation Guide"被替换为"T201 Implementation Record"，记录了实际实现的完整设计。

### 5. 没有修改的文件

- `core/models.py` —— T201 没有添加任何新模型，只使用了 T200 的 `MemoryHit` 和 `MemoryRetrieverResult`。
- `services/chat_context.py` —— 完全没有改动。ChatContext 的集成留给后续任务。

## 对后续开发的意义

- **T202**（retrieval eval set）现在可以基于统一的 `MemoryRetrieverResult` 格式，同时评估 `LocalMemoryRetriever` 和 `LocalApprovedStoreRetriever` 的检索质量。
- **T203**（optional Mem0 adapter spike）可以在同一个协议下试验外部适配器，三种检索器（本地、审批仓库、外部）共享完全相同的接口。
- 后续的 ChatContext 集成任务可以选择让 `ChatContextAssembler` 接受一个 `MemoryRetriever` 实例，统一消费来自不同来源的记忆。

## 为什么给出 PASS？

1. **任务目标完全达成**：实现了 `LocalApprovedStoreRetriever`，满足 `MemoryRetriever` 协议，从已审批仓库中检索，使用确定性过滤。
2. **没有伪实现**：所有代码都是真实的 Pydantic 模型操作、文件 I/O 和协议实现，没有 mock、stub 或硬编码假路径。
3. **测试充分**：63 个测试覆盖了所有检索行为、排除规则、边界情况和合约约束。全部通过。
4. **没有过度工程**：只添加了一个类（`LocalApprovedStoreRetriever`），方法职责清晰，没有缓存层、没有异步、没有复杂抽象。
5. **没有破坏现有功能**：T200 的 40 个测试和 T201 的 63 个测试一起通过（103 个）。models.py 没有被 T201 修改。chat_context.py 没有被修改。
6. **文档没有把计划写成事实**：合约文档清晰记录了实际实现，没有声称 ChatContext 集成已完成。
7. **遵守了禁止范围**：没有引入向量库、外部适配器、自动写入、原始聊天记录读取、planner 行为变更。
8. **三重门禁设计**：联系人匹配 + 运行时就绪 + 证据验证通过，确保只有完全审批且有有效证据的记录被检索。
9. **allowed-files 合规**：除了已建立的 `.claude/settings.json` 工作区产物噪音和 worker summary 惯例外，所有改动都在允许的文件列表内。

这是一个干净、确定性、范围恰当的任务实现，证明了 T200 的合约可以被实际实现并正确工作。
