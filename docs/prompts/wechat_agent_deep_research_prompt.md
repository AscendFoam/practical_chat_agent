# 微信优先 chat agent 后续推进深度调研 Prompt

你是接手 `practical_chat_agent` 项目的深度调研 AI。你的任务不是直接写代码，而是做一次面向后续工程推进的高质量技术调研与方案设计，重点回答：项目后续是否应该以微信为主线，是否应该引入 WeChatBot/iLink Bot SDK，如何实现微信聊天记录自动整理、长期记忆、联系人 skill 蒸馏，以及怎样把项目推进成一个更像真人聊天对象的 chat agent。

请用中文输出调研报告。报告要能直接指导后续工程实现，避免泛泛而谈。

## 1. 项目背景

当前仓库：`D:\Codes\Social\practical_chat_agent`

请先阅读并交叉核对这些文件：

- `docs/engineering_experiment_plan.md`
- `docs/stage_progress_summary.md`
- `docs/next_ai_handoff_prompt.md`
- `src/practical_chat_agent/app/container.py`
- `src/practical_chat_agent/runtime/agent_runtime.py`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/core/enums.py`
- `src/practical_chat_agent/services/chat_context.py`
- `src/practical_chat_agent/services/chat_suggestions.py`
- `src/practical_chat_agent/services/chat_memory.py`
- `src/practical_chat_agent/services/memory_retrieval.py`
- `src/practical_chat_agent/services/memory_lifecycle.py`
- `src/practical_chat_agent/services/policy.py`
- `src/practical_chat_agent/services/delivery.py`
- `src/practical_chat_agent/connectors/desktop/wechat_desktop.py`
- `src/practical_chat_agent/connectors/delivery/telegram_bot.py`

注意：最近一次较大规模 git 提交是 2026-05-01。`docs/stage_progress_summary.md` 的更新日期是 2026-04-20，因此它已经部分过时。不要只按该总结判断当前进度。

根据 2026-05-01 的 handoff 和代码现状，当前真实状态大致是：

- P0 基础框架已完成：统一模型、MySQL 仓储、CLI、AppContainer、AgentRuntime 都已存在。
- P1 聊天采集已覆盖 Telegram/Feishu 入站 payload 和微信桌面 UI/OCR 扫描。
- 会议子系统 P6/P7 已经较成熟，但后续不是主线重点。
- 聊天智能中间层已经不只是“未开始”：已有 `ChatContextAssembler`、`ChatSuggestionService`、`ChatMemoryExtractionService`、`MemoryRetrievalService`、profile facets、`MemoryLifecycleService`。
- 受控发送链路也已经开始：已有 `DeliveryConnector` 抽象、Telegram 投递、`PolicyEngine`、`ActionDeliveryService`、`ActionRepository`、`action-list/show/approve/send` CLI。
- 微信目前已有 `WeChatDesktopConnector`，但它主要是当前可见会话的桌面 UI/OCR 扫描，不等同于稳定的微信 bot 接入，也不等同于全量历史聊天记录同步。

## 2. 用户的新方向与目标

用户现在更倾向于把后续主线放在微信上，因为微信聊天比飞书和 Telegram 更符合个人使用习惯。

用户关心的问题：

1. 微信开放了 WeChatBot / iLink Bot 相关机器人能力，是否有必要 clone `https://github.com/corespeed-io/wechatbot` 并搭建微信机器人？
2. 仍然希望自动扫描微信聊天记录并整理保存。
3. 希望能根据整合后的聊天记录，把聊天对象蒸馏成某种 `skill`，从而更好地塑造 chat agent。
4. 记忆模块是棘手重点：需要结合当前研究与工程可行性，设计一套能长期运行、可审计、可纠错的记忆系统。
5. 总体目标是打造一个类似真人一样自然、连续、有记忆、有关系感的聊天对象。

隐私和边界说明：

- 用户表示这些能力仅供自己使用，不会外传，也不会泄露他人隐私。
- 方案仍应默认本地优先、最小化外发、可脱敏、可删除、可审计。
- “聊天对象蒸馏成 skill”应优先理解为：提炼联系人画像、沟通偏好、关系上下文、话题边界和交互策略，用于让 agent 更懂如何与该联系人相关地辅助用户；不要设计成对外冒充真实个人或欺骗第三方的系统。

