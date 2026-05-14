# Privacy Redaction Rules

更新日期：2026-05-14

本文档定义 WeFlow 聊天记录在本项目中的隐私脱敏边界。目标不是实现脱敏器，而是先把哪些信息可以进入 `docs/`、`examples/`、`tests/`，哪些信息只能留在 `private/` 说清楚，避免 T102 之后的 parser、normalize CLI 和蒸馏产物把私密内容带进可提交目录。

## 1. Scope

本规则适用于：

- `private/chat_history/**` 原始 WeFlow JSONL
- 未来 `private/distilled/**` 下的 normalize / chunk / summary / fact 产物
- `docs/`、`examples/`、`tests/` 中的 schema、fixture、review artifact、验证说明

默认原则：

1. 原始聊天原文只留在 `private/`。
2. 可提交目录只允许出现合成值、稳定别名、哈希别名、结构样例和计数统计。
3. 任何能直接或间接反推出真实联系人的标识，都不应明文进入 `docs/`、`examples/`、`tests/`。

## 2. Data Zone Rules

| 数据区域 | 可包含内容 | 禁止内容 |
| --- | --- | --- |
| `private/chat_history/**` | 原始 JSONL、真实 message text、真实文件名、真实平台 ID | 提交到 git |
| `private/distilled/**` | 运行时需要的私有中间产物；必要时可含原始 text 或精确 refs | 提交到 git；未受控扩散到 `docs/` / `examples/` / `tests/` |
| `docs/**` | 结构说明、统计、规则、合成示例、哈希化 ref 形态 | 真实原文、真实姓名、真实原始文件名、真实账号 ID |
| `examples/**` | 手工脱敏或纯合成 payload/JSONL fixture | 从真实聊天里直接复制的文本、真实 message ID、真实媒体路径 |
| `tests/**` | 合成输入、断言用占位值、脱敏 fixture | 真实聊天数据、真实联系人标识 |

## 3. PII And Sensitive Data Classes

### 3.1 Direct Identifiers

以下字段或内容按“直接标识”处理：

- 真实联系人姓名
- 真实备注名、昵称、群别名
- 真实原始文件名中包含的联系人信息
- `platformId`、`sender`、`accountName`、`platformMessageId`、`replyToMessageId`
- 头像路径、媒体路径、下载 URL、中转文件名

规则：

- `docs/`、`examples/`、`tests/` 只能出现稳定别名或合成值，例如：
  - `file_01`
  - `ACCOUNT_SELF`
  - `CONTACT_A`
  - `wxid_self_redacted`
  - `pmid_a1b2c3d4`
- 不得出现从真实值截断得到的“半脱敏”字符串，例如姓名首字、文件名前缀、ID 后四位。

### 3.2 Message Content And Quotes

以下内容按“原文内容”处理：

- `content`
- 引用回复里的被引内容
- `chatRecords[*].content`
- 系统播报中的 actor 名称与事件文本

规则：

- 可提交目录不保留任何真实聊天原文，哪怕是极短片段。
- 样例只能使用合成文本，例如 `[SYNTHETIC] neutral sample text`。
- 不允许以“节选一句真实话”作为文档例子。

### 3.3 Contact Metadata

以下内容按“联系人元数据”处理：

- `meta.name`
- `meta.groupAvatar`
- `avatar`
- 导出工具附带的会话封面、群头像、联系人图片引用

规则：

- `docs/`、`examples/`、`tests/` 只允许出现占位文件名或说明性字符串。
- 若某字段对结构说明不重要，优先删除，而不是保留占位路径。

### 3.4 Embedded Personal Data

即使字段本身不是“身份字段”，一旦内容里出现以下信息，仍然按高敏感数据处理：

- 手机号、座机号、邮箱
- 身份证、护照、银行卡、支付单号、收款码
- 住址、学校、公司、地理位置
- 第三方账号、token、cookie、二维码内容
- 明显的隐私事件、医疗信息、财务信息

