# T200 Review Explanation

## 这个任务在做什么？

T200 是 M9（Memory Retrieval Layer）的第一个任务，目标是定义一个 **检索器抽象接口**。

在 T200 之前，项目中记忆检索的逻辑直接写死在 `MemoryRetrievalService` 里——它把候选记忆按显著度排序、过滤后返回 `MemoryFact` 列表。这个实现没有问题，但它是"实现"而不是"合约"。如果未来想要：
- 从已审批的记忆仓库中检索（T201）
- 接入 Mem0/Zep 等外部记忆服务（T203）
- 换用向量相似度检索

每个新检索器都需要重新设计输入输出，而且无法保证它们返回的结果格式一致。

T200 的目标就是在不做任何新检索器的前提下，先定义好**"检索器应该长什么样、返回什么"**的合约，让后续任务有一个统一的目标去实现。

## 实现做了什么？

### 1. 新增数据模型（`core/models.py`）

三个新类型：

- **`MemoryHit`**：一次检索命中的结果。只携带 reviewer 安全的内容：`fact`（事实文本）、`memory_type`（类型）、`score`（相关度分数）、`evidence_refs`（证据引用）、`source`（来源标记）。明确不携带原始聊天文本、向量嵌入、写入能力。
- **`MemoryRetrieverResult`**：检索器返回的信封。包含 `status`（成功/未配置/错误）、`contact_id`、`hits`（命中列表）、`candidate_count`（候选总数）、`notes`（备注）。
- **`MemoryRetrieverStatus`**：状态字面量类型（`"success"`, `"not_configured"`, `"error"`）。

这些模型和现有的 `MemoryFact`、`MemoryRetrievalResult` 并存，不替换也不修改它们。

### 2. 新增协议（`services/memory_retrieval.py`）

- **`MemoryRetriever`**：一个 `typing.Protocol`，定义了 `retrieve(*, contact_id, query, limit) -> MemoryRetrieverResult` 方法。任何实现了这个方法的类都被视为合法的检索器。

### 3. 新增适配器

- **`LocalMemoryRetriever`**：把现有的 `MemoryRetrievalService` 包了一层，让它满足 `MemoryRetriever` 协议。使用 `with_context()` 注入上下文后才能检索，否则返回 `not_configured`。
- **`convert_retrieval_result()`**：把服务层的 `MemoryRetrievalResult` 转换成协议层的 `MemoryRetrieverResult`。

### 4. 测试（40 个）

覆盖了模型验证、协议一致性检查、适配器行为、转换保真度、限制执行、来源标记、分数派生、证据引用保持、备注传递、上下文隔离、JSON 往返、合约边界断言。

### 5. 合约文档

`docs/data_contracts/memory_retriever_contract.md` 详细说明了模型定义、协议约束、适配器行为、T201 实现指引、以及有意留出的空缺。

## 对后续开发的意义

- **T201**（local approved-store retriever）可以直接实现 `MemoryRetriever` 协议，返回 `source="approved_store"` 的 `MemoryHit`。合约文档中已有专门的 T201 实现指引。
- **T202**（retrieval eval set）可以基于统一的 `MemoryRetrieverResult` 格式设计评估用例。
- **T203**（optional Mem0 adapter spike）可以在同一个协议下试验外部适配器，不影响现有代码。
- 未来的 ChatContext 集成可以统一消费 `MemoryHit`，不需要关心底层是本地检索还是外部服务。

## 为什么给出 PASS？

1. **任务目标完全达成**：定义了 `MemoryRetriever` 协议、`MemoryHit` 数据合约、最小适配器、合约文档。
2. **没有伪实现**：所有代码都是真实的 Pydantic 模型和协议实现，没有 mock、stub 或硬编码假路径。
3. **测试充分**：40 个测试覆盖了模型、协议、适配器、转换和边界约束。全部通过。
4. **没有过度工程**：只添加了协议、3 个模型、1 个适配器和 1 个转换函数，恰好够用。
5. **没有破坏现有功能**：560 个测试全部通过（520 已有 + 40 新增），无回归。
6. **文档没有把计划写成事实**：合约文档清晰区分了"已实现"和"有意留出的空缺"。
7. **遵守了禁止范围**：没有引入向量库、外部适配器、自动写入、原始聊天记录读取、planner 行为变更。
8. **allowed-files 合规**：除了已建立的 `.claude/settings.json` 工作区产物噪音和 worker summary 惯例外，所有改动都在允许的文件列表内。

这是一个干净、合约优先、范围恰当的任务实现。
