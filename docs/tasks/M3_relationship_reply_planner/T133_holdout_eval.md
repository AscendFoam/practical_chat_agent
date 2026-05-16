# Task T133: Holdout Eval

## Task ID

T133

## Goal

对 T130-T132 的 ReplyPlanner 做匿名 holdout evaluation，判断当前 M3 是否可以进入下一里程碑。

评估重点不是继续开发功能，而是回答：当前 review-only reply planner 是否在自然度、边界遵守、证据使用、risk flags 可解释性和隐私安全上足以作为后续 feedback loop 的基础。

## Why Now

T130 已固定 `ReplyPlan` contract，T131 已实现 review-only planner wiring，T132 已加入 policy/boundary 风险层。下一步必须用 holdout 场景验证它不是只会套模板，也不能把未验证质量写成已完成事实。

## Allowed Files

- `docs/review/T133_milestone_review.md`
- `docs/07_handoff.md`
- private eval outputs under `private/distilled/**`

## Forbidden Scope

- 不修改 planner、policy、model、CLI 或任何 `src/**` 代码。
- 不提交 holdout 原文、真实联系人名、真实平台 ID、真实文件名或可识别 private content。
- 不读取或输出 `.env`。
- 不自动发送，不接实时平台，不接数据库，不引入向量库。
- 不推进 M4/T140。
- 不把缺少样本、缺少测试或质量不足写成完成事实。

## Inputs To Read

- `docs/review/T130_review.md`
- `docs/review/T131_review.md`
- `docs/review/T132_review.md`
- `docs/data_contracts/reply_plan_contract.md`
- `docs/tasks/M3_relationship_reply_planner/T133_holdout_eval.md`
- `docs/06_eval_protocol.md`
- Existing private synthetic or redacted eval outputs under `private/distilled/**`, if available.

## Required Evaluation Questions

The milestone review must explicitly answer:

- 当前功能是否真的完成到 M3 scope。
- ReplyPlanner 是否能从当前环境运行；如果没有 clean-env proof，必须如实记录。
- 是否有测试、demo 或实验结果；区分 inline synthetic verification、private eval、committed tests。
- 是否存在伪完成，例如把 template baseline 写成强 relationship-awareness。
- 是否允许进入 M4；允许时必须说明条件，不允许时必须说明 blocking gap。

## Suggested Metrics

Use anonymized counts or ratings only. Do not quote private chat text.

- `sample_count`: holdout scenarios evaluated.
- `valid_reply_plan_rate`: valid T130 `ReplyPlan` output rate.
- `candidate_count_ok_rate`: at least 3 candidates rate.
- `naturalness_rating`: human rating, e.g. 1-5.
- `boundary_adherence_rating`: human rating, e.g. 1-5.
- `evidence_usage_rating`: whether refs/rationales are useful and not over-claiming.
- `privacy_leakage_findings`: count and severity; should be zero for committed artifacts.
- `policy_false_positive_notes`: anonymized notes for over-conservative outputs.
- `policy_false_negative_notes`: anonymized notes for missed boundary / impersonation / over-proactivity risk.

## Expected Output

Create `docs/review/T133_milestone_review.md` with:

- Scope and input artifacts.
- Anonymized evaluation methodology.
- Results table or concise metric summary.
- Findings grouped by correctness, safety, quality, and testing gaps.
- Gate M3 verdict: `Allow`, `Conditional`, or `Block`.
- If `Conditional`, list exact conditions carried into M4/T150.
- If `Block`, list the smallest blocking fixes needed before another review.

Update `docs/07_handoff.md` with:

- T133 eval record.
- Gate M3 verdict.
- Next recommended task, but do not execute it.

## Verification

- Confirm generated docs contain no raw private chat content.
- Confirm no `src/**` files changed.
- Confirm `docs/review/T133_milestone_review.md` exists.
- If private eval outputs are produced, keep them under `private/distilled/**`.
- Run `git diff -- docs/review/T133_milestone_review.md docs/07_handoff.md` and inspect for privacy leakage before reporting completion.

## Reviewer Type

milestone

Reviewer should judge whether the milestone review is evidence-backed and privacy-safe, not whether the planner code could be improved in the abstract.
