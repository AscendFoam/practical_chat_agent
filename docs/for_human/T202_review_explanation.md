# T202 Review Explanation

## 这个任务在做什么？

T202 是 M9（Memory Retrieval Layer）的第三个任务，目标是为 `MemoryRetriever` 协议创建一个**合成的、可提交的检索评估集**。

在 T202 之前，项目已经有：
1. T200 定义的 `MemoryRetriever` 协议（统一的检索接口）
2. T201 实现的 `LocalApprovedStoreRetriever`（从已审批仓库检索记忆）

但这两个成果都缺乏一个系统化的评估基准。如果有人修改了检索逻辑（比如调整排序规则、放宽过滤条件、或者引入外部适配器），没有一个标准化的测试集来验证检索行为是否仍然正确。

T202 的目标就是：创建一个包含合成数据、覆盖各种检索场景的评估集，可以作为未来任何 `MemoryRetriever` 实现的回归测试基础。

## 实现做了什么？

### 1. 评估用例合约（`RetrievalEvalCase`）

定义了一个 frozen dataclass，每个实例描述一个检索评估场景：

- 用哪个联系人查询
- 用什么查询词（可选）
- 最多返回多少条
- 期望的状态码
- 期望返回哪些 memory_id（可选，用于验证排序）
- 期望的命中数量范围
- 禁止出现的 memory_id（用于验证排除规则）
- 期望的 candidate_count（可选）
- 维度标签（用于审计覆盖度）

这个设计的关键在于 `expected_hit_memory_ids` 可以是 `None`——当为 `None` 时不检查顺序，这使得不同排序策略的适配器也能通过同一个评估用例。

### 2. 合成记忆仓库（`build_synthetic_eval_store()`）

构建了一个确定性的合成仓库，包含 15 条记录、2 个联系人：

**synth_alice（12 条）**：
- 6 条已审批记录：涵盖 5 种蒸馏类型（procedural、relationship、episodic、semantic、reflection），importance 从 0.90 到 0.50 不等
- 6 条被排除记录：分别因为 candidate/rejected/frozen/archived/未人工审核/证据验证失败

**synth_bob（3 条）**：
- 3 条已审批记录：semantic、procedural、relationship

这个仓库的设计确保了：
- 每种排除类型都有对应的记录
- importance 值经过精心设计，使得排序结果是确定性的
- 两个联系人的内容没有交叉，可以测试跨联系人隔离

### 3. 通用评估运行器（`run_eval_case()`）

一个接受任何 `MemoryRetriever` 实例和 `RetrievalEvalCase` 的函数，执行以下断言：

1. 调用 `retrieve()` 获取结果
2. 验证状态码
3. 验证 contact_id 正确传播
4. 验证命中数量在预期范围内
5. 如果指定了 `expected_hit_memory_ids`，验证精确的有序列表
6. 验证禁止的 memory_id 没有出现
7. 如果指定了 `expected_candidate_count`，验证精确匹配

这个运行器只使用 `MemoryRetriever.retrieve()` 公共接口，不访问任何实现私有状态。

### 4. 19 个评估用例（E01-E19）

| 类别 | 用例 |
|------|------|
| 正面检索 | E01 单词查询命中、E02 全量无查询、E16 第二联系人独立检索、E18 多匹配查询 |
| 排除规则 | E04 candidate、E05 rejected、E06 frozen、E07 archived、E08 未审核、E09 证据验证失败、E17 全部排除综合 |
| 查询行为 | E03 查询无匹配、E14 大小写不敏感、E15 子串匹配、E19 limit 截断查询匹配 |
| 排序 | E11 确定性排序（精确 6-id 列表） |
| 边界 | E12 limit 执行、E13 未知联系人 |
| 跨联系人 | E10 跨联系人隔离 |

### 5. 8 个合约边界测试

- 所有 hit 的 `source` 为 `"approved_store"`
- 所有 `score` 在 `[0.0, 1.0]` 范围内
- 所有 hit 的 `evidence_refs` 非空
- 所有 `memory_type` 是合法的 `MemoryType` 枚举值
- `MemoryHit` 和 `MemoryRetrieverResult` 的 JSON 往返
- 检索不修改存储文件

