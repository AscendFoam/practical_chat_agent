# Review: T232

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01 The `_is_candidate_action_input` method (lines 208–220) is nearly identical to the same method in `LocalFakeOutboundAdapter` (lines 124–136 in `outbound_fake_adapter.py`) and `FeishuSandboxOutboundAdapter`. The detection logic — checking `isinstance(request, CandidateAction)` or mapping keys `schema_version == "candidate_action_v1"`, `"action_id"`, `"action_type"` — is duplicated across three adapters. This is acceptable because each adapter is independently testable and the duplication is small, but extraction to a shared utility would reduce drift risk if the detection heuristics ever change.

N02 The `_coerce_safety_decision` method (lines 200–206) converts a mapping to `WeComCustomerServiceSafetyDecision(**dict(safety_decision))`. Because `WeComCustomerServiceSafetyDecision` is a frozen dataclass, not a Pydantic model, this conversion does not perform deep validation of field types. A malformed mapping (e.g., `{"safety_state": 42}`) would raise `TypeError` or `ValueError` at dataclass construction time, which is caught at line 131 by the `except (TypeError, ValueError)` handler. This is correct behavior, but differs from the request coercion path where Pydantic `ValidationError` provides structured field-level error information.

N03 The `_blocked_invalid_request` method (lines 306–324) appends `"wecom_dry_run_blocked"` to the audit notes via `self._dedupe([*audit_notes, "wecom_dry_run_blocked"])`. However, at lines 75–81 (candidate-action rejection), the caller already passes `audit_notes=[*audit_notes, "candidate_action_input_rejected"]` without the `"wecom_dry_run_blocked"` suffix. The `_blocked_invalid_request` method then adds `"wecom_dry_run_blocked"` via deduplication. This means candidate-action rejections get both `"candidate_action_input_rejected"` and `"wecom_dry_run_blocked"` in their audit notes, which is consistent and informative. The `blocked_invalid_request` path at lines 83–92 follows the same pattern. No issue here, but the dual-site audit construction is worth noting.

N04 The adapter does not enforce that the safety decision's `request_id`/`contact_id`/`user_id` are non-None when checking identity match at lines 222–233. If a safety decision has `request_id=None` and the request also has `request_id` auto-generated, `None == request.request_id` would be `False`, producing a mismatch block. This is correct defensive behavior — a safety decision without a concrete `request_id` should not match any request — but it is not tested explicitly. The current `_matching_safety_decision` helper always fills in the request's actual IDs, so this edge is implicitly covered.

N05 The `_build_payload` method (lines 254–281) hardcodes `"msg_type": "text"` in the message payload. The task package specifies "include a text message body from `OutboundMessagePayload.draft_text`" and does not require multi-type message support. This is correct for dry-run scope, but a comment or contract note about the hardcoded msg_type would make the future multi-type extension boundary clearer.

N06 The `WeComCustomerServiceDryRunConfig` enforces `dry_run_only=True` at `__post_init__` time (line 39), which is stronger validation than the T233 `WeComCustomerServiceSafetyConfig` that validates `surface` only at `evaluate()` time. This is a positive difference and follows the reviewer's N03 suggestion from the T233 review. Worth noting as a pattern improvement.

N07 The adapter imports `WECom_CUSTOMER_SERVICE_SURFACE` from the T233 safety module (line 10) and uses it as the default `provider_surface` in both `WeComCustomerServiceDryRunConfig` and `WeComCustomerServiceDryRunResult`. It also uses the string literal `"wecom_customer_service"` in `_build_payload` (line 260). This creates a coupling: if `WECom_CUSTOMER_SERVICE_SURFACE` ever changes, `WeComCustomerServiceDryRunConfig.provider_surface` and `WeComCustomerServiceDryRunResult.provider_surface` would update automatically, but the payload string in `_build_payload` would not. This is a minor inconsistency; both values are currently the same string.

N08 Minor test-coverage gaps that are non-blocking for the task scope:
- no test for `WeComCustomerServiceDryRunConfig` with an empty `provider_surface` (the `__post_init__` raises `ValueError`)
- no test for `_coerce_safety_decision` with a mapping that has wrong field types (e.g., `safety_state=42`)
- no test for the `_blocked_invalid_request` path where `request_id` is non-None (the invalid-mapping test uses a minimal dict without `request_id`)
- no test for `prepared_payload` when `safe_summary` is `None` (the default `_sendable_request` always provides it via `OutboundMessagePayload`)
- no test verifying that `_has_required_safety_audit` rejects when audit_notes is an empty list
- no test for a non-default `provider_surface` config value in the allow path
- no test for `existing_audit=None` behavior (the default in `prepare_dry_run`)

