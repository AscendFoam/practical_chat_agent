# Task T21: Dedupe Service

## Task ID

T21

## Goal

实现微信消息 dedupe service，按 iLink、desktop OCR、import 三类来源生成 canonical key。

## Why now

同一条微信消息可能从多个来源进入，必须防止重复记忆和重复 action。

## Allowed files

- `src/practical_chat_agent/services/dedupe.py`
- `src/practical_chat_agent/services/ingestion.py`
- `examples/payloads/wechat_*`
- `docs/07_handoff.md`

## Forbidden scope

- 不直接删除 raw payload。
- 不把 skip 记录静默丢弃。

## Inputs to read

- `docs/02_experiment_plan.md` section 7.4
- existing event repository.

## Expected output

- Dedupe key strategy implemented.
- Duplicate events are skipped or linked while raw payload stats record skipped count.

## Verification

Run fixture ingestion twice and prove only one canonical event is created or would be created in dry-run mode.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

