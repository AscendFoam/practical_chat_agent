# Task T02: Receive Messages And Context Token

## Task ID

T02

## Goal

验证 SDK 是否能稳定收到测试微信消息，并提取 message id、sender、conversation id、timestamp、text、`context_token` 或等价会话字段。

## Why now

这些字段决定 M1 能否将微信消息映射为 `InboundEvent` 并支持后续 reply。

## Allowed files

- `docs/wechat_ilink_poc_notes.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- 仓库外 sandbox：`D:\Codes\Social\wechatbot_sandbox\**`

## Forbidden scope

- 不保存敏感原文。测试消息可以使用无敏感内容。
- 不修改主仓库业务代码。
- 不把真实联系人信息写入文档；使用脱敏 ID。

## Inputs to read

- `docs/02_experiment_plan.md`
- `docs/wechat_ilink_poc_notes.md`
- SDK message schema 文档。

## Expected output

`docs/wechat_ilink_poc_notes.md` 记录：

- 至少 10 条测试消息的字段摘要。
- 字段映射表：SDK 字段 -> 计划中的 `InboundEvent` 字段。
- 是否存在 `context_token`；若不存在，记录可替代字段。
- 重复消息、漏消息或延迟观察。

## Verification

- 向测试账号发送至少 10 条不同测试消息。
- 脚本输出脱敏字段摘要。
- 记录每条消息是否可唯一识别。

## Docs to update

- `docs/wechat_ilink_poc_notes.md`
- `docs/08_risks_and_open_questions.md` if needed

## Reviewer type

normal

