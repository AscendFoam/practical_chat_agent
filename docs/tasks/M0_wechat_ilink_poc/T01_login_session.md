# Task T01: Login And Session

## Task ID

T01

## Goal

验证 sandbox 中 SDK 的扫码登录、凭据缓存、重启恢复、登出/过期和自动重登行为。

## Why now

只有登录和 session 生命周期清楚，后续收消息和 reply 才有可靠基础。

## Allowed files

- `docs/wechat_ilink_poc_notes.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- 仓库外 sandbox：`D:\Codes\Social\wechatbot_sandbox\**`

## Forbidden scope

- 不修改主仓库业务代码。
- 不提交凭据、二维码、cookies、token 或账号敏感信息。
- 不 vendor SDK。

## Inputs to read

- `docs/wechat_ilink_poc_notes.md`
- `docs/review/T00_review.md`
- SDK 登录/session 文档。

## Expected output

在 `docs/wechat_ilink_poc_notes.md` 记录：

- 登录方式和命令。
- 是否需要扫码。
- 凭据保存位置，使用脱敏路径或相对描述。
- 重启后是否能恢复。
- 失效/登出时错误码或异常表现。
- 是否存在自动重登能力。
- T00 reviewer N01 处理结果：SDK 对 Python 3.12.7 与项目常用 Python 3.11 的兼容观察。
- T00 reviewer N02 处理结果：官方文档 URL、示例代码与本地 `wechatbot-sdk 0.2.1` 行为是否对应。

## Verification

- 完成至少一次登录。
- 关闭并重启脚本，观察是否复用凭据。
- 记录失败时的错误摘要。
- 明确记录使用的测试账号类型，但不要记录账号敏感信息。
- 明确记录是否有 Python 版本兼容风险。

## Docs to update

- `docs/wechat_ilink_poc_notes.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if needed

## Reviewer type

normal
