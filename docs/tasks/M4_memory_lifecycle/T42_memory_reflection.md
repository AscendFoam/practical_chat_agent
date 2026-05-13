# Task T42: Memory Reflection

## Task ID

T42

## Goal

实现 `memory-reflect`，按时间窗口生成带证据引用的反思记忆或 profile snapshot。

## Why now

ContactSkill 和长期关系管理需要周期性摘要，而不是无限读取原始聊天。

## Allowed files

- `src/practical_chat_agent/services/memory_lifecycle.py`
- `src/practical_chat_agent/services/chat_memory.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不生成无证据总结。
- 不覆盖用户手工纠错。

## Inputs to read

- existing memory/profile snapshot logic.
- `docs/02_experiment_plan.md` section 9.2.

## Expected output

- CLI supports agent/user/time window.
- Reflection includes evidence refs and status.

## Verification

Run against fixture events/memories and inspect output.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

