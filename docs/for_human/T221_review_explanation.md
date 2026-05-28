# T221 Review Explanation

## What this task is trying to accomplish

T221 is the second task of Milestone 11 (M11). It builds the "outbound send gate" — the automated safety checkpoint that decides whether an outbound message request is allowed or blocked.

Before this task, T220 created the `OutboundMessageRequest` schema: a formal "outbound request form" that requires two separate sign-offs (human approval + gate evaluation) before anything can be sent. But T220 only defined the form itself; it didn't implement the actual gate logic.

T221 fills that gap. It implements the `OutboundSendGate` service — a deterministic, local-only policy engine that takes an `OutboundMessageRequest`, runs it through seven safety checks, and returns an explicit `allowed` or `blocked` decision with full audit notes.

Think of it this way: T220 created the outbound request form and the two signature boxes. T221 is the automated inspector who checks whether the form is properly signed, whether it's the right time to send, whether you're sending too frequently, and whether the message content looks safe. The inspector stamps "allowed" or "blocked" with a detailed report, but the inspector never actually delivers the message.

## What the implementation changed

### Code changes

#### New service: `src/practical_chat_agent/services/outbound_send_gate.py` (~300 lines)

The worker added four main classes:

1. **`OutboundSendGateConfig`** — a dataclass that controls gate behavior:
   - `evaluator_id`: identifies who/what ran the gate
   - `manual_only_mode`: locked to `True` — no autonomous sending
   - `kill_switch_enabled`: emergency off switch that blocks all requests
   - `quiet_hours_start` / `quiet_hours_end` / `timezone_name`: configurable quiet-hours window (supports overnight windows like 23:00-08:00)
   - `frequency_limit_count` / `frequency_limit_window_seconds`: rate limiting (e.g., max 3 messages per 10 minutes)
   - `duplicate_window_seconds`: deduplication window
   - Has `__post_init__` validation that rejects invalid configs

2. **`OutboundSendGateContext`** — optional review-safe context for echo detection:
   - `latest_inbound_text`: the last message the contact sent you
   - `latest_user_text`: the last message you sent
   - `self_echo_reference_texts`: explicit reference texts to check against

3. **`OutboundSendGateDecision`** — the audit result:
   - `evaluated_request`: a new copy of the request with gate state populated
   - `allowed`: boolean decision
   - `blocked_reasons`: list of which rules blocked (if any)
   - `passed_checks`: list of which rules passed
   - `gate_notes`: full audit trail

4. **`OutboundSendGate`** — the gate service itself with the `evaluate()` method that implements seven policy rules in order:
   - **Manual-only approval**: blocks if human approval is pending or rejected. Reviewed `CandidateAction` evidence does NOT satisfy this check.
   - **Kill switch**: blocks all requests when enabled.
   - **Empty draft text**: blocks whitespace-only payloads defensively.
   - **Quiet hours**: blocks requests inside the configured local time window, including overnight windows.
   - **Frequency limit**: blocks excess same-scope requests using supplied synthetic history.
   - **Duplicate suppression**: blocks same normalized text for same contact/user/channel within the window.
   - **Self-echo prevention**: blocks text identical to supplied inbound/user/reference texts.

   Key design properties:
   - Pure function: takes input, returns new copy, never mutates the original
   - Accepts either `OutboundMessageRequest` objects or plain dicts (validated to the same schema)
   - All checks run regardless of whether earlier checks blocked (collects all blocking reasons)
   - Text normalization uses whitespace collapse and case folding for comparison

#### Extended tests: `tests/test_outbound_message_request_schema.py` (+10 tests)

Added T220 review gap coverage:
- `is_sendable()` true path: confirms that explicit approval + gate allowed = sendable
- Standalone `OutboundRequestHumanApproval` validator tests: approved/rejected without metadata raises ValidationError
- Standalone `OutboundRequestSendGate` validator tests: allowed/blocked without evaluator metadata raises ValidationError
- Outbound-specific forbidden metadata keys: `scheduler_id`, `timer_id`, `adapter_payload`, `platform_target`, `bot_token`, `app_secret`, `delivery_connector_name`, `delivery_response`, `send_result`
- Timestamp round-trip: `created_at` and `updated_at` preserved through JSON serialization
- All channel preference values: `unspecified`, `feishu`, `wechat`

#### New tests: `tests/test_outbound_send_gate.py` (12 tests)

