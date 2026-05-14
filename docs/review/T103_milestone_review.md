# Milestone Review: T103 M0 Gate

Review date: 2026-05-14
Author: Codex worker
Task package: `docs/tasks/M0_weflow_data_contract/T103_m0_review.md`
Status: worker draft, pending reviewer confirmation

## Scope

- 只评估 Gate M0，不写代码。
- 只使用 T100-T102 的产物、review 和治理文档作为证据。
- 不读取或输出 `private/chat_history/` 原文。

## Evidence Summary

| 项目 | 主要证据 | 结论 |
| --- | --- | --- |
| T100 schema profile | `docs/data_contracts/weflow_schema_profile.md` 第 1-8 节；`docs/review/T100_review.md` `PASS` | 已确认 WeFlow JSONL 可稳定解析、顶层类型稳定、时间戳/消息类型/回复链路候选明确，并已有脱敏 fixture。 |
| T100 normalized event contract | `docs/data_contracts/normalized_event_contract.md` 第 2-8 节；`docs/review/T100_review.md` `PASS` | 已定义 `event_id`、`source_ref`、`raw_ref`、`sender_role`、`timestamp`、`message_type` 的第一版规则。 |
| T101 privacy / source refs | `docs/data_contracts/privacy_redaction_rules.md` 第 2-7 节；`docs/data_contracts/source_ref_rules.md` 第 2-11 节；`docs/review/T101_review.md` `PASS` | 已明确可提交目录与 `private/` 的边界，以及 `source_ref/raw_ref` 的公开形态。 |
| T102 minimal normalize CLI | `docs/review/T102_review.md` `PASS`；`docs/07_handoff.md` 第 5 节 | 已确认 normalize CLI 可把 WeFlow JSONL 产出到 `private/distilled/`，并限制输入/输出路径与 stdout 泄漏面。 |

## Gate M0 Checklist

依据 `docs/06_eval_protocol.md` 第 2 节 Gate M0：

| Gate M0 要求 | 证据 | 结果 |
| --- | --- | --- |
| 能读取 `private/chat_history` 的 JSONL 并输出字段统计 | `docs/data_contracts/weflow_schema_profile.md` 第 1-3 节；`docs/review/T100_review.md` `PASS` | PASS |
| 不把真实聊天原文写入 docs | `docs/data_contracts/weflow_schema_profile.md` 引言；`docs/review/T100_review.md` / `docs/review/T101_review.md` 的 privacy audit | PASS |
| 明确 normalized event schema | `docs/data_contracts/normalized_event_contract.md` 第 2 节 | PASS |
| 至少生成一个脱敏 fixture | `docs/data_contracts/weflow_schema_profile.md` 第 8 节；`docs/review/T100_review.md` `PASS`；`docs/review/T101_review.md` `PASS` | PASS |
| 明确 `source_ref`、`event_id`、`sender_role`、`timestamp`、`message_type` 规则 | `docs/data_contracts/normalized_event_contract.md` 第 3-7 节；`docs/data_contracts/source_ref_rules.md` 第 2-8 节 | PASS |

## M1 Readiness Assessment

M1 的第一步是把 normalized events 继续切成 chunks，而不是立刻做 LLM 蒸馏。按这个标准看，当前 M0 已经具备进入 M1 的地基：

1. 输入结构已经稳定：T100 给出了 `_type=message` 的字段画像与 message type 候选，T102 已把这些规则实现为最小 normalize CLI。
2. 隐私边界已经明确：T101 把 `docs/examples/tests` 与 `private/` 的边界写清楚，T102 review 也确认 stdout/report 没有把真实原文、真实文件名、真实联系人或真实平台 ID 带进可提交目录。
3. 下游需要的不确定性信号仍被保留：`source_message_type_code`、`interaction_flags`、`risk_flags`、`timestamp_epoch_s` 这些字段让 T110 不必假设当前 normalize 已经“完全理解”所有消息。

## Non-Blocking Conditions

以下问题目前不构成 M0 `Block`，但足以让结论保持 `Conditional`：

1. `type=80` / `chatRecords` 的脱敏 fixture 与自动化覆盖仍不足，需在 T110/T150 延续保守处理并补测试。
2. `sender_role` 已有 `unknown` 和 `risk_flags` 兜底，但单文件场景与额外 `member` 行的稳健性还要在 T114/T150 用真实样本验证。
3. timezone fallback warning、双次读取文件、全量缓存 normalized lines 目前对 38k 行样本可接受，但应在 T110/T150 明确观察并决定是否流式化。
4. `event_id` 继续采用带 `weflow` 命名空间的 SHA-1，在 MVP 阶段可接受；若后续 reviewer 或测试要求更强摘要，再在 T150 前统一调整。
5. 结构化 PII token 替换不在 normalize 阶段完成，T112+ 任何面向 LLM 的蒸馏步骤都必须继续执行 T101 的隐私边界。

## Verdict

**Gate M0 verdict: `Conditional`**

原因：

- `docs/06_eval_protocol.md` 为 Gate M0 列出的硬性条件均已满足。
- T100/T101/T102 都已通过 reviewer `PASS`，没有留下会直接阻止 M1 chunking 的 blocker。
- 但 T102 review 明确留下了一组应被带入 M1 的非阻塞问题，因此更稳妥的 gate 结论是 `Conditional`，而不是 `Allow`。

## Recommended Next Unique Task

若 reviewer 接受本结论，建议下一唯一任务为：

`T110: 实现 conversation chunker v0`

理由：

1. T110 是 M1 的自然起点，直接消费 `normalized_events.jsonl`。
2. T110 最适合承接当前已知条件：保留 `risk_flags`、不要过度相信 `message_type`/`sender_role`、并开始暴露 chunking 对性能与边界信息的需求。
3. 先做 T110，再做 T111/T112，可以让后续摘要和事实抽取建立在已经跑通的 chunk artifact 上。

## Governance Note

按本轮 worker 规则，本草案只给出 M0 gate 建议，不直接把 T103 标记完成，也不切换 `Current Unique Task`。Reviewer / Captain 若接受本结论，再把任务板推进到 T110。
