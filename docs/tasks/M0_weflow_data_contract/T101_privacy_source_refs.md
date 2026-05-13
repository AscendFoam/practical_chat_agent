# Task T101: Privacy Rules And Source Refs

## Task ID

T101

## Goal

设计本项目处理 WeFlow 聊天记录的隐私脱敏规则、source_ref/raw_ref 规则和最小红线测试样例。

## Why now

离线蒸馏会触碰私密聊天内容，必须在写 parser 和 LLM 抽取前定义隐私边界与证据引用规则。

## Allowed files

- `docs/data_contracts/privacy_redaction_rules.md`
- `docs/data_contracts/source_ref_rules.md`
- `examples/payloads/weflow_redacted_sample.jsonl`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden scope

- 不修改 `src/**`。
- 不复制真实原文。
- 不实现脱敏器。
- 不做 LLM 抽取。

## Inputs to read

- T100 outputs.
- `docs/02_experiment_plan.md`
- `docs/06_eval_protocol.md`

## Expected output

- 明确 PII 类型和替换策略。
- 明确哪些字段可进入 docs/examples/tests，哪些只能留在 private。
- 明确 event_id/source_ref 不泄露真实文件名的规则。
- 更新 redacted sample 以覆盖 source_ref。

## Verification

- 人工检查 sample 无真实标识。
- 规则能解释 T100 中发现的隐私风险字段。

## Docs to update

- `docs/data_contracts/privacy_redaction_rules.md`
- `docs/data_contracts/source_ref_rules.md`
- `docs/07_handoff.md`

## Reviewer type

adversarial

