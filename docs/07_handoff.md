# Handoff

更新日期：2026-05-13

## 1. 当前状态

Captain 已对 `docs/review/T00_review.md` 做出判断：`PASS`。

T00 已完成并可作为仓库外 POC 的第一项证据，当前状态是：

- 仓库外 sandbox `D:\Codes\Social\wechatbot_sandbox` 已建立
- `wechatbot-sdk` 0.2.1 安装成功
- `from wechatbot import WeChatBot` 导入和构造成功
- 20 秒超时的 `login()` 探测已触发二维码 URL 回调，说明官方登录流程至少能进入扫码阶段
- 尚未完成真实扫码、收消息、reply、媒体和 `context_token` 验证
- `docs/wechat_ilink_poc_notes.md` 已写入真实命令和结果
- reviewer 的两个 non-blocking issue 已分类为 accepted，并并入 T01 输入项

当前不要把 Gate 0 视为通过。T00 只证明 SDK 能启动到二维码阶段，不能替代登录/session 验证。

已补齐：

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/tasks/` 任务包目录

`docs/02_experiment_plan.md` 保持为下一阶段实验计划主依据。

## 2. 当前唯一任务

T01: 验证扫码登录、凭据缓存、重启恢复和会话失效表现。

状态：ready for worker，不要由 Captain 直接执行。

任务包：`docs/tasks/M0_wechat_ilink_poc/T01_login_session.md`

## 3. 为什么现在做 T01

`02_experiment_plan.md` 明确指出：WeChatBot/iLink 不应立即进入主仓库。必须先验证 SDK 安装、登录、收发、媒体和 `context_token` 行为，再决定是否进入 Sprint 1。

本轮新增的真实结论：

- 可用的 Python 包名是 `wechatbot-sdk`
- 当前安装版本为 `0.2.1`
- 官方 Python 文档入口与本地包一致：`from wechatbot import WeChatBot`
- QuickStart 登录入口可走到二维码阶段，但还没有完成扫码确认

T01 要补的关键缺口：

- 真实扫码是否成功。
- 扫码后凭据是否落盘。
- 重启后是否能复用凭据。
- session 失效/登出/自动重登行为。
- `wechatbot-sdk 0.2.1` 在 Python 3.12.7 与项目常用 Python 3.11 环境之间是否存在明显兼容风险。
- 官方文档 URL 与本地 SDK 版本行为是否对应。

## 4. Worker 启动提示

```text
你是 Codex worker。

请先阅读：
- README.md
- AGENTS.md
- docs/02_experiment_plan.md
- docs/04_task_board.md
- docs/07_handoff.md

本轮只完成：
- docs/tasks/M0_wechat_ilink_poc/T01_login_session.md

严格遵守任务包中的 Allowed files 和 Forbidden scope。
完成后运行 Verification，更新任务包指定 docs，最后报告：改了什么、如何验证、剩余风险。
不要自动领取下一任务。
```

## 5. Reviewer 启动提示

```text
你是 Claude Code reviewer。

请先阅读：
- docs/02_experiment_plan.md
- docs/04_task_board.md
- docs/07_handoff.md

只读审查本次 diff，不要修改文件。重点检查 worker 是否越界修改主仓库代码、是否把扫码/session 未验证内容写成完成事实、是否记录了真实命令和失败点。

输出 Verdict: PASS / PASS_WITH_WARNINGS / BLOCK，并写入 docs/review/T01_review.md。
```

## 6. T00 Review 判断

Verdict：`PASS`

Captain 分类：

- Blocking issues：无。
- N01 Python 版本偏差：accepted，作为 T01 输入项。
- N02 官方文档 URL 未独立验证：accepted，作为 T01 输入项。
- Deferred warnings：无。
- Rejected warnings：无。

## 7. 下一步顺序

1. 可以提交当前治理文档、T00 POC notes 和 T00 review。
2. Worker 执行 T01。
3. Reviewer 审查 T01。
4. Captain 根据 T01 review 决定是否推进 T02。

## 8. 注意事项

- 当前 git 状态包含未跟踪治理文档和调研材料；不要误删。
- `.env` 可能含真实密钥，不要输出。
- PowerShell 输出中文时可能出现 mojibake，应使用 UTF-8 读取。
- 如果 worker 需要在 `D:\Codes\Social\wechatbot_sandbox` 写文件，可能需要用户批准或在自己的本地环境执行。
- 本轮已确认二维码阶段能启动，但尚未证明登录后会话可恢复。
- T01 需要用户或 worker 明确测试微信账号选择，不要使用敏感真实联系人做测试。
