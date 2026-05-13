# Task T60: Trigger Models

## Task ID

T60

## Goal

新增 trigger_rules 和 scheduled_actions 模型、表和仓储。

## Why now

主动关系管理必须建立在可审计的 schedule/action 模型上。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/storage/repositories/base.py`
- `src/practical_chat_agent/storage/mysql/models.py`
- `src/practical_chat_agent/storage/mysql/repositories.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不执行后台 scheduler。
- 不发送消息。

## Inputs to read

- `docs/02_experiment_plan.md` section 11.3.
- action repository patterns.

## Expected output

- Additive tables and repository methods.
- Status supports disabled/pending/draft/action linked states.

## Verification

Compile and DB init if available.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

