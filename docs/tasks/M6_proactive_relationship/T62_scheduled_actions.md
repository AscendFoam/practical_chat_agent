# Task T62: Scheduled Actions

## Task ID

T62

## Goal

实现 scheduled action 生成器，根据 trigger 和 ContactSkill/memory 生成 follow-up draft action。

## Why now

这是主动关系管理的最小产品闭环，但仍必须是审批草稿。

## Allowed files

- `src/practical_chat_agent/services/triggers.py`
- `src/practical_chat_agent/services/chat_suggestions.py` if prompt support needed
- `src/practical_chat_agent/runtime/agent_runtime.py` if action creation reuse needed
- `docs/07_handoff.md`

## Forbidden scope

- 不真实发送。
- 不创建骚扰式高频触发。
- 不在无联系人上下文时生成强假设内容。

## Inputs to read

- T61 CLI.
- ContactSkill and memory services.

## Expected output

- scheduled action links trigger/contact/platform/channel/action_id.
- status is `PENDING_APPROVAL` or `DRAFT_ONLY`.

## Verification

Run trigger once for test contact and show action pending approval.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

