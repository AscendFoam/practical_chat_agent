# Task T130: ReplyPlan Schema

## Task ID

T130

## Goal

定义 ReplyPlan schema 和 prompt contract，输出多候选草稿、rationale、risk flags 和引用记忆。

## Why now

回复 planner 需要强结构输出，便于 policy 和用户 review。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/reply_plan_contract.md`
- `docs/07_handoff.md`

## Forbidden scope

- 不调用 LLM。
- 不发送消息。

## Inputs to read

- `docs/02_experiment_plan.md`
- T123 context integration.

## Expected output

- ReplyPlan includes candidates, style rationale, boundary checks, cited refs.

## Verification

Compile if models added.

## Docs to update

- `docs/data_contracts/reply_plan_contract.md`
- `docs/07_handoff.md`

## Reviewer type

normal

