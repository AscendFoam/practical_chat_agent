# AI Handoff Prompt

Use this file as the starting prompt/context package for the next AI taking over development in this repository.

Generated on: 2026-05-01
Workspace root: `d:\Codes\Social\chat_scanner`
Primary language with the human user: Chinese

---

## 1. Your role

You are taking over an in-progress engineering prototype called `practical_chat_agent`.

Your job is not to redesign from scratch. Your job is to continue the existing architecture, respect the current worktree, and help the user iteratively ship a practical multi-platform chat/meeting assistant with:

- inbound chat ingestion
- desktop chat scanning
- meeting transcription and live assistance
- long-term memory and persona/profile modeling
- controlled outbound reply delivery

The user prefers direct execution over long planning. They are comfortable with iterative engineering work and usually want code, not just discussion.

---

## 2. Project goal in one paragraph

This project started as a "chat scanner" idea, but it has evolved into a unified social-agent platform. The long-term target is a reusable底层 framework that supports:

- scanning and structuring chat records from WeChat / Feishu / Telegram / similar platforms
- feeding chat and meeting data into LLM analysis
- real-time reply suggestions
- long-term memory and user/persona modeling
- controlled proactive messaging
- Tencent Meeting live transcription and meeting assistance
- future AI-generated social posts / "moments-like" content

The current codebase already has real infrastructure, not just notes.

---

## 3. High-level architecture

Core idea:

- normalize all inbound data into shared event models
- persist structured data in MySQL
- build context from recent events + long-term memory + persona/profile
- run LLM-backed services for suggestion/memory/minutes/assistant tasks
- represent outbound behavior as reviewable actions
- only send through controlled, policy-reviewed delivery connectors

Important architectural centers:

- `src/practical_chat_agent/core/`
- `src/practical_chat_agent/storage/`
- `src/practical_chat_agent/runtime/`
- `src/practical_chat_agent/services/`
- `src/practical_chat_agent/connectors/`
- `src/practical_chat_agent/app/main.py`
- `src/practical_chat_agent/app/container.py`

The container wiring in `app/container.py` is the fastest way to understand the whole system.

---

## 4. Current environment and assumptions

- OS: Windows / PowerShell
- Current date in this handoff: 2026-05-01, timezone `Asia/Shanghai`
- Python env used during recent verification:
  `C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe`
- Typical execution pattern:
  - set `PYTHONPATH=src`
  - run `python -m practical_chat_agent.app.main ...`
- MySQL is used as the primary store
- `.env` exists locally and likely contains real API keys and DB config
- Do not print secrets from `.env`

Important repo reality:

- the git worktree is dirty
- many files are modified or untracked from multiple prior phases
- do not reset or revert unrelated changes
- before editing, inspect `git status --short`

---

## 5. What already exists

### 5.1 Foundation / P0

Already implemented:

- unified enums and Pydantic models for events, memories, meetings, agent outputs, etc.
- MySQL-backed SQLAlchemy models and repositories
- `AppContainer` for dependency wiring
- Typer CLI entrypoint
- minimal in-memory event bus
- `AgentRuntime` as the central turn-processing loop

Main files:

