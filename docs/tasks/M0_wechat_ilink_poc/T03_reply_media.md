# Task T03: Reply And Media Probe

## Task ID

T03

## Goal

验证 SDK 的文本 reply/send 能力和媒体消息元数据能力。

## Why now

Gate 0 必须知道 SDK 能否完成受控回复，以及媒体至少能否归档元数据。

## Allowed files

- `docs/wechat_ilink_poc_notes.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- 仓库外 sandbox：`D:\Codes\Social\wechatbot_sandbox\**`

## Forbidden scope

- 不对非测试联系人发送消息。
- 不实现主仓库 delivery connector。
- 不绕过 SDK 官方/公开能力。
- 不保存真实媒体文件到主仓库。

## Inputs to read

- `docs/wechat_ilink_poc_notes.md`
- SDK reply/send/media 文档。

## Expected output

`docs/wechat_ilink_poc_notes.md` 记录：

- reply 文本是否成功。
- 主动 send 是否成功，是否依赖 `context_token`。
- token 失效时发送表现。
- 图片/语音/文件等媒体消息是否能拿到 type、size、id、download ref 或错误码。
- 失败路径和限制。

## Verification

- 对一条测试入站消息执行 reply。
- 若 SDK 支持，向测试联系人执行主动 send；若不支持，记录明确限制。
- 发送或接收一条测试图片，至少记录媒体元数据。

## Docs to update

- `docs/wechat_ilink_poc_notes.md`
- `docs/08_risks_and_open_questions.md` if needed

## Reviewer type

adversarial

