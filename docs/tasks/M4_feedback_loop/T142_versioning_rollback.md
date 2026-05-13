# Task T142: Versioning Rollback Freeze

## Task ID

T142

## Goal

实现 skill/memory version diff、rollback 和 freeze 机制。

## Why now

用户必须能撤销错误记忆和错误关系判断。

## Allowed files

- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不物理删除 private 原始数据，除非用户另行明确要求。
- 不自动覆盖 frozen 项。

## Inputs to read

- T120 file store.
- T141 proposals.

## Expected output

- Version history, diff view, rollback, freeze commands.

## Verification

Run version/diff/rollback on redacted fixture skill.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

