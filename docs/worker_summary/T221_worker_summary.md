# T221 Worker Summary

## Changed

- Added `src/practical_chat_agent/services/outbound_send_gate.py` with:
  - `OutboundSendGateConfig`
  - `OutboundSendGateContext`
  - `OutboundSendGateDecision`
  - `OutboundSendGate`
- Extended `tests/test_outbound_message_request_schema.py` to cover the most
  valuable T220 review gaps:
  - `is_sendable()` true path
  - standalone validator failures for incomplete approval metadata
  - standalone validator failures for incomplete gate metadata
  - outbound-specific forbidden metadata keys
  - timestamp round-trip preservation
  - all supported `channel_preference` values
- Added `tests/test_outbound_send_gate.py` covering deterministic gate
  behavior:
  - approved request allowed path
  - stable mapping input
  - pending/rejected approval blocking
  - kill switch blocking
  - whitespace draft rejection
  - quiet-hours blocking, including overnight windows
  - frequency-limit blocking from supplied synthetic history
  - duplicate suppression from supplied synthetic history
  - self-echo prevention from latest inbound text and explicit reference text
- Updated `docs/data_contracts/outbound_send_gate_contract.md` to include the
  T221 gate lifecycle, config and decision shape, audit-note conventions,
  rule semantics, and an explicit statement that gate allowance is not
  delivery.

## Gate Behavior Added

- `OutboundSendGate.evaluate()` accepts either a validated
  `OutboundMessageRequest` or a stable mapping that validates to one.
- Evaluation is pure and non-mutating: it returns a new request copy wrapped in
  `OutboundSendGateDecision`.
- The gate updates `send_gate` to:
  - `allowed` only when all checks pass
  - `blocked` when any check fails
- Evaluated gate state always carries:
  - `evaluator_id`
  - `evaluated_at`
  - deterministic `gate_notes`
- The service preserves request ids, contact/user ids, source refs, channel
  preference, and risk flags. It keeps `source_candidate_action_id` as evidence
  only and does not treat `channel_preference` as an adapter target.

## Policy Rules Implemented

- Manual-only approval:
  - pending outbound approval blocks with `human_approval_pending`
  - rejected outbound approval blocks with `human_approval_rejected`
  - reviewed `CandidateAction` evidence does not satisfy this rule
- Kill switch:
  - blocks all requests with `kill_switch_enabled`
- Quiet hours:
  - blocks inside the configured local HH:MM window
  - supports overnight windows
- Frequency limit:
  - counts same-scope prior gate-`allowed` requests from supplied synthetic
    history
  - blocks with `frequency_limit_exceeded`
- Duplicate suppression:
  - normalizes text with whitespace collapse and case folding
  - blocks same-scope duplicates with `duplicate_suppressed`
- Self-echo prevention:
  - blocks normalized text identical to supplied latest inbound/user text or
    explicit self-echo reference text
  - uses `self_echo_prevention`
- Defensive payload check:
  - whitespace-only draft text blocks with `empty_draft_text`

## Verification

Test-first evidence:

- `tests/test_outbound_send_gate.py` and the extra T220 coverage in
  `tests/test_outbound_message_request_schema.py` were added before the new
  service existed.
- The first targeted pytest run failed during import because
  `practical_chat_agent.services.outbound_send_gate` did not exist yet.

Formal verification used workspace-local temp and cache paths because the
Windows sandbox temp directory is not reliable here:

- `TEMP` and `TMP`: `artifacts\t221_pytest_tmp`
- pytest cache: `artifacts\t221_pytest_cache`
- pytest base temp: `artifacts\t221_pytest_basetemp`

Commands and results:

- `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py`
  - passed
- `pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q -o cache_dir=artifacts\t221_pytest_cache --basetemp=artifacts\t221_pytest_basetemp`
  - 31 passed
- `pytest tests/test_behavior_schema.py tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py -q -o cache_dir=artifacts\t221_pytest_cache --basetemp=artifacts\t221_pytest_basetemp`
  - 56 passed
- `pytest tests -q -o cache_dir=artifacts\t221_pytest_cache --basetemp=artifacts\t221_pytest_basetemp`
  - 811 passed

## Explicit Non-Actions

- No message sending.
- No scheduler, timer, reminder, background job, automation, or runtime loop.
- No fake adapter, Feishu adapter, WeChat adapter, review card, or platform
  integration.
- No CLI send command, app-container wiring, or delivery execution path.
- No LLM or provider calls, web services, vector DB, Mem0, or Zep.
- No mutation of `CandidateAction`, memory records, ContactSkill,
  `RelationshipState`, approved stores, or private artifacts.
- No reads from `private/chat_history/` and no committed private content.
- No update to `docs/04_task_board.md`.

## Remaining Risks

- T221 is gate-only. It records policy state, not delivery state. T222+ still
  need to decide how an allowed request is consumed without blurring
  `allowed` and `delivered`.
- Frequency and duplicate checks currently treat prior gate-`allowed` requests
  as send-equivalent synthetic history because the project still has no
  adapter/delivery layer in scope.
- `manual_only_mode` is intentionally fixed to the current conservative
  mainline; T221 does not provide or validate any autonomous send path.
