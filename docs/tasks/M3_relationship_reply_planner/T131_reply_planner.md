# Task T131: Relationship-Aware Reply Planner

## Task ID

T131

## Goal

实现基于 ContactSkill 和 memory 的 ReplyPlanner，生成 3 个候选回复草稿。

## Why now

这是验证“关系感知”是否能改善回复建议的核心 runtime。

## Allowed files

- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不发送消息。
- 不冒充联系人。
- 不输出 roleplay。

## Inputs to read

- T130 schema.
- existing `ChatSuggestionService` style.

## Expected output

- CLI or service can generate candidates from a redacted scenario.
- Output includes rationale and cited memory/skill refs.

## Verification

Run on redacted fixture context.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

