# T210 Worker Summary

## Changed

- Added T210 draft-only behavior schemas in `src/practical_chat_agent/core/models.py`:
  - `AgentSelfState`
  - `BehaviorPolicy`
  - `CandidateActionPayload`
  - `CandidateAction`
- Added `tests/test_behavior_schema.py` with committed synthetic schema tests.
- Added `docs/data_contracts/behavior_planner_contract.md` describing lifecycle, allowed draft-only action types, forbidden payload fields, privacy boundaries, evidence refs, and the later OutboundSendGate boundary.
- Appended a T210 implementation record to `docs/07_handoff.md`.

## Scope Boundaries Preserved

- No message sending.
- No real scheduler, background job, timer, reminder, or automation.
- No platform adapter or platform target.
- No BehaviorPlanner execution logic, rule engine, ranking engine, or CLI.
- No memory, ContactSkill, relationship-state, approved-patch, store, or private-artifact mutation.
- No private chat-history reads or committed private content.
- No LLM calls, provider configuration, embeddings, vector DBs, Mem0/Zep production use, or fine-tuning.

## Verification

Commands run with `TEMP` and `TMP` pointed to `.tmp/pytest`, and pytest cache
pointed to `.tmp/pytest_cache`:

- `python -m py_compile src/practical_chat_agent/core/models.py` passed.
- `pytest tests/test_behavior_schema.py -q -o cache_dir=.tmp\pytest_cache` passed: 25 tests.
- `pytest tests/ -q -o cache_dir=.tmp\pytest_cache` passed: 747 tests.

## Remaining Risks

- The T210 schemas are contract-only. They do not yet define planner selection,
  candidate ranking, review CLI behavior, or outbound send-gate integration.
- `CandidateAction.is_runtime_visible()` is only a visibility helper; it does
  not execute anything. Later tasks must preserve that distinction.
- Forbidden payload fields are enforced only inside `CandidateActionPayload.metadata`.
  Future payload expansion should keep the same no-platform/no-scheduler/no-raw
  boundary.
