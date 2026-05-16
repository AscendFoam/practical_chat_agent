# T131 Review Explained: Relationship-Aware Reply Planner

## 一、这个 Task 在做什么？（通俗解释）

想象你在微信上收到了一个朋友的消息，你想回复，但不确定怎么回比较合适。这个 Task 就是让系统帮你生成几个**回复草稿**供你选择。

但系统不是随便生成回复——它会参考之前分析过的你和这位朋友的关系信息。比如：
- 你们是朋友还是同事？
- 平时聊天风格是轻松的还是正式的？
- 有没有需要注意的边界（比如不要过于亲密、不要冒充对方说话）？

系统会根据这些信息生成至少 3 个不同风格的回复建议，每个建议都附带：
- 回复草稿文本
- 为什么这么回复的理由
- 引用了哪些已审核的关系信息
- 风险提示
- 边界提醒

**关键原则**：这些草稿只是给你看的，系统**绝不会自动发送**。

## 二、实现详解

### 2.1 任务目标

T131 的目标是实现一个名为 `ReplyPlanner` 的服务，它：

1. **只读取已审核的紧凑关系上下文**（来自 T123 的 `ApprovedStoreContext`），不读取原始聊天记录
2. **生成至少 3 个有意义的候选回复草稿**，不是简单的同义替换
3. **输出符合 T130 定义的 `ReplyPlan` 格式**的 JSON
4. **执行安全检查**：联系人 ID 对齐、候选排名唯一等

### 2.2 任务流程

```
ChatContext（紧凑安全上下文）
  │
  ├─ 检查 contact_id 对齐（ChatContext.user_id == approved store contact_id == skill contact_id）
  │
  ├─ 构建安全摘要（只用计数和状态，不用原始文本）
  │
  ├─ 根据关系类型选择草稿模板
  │   ├─ friend/classmate/family → 朋友风格模板
  │   ├─ colleague → 同事风格模板
  │   └─ unknown → 通用模板
  │
  ├─ 为每个候选构建引用来源（只引用已审核的 record id、evidence ref、recent event id 等）
  │
  ├─ 添加风险标记和边界提醒
  │
  └─ 最终验证（priority_rank 唯一、contact_id 对齐）
      │
      ▼
ReplyPlan JSON（3 个候选草稿 + 理由 + 引用 + 风险 + 边界）
```

### 2.3 代码变化

#### `src/practical_chat_agent/services/reply_planner.py`（新文件）

这是核心实现，包含两个主要类：

- **`ReplyPlannerError`**：安全检查失败时抛出的异常
- **`ReplyPlanner`**：回复规划服务，核心方法 `generate(context=...)` 流程：
  1. 从 `ChatContext.user_id` 提取目标联系人 ID
  2. 调用 `_validate_contact_alignment` 确保 approved store 和 skill 的 contact_id 与之一致
  3. 调用 `_build_source_context` 构建安全摘要（只用 enum 值、计数、状态字符串，不含原始文本）
  4. 调用 `_build_candidates` 根据 `relationship_type` 选择模板，生成 3 个候选：
     - **conservative_acknowledgment**（纯确认，不延伸话题）
     - **optional_follow_up**（温和地邀请更多交流）
     - **paced_next_step**（建议按节奏后续展开）
  5. 每个候选都有独立的引用来源、风险标记、边界提醒和置信度
  6. 最终 `_validate_plan` 验证 priority_rank 唯一且连续

#### `src/practical_chat_agent/app/main.py`（新增 CLI 命令）

新增 `chat-reply-plan` 命令：
- 输入：一个安全的 `ChatContext` JSON 文件
- 输出：`ReplyPlan` JSON（打印到终端或写入文件）
- 不回显原始输入上下文

#### `docs/07_handoff.md`（追加 Section 23）

记录了 T131 的实现内容、验证方式和剩余风险。

### 2.4 对后续开发的意义

T131 在整个项目路线图中的位置：

```
M0: 数据合约 → M1: 离线蒸馏 → M2: Store 审阅 → M3: 回复规划 → M4: 反馈闭环 → M5: 评估硬化
                                                 ↑
                                              我们在这里
```

**T131 的意义**：

1. **首次将"已审核的关系知识"转化为"可操作的回复建议"**。之前的 T100-T123 都是在准备数据、建存储、做审核，T131 是第一次把这些投入实际使用。

2. **建立了安全规划和合约接线（contract wiring）**。即使当前的草稿是模板式的，它证明了：
   - 只有已审核+人工审阅的数据才能进入回复流程
   - 原始聊天记录不会泄漏
   - 联系人 ID 在整个链路上保持一致
   - 候选排名不会冲突

3. **为 T132（边界/策略校验）和 T133（质量评估）打下基础**。T132 会检查草稿是否遵守边界和禁忌，T133 会用真实场景评估草稿质量。

4. **当前的局限性是设计上的有意选择**：T131 用确定性模板而非 LLM 生成，先证明安全边界正确，再在后续任务中提升质量。

## 三、为什么我给出了 PASS_WITH_WARNINGS 的 Review 结果？

### 通过（PASS）的部分

1. **任务包要求全部满足**：有服务、有 CLI、3 个候选、每个候选都有完整的字段（draft_text、rationale、refs、risk_flags、boundary_reminders、confidence）。

2. **没有违反任何禁止范围**：没有自动发送、没有读取原始聊天记录、没有接入数据库或向量库、没有冒充联系人。

3. **T130 的两个 warning 都被处理了**：
   - `priority_rank` 通过 `_validate_plan` 强制唯一且连续
   - `contact_id` 通过 `_validate_contact_alignment` 三重对齐检查

4. **安全摘要重建正确**：`_build_safe_context_summary` 只用 enum 值、计数和状态字符串，原始消息文本不会进入计划。

5. **没有破坏已有功能**：改动完全是增量的。

### 带有 Warning 的部分

Warning 1：**草稿模板是硬编码的，关系感知程度较浅。**
- 系统根据 `relationship_type`（朋友/同事/未知）选择模板，但三个类型的措辞差异很小
- 没有利用 `strategy_hints`（策略提示）、`relationship_summary`（关系摘要）或记忆事实的描述文本
- 意味着"关系感知"目前更多是结构上的（正确的引用来源），而不是内容上的（真正根据关系特点定制回复）
- **为什么不是 BLOCK**：任务没有要求 LLM 调用，worker 明确说明了这是启发式实现，T132/T133 负责提升质量

Warning 2：**置信度数值是人为设定的（0.78/0.71/0.66 等），不是基于证据推导的。**
- 传达了不存在的精确度
- **为什么不是 BLOCK**：`confidence` 字段在 schema 中是可选的，数值确实在有/无审核上下文时正确降低

Warning 3：**没有提交自动化测试或 fixture。**
- 验证是用内联合成上下文完成的，没有持久化
- **为什么不是 BLOCK**：T150 专门负责建立自动化测试

### 总结

T131 正确地建立了回复规划的安全框架和合约接线。当前的草稿质量有限（硬编码模板），但这是 MVP 阶段的合理取舍——先证明安全边界正确，再在 T132/T133 中提升内容质量。核心价值是：**当你未来加入 LLM 生成时，所有安全检查、引用来源、边界提醒的管道已经就位了。**
