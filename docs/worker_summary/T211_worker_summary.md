# T211 Worker Summary

## Changed

- Added `src/practical_chat_agent/services/behavior_planner.py`.
- Added `tests/test_behavior_rule_planner.py`.
- Updated `docs/data_contracts/behavior_planner_contract.md` with T211 rule-engine scope, input boundaries, rule firing semantics, ordering/max-candidate behavior, and downstream milestone boundaries.
- Appended a T211 implementation record to `docs/07_handoff.md`.

## Rule Behavior Added

- `BehaviorRulePlanner.plan()` accepts `AgentSelfState`, optional
  `BehaviorPolicy`, and optional `safe_context_labels`.
- Rule order is deterministic:
  1. `boundary_review_note`
  2. `memory_review_prompt`
  3. `relationship_check_in_draft`
  4. `do_nothing` fallback
- `do_nothing` is emitted for empty/thin context when policy allows it.
- If no rule is allowed and `do_nothing` is also disallowed, the planner returns
  an empty list.
- `BehaviorPolicy.allowed_action_types` is enforced before emission.
- `BehaviorPolicy.max_candidates` is respected after rule filtering.
- Candidate ids are deterministic hashes of safe ids and supporting refs.

## Explicit Non-Actions

- No message sending.
- No scheduler, timer, reminder, background job, automation, or recurring task.
- No Feishu, WeChat, browser, desktop, notification, email, webhook, or platform adapter.
- No CLI, app-container wiring, runtime loop, or execution hook.
- No LLM, provider API, embedding service, vector DB, Mem0/Zep, or external service.
- No final user-facing message draft generation.
- No mutation of `MemoryFact`, `ContactSkill`, `RelationshipState`,
  `PreferencePatchCandidate`, approved stores, private artifacts, or review metadata.
- No private chat-history reads or committed private content.

## Verification

Commands were run with `TEMP` and `TMP` set to `artifacts/pytest_tmp`, pytest
cache set to `artifacts/pytest_cache`, and full-suite `--basetemp` set to
`artifacts/pytest_basetemp` after `.tmp/pytest` hit a Windows permission error.

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py`: passed.
- `pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py -q -o cache_dir=artifacts\pytest_cache`: 40 passed.
- `pytest tests/ -q --basetemp=artifacts\pytest_basetemp -o cache_dir=artifacts\pytest_cache`: 762 passed.

## Remaining Risks

- T211 is intentionally under-generative and deterministic; it does not rank
  candidates beyond fixed rule order.
- `safe_context_labels` are trusted as caller-provided compact labels; the
  service API avoids raw-text parameters, but callers must still avoid passing
  raw content through labels.
- `relationship_check_in_draft` only creates a review-safe candidate summary,
  not final user-facing wording. T212 remains responsible for draft generation.

