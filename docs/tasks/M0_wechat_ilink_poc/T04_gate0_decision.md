# Task T04: Gate 0 Decision

## Task ID

T04

## Goal

汇总 T00-T03 的 POC 证据，给出 Gate 0 `Allow`、`Conditional` 或 `Block` 结论。

## Why now

只有 Gate 0 通过，后续 worker 才能开始 M1 主仓库代码任务。

## Allowed files

- `docs/wechat_ilink_poc_notes.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden scope

- 不修改 `src/practical_chat_agent/**`。
- 不添加 SDK 依赖。
- 不把条件性结论写成已完全通过。

## Inputs to read

- `docs/wechat_ilink_poc_notes.md`
- `docs/02_experiment_plan.md`
- `docs/06_eval_protocol.md`
- T00-T03 reviewer reports if present.

## Expected output

- `docs/wechat_ilink_poc_notes.md` 有完整能力矩阵和 Gate 0 结论。
- `docs/05_decision_log.md` 记录是否进入 M1。
- `docs/07_handoff.md` 指向下一唯一任务：T10 if Allow/Conditional，或回退任务 if Block。
- `docs/08_risks_and_open_questions.md` 更新未解决问题。

## Verification

- Gate 0 checklist 全部有证据或明确缺口。
- 结论与证据一致。

## Docs to update

- `docs/wechat_ilink_poc_notes.md`
- `docs/05_decision_log.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer type

milestone

