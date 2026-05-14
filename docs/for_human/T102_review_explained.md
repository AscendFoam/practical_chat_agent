# T102 任务与 Review 通俗解释

## 第一部分：T102 做了什么？（通俗解释）

### 背景

在 T102 之前，项目已经完成了两件事：

- **T100**：搞清楚了 WeFlow 导出的微信聊天记录长什么样——每行是 JSON，分三种类型（header/member/message），总共约 3.8 万行消息。
- **T101**：定义了隐私规则——哪些信息只能放在私密目录 `private/`，哪些可以放进 git 提交的代码里。

但这只是"文档和规则"，还没有任何可运行的代码。T102 的目标就是**把规则变成真正能跑的程序**。

### T102 要做的事

简单说：**写一个命令行工具，把微信聊天记录从原始格式转换成统一格式。**

类比：你有一堆不同格式的收据（手写的、打印的、电子的），T102 就是一个"收据标准化机器"——把所有收据统一整理成相同的表格格式，方便后续处理。

具体来说：

1. **读取** `private/chat_history/` 下的微信聊天记录文件（WeFlow 导出的 JSONL 格式）。
2. **识别** 每条消息是谁发的（用户自己 vs 联系人 vs 系统消息）。
3. **转换** 成统一的 normalized event 格式（统一的时间格式、统一的 ID 格式、统一的消息类型）。
4. **输出** 到 `private/distilled/` 目录，不泄露到任何会被 git 提交的地方。

### 为什么需要这一步

原始聊天记录的格式是 WeFlow 工具自己的格式，字段名和值都跟项目后续需要的格式不一样。比如：

- WeFlow 用数字表示消息类型（0=文本, 80=系统消息），但项目需要用文字（"text", "system"）。
- WeFlow 用原始微信 ID 标识发送者，但项目需要用哈希化的匿名 ID 保护隐私。
- 原始文件名包含真实联系人名字（如"私聊_某某.jsonl"），但项目里只能用 `file_01` 这样的代号。

这一步做完之后，后续的 chunker（把对话切块）、LLM 蒸馏（提取记忆）等模块就能在干净统一的数据上工作，不用再管 WeFlow 的原始格式。

---

## 第二部分：实现详解

### 任务目标

实现一个最小的命令行工具 `chatlog-normalize`，把 WeFlow JSONL 转换为 normalized events，输出限定在 `private/distilled/`。

### 任务流程

整个 normalize 流程分两阶段：

```
阶段 1: 扫描（_scan_inputs）
  读取所有 JSONL 文件 → 统计行数/类型 → 推断"哪个是我"和"每个文件的对方是谁"

阶段 2: 转换（_normalize_messages）
  再次读取文件 → 逐条消息转换格式 → 写入 normalized_events.jsonl
```

### 代码变化

#### 1. 新增 `src/practical_chat_agent/services/chatlog_ingestion.py`（~711 行）

这是核心实现，包含一个 `ChatlogIngestionService` 类。关键设计：

**身份推断（最核心的逻辑）**

代码需要判断每条消息是"用户自己发的"还是"联系人发的"。WeFlow 的数据里没有直接标明这一点，所以代码用了一个启发式策略：

1. 先看 `member` 行——有些成员对在多个聊天文件里重复出现（因为用户在多个聊天里身份相同），这个跨文件复用的身份对大概率就是"用户自己"。
2. 如果 member 行不够用，退化为看 `message` 行——在每个文件的 `(sender, accountName)` 消息对中，跨文件复用最多的就是"用户自己"。
3. 每个文件里排除"用户自己"之后，出现最多的消息对就是"联系人"。
4. 如果推断不出来，标记为 `unknown` 并在 `risk_flags` 里报警。

**消息类型映射**

WeFlow 的 `type` 字段是数字，代码做了保守映射：

- `type=0` → `text`（普通文本）
- `type=25` → `text`（带回复引用的文本）
- `type=80` → `system`（系统消息，如撤回通知、红包通知）
- `type=7` → `mixed`（混合内容，可能含图片、转发聊天记录等）
- 其他稀有类型 → `unknown`

**隐私保护**

所有输出中的 ID 都经过 SHA-1 哈希处理：
- 真实文件名 → `file_01`, `file_02`
- 发送者 ID → `sender_abc123def456`
- 消息 ID → `pmid_90fe12ab`
- 事件 ID → `evt_4b8c2d0f8d3c1a77`

路径边界通过 `Path.resolve()` + `relative_to()` 强制校验，确保输入只能在 `private/chat_history/`，输出只能在 `private/distilled/`。

**reply 链路**

如果消息引用了另一条消息（WeFlow 的 `replyToMessageId`），代码会在同文件的已扫描事件中查找对应的 `event_id`，建立 reply 链路。找不到的会在 `risk_flags` 中标记 `reply_target_unresolved`。

**forwarded_records**

对于转发聊天记录（WeFlow 的 `chatRecords` 字段），代码递归处理每条嵌套记录，同样做身份推断和匿名化。

#### 2. 修改 `src/practical_chat_agent/app/main.py`（新增 ~55 行）

注册了新的 CLI 命令 `chatlog-normalize`，提供 5 个选项：

