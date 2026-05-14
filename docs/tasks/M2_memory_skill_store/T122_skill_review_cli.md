# Task T122: Skill Review CLI

## Task ID

T122

## Goal

实现离线 contact-skill / memory store 的人工 review CLI，支持安全查看、approve、reject、freeze/archive 和导出 review artifact。Approve 必须受 T121 evidence validation gate 约束。

## Why now

T120 已提供 memory/skill file store、review metadata 和 human-review-first gate。T121 已提供 read-only evidence validator，能报告 missing refs、状态阻塞和 runtime readiness。下一步需要把这些能力连接成人工审阅工作流：

- 人工 reviewer 可以安全查看 candidate 摘要。
- reviewer 可以记录 approve / reject / freeze / archive 决策。
- approve 不能绕过 evidence validation。
- 审阅结果仍只保存在 `private/distilled/**`，不进入 runtime。

## Allowed files

- `src/practical_chat_agent/app/main.py`
- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/exporters/contact_skill_markdown.py`
- `docs/07_handoff.md`

如果发现必须改 `core.models.py` 才能正确表达 review decision，请停止并向 Captain 说明，不要自行扩大 scope。

## Forbidden scope

- 不自动 approve。
- 不批量默认 approve。
- 不绕过 T121 evidence validation report。
- 不做 runtime integration，不改 `ChatContextAssembler`，不把 approved records 注入 prompt。
- 不接数据库，不做 migration，不引入向量数据库或 pgvector。
- 不调用 LLM。
- 不自动发送或接实时平台。
- 不读取 `private/chat_history/` 原始聊天记录。
- 不把私密聊天原文、真实联系人名、真实文件名、真实平台 ID、raw prompt 或 raw response 写入 docs/examples/tests/stdout。

## Inputs to read

- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/review/T120_review.md`
- `docs/review/T121_review.md`
- `docs/tasks/M2_memory_skill_store/T120_file_store_models.md`
- `docs/tasks/M2_memory_skill_store/T121_evidence_validator.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/services/evidence_validation.py`
- `src/practical_chat_agent/exporters/contact_skill_markdown.py`

## Expected output

Implement a small CLI workflow for private file-store review.

Minimum CLI behavior:

- Add Typer command(s) in `src/practical_chat_agent/app/main.py`.
- Suggested command group/name: `chatlog-review-store`.
- Input path must be confined to `private/distilled/**`.
- Support listing records with safe summaries:
  - record id
  - artifact type
  - status
  - review state
  - evidence validation status
  - runtime-ready / approval-ready summary
  - safe private relative path
- Support record-level decisions:
  - `approve`
  - `reject`
  - `freeze`
  - `archive`
- Support notes/reviewer metadata:
  - reviewer id/name
  - decision timestamp
  - notes
  - evidence validation status used for the decision
- Support export:
  - Markdown review/export artifact under `private/distilled/**` by default.
  - JSON store write-back under `private/distilled/**`.

Approval gate requirements:

- Approve must require a T121 validation report unless an explicit safe revalidation command path is implemented in T122.
- Approve must fail if the validation report status is not `passed`.
- Approve must fail if the target record has any missing refs.
- Approve must fail for `rejected`, `frozen`, or `archived` records unless the CLI first records an explicit human decision to reopen; reopening is optional and not required for T122.
- Approve must set `status="approved"` on the candidate payload only after the gate passes.
- Approve must update `review_metadata.reviewed_by_human=True`, `last_decision`, `review_state`, reviewer fields, and append to decision history.

Reject/freeze/archive requirements:

- These actions do not require evidence validation passed.
- They must update payload status and review metadata.
- They must never make a record runtime-ready.

## Verification

Run compile verification:

```powershell
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/app/main.py src/practical_chat_agent/services/contact_skill.py src/practical_chat_agent/exporters/contact_skill_markdown.py
```

Run CLI verification with private synthetic fixture(s), not committed:

- Good approval case:
  - T120 store record has valid refs.
  - T121 evidence validation report is `passed`.
  - CLI approve updates status/review metadata/history.
- Missing-ref case:
  - T121 report is `failed` or target record has missing refs.
  - CLI approve is rejected and does not update the record to approved.
- Reject/freeze case:
  - CLI records decision and keeps record non-runtime-ready.
- Export case:
  - CLI writes Markdown/JSON only under `private/distilled/**`.

Use `private/distilled/t122_*` for any synthetic fixtures. Do not copy fixture contents into docs.

## Docs to update

- `docs/07_handoff.md`

The handoff update should include:

- Commands added.
- Which private synthetic fixture or safe sample was used.
- Compile command and CLI command outcomes.
- Whether approve was correctly blocked on missing refs.
- Remaining risks or assumptions.

Do not update `docs/04_task_board.md`, `docs/05_decision_log.md`, or `docs/08_risks_and_open_questions.md`; Captain updates those after review.

## Reviewer type

adversarial

Reviewer should specifically check:

- No auto-approve or bulk default approval.
- Approve cannot bypass T121 evidence validation.
- Review metadata history is updated correctly.
- Rejected/frozen/archived cannot become runtime-ready.
- Export does not leak private data to docs/examples/tests/stdout.
- No runtime integration, DB migration, vector DB, LLM call, or auto-send.
