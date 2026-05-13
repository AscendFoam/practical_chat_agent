# Task T120: File Store Models

## Task ID

T120

## Goal

新增离线 memory/skill 文件 store 和 Pydantic 模型，先不强制接数据库。

## Why now

MVP 产物需要稳定加载、版本化和供 runtime 使用。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/contact_skill.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不做 migration。
- 不引入向量数据库。

## Inputs to read

- M1 output contracts.

## Expected output

- Load/save candidate and approved skill/memory files.
- Preserve status and evidence refs.

## Verification

Compile and run minimal load/save on redacted fixture.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

