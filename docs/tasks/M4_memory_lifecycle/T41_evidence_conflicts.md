# Task T41: Evidence And Conflicts

## Task ID

T41

## Goal

实现 memory evidence 查看和 conflict group 可视化，并在 retrieval 中降低冲突记忆的注入优先级。

## Why now

记忆必须可解释，冲突事实不能同时高置信注入 prompt。

## Allowed files

- `src/practical_chat_agent/services/memory_retrieval.py`
- `src/practical_chat_agent/services/memory_lifecycle.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不自动删除冲突记忆。
- 不隐藏冲突证据。

## Inputs to read

- T40 implementation.
- existing memory retrieval code.

## Expected output

- `memory-evidence-show <memory_id>`
- `memory-conflict-list`
- retrieval notes mention conflict handling.

## Verification

Use fixture memories in same conflict group and confirm prompt/retrieval behavior.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

