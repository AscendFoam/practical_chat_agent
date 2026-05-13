# Review: T01 Login And Session

Review date: 2026-05-13
Reviewer: Claude Code
Task package: `docs/tasks/M0_wechat_ilink_poc/T01_login_session.md`

## Scope

只读审查 worker 针对 T01 的所有产出，对照任务包的 Allowed files、Forbidden scope 和 Verification 要求。

## Diff Summary

### 主仓库变更

| 文件 | 变化类型 | 是否在 Allowed files 内 |
| --- | --- | --- |
| `.gitignore` | modified（新增 `private/`） | 不在允许列表内 |
| `docs/engineering_experiment_plan.md` | deleted（用户手动迁移） | N/A（用户操作） |
| `docs/next_ai_handoff_prompt.md` | deleted（用户手动迁移） | N/A |
| `docs/stage_progress_summary.md` | deleted（用户手动迁移） | N/A |
| `docs/wechat_agent_deep_research_prompt.md` | deleted（用户手动迁移） | N/A |
| `docs/wechat_ilink_poc_notes.md` | deleted（用户手动迁移到 docs/notes/） | N/A |
| `docs/深度调研报告.docx` | deleted（用户手动迁移） | N/A |

Worker 声称未修改主仓库业务代码。经检查 `src/` 目录无任何 diff，确认无误。

用户已声明 docs 目录下的文件夹和文档位置变化为手动操作，不属于 worker 动作。Reviewer 采信此声明。

### 仓库外 sandbox 变更

| 文件 | 说明 |
| --- | --- |
| `t01_login_probe.py` | Worker 新建的登录探针脚本 |
| `t01_qr.png` | 探针生成的二维码图片（1362 bytes） |
| `t01_qr_url.txt` | 二维码 URL 文本 |
| `t01_session_probe_state.json` | 探针运行状态记录 |

sandbox 变更在 Allowed files 的 `D:\Codes\Social\wechatbot_sandbox\**` 范围内。

### 未更新的文档

T01 任务包要求更新以下文档，但 worker **未做任何更新**：

- `docs/notes/wechat_ilink_poc_notes.md`（或 `docs/wechat_ilink_poc_notes.md`，取决于迁移后位置）— 无变更
- `docs/07_handoff.md` — 无变更
- `docs/08_risks_and_open_questions.md` — 无变更

## Verification Check

T01 任务包要求以下验证，逐项检查：

| 验证要求 | 状态 | 证据 |
| --- | --- | --- |
| 完成至少一次登录 | **未通过** | `t01_session_probe_state.json` 显示 `status: "login_exception"`，错误为 `AuthError: QR code expired 3 times — login aborted`。QR 码被生成但无人扫码，3 次过期后 SDK 自动中止。 |
| 关闭并重启脚本，观察是否复用凭据 | **未执行** | 登录未成功，无凭据生成，无法测试重启复用。`credentials.json` 不存在。 |
| 记录失败时的错误摘要 | **部分完成** | 探针状态文件记录了错误类型和 traceback，但未写入 POC notes 文档。 |
| 明确记录使用的测试账号类型 | **未完成** | 无文档记录。 |
| 明确记录是否有 Python 版本兼容风险 | **未完成** | T00 reviewer N01 要求 T01 确认，但未在文档中记录。 |
| T00 N01：Python 3.12.7 与 3.11 兼容观察 | **未完成** | Worker 读了 SDK 源码但没有在文档中记录兼容性结论。 |
| T00 N02：官方文档 URL 与本地 SDK 行为对应 | **未完成** | Worker 搜索过官方文档但没有在文档中记录对应关系。 |

## Compliance Check

| 检查项 | 结果 |
| --- | --- |
| Allowed files 范围 | **WARN** — sandbox 文件在范围内，但 `.gitignore` 被修改（新增 `private/`），不在 T01 允许列表内。此变更是良性的安全措施，不构成阻断，但属于越界。 |
| 未修改 `src/practical_chat_agent/**` | PASS |
| 未提交凭据/二维码/cookies/token | PASS — `credentials.json` 不存在，sandbox 中的文件不含敏感凭据 |
| 未 vendor SDK | PASS |
| 文档更新 | **未完成** — POC notes、handoff、risks 均未更新 |

