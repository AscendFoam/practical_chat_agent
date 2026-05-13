# Task T14: Limited Listen

## Task ID

T14

## Goal

实现 `wechat-ilink-listen --limit n`，用 optional SDK adapter 或脱敏 adapter 把微信消息送入 `AgentRuntime`。

## Why now

这是 Gate 1 的主闭环：真实或 adapter 消息进入 events、memory、suggestion、action draft。

## Allowed files

- `src/practical_chat_agent/connectors/inbound/wechat_ilink.py`
- `src/practical_chat_agent/services/wechat_ingestion.py`
- `src/practical_chat_agent/services/wechat_ilink_session.py`
- `src/practical_chat_agent/app/container.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不无限后台运行。
- 不自动发送。
- SDK import 必须 optional。
- `WECHAT_ILINK_ENABLED=false` 时不得启动真实 SDK。

## Inputs to read

- T10-T13 implementation.
- `docs/wechat_ilink_poc_notes.md`.
- `src/practical_chat_agent/services/inbound.py`.

## Expected output

- CLI 支持有限条消息监听。
- 写入 canonical `events`。
- raw 中保留 connector/source/token 摘要。
- 可触发现有 suggestion/action draft。

## Verification

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main wechat-ilink-listen --agent-id <agent_id> --limit 3
```

如果无真实 SDK，用 fixture adapter 验证，并明确标注未完成真实验证。

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if real verification is deferred

## Reviewer type

adversarial