- `src/practical_chat_agent/core/enums.py`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/storage/mysql/models.py`
- `src/practical_chat_agent/storage/mysql/repositories.py`
- `src/practical_chat_agent/storage/repositories/base.py`
- `src/practical_chat_agent/app/container.py`
- `src/practical_chat_agent/app/main.py`

### 5.2 Official inbound connectors / P1 first half

Already implemented:

- Telegram inbound connector
- Feishu inbound connector
- JSON payload replay flow
- mixed payload directory replay

Main files:

- `src/practical_chat_agent/connectors/inbound/telegram_bot.py`
- `src/practical_chat_agent/connectors/inbound/feishu_bot.py`
- `src/practical_chat_agent/services/inbound.py`

Useful CLI:

- `demo-turn`
- `replay-payload-dir`

Example payloads exist under:

- `examples/payloads/`

### 5.3 WeChat desktop scanning / OCR fallback

Already implemented:

- first desktop connector skeleton for WeChat
- window detection
- pywinauto-based UI probing
- screenshot + OCR fallback
- finer OCR parsing for chat bubbles, timestamps, sender, system messages, recalled messages, quoted replies

Main files:

- `src/practical_chat_agent/connectors/desktop/wechat_desktop.py`
- `src/practical_chat_agent/connectors/desktop/pywinauto_support.py`
- `src/practical_chat_agent/connectors/desktop/screen_capture.py`
- `src/practical_chat_agent/services/ocr.py`
- `src/practical_chat_agent/services/desktop.py`

Useful CLI:

- `desktop-scan-preview`

### 5.4 Meeting subsystem / P6 + P7

This is currently the most mature subsystem.

Already implemented:

- Tencent Meeting desktop connector
- Windows loopback audio capture
- microphone capture mode
- chunked WAV capture
- GLM/Zhipu transcription integration
- chunk debug output with RMS / duration / silence / saved path / retry info
- microphone preprocessing improvements
- meeting sessions + segments persistence
- rolling summary / assistant integration
- Markdown minutes export
- minutes version history and diff
- live floating caption window with AI assistance
- GUI actions for minutes generation/history/diff

Main files:

- `src/practical_chat_agent/connectors/meeting/tencent_meeting_desktop.py`
- `src/practical_chat_agent/services/meeting_audio_capture.py`
- `src/practical_chat_agent/services/audio_transcription.py`
- `src/practical_chat_agent/services/meeting.py`
- `src/practical_chat_agent/services/meeting_assistant.py`
- `src/practical_chat_agent/services/meeting_live_loop.py`
- `src/practical_chat_agent/services/meeting_minutes.py`
- `src/practical_chat_agent/services/meeting_minutes_export.py`
- `src/practical_chat_agent/ui/live_caption_window.py`

Useful CLI:

- `meeting-live-preview`
- `meeting-live-window`
- `meeting-session-list`
- `meeting-session-show`
- `meeting-session-tail`
- `meeting-session-replay`
- `meeting-session-export`
- `meeting-session-minutes-history`
- `meeting-session-minutes-show`
- `meeting-session-minutes-diff`

### 5.5 Chat suggestion + memory + profile work

Already implemented before the latest delivery loop:

- chat context assembly
- chat suggestion generation
- chat memory extraction
- memory retrieval
- profile facets
- memory profile snapshots and history
- memory consolidation review/apply flow
- profile history diff
- fixture cleanup tooling for test memories/profiles

Main files:

- `src/practical_chat_agent/services/chat_context.py`
- `src/practical_chat_agent/services/chat_suggestions.py`
- `src/practical_chat_agent/services/chat_memory.py`
- `src/practical_chat_agent/services/memory_retrieval.py`
- `src/practical_chat_agent/services/memory_lifecycle.py`
- `src/practical_chat_agent/services/memory_utils.py`

Useful CLI:

- `memory-list`
- `memory-review`
- `memory-profile-show`
- `memory-profile-history`
- `memory-consolidate`
- `memory-fixture-cleanup`

---

## 6. Latest completed work: controlled outbound delivery loop

This was the most recent active implementation line before this handoff.

Goal:

- turn chat suggestions into a real, reviewable, sendable product flow:
  suggestion -> action plan -> policy review -> human approval -> official send -> audit log

What was added:

- delivery connector abstraction
- Telegram delivery connector using official Bot API
- persistent action records in MySQL
- minimal policy engine
- human approval + send service
- CLI for action review/approval/send

Main additions:

- `src/practical_chat_agent/connectors/delivery/base.py`
- `src/practical_chat_agent/connectors/delivery/telegram_bot.py`
- `src/practical_chat_agent/services/policy.py`
- `src/practical_chat_agent/services/delivery.py`

Core model/storage additions:

- `ActionStatus` enum
- `PolicyDecision`
- `ActionExecutionRecord`
- new table: `action_executions`
- new repository: `ActionRepository`

Runtime integration:

- `AgentRuntime` now persists generated reply drafts as action records
- policy is applied when action records are created
- audit logs are written for action creation

CLI added:

- `action-list`
- `action-show`
- `action-approve`
- `action-send`

Current policy behavior:

- default is conservative
- draft generation does not auto-send
- approval is required by default
- quiet hours add a risk flag
- group chat can be downgraded to draft-only
- frequency limit can block send
- empty messages are blocked
- send re-runs policy before actual delivery

Current delivery behavior:

- only Telegram official delivery is implemented
- send path uses Bot API `sendMessage`
- no remote draft concept exists for Telegram, so drafts stay local in outbox until approval/send

Important config added:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_DELIVERY_ENABLED`
- `TELEGRAM_DELIVERY_TIMEOUT_SECONDS`
- `OUTBOUND_QUIET_HOURS_START`
- `OUTBOUND_QUIET_HOURS_END`
- `OUTBOUND_POLICY_TIMEZONE`
- `OUTBOUND_FREQUENCY_LIMIT_COUNT`
- `OUTBOUND_FREQUENCY_LIMIT_WINDOW_SECONDS`
- `OUTBOUND_GROUP_CHAT_DRAFT_ONLY`

