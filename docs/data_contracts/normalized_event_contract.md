# Normalized Event Contract

更新日期：2026-05-14

本文档给出 WeFlow JSONL -> normalized event 的第一版合约草案。目标是让后续 adapter、chunker 和 evidence 管线建立在稳定、可审计、可脱敏的数据层上，而不是把 WeFlow 原始字段直接外溢到下游。

## 1. Scope

- 输入来源：`private/chat_history/` 下的 WeFlow JSONL 导出。
- 归一化对象：仅 `_type=message` 行。
- `header` / `member` 行用于补充会话元数据、身份映射和方向判定，不直接变成 event。
- 所有会进入可提交目录的示例、文档、测试数据都必须使用红线脱敏版本。

## 2. Draft Schema

```json
{
  "event_id": "evt_4b8c2d0f8d3c1a77",
  "platform": "wechat",
  "source": "weflow_jsonl",
  "source_row_type": "message",
  "source_message_type_code": 25,
  "source_ref": {
    "file_alias": "file_02",
    "line_no": 412,
    "platform_message_id_hash": "pmid_90fe12ab",
    "reply_to_platform_message_id_hash": "pmid_90fe12aa"
  },
  "raw_ref": "weflow:file_02:412",
  "conversation_id": "conv_2c4111bb7f14",
  "contact_id": "contact_6b7a3097a1d1",
  "sender_id": "sender_2e0e74c73dcb",
  "sender_alias": "contact",
  "sender_role": "contact",
  "timestamp": "2026-05-13T16:54:11+08:00",
  "timestamp_epoch_s": 1778662451,
  "timezone_assumption": "Asia/Shanghai",
  "text": "[redacted_or_private_text]",
  "message_type": "text",
  "content_kind_hint": "quoted_reply",
  "interaction_flags": ["reply"],
  "status": "normal",
  "reply_to_event_id": "evt_2e55d62117c5fe5e",
  "media_refs": [],
  "forwarded_records": [],
  "risk_flags": []
}
```

### 2.1 Field Notes

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `event_id` | 是 | 稳定、不可逆的事件 ID |
| `platform` | 是 | 固定为 `wechat` |
| `source` | 是 | 固定为 `weflow_jsonl` |
| `source_row_type` | 是 | 当前固定为 `message` |
| `source_message_type_code` | 是 | WeFlow 原始 `type`，必须保留 |
| `source_ref` | 是 | 可审计但已脱敏的来源定位对象 |
| `raw_ref` | 是 | 紧凑来源串，用于日志和 evidence |
| `conversation_id` | 是 | 会话级稳定 ID |
| `contact_id` | 是 | 联系人级稳定 ID |
| `sender_id` | 是 | 发言者稳定 ID |
| `sender_alias` | 否 | 可读性更强的别名，例如 `user` / `contact` |
| `sender_role` | 是 | `user | contact | system | unknown` |
| `timestamp` | 是 | ISO 8601，必须带时区偏移 |
| `timestamp_epoch_s` | 是 | 原始 epoch seconds |
| `timezone_assumption` | 否 | 记录 adapter 采用的时区配置 |
| `text` | 否 | 私有归档可留原文；公开或样例环境必须脱敏或合成 |
| `message_type` | 是 | 归一化后的消息类型 |
| `content_kind_hint` | 否 | 比 `message_type` 更细的候选标签 |
| `interaction_flags` | 否 | 引用、转发、系统事件等附加标记 |
| `status` | 是 | `normal | recalled | deleted | unknown` |
| `reply_to_event_id` | 否 | 若引用链能解析，则指向被引用 event |
| `media_refs` | 否 | 私有媒体定位信息；公共产物只留脱敏占位 |
| `forwarded_records` | 否 | 转发聊天记录的脱敏嵌套版本 |
| `risk_flags` | 否 | 记录解析不确定性 |

## 3. `event_id` Generation Rule

首选规则：

1. 仅对 `_type=message` 行生成 `event_id`。
2. 取 `file_alias`、`line_no`、`platformMessageId` 作为稳定输入。
3. 执行 `sha1("weflow|{file_alias}|{line_no}|{platformMessageId}")`。
4. 取前 16 个十六进制字符，前缀化为 `evt_`。

示例：

```text
evt_ + sha1("weflow|file_02|412|<platformMessageId>")[:16]
```

回退规则：

- 若未来样本里出现缺失 `platformMessageId` 的 message 行，则退化为：

```text
sha1("weflow|{file_alias}|{line_no}|{timestamp}|{sender_hash}|{type}")
```

要求：

- `event_id` 不得直接泄露原始 `platformMessageId`。
- 同一输入必须在多次重跑时生成相同的 `event_id`。

## 4. `source_ref` And `raw_ref` Rule

### 4.1 `source_ref`

建议结构：

```json
{
  "file_alias": "file_02",
  "line_no": 412,
  "platform_message_id_hash": "pmid_90fe12ab",
  "reply_to_platform_message_id_hash": "pmid_90fe12aa"
}
```

规则：

