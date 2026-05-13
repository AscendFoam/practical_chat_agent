# Task T13: Session Token Service

## Task ID

T13

## Goal

实现 `WeChatIlinkSessionService`，封装 session cursor、context token upsert、token 失效和状态查询。

## Why now

监听与发送都需要统一 token/session 生命周期，不应把逻辑散落在 connector 和 CLI。

## Allowed files

- `src/practical_chat_agent/services/wechat_ilink_session.py`
- `src/practical_chat_agent/app/container.py`
- `src/practical_chat_agent/app/main.py` for status command integration if needed
- `docs/07_handoff.md`

## Forbidden scope

- 不做真实发送。
- 不直接依赖 SDK 网络调用。
- 不保存明文敏感凭据。

## Inputs to read

- T12 repository implementation.
- `src/practical_chat_agent/services/delivery.py` for service style.

## Expected output

- Service can upsert context token from inbound raw fields.
- Service can mark token/session expired.
- CLI/status path can inspect session/token summary without secrets.

## Verification

Run a minimal repository/service roundtrip via existing CLI if available, or compile check plus targeted script approved by Captain.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

