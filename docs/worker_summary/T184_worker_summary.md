# T184 Worker Summary — Planner Holdout Eval

## 改了什么

### 评估执行

T184 是纯评估任务，不修改 planner/validator/generator 代码。

1. **设计并生成 6 个匿名 holdout 场景**：覆盖 baseline warm (S1)、work coordination (S2)、sensitive boundary (S3)、thin context (S4)、memory-rich (S5)、low-pressure (S6) 六种社交语境。

2. **运行 template vs hybrid 对比评估**：每个场景分别以 `chat-reply-plan`（默认 template 模式）和 `chat-reply-plan --hybrid`（hybrid 模式，使用 Deepseek deepseek-chat）执行，共产生 12 个 ReplyPlan 输出。

3. **跨 6 个维度比较两种模式**：naturalness、evidence usage、boundary adherence、privacy safety、candidate diversity、merge stability。

### 文档

- `docs/review/T184_milestone_review.md` — 新增 milestone review 文档
- `docs/07_handoff.md` — 新增 §86 T184 Eval Record

### 私有评估产物

仅存在于 `private/distilled/t184_holdout_eval/`（gitignored，不提交）：
- 6 个场景的 ChatContext JSON
- 12 个 ReplyPlan 输出（6 template + 6 hybrid）
- `eval_analysis.json` — 结构化对比数据

## 评估结果

| 维度 | Template | Hybrid | Delta |
|------|----------|--------|-------|
| naturalness | 3/5 | 4/5 | **+1** |
| evidence_usage | 3/5 | 3.5/5 | **+0.5** |
| boundary_adherence | 4/5 | 3/5 | **-1** |
| privacy_safety | 5/5 | 5/5 | 0 |
| candidate_diversity | 3/5 | 4/5 | **+1** |
| merge_stability | 5/5 | 5/5 | 0 |

### 核心发现

- **Hybrid 提升自然度和证据使用**：LLM 生成的 draft 更贴近具体场景，S5（memory-rich）中 LLM 直接提及 hiking trip 而 template 保持泛化。
- **Hybrid 边界遵守略降**：policy flag 正确标注但 LLM draft text 可能违背 flag 意图（S4 thin_context 中 LLM 仍提出 engaging questions）。
- **语言混搭问题**：Template 产出中文、LLM 产出英文，review 体验割裂。
- **LLM confidence 偏高**：0.79-0.95 vs template 0.45-0.78，未校准。
- **Approach_label 命名不一致**：hybrid label 混合 snake_case、title case、句子片段。

### Gate M7 (Holdout Eval Stage) Verdict

**Conditional**，需满足以下条件才能推进到下一 M7 任务：
1. 语言一致性 — LLM 应与 template 使用同种语言（中文）
2. 安全约束执行 — LLM draft text 必须尊重 thin_context/boundary_sensitive flag
3. Approach_label 规范化 — hybrid label 应与 template 保持相同命名约定
4. Merge success path 回归测试 — 需添加 committed synthetic valid-candidate merge test

## 如何验证

```bash
# 1. 确认 review 文档存在且无隐私泄露
cat docs/review/T184_milestone_review.md | grep -ci "private\|真实\|姓名\|phone\|email\|address"
# 期望：仅出现 safe private/distilled/ 路径引用

# 2. 确认私有产物路径
ls private/distilled/t184_holdout_eval/contexts/
ls private/distilled/t184_holdout_eval/plans_template/
ls private/distilled/t184_holdout_eval/plans_hybrid/
ls private/distilled/t184_holdout_eval/eval_analysis.json

# 3. 确认测试套件未受影响
pytest tests/ -q
# 期望：438 passed, 0 regressions

# 4. 确认 handoff 更新
grep "T184 Eval Record" docs/07_handoff.md
# 期望：找到 §86 T184 Eval Record
```

## 剩余风险

1. **语言混搭**：English LLM candidates 与 Chinese template candidates 并列，review 体验不一致。
2. **安全约束 bypass**：LLM draft text 在 thin_context/boundary_sensitive 场景下与 policy flag 意图不一致。
3. **LLM confidence 未校准**：持续偏高可能误导 reviewers。
4. **Hybrid merge 无 committed 回归测试**：T183 遗留的 M01 gap 仍未关闭。
5. **Approach_label 不一致**：可能影响下游 feedback clustering 等消费者。
6. **评估规模**：6 个 synthetic 场景足够暴露关键问题，但不足以全面代表真实对话多样性。
