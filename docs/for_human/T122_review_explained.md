# T122 Review Explained: Skill Review CLI

## 一、这个 Task 在做什么？（通俗解释）

想象你经营一家工厂。原材料（聊天记录）经过一系列加工（解析、分块、摘要、提取事实），最终产出了"产品候选"——也就是关于某个联系人的"沟通技能档案"（ContactSkill）和"记忆事实"（MemoryFacts）。

但这些候选产品不能直接上架。原因很简单：

1. **可能是错的**：AI 在提取过程中可能产生没有依据的"幻觉"。
2. **可能不完整**：某些声称的事实可能引用了不存在的证据。
3. **涉及隐私**：这些信息来自真实聊天记录，必须由人确认可以安全使用。

T122 做的事情就是：**建一个质检站的 CLI 工具**。这个工具让人工审核员可以：

- **查看**所有待审核的产品候选（list）
- **批准**（approve）通过验证的产品
- **拒绝**（reject）、**冻结**（freeze）或**归档**（archive）有问题的产品
- **导出**审核报告（export）

关键安全规则：**批准必须先通过 T121 的证据校验**——如果某个事实声称"有证据支持"，但证据实际上不存在，系统会自动阻止批准。

## 二、实现详解

### 2.1 任务目标

T122 的核心目标是把之前 T120（文件存储）和 T121（证据校验）的工作连接成一个完整的**人工审阅工作流**：

```
T120: 存储（file store）── 存放候选产品，带审核元数据
T121: 校验（evidence validator）── 检查证据是否存在
T122: 审阅（review CLI）── 人工查看、做决策、导出报告
```

具体来说，T122 需要在命令行中提供以下能力：

| 功能 | 说明 |
|---|---|
| `list` | 安全地列出所有待审核记录的摘要信息 |
| `approve` | 批准一条记录（必须通过证据校验） |
| `reject` | 拒绝一条记录 |
| `freeze` | 冻结一条记录（暂停审核） |
| `archive` | 归档一条记录 |
| `export` | 导出审核报告到 Markdown |

### 2.2 任务流程

整体审阅流程如下：

```
1. 审核员运行 evidence validator (T121) 对目标目录做校验
   → 产出 evidence_validation_report.json

2. 审核员运行 review CLI 的 list 命令查看待审记录
   → 每条记录显示：ID、类型、状态、审核状态、证据校验结果、是否可批准/可运行

3. 审核员根据查看的信息做决策：
   - 如果证据校验通过 → 可以 approve
   - 如果有疑问 → 可以 reject / freeze
   - 如果不再需要 → 可以 archive

4. 审核员可以随时 export 导出审核报告
```

批准（approve）的防护链：

```
approve 请求
  ├─ 检查：是否有人工审核员身份？（必须有 reviewer_id 或 reviewer_name）
  ├─ 检查：记录当前状态是否为 rejected/frozen/archived？（这些状态不能直接批准）
  ├─ 检查：是否存在 T121 证据校验报告？（必须存在）
  ├─ 检查：报告整体状态是否为 passed？（必须通过）
  ├─ 检查：目标记录是否出现在报告中？（必须出现）
  ├─ 检查：目标记录是否有缺失的证据引用？（必须为 0）
  ├─ 检查：目标记录是否有已校验的证据引用？（必须 > 0）
  │
  ├─ 全部通过 → 更新状态为 approved，写入审核元数据
  └─ 任一失败 → 报错并拒绝操作，原文件不变
```

### 2.3 代码变化

#### 2.3.1 `src/practical_chat_agent/services/contact_skill.py`

这是改动最大的文件，新增约 530 行代码：

**新增 `ContactSkillStoreReviewService` 类**——审阅服务的主类：

- `list_store_records()`: 加载存储 → 加载校验报告 → 为每条记录构建安全摘要
- `apply_record_decision()`: 执行审阅决策的核心方法
- `export_review_artifact()`: 导出 Markdown 审核报告

**新增辅助数据结构**：

- `StoreRecordSummary`: 单条记录的安全摘要（冻结的 dataclass）
- `StoreReviewListResult`: list 操作的返回结果
- `StoreReviewDecisionResult`: 决策操作的返回结果
- `StoreReviewExportResult`: 导出操作的返回结果
- `_StoreWorkspace`: 内部工作空间（加载的存储 + 路径）
- `_StoreRecordHandle`: 记录句柄（存储类型 + 索引 + 路径 + 记录对象）
- `_ValidationReportContext`: 校验报告上下文（报告内容 + 按记录 ID 索引）

**新增稳定 record_id 机制**：

之前 T120 包装 legacy 产物时，record_id 是 Pydantic 自动生成的，每次加载可能不同。T122 改为基于 SHA-1 哈希的确定性 ID：

```python
def _stable_store_record_id(*, prefix, seed):
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"
```

这样 T121 报告中的 record_id 和 T122 CLI 中的 record_id 能保持一致。

**修复存储规范化**：

`normalize_memory_store` 和 `normalize_contact_skill_store` 现在会保留 `generated_at` 字段，不再丢失原始生成时间。

#### 2.3.2 `src/practical_chat_agent/app/main.py`

新增 `chatlog-review-store` CLI 命令：

