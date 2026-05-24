# T203 Review Explanation

## 这个任务在做什么？

T203 是 M9（Memory Retrieval Layer）的第四个也是最后一个任务，目标是一次**可控的技术验证（spike）**：评估一个可选的 Mem0 外部记忆适配器能否接入已有的 `MemoryRetriever` 协议，同时不削弱项目"先审核再使用"的记忆安全原则。

在前面的任务中：
- T200 定义了 `MemoryRetriever` / `MemoryRetrieverResult` 统一协议
- T201 实现了 `LocalApprovedStoreRetriever`（从本地已审批仓库检索）
- T202 创建了合成检索评估集（19 个评估用例 + 边界测试 + 覆盖度审计）

T203 的核心问题是：**如果未来想用 Mem0 这样的外部记忆服务，能不能不改动现有代码、不引入硬依赖、不绕过安全规则地接入？** 答案通过一次 spike 来验证。

## 实现做了什么？

### 1. 新建适配器模块（`optional_mem0_adapter.py`）

创建了一个独立的适配器类 `Mem0AdapterRetriever`，实现了 `MemoryRetriever` 协议。核心设计：

**优雅降级**：当 Mem0 不可用时，不是报错或崩溃，而是返回 `status="not_configured"`。触发条件有三种：
1. 没有提供 API key → 返回 `not_configured`
2. `mem0` 包没有安装 → 通过 lazy import 捕获 `ImportError`，返回 `not_configured`
3. 客户端初始化失败 → 捕获异常，返回 `not_configured`

**只读不写**：适配器只调用 `search()` 和 `get_all()` 两个读方法，从不调用 `add()`、`delete()`、`update()` 等写方法。这是 spike 的一条硬约束。

**协议兼容**：`isinstance(adapter, MemoryRetriever)` 返回 `True`，证明适配器确实满足了协议的接口要求。

### 2. 结果转换（`_convert_results`）

Mem0 返回的是自己的 JSON 格式（`{"id": ..., "memory": ..., "score": ...}`），需要转换为项目标准的 `MemoryHit`。转换逻辑包括：
- 跳过非字典、缺少 id 或缺少 memory 的无效条目
- 分数从 Mem0 的 `score` 字段读取，缺省为 0.5，限制在 `[0.0, 1.0]` 范围内
- 来源标记为 `"external_adapter"`（区别于本地检索器的 `"approved_store"`）
- 证据引用生成为 `["mem0:<id>"]`（合成值，因为 Mem0 不提供结构化证据引用）

### 3. 类型推断（`_infer_memory_type`）

Mem0 不区分记忆类型，但项目的 `MemoryHit` 需要 `memory_type` 字段。适配器用关键词启发式来推断：
- "likes"、"prefers"、"enjoys" → PREFERENCE
- "friend"、"partner"、"met at" → RELATIONSHIP
- "feels"、"worries"、"stressed" → REFLECTION
- 其他 → FACT（默认值）

这是一个粗粒度推断，spike 文档明确标注了其局限性。

### 4. 测试覆盖（45 个测试）

测试全部使用 `unittest.mock.MagicMock` 模拟 Mem0 客户端，不需要真实的 Mem0 包或网络访问。覆盖了 11 个方面：

| 类别 | 测试数 | 覆盖内容 |
|------|--------|----------|
| 不可用降级 | 6 | 无 key、None key、空 key、空白 key、原因文本、多次调用 |
| 协议兼容 | 2 | isinstance 检查（有无 client） |
| 搜索查询 | 2 | 命中提取、空结果 |
| 全量获取 | 4 | 命中提取、空结果、默认分数、candidate_count |
| limit 执行 | 2 | 搜索和获取路径 |
| 错误处理 | 2 | 客户端异常 → error 状态 |
| 字段映射 | 11 | contact_id、分数来源、分数夹紧、无效分数、证据引用、缺失字段跳过、notes 内容 |
| 类型推断 | 5 | 偏好、关系、反思、默认事实、混合类型 |
| 合约边界 | 7 | 来源正确性、分数范围、无原始文本、无嵌入、无写能力、JSON 往返、不修改客户端 |
| 评估复用 | 4 | 成功案例、不可用案例、禁止 id 检测、get_all 路径选择 |

