# Task T22: Desktop Ingestion

## Task ID

T22

## Goal

将 `WeChatDesktopConnector` 扫描结果送入统一 ingestion pipeline。

## Why now

桌面扫描是 iLink 的补录和兜底来源，必须与 canonical event/去重共享路径。

## Allowed files

- `src/practical_chat_agent/services/desktop.py`
- `src/practical_chat_agent/connectors/desktop/wechat_desktop.py`
- `src/practical_chat_agent/services/ingestion.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不破坏 `desktop-scan-preview` 原有预览能力。
- 不强制 OCR。

## Inputs to read

- existing desktop scan service and OCR models.
- T20/T21 ingestion work.

## Expected output

- Desktop scan can optionally persist through ingestion.
- Source kind recorded as `wechat_desktop`.
- Dedupe applies to desktop scan results.

## Verification

Run `desktop-scan-preview` in non-persist preview mode and, if safe, a persist/dry-run mode.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

