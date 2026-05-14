# T120 Review Explained: File Store Models

## 1. 这个 Task 是什么？通俗解释

前面的任务（T110-T113）已经把聊天记录"切块"、"总结"、"提取事实"、"组装成联系人档案"了。但问题是——**这些产物散落在不同的 JSONL/JSON 文件里，没有统一的存储格式。**

打个比方：
- T112 产出了 `memory_facts.jsonl`（一条一条的事实，每行一个 JSON）
- T113 产出了 `contact_skill.candidate.json`（一份联系人策略档案）

这些文件各有各的格式，缺少统一的东西：
- **谁审阅过？** 没有"审阅状态"字段——不知道哪些是人工看过的，哪些是机器自动生成的。
- **从哪来的？** 虽然有 `evidence_refs`（证据引用），但没有统一的"来源元数据"来记录这个产物是从哪次蒸馏跑出来的、用了哪些上游文件。
- **能不能直接用？** 没有一个明确的"准入门槛"——理论上不应该让没审阅过的候选直接进入回复生成系统。

T120 做的就是给这些产物**加上统一的"外壳"和"存储格式"**：
1. 每个 memory fact 和 contact skill 都被包装成一个 **Store Record**，带着来源信息、审阅状态、时间戳。
2. 多个 Record 组成一个 **Store File**，可以整体加载和保存。
3. 加载时兼容旧格式（T112/T113 的产出），不需要返工。
4. 只有**人工审阅通过**的 Record 才标记为"runtime ready"——候选档案绝对不能直接进入回复系统。

用一个现实类比：
- T112/T113 的产出就像"一堆草稿纸"，每张纸上记着一些信息。
- T120 做的是给每张草稿纸套上一个**标准档案袋**，袋子上写着：这张纸是谁写的、什么时候写的、有没有人审阅过、审阅结论是什么。
- 然后把所有档案袋放进一个**标准档案柜**（Store File），方便后续查找和管理。

## 2. 实现详细解释

### 2.1 任务目标

T120 的核心目标是：

1. **定义 Store Record 模型**：给每个 memory fact 和 contact skill 加上统一的"外壳"，包含来源元数据（provenance）和审阅元数据（review metadata）。
2. **定义 Store File 模型**：把多个 Store Record 打包成一个文件，方便整体加载和保存。
3. **实现文件 Store 服务**：一个能加载旧格式、保存新格式、保持所有字段不丢失的服务类。
4. **保留审阅门槛**：只有 `status="approved"` 且 `reviewed_by_human=True` 的记录才被视为"runtime ready"。
5. **不越界**：不新增 CLI、不连数据库、不引入向量库、不做 runtime 注入。

### 2.2 任务流程

```
legacy memory_facts.jsonl          legacy contact_skill.candidate.json
        ↓                                      ↓
ContactSkillFileStoreService            ContactSkillFileStoreService
  .load_memory_store()                    .load_contact_skill_store()
        ↓                                      ↓
  包装为 MemoryFactStoreRecord           包装为 ContactSkillStoreRecord
  (加上 source_metadata,                   (加上 source_metadata,
   review_metadata)                         review_metadata)
        ↓                                      ↓
  MemoryFactStoreFile                    ContactSkillStoreFile
        ↓                                      ↓
  .save_memory_store()                   .save_contact_skill_store()
        ↓                                      ↓
  memory_fact_store.json                 contact_skill_store.json
```

### 2.3 代码变化详解

#### 文件 1: `src/practical_chat_agent/core/models.py`

这是变化最大的文件之一，新增了约 80 行 Pydantic 模型定义。

**新增的类型别名**：
- `DistillationReviewState`: 审阅状态（`pending_human_review` / `reviewed` / `unknown`）
- `DistillationEvidenceValidationStatus`: 证据校验状态（`not_run` / `passed` / `failed` / `partial`），为 T121 的 evidence validator 预留

**新增的结构化模型**（按层次从内到外）：

1. `ContactSkillRedactionPolicy`：把 `ContactSkillCandidate.redaction_policy` 从 `dict[str, Any]` 收紧为结构化模型，包含 `store_raw_quotes`、`max_quote_length`、`mask_names`、`mask_phone_numbers` 四个字段。默认值与之前完全一致，所以已有的 JSON 文件不受影响。

2. `DistilledArtifactReviewDecision`：单次审阅决定。记录审阅人、时间、结论状态、附注和证据校验状态。这个模型支持审阅历史——每次人工审阅都会生成一条 Decision。

