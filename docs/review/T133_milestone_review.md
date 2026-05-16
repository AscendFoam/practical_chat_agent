# Milestone Review: T133 Holdout Eval

Review date: 2026-05-16
Author: Codex worker
Task package: `docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`
Status: worker draft, pending reviewer confirmation

## Scope

- 仅对 T130-T132 的 ReplyPlanner 做匿名 holdout 评估。
- 只看允许文件和 private/distilled 下的私有评测产物。
- 不修改 planner 代码，不进入 M4，不写自动发送或平台接入。

## Method

- 评测样本数：6
- 样本类型：baseline、work、敏感边界、thin context、false-positive probe、false-negative probe
- 检查点：ReplyPlan 结构、候选数、priority_rank、refs、boundary flags、隐私面

## Results

| Metric | Result |
| --- | --- |
| sample_count | 6 |
| valid_reply_plan_rate | 6/6 |
| candidate_count_ok_rate | 6/6 |
| naturalness_rating | 3/5 |
| boundary_adherence_rating | 4/5 |
| evidence_usage_rating | 3/5 |
| privacy_leakage_findings | 0 committed leaks |

## Findings

### Correctness

- 6 个样本都生成了有效 `ReplyPlan`，且每个 plan 都有 3 个候选。
- `contact_id`、`priority_rank` 和 compact source context 都保持一致。
- 没有把 raw transcript 或 full store JSON 写进提交文档。

### Safety

- 敏感边界样本和 thin-context 样本都会更保守，这一点是对的。
- 但 false-positive probe 说明边界检测仍偏宽，容易把普通工作式语境推到保守模式。
- false-negative probe 说明某些更隐性的 pacing / delayed-reply 线索还可能没被充分抬高。

### Quality

- 文案整体可读，且保持 review-only、低压、非代言口吻。
- 但整体还是模板驱动，关系感知偏浅，`strategy_hints` / `relationship_summary` 的效果还不够强。

### Testing Gaps

- 目前只有私有 synthetic holdout，没有 committed regression tests。
- 还没有 clean-env 级别的广覆盖证明，T150 仍需要补自动化回归。

## Gate M3 Verdict

**Conditional**

## Conditions

1. 保持 ReplyPlanner review-only，不把本次结果当成自动发送或平台接入证明。
2. T150 必须补 committed regression 覆盖，至少包括结构、边界敏感、thin-context、false-positive 和 subtle false-negative 场景。
3. 在更广的样本上重新校准边界触发与 pacing heuristics，再把“关系感知已成熟”写成事实。

## Private Artifacts

- `private/distilled/t133_holdout_eval/contexts/*.context.json`
- `private/distilled/t133_holdout_eval/plans/*.reply_plan.json`
- `private/distilled/t133_holdout_eval/eval_summary.json`
