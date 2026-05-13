# Task T123: Context Integration

## Task ID

T123

## Goal

将 approved ContactSkill 和 approved memory facts 以 compact brief 形式接入 `ChatContext`。

## Why now

Reply planner 需要统一上下文，不应直接读取完整 skill 和全部记忆。

## Allowed files

- `src/practical_chat_agent/services/chat_context.py`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/app/container.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不注入 candidate/rejected/frozen skill。
- 不注入大段原文。

## Inputs to read

- approved skill/memory store from T120-T122.

## Expected output

- ChatContext can carry contact_skill_brief or equivalent field.
- Existing flows still work without skill.

## Verification

Run existing demo-turn or compile check plus fixture context assembly.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

