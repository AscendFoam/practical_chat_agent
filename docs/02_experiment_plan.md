# 微信主线 Chat Agent 后续工程化实验计划

更新日期：2026-05-13  
适用仓库：`D:\Codes\Social\practical_chat_agent`

## 1. 文档定位

本文档是 `practical_chat_agent` 下一阶段的工程化实验计划，用于指导后续真实开发流程。它不是重新设计总架构，而是在现有原型、骨架和深度调研结论之上，明确接下来应如何把项目推进为“微信优先、长期记忆、联系人 Skill、受控回复”的 chat agent。

参考优先级如下：

1. `docs/深度调研报告.docx`：最新、最有效，作为本文档的主依据。
2. `docs/next_ai_handoff_prompt.md`：用于校正 2026-05-01 之后的真实代码状态。
3. `docs/stage_progress_summary.md`：作为阶段历史参考，其中部分判断已经过时。
4. `docs/engineering_experiment_plan.md`：作为总体架构和长期方向参考。
5. `docs/wechat_agent_deep_research_prompt.md`：作为调研问题边界与质量标准参考。

一句话结论：

> 下一阶段应以微信为主线，但不要立即把 WeChatBot/iLink SDK vendor 进主仓库。应先做仓库外隔离 POC，验证登录、收消息、回复、媒体、`context_token` 和会话恢复，再以可回滚的方式接入现有 `InboundEvent -> Memory -> Suggestion -> Action -> Policy -> Delivery` 主流程。

## 2. 当前真实基线

### 2.1 已具备能力

当前仓库已经不是早期脚本，真实基础能力包括：

- P0 基础框架已完成：统一核心模型、MySQL 仓储、CLI、`AppContainer`、`AgentRuntime`、事件总线均已存在。
- P1 聊天采集已有基础：Telegram/飞书 payload 入站解析和 replay 链路已存在。
- 微信已有 `WeChatDesktopConnector`：可做 Windows 可见会话扫描、UI accessible text 读取、截图与 OCR 兜底。
- 聊天智能中间层已有实质实现：`ChatContextAssembler`、`ChatSuggestionService`、`ChatMemoryExtractionService`、`MemoryRetrievalService`、`MemoryLifecycleService` 与 profile facets 已存在。
- 受控发送链路已经启动：已有 `DeliveryConnector` 抽象、Telegram 投递、`PolicyEngine`、`ActionDeliveryService`、`ActionRepository`、`action-list/show/approve/send` CLI。
- 会议子系统 P6/P7 已较成熟，但下一阶段不应继续作为主线。

### 2.2 关键缺口

下一阶段要补的不是“从零开始的 agent”，而是以下缺口：

- 没有 WeChat/iLink 级别的稳定增量消息接入。
- 现有微信能力只覆盖桌面可见会话，不能承担实时 bot 主线。
- 没有微信账号、会话、cursor、context token、媒体引用的持久化模型。
- 没有面向联系人的 `ContactSkill` / `RelationshipSkill`。
- 记忆已有基础，但还缺少更清晰的层级、证据链、纠错、冻结、删除和联系人维度。
- 发送链路已有 Telegram，但微信投递尚未接入。
- 缺少 Alembic 式 migration，当前仍主要依赖 `create_schema`。

## 3. 研发原则与边界

### 3.1 默认模式

所有微信相关能力默认采用保守策略：

- 默认只生成草稿和建议，不自动发送。
- 任何真实发送动作必须经过 `PolicyEngine` 与人工审批。
- 主动消息、定时问候、沉默触发等功能必须在半自动闭环稳定后再做。
- 群聊默认更严格，优先草稿模式。

### 3.2 微信接入原则

- iLink/WeChatBot 用于登录后的增量消息与受控回复。
- `WeChatDesktopConnector` 保留为可见会话扫描、历史补录和 OCR 兜底。
- 用户手工导出/转发记录作为第三类历史导入来源。
- 不做绕过加密、破解本地数据库、规避平台风控、hook 或注入。

### 3.3 数据原则

