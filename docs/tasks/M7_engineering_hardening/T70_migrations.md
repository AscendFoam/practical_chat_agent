# Task T70: Migrations

## Task ID

T70

## Goal

引入 Alembic baseline 或等价 migration 方案，降低 schema 演进风险。

## Why now

微信、联系人、触发器和媒体表增加后，`create_schema` 已不足以管理变更。

## Allowed files

- `pyproject.toml`
- `migrations/**`
- `alembic.ini` if Alembic is chosen
- `src/practical_chat_agent/storage/mysql/**`
- `src/practical_chat_agent/app/main.py` if `init-db` behavior changes
- `docs/07_handoff.md`

## Forbidden scope

- 不破坏现有数据库。
- 不删除 existing migrations without explicit approval.

## Inputs to read

- current `migrations/001_initial_schema.sql`
- SQLAlchemy models.

## Expected output

- Baseline migration documented.
- `init-db` path clear: create database, then run migrations or explain fallback.

## Verification

Run migration on a safe/dev database or document exact reason not run.

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer type

adversarial

