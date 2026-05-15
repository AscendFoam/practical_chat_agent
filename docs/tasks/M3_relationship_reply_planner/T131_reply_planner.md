# Task T131: Relationship-Aware Reply Planner

## Task ID

T131

## Goal

Implement a relationship-aware ReplyPlanner that consumes the approved compact `ChatContext` brief and returns 3+ reviewable reply candidates using the T130 `ReplyPlan` schema.

## Why now

T123 has integrated approved/runtime-ready store data into `ChatContext`, and T130 has fixed the ReplyPlan contract. This task tests whether relationship-aware context can improve candidate replies without sending messages or exposing raw transcript data.

## Allowed files

- `src/practical_chat_agent/services/reply_planner.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

If a small model export/import update in `src/practical_chat_agent/core/models.py` is required, stop and explain why before widening scope.

## Forbidden scope

- Do not send messages.
- Do not impersonate the contact.
- Do not output roleplay such as "what the other person would say."
- Do not read `private/chat_history/`.
- Do not inject full raw transcripts, full ContactSkill JSON, or all memory facts.
- Do not implement DB migrations, vector DB, realtime platform integration, policy rewrite, auto-approval, or automatic sending.

## Inputs to read

- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/review/T123_review.md`
- `docs/review/T130_review.md`
- `docs/data_contracts/reply_plan_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/chat_context.py`
- Existing `ChatSuggestionService` / CLI style, if present.

## Expected output

- A service or CLI can generate a `ReplyPlan` from a safe synthetic or redacted runtime context.
- The plan contains at least 3 candidates.
- Each candidate includes draft text, rationale, cited refs, risk flags, boundary reminders, and a priority or confidence signal.
- Candidates should be meaningfully distinct, not minor paraphrases.
- The planner must consume compact approved-store context only and must not require raw transcript text.
- T130 warnings must be handled:
  - `priority_rank` values should be stable and unique within the plan.
  - `ReplyPlan.contact_id` must align with the source context / T123 approved-store context.

## Verification

Run compile verification if Python code changes:

```powershell
& 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m compileall src/practical_chat_agent/services/reply_planner.py src/practical_chat_agent/app/main.py
```

Run a synthetic or safe fixture context and confirm:

- 3+ candidates are emitted.
- Candidate refs point to approved-store ids, evidence refs, or safe runtime context ids.
- Candidate/rejected/frozen/archived records stay out of the plan.
- No raw transcript text is required or printed.
- `contact_id` alignment and unique ranking are checked.

## Docs to update

- `docs/07_handoff.md`

The handoff update should include:

- What service/CLI was added.
- Which safe fixture or synthetic context was used.
- Whether the T130 warning checks were enforced.
- Any remaining risks or assumptions.

Do not update `docs/04_task_board.md`, `docs/05_decision_log.md`, or `docs/08_risks_and_open_questions.md`; Captain updates those after review unless the task explicitly discovers a new risk that must be recorded immediately.

## Reviewer type

adversarial

Reviewer should specifically check:

- The planner stays review-only and offline-first.
- Candidate drafts are distinct and not just paraphrases.
- `contact_id` / source context alignment is enforced.
- No send logic, DB integration, vector DB, policy rewrite, or private transcript leakage is introduced.
