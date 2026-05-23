# T182 Worker Summary — Candidate Validator

## 改了什么

### 新增文件
- **`src/practical_chat_agent/services/reply_candidate_validator.py`** — 共享确定性校验模块。
  - 模块级函数：`check_text_non_empty`、`check_supporting_refs`、`check_boundary_reminders`、`check_ref_types`、`has_privacy_leak`、`has_impersonation`、`normalize_ranks`、`check_ranks_contiguous`、`check_input_size`。
  - 提供 `VALID_REF_TYPES`、`MAX_INPUT_CHARS`、`_IMPERSONATION_PATTERNS` 常量。
- **`tests/test_reply_candidate_validator.py`** — 共享校验器 46 个确定性测试。

### 修改文件
- **`src/practical_chat_agent/services/llm_reply_generator.py`**：
  - `LLMReplyPlanValidator` 委托 6/7 检查到共享模块。
  - 删除重复代码：`_IMPERSONATION_PATTERNS`、`_refs_are_valid`、`_ranks_are_contiguous`、`_has_privacy_leak`、`_has_impersonation`、`validate_ranks`。
  - 新增 `INPUT_TOO_LARGE` preflight（`generate()` 中调用 provider 前检查）。
  - 新增 `max_input_chars` 构造参数（默认 20000）。
  - 移除 T181 N03 标记的多余 `validate_ranks` 调用。
- **`src/practical_chat_agent/services/reply_planner.py`**：
  - `_validate_plan()` 使用共享 `check_ranks_contiguous()`。
- **`tests/test_llm_reply_generator.py`** — 新增 21 个回归测试（M01-M04，共 47 个测试）。
- **`docs/07_handoff.md`** — 新增 Section 84 T182 Implementation Record。

## 如何验证

```bash
python -m py_compile src/practical_chat_agent/services/reply_candidate_validator.py \
  src/practical_chat_agent/services/llm_reply_generator.py \
  src/practical_chat_agent/services/reply_planner.py \
  src/practical_chat_agent/app/main.py
# COMPILE OK

pytest tests/test_reply_candidate_validator.py -q
# 46 passed

pytest tests/test_llm_reply_generator.py -q
# 47 passed

pytest tests/test_reply_planner.py -q
# Existing tests pass unchanged

pytest tests/ -q
# 420 passed (327 existing + 47 T181/T182 + 46 shared validator), 0 regressions
```

## 剩余风险

1. **Privacy leak 检测仍是确定性 exact-match**：改进为两阶段（完整子串 + 4 词连续序列），但 paraphrase 泄露仍无法检测。
2. **Input-size preflight 用字符数代理 token 数**：可能略微高估或低估实际 provider token 用量，但作为保守的 preflight 充分。
3. **Impersonation 模式是模块级常量**（不可注入）：扩展需修改源码，但可为测试和定制导入检查。
4. **未执行 live provider smoke test**（与 T181 相同约束）。
5. **`ReplyCandidateValidator` 不依赖 `ReplyPlanPolicyEngine._IMPERSONATION_CUES`**：两个独立实现，未来可考虑统一。
