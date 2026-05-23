# M7 Review: LLM-Assisted ReplyPlanner

Reviewer: Codex Captain
Date: 2026-05-23
Scope: T180-T185, optional LLM candidate generation / validation / hybrid planning / holdout evaluation / alignment hardening
Verdict: `Allow`

## 1. 当前功能是否真的完成

是，在 M7 既定范围内已经完成。

M7 需要证明的不是“回复质量已经成熟到可自动使用”，而是“在不破坏既有 review-only、privacy、boundary、compact-context contract 的前提下，引入一个可选的 LLM candidate 路径，并把关键风险收敛到可审查状态”。

这条链路现在已经闭合：

- T180: 定义可选 `LLMReplyPlan` / candidate contract，不改 runtime。
- T181: 提供离线、私有输出的 LLM candidate CLI。
- T182: 抽取并加固 template / LLM 共用的 deterministic validator。
- T183: 把 template planner 和可选 LLM candidates 合并为 opt-in hybrid planner，保留 template baseline 和 fallback。
- T184: 用匿名 holdout 场景验证 hybrid 路径的质量收益与剩余缺口。
- T185: 修复 T184 暴露的四个 gate 条件：语言对齐、thin_context / boundary_sensitive prompt-level safety、`approach_label` 归一化、merge success path committed regression coverage。

因此，M7 的“optional LLM-assisted ReplyPlanner”目标已经完成；未完成的是更高一级的质量成熟度、confidence calibration 和更强的 post-generation enforcement，这些不属于 M7 必备闭环。

## 2. 是否能从干净环境运行

可以，达到通过本里程碑 gate 所需的可复现程度。

当前证据显示，M7 的关键行为已具备 committed tests，而不是只依赖私有手工验证：

- T181/T182/T183/T185 的实现均有 committed test coverage。
- `tests/test_hybrid_reply_planner.py` 现已覆盖 hybrid fallback、opt-in behavior、policy assessment，以及 T185 新增的 merge success path。
- `tests/test_llm_reply_generator.py` 与 `tests/test_reply_candidate_validator.py` 覆盖 generator / validator 关键路径。
- handoff 记录显示 `pytest tests/ -q` 达到 441 passed，无回归。

仍需明确：live provider holdout 和 smoke run 不是 clean-env gate 的一部分，因为它们依赖外部 provider 与私有输入；但这并不阻止 M7 作为“可选 LLM 规划层”进入下一里程碑。

## 3. 是否有测试、demo 或实验结果

有，而且证据链完整。

- 测试：
  - generator / validator / hybrid planner committed tests
  - T185 新增 3 个 merge success path regression tests
  - 全量 `pytest tests/ -q` 通过
- demo / smoke：
  - T183 记录了 live provider smoke，证明 hybrid 路径确实能跑通
- 实验：
  - T184 在 6 个匿名 holdout 场景上比较了 template 与 hybrid 输出
  - 结果显示 hybrid 在 naturalness 和 evidence usage 上有提升，同时暴露了语言、安全提示和标签规范问题
  - T185 已对这些问题做窄范围修复

这对 M7 来说足够，因为本里程碑的目标是“安全、可审查地接入可选 LLM candidate 路径”，不是完成最终质量宣称。

## 4. 是否存在伪完成

未发现阻塞性的伪完成。

当前实现没有把以下内容伪装成已完成：

- 没有把 hybrid planner 写成 default planner。
- 没有把 prompt-level language/safety alignment 伪装成绝对强约束。
- 没有把 holdout 结果写成“质量已成熟”。
- 没有绕过 validator、policy gate、review-only contract 或 compact-context boundary。
- 没有把 live provider smoke 当作 committed reproducibility 的替代品。

仍然存在真实但可接受的遗留：

- safety context detection 仍是 heuristic，不是 policy-engine-native 信号。
- Chinese enforcement 仍是 prompt-level，不是 post-generation hard validator。
- LLM confidence calibration 仍未解决。

这些都已被明确记录为风险或 accepted warning，而不是被包装成“已彻底解决”。

## 5. 是否允许进入下一里程碑

允许，以 `Allow` 进入 M8，从 T190 `RelationshipState schema` 开始。

允许进入的理由：

- M7 的四个 gate 条件已被 T185 关闭。
- hybrid path 仍保持 opt-in、review-only、template-compatible。
- committed regression coverage 已足以支撑后续在不重开 M7 的前提下继续推进。

进入 M8 的前提仍然保留：

- 不允许把 M7 解释为“已可自动发送”或“已可无人值守使用”。
- 后续 RelationshipState 只能走 schema -> signal -> delta -> review -> context -> eval 的 review-first 路径。
- 若未来 mixed-language、heuristic safety drift 或 confidence calibration 在真实评估中再次成为问题，应在后续任务中显式处理，而不是倒退修改 M7 结论。

## Remaining Risks Carried Forward

- R039: LLM 质量与置信度仍可能被过度解读；M7 完成不等于自动化 readiness。
- R040: 后续 M8+ 仍必须维持 compact-context / anonymized-input 边界，不得引入 raw transcript shortcut。
- R041: approved patches、derived briefs、future relationship state 都必须保持 review-only interpretation，而非隐式自动学习。
- R069: safety-context detection 仍是 heuristic，若后续发现误报/漏报，应考虑与 `ReplyPlanPolicyEngine` 做更强对齐。
- R070: Chinese output alignment 仍依赖 prompt discipline，若混语再次成为真实问题，需要后续加入 post-generation detection / enforcement。
- R071: LLM confidence calibration 尚未完成，当前分数不应被解释为校准概率。

## Required Next Task

Proceed to `docs/tasks/M8_relationship_state/T190_relationship_state_schema.md`.