3. `DistilledArtifactReviewMetadata`：审阅状态汇总。包含当前审阅状态、是否经过人工审阅、最近一次决定、审阅人信息、以及完整的审阅历史列表。关键是 `is_runtime_ready()` 方法——只有三个条件同时满足才返回 True：
   - `status == "approved"`
   - `reviewed_by_human == True`
   - `last_decision == "approved"`

4. `DistilledArtifactSourceMetadata`：来源元数据。记录这个产物是从哪次蒸馏跑出来的（`source_run_id`）、原始文件路径、审阅文档路径、以及来源的 chunk ID、memory ID、event ID 列表。

5. `MemoryFactStoreRecord`：单个 memory fact 的存储记录。核心字段是：
   - `memory_fact`: 原始的 `MemoryFactCandidate`（T111 定义的）
   - `source_metadata`: 来源信息
   - `review_metadata`: 审阅信息
   - `record_id`, `created_at`, `updated_at`: 管理字段
   - `is_runtime_ready()`: 委托给 `review_metadata.is_runtime_ready()`

6. `MemoryFactStoreFile`：多个 Store Record 的集合，加上 `schema_version` 和 `generated_at`。

7. `ContactSkillStoreRecord` / `ContactSkillStoreFile`：与 memory fact 版本对称，包装 `ContactSkillCandidate`。

**新增的 helper 方法**（在 `MemoryFactCandidate` 上）：
- `to_runtime_memory_type()`：把蒸馏阶段的 `DistillationMemoryType`（semantic/episodic/relationship/procedural/reflection）映射到运行时的 `MemoryType`（FACT/RELATIONSHIP/PREFERENCE/REFLECTION）。
- `to_memory_fact()`：直接构造一个运行时的 `MemoryFact` 对象，为 T123 把 approved records 接入 `ChatContext` 预留。当前不调用，只是工具方法。

#### 文件 2: `src/practical_chat_agent/services/contact_skill.py`

新增了 `ContactSkillFileStoreService` 类（约 270 行），以及 `FileStoreSaveResult` 数据类。

**`ContactSkillFileStoreService` 的设计**：

- **初始化**：与 `ContactSkillBuilderService` 一样，解析 repo root 和 `private/distilled/` 路径。
- **加载策略**（以 memory store 为例）：
  - 如果输入是目录，优先找 `memory_fact_store.json`（新格式）；没有的话找 `memory_facts.jsonl`（T112 旧格式）并包装。
  - 如果输入是文件名匹配 `memory_facts.jsonl`，自动包装。
  - 否则作为 store JSON 文件加载。
- **保存策略**：序列化为 JSON 写入 `private/distilled/`，返回 `FileStoreSaveResult`（输出路径、记录数、状态列表）。
- **Legacy 包装**：`_wrap_memory_facts_jsonl()` 和 `_wrap_contact_skill_candidate()` 把旧格式产物包装成 Store Record：
  - 从文件路径推断 `source_run_id`（取 `private/distilled/<run_id>/` 的中间段）。
  - 从 `evidence_refs` 中提取 `evt_` 前缀的 event IDs。
  - 候选状态的产物得到 `review_state="pending_human_review"`。
  - 非候选状态（如已审批的旧产物）得到 `review_state="unknown"` 并附加说明："需要重新确认人工审批"。
- **路径安全**：所有输入输出都通过 `_ensure_within_root()` 检查，确保不会读写 `private/distilled/` 之外的文件。

**与 `ContactSkillBuilderService` 的关系**：
- 两个类有若干相同的 private helper（路径解析、JSON 读写等），但没有继承关系。
- `ContactSkillBuilderService` 负责构建候选档案（T113 的功能）。
- `ContactSkillFileStoreService` 负责存储和加载（T120 的功能）。
- 两者独立工作，通过共享的 Pydantic 模型（`MemoryFactCandidate`、`ContactSkillCandidate` 等）连接。

#### 文件 3: `docs/07_handoff.md`

- 更新了 T120 的状态描述，从"只做 file store models"改为"worker draft 已实现，待 reviewer 审核"。
- 新增了第 12 节"T120 worker draft 记录"，详细记录了实现内容、验证步骤和注意点。
- 后续小节重新编号（13-17）。

### 2.4 对后续开发的意义

T120 在整个 M2 milestone 中的位置：

```
T114 (M1 gate) → T120 (file store models) → T121 (evidence validator) → T122 (review CLI) → T123 (context integration)
```

T120 完成后，后续任务可以：