## 3. 必须调研的外部资料

请联网核实以下资料，不要只凭记忆：

- WeChatBot GitHub：`https://github.com/corespeed-io/wechatbot`
- WeChatBot 文档：`https://www.wechatbot.dev/` 与 `https://www.wechatbot.dev/en`
- iLink Bot 协议说明：`https://www.wechatbot.dev/en/protocol`
- Python SDK README：`https://github.com/corespeed-io/wechatbot/blob/main/python/README.md`
- Node.js SDK README、Go/Rust SDK README、pi-agent README
- npm / PyPI / crates.io / Go module 上的包名、版本、维护状态
- Tencent/微信官方相关来源，尤其是 `@tencent-weixin/openclaw-weixin`、OpenClaw、ClawBot、iLink Bot 的官方性、适用范围、限制和风险
- GitHub issues / releases / commits，用于判断项目成熟度、风险、维护活跃度

可作为调研起点的初步事实（仍需你再次核实）：

- `corespeed-io/wechatbot` 当前 README 宣称提供 Node.js、Python、Go、Rust 四种 SDK；Python 安装名是 `wechatbot-sdk`，要求 Python >= 3.9，依赖 `aiohttp` 和 `cryptography`。
- 该仓库 README 宣称能力包括扫码登录、长轮询接收、富媒体、`context_token` 自动管理、typing 指示、AES-128-ECB CDN 媒体加密、会话恢复和文本分片。
- iLink 协议文档显示收消息是 `getupdates` 长轮询，不是 WebSocket；首次 `get_updates_buf` 为空，后续要把返回的 `get_updates_buf` 当作不透明 cursor 持久化。
- iLink 协议文档强调 `context_token` 是回复路由的关键：入站消息带 token，出站 `sendmessage` 必须回传 token；如果要主动 `send(user_id, ...)`，也依赖此前缓存的上下文 token。
- Python SDK README 显示 `bot.reply(msg, text)` 自动携带 context token，`bot.send(user_id, text)` 需要先前已有上下文。
- Tencent/openclaw-weixin 是 OpenClaw 的 Weixin channel plugin，支持扫码登录授权，多账号登录和本地凭据保存；它与 WeChatBot SDK 的关系、官方性和可替代性需要仔细厘清。

调研时请特别核对：

- 这是微信官方开放能力，还是社区根据 iLink/OpenClaw 协议封装的 SDK？
- 是否支持个人微信号？是否要求扫码登录？是否会生成独立 bot 账号？
- 支持 1v1、群聊、公众号、企业微信的边界分别是什么？
- 是否能读取历史消息，还是只能接收 bot 登录后的新消息？
- 是否能主动发送消息？是否依赖 `context_token` 或先前会话上下文？
- 是否支持图片、语音、文件、视频等媒体收发和下载？
- token、cursor、context、凭据如何持久化？会话过期如何处理？
- 与当前仓库 Python 3.11+/MySQL/Typer CLI 架构集成的成本如何？
- 是否应该 clone 源码、作为子模块/vendor、直接依赖包，还是只先做隔离 POC？

## 4. 核心调研问题

### 4.1 是否应该 clone WeChatBot

请给出明确建议，但不要只回答“是/否”。至少比较四种方案：

1. 不 clone，先只读源码和文档，使用包管理器依赖做 POC。
2. clone 到仓库外部 sandbox，验证登录、收消息、发消息、媒体能力。
3. 作为 git submodule/vendor 引入本仓库。
4. 不依赖 WeChatBot，继续强化当前微信桌面 UI/OCR 方案。

请从以下维度评分：

- 稳定性
- 合规/账号风险
- 可维护性
- 与当前架构适配成本
- 是否支持用户想要的“微信主线 chat agent”
- 是否支持历史聊天记录扫描
- 是否支持半自动/审批式发送
- 隐私与安全

预期输出：给出阶段性建议，例如“不要马上 vendor 进主仓库；先在仓库外隔离验证，再抽象成 `WeChatIlinkConnector`”之类的可执行结论。

### 4.2 微信接入总体架构

请设计微信优先接入架构，至少包含：