- 原始事件不可变，后续摘要、记忆、Skill 都必须保留证据引用。
- 联系人 Skill 不用于冒充联系人，只用于辅助理解、回复建议和用户自己的上下文管理。
- 本地优先，最小外发。调用外部模型前应支持脱敏或配置关闭。
- 所有对外发送动作必须可审计、可回放、可解释、可回滚到草稿模式。

## 4. 总体路线图

下一阶段按 7 个 Sprint 推进，每个 Sprint 都有独立验收门槛。

```text
Sprint 0: WeChatBot/iLink 仓库外隔离 POC
  -> Sprint 1: 微信 iLink 增量消息接入主流程
  -> Sprint 2: 微信 ingestion、去重、媒体与历史补录统一
  -> Sprint 3: ContactSkill / RelationshipSkill 蒸馏
  -> Sprint 4: 记忆生命周期与联系人画像强化
  -> Sprint 5: 半自动微信回复投递闭环
  -> Sprint 6: 主动触发与长期关系管理
  -> Sprint 7: 工程硬化、迁移、测试、观测
```

建议不要并行大规模展开。每次只推进一个可验收闭环，确保失败时可以退回到上一阶段。

## 5. Sprint 0：WeChatBot/iLink 隔离 POC

### 5.1 目标

在不污染主仓库的前提下，验证 WeChatBot Python SDK 是否能支撑微信主线：

- 扫码登录。
- 收取新消息。
- 回复文本。
- 发送图片或至少验证媒体下载/上传接口。
- 验证 `context_token` 的自动缓存与失效行为。
- 验证会话过期、重登、长轮询异常的表现。

### 5.2 工作范围

不要修改主仓库业务代码。建议在仓库外建立隔离目录，例如：

```text
D:\Codes\Social\wechatbot_sandbox
```

在 sandbox 中通过包管理器安装 SDK，优先使用 Python 包：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install wechatbot-sdk
```

如果 Python SDK 无法满足测试，再评估 Node.js SDK。不要在这个阶段 clone 到主仓库，也不要作为 submodule/vendor 引入。

### 5.3 验证脚本能力

POC 脚本至少需要输出：

- 登录状态。
- 当前账号标识。
- 收到消息的原始字段摘要。
- `message_id`、`from_user_id`、`room_id` 或等价会话标识。
- `context_token` 是否存在。
- 文本回复结果。
- 媒体消息的元数据。
- 会话过期或发送失败时的错误码。

### 5.4 验收标准

满足以下条件才进入 Sprint 1：

- 能稳定扫码登录，并在重启后复用凭据或清楚知道凭据恢复机制。
- 能收到至少 10 条新消息，文本内容、时间、发送者、会话 ID 可解析。
- 能对入站消息执行 reply，并确认微信端实际收到。
- 能证明主动 `send(user_id, text)` 是否依赖已有上下文 token。
- 至少完成一次图片或媒体能力验证，哪怕只做到接收和元数据归档。
- 明确记录 SDK 版本、安装方式、已知 issue 和失败场景。

### 5.5 回滚与停止条件

出现以下情况应暂停微信 iLink 主线，暂时回退到桌面扫描与官方平台：

- 无法稳定扫码登录。
- SDK 与当前 Python 3.11 环境严重不兼容。
- 长轮询收消息存在不可接受的漏消息。
- 发送能力对个人微信场景不可用。
- 账号或平台风险高于调研预期。

### 5.6 产出物

- `docs/wechat_ilink_poc_notes.md`：记录 SDK 版本、验证过程、能力矩阵、失败点、是否进入 Sprint 1。
- 不要求提交 sandbox 源码到主仓库；如需要保留，可只提交脱敏后的实验记录。

## 6. Sprint 1：微信 iLink 增量消息接入主流程

### 6.1 目标

把 WeChat/iLink 登录后的新消息接入现有主流程：

```text
WeChat iLink message -> InboundEvent -> EventRepository
  -> ChatMemoryExtractionService
  -> ChatContextAssembler
  -> ChatSuggestionService
  -> ActionExecutionRecord
