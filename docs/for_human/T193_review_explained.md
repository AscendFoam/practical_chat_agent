# T193 Review Explained

## 1. 这个 Task 在做什么？（通俗版）

想象你在管理一段人际关系 —— 你不想凭感觉做判断，而是希望有一个系统帮你看"证据"。

之前 T190 定义了"关系状态"的 8 个维度（熟悉度、信任感、温暖度等），T191 从你的反馈中提取"关系信号"，T192 把这些信号打包成"关系变更提案"（delta candidate）。

**T193 的任务就是：让你（人类）来审阅这些提案。**

你可以对每个提案说：
- **批准（approve）**：同意这个变更
- **拒绝（reject）**：不同意这个变更
- **冻结（freeze）**：暂时不处理
- **归档（archive）**：不再需要处理

就像一个 PR review 系统 —— 但 T193 只帮你做"审查决定"，不会自动应用这些变更到真正的关系状态上。安全和可控是它的核心原则。

## 2. 技术实现详解

### 任务目标

在 T192 能生成"关系变更提案"后，需要一个工具让人来审阅这些提案。T193 就是这个审阅工具。

### 任务流程

```
T192 生成的关系变更提案 (JSON)
  -> relationship-review-delta CLI
  -> RelationshipDeltaReviewService
  -> 人类审阅决定 (approve/reject/freeze/archive)
  -> 更新后的提案 (含审阅记录)
  -> 写入 JSON 文件
  -> 等待后续任务实际应用到 RelationshipState
```

### 代码变化

**1. `src/practical_chat_agent/services/feedback.py` — 新增审阅服务**

新增了 `RelationshipDeltaReviewService` 类，核心方法 `review_delta()`：
- 接收一个关系变更提案（delta）、一个决定（decision）、审查者身份（reviewer）、可选备注（note）
- 先对提案做深拷贝（deep copy），保证原提案不被修改
- 校验决定必须是 `approve` / `reject` / `freeze` / `archive` 之一（不区分大小写，容忍前后空格）
- 更新提案的状态、审阅元数据、时间戳
- 所有证据引用（evidence_refs）、信号引用（signal_refs）、维度变更（dimension_changes）都不变
- 如果批准了，提案的 `is_runtime_ready()` 返回 True，表明"这个提案可以进入下一步了"

关键设计决策：
- **全有或全无（all-or-nothing）**：一个提案包含多个维度的变更，你要么全部批准，要么全部拒绝，不支持只批准部分维度
- **复用已有模式**：审阅决策记录复用了 T120/T163 的 `DistilledArtifactReviewDecision` 模式，保持项目一致性

**2. `src/practical_chat_agent/app/main.py` — 新增 CLI 命令**

新增 `relationship-review-delta` CLI 命令，作为用户的交互入口：
- `--input`：要审阅的提案 JSON 文件路径
- `--output`：可选，输出路径（默认为覆盖输入文件）
- `--decision`：审阅决定（approve/reject/freeze/archive）
- `--reviewer`：审查者身份
- `--note`：可选，审阅备注

CLI 做的事情：读取 JSON -> 调用服务 -> 写回 JSON -> 输出安全摘要。

安全摘要只输出元数据（delta_id, contact_id, status, is_runtime_ready, 维度数量等），不输出原始提案内容。

**3. `tests/test_relationship_review_cli.py` — 22 个测试**

覆盖了：
- 4 种审阅决定（approve/reject/freeze/archive）各自正常工作
- 带备注的批准
- 非法决定的错误处理
- 大小写不敏感和空格容忍
- 批准后的 runtime-ready 状态
- 候选状态/reject 状态不是 runtime-ready
- 证据引用、信号引用、维度变更不被修改
- 审阅元数据正确更新
- 原提案不被修改（深拷贝验证）
- 多次审阅累积历史
- 多维度提案整体审阅

**4. 文档更新**

- `docs/data_contracts/relationship_state_contract.md`：增加了 T193 审阅相关的合约说明，包括审阅动作表、流程、安全约束
- `docs/07_handoff.md`：添加了 T193 Worker 完成记录

