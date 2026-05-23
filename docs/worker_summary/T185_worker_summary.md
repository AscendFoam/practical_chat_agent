# T185 Worker Summary — Hybrid Planner Language and Safety Alignment

## 改了什么

### 代码改动

**`src/practical_chat_agent/services/llm_reply_generator.py`** (主要改动):

1. **System prompt 语言强制** — 新增规则 6，要求 LLM 所有 `draft_text` 使用中文输出，与 template 语言保持一致，解决 T184 评估发现的语言混搭问题。

2. **Safety constraints 加强** — 重写规则 4，详细说明 thin_context 和 boundary_sensitive 场景下 LLM 必须遵循的安全指引。同时在 `_build_llm_input()` 中添加自动安全上下文检测：
   - 当 `approved_store_context.status` 为 `not_configured` 或 `no_runtime_ready_records` 时，向 LLM 输入注入 `thin_context` 标记
   - 当 `derived_brief_context.boundary.sensitivity_summary` 包含 `sensitive` 或 `high` 时，注入 `boundary_sensitive` 标记
   - 系统提示要求 LLM 必须遵守这些安全标记的指引

3. **Approach_label 规范化** — 新增 `_normalize_label()` 静态方法，将 LLM 返回的任意格式标签统一转换为 `snake_case`（转小写、非字母数字字符替换为下划线）。在 `_build_candidates()` 中应用，确保 hybrid 标签与 template 标签保持相同命名约定。

4. **`import re`** — 新增正则支持用于标签规范化。

**`tests/test_hybrid_reply_planner.py`** (新增测试):

5. **Merge success path 回归测试** — 新增 `TestHybridMergeSuccessPath` 测试类（3 个测试用例），使用 `_MockSuccessGenerator` 返回预制有效 LLM candidates（不调用真实 provider）。验证：
   - template[0] 始终保留为 safety baseline
   - LLM candidates 替换 template 2+ 位
   - merge 后 3 个 candidates rank 为连续的 1..3

### 未修改文件

- `reply_planner.py` — 无需改动，merge 逻辑已正确
- `app/main.py` — 无需改动，CLI 接口不变
- `test_llm_reply_generator.py` / `test_reply_candidate_validator.py` — 不受影响

## 验证结果

```bash
# 编译检查
python -m py_compile src/practical_chat_agent/services/llm_reply_generator.py \
                    src/practical_chat_agent/services/reply_planner.py \
                    src/practical_chat_agent/app/main.py
# 通过

# 专项测试
pytest tests/test_hybrid_reply_planner.py -q    # 21 passed (3 new)
pytest tests/test_llm_reply_generator.py -q     # 47 passed
pytest tests/test_reply_candidate_validator.py -q # 46 passed

# 全量回归
pytest tests/ -q  # 441 passed, 0 regressions
```

## 剩余风险

1. **LLM 行为非完全确定** — 系统提示和安全上下文引导 LLM 行为，但 LLM 仍可能在边界情况下生成非中文或违反安全约束的文本。确定性 validator（impersonation/privacy 检测）作为第二道防线。
2. **安全上下文检测基于启发式** — 当前通过 `approved_store_context.status` 和 `boundary.sensitivity_summary` 判断 thin/sensitive 条件。更精确的方式是直接使用 `ReplyPlanPolicyEngine`，但这超出了 generator 范围。
3. **LLM confidence 仍未校准** — T184 发现的 0.79-0.95 偏高范围未在本任务处理。
4. **标签规范化可能截断过长的 LLM 标签** — 转换为 snake_case 保持一致性但可能丢失部分信息。
5. **Template-only 行为不变** — 已验证全部 438 个既有测试通过，无需修改。
