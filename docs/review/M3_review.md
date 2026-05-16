# M3 Review: Relationship Reply Planner

Reviewer: Codex Captain
Date: 2026-05-16
Scope: T130-T133, review-only `ReplyPlan` / `ReplyPlanner` / policy layer / holdout eval
Verdict: `Conditional`

## 1. 当前功能是否真的完成

M3 在结构目标上已经完成：T130 定义了 `ReplyPlan` contract，T131 实现了 review-only planner，T132 增加了 boundary/policy 风险层，T133 完成了匿名 synthetic holdout eval，并确认 6/6 场景可生成有效 3-candidate plan。

但这不是“关系感知质量成熟版”。当前 drafts 仍主要由 deterministic templates 驱动；T133 记录的 naturalness 为 3/5，evidence usage 为 3/5。因此 M3 只能视为安全结构和 review-only wiring 完成，而不是最终回复质量完成。

## 2. 是否能从干净环境运行

不能完全证明。现有证据证明当前开发环境中 compile、CLI synthetic verification 和 T133 private eval 能运行；但尚无 committed regression tests / fixtures 能在干净环境中复现 ReplyPlanner 的关键路径。

结论：当前环境可运行，clean-env reproducibility 尚未充分证明，必须由 T150 补齐。

## 3. 是否有测试、demo 或实验结果

有实验结果，但测试硬化不足：

- T131/T132 有 inline synthetic verification 和 compile 记录。
- T133 有 6 个 synthetic anonymized holdout scenarios，覆盖 baseline friend、practical colleague、sensitive boundary、thin context、false-positive probe、false-negative probe。
- T133 private artifacts 位于 `private/distilled/t133_holdout_eval/**`，未进入 git。
- 尚无 committed automated tests / fixtures。

## 4. 是否存在伪完成

未发现明显伪完成。T133 没有把 template-driven baseline 写成 strong relationship-awareness，也没有隐藏 naturalness/evidence usage 的限制。

主要风险是后续文档或 worker 误把 M3 的 `Conditional` 解释为“回复质量已经成熟”。这不允许。M3 当前只证明 review-only planner 的结构、安全边界和基础 policy behavior 可继续迭代。

## 5. 是否允许进入下一里程碑

允许以 `Conditional` 进入 M4/T140，但必须带条件：

1. ReplyPlanner 继续保持 review-only；不允许 auto-send、realtime platform integration、LLM drafting expansion。
2. T150 必须新增 committed regression tests，覆盖结构、boundary sensitivity、thin context、false positives、subtle false negatives、privacy leakage、contact alignment 和 ranking。
3. 在更大样本重新校准前，不得宣称 relationship-aware maturity。

## T133 Review Decision

`docs/review/T133_review.md` verdict = `PASS_WITH_WARNINGS`。

Captain decision: accept reviewer verdict. T133 is complete; Gate M3 is `Conditional`; next recommended Current Unique Task is T140 Feedback Schema CLI, but do not execute T140 in this Captain step.

Warning disposition:

- N01 accepted: self-reported ratings are acceptable for MVP milestone; T150 may add independent review.
- N02 accepted: 6 synthetic scenarios are reasonable under T133 constraints.
- N03 accepted: naturalness 3/5 is honestly reported; condition 3 prevents maturity overclaim.
- N04 accepted: evidence usage 3/5 is honestly reported; structural refs are present.
- N05 accepted: omission of H01/H02 detailed notes is minor because summary confirms all six plans succeeded.

No deferred warnings and no rejected warnings from T133 review.

## Next Task Recommendation

Proceed to T140 Feedback Schema CLI only under M3 conditions. T140 should record human feedback on candidate drafts, not mutate memory/ContactSkill automatically and not send messages.
