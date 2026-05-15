# Task T123: Context Integration

## Task ID

T123

## Goal

将 approved + runtime-ready 的 ContactSkill 和 memory facts 以 compact brief 形式接入现有 `ChatContext` / context assembly 流程，为后续 ReplyPlanner 提供安全、可控、可审计的上下文入口。

## Why now

T120 已提供 file store 与 `is_runtime_ready()` gate。T121 已提供 evidence validator。T122 已提供人工 review/approve/reject/freeze/export CLI。下一步需要让运行时上下文层能消费这些已审阅资产，但仍保持 M2 边界：

- 只读取人工 approved 且 runtime-ready 的 records。
- 只生成 compact brief，不注入完整 skill JSON 或全部 memory。
- 不实现 ReplyPlanner，不自动发送。

## Allowed files

- `src/practical_chat_agent/services/chat_context.py`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/app/container.py`
- `docs/07_handoff.md`

如果现有 context assembly 实际文件名与任务包不同，先阅读 repo 后再判断；若需要修改 `app/main.py`、`services/contact_skill.py` 或其他文件，请停止并向 Captain 说明，不要自行扩大 scope。

## Forbidden scope

- 不注入 candidate records。
- 不注入 rejected / frozen / archived records。
- 不注入 missing-evidence 或 not-human-reviewed records。
- 不把完整 `contact_skill.candidate.json`、完整 store JSON 或全部 memory facts 放进 `ChatContext`。
- 不写 ReplyPlanner，不生成候选回复。
- 不自动发送，不接 realtime platform。
- 不接数据库，不做 migration，不引入向量数据库或 pgvector。
- 不调用 LLM。
- 不读取 `private/chat_history/` 原始聊天记录。
- 不把私密聊天原文、真实联系人名、真实平台 ID、raw prompt 或 raw response 写入 docs/examples/tests/stdout。

## Inputs to read

- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/review/T120_review.md`
- `docs/review/T121_review.md`
- `docs/review/T122_review.md`
- `docs/tasks/M2_memory_skill_store/T120_file_store_models.md`
- `docs/tasks/M2_memory_skill_store/T121_evidence_validator.md`
- `docs/tasks/M2_memory_skill_store/T122_skill_review_cli.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/chat_context.py`
- `src/practical_chat_agent/app/container.py`
- Existing context / memory services as needed for read-only understanding.

## Expected output

Implement a minimal approved-store context integration.

Minimum behavior:

- Add fields or helper model(s) so `ChatContext` can carry:
  - compact contact skill brief
  - compact approved memory facts brief
  - source record ids / evidence refs for auditability
  - status that indicates whether approved store context was present
- Add a service/helper path that can load T120/T122 store files from `private/distilled/**`.
- Filter records using record-level `is_runtime_ready()` and payload status.
- Include only approved + human-reviewed + evidence-valid records.
- Exclude candidate, rejected, frozen, archived, missing-evidence, and not-human-reviewed records.
- Keep brief compact:
  - no raw chat transcript
  - no long quotes
  - no full JSON dump
  - prefer short claims, strategy bullets, boundary reminders, record ids, and evidence refs
- Preserve existing behavior when no store path is configured or no approved records exist.

Integration guidance:

- Prefer a small optional context field over a broad model rewrite.
- Prefer dependency injection via `AppContainer` only if needed by existing construction patterns.
- Do not require private store artifacts for normal app startup.
- T123 may add a safe helper for building a context fixture, but should not add user-facing CLI unless it already exists in allowed files and is necessary for verification.

## Verification

Run compile verification:

```powershell
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/chat_context.py src/practical_chat_agent/core/models.py src/practical_chat_agent/app/container.py
```

Run context assembly verification with private synthetic fixture(s), not committed:

- Approved/runtime-ready fixture:
  - one approved memory record and/or contact skill record that passes `is_runtime_ready()`
  - context contains compact brief and source record ids
- Exclusion fixture:
  - candidate, rejected, frozen, archived, missing-evidence, or not-human-reviewed records
  - context excludes them
- Compatibility fixture:
  - no store path or missing store
  - existing context assembly still works

Use `private/distilled/t123_*` for synthetic fixtures. Do not copy fixture contents into docs.

## Docs to update

- `docs/07_handoff.md`

The handoff update should include:

- What `ChatContext` / context assembly fields or helpers were added.
- How runtime-ready filtering is enforced.
- Which private synthetic fixture or safe sample was used.
- Compile command and context assembly command/script outcomes.
- Any remaining risks or assumptions.

Do not update `docs/04_task_board.md`, `docs/05_decision_log.md`, or `docs/08_risks_and_open_questions.md`; Captain updates those after review.

## Reviewer type

adversarial

Reviewer should specifically check:

- Only approved + runtime-ready records can enter `ChatContext`.
- Candidate/rejected/frozen/archived/missing-evidence/not-human-reviewed records are excluded.
- Brief is compact and does not include raw chat transcript or full JSON dumps.
- Existing flows still work without approved store context.
- No ReplyPlanner, no auto-send, no DB/vector migration, no LLM call.
- No private data leakage to docs/examples/tests/stdout.