```bash
# 列出所有记录
chatlog-review-store --input private/distilled/t122_pass_fixture --action list

# 批准（需要校验报告通过）
chatlog-review-store --input private/distilled/t122_pass_fixture \
  --action approve \
  --record-id skillstore_bae8944df32d64b2 \
  --reviewer-id human_reviewer_1 \
  --reviewer-name "Alice"

# 拒绝
chatlog-review-store --input private/distilled/t122_reject_fixture \
  --action reject \
  --record-id skillstore_0edb3e3030c16049 \
  --reviewer-id human_reviewer_1 \
  --note "需要重写"

# 导出
chatlog-review-store --input private/distilled/t122_pass_fixture \
  --action export \
  --output private/distilled/t122_pass_fixture/review_exports
```

新增 `_safe_cli_path()` 辅助函数，确保 CLI 输出中的路径是安全的相对路径。

#### 2.3.3 `src/practical_chat_agent/exporters/contact_skill_markdown.py`

新增 `render_store_review_markdown()` 函数，生成审核报告的 Markdown。报告内容只包含：

- 记录 ID、类型、状态
- 审核状态、审核员信息
- 证据校验结果
- 批准/运行时的阻塞原因
- 安全的文件路径

**不包含任何原始聊天内容或私密信息。**

#### 2.3.4 `docs/07_handoff.md`

新增第 14 节 "T122 worker draft"，记录：
- 代码变更清单
- CLI 功能说明
- 审核流程描述
- 私有 fixture 验证结果
- 剩余风险和假设

### 2.4 对后续开发的意义

T122 是 M2 里程碑（Memory/Skill Store 与证据校验）的第三个任务。它完成后：

1. **T123（上下文集成）可以安全开始**：T123 需要把 approved + runtime-ready 的记忆/技能接入 `ChatContext`。T122 确保只有经过人工审核、证据校验通过的记录才能被批准，T123 只需检查 `is_runtime_ready()` 即可安全加载。

2. **人工审核工作流已闭环**：T120（存储）→ T121（校验）→ T122（审阅 CLI）形成完整的"存储-校验-审阅"链条。每一步都保持 candidate-only / human-review-first 语义。

3. **隐私和安全护栏进一步加强**：
   - 所有操作限定在 `private/distilled/` 目录
   - 导出只包含安全摘要
   - 不可能绕过证据校验批准记录
   - rejected/frozen/archived 记录永远不会变成 runtime-ready

4. **为 M3（回复 Planner）奠定基础**：M3 需要 approved 的 ContactSkill 来生成回复草稿。T122 确保这个 approved 状态是经过人工和证据双重验证的。

## 三、为什么给出 PASS_WITH_WARNINGS 的评审结果？

### 整体评价

T122 的实现**完整且正确地完成了任务目标**，没有越界，没有伪实现，安全护栏到位。但由于存在几个不影响正确性但值得记录的小问题，我给出了 `PASS_WITH_WARNINGS` 而非 `PASS`。

### 做对了什么

1. **批准防护链是完整的**：六重检查（人工审核员、状态检查、报告存在、报告通过、记录在报告中、无缺失引用、有已校验引用），每一项都有清晰的错误消息。我逐一验证了代码逻辑，确认没有任何绕过路径。

2. **没有自动批准或批量操作**：每一次决策都需要明确指定 `--record-id`、`--action` 和审核员身份。不存在"默认通过"的路径。

3. **rejected/frozen/archived 永远不能变成 runtime-ready**：`_build_gate_summary` 对这些状态硬编码了 `status_{status}_never_runtime_ready` 阻塞原因。不存在任何代码路径能让这些状态变成可运行。

4. **审核元数据历史完整**：每次决策都会创建 `DistilledArtifactReviewDecision` 记录并追加到 `history`，包含审核员、时间戳、决策、备注和证据校验状态。不会覆盖历史记录。

5. **导出安全**：`_resolve_markdown_output_path` 强制输出在 `private/distilled/` 内，Markdown 内容只包含元数据。

6. **验证充分**：五个场景（happy approve、missing-ref block、reject、freeze、export）都使用了私有 fixture 验证，覆盖了任务包要求的所有情况。

### 警告（Non-blocking Issues）

以下是几个不影响正确性但值得注意的小问题：

| 编号 | 问题 | 严重程度 | 处理建议 |
|---|---|---|---|
| N01 | `_resolve_evidence_validation_status` 方法接收了 `current_status` 参数但立即 `del` 掉了（未使用），接口略有误导 | 低 | MVP 可接受 |
| N02 | `_update_candidate_status` 递归修改所有名为 `status` 的字段，如果未来模型添加不同语义的 `status` 字段可能误改 | 低 | 当前 schema 正确，未来需注意 |
| N03 | `store_runtime_ready` 变量在非 approved 状态下也会计算（虽然不影响正确性） | 可忽略 | 无需处理 |
| N04 | 审阅服务访问了文件存储服务的私有方法（`_resolve_existing_path` 等），耦合较紧 | 低 | MVP 可接受，后续可提取共享 API |
| N05 | `_StoreWorkspace` 是可变 dataclass 但被当作准不可变状态使用 | 可忽略 | 无需处理 |
| N06 | 没有提交自动化测试（与项目惯例一致，留给 T150） | 顺延 | T150 补充 |

这些警告都不影响功能正确性、安全性和隐私保护。T122 的核心目标——"实现人工审阅 CLI，批准必须经过证据校验"——已经完整达成。

### 没有给出的更差评价

- **不是 BLOCK**：没有阻断性问题。所有要求的功能都已实现且正确。
- **不是 PASS**：存在几个值得记录的代码质量问题（N01 的未使用参数、N04 的耦合），虽然不影响正确性，但记录下来对后续维护有帮助。