- **T121**：利用 `DistilledArtifactSourceMetadata` 中的 `source_event_ids` / `source_chunk_ids` 实现证据存在性和支撑性校验。`DistillationEvidenceValidationStatus` 字段已经预留在 review metadata 中。
- **T122**：基于 `DistilledArtifactReviewMetadata` 实现审阅 CLI——approve/reject/freeze 操作会更新 `last_decision`、`reviewed_by_human`、`history` 等字段。
- **T123**：通过 `is_runtime_ready()` 筛选可用记录，通过 `MemoryFactCandidate.to_memory_fact()` 将 approved memory 转换为 runtime `MemoryFact`，接入现有 `ChatContext`。

T120 的核心价值是：**第一次给离线蒸馏产物加上了统一的"身份证"和"审阅档案"**。之前 T112/T113 的产出就像散落的草稿纸——虽然有内容，但没有标准化的来源追踪和审阅状态。T120 之后，每条记忆和每个联系人技能都有：
- 唯一的 record ID
- 完整的来源链（从哪次 run、哪个文件、用了哪些 chunk/memory/event）
- 审阅状态和历史（谁审的、什么时候审的、结论是什么）
- 明确的准入门槛（只有人工审阅通过的才能进 runtime）

这为后续的自动化审阅、证据校验、版本管理和 rollback 奠定了基础。

## 3. 为什么给出 PASS_WITH_WARNINGS？

### 总体判断

T120 完成了任务包要求的所有内容：
- 新增了 Store Record 和 Store File 模型
- 保留了 status、evidence_refs、source ids 和 review metadata
- 实现了从旧格式加载和保存到新格式的服务
- `is_runtime_ready()` 保持了 candidate-only / human-review-first 语义
- `redaction_policy` 从 dict 收紧为结构化模型
- 提供了 `to_runtime_memory_type()` / `to_memory_fact()` 映射工具
- 没有新增 CLI、没有连数据库、没有引入向量库、没有做 runtime 注入
- 文档明确标注为 worker draft，没有把计划写成事实

没有发现任何需要返工的 blocking 问题，所以不是 BLOCK。

### 为什么不是纯 PASS？

有 5 个非阻塞性问题值得记录：

1. **保存时 `updated_at` 的"假更新"**（N01）：`save_memory_store()` 和 `save_contact_skill_store()` 在保存前做了一步 `record.model_copy(update={"updated_at": record.updated_at})`——把 `updated_at` 复制给自己，实际上什么都没变。看起来原本是想更新为当前时间，但代码写错了。不过这不影响正确性（时间戳值确实被正确写入了），只是多了一步无用功。归类为 accepted。

2. **两个 Service 类之间的代码重复**（N02）：`ContactSkillFileStoreService` 和 `ContactSkillBuilderService` 有若干相同的 private helper（路径解析、JSON 读写等），但没有提取为共享工具。两个类的代码加起来快 1300 行了。不过对于 MVP 来说，两个独立的 Service 各管各的也说得过去。归类为 accepted/deferred——如果后续出现第三个 Service 也需要同样的 helper，就应该提取了。

3. **单条记录 JSON 静默包装**（N03）：加载 store JSON 时，如果文件包含 `"memory_fact"` 或 `"contact_skill"` 顶级键（而不是标准的 `"records"`），会被静默包装成单元素列表。这是为了兼容性做的设计，但意味着格式不标准的文件可能被意外接受。Pydantic 的类型校验足以兜底，实际风险很低。归类为 accepted。

4. **`DistillationMemoryType` 到 `MemoryType` 的映射有损**（N04）：`"semantic"` 和 `"episodic"` 都映射到了 `MemoryType.FACT`，两个类型的区别在转为 runtime 格式时丢失了。这是 runtime 模型粒度较粗的限制，不是 T120 的设计错误。T111 reviewer 就已经指出这个问题并推迟到 T120。归类为 accepted。

5. **没有提交自动化测试**（N05）：验证是通过手动脚本完成的（写到 `private/distilled/t120_store_smoke/`），没有提交 `tests/` 下的单元测试。这是项目惯例——自动化测试统一安排在 T150。归类为 deferred。

### 结论

T120 实现了任务包的全部要求，没有越界，安全约束（candidate-only、human-review-first、路径限制）全部满足。非阻塞问题都是"代码小瑕疵"和"MVP 阶段惯例"类的——不影响正确性，不引入安全风险，不需要返工。

因此判定为 **PASS_WITH_WARNINGS**，可以继续推进到 T121。