规则：

- `private/` 外一律不保留明文。
- 若未来需要在私有蒸馏流程中保留，应至少支持结构化替换，例如：
  - `[PHONE]`
  - `[EMAIL]`
  - `[ADDRESS]`
  - `[ACCOUNT_ID]`
  - `[PAYMENT_REF]`
  - `[TOKEN]`

## 4. Field Handling Matrix

| 字段/内容 | `private/chat_history` | `private/distilled` | `docs/examples/tests` |
| --- | --- | --- | --- |
| 真实文件名 | 保留 | 映射后可不保留 | 禁止；改为 `file_XX` |
| `content` | 保留 | 仅在确有必要时保留 | 禁止真实值；只能用合成文本 |
| `sender` / `accountName` / `platformId` | 保留 | 转成稳定 hash/alias | 禁止真实值；只能用合成别名 |
| `platformMessageId` / `replyToMessageId` | 保留 | 转成 hash / internal ID | 禁止真实值；只能用合成值或哈希别名 |
| `avatar` / `groupAvatar` / 媒体路径 | 保留 | 可删或转占位 ref | 禁止真实路径 |
| `timestamp` | 保留 | 保留 | 文档可出现合成或说明性时间；不要把真实时间线当案例摘录 |
| `chatRecords[*]` 嵌套内容 | 保留 | 递归脱敏 | 递归使用合成值或占位符 |

## 5. Replacement Strategy

### 5.1 Stable Alias

用于文档、fixture、测试：

- 本地用户：`ACCOUNT_SELF`
- 联系人：`CONTACT_A`、`CONTACT_B`
- 会话：`conversation_redacted`
- 文件：`file_01`、`file_02`

要求：

- 同一 artifact 内保持一致，便于 reviewer 看懂结构。
- 不要求跨所有 artifact 共享同一别名映射，除非验证场景明确需要。

### 5.2 Stable Hash Alias

用于下游 evidence / source_ref / internal ID 说明：

- `pmid_<hex>`
- `sender_<hex>`
- `contact_<hex>`
- `evt_<hex>`

要求：

- 必须带命名空间前缀，避免把原始值误看成真实 ID。
- 只能展示哈希别名，不能同时把原始值和哈希值并排出现。

### 5.3 Synthetic Text

用于样例中的 `content`、引用内容、系统播报文本：

- 只能写人工合成内容
- 应避免拟真到可被误认成真实聊天摘录
- 推荐显式加 `[SYNTHETIC]` 前缀

## 6. Nested Structure Rules

### 6.1 Reply / Quote

- `replyToMessageId` 本身不能明文进入可提交目录。
- 如果样例需要展示引用关系，使用合成 ID 或哈希别名。
- 引用内容同样不得保留真实原文。

### 6.2 `chatRecords`

- 视为嵌套 message 列表，递归应用同一套规则。
- 任意一层出现真实 `sender` / `accountName` / `content` / `avatar`，都算泄漏。

### 6.3 System Messages

- 对撤回、红包、位置共享等系统播报，不要因为“不是对话正文”就放松要求。
- 若播报文本里包含联系人姓名或真实账号名，也必须替换成占位名。

## 7. Red-Line Checklist

以下任一情况都视为 T101/T102 阶段失败：

1. `docs/`、`examples/`、`tests/` 中出现真实聊天原文。
2. 出现真实联系人姓名、备注名或可识别原始文件名。
3. 出现真实 `platformMessageId`、`replyToMessageId`、`platformId`、媒体路径。
4. 使用“只遮一半”的方式保留可回推身份的信息。
5. 用真实文本稍改几个字就当作“脱敏样例”。

## 8. T101 Deliverable Notes

- 本轮只定义规则，不实现脱敏器。
- T102 的 normalize CLI 必须遵守本规则，把私有 refs 留在 `private/distilled/`，把可提交样例限制在合成/脱敏范围内。
