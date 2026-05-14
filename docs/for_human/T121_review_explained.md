# T121 Review Explained: Evidence Validator

## 1. 这个 Task 是什么？通俗解释

在前一个任务 T120 里，每条记忆事实和联系人技能都被装进了一个"标准档案袋"（Store Record），袋子上写好了来源信息、审阅状态。现在的问题是——**档案袋里引用的证据，真的存在吗？**

打个比方：
- T112 提取了一条记忆事实："这个联系人对考试成绩有压力"。这条事实附带了 `evidence_refs: ["evt_001", "chk_003"]`，意思是"这个结论来自事件 001 和对话块 003"。
- 但如果后来有人手动删除了事件文件，或者蒸馏过程出了 bug 导致 `evt_001` 根本不存在，那这条记忆事实就变成了"没有证据支撑的断言"——这可能带来幻觉风险。

T121 做的就是**证据验证**：把所有 Store Record 里的 `evidence_refs` 拿出来，去上游产物里逐个查找，看这些引用的 ID 是否真的存在。同时还要检查**状态规则**：
- 候选（candidate）状态的记录能不能直接被批准？——不能，必须先人工审阅。
- 被拒绝（rejected）、冻结（frozen）、归档（archived）的记录能不能进入回复系统？——绝对不能。
- 已经批准（approved）但证据有缺失的记录怎么办？——必须拦截，不能进入下游。

用一个现实类比：
- T120 给每份材料套上了标准档案袋，袋子上写着"引用了文件 A、B、C"。
- T121 做的是**核查**：去档案库里找一遍，A、B、C 是否真的在库？如果 B 不在了，就在袋子上贴个"证据缺失，不可使用"的标签。
- 但 T121 **只贴标签，不销毁也不修改原文件**——真正的"处理"是 T122 的工作。

## 2. 实现详细解释

### 2.1 任务目标

T121 的核心目标是：

1. **建立证据索引**：读取同一次蒸馏 run 目录下的所有上游产物（normalized events、chunks、chunk summaries、memory facts、contact skill candidate），把所有可被引用的 ID 汇总成一个集合。
2. **校验每条 Store Record**：递归遍历每个记录的所有嵌套字段，找到所有 `evidence_refs`，逐个检查是否存在于索引中。
3. **执行状态规则**：
   - `candidate` → 默认不能审批/进入 runtime
   - `approved` + 缺失 refs → 被拦截
   - `rejected`/`frozen`/`archived` → 永远不能进入 runtime
   - `approved` + refs 完整 + 人工审阅通过 → 才算真正可用
4. **输出验证报告**：包含每条记录的检查结果、缺失引用、拦截原因、来源信息和审阅状态快照。
5. **不越界**：不自动审批、不改写原始数据、不调 LLM、不接数据库。

### 2.2 任务流程

```
private/distilled/<run_id>/
  ├── memory_fact_store.json (或 memory_facts.jsonl)
  ├── contact_skill_store.json (或 contact_skill.candidate.json)
  ├── normalized_events.jsonl
  ├── chunks.jsonl
  ├── chunk_summaries.jsonl
  └── ...
          ↓
EvidenceValidationService.validate_evidence()
          ↓
  1. 解析输入路径，确定 run 目录
  2. 加载 Store Records (通过 T120 的 ContactSkillFileStoreService)
  3. 建立证据索引 (从所有上游产物中收集 ID)
  4. 对每条 Record:
     a. 递归收集所有嵌套的 evidence_refs
     b. 逐个检查是否存在于索引
     c. 根据 status 执行状态规则
     d. 计算 approval_ready / runtime_ready
  5. 生成报告 (写入 private/distilled/<run_id>/evidence_validation_report.json)
  6. CLI stdout 只输出安全摘要
```

### 2.3 代码变化详解

#### 文件 1: `src/practical_chat_agent/services/evidence_validation.py`（新文件）

这是 T121 的核心文件，约 785 行。

**主要组件**：

