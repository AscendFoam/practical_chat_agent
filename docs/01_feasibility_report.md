# Feasibility Report

更新日期：2026-05-13

## 1. 问题定义

目标是把现有多平台 chat/meeting assistant 原型推进为微信优先的社交 agent 工程实验闭环。核心问题不是“能否做一个聊天机器人”，而是能否在个人微信场景下安全、稳定、可审计地完成：

- 新消息 ingestion。
- 记忆与联系人 Skill。
- 回复建议。
- 人工审批后的受控投递。

## 2. 相关工作矩阵

| 方向 | 优点 | 局限 | 本项目采用方式 |
| --- | --- | --- | --- |
| Telegram/飞书官方 bot | API 稳定、发送安全、易测试 | 不覆盖个人微信 | 保留为回归和对照链路 |
| 微信桌面扫描/OCR | 不依赖非官方网络 SDK，可补可见历史 | 实时性和稳定性有限 | 作为历史补录和兜底来源 |
| WeChatBot/iLink SDK | 可能支持个人微信增量消息与 reply | 稳定性、风控和接口变化未知 | 先仓库外 POC，再决定接入 |
| 长期记忆助手 | 能提升持续对话体验 | 容易产生错记忆和隐私风险 | 必须保留证据、纠错、冻结、删除 |
| 自动发消息 agent | 闭环完整 | 误发送代价高 | 默认草稿/审批，不做无人值守自动发送 |

## 3. 最像的 5 个已有工作

1. 官方 bot 平台 assistant：稳定但平台受限。
2. 桌面自动化聊天助手：可接近真实 IM，但依赖 UI 状态。
3. 私人知识库/记忆助手：擅长记忆和检索，但没有发送闭环。
4. CRM/contact intelligence 工具：擅长联系人摘要，但不适合个人社交隐私。
5. 自动回复机器人：闭环强，但常缺少审批、policy 和可审计性。

## 4. 可差异化点

- 微信优先，但不把不稳定 SDK 直接污染主仓库。
- 所有原始事件不可变，记忆、Skill 和建议保留证据链。
- 默认 human-in-the-loop，真实发送经 `PolicyEngine` 与人工审批。
- `WeChatDesktopConnector`、iLink、手工导入三类来源最终统一 ingestion。
- ContactSkill 只辅助用户理解和回复，不冒充联系人。

## 5. MVP 实验

MVP 分两层：

1. Gate 0：仓库外 iLink POC，验证登录、收消息、reply、媒体和 `context_token`。
2. Gate 1：在主仓库中先用 fixture mapper 接入，再逐步加入真实 SDK adapter，确保关闭微信配置不影响既有功能。

当前 Gate 0 进展：

- T00 已验证 SDK 安装、导入、构造和二维码登录入口。
- 尚未验证扫码后凭据落盘、重启恢复、收消息、reply、媒体和 `context_token`。
- reviewer 对 T00 给出 `PASS`，两个 non-blocking issue 已接受为 T01 输入项。

## 6. 风险

- iLink SDK 不稳定或接口变化。
- 个人微信账号风控。
- 会话 token 过期导致误发送或发送失败。
- 记忆或 ContactSkill 保存敏感原文。
- Worker 越界实现主动发送或 vendor SDK。
- 目前缺少 Alembic，表结构扩展需要谨慎。

## 7. Go / No-Go 判断

当前判断：`Go with constraints`。

约束：

- Sprint 0 不改主仓库业务代码。
- Sprint 1 先做 fixture mapper 和 disabled-by-default 配置。
- 真实发送必须等 Sprint 5，且默认审批。
- 主动触发必须等半自动发送稳定后才进入。