---

## 7. What was actually verified

Verified on 2026-04-30:

1. Python compilation passed for the newly touched delivery/policy/runtime/storage/CLI files.
2. `init-db` succeeded and created `action_executions`.
3. `demo-turn examples/payloads/telegram_bot_dm.json` succeeded.
4. That inbound demo created a real outbox action in MySQL.
5. `action-list --text-only` worked.
6. `action-show <action_id> --text-only` worked.
7. `action-approve <action_id>` worked.

Important runtime observation from `show-config` on 2026-04-30:

- `openai_api_key_present = true`
- `chat_suggestion_model = deepseek-chat`
- `telegram_bot_token_present = false`

Meaning:

- LLM suggestion path was available during the last verification
- Telegram official send was not end-to-end verified because token was not configured at that time

Do not assume send is production-ready until `action-send` is tested with a real safe chat target.

---

## 8. Current CLI map

Important CLI groups already available:

- config/bootstrap:
  - `show-config`
  - `init-db`
  - `create-agent`
- inbound chat replay:
  - `demo-turn`
  - `replay-payload-dir`
- outbound action review/send:
  - `action-list`
  - `action-show`
  - `action-approve`
  - `action-send`
- memory/profile:
  - `memory-list`
  - `memory-review`
  - `memory-profile-show`
  - `memory-profile-history`
  - `memory-consolidate`
  - `memory-fixture-cleanup`
- desktop chat scan:
  - `desktop-scan-preview`
- meeting:
  - `meeting-live-preview`
  - `meeting-live-window`
  - `meeting-session-*`

The CLI file is large. Read `src/practical_chat_agent/app/main.py` in sections rather than all at once.

---

## 9. Key files to read first

Recommended reading order for fast onboarding:

1. `src/practical_chat_agent/app/container.py`
2. `src/practical_chat_agent/runtime/agent_runtime.py`
3. `src/practical_chat_agent/core/models.py`
4. `src/practical_chat_agent/storage/mysql/models.py`
5. `src/practical_chat_agent/storage/mysql/repositories.py`
6. `src/practical_chat_agent/app/main.py`
7. `src/practical_chat_agent/services/chat_context.py`
8. `src/practical_chat_agent/services/chat_suggestions.py`
9. `src/practical_chat_agent/services/chat_memory.py`
10. `src/practical_chat_agent/services/memory_retrieval.py`
11. `src/practical_chat_agent/services/policy.py`
12. `src/practical_chat_agent/services/delivery.py`
13. `src/practical_chat_agent/connectors/delivery/telegram_bot.py`

If focusing on meetings, then also read:

- `src/practical_chat_agent/services/meeting.py`
- `src/practical_chat_agent/ui/live_caption_window.py`

---

## 10. Known gaps and risks