```

### 6.2 代码改动范围

建议新增：

```text
src/practical_chat_agent/connectors/inbound/wechat_ilink.py
src/practical_chat_agent/services/wechat_ilink_session.py
src/practical_chat_agent/services/wechat_ingestion.py
```

建议修改：

```text
src/practical_chat_agent/app/config.py
src/practical_chat_agent/app/container.py
src/practical_chat_agent/app/main.py
src/practical_chat_agent/core/enums.py
src/practical_chat_agent/core/models.py
src/practical_chat_agent/storage/mysql/models.py
src/practical_chat_agent/storage/mysql/repositories.py
src/practical_chat_agent/storage/repositories/base.py
```

### 6.3 模型与枚举扩展

短期可继续使用 `Platform.WECHAT`，但必须通过 `event.raw["connector_name"]` 区分来源：

- `wechat_ilink`
- `wechat_desktop`
- `wechat_import`

中期可以考虑新增字段 `connector_name` 到事件表；在没有 migration 前，不建议直接破坏现有 `events` 结构。优先把扩展字段放在 `raw`。

建议扩展 `ActionKind`：

```text
REPLY_DRAFT      当前已有，继续保留
SEND_TEXT        后续真实发送文本
SEND_MEDIA       后续媒体发送
TYPING           可选，输入状态
FOLLOWUP_DRAFT   主动触发草稿
NO_OP            当前已有，继续保留
```

如果暂时不改 `ActionKind`，Sprint 1 可以只用 `REPLY_DRAFT`，真实发送留到 Sprint 5。

### 6.4 配置项

建议新增配置：

```text
WECHAT_ILINK_ENABLED=false
WECHAT_ILINK_CREDENTIAL_DIR=.cache/wechat_ilink
WECHAT_ILINK_BASE_URL=https://ilinkai.weixin.qq.com
WECHAT_ILINK_POLL_TIMEOUT_SECONDS=35
WECHAT_ILINK_AUTO_RELOGIN=false
WECHAT_ILINK_ACCOUNT_ID=default_wechat
WECHAT_ILINK_SAVE_RAW_PAYLOAD=true
```

### 6.5 数据库变更

Sprint 1 最小新增表：

```text
platform_accounts
  account_id
  platform
  connector_name
  display_name
  credential_ref
  status
  raw_payload
  created_at
  updated_at

platform_sessions
  session_id
  account_id
  platform
  connector_name
  status
  update_cursor
  last_polled_at
  expires_at
  raw_payload
  created_at
  updated_at

conversation_context_tokens
  token_id
  account_id
  platform
  connector_name
  channel_id
  actor_id
  context_token
  token_status
  last_seen_event_id
  last_seen_at
  raw_payload
  created_at
  updated_at
```

注意：当前项目缺正式 migration。此 Sprint 可以继续使用 `create_schema` 新建表，但如果涉及现有表结构变更，应先引入 Alembic 或写清楚手工迁移脚本。

### 6.6 CLI

建议新增：

```text
wechat-ilink-check
wechat-ilink-login
wechat-ilink-listen --agent-id <agent_id> --limit <n>
wechat-ilink-session-show
wechat-ilink-session-reset
```

其中 `wechat-ilink-listen` 初期可以只跑有限条消息，避免无限后台进程难以调试。

### 6.7 测试方案

单元测试：

- iLink raw payload -> `InboundEvent` 映射。
- `context_token` 提取与入库。
- 缺少文本、图片消息、系统消息等边界。
- session cursor 更新逻辑。

集成测试：

- 用脱敏 fixture 模拟 5 到 10 条微信消息，验证 replay 能入库。
- 真实账号手工测试时只发测试内容，不使用敏感联系人。

### 6.8 验收标准

- `wechat-ilink-listen --limit 10` 能将真实新消息写入 `events`。
- 每条事件的 `raw` 包含原始消息摘要、SDK message id、`context_token` 或明确的缺失原因。
- 现有 `AgentRuntime` 能对微信事件生成建议和 action 草稿。
- `memory-review` 能看到微信消息抽取出的候选记忆。
- 关闭 `WECHAT_ILINK_ENABLED` 后不影响 Telegram/飞书/会议功能。

## 7. Sprint 2：微信 Ingestion、去重、媒体与历史补录统一

### 7.1 目标

把三类微信来源统一到同一条 ingestion pipeline：

```text
iLink 增量消息
微信桌面可见会话扫描
用户手工导出/转发记录
  -> raw payload/archive
  -> normalization
  -> dedupe
  -> event store
  -> media store
  -> memory extraction
  -> contact skill update
