# Risks And Open Questions

更新日期：2026-05-13

## Active Risks

| ID | 风险 | 影响 | 当前缓解 |
| --- | --- | --- | --- |
| R001 | WeChatBot/iLink SDK 无法稳定登录或收消息 | 微信主线无法进入主仓库 | Sprint 0 仓库外 POC，Gate 0 阻断 |
| R002 | 个人微信账号风控或平台风险 | 账号安全风险 | 只用测试账号/测试联系人，禁止绕过加密、hook、注入 |
| R003 | `context_token` 不可用或过期不可控 | reply/send 失败或误路由 | Sprint 0 明确记录 token 行为，M1 建 token 表 |
| R004 | Worker 提前 vendor SDK 或实现真实发送 | 主仓库污染和误发送风险 | `AGENTS.md` 与任务包禁止，review 阻断 |
| R005 | 记忆和 ContactSkill 保存敏感原文 | 隐私风险 | 证据引用、脱敏、review/approve 后才能注入 |
| R006 | 目前缺少 Alembic migration | schema 演进风险 | M1/M2 优先 additive tables，M7 引入 migration |
| R007 | 关闭微信功能后破坏既有 Telegram/飞书/会议 | 回归风险 | 每个主仓库任务都要求 disabled-by-default 验证 |
| R008 | 主动触发变成无人值守自动聊天 | 社交和安全风险 | M6 前禁止主动触发，M6 默认审批草稿 |
| R009 | T00 只在仓库外 `Python 3.12.7` sandbox 验证了安装与二维码阶段，尚未证明目标运行环境和登录后会话恢复稳定 | 可能在 T01/T02 暴露环境差异或会话持久化问题 | 保持主仓库零侵入，T01 先完成扫码、凭据落盘、重启复用和 Python 版本兼容观察 |

## Open Questions

| ID | 问题 | 需要谁回答 | 最晚解决点 |
| --- | --- | --- | --- |
| Q002 | sandbox 是否使用测试微信账号，还是用户当前账号？ | 用户/worker | T01 前 |
| Q003 | `context_token` 是否真实存在，字段名是什么，是否可持久化？ | T02 worker | Gate 0 |
| Q004 | reply 与主动 send 是否都可用，是否都依赖 token？ | T03 worker | Gate 0 |
| Q005 | 媒体下载/上传能力最小可用边界是什么？ | T03 worker | Gate 0 |
| Q006 | 若 iLink 不可行，是否继续强化桌面扫描 + Telegram/飞书闭环？ | 用户/Captain | Gate 0 Block 时 |
| Q007 | 首个真实微信发送测试联系人是谁？ | 用户 | M5 前 |
| Q008 | ContactSkill 的脱敏等级默认多严格？ | Captain/用户 | M3 前 |
| Q009 | `credentials.json` 是在扫码后、确认后还是首次收消息后落盘？重启后是否能直接复用？ | T01 worker | T01 |
| Q010 | `wechatbot-sdk 0.2.1` 是否明确支持项目常用 Python 3.11，还是仅确认 Python 3.12.7 可用？ | T01 worker | T01 |
| Q011 | 官方文档 `https://www.wechatbot.dev/en/python` 是否与本地 `wechatbot-sdk 0.2.1` 行为一致？ | T01 worker | T01 |

## Closed Questions

| ID | 结论 | 关闭依据 |
| --- | --- | --- |
| Q001 | SDK 包名为 `wechatbot-sdk`，当前验证版本 `0.2.1`，导入路径为 `from wechatbot import WeChatBot`。 | T00 worker notes + `docs/review/T00_review.md` PASS |

## Deferred Items

- Alembic migration：推迟到 M7，除非 M1/M2 schema 变更开始阻碍开发。
- Feishu delivery connector：当前不是微信主线，除非用户重新要求官方平台 demo。
- 会议子系统增强：当前暂停作为主线。
- 朋友圈/动态内容：等 persona、memory、policy 和 delivery 稳定后再讨论。