### 10.1 Migrations are still weak

The project still relies on `create_schema(engine)` style bootstrapping.

- there is no real Alembic migration flow yet
- adding tables is okay
- changing existing columns later will become risky

### 10.2 Worktree is not clean

There are many modified/untracked files beyond the latest delivery work.

- do not revert unrelated changes
- assume the user may care about those files
- work incrementally

### 10.3 Telegram official send is only partially verified

- outbox/approval flow is verified
- actual send was not verified because token was absent on 2026-04-30

### 10.4 Policy layer is intentionally minimal

Current `PolicyEngine` covers:

- draft-only agent mode
- approval-required mode
- quiet hours
- frequency limit
- group chat downgrade
- empty message block

Still missing future-grade policy features such as:

- disclosure enforcement
- content classification / risk categories
- per-user cooldown families
- stronger group-chat restrictions
- richer approval reasons and operator UX

### 10.5 Docs may look mojibake in PowerShell

When opened through the terminal, some Chinese Markdown files may render as mojibake because of terminal encoding.

Likely affected:

- `docs/engineering_experiment_plan.md`
- `docs/stage_progress_summary.md`

Do not assume the files are corrupted. Treat this as an output encoding/display issue unless proven otherwise.

---

## 11. Recommended next plan

This is the recommended continuation path as of 2026-05-01.

### Primary recommendation: finish the controlled delivery loop into a true demo product

Suggested order:

1. Safely verify `action-send` with a real Telegram bot token and a non-production test chat.
2. Improve action/operator UX:
   - maybe `action-show --json/--text` polish
   - maybe list filters by platform/channel/date
   - maybe bulk approval/review
3. Add a second official delivery connector, preferably Feishu.
4. Expand policy behavior:
   - clearer quiet-hours semantics
   - safer group-chat behavior
   - explicit deny/block reasons
   - retry-friendly send states
5. Add richer action kinds beyond `reply_draft`.

Why this is recommended:

- it turns the already-existing suggestion + memory + persona stack into a more obviously usable product
- it stays aligned with the user's latest request line
- it creates a safe bridge toward future proactive agent behavior

### Secondary recommendation: keep strengthening the chat intelligence middle layer

Areas still worth improving:

- better memory extraction quality
- more reliable profile facet consolidation
- better context assembly into reply suggestion prompts
- better memory retrieval strategies by intent

### Defer for now unless user explicitly asks

- do not immediately sink more time into the Tencent Meeting branch unless the user reopens it
- that subsystem is already comparatively strong and was intentionally paused

---

## 12. Practical commands for your first 15 minutes

Use these commands first:

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main show-config
```

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main action-list --text-only --limit 10
```

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main demo-turn examples/payloads/telegram_bot_dm.json
```

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main action-list --text-only --limit 10
```

If you need to initialize schema again:

```powershell
$env:PYTHONPATH='src'
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main init-db
```

---

## 13. Behavioral guidance for the next AI

Please work with these assumptions:

- the user prefers concrete implementation over abstract debate
- the user is comfortable with large scope, but still wants safe incremental progress
- default to conservative behavior for outbound messaging
- official-platform paths are preferred over unofficial automation when available
- do not break the existing meeting subsystem while working on chat/delivery
- do not remove existing memory/profile features just because they are imperfect

When you continue:

- inspect the current worktree before editing
- preserve existing patterns in `AppContainer`, repositories, and Typer CLI
- keep the delivery loop human-in-the-loop by default
- favor small verifiable steps

---

## 14. Immediate handoff instruction

If you are the next AI, start by doing this:

1. Read `app/container.py`, `runtime/agent_runtime.py`, and the delivery/policy files.
2. Check `show-config` and confirm whether `TELEGRAM_BOT_TOKEN` is now configured.
3. Inspect the current action records with `action-list`.
4. Decide whether the next step is:
   - end-to-end Telegram send verification
   - Feishu delivery connector
   - policy hardening
   - approval UX improvements
5. Continue without resetting unrelated changes.

That is the intended continuation point.
