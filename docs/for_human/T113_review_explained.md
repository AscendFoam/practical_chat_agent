# T113 Review Explained: ContactSkill Builder

## 1. 这个 Task 是什么？通俗解释

想象你在微信上有一个很久没联系的同学。你们之间的聊天记录已经被导出到了本地文件。之前的步骤（T110-T112）已经把这些聊天记录"切块"、"总结"、"提取了关键事实"。

现在的问题是：**这些总结和事实，能不能组装成一份"这个联系人档案"？**

这份档案不是用来"假装那个人说话"的——它更像是一份**对话策略备忘录**，告诉你："跟这个人聊天的时候，什么话题可以聊、什么话题要小心、建议用什么语气"。

T113 就是实现这个"组装"步骤：把上游产生的"总结"和"事实"合成为一份候选人档案（ContactSkill candidate），再生成一份人类可以审阅的 Markdown 文档。**重点是：这份档案只是候选，必须人工看过才能用。**

打个比方：
- T102 做的是"把原始聊天记录翻译成统一格式"
- T110 做的是"把统一格式的记录按对话切成块"
- T112 做的是"让 AI 总结每块在聊什么，提取关键事实"
- T113 做的是"把所有总结和事实汇总成一份联系人策略档案"

## 2. 实现详细解释

### 2.1 任务目标

T113 的核心目标是：

1. **消费上游产物**：读取 T112 生成的 `chunk_summaries.jsonl`（对话块摘要）和 `memory_facts.jsonl`（记忆事实）。
2. **生成候选档案**：把这些信息合成一个 `ContactSkillCandidate`，包含关系状态、沟通风格、话题偏好、情感模式、回复策略等。
3. **生成人类审阅文档**：输出一份 Markdown 格式的审阅文档，让人能看懂每一条判断来自哪些证据。
4. **严格约束**：档案状态只能是"candidate"（候选），不能自动变为"approved"（已批准）；不能保存原始聊天原文；不能生成"模拟联系人说话"的内容。

### 2.2 任务流程

```
chunk_summaries.jsonl + memory_facts.jsonl
       ↓
ContactSkillBuilderService.build_contact_skill()
       ↓
  1. 读取并校验 JSONL 文件（Pydantic schema 验证）
  2. 按 contact_id 过滤（支持指定联系人）
  3. 用启发式规则推断关系类型、沟通风格等
  4. 组装 ContactSkillCandidate
  5. 调用 Markdown exporter 生成审阅文档
  6. 写出 candidate.json + review.md + 更新 run_report.json
       ↓
private/distilled/<run_id>/
  contact_skill.candidate.json   ← 机器可读的候选档案
  contact_skill.review.md        ← 人类可读的审阅文档
```

### 2.3 代码变化详解

#### 文件 1: `src/practical_chat_agent/services/contact_skill.py`

这是最核心的文件，从一个轻量辅助模块重写为完整的 builder 服务。

**主要组件**：

- `ContactSkillBuilderService`：主服务类
  - `build_contact_skill()`：主入口，协调整个构建流程
  - `_build_candidate()`：组装候选档案，强制 `status="candidate"`
  - `_build_relationship_state()`：推断关系状态（亲密程度、信任等级、互动频率等）
  - `_build_communication_style()`：推断沟通风格（消息长度、语气、直接程度等）
  - `_build_preferred_topics()` / `_build_avoid_topics()`：基于事实中的关键词提取偏好/回避话题
  - `_build_reply_strategy()`：生成回复策略建议
  - `_build_review_notes()`：生成审阅提醒（比如"有转发内容风险"）

**关键设计决策**：

1. **纯启发式，不调 LLM**：所有推断都基于关键词匹配和简单计算，不依赖大模型。这是故意的——避免引入新的幻觉风险。
2. **保守默认值**：`closeness` 的基础值只有 0.22，需要足够的事实才能慢慢涨上去。
3. **断言检查**：`_assert_candidate()` 确保输出一定有 evidence_refs 且状态是 candidate。
4. **路径安全**：`_ensure_within_root()` 确保输入输出都限制在 `private/distilled/` 内。

**局限性**（也是 review 中指出的）：

- 关键词列表（`_CONCERN_TOKENS` 等）和话题映射（`_extract_topic`）是针对当前考试准备样本写的，换个联系人类型可能不太好用。
- `initiative_balance` 是按事实数量推断的，不是按实际消息方向推断的——比较粗糙。

#### 文件 2: `src/practical_chat_agent/exporters/contact_skill_markdown.py`（新文件）

这是一个纯粹的渲染模块，把 `ContactSkillCandidate` 转成人类可读的 Markdown。