| 选项 | 作用 |
| --- | --- |
| `--input` | 输入目录或文件，默认 `private/chat_history` |
| `--output` | 输出目录，默认 `private/distilled/weflow_normalize_时间戳` |
| `--limit` | 只处理前 N 条消息，用于小样本验证 |
| `--dry-run` | 只输出统计报告，不写文件 |
| `--timezone-name` | 时间戳渲染时区，默认 `Asia/Shanghai` |

CLI 层很薄——解析参数、调用 service、输出 report。所有逻辑在 service 里。

#### 3. 修改 `docs/07_handoff.md`

- 更新 T102 状态为"worker 交付已出，等待 reviewer 判定"。
- 新增 8.1 节记录 T102 的产物清单、高信号结论和本地验证命令。

#### 4. 修改 `docs/08_risks_and_open_questions.md`

- 更新 R011（type=80/chatRecords 已保守处理）。
- 更新 R012（event_id SHA-1 已落地）。
- 关闭 Q102（时区默认 Asia/Shanghai）和 Q103（type=7/4/23/24/99 保守映射）。

### 对后续开发的意义

T102 是整个离线蒸馏管线的**数据入口**。它产出的 `normalized_events.jsonl` 是后续所有模块的输入：

```
T102 normalize → T110 chunker → T112 summary/fact extraction → T113 ContactSkill
```

具体影响：

1. **T110（chunker）**：可以在 T102 产出的统一格式上直接工作，不需要再处理 WeFlow 原始格式。
2. **T112（LLM 蒸馏）**：每条 normalized event 都有稳定的 `event_id` 和 `source_ref`，可以作为 evidence ref 的基础。
3. **T150（测试）**：有了真实可运行的 normalize CLI，可以用 limit 小样本生成脱敏 fixture。
4. **T103（M0 review）**：T102 完成意味着 Milestone 0 的所有任务都已落地为可运行代码。

---

## 第三部分：为什么给出 PASS 的 Review 结论

### Review 过程

我作为 reviewer 做了以下检查：

1. **任务完成度**：对照任务包逐条检查，所有要求都已实现（CLI 参数、输出格式、dry-run/limit 支持、路径限制、文档更新）。
2. **隐私合规**：逐字段检查了所有输出（stdout report、normalized_events.jsonl、run_report.json），确认没有真实原文、真实文件名或真实联系人名泄露到 git 可提交的区域。
3. **合约对齐**：把代码的输出字段与 T100 normalized_event_contract 和 T101 privacy_redaction_rules / source_ref_rules 逐一比对，全部一致。
4. **实现真实性**：检查了每个核心功能（身份推断、类型映射、reply 链路、路径校验），确认都是真实实现，不是 mock 或 stub。
5. **越界检查**：确认没有实现任务包禁止的功能（LLM 调用、chunker、ContactSkill、数据库、实时微信接入）。
6. **回归风险**：确认新增代码不影响已有的 Telegram、飞书、会议、记忆等链路。
7. **文档准确性**：确认 handoff 和 risks 文档没有把计划写成已完成事实。

### 给出 PASS 的理由

**核心判断：代码做了该做的事，没做不该做的事，隐私没泄漏。**

展开来说：

1. **任务完成**：CLI 的 5 个选项全部实现，输出格式与合约一致，dry-run 和 limit 都能用。
2. **隐私安全**：这是整个项目最敏感的部分——处理真实聊天记录。代码的防护是多层的：
   - 路径边界强制校验（输入/输出只能在 private/ 下）
   - 所有 ID 哈希化（不暴露原始微信 ID）
   - 文件名用别名替代
   - stdout 只输出统计信息
   - 原始文本只留在 `private/distilled/`（受 .gitignore 保护）
3. **无伪实现**：身份推断用的是真实的跨文件复用统计，不是写死的。类型映射基于 WeFlow 实际的 type code，不是猜的。
4. **无越界**：代码严格限制在 normalize 层，没有提前做 chunking、LLM 抽取或 ContactSkill。
5. **验证充分**：worker 跑了编译检查、dry-run、小样本生成和 JSON 解析验证。

### 发现的 6 个非阻塞问题

我发现了 6 个值得注意但不阻碍通过的问题（Non-blocking Issues），都是"可以更好但不影响当前任务完成"的级别：

1. **无效时区静默降级**：传入错误的时区名不会报错，只是默默用 UTC。建议加个 warning。
2. **双次文件读取**：扫描和转换各读一次文件，性能可以优化，但当前数据量不大。
3. **全量内存缓存**：所有转换结果存在内存里再写文件，大数据量时可能有问题。
4. **系统消息关键词硬编码**：用 7 个中文关键词匹配系统消息，可能漏判，但有 unknown 兜底。
5. **PII 替换 token 未实现**：T101 定义的 `[PHONE]` 等 token 在 normalize 阶段没实现，但这是合理的——应该在后续 LLM 蒸馏阶段做。
6. **单文件场景身份推断可能不稳定**：如果只有一个聊天文件，跨文件复用策略无法工作，但有 warning 提示。

这些问题都不影响 T102 的完成判定，可以在后续任务中顺带处理。