```

### 7.2 代码改动范围

建议新增：

```text
src/practical_chat_agent/services/ingestion.py
src/practical_chat_agent/services/dedupe.py
src/practical_chat_agent/services/media_assets.py
src/practical_chat_agent/services/wechat_import.py
```

建议改造：

```text
src/practical_chat_agent/services/desktop.py
src/practical_chat_agent/connectors/desktop/wechat_desktop.py
src/practical_chat_agent/services/inbound.py
```

### 7.3 数据库变更

建议新增：

```text
raw_message_payloads
  raw_id
  platform
  connector_name
  account_id
  channel_id
  provider_message_id
  event_id
  source_kind
  payload_hash
  raw_payload
  received_at
  created_at

media_assets
  media_id
  platform
  connector_name
  account_id
  event_id
  media_type
  provider_media_id
  local_path
  remote_ref
  encryption_metadata
  download_status
  raw_payload
  created_at
  updated_at

ingest_runs
  ingest_run_id
  source_kind
  platform
  connector_name
  account_id
  status
  started_at
  finished_at
  stats_payload
  error_message
```

### 7.4 去重策略

按来源分层：

- iLink：优先使用 provider message id；缺失时使用 `platform + account_id + channel_id + actor_id + occurred_at + text_hash`。
- Desktop OCR：使用 `channel_hint + display_time + bubble_side + normalized_text_hash + screenshot_region_hash`。
- 手工导入：使用导出文件消息 id；没有 id 时用时间戳和文本 hash。

去重结果不要直接丢弃，应在 `raw_message_payloads` 或 `ingest_runs` 中记录 skipped 统计。

### 7.5 媒体策略

Sprint 2 不要求完整支持所有媒体发送。优先完成：

- 媒体元数据入库。
- 图片/语音/文件可延迟下载。
- 本地保存路径可配置。
- 下载失败可重试。
- 媒体与事件建立引用关系。

### 7.6 CLI

建议新增：

```text
wechat-desktop-ingest --agent-id <agent_id> --conversation-hint <hint>
wechat-import-file --agent-id <agent_id> --path <file>
ingest-run-list
ingest-run-show <ingest_run_id>
media-asset-list --event-id <event_id>
media-asset-fetch <media_id>
```

### 7.7 验收标准

- 同一条微信消息从 iLink 与桌面扫描重复进入时，最终只生成一条 canonical event。
- 桌面扫描仍可独立运行，且其结果能进入统一 `events`。
- iLink 图片消息至少能保存媒体元数据。
- ingestion 过程有可读统计：新增、跳过、失败、媒体数量。
- 失败不会污染主流程，可以重复运行。

## 8. Sprint 3：联系人 Skill 蒸馏

### 8.1 目标

实现本地私有的 `ContactSkill` / `RelationshipSkill`，让系统能理解某个联系人：

- 这个人常用什么沟通风格。
- 与用户是什么关系。
- 重要共同经历是什么。
- 哪些话题适合聊，哪些不适合。
- 用户希望如何与此人沟通。

强调：ContactSkill 不是为了冒充该联系人，而是为了辅助用户理解和回复。

### 8.2 建议数据模型

新增 Pydantic 模型：

```text
ContactSkill
  skill_id
  contact_id
  display_name
  platform_ids
  relationship_type
  communication_style
  preferred_topics
  avoid_topics
  important_events
  stable_preferences
  emotional_patterns
  user_side_preferences
  reply_strategy
  example_patterns
  confidence
  evidence_refs
  redaction_policy
  status
  created_at
  updated_at
```

新增数据库表：

```text
contacts
  contact_id
  display_name
  platform
  platform_user_id
  aliases
  metadata_payload
  created_at
  updated_at

