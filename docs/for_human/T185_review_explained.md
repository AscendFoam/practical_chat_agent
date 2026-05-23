# T185 Review 通俗解释

## 1. 这个 Task 在做什么？

T185 是 Milestone 7（LLM 辅助回复规划器）的第五步，也是**修复步骤**。

**通俗理解**：T184 的评估发现混合模式有 4 个问题：
1. **语言混搭**：模板回复是中文，LLM 回复是英文 → 看着别扭
2. **安全约束被绕过**：policy 说"别问私人问题"，但 LLM 还是问了
3. **标签命名混乱**：有的 snake_case、有的标题大小写、有的句子片段
4. **缺少回归测试**：没有测试能验证 LLM 正常返回候选时的合并逻辑

T185 的任务就是修这 4 个问题。不扩大功能，不改默认行为，只做窄范围修复。

## 2. 任务实现详解

### 目标

修复 T184 评估发现的 4 个问题，让混合模式更安全、更一致。

### 实现方式

Worker 只改了两个文件：

**`llm_reply_generator.py`**（核心改动）：

1. **语言强制**（修复问题 1）：
   - 在系统提示中新增规则 6：所有 `draft_text` 必须用中文（中文）写
   - LLM 如果遵守提示，就会输出中文

2. **安全约束加强**（修复问题 2）：
   - 在 `_build_llm_input()` 中新增自动检测：
     - 如果 `approved_store_context` 状态为 `not_configured` 或 `no_runtime_ready_records` → 向 LLM 输入注入 `thin_context` 标记
     - 如果 `boundary.sensitivity_summary` 包含 "sensitive" 或 "high" → 注入 `boundary_sensitive` 标记
   - 更新系统提示规则 4，要求 LLM 必须遵守这些安全标记
   - 例如：有 `thin_context` 标记时，LLM 被告知不要问 engaging questions

3. **标签规范化**（修复问题 3）：
   - 新增 `_normalize_label()` 方法，将任意格式标签统一为 snake_case
   - 转换规则：转小写 → 非字母数字变下划线 → 去首尾下划线 → 合并连续下划线
   - 例如："Direct and professional" → "direct_and_professional"
   - 在 `_build_candidates()` 中调用，确保所有 LLM 标签经过规范化

**`tests/test_hybrid_reply_planner.py`**（修复问题 4）：

4. **新增合并成功路径测试**：
   - 新增 `TestHybridMergeSuccessPath` 测试类（3 个测试用例）
   - 使用 `_MockSuccessGenerator` 返回预制有效 LLM candidates（不调真实 provider）
   - 验证：
     - template[0] 始终保留为 rank 1（安全基线）
     - LLM candidates 替换 template 的 2、3 位
     - 合并后 3 个 candidates 的 rank 为连续的 [1, 2, 3]

### 未修改的文件

- `reply_planner.py` — 不需要改，merge 逻辑已正确
- `app/main.py` — 不需要改，CLI 接口不变

### 改动规模

| 文件 | 新增行 |
|------|--------|
| `llm_reply_generator.py` | ~30 行（safety context 检测 + prompt 更新 + normalize_label） |
| `test_hybrid_reply_planner.py` | ~100 行（3 个新测试 + MockSuccessGenerator） |
| `.claude/settings.json` | 权限条目更新（同 T160+ 一贯模式） |

### 对后续开发的意义

1. **Gate M7 的 4 个条件全部解决**：语言一致、安全约束、标签规范、回归测试都有了
2. **T183 的 M01/M02 缺口关闭**：现在有 committed 测试覆盖 LLM 正常返回场景的合并路径
3. **M8（RelationshipState）可以启动了**：前提是 Captain 裁定 T185 满足 Gate M7 条件
4. **遗留问题**：LLM 自信度校准（0.79-0.95 偏高）仍未处理，但这超出了 T185 范围

## 3. 为什么我给出了 PASS_WITH_WARNINGS？

### 没有 Blocking Issues

所有验收条件都满足：
- ✅ LLM 输出语言现在要求中文 → 规则 6 加入 prompt
- ✅ thin_context / boundary_sensitive 场景的 draft 被约束 → safety_context 检测 + 更新规则 4
- ✅ 标签命名规范化 → `_normalize_label()` 方法
- ✅ 合并成功路径有 committed 回归测试 → `TestHybridMergeSuccessPath`（3 tests）
- ✅ 纯模板模式不变 → 438 个既有测试全部通过

没有伪实现、没有 hardcode、没有过度工程。

### Warnings 原因（N01-N03）

**N01 — settings.json 越界**：同 T160+ 每个任务的一贯模式。

**N02 — 安全检测基于启发式**：
- `thin_context` 检测看的是 `approved_store_context.status`，可能不精确
- `boundary_sensitive` 检测用的是字符串包含匹配（"sensitive" 或 "high"），可能误报
- 但这是 prompt 级别的改进，第二道防线有 policy engine

**N03 — 语言要求是 prompt 级别的，不是硬约束**：
- LLM 可能不遵守"用中文"的指令，但检查 LLM 实际输出语言需要实时调用
- 这是一个已知的权衡，worker 已在剩余风险中注明

### 和 T183/T184 review 的对比

| Task | 核心问题 | Verdict |
|------|----------|---------|
| T183 | 缺 LLM 合并成功路径测试（M01） | PASS_WITH_WARNINGS |
| T184 | 评估发现 4 个问题 | PASS_WITH_WARNINGS |
| T185 | 修复了这 4 个问题，有 3 个 minor warnings | **PASS_WITH_WARNINGS** |

## 4. Worker 文档的补充说明

Worker 的 `T185_worker_summary.md` 写得完整准确，没有发现错误。以下是可以补充的几点：

1. **`_normalize_label()` 的 LLM 默认标签处理**：如果 LLM 返回空字符串的 approach_label，代码先回退到 `"llm_generated"` 再 normalization，最终为 `"llm_generated"`。这和模板的命名风格一致。

2. **MockSuccessGenerator 的标签已预规范化**：测试中 `"llm_candidate_1"` 和 `"llm_candidate_2"` 已经是 snake_case，所以它们不经过 `_normalize_label()` ——这是合理的，因为测试测的是 merge 路径不是 normalization。

3. **设置文件越界已按一贯模式标注**：没有额外风险。

4. **T185 可以关闭 M7 的所有 4 个条件**：如果 Captain 认可，Gate M7 可以从 `Conditional` 推进到 `Allow`。剩余的唯一开放问题是 LLM confidence 校准（已从 T184 确认但不属于 T185 修复范围）。
