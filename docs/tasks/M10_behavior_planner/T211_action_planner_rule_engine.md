# Task T211: Action Planner Rule Engine

## Task ID

T211

## Goal

Implement a deterministic, local rule engine that can propose zero or more draft-only `CandidateAction` records from T210 behavior contracts.

This is the first executable M10 layer, but it must remain non-executing: it decides what should be shown to a human reviewer as a candidate action, not what should be sent, scheduled, or applied.

## Why Now

T210 has passed review with `PASS` and established the non-executable behavior schemas:

- `AgentSelfState`
- `BehaviorPolicy`
- `CandidateActionPayload`
- `CandidateAction`

The next safe step is to prove the repo can generate candidate actions deterministically while preserving those schema invariants. This must happen before T212 draft-text generation, T213 review CLI, T214 safety eval, or any later OutboundSendGate/platform work.

## Inputs To Read

- `AGENTS.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/data_contracts/behavior_planner_contract.md`
- `src/practical_chat_agent/core/models.py`
- `tests/test_behavior_schema.py`
- Existing deterministic service/test patterns, especially:
  - `src/practical_chat_agent/services/reply_planner.py`
  - `src/practical_chat_agent/services/feedback.py`
  - `tests/test_reply_planner.py`
  - `tests/test_behavior_schema.py`

## Allowed Files

- `src/practical_chat_agent/services/behavior_planner.py`
- `src/practical_chat_agent/core/models.py` only if a narrowly scoped model/helper addition is necessary for the rule engine contract
- `tests/test_behavior_rule_planner.py`
- `tests/test_behavior_schema.py` only if the worker chooses to close narrow T210 accepted test-strength gaps while already touching schema behavior
- `docs/data_contracts/behavior_planner_contract.md`
- `docs/worker_summary/T211_worker_summary.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not send messages.
- Do not schedule real actions, create timers, reminders, background jobs, automations, or recurring tasks.
- Do not integrate Feishu, WeChat, browser, desktop, notification, email, webhook, or any platform adapter.
- Do not add CLI commands, app container wiring, runtime background loops, or automatic execution hooks.
- Do not call an LLM, provider API, embedding service, vector DB, Mem0/Zep, or any external service.
- Do not generate final user-facing message drafts in this task; T212 owns draft generation. T211 may use short review-safe `safe_summary` text only.
- Do not mutate `MemoryFact`, `ContactSkill`, `RelationshipState`, `PreferencePatchCandidate`, approved stores, private artifacts, or review metadata.
- Do not read `private/chat_history/` or commit private chat content.
- Do not bypass human review or treat an approved/runtime-visible `CandidateAction` as sendable or schedulable.
- Do not update `docs/04_task_board.md`; Captain will mark completion after review.

## Expected Output

Add a deterministic service, preferably in `src/practical_chat_agent/services/behavior_planner.py`, with a name such as `BehaviorRulePlanner` or `BehaviorRulePlannerService`.

The service should:

- Accept an `AgentSelfState` and an optional `BehaviorPolicy`.
- Accept only review-safe inputs such as approved context refs, recent signal refs, compact risk flags, and short caller-provided context labels. It must not accept raw transcript text.
- Return a stable list of `CandidateAction` records.
- Return `do_nothing` or an empty candidate set when context is too thin or no rule fires. Pick one behavior and document it.
- Preserve T210 invariants on every emitted candidate:
  - `human_review_required=True`
  - `auto_send_allowed=False`
  - `platform_execution_allowed=False`
  - `scheduler_allowed=False`
  - `platform_target=None`
  - payload metadata contains no forbidden keys
- Enforce `BehaviorPolicy.allowed_action_types` before emitting a candidate.
- Keep ordering deterministic when multiple rules fire.
- Respect `BehaviorPolicy.max_candidates`.
- Include at least one `supporting_context_ref` for every emitted candidate.
- Include rule-specific `rationale`, `risk_flags`, and review-safe payload `safe_summary`.

Recommended initial rule surface:

- `boundary_review_note`: fire when `risk_flags` or explicit inputs indicate boundary-sensitive context.
- `memory_review_prompt`: fire when recent safe signal refs suggest memory or relationship context should be reviewed before replying.
- `relationship_check_in_draft`: fire only when there is at least one approved context ref and no hard risk flag blocks proactive wording.
- `do_nothing`: fire when context is too thin, blocked by risk, or no other rule is allowed.

The exact rule names may vary, but the implementation must be conservative, deterministic, and under-generative. Prefer fewer candidates with clear rationale over speculative proactive behavior.

Update `docs/data_contracts/behavior_planner_contract.md` with:

- T211 rule-engine scope
- input boundary
- output ordering and max-candidate behavior
- rule firing semantics
- no-send/no-scheduler/no-platform/no-mutation guarantees
- relationship to T212/T213/T214

Write `docs/worker_summary/T211_worker_summary.md` with:

- files changed
- rule behavior added
- verification commands/results
- explicit non-actions
- remaining risks

Append a T211 implementation record to `docs/07_handoff.md`.

## Verification

Run:

```powershell
python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py
pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py -q
pytest tests/ -q
```

If the Windows default temp directory is inaccessible in this sandbox, set `TEMP` and `TMP` to a workspace-local temp directory before running pytest and record that fact in `docs/07_handoff.md`.

Minimum test coverage expected in `tests/test_behavior_rule_planner.py`:

- no candidates or `do_nothing` for empty/thin context
- deterministic candidate ordering
- `max_candidates` limit
- policy disallows a rule and the service skips/falls back safely
- emitted candidates validate as `CandidateAction`
- emitted candidates preserve all no-send/no-platform/no-scheduler invariants
- no forbidden payload metadata appears
- supporting refs are required and preserved
- boundary-sensitive input produces conservative `boundary_review_note` behavior
- memory/review signal input produces `memory_review_prompt` behavior
- relationship check-in rule requires approved context refs
- no raw transcript/private field is accepted or echoed by the public service API

## Docs To Update

- `docs/data_contracts/behavior_planner_contract.md`
- `docs/07_handoff.md`
- `docs/worker_summary/T211_worker_summary.md`

Do not update `docs/04_task_board.md`; Captain will mark completion after review.

## Reviewer Type

adversarial