contact_skills
  skill_id
  contact_id
  agent_id
  backend
  model
  status
  confidence
  skill_payload
  evidence_event_ids
  evidence_memory_ids
  redaction_policy
  created_at
  updated_at
```

`example_patterns` 只保存少量脱敏、高价值表达模式，不保存大段原文。

### 8.3 代码改动范围

建议新增：

```text
src/practical_chat_agent/services/contact_skill.py
src/practical_chat_agent/services/contact_resolution.py
src/practical_chat_agent/exporters/contact_skill_markdown.py
```

建议修改：

```text
src/practical_chat_agent/core/models.py
src/practical_chat_agent/storage/mysql/models.py
src/practical_chat_agent/storage/mysql/repositories.py
src/practical_chat_agent/services/chat_context.py
src/practical_chat_agent/services/chat_suggestions.py
src/practical_chat_agent/app/container.py
src/practical_chat_agent/app/main.py
```

### 8.4 生成流程

第一版不要直接把所有原始聊天塞给模型。建议：

1. 按联系人和时间窗口加载事件。
2. 先用规则和已有 `MemoryFact` 生成候选事实。
3. 按主题聚合：工作、日常、情绪、计划、偏好、冲突、共同经历。
4. 对每个主题生成短摘要和证据引用。
5. 合成 ContactSkill。
6. 做隐私清洗和置信度标注。
7. 进入 review 状态，人工确认后再用于回复建议。

### 8.5 CLI

建议新增：

```text
contact-list
contact-show <contact_id>
contact-skill-generate --contact-id <contact_id> --agent-id <agent_id>
contact-skill-show <skill_id>
contact-skill-review <skill_id>
contact-skill-approve <skill_id>
contact-skill-export <skill_id> --format markdown
```

### 8.6 与建议链路集成

`ChatContextAssembler` 应根据当前 `event.actor_id` 和 `channel_id` 加载 approved ContactSkill，并传入 `ChatContext`。

`ChatSuggestionService` 的 prompt 中只注入压缩后的 skill 摘要，例如：

- 对方沟通风格。
- 用户对这个联系人偏好的回复策略。
- 需要避免的话题。
- 最近相关共同事件。

不要把完整 skill 和大量证据一次性塞入 prompt。

### 8.7 验收标准

- 对一个测试联系人生成 ContactSkill，字段完整且证据引用可追溯。
- 生成结果不包含电话、身份证、住址等敏感原文。
- `contact-skill-show` 可读，`contact-skill-export` 可生成 Markdown 审阅版。
- 回复建议能体现 skill 信息，但不会机械复述。
- 禁用 ContactSkill 后，建议链路仍可正常运行。

## 9. Sprint 4：记忆生命周期与联系人画像强化

### 9.1 目标

在当前 `MemoryFact`、`MemoryProfileSnapshot`、`MemoryProfileFacet` 基础上，补齐长期运行需要的记忆治理能力：

- 分层记忆。
- 证据链。
- 冲突处理。
- 用户纠错。
- 删除与冻结。
- 联系人维度。
- 反思与周期性总结。

### 9.2 记忆分层

建议使用以下层级，不必一次性新增所有表，但代码和命名应按这个方向演进：

- 原始事件层：`events`、`raw_message_payloads`，不可变。
- 工作记忆：最近 N 轮，由 `ChatContextAssembler` 管理。
- 情节记忆：重要事件、约定、冲突、具体对话摘要。
- 语义记忆：稳定事实、长期偏好、身份背景。
- 关系记忆：联系人关系、熟悉度、边界、沟通节奏。
- 反思记忆：每日/每周总结近期状态和关系变化。
- 程序性记忆：如何与某人或某类场景互动，和 ContactSkill 强相关。

### 9.3 数据字段补强

当前 `MemoryFact` 已有 `salience`、`confidence`、`evidence_refs`。建议新增或通过 `raw` 过渡承载：

```text
status: candidate | approved | rejected | frozen | archived
valid_from
valid_until
supersedes_memory_id
conflict_group_id
source_kind
privacy_level
redaction_policy
last_verified_at
```

如果不想立即改表，可先增加 `memory_metadata` JSON 字段，后续 migration 稳定后拆列。

### 9.4 记忆写入规则

不应把每句闲聊写入长期记忆。写入条件：

- 明确事实：身份、偏好、计划、约定、重要事件。
- 重复出现：多次被提到的稳定偏好。
- 高情绪强度：需要后续照顾语气和边界。
- 与联系人 Skill 或关系状态有关。
- 用户显式要求“记住”。

不写入条件：

- 无意义寒暄。
- 单次弱信号。
- 高隐私且无必要保存。
- 模型不确定且没有证据。

### 9.5 CLI

建议补充：

```text
memory-freeze <memory_id>
memory-archive <memory_id>
memory-correct <memory_id> --fact <text>
memory-evidence-show <memory_id>
memory-conflict-list
memory-reflect --agent-id <agent_id> --user-id <user_id>
```

### 9.6 验收标准

- 用户可以冻结或归档错误记忆，后续建议不再使用。
- 冲突记忆能被标记，不会同时高置信度注入 prompt。
- 反思记忆能按时间窗口生成，且带证据引用。
- ContactSkill 生成优先使用 approved memory 和 approved event，不直接依赖不可信原文。

## 10. Sprint 5：半自动微信回复投递闭环

### 10.1 目标

打通微信端：

```text
微信入站消息 -> 建议草稿 -> ActionExecutionRecord
  -> PolicyEngine
  -> 人工审批
  -> WeChatIlinkDeliveryConnector
  -> 审计日志
