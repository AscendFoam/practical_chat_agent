# Task T130: ReplyPlan Schema

## Task ID

T130

## Goal

定义 ReplyPlan schema 和 prompt contract，用于表达多候选回复草稿、推荐理由、边界检查和引用的 skill / memory / policy 证据。

## Why now

T123 已把 approved + runtime-ready 的 store 资产安全接入 `ChatContext`。下一步需要把这类上下文转成明确、可审计、可校验的回复规划结构，供后续 ReplyPlanner 使用，但本轮仍不实现真实回复生成。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/reply_plan_contract.md`
- `docs/07_handoff.md`

如果发现确实需要额外修改 `src/practical_chat_agent/services/chat_context.py` 或 `app/main.py` 才能正确表达 schema，请先停下来向 Captain 说明，不要自行扩大 scope。

## Forbidden scope

- 不调用 LLM。
- 不生成回复草稿逻辑。
- 不发送消息。
- 不自动改写 ContactSkill、memory facts 或 policy。
- 不接数据库，不做 migration，不引入向量数据库或 pgvector。
- 不读取 `private/chat_history/` 原始聊天记录。
- 不把私密聊天原文、真实联系人名、真实平台 ID、raw prompt 或 raw response 写入 docs/examples/tests/stdout。

## Inputs to read

- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/review/M2_review.md`
- `docs/review/T123_review.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/chat_context.py`
- Approved-store context models introduced by T123.

## Expected output

Implement a minimal, strongly typed ReplyPlan contract.

Minimum schema behavior:

- Represent at least 3 candidate reply drafts.
- Include per-candidate:
  - draft text
  - rationale
  - cited skill/memory refs
  - risk flags
  - boundary reminders
  - confidence or priority signal if useful
- Represent overall planning metadata:
  - contact_id
  - source context ids
  - policy or boundary summary
  - notes explaining why candidates differ
- Make the schema compatible with the compact `ChatContext` brief from T123.
- Keep field names explicit and review-friendly.
- Do not overfit to one contact or one demo sample.

Prompt contract expectations:

- Describe how the ReplyPlan is intended to be used.
- State that it is for candidate generation and review only.
- State that it must not impersonate the contact or claim knowledge without evidence.
- State that it should prefer conservative options for uncertain or sensitive cases.

## Verification

Run compile verification if Python models are added or changed:

```powershell
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/core/models.py
```

Run a lightweight contract check using synthetic fixture data or simple model validation:

- The schema can represent 3+ candidates.
- The schema can reference approved-store context ids / evidence refs.
- The schema does not require raw transcript text.
- Existing `ChatContext` / approved-store fields remain compatible.

No demo turn, LLM call, or send step is required for T130.

## Docs to update

- `docs/data_contracts/reply_plan_contract.md`
- `docs/07_handoff.md`

The handoff update should include:

- What ReplyPlan fields / contract were added.
- How the schema ties back to T123 approved-store context.
- Which synthetic validation or compile check was used.
- Any remaining risks or assumptions.

Do not update `docs/04_task_board.md`, `docs/05_decision_log.md`, or `docs/08_risks_and_open_questions.md`; Captain updates those after review.

## Reviewer type

normal

Reviewer should specifically check:

- The schema supports at least 3 candidate drafts.
- No LLM call or send logic was introduced.
- No raw transcript or private data leaked.
- The contract is compatible with approved-store context from T123.
- Field names and usage boundaries are explicit enough for T131/T132.
