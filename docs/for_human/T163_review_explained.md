# T163 通俗解释与 Review 说明

## 一、这个 Task 在做什么？（通俗解释）

想象一下，你已经有了一个"助手"（一个 AI 系统），它能够根据你的聊天记录分析出一些**候选的偏好补丁（Preference Patch）**。这些补丁类似于"提醒便签"——例如：

- "这个联系人喜欢简短直接的回复风格"（tone_preference）
- "这个联系人讨论某些话题时应该更谨慎"（boundary_preference）
- "不要太主动联系这个人"（proactivity_preference）

在 T162 中，系统已经能够根据你之前对回复草稿的反馈（accept/reject/boundary），自动聚类并生成这些候选补丁。但这些补丁当时只是"提案"状态（candidate），还不能影响系统的实际行为——它们必须先经过**人工审核**。

**T163 就是做这件事：给前端工具提供了一套明确的人工审核命令**。你可以用命令行告诉系统：

- "我批准（approve）这个补丁" → 补丁变为 `approved`，状态标记为"运行时可用"（runtime-ready）
- "我拒绝（reject）这个补丁" → 补丁变为 `rejected`，永远不会进入运行时
- "我冻结（freeze）这个补丁" → 补丁变为 `frozen`，暂时不用但保留（比如等信息更多时再决定）
- "我归档（archive）这个补丁" → 补丁变为 `archived`，保留历史但不再活跃

每次审核都会记录：谁做的决定、什么时候做的、备注是什么，而且这些历史记录会累积起来，不会互相覆盖。最关键的是：**审核过程绝对不会修改补丁中的原始证据**（supporting_feedback_ids、claim、confidence 等）——审核只是改变状态和元数据。

## 二、实现详解

### 2.1 任务目标

T163 位于 M5（Feedback to Patch）阶段的第三步。前两步分别是：
- T160：定义了 PreferencePatch 的数据结构（schema）
- T161：对用户反馈进行聚类（clusterer）
- T162：从聚类结果生成候选补丁（proposal CLI）

T163 要在 T162 的基础上，提供明确的人工审核决策能力，但必须保持以下严格边界：
- **不自动批准**任何补丁
- **不把批准的补丁注入运行时**（这是 T164 的工作）
- **不修改** ContactSkill / MemoryFact
- **不调用** LLM
- **不发送**任何消息
- **不改变**补丁中的原始证据字段

### 2.2 代码变化

#### 2.2.1 `src/practical_chat_agent/services/feedback.py`

新增 `PatchReviewService` 类（约 180 行），核心方法：

| 方法 | 职责 |
|------|------|
| `review()` | 主入口，协调整个审核流程 |
| `_normalize_decision()` | 校验决策字符串（approve/reject/freeze/archive） |
| `_load_proposal_report()` | 加载 T162 提案报告 JSON，校验 schema_version |
| `_find_patch()` | 按 patch_id 查找目标补丁，列出可用的 patch_id |
| `_apply_decision()` | 核心审核逻辑：创建 ReviewDecision、追加 history、更新 status 和 metadata |
| `_finalize()` | 写回 JSON、构建隐私安全的 stdout 输出 |

关键设计决策：
- 使用已有模型 `DistilledArtifactReviewDecision` 和 `DistillationStatus`（与 T122 保持一致的审核模式）
- Evidence 字段（supporting_feedback_ids, claim, behavior_instruction, confidence 等）在审核中**零修改**
- `review_metadata.history` 采用追加（append）而非覆盖模式
- `is_runtime_ready()` 三重检查：status == "approved" + reviewed_by_human == True + last_decision == "approved"

#### 2.2.2 `src/practical_chat_agent/app/main.py`

新增 `chat-feedback-review-patch` CLI 命令：

```
chat-feedback-review-patch --input <path> --patch-id <id> --decision <approve|reject|freeze|archive> --reviewer <name> [--note <text>] [--output <path>]
```

参数说明：
- `--input`：T162 提案报告 JSON（必需）
- `--patch-id`：目标补丁 ID（必需）
- `--decision`：审核决定（必需，四选一）
- `--reviewer`：审核人标识（必需）
- `--note`：可选备注
- `--output`：可选输出路径（不指定则覆写输入文件）

stdout 输出经过隐私安全处理：
- `input_path` / `output_path` 通过 `_safe_cli_path()` 脱敏
- 只输出 patch_id、contact_id、patch_type、status、confidence、sensitivity、instruction_scope、supporting_feedback_ids、supporting_cluster_ids、is_runtime_ready、review_metadata 等安全字段
- **绝不**输出原始反馈文本、编辑文本、备注或边界标注

