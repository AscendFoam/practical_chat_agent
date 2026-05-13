# Task T10: iLink Fixture Mapper

## Task ID

T10

## Goal

新增不依赖真实 SDK 的微信 iLink raw payload fixture mapper，把脱敏 fixture 转换为 `InboundEvent`。

## Why now

先锁定 schema 和映射逻辑，避免真实 SDK 不稳定时阻塞主仓库开发。

## Allowed files

- `src/practical_chat_agent/connectors/inbound/wechat_ilink.py`
- `src/practical_chat_agent/connectors/inbound/__init__.py`
- `src/practical_chat_agent/services/inbound.py` if required
- `examples/payloads/wechat_ilink_*.json`
- `docs/07_handoff.md`

## Forbidden scope

- 不导入真实 SDK。
- 不新增发送能力。
- 不改数据库 schema。

## Inputs to read

- `docs/wechat_ilink_poc_notes.md`
- `src/practical_chat_agent/connectors/inbound/telegram_bot.py`
- `src/practical_chat_agent/connectors/inbound/feishu_bot.py`
- `src/practical_chat_agent/core/models.py`

## Expected output

- `WeChatIlinkInboundConnector` 可解析脱敏 fixture。
- `raw["connector_name"] == "wechat_ilink"`。
- 保留 SDK message id、account/session/channel/sender/context token 字段摘要。

## Verification

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main demo-turn examples/payloads/wechat_ilink_text.json --connector-name wechat_ilink
```

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