- `WeChatIlinkInboundConnector`：长轮询接收新消息，转换成 `InboundEvent`。
- `WeChatIlinkDeliveryConnector`：基于 iLink context token 的回复/发送。
- `WeChatDesktopConnector` 的定位：继续作为可见会话扫描、历史补录、OCR 兜底，而不是替代 iLink bot。
- 凭据和状态持久化：bot token、base URL、cursor/get_updates_buf、context_token、media metadata、会话过期状态。
- MySQL schema 是否需要新增表：例如 `platform_accounts`、`platform_sessions`、`conversation_context_tokens`、`raw_message_payloads`、`media_assets`。
- 运行方式：CLI 长轮询、后台 worker、FastAPI 服务、Windows 桌面托盘进程分别如何取舍。
- 与现有 `InboundEventService`、`AgentRuntime`、`ActionRepository`、`PolicyEngine` 的集成点。

请指出当前模型中需要扩展的字段，例如：

- `raw.context_token`
- `raw.message_id`
- `raw.cursor`
- `raw.media_refs`
- `Platform.WECHAT` 已存在，但 action connector 和 inbound connector 需要区分 `wechat_desktop` 与 `wechat_ilink`
- `ActionKind` 目前只有 `REPLY_DRAFT` 和 `NO_OP`，是否需要扩展为 media reply、typing、followup、proactive draft 等

### 4.3 微信聊天记录自动扫描与保存

用户仍然希望自动扫描微信聊天记录并整理保存。请区分不同来源：

1. iLink Bot 登录后的增量新消息。
2. 当前微信桌面窗口可见消息的 UI/OCR 扫描。
3. 用户手工导出的聊天记录或转发记录。
4. 不建议做的路径：绕过加密、破解本地数据库、规避平台风控等。

请为每类来源设计：

- 可获得的数据范围
- 技术方案
- 工程复杂度
- 风险
- 去重策略
- 时间线排序策略
- 附件/图片/语音处理
- 入库模型
- 验证方法

输出一个推荐的“微信记录 ingestion pipeline”：

```text
source -> raw payload/archive -> normalization -> dedupe -> event store -> media store -> memory extraction -> profile/contact skill update
```

### 4.4 联系人 skill 蒸馏设计

请设计“根据整合后的聊天记录将聊天对象蒸馏成 skill”的工程方案。

重要边界：不要把它设计成对外冒充该联系人。更合理的目标是形成一个本地私有的 `ContactSkill` / `RelationshipSkill`，用于：

- 让 agent 理解该联系人的沟通风格。
- 帮助用户回复该联系人。
- 记住与该联系人的共同经历、偏好、禁忌、关系状态。
- 在生成建议时更自然、更贴合上下文。

请给出结构化 schema，至少包含：

- `contact_id`
- `display_name`
- `platform_ids`
- `relationship_type`
- `communication_style`
- `preferred_topics`
- `avoid_topics`
- `important_events`
- `stable_preferences`
- `emotional_patterns`
- `user_side_preferences`：用户在与此人聊天时自己的偏好和边界
- `reply_strategy`
- `example_patterns`：少量脱敏、高价值的表达模式，不要保存大段原文
- `confidence`
- `evidence_refs`
- `last_updated_at`
- `redaction_policy`

请说明：

- skill 文件是否适合落为 Markdown、JSON、YAML、数据库记录，或多种并存。
- 是否应该参考 Codex `SKILL.md` 形式，还是设计项目内部的 `ContactSkill` 格式。
- 如何从大量聊天记录抽取 skill：分批摘要、聚类、主题建模、LLM 归纳、证据链绑定、人工审核。
- 如何防止隐私泄露、过度拟合、错误记忆、风格漂移。
- 如何在 agent 回复时调用这些 skill：作为检索命中、profile facet、system prompt 片段，还是工具调用结果。

### 4.5 记忆模块设计

请重点设计记忆系统。当前已有：

- `MemoryFact`
- `MemoryProfileSnapshot`
- `MemoryProfileFacet`
- `ChatMemoryExtractionService`
- `MemoryRetrievalService`
- `MemoryLifecycleService`
- 记忆 review/consolidate/profile history CLI

