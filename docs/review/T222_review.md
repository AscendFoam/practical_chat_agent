# Review: T222

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01: `_is_candidate_action_input` mapping heuristic uses `action_id`, `action_type`, and `schema_version=="candidate_action_v1"` as CandidateAction fingerprints. A non-CandidateAction mapping that happens to carry an `action_type` key would be rejected. This is conservative and safe for current scope, but is a heuristic rather than a type-check.

N02: `_mapping_value` returns `None` for non-Mapping inputs (including `CandidateAction` model instances), so rejected CandidateAction results report `contact_id=None` and `user_id=None` even though the model has those fields. The result is already `blocked_invalid_request`, so this is cosmetic rather than behavioral.

N03: `payload_preview` truncation collapses whitespace via `" ".join(draft_text.split())` and then truncates. There is no content-level redaction beyond length capping. Acceptable for synthetic-only test scope, but future real adapters must not rely on preview truncation as a privacy boundary.

## Missing Tests

M01: No test exercises `FakeOutboundAdapterConfig` validation: empty `adapter_name` and non-positive `preview_char_limit` should raise `ValueError` per `__post_init__`.

M02: No test passes `existing_audit` to `deliver()` and verifies those notes appear in `result.audit_notes`. The `_clean_audit` / `_dedupe` path is covered indirectly through the blocked paths but not with explicit pre-seeded audit content.

M03: No test covers `payload_preview` truncation at the exact boundary (draft text length equals `preview_char_limit`, or `preview_char_limit <= 3` edge case).

## Suspicious Implementation Details

None. The implementation is straightforward, deterministic, and local. No external calls, no disk writes, no scheduler behavior, no mutation of inputs. The adapter correctly delegates sendability to `OutboundMessageRequest.is_sendable()` and adds informative audit notes for why blocked requests failed.

## Verification

- `python -m py_compile` for all three source files: passed.
- `pytest tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py`: 24 passed.
- `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py`: 43 passed.
- Full suite: 10 pre-existing failures (typer/LLM/CLI-dependent), 762 passed. No new failures from T222.

## Allowed Files Check

All changed files are within the T222 allowed list:

- `src/practical_chat_agent/services/outbound_fake_adapter.py` (new)
- `tests/test_outbound_fake_adapter.py` (new)
- `tests/test_outbound_send_gate.py` (T221 clear-path additions)
- `docs/data_contracts/outbound_send_gate_contract.md` (T222 sections)
- `docs/worker_summary/T222_worker_summary.md` (new)
- `docs/07_handoff.md` (T222 completion record)

No forbidden files modified. `pyproject.toml` and `__init__.py` not modified (tzdata decision: UTC-only, R097 remains open).

## Forbidden Scope Check

- No real message sending.
- No Feishu/WeChat/webhook/email/browser/desktop/notification API calls.
- No scheduler/timer/reminder/background job/automation/runtime loop.
- No CLI send path or app-container wiring.
- No LLM/provider calls, web services, vector DB, Mem0/Zep.
- No mutation of CandidateAction, memory, ContactSkill, RelationshipState, approved stores, or private artifacts.
- No `private/chat_history/` reads.
- No task-board update.
- `CandidateAction` inputs are explicitly rejected at the adapter boundary.
- `is_sendable()` is respected as the adapter boundary.
- Gate `allowed` is not treated as delivery completion.

## Recommended Next Action

T222 is review-complete. Captain may mark T222 as complete and advance to T223 (Feishu adapter) or T224 (Feishu review card). The fake adapter boundary and audit trail established here should be carried forward as the reference pattern for real adapter tasks.
