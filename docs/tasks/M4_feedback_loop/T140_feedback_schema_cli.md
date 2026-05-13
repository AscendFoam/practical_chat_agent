# Task T140: Feedback Schema CLI

## Task ID

T140

## Goal

定义用户反馈日志 schema，并实现 accept/edit/reject/boundary feedback 的最小 CLI。

## Why now

长期 agent 需要从用户修改中学习，但不能直接无审查修改记忆。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不训练模型。
- 不自动改 ContactSkill。

## Inputs to read

- ReplyPlan schema.

## Expected output

- Feedback records include draft_id/action, diff/ref, user note, timestamp.

## Verification

Run CLI on redacted draft fixture.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

