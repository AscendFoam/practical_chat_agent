# T142 Review Explained — Feedback Summary Exporter

## 1. 这个 Task 在做什么？（通俗解释）

想象你在用 AI 帮你写微信回复草稿。每次 AI 给你几个候选回复，你会选择：
- **接受**（直接用）
- **编辑**（改了再用）
- **拒绝**（不用）
- **标记边界**（觉得哪里不对劲）

T140 已经把这些选择记录下来了，T141 已经能验证这些记录有没有问题。但你还缺一个东西：**一眼看到整体情况的能力**。

T142 就是那个"总结器"——它把一堆反馈记录变成一个简洁的统计报表，比如：

> "一共 20 条反馈，其中 8 条接受、6 条编辑、4 条拒绝、2 条边界标记。涉及 3 个联系人。保守风格回复被接受最多，热情跟进式回复被拒绝最多。"

关键是：**这个报表只说数字和 ID，不会泄露你具体改了什么、写了什么备注、或者对话原文**。

## 2. 实现详解

### 2.1 任务目标

在 T140（反馈记录）和 T141（反馈验证）之后，实现一个**只读的聚合摘要导出器**。它读取反馈日志，计算各种统计量，输出一份隐私安全的摘要。不修改任何现有数据，不调用 LLM，不触发任何自动学习或更新行为。

### 2.2 任务流程

```
反馈日志 JSON → FeedbackSummaryService.summarize()
  ├─ 加载并校验日志文件（复用 T140 的 Pydantic 模型）
  ├─ 遍历每条记录，累加各种统计量
  │   ├─ 按动作类型计数（accept/edit/reject/boundary）
  │   ├─ 收集去重后的 contact_id、candidate_id、reply_plan_id
  │   ├─ 统计有边界标签、有编辑文本、有用户备注的记录数
  │   └─ 尽力加载引用的 ReplyPlan，提取候选回复的 approach_label
  ├─ 可选：合并 T141 验证报告的聚合数据
  └─ 输出到 stdout 和/或私有 JSON 文件
```

### 2.3 代码变化

#### `src/practical_chat_agent/services/feedback.py`

新增 `FeedbackSummaryService` 类（约 190 行），包含：

- `summarize()` — 主入口，返回聚合摘要字典
- `_init_summary()` — 初始化摘要模板，包含所有聚合字段
- `_load_log()` — 加载反馈日志，处理文件不存在、JSON 损坏、schema 校验失败等情况
- `_resolve_plan_path()` — 解析反馈记录中引用的 ReplyPlan 路径（支持绝对路径、CWD 相对路径、日志目录相对路径）
- `_load_plan_safe()` — 安全加载 ReplyPlan，失败时静默返回 None
- `_get_approach_label()` — 从加载的 ReplyPlan 中匹配候选回复的 approach_label（带缓存）
- `_merge_validation_report()` — 可选合并 T141 验证报告的聚合计数
- `_finalize()` — 可选写入输出文件

关键设计决策：
- 使用 `_plan_cache` 字典缓存已加载的 ReplyPlan，避免同一计划被重复读取
- `_load_log` 和 T141 的加载逻辑保持一致的错误处理模式（`corrupted_reason` 等）
- `_merge_validation_report` 只提取聚合计数，不包含原始的 `record_results` 详情

#### `src/practical_chat_agent/app/main.py`

新增 `chat-reply-feedback-summary` CLI 命令，支持三个参数：
- `--input`（必填）：反馈日志 JSON 文件
- `--output`（可选）：私有输出路径
- `--validation-report`（可选）：T141 验证报告

stdout 输出只包含安全字段（聚合计数、ID 数量、时间范围），不包含任何私人文本。不可读输入导致 exit code 1。

#### `docs/07_handoff.md`

新增 Section 40，记录 T142 的实现细节、验证结果和明确声明未做的操作。

### 2.4 对后续开发的意义

T142 完成了 M4 反馈闭环的最后一个环节——**可见性**。现在 M4 的三个任务形成完整链路：

```
T140（记录反馈）→ T141（验证反馈）→ T142（汇总反馈）
```

这对后续开发的影响：

1. **T160+ 反馈到补丁**：T142 的聚合摘要为 T161（反馈聚类）提供了输入基础——知道哪些 pattern 频繁出现，才知道哪些值得变成偏好补丁
2. **T150/T152 回归测试**：T142 验证了端到端链路的正确性，但缺少提交的自动化测试。T152 需要为整个 M4 CLI 链路（记录→验证→汇总）建立回归保护
3. **数据驱动决策**：有了聚合摘要，人类可以基于统计而非直觉判断 AI 回复的质量趋势，决定是否需要调整策略

## 3. 为什么给出这个 Review 结果？

### 判定：PASS_WITH_WARNINGS

**为什么通过（PASS）：**

1. **任务目标完整达成**：所有要求的聚合字段都已实现（total_records、counts_by_action、counts_by_approach_label、records_with_boundary_label 等）。reason_tag 和 policy_risk_flag 标注为"when available"，当前数据模型没有这些字段，所以正确地跳过了
2. **隐私安全**：stdout 和输出文件经确认不包含任何草稿文本、编辑文本、用户备注、边界备注或原始对话内容。只有聚合计数和去重 ID 数量
3. **严格只读**：不修改任何反馈日志、ReplyPlan、ContactSkill、MemoryFact 或其他文件
4. **不越界**：没有引入 LLM 调用、自动发送、数据库、向量数据库、实时平台集成或 `private/chat_history/` 读取
5. **错误处理合理**：损坏文件、缺失计划、缺失验证报告都有对应的描述性处理

**为什么有警告（WARNINGS）：**

1. **代码重复**：`_resolve_plan_path` 和 `_load_plan_safe` 现在是第三份拷贝（T121、T141、T142 各一份）。不影响正确性，但是技术债务在增长
2. **无提交的自动化测试**：和 T140/T141 一样，验证是通过私有 fixture 手动完成的。从提交的仓库无法复现验证结果。这已经递延到 T150/T152
3. **返回类型是 dict 而非 Pydantic 模型**：和 T140/T141 风格一致，但缺少类型约束。未来如果摘要字段变更，没有编译期保护
4. **raw input_path 在 stdout**：和 T141 相同的已接受问题，`input_path` 没有经过 `_safe_cli_path()` 处理

这些警告都不阻塞发布，但值得在 T150 回归硬化时一起清理。
