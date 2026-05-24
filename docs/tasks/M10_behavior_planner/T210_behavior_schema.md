# Task T210: Behavior Schema

## Task ID

T210

## Goal

Define the first M10 draft-only proactive behavior contracts:

- `AgentSelfState`
- `BehaviorPolicy`
- `CandidateAction`

The task should create typed, reviewable schemas and a data contract for future BehaviorPlanner work, without implementing planner execution, real scheduling, platform integration, or message sending.

## Why Now

M9 is complete at task level: the project now has memory retrieval contracts, a local approved-store retriever, synthetic retrieval evals, and an optional external-adapter spike. The next safe step is not sending or autonomy. M10 must begin with a schema-only boundary that makes proactive behavior reviewable before any engine or adapter exists.

## Inputs To Read

- `AGENTS.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `src/practical_chat_agent/core/models.py`
- Existing model tests under `tests/`, especially tests that validate Pydantic schema behavior and review-only lifecycle patterns.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `tests/test_behavior_schema.py`
- `docs/data_contracts/behavior_planner_contract.md`
- `docs/worker_summary/T210_worker_summary.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not send messages.
- Do not schedule real actions, create background jobs, timers, reminders, or automations.
- Do not integrate Feishu, WeChat, browser, desktop, notification, email, or any platform adapter.
- Do not add BehaviorPlanner execution logic, rule engines, candidate ranking engines, or CLI commands.
- Do not mutate `MemoryFact`, `ContactSkill`, relationship state, approved patches, stores, or private artifacts.
- Do not read private raw chat history or commit private content.
- Do not introduce LLM calls, provider configuration, embeddings, vector DBs, Mem0/Zep production use, or fine-tuning.
- Do not bypass human review or encode any automatic-send policy.

## Expected Output

The worker should add schema-only behavior models that are conservative and explicit:

- `AgentSelfState`: compact state about the assistant/user context that may inform future proactive suggestions, without storing raw private text.
- `BehaviorPolicy`: explicit review and safety constraints for future behavior candidates, including no-auto-send semantics.
- `CandidateAction`: a review-only proposed action artifact with stable ids, contact/user scope, action type, rationale, supporting refs, risk flags, review status, and non-executable payload shape.

The contract document should define:

- lifecycle states and which states are allowed to be runtime-visible
- allowed action-type categories for draft-only M10 scope
- forbidden payload fields and privacy boundaries
- evidence/supporting-ref expectations
- review-first semantics and relationship to later OutboundSendGate milestones

Tests should cover:

- valid minimal and rich model construction
- required fields and validation failures
- review-only defaults
- no-auto-send / no-platform-execution invariants
- status/lifecycle transitions represented as data only
- JSON round-trip
- payload does not require raw transcript text
- risk flag and supporting-ref preservation
- stable id/contact/user scope behavior where applicable

## Verification

Run:

```powershell
python -m py_compile src/practical_chat_agent/core/models.py
pytest tests/test_behavior_schema.py -q
pytest tests/ -q
```

If the Windows default temp directory is inaccessible in this sandbox, set `TEMP` and `TMP` to a workspace-local temp directory before running pytest and record that fact in `docs/07_handoff.md`.

## Docs To Update

- `docs/data_contracts/behavior_planner_contract.md`
- `docs/07_handoff.md`
- `docs/worker_summary/T210_worker_summary.md`

Do not update `docs/04_task_board.md`; Captain will mark completion after review.

## Reviewer Type

adversarial