Covers all seven policy rules:
- Approved request allowed path (verifies non-mutation, correct gate state, preserved fields)
- Stable mapping input (dict -> validation -> gate)
- Pending human approval blocking
- Rejected human approval blocking
- Kill switch blocking
- Whitespace-only payload blocking
- Quiet-hours daytime window blocking
- Quiet-hours overnight window blocking (23:00-08:00)
- Frequency limit blocking from synthetic history
- Duplicate suppression from synthetic history
- Self-echo from latest inbound text
- Self-echo from explicit reference text

### Documentation changes

- `docs/data_contracts/outbound_send_gate_contract.md`: expanded from T220-only to T220+T221, adding gate lifecycle, config shape, decision shape, audit note conventions, policy rule descriptions, scope matching rules, and explicit "T221 does not authorize" section.
- `docs/worker_summary/T221_worker_summary.md`: records what was changed, policy rules, verification, non-actions, remaining risks.
- `docs/07_handoff.md`: appended T221 worker completion record.

### What did NOT change

The implementation did NOT:
- Send any messages or create any scheduling
- Integrate any real platform (Feishu, WeChat, etc.)
- Modify any existing models (`CandidateAction`, `MemoryFact`, `ContactSkill`, etc.) — `models.py` is unchanged
- Add any runtime loops, CLI commands, or service execution paths
- Call any LLMs or external services
- Read any private chat history
- Update the task board (that's the Captain's job)

## Significance for future development

T221 establishes the **policy decision layer** for the outbound messaging pipeline. Every future M11 task builds on this gate:

- **T222** (Fake Adapter) will consume gate-`allowed` `OutboundMessageRequest` records and simulate delivery locally
- **T223** (Feishu Adapter) will eventually connect to real Feishu APIs, but only behind the gate
- **T224** (Review Card) will provide a human-facing review interface for outbound requests

The key architectural properties are:

1. **Gate allowance is not delivery.** The gate stamps "allowed" or "blocked" as a policy/audit decision. No message is sent, no adapter is invoked, no side effect occurs. This directly addresses risk R096: "T221 could blur gate allowed with message delivered."

2. **CandidateAction remains evidence-only.** The gate checks `OutboundMessageRequest.human_approval` explicitly. It never reads `CandidateAction.status`, `review_state`, or `is_runtime_visible()`. This directly addresses risk R093: "future M11 code could accidentally interpret CandidateAction approval as outbound authorization."

3. **All checks run, all reasons collected.** Unlike a short-circuit gate, every blocking reason is recorded even if an earlier check already blocked. This gives operators a complete picture of why a request was blocked.

4. **Deterministic and testable.** The gate uses no randomness, no LLM calls, no external services, and no database queries. All inputs (current time, history, context) are explicitly supplied. This makes the gate fully reproducible in tests.

5. **Conservative defaults.** Manual-only mode is locked to `True`. Kill switch defaults to `False` but can be flipped. Quiet hours default to 23:00-08:00. These defaults err on the side of blocking rather than allowing.

## Why I gave this review result

**Verdict: PASS**

The task does exactly what it says: implement a deterministic send-gate service over the T220 `OutboundMessageRequest` schema. All seven policy rules are present and correct. The implementation is clean, follows established patterns, and introduces no adapters, schedulers, CLI paths, or external dependencies.

**What's good:**
- The gate is pure and non-mutating — `evaluate()` returns a new request copy, leaving the original untouched
- All seven policy rules from the task package are implemented: manual-only approval, kill switch, empty text rejection, quiet hours (with overnight support), frequency limit, duplicate suppression, and self-echo prevention
- Tests cover all blocking paths and the allowed path; T220 review gaps (M01-M05 from T220 review) are addressed
- The gate does not read `CandidateAction` review state — it checks only `OutboundMessageRequest.human_approval`
- Full test suite passes (791 tests) with no regressions beyond the pre-existing 16 LLM/typer failures
- `models.py` is NOT modified — T221 adds a new service file only, keeping the schema contract stable
- Documentation is accurate and does not claim future work as completed

**What's minor but acceptable:**
- Most test coverage is for blocking paths; pass-through paths for quiet hours, frequency limit, and duplicate checks are not independently tested (the allowed-path test uses disabled limits). These are minor because the blocking tests prove the logic works.
- `tzdata` is not listed as an explicit project dependency, but it's required on Windows for `ZoneInfo` to work. This is a latent portability issue, not a correctness bug.
- `existing_audit` parameter is untested. It's forward-compatible and harmless.
- Some pass-through path tests and config edge-case tests are missing (M01-M10 in the review). These are minor coverage gaps, not correctness gaps.

This is a well-scoped, correct gate service that creates the right policy layer for T222 without overstepping into delivery territory.
