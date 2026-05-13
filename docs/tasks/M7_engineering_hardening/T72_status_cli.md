# Task T72: Status CLI

## Task ID

T72

## Goal

新增 `system-status`、`connector-status`、`wechat-status`、`policy-status`，提供 text 和 JSON 输出。

## Why now

真实运行需要快速定位 connector、session、policy、pending action 和错误状态。

## Allowed files

- `src/practical_chat_agent/app/main.py`
- `src/practical_chat_agent/app/container.py`
- relevant service files if summary helpers are needed
- `docs/07_handoff.md`

## Forbidden scope

- 不输出 secrets、tokens、完整 raw payload。
- 不改变 existing command behavior.

## Inputs to read

- Settings, repositories, session/token service, action repository, policy service.

## Expected output

- Status commands support concise text and JSON.
- WeChat disabled/missing SDK/session expired states are visible.

## Verification

Run all status commands with default config and with微信 disabled.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

