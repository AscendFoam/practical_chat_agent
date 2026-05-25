# Task T212: Proactive Draft Generator

## Task ID

T212

## Goal

Generate short review-safe draft text for draft-only `CandidateAction` records.

This task enriches candidate actions with `CandidateActionPayload.draft_text`, but it must remain review-only and non-executable.

## Why Now

T211 has passed review with `PASS` and established deterministic candidate-action proposal. The next safe step is to enrich those candidate actions with short draft text so reviewers can inspect a more complete proposed behavior, while still forbidding sending, scheduling, platform execution, or approval bypass.

## Inputs To Read

- `AGENTS.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/data_contracts/behavior_planner_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/behavior_planner.py`
- `tests/test_behavior_schema.py`
- `tests/test_behavior_rule_planner.py`
- Existing review-only draft/planner patterns, especially:
  - `src/practical_chat_agent/services/reply_planner.py`
  - `tests/test_reply_planner.py`

## Allowed Files

- `src/practical_chat_agent/services/behavior_planner.py`
- `src/practical_chat_agent/core/models.py` only if a narrowly scoped model/helper addition is necessary for the draft-text contract
- `tests/test_behavior_rule_planner.py`
- `tests/test_behavior_schema.py` only if a narrow schema boundary needs to be hardened for draft payloads
- `docs/data_contracts/behavior_planner_contract.md`
- `docs/worker_summary/T212_worker_summary.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not send messages.
- Do not schedule real actions, create timers, reminders, background jobs, automations, or recurring tasks.
- Do not integrate Feishu, WeChat, browser, desktop, notification, email, webhook, or any platform adapter.
- Do not add CLI commands, app container wiring, runtime loops, or automatic execution hooks.
- Do not call an LLM, provider API, embedding service, vector DB, Mem0/Zep, or any external service.
- Do not make proactive generation the default for outbound behavior.
- Do not mutate `MemoryFact`, `ContactSkill`, `RelationshipState`, `PreferencePatchCandidate`, approved stores, private artifacts, or review metadata.
- Do not read `private/chat_history/` or commit private chat content.
- Do not bypass human review or treat a draft-text-enriched `CandidateAction` as sendable or schedulable.
- Do not update `docs/04_task_board.md`; Captain will mark completion after review.

## Expected Output

Add deterministic draft-text enrichment for existing safe `CandidateAction` records.

The service should:

- Accept a `CandidateAction` or a stable candidate-action input shape and return a `CandidateAction` with `payload.draft_text` populated.
- Preserve T210/T211 invariants on every emitted or updated candidate.
- Preserve the candidate’s `action_type`, `supporting_context_refs`, `risk_flags`, `policy`, and `status`.
- Keep `draft_text` short, reviewable, and clearly aligned with the candidate’s `safe_summary` and rationale.
- Avoid raw transcript or private-text echoing.
- Avoid platform-target or send semantics.
- Keep output deterministic for the same input candidate.

Recommended draft-text behavior:

- `boundary_review_note`: produce a short review note that tells the reviewer to check boundary-sensitive context first.
- `memory_review_prompt`: produce a short note reminding the reviewer to verify recent memory/relationship signals before replying.
- `relationship_check_in_draft`: produce a short, low-pressure check-in draft that remains obviously review-only and non-committal.
- `do_nothing`: produce a concise review-safe no-action note.

The drafts should be phrased as candidate text for human review, not as final outbound text. Keep the output conservative, small, and unembellished. The service must not attempt to improve engagement, imitate a specific person, or simulate a real conversational turn.

Update `docs/data_contracts/behavior_planner_contract.md` with:

- T212 draft-enrichment scope
- allowed input/output shape
- draft safety and length constraints
- relationship to T211 and T213/T214

Write `docs/worker_summary/T212_worker_summary.md` with:

- files changed
- draft generation behavior added
- verification commands/results
- explicit non-actions
- remaining risks

Append a T212 implementation record to `docs/07_handoff.md`.

## Verification

Run:

```powershell
python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py
pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py -q
pytest tests/ -q
```

If the Windows default temp directory is inaccessible in this sandbox, set `TEMP` and `TMP` to a workspace-local temp directory before running pytest and record that fact in `docs/07_handoff.md`.

Minimum test coverage expected in `tests/test_behavior_rule_planner.py`:

- draft text is populated for the supported candidate types
- draft text is short and review-safe
- deterministic draft text for the same input
- no raw transcript/private text is echoed
- no send/schedule/platform fields appear
- existing candidate invariants remain intact after enrichment
- `do_nothing` remains a safe review-only output
- boundary-sensitive candidates produce conservative draft wording
- memory-review candidates produce review-safe reminder wording
- relationship check-in candidates remain low-pressure and non-committal

## Docs To Update

- `docs/data_contracts/behavior_planner_contract.md`
- `docs/07_handoff.md`
- `docs/worker_summary/T212_worker_summary.md`

Do not update `docs/04_task_board.md`; Captain will mark completion after review.

## Reviewer Type

adversarial