```

### 10.2 代码改动范围

建议新增：

```text
src/practical_chat_agent/connectors/delivery/wechat_ilink.py
src/practical_chat_agent/services/wechat_delivery.py
```

建议修改：

```text
src/practical_chat_agent/services/delivery.py
src/practical_chat_agent/services/policy.py
src/practical_chat_agent/app/container.py
src/practical_chat_agent/app/main.py
src/practical_chat_agent/core/enums.py
src/practical_chat_agent/core/models.py
```

### 10.3 投递策略

微信发送第一版只支持文本：

- `send_text(action)`：从 action 中读取 `channel_id`、`actor_id`、`message_text`。
- 优先使用与原始事件绑定的 `context_token` 执行 reply。
- 如果是主动发送，必须查询 `conversation_context_tokens` 中未过期 token。
- token 不存在或失效时，action 标记为 `FAILED` 或 `DRAFT_ONLY`，提示用户手动发送或重新登录。

媒体发送延后到文本闭环稳定之后。

### 10.4 PolicyEngine 扩展

微信平台需要更严格的规则：

- 默认必须人工审批。
- 群聊默认草稿。
- 安静时段只生成草稿。
- 连续未回复时自动降频。
- 高频发送直接阻断。
- `do_not_do` 与联系人 `avoid_topics` 进入风险检查。
- 不允许在公开或群聊场景伪装成真人。

### 10.5 CLI

现有 `action-list/show/approve/send` 应继续复用，并增加过滤能力：

```text
action-list --platform wechat --status pending_approval
action-show <action_id> --include-policy --include-context
action-send <action_id>
```

可选增加：

```text
wechat-action-send <action_id>
```

但优先复用现有 action 命令，避免重复 UX。

### 10.6 验收标准

- 微信入站消息能生成 `PENDING_APPROVAL` action。
- 审批前不会真实发送。
- 审批后能实际发送到对应微信会话。
- 发送结果写入 `delivery_response` 和 `audit_logs`。
- token 失效时 action 失败状态清晰，不会误判为已发送。
- 关闭微信 delivery 后，仍保留本地草稿。

## 11. Sprint 6：主动触发与长期关系管理

### 11.1 前置条件

必须完成 Sprint 5 的半自动闭环后再做。不要在微信发送未稳定前做主动聊天。

### 11.2 目标

让 agent 能提出主动交流建议，但仍默认进入审批：

- 定时问候。
- 纪念日。
- 长时间未互动。
- 用户提过的重要事件临近。
- 会议或任务后的跟进。
- 联系人关系状态变化后的轻量提醒。

### 11.3 数据库变更

建议新增：

```text
trigger_rules
  trigger_id
  agent_id
  contact_id
  trigger_type
  enabled
  schedule_payload
  policy_payload
  created_at
  updated_at