## Missing Tests

None required beyond the non-blocking coverage gaps noted in N08. The task package requires minimum test scenarios for: allowed sendable request + allowed matching safety decision returning `wecom_dry_run_ready`; pending/blocked send gate returning `blocked_not_sendable`; missing safety decision; blocked safety decision; mismatched identity; wrong surface; missing aliases; non-wechat channel; direct `CandidateAction` rejection; candidate-shaped mapping rejection; invalid mapping; mapping parity; metadata not copied; input non-mutation; no transport/send/deliver seam. All 15 required scenarios are covered by the 23 committed tests. The additional test for missing T233 boundary audit notes (lines 313–326) goes beyond the minimum requirements.

## Suspicious Implementation Details

None. The adapter is a genuine, deterministic, local payload-preparation boundary. Every blocked status is derived from explicit inputs: request fields, safety-decision fields, config values, and audit notes. No mock, stub, hardcoded output, random value, hidden state, transport seam, API call, credential read, or delivery claim exists. The `wecom_dry_run_ready` path correctly sets `delivered=False` and records `wecom_dry_run_only` and `no_provider_delivery` audit notes. The prepared payload contains only aliases, approved draft text, optional safe summary, and source audit context. Arbitrary metadata is not copied. Input request and safety decision are not mutated.

## Allowed Files Verification

Files changed by T232 worker:

- `src/practical_chat_agent/services/wecom_customer_service_outbound_adapter.py` — new file, within allowed scope
- `tests/test_wecom_customer_service_outbound_adapter.py` — new file, within allowed scope
- `docs/data_contracts/wecom_customer_service_outbound_contract.md` — new file, within allowed scope
- `docs/worker_summary/T232_worker_summary.md` — new file, within allowed scope
- `docs/07_handoff.md` — modified, within allowed scope

No `src/practical_chat_agent/core/models.py`, `OutboundSendGate`, T233 safety gate code, inbound connectors, Feishu adapters, fake adapters, runtime services, CLI commands, or `docs/04_task_board.md` were modified.

## Task Goal Verification

The task package required:

1. `WeComCustomerServiceDryRunOutboundAdapter` as a pure local payload-preparation boundary — implemented.
2. `WeComCustomerServiceDryRunConfig` with `provider_surface`, `dry_run_only=True`, rejecting `dry_run_only=False` — implemented.
3. `WeComCustomerServiceDryRunResult` with required fields and `delivered=False` — implemented.
4. Required validation behaviors (15 items): reject CandidateAction, reject candidate-shaped mappings, reject invalid mappings, reject non-sendable requests, reject non-wechat channel, reject missing safety, reject blocked safety, reject mismatched identity, reject wrong surface, reject missing aliases, require T233 boundary audit notes, preserve audit with deduplication, never mutate inputs — all implemented.
5. Required dry-run payload behavior: deterministic in-memory payload with provider_surface, dry_run=True, request/contact/user scope, recipient aliases only, draft text, optional safe_summary, source context, no arbitrary metadata — implemented.
6. Required test scenarios (15 items): all covered by 23 committed tests.
7. Data contract document — present and complete.
8. Worker summary — present and complete.
9. Handoff record — appended to `docs/07_handoff.md`.

Verification commands documented in the worker summary:
- `py_compile` passed.
- 23 focused T232 tests passed.
- 84 combined tests (T232 + T233 + outbound schema + send gate) passed.
- `git diff --check` passed (line-ending warnings only).
- `git status --short` shows only T232 allowed-file changes.

## Recommended Next Action

T232 is complete as a deterministic local dry-run outbound adapter for WeCom Customer Service.

Captain should:

1. Accept T232 as complete.
2. Update `docs/04_task_board.md` to mark T232 as passed.
3. Determine whether M12 is now complete at the task level. M12 has completed: T230 (research spike, Gate M12 Conditional), T231 (synthetic inbound contract), T232 (dry-run outbound adapter), T233 (provider safety gate). All M12 tasks are now complete.
4. If M12 is to be closed, write a milestone gate review documenting what M12 proves (synthetic WeCom Customer Service inbound parsing, provider safety eligibility, dry-run outbound payload preparation — all local/deterministic/no live APIs) and what remains (live credentials, callbacks, real delivery, production recipient mapping, error/retry handling).
5. If further WeCom work is desired, future tasks should remain gated by the T232/T233 boundaries and should not bypass the safety gate or dry-run adapter.