### 5. Spike 发现文档（`docs/spikes/T203_mem0_adapter_spike.md`）

这是一份诚实的 spike 总结，包含：

**可行的方面**：
- 协议适配成功
- 优雅降级有效
- 结果形状兼容
- 无写入接口
- 评估用例形状可复用

**局限性**：
- Mem0 结果没有经过人工审核或证据验证
- 类型推断是启发式的，可能误分类
- 证据引用是合成的，无法追溯源头事件
- 排序依赖 Mem0 内部逻辑
- SDK 版本敏感
- 没有重试、限流或退避策略

**建议**：适配器在技术上可行，但在生产使用前需要解决审核集成、证据映射、SDK 版本固定和错误恢复等问题。

### 6. 合约文档更新

- `docs/data_contracts/memory_retriever_contract.md`：在 "Intentional Gaps" 之前添加了 T202 和 T203 的引用段落
- `docs/07_handoff.md`：添加了 T203 Worker Completion Record

### 7. 没有修改的文件

- `src/practical_chat_agent/core/models.py` — 未修改
- `src/practical_chat_agent/services/memory_retrieval.py` — 未修改
- `src/practical_chat_agent/services/chat_context.py` — 未修改
- 适配器是独立的新模块，不与现有运行时代码耦合

## 对后续开发的意义

- **M9 里程碑收尾**：T200-T203 四个任务共同完成了 Memory Retrieval Layer 的全部目标：定义协议（T200）、实现本地检索器（T201）、建立评估基准（T202）、验证外部适配器可行性（T203）。Captain 现在可以评估 M9 是否满足关闭条件。
- **M10 BehaviorPlanner**：下一个里程碑 M10 的 T210（行为 schema）可以开始。M9 的 `MemoryRetriever` 为 M10 的行为规划器提供了记忆检索能力——当行为规划器需要了解某个联系人的偏好或关系状态时，可以通过统一的 `MemoryRetriever` 接口检索。
- **外部记忆路径选择**：T203 spike 的结论是"技术可行但有明显局限"。这意味着如果项目未来决定引入 Mem0 或类似服务，有一条清晰的集成路径，但当前的本地已审批检索器仍然是推荐的主要路径。
- **审核安全边界**：spike 明确揭示了外部适配器不满足项目审核安全要求的问题（没有人工审核、没有证据验证）。这个发现为未来可能的外部适配器集成提供了明确的前置条件清单。

## 为什么给出 PASS？

1. **任务目标完全达成**：spike 验证了可选 Mem0 适配器在技术上可以接入 `MemoryRetriever` 协议，并且优雅降级有效。任务允许的两种输出（实现适配器或记录 blocker）中，worker 选择了更有价值的路径——实现了可运行的适配器。
2. **没有伪实现**：所有工作路径通过 mock 客户端执行了真实的协议接口调用。`_infer_memory_type` 是真实的关键词启发式函数，不是 stub。降级路径是真实的条件分支，不是硬编码返回值。
3. **测试充分**：45 个测试覆盖了 11 个行为维度。所有测试通过，没有需要 Mem0 包或网络访问。
4. **没有修改运行时代码**：`models.py`、`memory_retrieval.py`、`chat_context.py` 完全未变。适配器是独立的新模块。
5. **没有过度工程**：一个类、一个辅助函数、一组关键词表。结构清晰，没有缓存、异步或复杂抽象。独立的模块避免了与 1665 行的 `memory_retrieval.py` 耦合。
6. **文档诚实**：spike 文档明确记录了所有限制，没有声称 Mem0 已被采用或生产就绪。合约文档的添加是事实性的。
7. **遵守了禁止范围**：没有引入硬依赖、没有网络调用、没有私有聊天内容、没有自动写入、没有 approved store 修改、没有 ChatContext/ReplyPlanner/policy/send 变更。
8. **allowed-files 合规**：新建的适配器模块是任务明确授权的"exactly one new file under `src/practical_chat_agent/services/`"。`.claude/settings.json` 和 worker summary 是已有的约定噪声。
9. **没有回归**：M9 全部 181 个测试通过，全套件 706 个测试通过（16 个预先存在的 typer 模块缺失失败与 T203 无关）。