### 6. 6 个覆盖度审计测试

这是对评估集本身的元测试：
- 所有必需的维度标签都存在
- 所有 6 种排除类型都有对应的 forbidden_id 检查
- 涵盖多个联系人
- 仓库构建是确定性的
- 至少有一个排序用例指定了精确的 id 列表
- 仓库包含预期数量的记录（15 条）

### 7. 1 个复用演示

展示了一个未来检索器如何使用相同的评估用例：将 `LocalApprovedStoreRetriever` 以 `MemoryRetriever` 协议类型传入 `run_eval_case()`，证明运行器只依赖协议接口。

### 8. 合约文档更新

- 新增 `docs/data_contracts/memory_retriever_eval_set.md`：完整的评估集合约文档，包含合成仓库布局、用例表、覆盖度要求、复用说明。
- 更新 `docs/data_contracts/memory_retriever_contract.md`：在"Intentional Gaps"之前添加了 T202 评估集引用。

### 9. 没有修改的文件

- `src/practical_chat_agent/core/models.py` —— 未修改
- `src/practical_chat_agent/services/memory_retrieval.py` —— 未修改
- `src/practical_chat_agent/services/chat_context.py` —— 未修改
- 没有任何运行时代码被修改。T202 纯粹是评估脚手架。

## 对后续开发的意义

- **T203**（optional Mem0 adapter spike）现在可以通过导入 `EVAL_CASES`、`run_eval_case()` 和 `build_synthetic_eval_store()`，将新的外部适配器传入运行器，验证它是否满足相同的检索合约。如果外部适配器使用不同的排序策略，可以将 `expected_hit_memory_ids` 设为 `None` 只检查命中集合。
- **检索质量回归保护**：任何未来对 `LocalApprovedStoreRetriever` 的修改（比如添加缓存、改变排序、放宽过滤）都会被这 19 个评估用例捕捉到。
- **跨实现对比**：T202 建立了一个标准化的"检索行为应该是什么样的"基准，使得本地检索器和外部适配器的行为可以通过同一套度量来比较。
- 后续如果需要评估 `LocalMemoryRetriever`（T200 的 `MemoryRetrievalService` 适配器），可以扩展现有评估集，但需要先解决它对 live `AgentProfile`/`InboundEvent` 对象的依赖问题。

## 为什么给出 PASS？

1. **任务目标完全达成**：创建了合成检索评估集，覆盖了正面检索、排除规则、查询行为、确定性排序和边界情况。
2. **没有伪实现**：所有数据都是真实的 Pydantic 模型实例，不是 mock 或 stub。评估运行器通过公共协议接口执行真实的磁盘 I/O 路径。
3. **测试充分**：33 个测试（19 评估用例 + 8 边界 + 6 审计 + 1 复用演示），全部通过。
4. **没有修改运行时代码**：`models.py`、`memory_retrieval.py`、`chat_context.py` 完全未变。T202 是纯粹的评估脚手架。
5. **没有过度工程**：一个 dataclass、一个构建函数、一个运行器函数、一个用例表。结构清晰，没有缓存、异步或复杂抽象。
6. **合成且安全**：所有数据都是合成的（synth_alice、synth_bob），不含真实聊天内容、真实姓名、真实平台 ID 或真实文件路径。
7. **可复用设计**：`run_eval_case()` 只依赖 `MemoryRetriever` 协议，任何实现都可以通过同一个运行器评估。
8. **文档没有把计划写成事实**：合约文档准确记录了评估集的设计和覆盖范围，没有声称 `LocalMemoryRetriever` 已被评估或 ChatContext 集成已完成。
9. **遵守了禁止范围**：没有引入向量库、外部适配器、自动写入、原始聊天记录读取、planner 行为变更、provider 调用。
10. **allowed-files 合规**：除了已建立的 `.claude/settings.json` 工作区产物噪音和 worker summary 惯例外，所有改动都在允许的文件列表内。
