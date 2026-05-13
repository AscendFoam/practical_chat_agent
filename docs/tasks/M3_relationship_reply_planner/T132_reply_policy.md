# Task T132: Reply Policy

## Task ID

T132

## Goal

为 ReplyPlanner 增加边界、禁忌话题和过度主动风险检查。

## Why now

关系感知不只是更亲近，也包括知道何时收住。

## Allowed files

- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/services/policy.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不降低 outbound policy 安全性。
- 不允许自动发送。

## Inputs to read

- T131 implementation.
- ContactSkill avoid_topics/boundaries.

## Expected output

- Sensitive/boundary scenarios produce conservative candidate or no-reply suggestion.
- Risk flags explain why.

## Verification

Run redacted boundary fixtures.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