- `file_alias` 使用 `file_XX`，绝不写真实原始文件名。
- `platform_message_id_hash` 和 `reply_to_platform_message_id_hash` 使用稳定哈希，不落明文 ID。
- `line_no` 允许明文保留，因为它本身不暴露内容。

### 4.2 `raw_ref`

建议格式：

```text
weflow:{file_alias}:{line_no}
```

示例：

```text
weflow:file_02:412
```

说明：

- `raw_ref` 的目标是做 evidence 链接和日志追踪，不负责承载真实文件名。
- 真正的“别名 -> 本地真实文件”映射只存在于本地运行态，不进入可提交目录。

## 5. `sender_role` Rule

当前样本支持如下保守判定流程：

1. 先从 `_type=member` 行提取 `(platformId, accountName)` 成员对。
2. 在多个私聊文件中寻找跨文件重复出现的成员对；当前样本显示有一对成员在 4 个文件里复用，可作为本地用户身份候选。
3. 对 `_type=message` 行，把 `(sender, accountName)` 与成员对做匹配：
   - 命中“本地用户候选对” -> `sender_role = "user"`
   - 命中同文件其他高频成员对 -> `sender_role = "contact"`
4. 若 `source_message_type_code = 80` 且内容表现为系统动作（撤回、红包、位置共享状态、打招呼等），优先写 `sender_role = "system"`。
5. 无法稳定判定时写 `sender_role = "unknown"`，并在 `risk_flags` 里加入 `sender_role_unresolved`。

注意：

- 不要简单用 `sender == accountName` 判断方向；当前样本里这两个字段属于不同身份槽位。
- `file_04` 虽然是私聊导出，但 `member` 行很多，说明“成员集合”不能直接等价于“当前会话仅两人”。

## 6. Timestamp Parse Rule

规则：

1. 原始 `timestamp` 按 Unix epoch seconds 解析。
2. 原始整数原样保留到 `timestamp_epoch_s`。
3. 归一化输出时，转换为带时区偏移的 ISO 8601 字符串，写入 `timestamp`。
4. 时区不要从文本内容猜测；由 adapter 配置项显式提供，当前数据默认候选为 `Asia/Shanghai`。
5. 缺失或非法时间戳时：
   - `timestamp = null`
   - `status` 不变
   - `risk_flags += ["timestamp_missing_or_invalid"]`

当前样本里时间值全部合法，但原始行没有显式时区字段，因此“使用哪个本地时区输出”仍然是配置问题，不应被硬编码成已证实事实。

## 7. `message_type` Mapping Rule

建议把 WeFlow 原始 `type` 与归一化层拆开：保留 `source_message_type_code`，同时给出保守的 `message_type`。

| WeFlow `type` | 当前样本证据 | `message_type` 建议 | 其他字段 |
| --- | --- | --- | --- |
| `0` | 绝大多数为普通文本/短句 | `text` | 若内容明显为占位列表，可降级为 `mixed` 并加 `risk_flags` |
| `25` | 100% 带 `replyToMessageId` | `text` | `interaction_flags += ["reply"]`；能解析时填 `reply_to_event_id` |
| `80` | 系统播报/撤回/红包/位置共享结束等 | `system` | 撤回类建议写 `status = "recalled"` |
| `7` | 结构化内容、媒体占位、转发聊天记录混合存在 | `mixed` | 用 `content_kind_hint` 标注 `forwarded_records` / `image_like` / `unsupported_media` |
| `4` / `23` / `24` / `99` | 样本极少，且为结构化内容 | `unknown` | 保留原始 `source_message_type_code`，等 T102/T103 再细分 |

设计原因：

- 当前 T100 只做 schema profiling，不做过早的语义猜测。
- 第一版 adapter 宁可把不确定类型保守映射为 `mixed` / `unknown`，也不要在没有足够证据时硬判成图片、语音或文件。

## 8. Redaction Principles

1. 文档、fixture、测试、review artifact 中不得出现真实聊天原文。
2. 真实文件名统一改写成 `file_XX`。
3. `sender`、`accountName`、`platformId`、`platformMessageId`、`replyToMessageId` 必须用稳定哈希或生成别名替换。
4. `chatRecords`、引用内容、系统播报里的人名同样适用脱敏规则。
5. 若将来需要在 `private/distilled/` 中保留私有原文，也必须保证这些文件继续留在 `.gitignore` 保护范围内。

## 9. Current Open Questions

1. `type=7` 里有哪些稳定子类，是否值得拆成 `image` / `file` / `forwarded_records` / `app_share` 多个归一化类型。
2. `type=4`、`23`、`24`、`99` 的精确语义是什么，是否只在少量联系人或少量交互场景里出现。
3. `type=80` 是否需要进一步区分“系统播报”和“带 actor 的撤回事件”。
4. `file_04` 中额外 `member` 行的来源是什么，是否会影响私聊和群聊的统一方向判定。
5. `timestamp` 的最终输出时区应固定为 `Asia/Shanghai`，还是在 normalized event 中同时保留 UTC 与本地时间字段。
