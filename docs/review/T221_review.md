# Review: T221

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01 `OutboundSendGateConfig` uses a plain `@dataclass` rather than a Pydantic `BaseModel`. This is internally consistent with `OutboundSendGateContext` and `OutboundSendGateDecision` (which are also dataclasses), but it means config validation in `__post_init__` raises plain `ValueError` rather than Pydantic `ValidationError`. This is acceptable for a service-layer config object that is not serialized/deserialized through JSON round-trips.

N02 `_parse_hhmm` is called twice on each config field during `_is_quiet_hours` (once to parse, once to compare) because the parsed `time` objects are not cached. This is harmless for the current scale (a single call per `evaluate`), but a future optimization could parse once in `__post_init__` and store the result.

N03 `_normalize_text` uses `casefold()` for case-insensitive matching, which is correct for Latin text but may not fully normalize CJK characters that have case or compatibility variants. For Chinese draft text, this is acceptable because Chinese characters do not have case variants; `casefold` is effectively a no-op for them, and the whitespace collapse via `split()`/join is the meaningful normalization.

N04 The `tzdata` package is not listed as a project dependency. The gate service imports `ZoneInfo` from the standard library `zoneinfo` module, which requires `tzdata` on Windows (Python 3.9+). Without `tzdata` installed, all tests involving timezone-aware datetime construction fail. The worker's environment had `tzdata` installed, so the 811-passed result is reproducible only when `tzdata` is present. This is a latent portability issue, not a correctness bug.

N05 `OutboundSendGateConfig.__post_init__` enforces `manual_only_mode=True` with a `ValueError`, which is correct for the current conservative mainline. However, the field remains on the config as a `bool`, so a caller who sets `manual_only_mode=False` in the constructor dict (before `__post_init__` runs) gets a clear error. This is appropriate defensive design.

N06 `existing_audit` parameter in `evaluate()` accepts a `Sequence[str]` of prior gate notes that are merged into the new gate notes. This is currently unused in the test suite (no test passes `existing_audit`). The feature is harmless and forward-compatible, but untested.

N07 `OutboundSendGateDecision` does not record the `config` or `evaluator_id` used at decision time; the evaluator_id is only on the evaluated request's `send_gate`. This is fine since `evaluated_request.send_gate.evaluator_id` carries it, but the decision object itself is not self-contained for audit purposes without referencing back to the request.

## Missing Tests

M01 No test for the quiet-hours clear path (i.e., verifying that a request made outside the quiet-hours window gets `quiet_hours_clear` in passed_checks). The existing tests only verify blocking, not the pass-through case with quiet hours configured.

M02 No test for the frequency-limit clear path (i.e., verifying that a request made within the frequency limit gets `frequency_limit_clear`). The existing test only verifies the exceeded case.

M03 No test for the duplicate-suppression clear path (i.e., verifying that a request with different text or outside the window gets `duplicate_check_clear`). The existing test only verifies the blocked case.

M04 No test for self-echo clear path (i.e., verifying that a request whose text does not match any context references gets `self_echo_clear`). The existing tests only verify the blocked cases.

M05 No test for the `existing_audit` parameter being merged into gate notes.

M06 No test for `OutboundSendGateConfig` validation edge cases: empty `evaluator_id`, negative `frequency_limit_count`, negative `duplicate_window_seconds`, invalid `quiet_hours_start` format.

M07 No test verifying that the gate decision is deterministic (i.e., calling `evaluate` twice with the same inputs produces identical results).

M08 No test for the `_coerce_context` path with a `Mapping[str, Any]` input (only `OutboundSendGateContext` and `None` are tested).

M09 No test verifying that `model_copy` does not mutate the original request's `updated_at` (the non-mutation test checks `send_gate.gate_state` but not `updated_at` on the original).

M10 No test for kill-switch AND pending-approval both blocking, verifying that `blocked_reasons` contains both `kill_switch_enabled` and `human_approval_pending`.

## Suspicious Implementation Details

None. The implementation is clean, minimal, and deterministic. All seven policy rules are present and correct. The gate is pure (non-mutating), returns a new request copy, and does not introduce adapters, schedulers, CLI paths, or external dependencies. The code follows established project patterns for service-layer implementations.

## Verification

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py`: passed
- `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q`: 31 passed (after installing `tzdata`; fails without it due to `ZoneInfo` requiring `tzdata` on Windows)
- `pytest tests/test_behavior_schema.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q`: 56 passed (worker reports same)
- Full suite: 791 passed, 16 pre-existing failures in LLM/typer-dependent tests (not related to T221)

Note: The worker's test results (811 passed) match the current count (791 + 20 new T221 tests = 811). All verification used workspace-local temp/cache paths as documented.

## Allowed Files Compliance

Changed files:
- `src/practical_chat_agent/services/outbound_send_gate.py` — in allowed list
- `tests/test_outbound_send_gate.py` — in allowed list
- `tests/test_outbound_message_request_schema.py` — in allowed list
- `docs/data_contracts/outbound_send_gate_contract.md` — in allowed list
- `docs/worker_summary/T221_worker_summary.md` — in allowed list
- `docs/07_handoff.md` — in allowed list

No forbidden files were modified. `src/practical_chat_agent/core/models.py` was NOT modified by T221. No forbidden scope was entered.

## Forbidden Scope Compliance

- No message sending, scheduling, timers, reminders, background jobs, or automations.
- No Feishu, WeChat, webhook, email, browser, desktop, or platform adapter integration.
- No runtime loops, CLI execution paths, app-container wiring, or service execution.
- No LLM/provider API calls, embeddings, vector DB, Mem0/Zep, web services, or external systems.
- No mutation of `MemoryFact`, `ContactSkill`, `RelationshipState`, `CandidateAction`, approved stores, private artifacts, or review metadata.
- No `CandidateAction` approval/status/runtime-visibility treated as send/schedule/platform authorization.
- No implementation of T222 fake adapter, T223 Feishu adapter, or T224 review card.
- No `private/chat_history/` reads or committed private content.
- No `docs/04_task_board.md` update.

## Recommended Next Action

T221 is complete as a deterministic send-gate service. The next task should be T222 (local fake adapter), which will consume sendable `OutboundMessageRequest` records and simulate delivery locally.

The missing tests (M01-M10) are minor coverage gaps for pass-through paths and config edge cases. They do not block acceptance. The most valuable to add early in T222 would be M01-M04 (pass-through path tests for quiet hours, frequency limit, duplicate, and self-echo) to confirm the full allow-path works end-to-end when a real adapter starts consuming gate decisions.