### 对后续开发的意义

1. **T193 是 M8（RelationshipState）的关键一环**：T190 定义 schema -> T191 提取信号 -> T192 生成提案 -> T193 人工审阅 -> T194 集成到上下文 -> T195 评估效果
2. **保持了"先审阅后应用"的安全原则**：approved delta 不会自动更新到 RelationshipState，需要未来 task（T194/T195）来设计从 approved delta 到 state update 的路径
3. **审计追溯**：每个审阅决定都记录在历史中，谁、什么时间、做了什么决定、为什么，都可追溯
4. **为后续任务提供了先决条件**：T194 需要读取 approved delta 并将其集成到 compact context 中

## 3. Review 结果：为什么是 PASS_WITH_WARNINGS

**任务目标达成情况**：Worker 完成了 T193 的所有要求 —— 有 CLI 审阅界面，有 4 种明确的操作，有 22 个测试覆盖，文档已更新，没有越界行为。

**为什么不是 BLOCK**：没有阻塞性问题。代码正确、测试充分、没有伪实现、没有破坏已有功能、没有越界操作。

**为什么不是 PASS（而是有警告）**：存在 4 个非阻塞性问题：

1. **没有 CLI 集成测试**（N01/M01）：22 个测试都只测试了服务层（`RelationshipDeltaReviewService`），没有测试 Typer CLI 命令本身。命令行参数解析、文件读写、JSON 解析错误处理等路径没有被提交测试覆盖。这是项目的一个历史遗留模式（T163、T162、T161 都有类似情况）。

2. **默认覆盖输入文件没有安全机制**（N02）：如果不指定 `--output`，审阅结果会覆盖原文件。如果写入过程中断，原提案会丢失。这沿用了 T163 的模式。

3. **没有证据预验证**（N03）：和 T122（要求证据验证报告通过才能批准）不同，T193 可以批准任何提案，不检查证据引用是否有效。这是有意的简化设计，但可能产生一个问题：批准的 delta 中的证据引用可能已经失效。

4. **settings.json 有修改**（N04）：添加了验证命令的权限条目，和之前所有 task 一样，属于工作区工件，不是 scope 违规。

**总结**：T193 是一个高质量的完成，所有核心功能正确实现且有充分测试。警告项都是已知的、文档化的、可接受的。

## 4. 对 Worker 文档的补充说明

Worker 的总结文档（`docs/worker_summary/T193_worker_summary.md`）准确且完整，没有发现错误或遗漏。

以下是补充说明（非修正，仅深化理解）：

1. **关于审阅模式的复用**：Worker 提到"Reuses existing `DistilledArtifactReviewDecision` / `DistilledArtifactReviewMetadata` patterns"，这是正确的。但需要注意 T193 和 T122 的一个重要区别 —— T122 的 approve gate 要求证据验证报告通过，而 T193 没有这个要求。这是有意的设计简化，但意味着 T194/T195 需要在应用 delta 时自行验证证据。

2. **关于 `reviewer` vs `reviewer_id`**：T193 把 `--reviewer` 同时用作 reviewer identity 和 reviewer ID（存储在 `last_reviewer_id` 和 `history[].reviewer_id` 中），而 T122 区分 `--reviewer-id` 和 `--reviewer-name`。T193 的简化版本对当前 scope 足够，但如果未来需要区分审查者姓名和 ID，需要增加参数。

3. **关于默认覆盖风险**：Worker 已记录此风险。补充建议：未来可以在写入前先做一次备份（如 `.bak` 文件），或者增加 `--backup` 选项，或者默认使用 copy-on-write（输出到新文件）。

4. **关于后续路径**：Worker summary 正确地指出 state application 被推迟到后续 task。补充一点：T194 的 task 描述说是"context-only"，T195 是"eval-only"，这意味着"从 approved delta 到 relationship state update"的完整路径目前还没有被设计。这个 gap 需要在 M8 的后期 task 中解决。
