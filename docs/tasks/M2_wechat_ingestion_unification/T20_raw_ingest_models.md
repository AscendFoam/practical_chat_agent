# Task T20: Raw Ingest Models

## Task ID

T20

## Goal

新增 raw message payloads 和 ingest runs 的模型、表和仓储。

## Why now

统一 iLink、desktop、import 前，需要保存原始 payload 和每次导入统计。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/storage/repositories/base.py`
- `src/practical_chat_agent/storage/mysql/models.py`
- `src/practical_chat_agent/storage/mysql/repositories.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不改变 existing `events` 语义。
- 不保存未脱敏测试敏感内容到 examples。

## Inputs to read

- `docs/02_experiment_plan.md` section 7.3
- existing repository patterns.

## Expected output

- `raw_message_payloads` and `ingest_runs` additive storage.
- Repository methods for create/list/update stats.

## Verification

Run compile checks and `init-db` if DB is available.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

