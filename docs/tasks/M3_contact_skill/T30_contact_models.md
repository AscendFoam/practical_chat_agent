# Task T30: Contact Models

## Task ID

T30

## Goal

新增 contacts 和 contact_skills 的 Pydantic schema、数据库表和仓储。

## Why now

ContactSkill 是微信主线区别于普通 bot 的核心中间层。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/storage/repositories/base.py`
- `src/practical_chat_agent/storage/mysql/models.py`
- `src/practical_chat_agent/storage/mysql/repositories.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不生成 LLM skill。
- 不注入 prompt。

## Inputs to read

- `docs/02_experiment_plan.md` section 8.2
- existing memory/profile models.

## Expected output

- Contact and ContactSkill records.
- status/confidence/evidence/redaction fields.
- repository roundtrip support.

## Verification

Compile and DB schema initialization if available.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

