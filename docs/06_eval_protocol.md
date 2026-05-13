# Eval Protocol

更新日期：2026-05-13

## 1. 评价目标

验证项目是否从“功能原型”推进到“微信主线 chat agent 工程实验闭环”。评价重点不是模型回答是否好听，而是数据、记忆、联系人理解和发送链路是否可靠、安全、可审计。

## 2. Gate 评价

### Gate 0: iLink 是否进入主仓库

必须满足：

- sandbox 可扫码登录。
- 可收到至少 10 条测试消息。
- 可解析文本、时间、发送者、会话 ID 或等价字段。
- 可完成文本 reply。
- `context_token` 或等价机制的存在、过期和恢复行为记录清楚。
- 媒体能力至少完成元数据验证。
- 风险记录完整。

结论：`Allow`、`Conditional` 或 `Block`。

当前进展：

- T00 已通过 review，只覆盖 SDK 安装、导入、构造和二维码登录入口。
- T01 必须补齐真实扫码、凭据落盘、重启复用和 session 失效验证。
- T00 不能单独作为 Gate 0 通过证据。

### Gate 1: 是否开启主仓库微信监听

必须满足：

- fixture mapper 测试通过。
- session/token 表或仓储可写可读。
- `wechat-ilink-listen --limit n` 不影响 Telegram、飞书、会议和 action CLI。
- 微信配置关闭时项目仍可启动。

### Gate 2: 是否启用 ContactSkill 注入

必须满足：

- Skill 字段完整。
- 证据引用可追溯。
- 可 review/approve/export。
- 脱敏检查通过。
- 注入后建议质量提升，且不机械复述。

### Gate 3: 是否开启微信真实发送

必须满足：

- 文本发送端到端成功。
- 审批前不会发送。
- token 失效时状态清楚。
- policy 能处理群聊、安静时段、高频和 avoid topics。
- 审计日志完整。

### Gate 4: 是否开启主动触发

必须满足：

- 半自动发送稳定。
- trigger 产生的 action 默认审批或草稿。
- 可一键禁用。
- quiet-hours 和退让规则可验证。

## 3. 指标

### 接入侧

- 登录成功率。
- 连续 poll 运行时长。
- 新消息漏收率。
- 重复消息率。
- token 失效率。
- 媒体元数据完整率。

### 记忆侧

- 有效记忆写入率。
- 错误记忆率。
- 证据可追溯率。
- 冻结/归档后误用次数。
- 用户纠错后生效时间。

### ContactSkill 侧

- 字段完整率。
- 人工审核通过率。
- 脱敏违规次数。
- Skill 注入后的建议自然度。
- 建议二次编辑距离。

### 发送侧

- 草稿到审批通过率。
- 审批后发送成功率。
- policy 阻断准确率。
- 误发送次数，目标为 0。
- 群聊草稿降级率。

## 4. 验证分层

- 单元测试：raw payload mapper、dedupe、policy、token 状态、schema roundtrip。
- fixture 集成测试：脱敏微信 payload replay 到 runtime。
- 手工真实验证：只使用测试联系人和测试内容。
- 里程碑审查：每个 milestone 结束由 reviewer 产出 milestone review。

T01 额外验证要求：

- 明确记录 Python 版本与 SDK 兼容性观察。
- 明确记录 SDK 文档 URL、示例代码和本地版本是否一致。

## 5. 不合格判据

任一情况视为失败或暂停：

- 文档声称能力完成，但没有验证证据。
- 关闭微信配置后破坏既有功能。
- 真实发送绕过审批。
- 未经脱敏保存敏感联系人原文到 ContactSkill。
- 主动触发在 M6 前出现。
- SDK vendor 进入主仓库但 Gate 0 未通过。
