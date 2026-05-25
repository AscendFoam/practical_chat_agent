# T213 Worker Summary

## Changed

- Added `CandidateActionReviewService` and `CandidateActionReviewError` to
  `src/practical_chat_agent/services/behavior_planner.py`.
- Added `chat-behavior-review-action` CLI command in
  `src/practical_chat_agent/app/main.py`.
- Expanded `tests/test_behavior_rule_planner.py` with service-level review tests.
- Added `tests/test_behavior_review_cli.py` for CLI review and stdout safety.
- Updated `docs/data_contracts/behavior_planner_contract.md` with T213 review
  semantics and approved-is-not-sendable boundaries.
- Appended a T213 implementation record to `docs/07_handoff.md`.

## Service And CLI Behavior Added

- `CandidateActionReviewService.review_candidate()` accepts a validated
  `CandidateAction` or mapping and returns a new reviewed object.
- Supported decisions are `approve`, `reject`, `freeze`, and `archive`.
- Reviewer id is required.
- Review updates status, review metadata, history, and optional decision notes.
- Review preserves action type, payload safe summary, draft text, supporting
  refs, risk flags, policy, and all no-send/no-platform/no-scheduler invariants.
- `chat-behavior-review-action` reads one CandidateAction JSON file, applies a
  manual decision, writes reviewed JSON, and prints only safe metadata.

## Explicit Non-Actions

- No message sending.
- No scheduler, timer, reminder, background job, automation, or recurring task.
- No Feishu, WeChat, browser, desktop, notification, email, webhook, platform adapter, or send gate.
- No LLM calls, provider APIs, embeddings, vector DBs, Mem0/Zep, or external services.
- No mutation of `MemoryFact`, `ContactSkill`, `RelationshipState`,
  `PreferencePatchCandidate`, approved stores, private artifacts, or unrelated review metadata.
- No private chat-history reads or committed private content.
- No task board update.

## Verification

Commands were run with `TEMP` and `TMP` set to `artifacts/t213_pytest_tmp`, pytest
cache set to `artifacts/t213_pytest_cache`, and full-suite `--basetemp` set to
`artifacts/t213_pytest_basetemp` to avoid the sandbox's Windows default temp/cache
permission warnings.

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py src/practical_chat_agent/app/main.py`: passed.
- `pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py tests/test_behavior_review_cli.py -q -o cache_dir=artifacts\t213_pytest_cache --basetemp=artifacts\t213_pytest_basetemp`: 58 passed.
- `pytest tests -q -o cache_dir=artifacts\t213_pytest_cache --basetemp=artifacts\t213_pytest_basetemp`: 780 passed.

## Remaining Risks

- CLI output path is caller-controlled; stdout is tested as safe, but operators
  should keep operational review artifacts under `private/`.
- Approval makes a candidate runtime-visible under existing schema semantics,
  but it remains non-sendable and non-schedulable until later OutboundSendGate work.
- T213 does not run behavior safety evaluation; T214 remains responsible for that layer.
