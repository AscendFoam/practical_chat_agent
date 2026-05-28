# Task T224: Feishu Review Card

## Task ID

T224

## Goal

Build a local, deterministic Feishu review-card renderer and synthetic card-action parser for M11 outbound review.

This task should let later human-review UX show an already-created `OutboundMessageRequest`, its gate state, and optional Feishu sandbox adapter result as an inert review artifact. It must not approve, edit, reject, send, log feedback, write memory, call Feishu, or register any callback server.

## Background

T220 created the inert `OutboundMessageRequest` contract. T221 added the deterministic `OutboundSendGate`. T222 added a local fake adapter for already-sendable requests. T223 added a Feishu sandbox adapter that prepares Feishu-shaped text payloads behind explicit approval, gate allow state, channel `feishu`, and explicit sandbox recipient mapping.

T224 is the next step because the project now needs a review-card artifact that can be inspected by a human before any later workflow applies review decisions. The card is presentation/intent data only. It is not a delivery mechanism and not an approval mechanism.

## Required Behavior

Implement a service module such as `src/practical_chat_agent/services/feishu_review_card.py` with clear, typed boundaries. Exact class/function names are up to the Worker, but the behavior must be covered by tests and documented.

Required renderer behavior:

- Accept a validated `OutboundMessageRequest` or a stable mapping that validates to one.
- Reject direct `CandidateAction` instances and candidate-shaped mappings with a deterministic blocked/invalid result.
- Render a deterministic Feishu-compatible interactive-card payload or stable local approximation, without network calls.
- Include review-safe sections for request identity, contact/user ids, channel, approval state, gate state, sendability, risk flags, audit notes, draft preview, and optional T223 Feishu sandbox result summary.
- Include action values for `approve`, `request_edit`, `reject`, and `boundary_feedback`.
- Encode every action value as inert `review_intent` data with `schema_version`, `request_id`, and `action`.
- Preserve the distinction between display preview and payload text: truncation/normalization is for card display only and must not be claimed as redaction.
- Avoid leaking forbidden recipient metadata such as `open_id`, `chat_id`, `receive_id`, `receive_id_type`, `feishu_open_id`, or `feishu_chat_id` from `OutboundMessagePayload.metadata`.
- Not mutate the input request, gate decision, sandbox result, or any store.

Required parser behavior:

- Parse a synthetic Feishu card-action mapping into a local validated review-intent object or equivalent stable mapping.
- Accept only `approve`, `request_edit`, `reject`, and `boundary_feedback`.
- Require matching `request_id` when an expected request id is supplied.
- Reject missing schema version, missing request id, unknown action, malformed action value, and cross-request action payloads deterministically.
- Return intent data only. Do not apply approval, modify `human_approval`, re-run the send gate, call adapters, write feedback logs, or write memory.

## Explicit Non-Goals

- No real Feishu API calls.
- No Feishu webhook/event callback server.
- No OAuth, bot installation, app credential, tenant token, secret, or environment-variable handling.
- No production Feishu delivery.
- No CLI send path.
- No `AppContainer` wiring.
- No scheduler, timer, background job, automation, retry loop, or runtime delivery hook.
- No automatic approval or sending.
- No mutation of `OutboundMessageRequest`, `CandidateAction`, memory records, ContactSkill, `RelationshipState`, approved stores, feedback logs, or private artifacts.
- No `private/chat_history/` reads and no committed private content.
- No WeChat, browser, desktop, notification, email, or other platform integration.

## Allowed Files

Worker may edit only:

- `src/practical_chat_agent/services/feishu_review_card.py`
- `src/practical_chat_agent/services/feishu_outbound_adapter.py` only if a tiny type/export compatibility change is needed
- `src/practical_chat_agent/core/models.py` only if a small shared enum/model is strongly justified; prefer service-local dataclasses
- `tests/test_feishu_review_card.py`
- `tests/test_feishu_outbound_adapter.py` only if needed for compatibility with the review-card result summary
- `docs/data_contracts/outbound_send_gate_contract.md`
- `docs/worker_summary/T224_worker_summary.md`
- `docs/07_handoff.md`

Do not edit `src/practical_chat_agent/app/main.py`, connector modules, runtime configuration, task board, governance docs other than `docs/07_handoff.md`, or unrelated tests.

## Test Requirements

Add focused tests that cover at least:

- Rendering a pending/non-sendable outbound request card.
- Rendering a sendable Feishu outbound request card.
- Rendering a blocked gate-state card without implying delivery.
- Rendering a card with an optional T223 Feishu sandbox result summary.
- Rejecting direct `CandidateAction` input.
- Rejecting candidate-shaped mappings.
- Ensuring card rendering does not mutate the input request.
- Ensuring card rendering does not call a Feishu transport or adapter delivery method.
- Ensuring forbidden recipient metadata keys are absent from the card output.
- Display truncation and exact-boundary behavior for long draft text.
- Deterministic action values for approve/edit/reject/boundary-feedback buttons.
- Parsing valid synthetic approve, request-edit, reject, and boundary-feedback actions.
- Rejecting malformed action payloads, missing request ids, unknown actions, and cross-request action payloads.

Tests must remain synthetic, dependency-light, network-free, credential-free, and private-content-free.

## Suggested Verification Commands

Use workspace-local temp/cache paths if pytest needs them on Windows.

```powershell
python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/outbound_send_gate.py src/practical_chat_agent/services/outbound_fake_adapter.py src/practical_chat_agent/services/feishu_outbound_adapter.py src/practical_chat_agent/services/feishu_review_card.py
pytest tests/test_outbound_message_request_schema.py tests/test_outbound_send_gate.py tests/test_outbound_fake_adapter.py tests/test_feishu_outbound_adapter.py tests/test_feishu_review_card.py -q
```

If feasible in the local environment, also run the full test suite and report any pre-existing environment-dependent failures separately from T224-targeted results.

## Deliverables

- Review-card service and parser implementation.
- Focused synthetic test coverage.
- Contract documentation update explaining card payload and review-intent semantics.
- Worker summary in `docs/worker_summary/T224_worker_summary.md`.
- Handoff update in `docs/07_handoff.md` that states T224 is complete and explicitly lists non-actions.

## Reviewer Type

adversarial
