# T182 Review Explained

## 1. 这个 Task 在做什么？（通俗版）

T182 是"给聊天助手的 AI 草稿生成器加安全护栏"的第二步。

**背景故事**：在 T181 中，worker 做了一个独立的 AI 草稿生成器（`chat-reply-generate-llm`），生成的草稿要经过 7 道检查才能用。但这 7 道检查是写在 LLM 生成器内部的，普通模板规划器（ReplyPlanner）用不了。

T182 的任务有三件事：

1. **提取共享校验器**：把这 7 道检查从 LLM 生成器里抽出来，放到一个独立模块（`reply_candidate_validator.py`）里，这样普通模板规划器和 LLM 生成器都能用。
2. **关闭 T181 的遗留问题**：T181 review 发现了 9 个待处理事项（5 个代码注意事项 + 4 个测试缺口），T182 要逐个修复。
3. **实现输入大小检查**：T181 定义了 `INPUT_TOO_LARGE` 拒绝码但从没触发过，T182 要实现这个预检。

简单说：**把安全校验规则变成共享库，修复上一轮的遗留问题，加一个新的输入大小预检**。

## 2. 实现详解

### 2.1 修改了哪些文件？

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `services/reply_candidate_validator.py` | **新建** | 共享确定性校验模块，9 个函数 |
| `tests/test_reply_candidate_validator.py` | **新建** | 46 项共享校验器测试 |
| `services/llm_reply_generator.py` | 修改 | 委托校验到共享模块，新增 INPUT_TOO_LARGE 预检 |
| `services/reply_planner.py` | 修改 | 使用共享的 `check_ranks_contiguous()` |
| `tests/test_llm_reply_generator.py` | 修改 | 新增 21 项回归测试（M01-M04） |
| `docs/07_handoff.md` | 修改 | 新增 Section 84 T182 完成记录 |
| `.claude/settings.json` | 修改 | 新增测试命令的权限条目（工作区工件） |

### 2.2 新增共享校验模块（reply_candidate_validator.py）

不再使用类包装，而是模块级别的纯函数：

| 函数 | 说明 |
|------|------|
| `check_text_non_empty(draft_text)` | 草稿文本不能为空 |
| `check_supporting_refs(refs)` | 至少 1 个上下文引用 |
| `check_boundary_reminders(reminders)` | 至少 1 个边界提醒 |
| `check_ref_types(refs)` | 所有引用类型在 `VALID_REF_TYPES` 中（6 种） |
| `has_privacy_leak(draft_text, context_texts)` | **双级检查**：完整子串 + 4 词连续序列 |
| `has_impersonation(draft_text)` | 正则检测冒充模式 |
| `normalize_ranks(candidates)` | 重编号为 1..N（原地修改） |
| `check_ranks_contiguous(candidates)` | 检查排名的连续性和唯一性 |
| `check_input_size(serialized_json, max_chars)` | 字符数代理 token 预算检查 |

### 2.3 隐私泄露检测改进（T181 N04 修复）

T181 只有一级检测：完整子串匹配（min 8 字符）。T182 新增第二级：**4 个连续词序列匹配**。如果草稿中出现了上下文里的连续 4 个词（不管位置），也判定为泄露。

例如：
- 上下文："my cat likes to sleep on warm surfaces"
- 草稿："I remember you mentioned your cat likes to sleep on the sofa."
- 检测到 4 词序列 "cat likes to sleep" → 标记泄露

这仍然不是语义级检测，但比 T181 的逐字照搬检测更强。

### 2.4 INPUT_TOO_LARGE 预检（T181 N05 修复）

在调用 provider 前，估算总输入大小（system prompt + 序列化的 llm_input），超过 `max_input_chars`（默认 20000）时返回结构化拒绝。

```python
estimated_size = len(system_prompt) + len(input_json)
if not check_input_size(str(estimated_size), max_chars=self.max_input_chars):
    return self._refusal(code="INPUT_TOO_LARGE", ...)
```

```
⚠️ 注意：这里有一个调用 bug——str(estimated_size) 把整数转成了字符串，
导致 check_input_size 检查的是字符串长度而不是字符数，
所以 INPUT_TOO_LARGE 实际上永远不会触发。
详见 N01 说明。
```

