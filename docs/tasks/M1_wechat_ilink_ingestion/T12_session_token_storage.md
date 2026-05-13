# Task T12: Session And Token Storage

## Task ID

T12

## Goal

新增 additive schema 和 repository 支持 platform accounts、sessions、conversation context tokens。

## Why now

微信增量监听需要持久化账号、cursor、session 状态和 context token。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/storage/repositories/base.py`
- `src/practical_chat_agent/storage/mysql/models.py`
- `src/practical_chat_agent/storage/mysql/repositories.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不破坏 existing tables。
- 不改已有字段含义。
- 不引入 Alembic unless Captain explicitly changes task.

## Inputs to read

- `docs/02_experiment_plan.md` section 6.5
- existing action repository patterns.

## Expected output

- Pydantic records for platform account/session/context token.
- SQLAlchemy tables via `create_schema`.
- Repository methods for add/upsert/get/list.

## Verification

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main init-db
```

If DB is unavailable, run compile checks and document DB verification gap.

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if DB verification cannot run

## Reviewer type

adversarial

