# T183 Worker Summary — Hybrid ReplyPlanner

## 改了什么

### 核心逻辑：`reply_planner.py`

- `ReplyPlanner` 新增 `hybrid_mode` (bool, 默认 `False`) 和 `llm_generator` (optional `LLMReplyGeneratorService`) 构造参数。
- `generate()` 新增 `force_template` 参数，即使 hybrid 模式下也可强制跳过 LLM。
- 新增 `_generate_llm_candidates()`：调用 LLM generator，捕获所有异常，永不抛出。
- 新增 `_build_llm_candidate()`：对 LLM candidate 执行 `policy_engine.assess_candidate()`，确保和 template candidate 一致的政策审查。
- 新增 `_merge_candidates()`：确定性的合并策略——保留 template candidate 1 作为安全基线，替换 2+ 为最多 2 个 LLM candidates，填充至恰好 3 个，重新标 rank 为 1..3。
- 更新 `_build_candidate_difference_notes()`：当有 LLM candidates 时添加 LLM 来源说明。
- 所有异常/拒绝场景安全降级为 template-only，不会崩溃。

### T182 N01 修复

- `check_input_size()` 签名从 `(serialized_json: str)` 改为 `(size: int)`。
- `LLMReplyGeneratorService.generate()` 调用处传 `estimated_size` (int) 而非 `str(estimated_size)`。

### CLI：`main.py`

- `chat-reply-plan` 新增 `--hybrid` flag（默认 False）。
- 启用时读取 LLM provider 配置构造 `LLMReplyGeneratorService`。

### 测试：`test_hybrid_reply_planner.py` (18 tests)

1. **向后兼容**：默认 planner 无 LLM，输出有效的 3-candidate ReplyPlan。
2. **Opt-in**：`hybrid_mode` 默认 False，必须显式启用。
3. **LLM 拒绝降级**：无 API key 时 hybrid 模式返回 template-only，不崩溃。
4. **LLM 异常降级**：generator 抛出异常时 hybrid 模式返回 template-only。
5. **`force_template`**：覆盖 hybrid 模式强制 template-only。
6. **Policy 审查**：所有 candidate 携带 risk_flags、boundary_reminders、confidence。
7. **输出合约**：始终 `candidate_review_only`，有效 schema，可审查 candidate。
8. **CLI**：`--hybrid` 被接受，provider 不可用时仍产出有效 ReplyPlan。

### Live provider smoke test

使用 `.env` 中 Deepseek API key 执行 hybrid smoke run：

```bash
# 合成 ChatContext → chat-reply-plan --hybrid
# provider: Deepseek (api.deepseek.com)
# 模型: deepseek-chat

PYTHONPATH=src 'python' -m practical_chat_agent.app.main \
  chat-reply-plan \
  --input private/distilled/t183_smoke/context.json \
  --output private/distilled/t183_smoke/hybrid_plan.json \
  --hybrid
```

结果：**成功，3 candidates 产出**

| Rank | 来源 | approach_label | draft_text | confidence |
|------|------|----------------|------------|------------|
| 1 | Template (安全基线) | conservative_acknowledgment | 收到，我先接住你这条消息。 | 0.78 |
| 2 | **LLM (Deepseek)** | enthusiastic follow-up | That's awesome! Congrats on the new gig. What part of it is intense so far? | 0.90 |
| 3 | **LLM (Deepseek)** | casual support | Nice! Glad it's going well. Intense can be good—hope you're settling in okay. | 0.85 |

合并规则验证通过：
- Template candidate 1 作为安全基线保留（中文，保守确认）
- LLM candidate 1 替换 rank 2（英文，热情跟进，带 follow-up 问题）
- LLM candidate 2 替换 rank 3（英文，支持性语气，低压）
- Policy assessment 已应用：`boundary_reminders` 含 "stay friendly and relaxed"
- 最终输出：`plan_mode=candidate_review_only`，3 candidates，ranks 1..3 连续
- 输出写入 `private/distilled/t183_smoke/hybrid_plan.json`（私密路径，不提交）

## 如何验证

```bash
python -m py_compile src/practical_chat_agent/services/reply_planner.py \
  src/practical_chat_agent/services/llm_reply_generator.py \
  src/practical_chat_agent/services/reply_candidate_validator.py \
  src/practical_chat_agent/app/main.py
# COMPILE OK

pytest tests/test_hybrid_reply_planner.py -q
# 18 passed

pytest tests/test_reply_planner.py -q
# Existing tests pass unchanged

pytest tests/test_llm_reply_generator.py -q
# 47 passed

pytest tests/test_reply_candidate_validator.py -q
# 46 passed

pytest tests/ -q
# 438 passed (420 existing + 18 new), 0 regressions
```

## 剩余风险

1. **LLM candidate 质量未评估**：T183 只做集成，质量判断留给 T184 holdout eval。
2. **合并规则未验证真实 LLM 输出多样性**：保留 template[0] + 替换 2+ 的规则是确定性的，单次 smoke test 不足以评估多样性。
3. **单 LLM candidate 填充**：如果 LLM 只返回 1 个合法 candidate，合并会用 template 填充，可能产生混合风格输出。
4. **LLM candidate 使用英文**：当前 prompt 不指定语言，Deepseek 返回了英文 draft。如果期望中文回复，需要在 prompt 中显式指定。
5. **重复 `input_path` 在 ChatContext 输出中**：与 T141 N01 相同的已知问题，CLI stdout 包含 `input_path`。