- `EvidenceValidationService`：主服务类
  - `validate_evidence()`：主入口，协调整个验证流程
  - `_build_evidence_index()`：从上游产物构建 ID 索引
  - `_validate_record_payload()`：对单个 Record 做完整验证
  - `_collect_evidence_ref_locations()`：递归遍历序列化后的模型，收集所有 `evidence_refs` 的位置
  - `_validate_memory_record()` / `_validate_contact_skill_record()`：针对两种 Record 类型的适配器

**关键设计决策**：

1. **递归收集 evidence_refs**：`_collect_evidence_ref_locations()` 方法不硬编码字段路径，而是递归遍历整个 `model_dump()` 后的字典，找到所有名为 `evidence_refs` 的键。这意味着无论 `ContactSkillCandidate` 的嵌套结构如何变化（新加一个子字段包含 `evidence_refs`），验证都能自动覆盖。

2. **状态规则是分段执行的**：
   - 先检查是否有 `evidence_refs`（完全没有引用 → 阻断）
   - 再检查是否有缺失引用（有缺失 → 阻断）
   - 然后按 status 分支：
     - `candidate` → 加两个阻断原因
     - `rejected`/`frozen`/`archived` → 加两个阻断原因
     - `approved` 但未经过人工审阅 → runtime 阻断（但审批不阻断）

3. **区分 approval_ready 和 runtime_ready**：这两个是独立计算的。
   - `approval_ready`：`status == "approved"` 且没有审批阻断原因（即引用完整）。
   - `runtime_ready`：`status == "approved"` 且没有缺失引用 且 T120 的 `is_runtime_ready()` 为 True（即通过了人工审阅门控）。
   - 这意味着：一个 approved 记录可以"审批就绪"但"runtime 不就绪"——比如证据完整但还没被人工审阅过。

4. **只读设计**：验证器只生成报告，不回写 Store Record 的任何字段。状态变更留给 T122 的审阅 CLI。

5. **BOM 处理**：`_load_jsonl_objects` 在第一行剥离 UTF-8 BOM（`﻿`），解决 PowerShell 写文件时可能添加 BOM 的问题。

**证据索引的构建过程**：

索引从以下来源收集 ID：
- `normalized_events.jsonl` → `event_id`
- `chunks.jsonl` → `chunk_id` + `event_ids`（chunks 里也包含 event ID 列表）
- `chunk_summaries.jsonl` → `summary_id`（如果有的话）+ `chunk_id` + `event_ids`
- `memory_facts.jsonl` → `memory_id`
- `contact_skill.candidate.json` → 尝试找 `contact_skill_id`/`skill_id`/`candidate_id`（当前 schema 里不存在，会跳过）
- Store Records 本身的 `memory_id`

每个 ID 被索引时，同时记录来源（比如 "normalized_events.jsonl:event_id"），方便在报告中显示"这个 ID 是从哪个文件来的"。

#### 文件 2: `src/practical_chat_agent/app/main.py`

只增加了一个新 CLI 命令 `chatlog-validate-evidence`，带参数：
- `--input`：输入目录或文件路径（默认 `private/distilled`）
- `--output`：可选的报告输出路径
- `--dry-run`：只验证不写报告

CLI 的 stdout 输出只包含安全摘要（记录数、缺失数、阻断数、相对路径），不包含任何聊天原文或真实联系人信息。

#### 文件 3: `docs/07_handoff.md`

- 更新了当前唯一任务为 T121
- 新增了 T120 完成记录（包括 reviewer 结论和 warning 处理）
- 新增了 T121 worker draft 记录（验证命令、good/bad case 结果、剩余风险）
- 重新编号了后续小节

### 2.4 对后续开发的意义

T121 在整个 M2 milestone 中的位置：

```
T120 (file store models) → T121 (evidence validator) → T122 (review CLI) → T123 (context integration)
```

T121 完成后，后续任务可以：

- **T122**：在实现 review/approve CLI 时，可以要求"只有通过了 evidence validation 的记录才能被 approve"。T121 生成的 `evidence_validation_report.json` 就是 T122 的关键输入。
- **T123**：在把 approved records 接入 `ChatContext` 时，可以确认所有 runtime-ready 的记录都经过了证据验证和人工审阅双重门控。
- **T150**：可以把 evidence validator 的状态规则和嵌套 refs 收集逻辑加入自动化测试。

