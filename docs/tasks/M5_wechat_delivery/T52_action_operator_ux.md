# Task T52: Action Operator UX

## Task ID

T52

## Goal

增强 action CLI 的 platform/status/context/policy 查看能力，方便人工审批微信回复。

## Why now

人工审批质量依赖可读的上下文和风险解释。

## Allowed files

- `src/practical_chat_agent/app/main.py`
- `src/practical_chat_agent/services/delivery.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不批量自动审批。
- 不默认输出敏感 raw payload。

## Inputs to read

- existing action-list/show/approve/send CLI.
- Policy decision fields.

## Expected output

- `action-list --platform wechat --status pending_approval`
- `action-show --include-policy --include-context`
- JSON and text output remain usable.

## Verification

Run against fixture/pending actions and confirm output includes policy summary.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

