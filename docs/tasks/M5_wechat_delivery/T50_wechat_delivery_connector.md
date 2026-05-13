# Task T50: WeChat Delivery Connector

## Task ID

T50

## Goal

新增 `WeChatIlinkDeliveryConnector`，支持审批后的文本发送，并清晰处理 token 缺失或失效。

## Why now

微信主线需要从建议草稿进入半自动发送闭环，但必须在 M5 才做。

## Allowed files

- `src/practical_chat_agent/connectors/delivery/wechat_ilink.py`
- `src/practical_chat_agent/services/wechat_delivery.py`
- `src/practical_chat_agent/services/delivery.py`
- `src/practical_chat_agent/app/container.py`
- `src/practical_chat_agent/core/enums.py` if needed
- `docs/07_handoff.md`

## Forbidden scope

- 不自动发送未审批 action。
- 不发送媒体。
- 不在 SDK missing 时破坏 CLI import。

## Inputs to read

- `docs/wechat_ilink_poc_notes.md`
- existing Telegram delivery connector.
- session/token service.

## Expected output

- Text send through SDK adapter.
- Missing/expired token returns failed/draft-only with useful error.
- Delivery response and audit log persisted.

## Verification

Use safe test action; if no real SDK/session, run fake adapter tests and mark real send unverified.

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if real send deferred

## Reviewer type

adversarial