scheduled_actions
  scheduled_action_id
  trigger_id
  agent_id
  contact_id
  platform
  channel_id
  status
  due_at
  action_id
  raw_payload
  created_at
  updated_at
```

### 11.4 CLI

建议新增：

```text
trigger-create
trigger-list
trigger-disable <trigger_id>
trigger-run-once <trigger_id>
scheduled-action-list
scheduled-action-show <scheduled_action_id>
```

### 11.5 验收标准

- 能创建一个测试触发器并生成 follow-up 草稿。
- 所有主动消息都进入 `PENDING_APPROVAL` 或 `DRAFT_ONLY`。
- 连续未回复触发退让规则。
- 安静时段不触发真实发送。
- 用户可以一键禁用触发器。

## 12. Sprint 7：工程硬化

### 12.1 Migration

当前 `create_schema` 对新增表尚可接受，但继续扩展会变危险。建议在 Sprint 1 或 Sprint 2 后尽快引入 Alembic：

- 初始化 migration 目录。
- 为当前 schema 生成 baseline。
- 后续新增表和字段通过 migration 管理。
- `init-db` 只负责创建数据库和运行 migration，不再直接承担全部 schema 变更。

### 12.2 自动化测试

建议建立 `tests/`，优先覆盖：

- 微信 raw payload 解析。
- ingestion dedupe。
- contact skill schema 验证。
- memory freeze/correct 不再进入 context。
- policy quiet hours、频率限制、群聊草稿。
- delivery token 缺失失败路径。
- repository roundtrip。

### 12.3 可观测性

新增结构化日志或 CLI 状态视图：

```text
system-status
connector-status
wechat-status
policy-status
```

状态视图至少展示：

- iLink 是否启用。
- 最近一次 poll 时间。
- 最近一次错误。
- 当前 session 状态。
- 待审批 action 数量。
- 最近发送失败数。
- 记忆候选数量。

### 12.4 验收标准

- 新增功能有最小测试。
- 关键 CLI 可输出 text 和 JSON 两种形式。
- 真实发送失败可定位原因。
- 数据库变更可重放。
- 关闭微信相关配置后，项目仍能运行既有 Telegram/飞书/会议流程。

## 13. 推荐实现顺序清单

### 第一批：必须先做

1. 完成 WeChatBot/iLink sandbox POC。
2. 写 `docs/wechat_ilink_poc_notes.md`，给出进入或不进入 Sprint 1 的决策。
3. 新增 `WeChatIlinkInboundConnector` 的 fixture 解析版，先不接真实 SDK。
4. 新增 session/token 的数据模型和仓储。
5. 打通 `wechat-ilink-listen --limit n` 的真实入库。

### 第二批：形成微信数据闭环

1. 统一 iLink、desktop、import 三类来源的 ingestion。
2. 建立 raw payload 与 media metadata 归档。
3. 补去重与 ingest run 统计。
4. 将微信事件接入现有 memory 和 suggestion。

### 第三批：形成“懂联系人”的能力

1. 新增 ContactSkill 模型。
2. 做 `contact-skill-generate/show/review/approve`。
3. 将 approved ContactSkill 注入 `ChatContext`。
4. 建立 skill 的证据链和脱敏导出。

### 第四批：形成半自动行动闭环

1. 新增 `WeChatIlinkDeliveryConnector`。
2. 接入 `ActionDeliveryService`。
3. 扩展微信平台策略。
4. 验证审批后真实发送。
5. 失败时回落草稿。

### 第五批：再做主动关系管理

1. 做触发器。
2. 做 scheduled actions。
3. 做关系反思与联系人节奏管理。
4. 仍保持审批优先。

## 14. 不建议现在做的事

- 不要立即把 `corespeed-io/wechatbot` 作为 submodule/vendor 放进主仓库。
- 不要在微信发送闭环未稳定前做主动自动发送。
- 不要继续深挖会议侧，除非用户重新指定会议为主线。
- 不要优先做动态/朋友圈内容生成，除非 persona、memory、policy 已经稳定。
- 不要做破解微信本地数据库、绕过加密或规避风控的历史导入。
- 不要让 ContactSkill 被用于对外冒充真实联系人。

## 15. 阶段门禁

### Gate 0：是否接入 iLink

进入条件：

- sandbox POC 可登录、收消息、reply。
- context token 行为清楚。
- 风险可接受。

失败处理：

- 暂停 iLink 主线。
- 强化桌面扫描和 Telegram/飞书闭环。

### Gate 1：是否开启主仓库微信监听

进入条件：

- fixture 解析测试通过。
- session/token 表可写可读。
- `wechat-ilink-listen --limit n` 不影响其他流程。

失败处理：

- 保留 connector 代码但默认 disabled。

### Gate 2：是否启用 ContactSkill 注入

进入条件：

- Skill 有证据链、置信度、脱敏策略。
- 用户可 review/approve。
- prompt 注入后建议质量提升，且不机械复述。

失败处理：

- 只保留 skill 查看，不进入建议链路。

### Gate 3：是否开启微信真实发送

进入条件：

- 文本发送端到端成功。
- 审批与审计完整。
- token 失效能清晰失败。
- policy 在群聊、安静时段、高频场景下能阻断或降级。

失败处理：

- 全部退回 `DRAFT_ONLY`。

### Gate 4：是否开启主动触发

进入条件：

- 半自动发送稳定。
- 触发器产生的 action 默认审批。
- 退让、限频和禁用机制可用。

失败处理：

- 禁用 trigger，只保留被动建议。

## 16. 评估指标

### 接入侧

- 登录成功率。
- 长轮询连续运行时长。
- 新消息漏收率。
- 重复消息率。
- token 失效率。
- 媒体元数据完整率。

### 记忆侧

- 有效记忆写入率。
- 错误记忆率。
- 记忆证据可追溯率。
- 用户纠错次数。
- 冻结/删除后误用次数。

### ContactSkill 侧

- 字段完整率。
- 人工审核通过率。
- 脱敏违规次数。
- 建议引用 skill 的自然度评分。
- 建议二次编辑距离。

### 发送侧

- 草稿生成到审批通过率。
- 审批后发送成功率。
- policy 阻断准确率。
- 误发送次数，目标为 0。
- 群聊草稿降级率。

## 17. 推荐第一步

```text
推荐第一步：
目标：在仓库外完成 WeChatBot Python SDK 的最小 POC。
为什么：深度调研报告明确建议微信主线可行，但 SDK 不宜立即进入主仓库；必须先验证登录、收发、媒体和 context_token 行为。
需要改动：主仓库不改业务代码；只新增或后续补充一份 docs/wechat_ilink_poc_notes.md 记录实验结论。
验证命令：在 sandbox 中运行官方 QuickStart 或最小脚本，扫码登录，向测试联系人发送消息，控制台打印收到消息并执行 echo reply。
通过标准：能稳定登录、收到消息、回复文本、记录 context_token 行为，并完成一次媒体能力验证或明确媒体限制。
不建议现在做：不 vendor WeChatBot，不做自动发送，不做破解历史库，不做朋友圈/动态内容。
```

## 18. 最终交付定义

当上述 Sprint 完成后，项目应达到下一阶段可用形态：

- 微信新消息能稳定进入统一事件库。
- 桌面扫描能补历史可见上下文。
- 联系人 Skill 可生成、审阅、导出和注入建议链路。
- 长期记忆可审计、可纠错、可冻结、可删除。
- 微信回复能从建议草稿走到人工审批和真实发送。
- 所有真实发送都有 policy、审计和回滚路径。
- 主动触发只作为审批草稿出现，不无人值守骚扰联系人。

这时项目才算从“多功能原型”进入“微信主线 chat agent 工程实验闭环”。
