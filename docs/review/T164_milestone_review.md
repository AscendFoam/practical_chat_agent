# Milestone Review: T164 M5 Gate

Reviewer: Codex Captain
Date: 2026-05-22
Scope: T160-T164, review-only feedback-to-patch pipeline
Verdict: `Conditional`

## 1. 当前功能是否真的完成

是，按当前定义的 M5 scope 来看已经完成。

M5 的目标不是自动学习、自动应用 patch，或运行时直接改写 `ContactSkill` / `Memory`。M5 的实际目标是把重复反馈转成可审查、可批准、可受控注入的 review-only patch 流水线。这个链条现在已经闭合：

- T160: `PreferencePatchCandidate` schema
- T161: feedback clusterer
- T162: candidate-only patch proposal CLI
- T163: explicit human patch review CLI
- T164: approved-only compact patch context integration

从 `docs/review/T160_review.md` 到 `docs/review/T164_review.md`，五个任务都已通过 review，且没有遗留 blocking issue。当前仓库确实具备一条完整的、approval-gated、non-mutating 的 M5 patch pipeline。

## 2. 是否能从干净环境运行

部分可以，但还不能把整条 M5 流水线描述成“已经从 committed repo contents 充分证明 clean-env reproducible”。

当前可以确认的正面证据：

- `src/practical_chat_agent/app/main.py` 已接入 `chat-feedback-cluster`、`chat-feedback-propose-patch`、`chat-feedback-review-patch`
- `src/practical_chat_agent/services/feedback.py` 中已存在 `FeedbackClusterService`、`PatchProposalService`、`PatchReviewService`、`ApprovedPatchContextService`
- 我实际运行了：
  - `$env:PYTHONPATH='src'; pytest tests/test_t164_synthetic.py`
  - 结果：13 passed
- 我实际运行了：
  - `python -m compileall src/practical_chat_agent/services/feedback.py src/practical_chat_agent/services/chat_context.py src/practical_chat_agent/core/models.py src/practical_chat_agent/app/main.py`
  - 结果：通过

但 clean-env 证据仍然不完整，原因也很明确：

- T161-T163 目前没有 committed automated tests
- 没有一条 committed 的端到端 M5 integration test 覆盖 cluster -> propose -> review -> approved-context
- `pytest` 运行时出现 `.pytest_cache` 写入权限 warning，虽不影响测试通过，但说明当前环境并非完全无摩擦的标准写环境

因此，“可运行”成立于局部验证和任务级 review 证据层面；“整条 M5 已被干净环境完整证明”暂不成立。

## 3. 是否有测试、demo 或实验结果

有，但证据强度不均衡。

现有证据：

- committed tests:
  - `tests/test_t164_synthetic.py`，13 个测试，覆盖 `ApprovedPatchContextService` 的核心筛选与 compact brief 行为
  - T150-T152 的 176 个 committed tests 继续为 M3/M4.5 基线提供可复现保障，但它们不是 M5 直接测试
- reviewed implementation evidence:
  - `docs/review/T161_review.md`
  - `docs/review/T162_review.md`
  - `docs/review/T163_review.md`
  - `docs/review/T164_review.md`
- committed runtime surface:
  - CLI wiring 已在 `main.py` 中落地
  - patch contract 已在 `docs/data_contracts/preference_patch_contract.md` 中成文

缺口同样明显：

- 没有 committed tests 覆盖 T161 clusterer
- 没有 committed tests 覆盖 T162 proposal
- 没有 committed tests 覆盖 T163 review
- 没有 committed end-to-end demo 或 integration test 覆盖整条 M5 链路

所以答案是：有测试和 review 证据，但不足以把 M5 称为“高置信 clean-env fully reproduced milestone”。

## 4. 是否存在伪完成

没有发现 blocking 级别的伪完成，但存在“如果表述不精确就会被误读”的风险。

真实完成的部分是：

- review-only feedback aggregation
- candidate-only patch generation
- explicit human review
- approved-only compact runtime hints

没有完成、也绝不能被写成已完成的部分是：

- automatic learning
- automatic patch apply
- runtime mutation of `ContactSkill` / `Memory`
- outbound behavior changes
- LLM-assisted patch generation
- fully reproducible end-to-end M5 regression coverage

因此，M5 不是伪完成，但它的“完成”必须带限定词：功能上完成，验证上仍是 `Conditional`。

## 5. 其它问题

以下问题不构成 M5 blocker，但都应该明确记录：

- `patch_id` 仍是非确定性的，合同文档对 determinism 的表述有偏差
- cluster / proposal stdout 仍有 `input_path` 暴露的路径处理债务
- `PatchReviewService` 默认写回输入文件，存在写失败时原文件损坏风险
- `review_metadata.history` 可无界增长
- T164 仍缺少三类覆盖：`frozen/archived` exclusion、assembler 端到端集成、empty/whitespace `behavior_instruction`
- `docs/06_eval_protocol.md` 下半部分仍保留较早阶段的 gate 命名与描述，和当前 M4.5/M5 定义并不完全一致，存在治理文档漂移

## Gate M5 Verdict

**`Conditional`**

理由：

- M5 功能链条已经完成，且没有 blocking issue
- 但整条流水线的 committed clean-env reproducibility 仍未被充分证明
- 当前证据足以支持项目继续进入 `T170` 这类 design-only、non-breaking 的 M6 起始任务
- 当前证据不足以把 M5 宣称为“像 M4.5 那样已经被完整回归硬化的里程碑”

## Allowed Next Step

允许继续到：

- `docs/tasks/M6_contactskill_decomposition/T170_decomposition_design.md`

但前提是：

- 保持 M5 的 review-only、approval-gated、non-mutating 解释
- 不把当前状态表述成“自动学习已完成”或“整条 patch pipeline 已有完整回归测试”