## Probe Script Quality

Worker 创建的 `t01_login_probe.py` 质量评价：

**优点：**

- 结构清晰，回调齐全（`on_qr_url`、`on_scanned`、`on_expired`、`on_error`）
- 状态机设计合理，通过 JSON 文件持久化每个阶段的状态
- QR 码同时支持 data URL 和远程 URL 两种格式
- 登录成功时计划记录脱敏后的账号信息（仅保留后 6 位），符合安全要求
- 超时设置为 600 秒，给扫码留了充足时间
- 异常处理完整，包含 traceback 记录

**无伪实现/mock/stub/hardcode：** 脚本直接调用真实 SDK API，不存在模拟行为。

**不过度工程：** 脚本约 120 行，恰好覆盖登录流程的状态追踪需求，没有多余的抽象层。

## Blocking Issues

1. **B01 — 登录未成功**：T01 的核心目标是"完成至少一次登录"。当前探针运行结果为 `AuthError: QR code expired 3 times — login aborted`，QR 码已生成但无人扫码，3 次过期后 SDK 中止。这是 T01 最基本的验证条件，不满足则无法评估凭据落盘、重启恢复和会话失效行为。

2. **B02 — 文档未更新**：T01 任务包明确要求在 `docs/wechat_ilink_poc_notes.md` 记录登录方式、凭据行为、重启恢复、失效表现等。当前 POC notes 仍停留在 T00 的内容，未追加任何 T01 实验 result。`docs/07_handoff.md` 和 `docs/08_risks_and_open_questions.md` 也未更新。

## Non-blocking Issues

1. **N01 — `.gitignore` 越界修改**：Worker 在 `.gitignore` 中新增了 `private/`。虽然这是一个合理的安全措施，但不在 T01 的 Allowed files 列表内。建议 Captain 决定是否接受此变更。

2. **N02 — Worker 阅读了 SDK 源码但未记录结论**：Worker 提到读了 `client.py`、`auth.py`，了解了凭据文件名、自动重登和回调机制。这些发现对 T01 很有价值，但未写入任何文档。建议在补完时一并记录。

3. **N03 — 探针在前台跑完后状态已定格**：`t01_session_probe_state.json` 显示最终状态为 `login_exception`，说明探针已经运行完毕并失败。Worker 的工作流描述最后一步是"二维码已经准备好了，请用测试微信账号扫描这张码"，但实际探针已经因为 QR 过期而退出。如果需要重新尝试，需要重新运行探针。

## Missing Tests

不适用。T01 是仓库外 sandbox 探测任务，不涉及主仓库代码。

## Suspicious Implementation Details

无。探针脚本直接调用真实 SDK API，状态文件记录了真实的错误信息。

## Over-engineering Check

无。探针脚本规模适中，没有多余的抽象。

## Regression Risk

无。`src/` 目录无任何变更。

## Verdict

**BLOCK**

Worker 的探针脚本质量良好，方法论正确（先读源码再测），sandbox 内操作符合范围。但 T01 的核心验证条件——完成至少一次真实扫码登录——未满足，所有文档更新也未执行。Worker 的工作停留在"二维码已生成、等待扫码"阶段，而实际探针已经因 QR 过期而中止。

这不是方法论问题，而是执行未完成。Worker 需要在用户配合扫码后重新运行探针，或等待新的会话来完成任务。

## Recommended Next Action

1. 用户确认使用哪个测试微信账号（Q002 仍未解决）。
2. 重新运行 `t01_login_probe.py`，用户在 QR 码生成后 5 分钟内扫码确认。
3. 登录成功后：
   - 检查 `credentials.json` 是否生成，记录大小和脱敏结构。
   - 重新运行探针（不带 `force=True`），验证是否能复用凭据跳过扫码。
   - 手动删除或重命名凭据文件，验证失效后的错误表现。
4. 将所有结果写入 POC notes，更新 handoff 和 risks 文档。
5. 处理 T00 reviewer N01（Python 版本兼容）和 N02（文档 URL 对应）。