### 2.5 回归测试覆盖（T181 M01-M04 修复）

| 缺口 | 测试数 | 说明 |
|------|--------|------|
| M01 `_build_llm_input` 输出形状 | 7 | 最小上下文、skill brief、memory facts、derived briefs、approved patches、空 ID、事件计数 |
| M02 `_parse_provider_response` 错误路径 | 10 | 缺失 choices、空列表、非列表、非 dict choice、缺失 message、非 dict message、空内容、无效 JSON、非对象 JSON、有效响应 |
| M03 generator→validator 流水线 | 2 | 完整合成流水线、隐私泄露过滤验证 |
| M04 CLI stdout 隐私回归 | 2 | dry-run 模式和生成模式均断言无草稿文本泄露 |

### 2.6 ReplyPlanner 的共享化改动

`reply_planner.py` 中原有的内联排名检查（检查唯一性和连续性）现在改用共享的 `check_ranks_contiguous()`。行为不变，错误信息改为合并的一条。这是安全的提取重构，不改变 planner 策略选择逻辑。

### 2.7 对后续开发的意义

1. **T183（混合规划器）** — 共享校验器就位后，可以安全地将 AI 生成的候选与确定性候选合并排序，因为两边的校验逻辑是同一个。
2. **T184（评估）** — 有了共享校验基线，可以在 holdout 场景中统一评估草稿质量。
3. **后续扩展** — `has_privacy_leak` 和 `has_impersonation` 都是模块级函数，可以独立增强而不影响调用方。

## 3. 为什么给出 PASS_WITH_WARNINGS？

### 任务目标都完成了吗？大部分 ✅

- ✅ 提取共享校验器层 — `reply_candidate_validator.py`，9 个函数
- ✅ 显式校验检查 — 全部 7 项 + 排名归一化 + 输入大小
- ✅ 隐私泄露检测改进 — 从单级变为双级
- ✅ INPUT_TOO_LARGE 预检 — **尝试实现但有一个调用 bug（N01）**
- ✅ M01-M04 回归测试 — 全部覆盖（21 + 46 = 67 项新测试）
- ✅ handoff 更新 — Section 84，准确完整
- ✅ 没有越界做新生成路径、混合规划器、默认 LLM、发送/平台集成
- ✅ 420 项测试全部通过，零回归

### 为什么不是 BLOCK？

核心任务目标（提取共享校验器、关闭 T181 测试缺口）全部高质量完成。N01 的 INPUT_TOO_LARGE bug 不影响系统安全（provider 错误处理仍能兜底），修复成本极低（一行代码）。

### 为什么不是 PASS？

N01 的 INPUT_TOO_LARGE preflight 调用 bug 导致这个验收标准不满足。虽然没有安全风险，但代码给人虚假的安全感，而且 T181 N05 "INPUT_TOO_LARGE 定义了但从不触发"在实质上仍然存在。这个 bug 应该在进入 T183 前修复。

N02 的 `.claude/settings.json` 超范围是延续了从 T160 以来的模式，已被一致接受。

## 4. Worker 文档准确性评估

### docs/07_handoff.md Section 84 ✅

准确完整。正确列出了：
- 新增文件和修改文件
- 共享校验器的函数清单和常量
- LLMReplyPlanValidator 的委托重构
- INPUT_TOO_LARGE preflight（未提及调用 bug，这本应由 reviewer 发现）
- ReplyPlanner 的共享化改动
- M01-M04 回归测试覆盖
- 验证结果（420 passed）
- 剩余风险

### docs/worker_summary/T182_worker_summary.md ✅

准确且更简洁。与 handoff 内容一致，额外提到：
- `check_ranks_contiguous` 替代 `_validate_plan` 的内联检查
- Privacy leak 改进为两阶段
- `ReplyCandidateValidator` 不依赖 `ReplyPlanPolicyEngine._IMPERSONATION_CUES`

**可补充**：两个文档都没有提到 `INPUT_TOO_LARGE` 调用的潜在问题（reviewer 也应在此时发现）。这属于 review 环节的职责，不要求 worker 返修。