但长期来看还不够。请提出下一版记忆架构，至少包含：

1. 原始事件层：不可变事件、原始 payload、附件引用。
2. 工作记忆：最近 N 轮、短期上下文。
3. 情节记忆：具体事件、约定、冲突、重要对话片段。
4. 语义记忆：稳定事实、偏好、生活背景。
5. 关系记忆：不同联系人之间的关系状态、边界、信任、熟悉度、沟通节奏。
6. 反思记忆：周期性总结，形成“最近状态”和“关系变化”。
7. 程序性/skill 记忆：如何与某人聊天、如何处理某类场景。
8. 向量索引与结构化索引：哪些放 MySQL，哪些放向量库，哪些只放文件。

请回答：

- 记忆何时写入、何时不写入？
- 如何做置信度、重要性、时效性、证据链？
- 如何处理冲突和过时记忆？
- 如何支持用户纠错、删除、冻结某条记忆？
- 如何为“像真人一样自然”服务，而不是机械堆上下文？
- 如何评估记忆质量：命中率、错误记忆率、用户编辑距离、自然度、越界率。
- 是否需要引入 MemGPT/Generative Agents/Reflexion/LongMem/MemoryBank 等研究思想？请只采纳能工程落地的部分。

### 4.6 类真人 chat agent 产品路线

请把目标拆成可执行路线，而不是一次性追求“真人感”。

至少给出 4 个阶段：

- 阶段 0：WeChatBot/iLink 隔离验证与能力边界确认。
- 阶段 1：微信增量消息进入现有 `InboundEvent` + 记忆抽取 + action draft。
- 阶段 2：联系人 skill 蒸馏 + 微信回复建议调试面板/CLI。
- 阶段 3：半自动微信回复：草稿、审批、投递、审计、限频。
- 阶段 4：主动聊天与长期关系管理：触发器、日程、沉默超时、纪念日、安静时段、退让规则。

每个阶段请列出：

- 目标
- 具体代码改动范围
- 新增 CLI/配置项
- 数据库变更
- 测试方案
- 验收标准
- 风险和回滚方案

## 5. 输出格式要求

请输出一份完整调研报告，建议结构如下：

1. 结论摘要：是否建议以微信为主线，是否建议 clone WeChatBot，下一步最小验证是什么。
2. 当前仓库状态校正：指出 `stage_progress_summary.md` 哪些判断已过时。
3. WeChatBot/iLink 能力与限制调研。
4. 方案对比矩阵。
5. 推荐架构：微信接入、消息同步、投递、状态持久化。
6. 微信聊天记录 ingestion pipeline。
7. 联系人 skill 蒸馏方案。
8. 下一版记忆模块设计。
9. 类真人 chat agent 路线图。
10. 安全、隐私、合规和伦理边界。
11. 具体工程任务清单：按 P0/P1/P2 或 Sprint 拆分。
12. 待确认问题。

报告必须包含“明确建议”和“可执行下一步”。不要只列资料。

## 6. 质量标准

你的报告应满足：

- 能指导下一个工程 AI 直接进入实现。
- 对 WeChatBot 的判断必须基于源码/文档/包状态/issue/release，而不是凭感觉。
- 能区分“微信 bot 增量消息”与“历史聊天记录扫描”这两个完全不同的问题。
- 能说明为什么当前 `WeChatDesktopConnector` 仍有价值，但不能承担全部微信主线。
- 对记忆模块给出数据结构、生命周期、更新流程和评估指标。
- 对联系人 skill 给出 schema、生成流程、调用方式、边界和风险控制。
- 对自动发送保持保守：默认草稿/审批，主动发送必须经过策略引擎。
- 对隐私保持本地优先、可删除、可审计、最小外发。

## 7. 最后请给出你的推荐第一步

最后单独给出一个“推荐第一步”，格式如下：

```text
推荐第一步：
目标：
为什么：
需要改动：
验证命令：
通过标准：
不建议现在做：
```

如果你认为应该先 clone WeChatBot，请明确 clone 到哪里、是否纳入 git、是否只是 sandbox、如何避免污染当前仓库。

如果你认为不应该马上 clone，请明确替代动作，例如先读源码、安装 SDK 做最小 POC、或先补本仓库接口。
