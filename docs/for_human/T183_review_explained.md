# T183 Review 通俗解释

## 1. 这个 Task 在做什么？

T183 是 Milestone 7（LLM 辅助回复规划器）的第三步。

**通俗理解**：之前的 ReplyPlanner（回复规划器）只会用固定的模板生成 3 条备选回复。T183 给它加了一个"混合模式"：你可以在保留模板兜底的前提下，额外让 LLM（如 Deepseek）也生成几条候选回复，然后把模板策略和 LLM 策略合并在一起，输出最终供人审阅的 3 条备选回复。

关键限制：
- **必须是手动开启的**（`--hybrid` 参数），不是默认行为。
- **模板回复永远是安全基线**（第 1 条始终来自模板）。
- **LLM 回复也要经过同样的政策审查（policy assessment）**，不能绕过安全检查。
- **LLM 不可用时不能崩溃**，必须安全降级回纯模板模式。

## 2. 任务的实现细节

### 目标

把 T181（LLM 离线生成器）和 T182（候选回复校验器）的成果整合到主 planner 中，但不改变原有的模板模式行为，也不让 LLM 成为默认选项。

### 实现流程

```
用户请求回复
  → ReplyPlanner.generate()
    → 1. 先生成 3 条模板候选（安全基线）
    → 2. 如果 hybrid_mode=True 且 force_template=False：
         → 调用 LLMReplyGeneratorService.generate()
         → 捕获所有异常，绝不抛出
         → 如果 LLM 拒绝或报错 → 返回空列表
    → 3. 合并：
         → 保留模板候选 1（安全基线）
         → 把最多 2 条 LLM 候选放入 rank 2 和 rank 3
         → 如果不够 3 条，用剩余模板候选补齐
         → 重新标 rank 为连续 1..3
    → 4. 每条候选都经过 policy_engine.assess_candidate() 检查
    → 5. 输出 review-only 的 ReplyPlan
```

### 代码变化

**`reply_planner.py`**（核心修改）：
- 构造函数新增 `llm_generator` 和 `hybrid_mode` 参数
- `generate()` 新增 `force_template` 参数
- 新增 `_generate_llm_candidates()`：安全调用 LLM，永不抛异常
- 新增 `_build_llm_candidate()`：对 LLM 候选执行政策审查
- 新增 `_merge_candidates()`：确定性合并策略
- 更新模板候选差异说明，当有 LLM 候选时加入 LLM 来源提示

**`llm_reply_generator.py`** 和 **`reply_candidate_validator.py`**：
- 修复 T182 N01 bug：`check_input_size()` 签名从 `str` 改为 `int`
- 调用处 `str(estimated_size)` 改为 `estimated_size`

**`main.py`**（CLI 修改）：
- `chat-reply-plan` 新增 `--hybrid` 参数
- 启用时读取 LLM provider 配置构造 generator

**`test_hybrid_reply_planner.py`**（新文件，18 个测试）：
- 向后兼容性：默认 planner 无 LLM
- Opt-in 验证：hybrid_mode 默认 False
- LLM 拒绝降级：无 API key 时安全返回模板
- LLM 异常降级：generator 抛异常时安全返回模板
- `force_template` 覆盖：强制跳过 LLM
- 政策审查不变：候选始终有 risk_flags、boundary_reminders
- 输出合约：始终是 review-only

### 真实联调验证

Worker 用 Deepseek API 做了真实的 hybrid 联调，产出了 3 条混合候选：
1. 模板：中文保守确认（安全基线）
2. LLM：英文热情跟进
3. LLM：英文支持性语气

### 对后续开发的意义

- T184（holdout eval）可以评估 LLM 候选的质量了
- 为后续可能的 LLM planner 改进提供了集成基础设施
- 保留了模板模式兼容性，现有 T150 回归测试全部通过
- `force_template` 参数让上层调用者可以灵活控制

## 3. 为什么我给出了 PASS_WITH_WARNINGS？

### 没有 Blocking Issues

任务目标全部完成：
- ✅ 混合模式是 opt-in，不是默认
- ✅ 模板模式完全向后兼容
- ✅ LLM 候选通过同样的政策审查
- ✅ LLM 拒绝/异常不会崩溃
- ✅ 确定性合并策略
- ✅ 修复了 T182 N01 bug
- ✅ 438 个测试全部通过，0 回归
- ✅ 无违禁范围（no send、no mutation、no impersonation）

### Warnings 原因（标记为 N02）

唯一真正的问题是：**没有提交一个"LLM 候选正常返回→合并→政策审查→重排 rank"的端到端测试**。

18 个测试全部只测了 LLM 拒绝和异常降级路径，没有测 LLM 正常返回候选的合并路径。合并路径只在私有联调中验证过。

但这个风险是 **低风险的**，因为：
- 合并代码简单且确定性强
- 私有联调验证了真实输出
- 代码路径是纯加法，不影响现有模板模式

另外 `.claude/settings.json` 超出了允许文件范围（N01），但这是从 T160 开始每个任务都会有的"工作区配置"，已被一贯接受。

## 4. Worker 文档的补充说明

Worker 的 `T183_worker_summary.md` 写得很完整，没有发现错误。可以补充的几点：

1. **测试盲区**：Worker 没有提到测试只覆盖失败降级路径，没有覆盖 LLM 合并成功路径。这不是 worker 的失误——项目惯例是不 mock LLM 成功路径，这是一个有意的选择。但应该在风险中注明。

2. **`.claude/settings.json` 越界**：Worker 的 Allowed Files 超出提醒中已经包含了这个问题，但没有在剩余风险中显式列出。建议后续任务保持注意。

3. **联调结果的语言问题**：Worker 已经正确地将"LLM 返回英文而模板是中文"记录为观察结果。这是一个真实的整合问题——如果用户期望中文回复，LLM 的 prompt 需要显式指定语言。

整体来说，Worker 的工作质量很高，代码干净、测试覆盖了关键安全路径、文档详细、联调验证充分。
