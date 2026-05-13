# Task T00: Sandbox Install

## Task ID

T00

## Goal

在主仓库外建立 WeChatBot/iLink SDK sandbox，完成安装和官方 QuickStart/最小启动验证，并记录真实结果。

## Why now

这是 Gate 0 的第一步。未确认 SDK 能安装、导入和启动前，不能进入主仓库 connector 开发。

## Allowed files

- `docs/wechat_ilink_poc_notes.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- 仓库外 sandbox：建议 `D:\Codes\Social\wechatbot_sandbox\**`

如果当前 Codex sandbox 不允许写仓库外路径，先请求用户批准，或只记录需要用户本地执行的命令和阻塞原因。

## Forbidden scope

- 不修改 `src/practical_chat_agent/**`。
- 不修改 `pyproject.toml`。
- 不把 SDK clone/vendor/submodule 到主仓库。
- 不读取或打印 `.env` 密钥。
- 不做真实联系人自动发送。

## Inputs to read

- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/08_risks_and_open_questions.md`
- SDK 官方 README 或包文档。

## Expected output

- `docs/wechat_ilink_poc_notes.md` 新增或更新：
  - SDK 名称、版本、安装命令。
  - Python/Node 版本。
  - sandbox 路径。
  - QuickStart 命令。
  - 导入/启动是否成功。
  - 遇到的错误、完整错误摘要和下一步建议。
- `docs/07_handoff.md` 更新当前任务结果和下一个唯一任务建议。
- 如遇阻塞，`docs/08_risks_and_open_questions.md` 更新风险或问题。

## Verification

至少运行一种真实命令并记录结果：

```powershell
python --version
python -m pip show wechatbot-sdk
```

以及 SDK QuickStart 或最小 import 命令。若包名不同，以实际 SDK 文档为准。

## Docs to update

- `docs/wechat_ilink_poc_notes.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if needed

不要把 `docs/04_task_board.md` 的 T00 标成完成；由 Captain 在 review 后更新。

## Reviewer type

normal

