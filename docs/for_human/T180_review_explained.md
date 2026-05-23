# T180 Review Explanation

## 1. 这个任务在做什么？（通俗解释）

T180 是 M7 阶段的第一个任务，目标非常狭窄：**写一份说明书（contract），定义将来如果要用 AI 大模型帮助生成回复草稿，输入和输出应该长什么样**。

这个任务**不调用任何 AI 模型**，也**不改任何代码**——只是把规则写清楚，让后续任务（T181）知道该做什么。

打个比方：
- T131/T132 是现有的"模板回复生成器"（确定性的，不调用 AI）
- T180 在画一个"未来 AI 回复生成器"的设计蓝图
- 蓝图的作用是确保未来 AI 生成的东西能和现有系统兼容，且不引入安全风险

## 2. 实现细节

### 任务目标

为可选的 LLM 辅助回复候选生成器定义输入/输出合约，确保：
- 与现有 T130 `ReplyPlan` 结构兼容
- 不突破 T123/T164/T174 已有的 compact-context 边界
- 确定性的验收边界（生成可非确定，验收必须确定）
- 隐私、反冒充、安全约束

### 任务流程

1. 读取 T180 任务包和所有上游文档（合约、架构、handoff 等）
2. 阅读 M6 的评审记录和 M7 的约束条件
3. 编写合约文档 `docs/data_contracts/llm_candidate_generator_contract.md`
4. 更新 `docs/07_handoff.md` 追加 T180 Implementation Record
5. 做 23 项合约完整性自检

### 文件/配置变化

**新建文件：**
- `docs/data_contracts/llm_candidate_generator_contract.md` — 核心产物，包含：
  - 输入合约：LLM 只能使用 T123/T164/T174 已达成的 compact-context 输入，不能访问原始聊天记录或完整 store JSON
  - 输出合约：定义 `LLMReplyPlan`（扩展自 T130 `ReplyPlan`），增加了 `generator_type`、`generation_metadata`、`refusal` 字段
  - 拒绝形状（Refusal Shape）：5 种结构化拒绝码
  - 确定性验证边界：7 项验收检查
  - 隐私/反冒充规则：禁止 impersonation、禁止 contact simulation、禁止无证据的关系猜测

**修改文件：**
- `docs/07_handoff.md` — section 80 记录了合约内容、安全约束、T181 可做的和仍禁止的事项

### 对后续开发的意义

- T181 可以基于这份合约直接实现离线 LLM Candidate Generator CLI
- T182 可以基于第 7 节的验证期望实现确定性校验器
- T183 可以安全地实现 hybrid ReplyPlanner（合并确定性和 LLM 候选）
- 整个 M7 阶段有了清晰的第一块基石

## 3. 为什么给出 PASS？

给出 `PASS` 而非 `PASS_WITH_WARNINGS` 的原因：

1. **任务目标完整达成**：合约覆盖了任务包要求的所有 10 项输出（ReplyPlanCandidate 兼容、candidate type、rationale、supporting refs、boundary reminders、隐私/反冒充规则、schema validation 期望、失败/拒绝形状、确定性验证边界、review-only 说明）
2. **只改了 Allowed files**：仅修改了 `docs/data_contracts/` 和 `docs/07_handoff.md`，没有碰任何代码文件
3. **没有越界行为**：没有调用 LLM、没有改 ReplyPlanner、没有改 policy engine、没有加发送逻辑
4. **没有伪实现**：这是一个纯文档任务，不需要 mock/stub/hardcode
5. **合约具体到 T181 可以直接用**：输入字段表、输出 JSON shape、拒绝码、验证检查列表都足够具体
6. **文档不夸大事实**：没有声称 LLM 候选已启用、生产就绪或质量已验证

没有任何阻塞性问题（Blocking Issues），也没有非阻塞性问题（Non-Blocking Issues）。

## 4. 对 Worker 产出/解释的补充说明

Worker 没有写 review 或 explanation 文档（这是正常的，任务包没有要求 worker 写这些）。Worker 的总结报告准确反映了合约内容、验证结果和剩余风险。

补充一点治理层面的建议：
- T180 的变更**尚未提交到 git**，需要 Captain 或后续 worker 提交
- `docs/04_task_board.md` 中的 T180 条目还被标记为 `[ ]`，需要 Captain 更新为 `[x]` 并设置 Current Unique Task 为 T181
