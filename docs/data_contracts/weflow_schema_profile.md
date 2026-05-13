# WeFlow Schema Profile

更新日期：2026-05-14

本文档基于 `private/chat_history/` 下 4 个 WeFlow JSONL 导出文件的本地统计结果编写，只记录结构、计数和候选规则，不包含真实聊天原文、真实联系人姓名、真实原始文件名或真实平台 ID。文中使用 `file_01` 到 `file_04` 作为文件别名。

## 1. Dataset Summary

| 指标 | 数值 |
| --- | ---: |
| 文件数量 | 4 |
| 总行数 | 38,289 |
| 可解析 JSON 行数 | 38,289 |
| 失败行数 | 0 |
| `_type=header` | 4 |
| `_type=member` | 32 |
| `_type=message` | 38,253 |

### 1.1 File-Level Summary

| 文件别名 | 大小（bytes） | header 行 | member 行 | message 行 | reply 行 | `chatRecords` 行 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `file_01` | 344,012 | 1 | 3 | 1,322 | 265 | 1 |
| `file_02` | 1,320,283 | 1 | 2 | 6,216 | 971 | 0 |
| `file_03` | 146,293 | 1 | 2 | 483 | 181 | 0 |
| `file_04` | 7,938,599 | 1 | 25 | 30,232 | 3,373 | 114 |

观察：

- 4 个文件全部可解析，没有坏行。
- `file_04` 的 `meta.type` 仍为 `private`，但存在 25 条 `member` 行，说明导出文件里可能包含额外成员/引用对象/历史参与者信息；后续 parser 不能把 `member` 行数直接等同于“当前私聊人数”。

## 2. Row Classes

### 2.1 `_type=header`

出现 4 次，每个文件 1 行。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `_type` | `str` | 固定为 `header` |
| `chatlab` | `dict` | 导出工具元数据 |
| `meta` | `dict` | 会话元数据 |

嵌套字段：

- `chatlab.version: str`
- `chatlab.exportedAt: int`
- `chatlab.generator: str`
- `meta.name: str`
- `meta.platform: str`
- `meta.type: str`
- `meta.groupAvatar: str`

当前样本中：

- `meta.platform` 统一为 `wechat`
- `meta.type` 统一为 `private`

### 2.2 `_type=member`

出现 32 次。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `_type` | `str` | 固定为 `member` |
| `platformId` | `str` | 平台侧成员标识候选 |
| `accountName` | `str` | 成员展示名/账户名候选 |
| `avatar` | `str` | 头像路径或引用候选 |

### 2.3 `_type=message`

出现 38,253 次，是后续 normalized event 的主要来源。

必有字段：

| 字段 | 类型 | 出现率（相对 message 行） |
| --- | --- | ---: |
| `_type` | `str` | 100.00% |
| `sender` | `str` | 100.00% |
| `accountName` | `str` | 100.00% |
| `timestamp` | `int` | 100.00% |
| `type` | `int` | 100.00% |
| `content` | `str` | 100.00% |
| `platformMessageId` | `str` | 100.00% |

可选字段：

| 字段 | 类型 | 出现率（相对 message 行） | 说明 |
| --- | --- | ---: | --- |
| `replyToMessageId` | `str` | 12.52% | 引用/回复链路候选 |
| `chatRecords` | `list[dict]` | 0.30% | 转发聊天记录候选 |

`chatRecords[*]` 在样本中的嵌套字段：

- `sender: str`
- `accountName: str`
- `timestamp: int`
- `type: int`
- `content: str`
- `avatar: str`

## 3. Top-Level Field Set, Types, And Occurrence Rates

下表按“所有可解析 JSON 行”统计：

| 字段 | 出现次数 | 出现率 | 类型统计 |
| --- | ---: | ---: | --- |
| `_type` | 38,289 | 100.00% | `str: 38,289` |
| `accountName` | 38,285 | 99.99% | `str: 38,285` |
| `sender` | 38,253 | 99.91% | `str: 38,253` |
| `timestamp` | 38,253 | 99.91% | `int: 38,253` |
| `type` | 38,253 | 99.91% | `int: 38,253` |
| `content` | 38,253 | 99.91% | `str: 38,253` |
| `platformMessageId` | 38,253 | 99.91% | `str: 38,253` |
| `replyToMessageId` | 4,790 | 12.51% | `str: 4,790` |
| `chatRecords` | 115 | 0.30% | `list: 115` |
| `platformId` | 32 | 0.08% | `str: 32` |
| `avatar` | 32 | 0.08% | `str: 32` |
| `chatlab` | 4 | 0.01% | `dict: 4` |
| `meta` | 4 | 0.01% | `dict: 4` |

## 4. Message Type Candidates

`type` 是 message 行的主候选消息类型字段。当前样本里出现的编码如下：

