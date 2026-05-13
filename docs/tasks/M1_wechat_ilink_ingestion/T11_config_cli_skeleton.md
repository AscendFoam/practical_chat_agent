# Task T11: iLink Config And CLI Skeleton

## Task ID

T11

## Goal

新增微信 iLink 配置项和 CLI 壳，默认 disabled，并保证未安装 SDK 时现有 CLI 不受影响。

## Why now

配置边界先稳定，后续真实 listen 和 session 服务才可安全接入。

## Allowed files

- `src/practical_chat_agent/app/config.py`
- `src/practical_chat_agent/app/main.py`
- `.env.example`
- `docs/07_handoff.md`

## Forbidden scope

- 不实现真实网络轮询。
- 不添加硬依赖 SDK。
- 不修改 existing CLI 行为。

## Inputs to read

- `docs/02_experiment_plan.md`
- `src/practical_chat_agent/app/config.py`
- `src/practical_chat_agent/app/main.py`

## Expected output

- 配置项包括 `WECHAT_ILINK_ENABLED`、credential dir、poll timeout、auto relogin、account id、save raw。
- CLI 至少包含 `wechat-ilink-check`，能说明 disabled、SDK missing 或 ready。

## Verification

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main show-config
```

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main wechat-ilink-check
```

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

