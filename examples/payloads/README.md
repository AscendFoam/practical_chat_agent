# examples/payloads

示例 webhook 载荷与对话数据，用于开发和测试入站连接器。

## 文件说明

| 文件 | 平台 | 说明 |
|------|------|------|
| `feishu_im_message.json` | 飞书 | 飞书机器人接收消息事件 (`im.message.receive_v1`) 的标准载荷 |
| `telegram_bot_dm.json` | Telegram | Telegram Bot 私聊消息的标准 Update 载荷 |
| `telegram_preference_followup.json` | Telegram | 用户分享个人偏好的示例消息 |
| `telegram_preference_profile.json` | Telegram | 用户分享关系信息的示例消息 |
| `telegram_reflection_followup.json` | Telegram | 用户表达情绪与价值观的示例消息 |
| `telegram_reflection_profile.json` | Telegram | 用户情绪状态后续反馈的示例消息 |
| `telegram_relationship_profile.json` | Telegram | 生活方式对话示例，用于关系建立 |
| `weflow_redacted_sample.jsonl` | 微信 (WeFlow) | 已脱敏的微信私聊导出样本 (JSONL)，含 header / member / message 三种记录类型 |

## 载荷结构

所有载荷在顶层包含 `_meta` 字段，用于标注 `connector_name`，其余字段保持与平台原始 webhook 格式一致。

WeFlow JSONL 每行一个 JSON 对象，通过 `_type` 区分：
- `header` — 元信息（平台、会话类型、版本）
- `member` — 参与者信息
- `message` — 单条消息（含回复引用与来源标注）

## 用途

- 作为单元测试和集成测试的 fixture 输入
- 作为新连接器开发时的参考格式
- 作为对话分析 pipeline 的样本数据