| `type` | 行数 | 占比 | 结构观察 | 当前候选归类 |
| --- | ---: | ---: | --- | --- |
| `0` | 27,828 | 72.75% | 以普通短文本为主，也有少量列表状占位内容 | `text` 主候选 |
| `7` | 5,346 | 13.98% | 大量列表状/结构化内容；部分为本地媒体占位路径；少量行带 `chatRecords` | `mixed` / `media_or_app` 候选 |
| `25` | 4,774 | 12.48% | 100% 带 `replyToMessageId`；内容中常见引用包装 | `text` + `reply` 标记候选 |
| `80` | 264 | 0.69% | 文本表现为撤回、红包、位置共享结束、打招呼等系统动作 | `system` / `recalled` 候选 |
| `4` | 18 | 0.05% | 稀有结构化列表状内容 | `unknown` |
| `99` | 12 | 0.03% | 稀有结构化列表状内容 | `unknown` |
| `24` | 9 | 0.02% | 稀有结构化列表状内容 | `unknown` |
| `23` | 2 | 0.01% | 稀有结构化列表状内容 | `unknown` |

补充观察：

- `type=25` 的 `replyToMessageId` 共有 4,578 个唯一目标 ID，其中 4,576 个能在当前样本内解析到对应的 `platformMessageId`，2 个未命中。
- `platformMessageId` 在当前样本 38,253 条 message 行里全部唯一，适合作为 `event_id` 的一部分输入，但不应以明文进入可提交产物。
- `type=7` 的 115 行包含 `chatRecords`，说明它至少覆盖“转发聊天记录”一类消息；其余 `type=7` 行还混有媒体占位路径和其他结构化内容，因此后续 adapter 不能只靠 `type=7` 直接断言成单一媒体类型。

## 5. Timestamp Candidates And Format Observations

`timestamp` 是当前样本里最稳定的时间字段候选：

- 类型固定为 `int`
- 出现于 100% 的 message 行
- 数值规模符合 Unix epoch seconds，而不是 milliseconds

时间范围（按 UTC 解释 epoch）：

- 最早：`2025-11-25T08:05:57+00:00`
- 最晚：`2026-05-13T08:54:11+00:00`

当前未见：

- 行内显式时区字段
- 独立的字符串时间字段

结论：

- `timestamp` 可以作为后续 normalized event 的原始时间源。
- 时区应由 adapter 配置项显式提供；不要在 contract 里把原始 epoch 误写成“自带 +08:00 标签的字符串时间”。

## 6. Sender / Receiver / Direction Candidates

当前样本对“谁发的消息”给出了较强信号：

1. `member` 行提供了 `(platformId, accountName)` 对。
2. `message` 行提供了 `(sender, accountName)` 对。
3. 在每个文件内，message 行只使用两个高频成对身份；其中一对跨 4 个文件重复出现，强烈提示它是本地用户自身身份。

因此，当前最稳妥的方向判定候选规则是：

- `sender` 更像平台侧发言者标识。
- `accountName` 更像该发言者在导出中的展示名槽位。
- 在私聊导出里，可通过“跨文件重复出现的成员对”识别本地用户，再把其余活跃成员对视为联系人。

限制：

- 原始行里没有单独的“receiver”字段。
- `file_04` 虽然是 `private` 导出，但 `member` 行数显著大于 2，说明成员集合不能被机械解读为“当前聊天实时成员列表”。

## 7. Media / System / Recall / Reference Candidates

| 线索字段 / 模式 | 计数 | 候选意义 |
| --- | ---: | --- |
| `replyToMessageId` | 4,790 行 | 明确的引用/回复链路 |
| `chatRecords` | 115 行 | 转发聊天记录或嵌套消息集合 |
| `type=80` | 264 行 | 系统动作、撤回、红包、位置共享状态等 |
| `platformMessageId` | 38,253 行 | 原始消息唯一标识候选 |
| `avatar` / `groupAvatar` | 36 行 | 头像或会话图片引用 |

对 `type=80` 的安全观察：

- 内容形态表现出系统播报性质。
- 其中一部分明显对应“撤回一条消息”，后续 normalized event 可以把这类行映射为 `status=recalled` 或 `message_type=system`。

## 8. Privacy Risk Fields

以下字段不应以明文进入可提交文档、fixture、测试或公开日志：

- `content`
- `sender`
- `accountName`
- `platformId`
- `platformMessageId`
- `replyToMessageId`
- `avatar`
- `meta.name`
- `meta.groupAvatar`
- `chatRecords[*].content`
- `chatRecords[*].sender`
- `chatRecords[*].accountName`
- `chatRecords[*].avatar`

建议处理方式：

- 真实文件名只在本地运行态使用，落盘时改为 `file_XX` 别名。
- 所有用户、联系人、平台 ID、消息 ID 用稳定哈希或生成别名替代。
- 样例和文档一律使用合成文本，不保留原文片段。

## 9. Adapter Notes For T102

- 只把 `_type=message` 行映射为 normalized event；`header` 和 `member` 作为元数据输入。
- 必须保留 `source_message_type_code`，不要在第一版 adapter 里丢弃 WeFlow 原始 `type`。
- `type=7`、`type=4`、`type=23`、`type=24`、`type=99` 先走保守映射，后续再细分。
- 方向判定需要利用 `member` 行和跨文件复用身份，不建议只靠单个文件内的名称比较。
