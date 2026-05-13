# Review: T00 Sandbox Install

Review date: 2026-05-13
Reviewer: Claude Code
Task package: `docs/tasks/M0_wechat_ilink_poc/T00_sandbox_install.md`

## Scope

只读审查 worker 针对 T00 的所有产出，对照任务包的 Allowed files、Forbidden scope 和 Verification 要求。

## Diff Summary

本次全部为新增文件（untracked），无已跟踪文件修改：

- `docs/wechat_ilink_poc_notes.md` — 新增，SDK 安装与 QuickStart 探测实验记录
- `docs/07_handoff.md` — 新增，交接文档，含 T00 执行状态和后续顺序
- `docs/08_risks_and_open_questions.md` — 新增，补充 R009 风险和 Q009 开放问题
- `docs/for_human/` — 空目录（已存在）
- `docs/review/` — 空目录（已存在）

仓库外 sandbox `D:\Codes\Social\wechatbot_sandbox` 含 `.venv`，已独立验证存在。

## Compliance Check

| 检查项 | 结果 |
| --- | --- |
| Allowed files 范围 | PASS — 只改了 `docs/wechat_ilink_poc_notes.md`、`docs/07_handoff.md`、`docs/08_risks_and_open_questions.md`，均在允许列表内 |
| 未修改 `src/practical_chat_agent/**` | PASS |
| 未修改 `pyproject.toml` | PASS |
| 未 vendor SDK 到主仓库 | PASS |
| 未把 `docs/04_task_board.md` T00 标完成 | PASS |
| 未读取或打印 `.env` 密钥 | PASS |
| 未做真实联系人发送 | PASS |

## Verification Check

任务包要求 "至少运行一种真实命令并记录结果"。Worker 执行了以下真实命令并记录输出：

1. `python --version` → `Python 3.12.7`
2. `python -m venv .venv` + `pip install wechatbot-sdk` → 安装成功
3. `pip show wechatbot-sdk` → 版本 `0.2.1`
4. `from wechatbot import WeChatBot` + 构造 → 成功，输出 `WeChatBot`
5. `await bot.login()` 20 秒超时探测 → 收到 `QR_URL` 回调后超时

Reviewer 独立重跑了第 2、3、4 项，结果与记录一致：
- `pip show` 确认 `wechatbot-sdk 0.2.1` 安装在 sandbox `.venv` 中
- `from wechatbot import WeChatBot` 导入和构造成功
- `Summary` 字段确实存在少量编码异常字符，与 POC notes 记录一致

第 5 项（login 超时探测）依赖异步运行时且可能触发扫码流程，reviewer 未重跑，但记录中的 `QR_URL_RECEIVED` + `STATES:['qr']` 输出格式与 SDK async 行为一致，不像是编造。

## Expected Output Check

| 期望产出 | 状态 |
| --- | --- |
| SDK 名称 | `wechatbot-sdk` ✓ |
| SDK 版本 | `0.2.1` ✓ |
| 安装命令 | `pip install wechatbot-sdk` ✓ |
| Python 版本 | `3.12.7` ✓ |
| sandbox 路径 | `D:\Codes\Social\wechatbot_sandbox` ✓ |
| QuickStart 命令 | `from wechatbot import WeChatBot` + `await bot.login()` ✓ |
| 导入/启动是否成功 | 已记录，导入和构造成功，login 进入 QR 阶段 ✓ |
| 遇到的错误 | 已记录：超时、Summary 编码异常、Home-page 为空 ✓ |
| 下一步建议 | 已记录：T01 继续复用 sandbox，优先验证扫码后凭据落盘 ✓ |
| `07_handoff.md` 更新 | 已更新，含任务结果和下一步建议 ✓ |
| `08_risks_and_open_questions.md` 更新 | 已补充 R009 和 Q009 ✓ |

## Content Quality

1. **已确认 vs 未确认的边界清晰**：POC notes 第 5 节明确列出 "已确认" 四项和 "仍未确认" 五项，没有把未验证内容写成已完成事实。
2. **handoff 态度保守**：明确写出 "当前不要把 Gate 0 视为通过"、"先等 reviewer 审查"。
3. **风险记录诚实**：R009 直接说明 T00 只验证到二维码阶段，尚未证明登录后会话恢复。
4. **回答了 Q001**：在 POC notes 中提供了 SDK 包名、版本、导入路径，使 `08_risks_and_open_questions.md` 的 Q001 可以在 reviewer 通过后关闭。

## Blocking Issues

无。

## Non-blocking Issues

1. **N01 — Python 版本偏差**：项目 `02_experiment_plan.md` 提及 Python 3.11，但 sandbox 实际使用系统 Python 3.12.7。当前不影响 POC 结论，但 T01 起应确认 SDK 是否对 Python 版本有约束，以免后续主仓库接入时出现兼容问题。建议在 POC notes 中补充一条注释。
2. **N02 — 官方文档 URL 未经独立验证**：POC notes 引用了 `https://www.wechatbot.dev/en/python`，reviewer 未验证该 URL 是否可达。这不影响本地实验结果的真实性，但建议 T01 时确认文档与 SDK 版本是否对应。

## Missing Tests

不适用。T00 是仓库外 sandbox 探测任务，不涉及主仓库代码，不需要写自动化测试。

## Suspicious Implementation Details

无。所有记录的命令和结果可独立复现，无伪实现、mock、stub 或 hardcode 痕迹。

## Over-engineering Check

无。文档量适当，没有提前设计架构、写配置模板或准备超出 T00 范围的脚手架。

## Regression Risk

无。本次不涉及任何主仓库源码或配置变更。

## Verdict

**PASS**

Worker 严格遵守了任务包的 Allowed files 和 Forbidden scope，执行了真实命令并如实记录结果，没有把未验证内容写成完成事实，没有提前越界。两个 non-blocking issue 可由 Captain 决定是否转为 T01 的输入项。

## Recommended Next Action

1. Captain 标记 T00 完成，将 Current Unique Task 推进到 T01（登录/session 验证）。
2. T01 应复用同一 sandbox，优先完成真实扫码、凭据落盘、重启复用验证。
3. T01 开始前，用户需确认使用哪个微信测试账号（Q002）。
4. 可选：在推进 T01 之前，补充 N01 中 Python 版本偏差的注释。
