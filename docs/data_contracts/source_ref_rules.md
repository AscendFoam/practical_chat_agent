# Source Ref Rules

更新日期：2026-05-14

本文档定义 WeFlow normalize 过程中的 `source_ref`、`raw_ref` 和相关 `event_id` 引用边界。目标是同时满足两件事：

1. evidence 能回到本地原始 JSONL 行；
2. 可提交目录不泄露真实文件名、真实消息 ID 或真实联系人标识。

## 1. Design Goals

- 保留对原始证据的可追溯性。
- 在 `docs/`、`examples/`、`tests/` 中只暴露别名、行号和哈希别名。
- 让 `event_id` / `source_ref` / `raw_ref` 在多次重跑中保持稳定。
- 把“本地真实文件 -> file alias”的映射限制在运行态或 `private/` 内部。

## 2. Allowed Public Shape

对可提交文档、fixture、review artifact，允许公开的 source ref 只应长这样：

```json
{
  "file_alias": "file_01",
  "line_no": 4,
  "platform_message_id_hash": "pmid_a1b2c3d4",
  "reply_to_platform_message_id_hash": "pmid_a1b2c3d3"
}
```

对应的 `raw_ref`：

```text
weflow:file_01:4
```

不允许公开：

- 真实文件名
- 真实 `platformMessageId`
- 真实 `replyToMessageId`
- 真实联系人姓名或账号 ID

## 3. File Alias Rules

### 3.1 Alias Format

文件别名统一使用：

```text
file_01
file_02
file_03
...
```

要求：

- 只按当前输入集合分配，不从真实文件名截前缀。
- 同一 run 内稳定。
- 出现在 docs/examples/tests 时，只能使用别名，不能拼接真实路径。

### 3.2 Alias Mapping Storage

真实文件名与 `file_XX` 的映射：

- 可以存在运行态内存
- 可以存在 `private/distilled/<run_id>/` 下的私有 run report
- 不得进入 `docs/`、`examples/`、`tests/`

## 4. Line Number Rules

`line_no` 允许公开保留，原因是：

- 行号本身不包含内容
- 对 reviewer 和 validator 足够有用
- 与 `file_alias` 组合后可在本地定位对应 JSONL 行

限制：

- 行号必须相对于原始 JSONL 文件，从 1 开始计数
- 如果未来预处理会过滤空行或注释，必须明确写入“原始文件行号”，不能写“过滤后序号”

## 5. Message ID And Reply ID Rules

### 5.1 Public Artifacts

在 `docs/`、`examples/`、`tests/` 中：

- 不公开真实 `platformMessageId`
- 不公开真实 `replyToMessageId`
- 只允许出现两类值：
  - 纯合成值：`msg_0001`
  - 哈希别名：`pmid_a1b2c3d4`

### 5.2 Private Runtime

在 `private/` 内部运行态中：

- 可以暂存原始 `platformMessageId`
- 可以用它建立 reply 链路和 `event_id`
- 后续若产物可能离开 `private/`，必须先转成哈希别名或内部 ID

## 6. `source_ref` Object Rules

推荐字段：

| 字段 | 是否公开 | 说明 |
| --- | --- | --- |
| `file_alias` | 是 | `file_XX` |
| `line_no` | 是 | 原始文件行号 |
| `platform_message_id_hash` | 是 | 原始 `platformMessageId` 的哈希别名 |
| `reply_to_platform_message_id_hash` | 条件公开 | 仅在 reply 场景下出现 |

说明：

- `source_ref` 的职责是“让证据可追溯”，不是“完整复制原始行元数据”。
- 如果某条 message 没有 reply 关系，就不需要 `reply_to_platform_message_id_hash`。
- 若未来需要加 `conversation_alias`、`contact_alias`，也必须使用别名，不得写真实值。

## 7. `raw_ref` String Rules

格式固定为：

```text
weflow:{file_alias}:{line_no}
```

示例：

```text
weflow:file_01:4
```

规则：

- `raw_ref` 不包含真实文件名、真实 message ID、真实联系人名。
- `raw_ref` 的用途是日志、evidence 链接和 review Markdown；更细粒度定位靠 `source_ref` 补充。
- 如果将来引入其他 source 类型，前缀必须保留命名空间，例如 `telegram:`、`feishu:`。

## 8. `event_id` Relationship

`event_id` 仍应从稳定输入生成，但公开规则与 `source_ref` 保持一致：

- 不把真实 `platformMessageId` 暴露到 docs/examples/tests
- 使用带命名空间前缀的稳定 hash alias，例如 `evt_<hex>`

当前与 T100 contract 的关系：

- `normalized_event_contract.md` 里给出了当前草案示例
- T102 会最终确认底层 digest 继续使用 SHA-1，还是升级为 SHA-256
- 无论底层 digest 如何调整，公共形态都应保持 `evt_<hex>`，避免把算法细节耦合到文档消费者

## 9. Docs / Examples / Tests Rules

### 9.1 `docs/`

允许：

- `file_XX`
- `line_no`
- `pmid_<hex>`
- `evt_<hex>`
- `weflow:file_XX:<line_no>`

禁止：

- `private/chat_history/真实文件名.jsonl`
- 真实消息 ID
- 真实 reply 目标 ID

### 9.2 `examples/`

允许：

- 纯合成 `platformMessageId`，例如 `msg_0001`
- 预览型 `sourceRefPreview` / `rawRefPreview`

禁止：

- 从真实导出里复制的原始 ID
- 能反推出真实联系人或真实文件的 path / id / name

### 9.3 `tests/`

允许：

- 合成 alias、合成 line number、哈希占位符

禁止：

- 依赖真实私聊文件名或真实 message ID 做断言

## 10. Sample Fixture Convention

`examples/payloads/weflow_redacted_sample.jsonl` 继续以“接近 WeFlow 原始输入”的结构为主，但本轮额外加入以下 preview 字段：

- `eventIdPreview`
- `sourceRefPreview`
- `rawRefPreview`

这些 preview 字段的作用：

- 演示 T101 定下来的 `event_id` / `source_ref` / `raw_ref` 公共形态
- 让 reviewer 能直接看到样例是否安全
- 明确它们是 fixture 注释字段，不应被当成原始 WeFlow 官方字段

## 11. Red Lines

以下任一情况都不符合本规则：

1. `source_ref` 里直接写真实文件名。
2. `raw_ref` 里携带真实文件名或真实 message ID。
3. 公开样例里同时出现真实 `platformMessageId` 和其哈希别名。
4. 通过 message ID、reply ID、文件名片段可以回推真实联系人。