**输出结构**：
- 概览（关系类型、状态、置信度、敏感度）
- 关系状态（亲密程度、信任等级、互动频率等）
- 沟通风格（消息长度、语气、回复延迟等）
- 偏好话题 / 回避话题
- 重要事件
- 稳定偏好 / 情感模式
- 用户侧偏好 / 回复策略
- 使用边界（明确禁止 persona clone、impersonation 等）
- 审阅提醒
- 来源快照（显示用了哪些 chunk 和 fact）
- 参考事实列表

**安全措施**：
- `_safe_text()` 函数会遮罩邮箱、手机号、URL、长数字、姓名，并截断超长文本（120字符）。
- 每个段落都显示 evidence_refs，让人能追溯到具体证据。
- 末尾有明确提醒："Do not use this artifact to simulate how the contact would speak."

#### 文件 3: `src/practical_chat_agent/app/main.py`

只增加了一个新 CLI 命令 `chatlog-build-contact-skill`，带参数：
- `--input`：输入目录或文件路径
- `--output`：输出目录（默认与输入相同）
- `--contact-id`：可选的联系人过滤
- `--dry-run`：只打印报告不写文件

#### 文件 4: `docs/07_handoff.md`

新增了第 15 节，记录 T113 的实现状态。关键点：
- 明确写了"当前仅为 implementation ready"，没有把任务标记为已完成。
- 记录了验证命令、样本输出确认和待审风险。

### 2.4 对后续开发的意义

T113 在整个离线蒸馏管线中的位置：

```
T102 (normalize) → T110 (chunk) → T112 (summarize + extract facts) → T113 (build skill) → T114 (run full sample)
```

T113 完成后，后续任务可以：

- **T114**：在一个更大的样本上跑完整管线，人工抽查 evidence 是否可靠。
- **T120**：把 ContactSkill 接入持久化存储（文件 store 或数据库）。
- **T121**：实现 evidence validator，验证证据引用确实能回溯到原始事件。
- **T130/T131**：基于已审批的 ContactSkill 生成联系人感知的回复草稿。

T113 的核心价值是：**第一次把分散的"总结"和"事实"整合成一个结构化的、可审阅的、有明确使用边界的联系人策略档案。** 虽然当前的启发式方法比较粗糙，但它确立了关键模式——一切都要有证据、一切都要人工审阅、绝不能模拟联系人说话。

## 3. 为什么给出 PASS_WITH_WARNINGS？

### 总体判断

T113 完成了任务包要求的所有内容：
- 实现了 ContactSkill builder
- 实现了 Markdown review exporter
- 候选档案保持了 `status="candidate"`
- 所有字段都有 evidence_refs
- 没有自动审批、没有保存原文、没有模拟联系人说话
- CLI 工作正常，编译通过
- 文档没有把计划写成事实

没有发现任何需要返工的 blocking 问题，所以不是 BLOCK。

### 为什么不是纯 PASS？

有 5 个非阻塞性问题值得记录：

1. **`_build_report` 被调用了两次**（N01）：在非 dry-run 路径中，报告构建函数被调用了两次——一次写入文件，一次返回结果。不影响正确性，但是浪费计算。归类为 accepted，不影响后续。

2. **启发式关键词过度贴合当前样本**（N02）：`_CONCERN_TOKENS`（"worry", "concern", "pressure"）和 `_extract_topic` 的映射（"target school" -> "school plans"）明显是为当前考试准备样本写的。换一个同事或家人的样本，这些规则可能几乎不会触发。这不是 bug——任务包明确说"先选 1 个高价值联系人或一个小样本"——但后续需要注意。归类为 accepted/deferred。

3. **置信度计算是公式化的**（N03）：比如 `closeness = 0.22 + min(len(contact_facts), 6) * 0.08` 是按事实数量线性增长的，不是基于证据质量的加权。这会让置信度数字看起来精确但实际上是拍脑袋的。不过因为候选档案需要人工审阅，审阅者可以看到并调整这些数字，所以影响有限。归类为 accepted/deferred。

4. **缺少 `__init__.py`**（N04）：新建的 `exporters/` 目录没有 `__init__.py`。Python 3 可以工作，但不一致。归类为 accepted。

5. **有未使用的函数**（N05）：`collect_reference_fact_ids` 定义了但没有被调用。无功能影响。归类为 accepted。

### 结论

T113 实现了任务包的全部要求，没有越界，安全约束全部满足。非阻塞问题都是"当前启发式方法比较粗糙"和"小样本局限"类的——这些是已知的、被任务包和项目计划接受的 MVP 限制。后续任务（T114 的全量样本抽查、T120+ 的存储和校验）会进一步暴露和解决这些问题。

因此判定为 **PASS_WITH_WARNINGS**，可以继续推进到 T114。