T121 的核心价值是：**建立了证据可追溯性的自动化校验**。之前的任务虽然要求所有 claim 都有 `evidence_refs`，但没有自动化手段验证这些引用是否真的指向存在的对象。T121 补上了这个缺口：
- 所有引用都会被检查（包括嵌套在 relationship_state、communication_style、topics 等子结构中的）
- 缺失引用会明确阻断审批和 runtime 使用
- 状态规则确保 candidate/rejected/frozen/archived 记录不会被误用

这为后续的安全护栏（"绝不让无证据的断言进入回复系统"）提供了技术基础。

## 3. 为什么给出 PASS_WITH_WARNINGS？

### 总体判断

T121 完成了任务包要求的所有内容：
- 实现了证据验证服务，能加载 T120 store records 并校验所有 evidence_refs
- 建立了全面的证据索引（events、chunks、summaries、memories、skills）
- 递归遍历所有嵌套 evidence_refs，不遗漏
- 状态规则完整且正确（candidate 阻断、approved+缺失 阻断、rejected/frozen/archived 永远阻断、人工审阅门控）
- 实现了 CLI 和报告输出
- 不自动审批、不改写原始数据、不调 LLM、不接数据库、不做 runtime 注入
- 好案例和坏案例都验证通过
- 文档没有把计划写成事实

没有发现任何需要返工的 blocking 问题，所以不是 BLOCK。

### 为什么不是纯 PASS？

有 5 个非阻塞性问题值得记录：

1. **`_extract_contact_skill_ids` 对当前 schema 总是返回空列表**（N01）：这个方法试图从 `ContactSkillCandidate` 的序列化结果中找 `contact_skill_id`、`skill_id`、`candidate_id` 三个字段，但当前 schema 里这三个字段都不存在——唯一类似的是 `contact_id`。所以这个方法总是返回空，而代码会 fallback 到用 `contact_id`。这不影响正确性（联系人技能主要靠 `evidence_refs` 校验，不靠自身 ID），但"contact_skill_ids" 在索引中的计数永远是 0。归类为 accepted。

2. **JSONL/JSON 加载代码是第三次复制**（N02）：`EvidenceValidationService` 里的 `_load_jsonl_objects`、`_read_json_object`、`_write_json` 和之前的 `ContactSkillBuilderService`、`ContactSkillFileStoreService` 里的几乎一样。现在是第三份副本了。不过 MVP 阶段可以接受，等以后出现第四个 Service 再重构也不迟。归类为 accepted/deferred。

3. **递归遍历整个序列化 payload 的性能**（N03）：`_collect_evidence_ref_locations` 递归遍历整个 `model_dump()` 后的字典来查找 `evidence_refs`。对于当前的数据量来说完全没问题，但如果未来 skill 结构非常复杂（很多嵌套的 topics、patterns、events），遍历开销会增加。不过这不是真正的瓶颈。归类为 accepted。

4. **验证器只读不改写**（N04）：验证器计算了 `approval_ready_after_validation` 和 `runtime_ready_after_validation`，但不把这些结果写回 Store Record 的 `review_metadata.evidence_validation_status`。这是有意为之的设计——保持验证器只读，把状态变更留给 T122 的审阅 CLI。归类为 accepted。

5. **没有提交自动化测试**（N05）：验证是通过手动运行 CLI 完成的（good case 用 t102_smoke，bad case 用合成 fixture），没有提交 `tests/` 下的单元测试。这是项目惯例——自动化测试统一安排在 T150。归类为 deferred。

### 结论

T121 实现了一个正确、全面的证据验证器。状态规则逻辑清晰且正确，嵌套 evidence_refs 的递归收集方法设计得很好，隐私保护措施到位。非阻塞问题都是"代码可以更优雅"和"测试可以更完善"类的——不影响正确性，不引入安全风险，不需要返工。

因此判定为 **PASS_WITH_WARNINGS**，可以继续推进到 T122。
