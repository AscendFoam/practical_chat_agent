# Task T61: Trigger CLI

## Task ID

T61

## Goal

实现 trigger create/list/disable/run-once 和 scheduled-action-list/show CLI。

## Why now

主动触发必须可人工创建、查看、禁用和单次运行。

## Allowed files

- `src/practical_chat_agent/app/main.py`
- `src/practical_chat_agent/services/triggers.py`
- `src/practical_chat_agent/app/container.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不自动后台运行。
- 不绕过 policy 直接发送。

## Inputs to read

- T60 models.
- existing action CLI UX.

## Expected output

- CLI commands from `02_experiment_plan.md` section 11.4.
- `trigger-run-once` only creates draft/pending action.

## Verification

Create test trigger, list it, run once, inspect scheduled action/action record.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