#### 2.2.3 `docs/data_contracts/preference_patch_contract.md`

新增 "Patch Review Contract (T163)" 章节，记录：
- CLI 形状
- 决策到状态的映射表
- 审核行为规则（证据保留、历史累积、覆写行为、runtime 门控）
- 审核输出 JSON 形状
- 隐私安全声明

#### 2.2.4 `docs/07_handoff.md`

新增 Section 63（T163 Implementation Record），包含：
- 文件改动清单
- 已实现功能说明
- 决策映射与状态转换规则
- 10 项合成验证的结果摘要
- T164 必须遵守的约束

#### 2.2.5 `docs/08_risks_and_open_questions.md`

新增 Captain Update（2026-05-19）和两个新风险：
- **R057**：默认覆写输入文件，非原子写入可能导致数据损坏
- **R058**：review_metadata.history 无上限，多次审核后可能无限增长
- 同时更新了 R053 和 R054 的状态以覆盖 T163

### 2.3 决策到状态的映射

| CLI 决策 | Patch 状态 | is_runtime_ready() |
|----------|-----------|-------------------|
| approve  | approved  | True（需同时满足三个条件） |
| reject   | rejected  | False |
| freeze   | frozen    | False |
| archive  | archived  | False |

### 2.4 对后续开发的意义

- **T164（Approved Patch Compact Context）** 的基础：T164 现在可以安全地从 T163 审核后的报告中只提取 `status == "approved"` 且 `is_runtime_ready() == True` 的补丁
- **审核历史可追溯**：所有决策都有时间戳、审核人、备注，为未来的审计和回溯提供了完整记录
- **与现有模式一致**：T163 的审核模式（DistilledArtifactReviewDecision、DistilledArtifactReviewMetadata）与 T122 的 Skill 审核模式保持一致

## 三、为什么给了 PASS_WITH_WARNINGS？

### 通过的方面

1. **任务目标完全达成**：四种审核动作（approve/reject/freeze/archive）全部实现，语义清晰
2. **没有伪实现、mock 或 stub**：所有代码都是真实可运行的
3. **严格在 scope 内**：没有自动批准、没有运行时注入、没有修改 ContactSkill/MemoryFact、没有调用 LLM
4. **证据字段零修改**：supporting_feedback_ids、claim、confidence 等在审核过程中完全不动
5. **隐私安全**：stdout 只输出安全的聚合 id 和元数据，不泄露原始文本
6. **没有过度工程**：代码简洁直接（~180 行），没有不必要的抽象
7. **176 个已有测试全部通过，零回归**
8. **文档准确反映了实际实现**，没有把计划写成已完成

### 保留的警告（Warnings）

| 编号 | 问题 | 严重程度 | 为什么不是 BLOCK |
|------|------|---------|-----------------|
| N01 | 合同文档中 T162 的 determinism guarantee 仍然声称 patch_id 是确定性的（实际是 UUID 随机生成），虽然 T163 新增部分正确，但没有修正这个已知错误 | 低 | T162 review 已将此标记为 deferred；T163 本身没有引入新的错误 |
| N02 | 没有已提交的自动化测试 | 中 | 与 T160/T161/T162 一致的模式；已有 10 项合成验证；R054 已记录 |
| N03 | 默认覆写输入文件，非原子写入 | 中 | R057 已记录；单用户离线场景下风险可控 |
| N04 | review history 无上限增长 | 低 | R058 已记录；实际使用中不会频繁重复审核 |
| N05 | settings.json 工作区变更 | 极低 | 与 T160/T161/T162 一致的惯例 |

### 为什么不给 BLOCK？

没有阻塞性问题。所有未解决的问题都有明确的性质（已知的跨任务债务、已在风险台账中记录），没有安全问题，没有伪实现，没有破坏已有功能。

### 为什么不是纯 PASS？

因为 N01 是一个本应在这次修复的小问题（T163 任务包明确要求"如果触及合同文件，必须修正 determinism 声明"），加上 N02 和 N03 虽然不是 T163 独有的问题，但它们延续了 M5 阶段的系统性风险（缺乏测试覆盖 + 文件写入安全），这些都使得 `PASS_WITH_WARNINGS` 是更准确的评价。

## 四、下一步

T164（Approved Patch Compact Context）可以继续推进，但必须遵守 T163 建立的约束：
- 只能消费 `status == "approved"` 且 `is_runtime_ready() == True` 的补丁
- 不能清除或覆盖 review history
- 不能声称获批补丁已经在运行时活跃
- stdout 和输出不能包含原始反馈文本或隐私路径
