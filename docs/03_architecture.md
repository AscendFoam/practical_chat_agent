# Architecture

更新日期：2026-05-13

## 1. 当前基础

仓库已有的核心结构：

```text
src/practical_chat_agent/
  app/                 Typer CLI, Settings, AppContainer
  core/                enums, Pydantic models, event bus
  storage/             repository interfaces and MySQL implementation
  connectors/
    inbound/           Telegram, Feishu payload ingestion
    desktop/           WeChat desktop scan and OCR fallback
    delivery/          Delivery abstraction and Telegram delivery
    meeting/           Tencent Meeting connector
  services/            chat context, suggestions, memory, policy, delivery, meetings
  runtime/             AgentRuntime turn loop
  ui/                  meeting live caption window
```

Important existing flow:

```text
Inbound payload or desktop scan
  -> InboundEvent
  -> AgentRuntime
  -> EventRepository
  -> MemoryRetrievalService
  -> ChatContextAssembler
  -> ChatMemoryExtractionService
  -> ChatSuggestionService
  -> ActionExecutionRecord
  -> PolicyEngine
  -> ActionDeliveryService
```

## 2. Target WeChat-first Flow

```text
WeChat iLink new message
  -> WeChatIlinkInboundConnector
  -> WeChatIngestionService
  -> raw_message_payloads
  -> dedupe
  -> events
  -> memory extraction
  -> contact skill update candidates
  -> reply suggestion
  -> action record
  -> policy
  -> approval
  -> WeChatIlinkDeliveryConnector
```

T00 POC 已确认的最低事实：

- SDK 包名：`wechatbot-sdk`
- 已验证版本：`0.2.1`
- Python import：`from wechatbot import WeChatBot`
- 登录入口：`login()` 可触发二维码 URL 回调

这些事实只证明 SDK 可以启动到扫码阶段，不代表已完成微信主仓库 connector 设计。

Desktop and import sources should eventually join the same ingestion layer:

```text
wechat_ilink | wechat_desktop | wechat_import
  -> normalization
  -> dedupe
  -> canonical event
```

## 3. Connector Boundaries

- `wechat_ilink`: real-time or near-real-time message source after SDK POC passes.
- `wechat_desktop`: visible-session scan, OCR fallback, and historical補录.
- `wechat_import`: user-provided exports or manually forwarded history.

During Sprint 1, `Platform.WECHAT` can remain the platform enum. The connector source should be carried in `event.raw["connector_name"]` until a schema migration adds a first-class column.

## 4. Persistence Boundaries

Existing persistence should be reused:

- `events`: canonical normalized event.
- `memories`: long-term facts and profile facets.
- `action_executions`: reviewable outbound action records.
- `audit_logs`: important state changes and delivery attempts.

Planned WeChat-specific additions:

- `platform_accounts`
- `platform_sessions`
- `conversation_context_tokens`
- `raw_message_payloads`
- `media_assets`
- `ingest_runs`
- `contacts`
- `contact_skills`
- `trigger_rules`
- `scheduled_actions`

Until Alembic exists, additive tables are safer than changing existing columns.

## 5. Safety Architecture

Default safety posture:

- inbound processing can run unattended only after connector stability is proven;
- generated replies are local action records;
- real delivery requires `PolicyEngine` and approval;
- group chats default to draft-only;
- active/proactive triggers are forbidden before Sprint 6;
- ContactSkill is private context, not a persona impersonation mechanism.

## 6. Configuration Principles

All WeChat iLink features must be disabled by default:

```text
WECHAT_ILINK_ENABLED=false
WECHAT_ILINK_CREDENTIAL_DIR=.cache/wechat_ilink
WECHAT_ILINK_AUTO_RELOGIN=false
WECHAT_ILINK_SAVE_RAW_PAYLOAD=true
```

Workers should avoid importing optional SDK packages at module import time. Optional SDK loading should happen behind connector initialization or command execution so the existing CLI remains usable without the SDK.

T01 起还需要确认 `wechatbot-sdk 0.2.1` 对 Python 3.11/3.12 的兼容边界。主仓库当前仍应避免把该 SDK 作为强依赖加入 `pyproject.toml`。
