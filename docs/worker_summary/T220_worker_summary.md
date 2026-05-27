# T220 Worker Summary

## Changed

- Added four T220 schema models in `src/practical_chat_agent/core/models.py`:
  - `OutboundMessagePayload`
  - `OutboundRequestHumanApproval`
  - `OutboundRequestSendGate`
  - `OutboundMessageRequest`
- Kept M10 `CandidateAction` separate from outbound intent:
  - `source_type="candidate_action"` means evidence only
  - `source_candidate_action_id` stores the candidate artifact id only
  - `CandidateAction.status="approved"` and `is_runtime_visible()` do not make a request sendable
- Added outbound payload metadata validation that rejects:
  - scheduler fields such as `send_at`, `scheduled_at`, and `scheduler_id`
  - adapter and transport fields such as `channel_id`, `webhook_url`, and `adapter_payload`
  - credential fields such as `access_token`, `api_key`, and `app_secret`
  - raw or private content fields such as `raw_transcript`, `chat_history`, and `private_messages`
- Added `tests/test_outbound_message_request_schema.py` covering:
  - minimal valid construction
  - candidate-action evidence construction
  - JSON round-trip
  - default non-sendable state
  - reviewed `CandidateAction` is not implicit send authorization
  - forbidden execution metadata rejection
  - absence of scheduler and platform-adapter fields
- Added `docs/data_contracts/outbound_send_gate_contract.md` describing the T220 contract boundary, its relationship to M10 `CandidateAction`, the pre-T221 lifecycle, and explicit non-authorizations.

## Verification

Test-first evidence:

- `tests/test_outbound_message_request_schema.py` was written before the new schema existed.
- The first targeted pytest run failed during import because `OutboundMessagePayload` and `OutboundMessageRequest` did not exist yet.

Formal verification used workspace-local temp and cache paths because the Windows sandbox temp directory is not reliable here:

- `TEMP` and `TMP`: `artifacts\t220_pytest_tmp`
- pytest cache: `artifacts\t220_pytest_cache`
- pytest base temp: `artifacts\t220_pytest_basetemp`

Commands and results:

- `python -m py_compile src/practical_chat_agent/core/models.py`
  - passed
- `pytest tests/test_outbound_message_request_schema.py -q -o cache_dir=artifacts\t220_pytest_cache --basetemp=artifacts\t220_pytest_basetemp`
  - 11 passed
- `pytest tests/test_behavior_schema.py tests/test_outbound_message_request_schema.py -q -o cache_dir=artifacts\t220_pytest_cache --basetemp=artifacts\t220_pytest_basetemp`
  - 36 passed
- `pytest tests -q -o cache_dir=artifacts\t220_pytest_cache --basetemp=artifacts\t220_pytest_basetemp`
  - 791 passed

## Explicit Non-Actions

- No message sending.
- No T221 `OutboundSendGate` implementation.
- No fake adapter, Feishu adapter, WeChat adapter, or review card implementation.
- No scheduler, timer, reminder, background job, automation, runtime loop, or CLI send path.
- No LLM or provider calls, web services, vector DB, Mem0, or Zep.
- No mutation of `CandidateAction` semantics into executable outbound behavior.
- No reads from `private/chat_history/` and no committed private content.
- No update to `docs/04_task_board.md`.

## Remaining Risks

- T220 defines the contract only; T221 still needs to implement quiet hours, frequency limits, duplicate suppression, kill switch behavior, and audit policy.
- `source_context_refs` remain caller-supplied review-safe refs in T220; this task does not perform store-backed evidence validation.
- `channel_preference` is intentionally data-only and not a real adapter target; later platform tasks must preserve that separation explicitly.
