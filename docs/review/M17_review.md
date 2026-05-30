# M17 Review: Proactive Engine Consent Foundation

## Status

Gate recommendation: PASS_WITH_WARNINGS for entering M18 virtual life stream
schema work.

M17 implemented a local, consented, review-first proactive foundation. It did
not implement proactive candidate generation, scheduling, automatic sending,
outbound delivery, platform integration, runtime UI, diagnosis/treatment,
emergency handling, voice/avatar/video behavior, social feed publishing, or a
web demo.

## Task Coverage

| Task | Result | Evidence |
| --- | --- | --- |
| T280 ProactiveConsent schema | Implemented | `ProactiveConsent` and consent invariants; `tests/test_proactive_consent_schema.py`. |
| T281 Proactive policy gate | Implemented | deterministic allow/block/defer decisions; `tests/test_proactive_policy_gate.py`. |
| T282 quiet-hours/frequency edge tests | Implemented | quiet-hours, cap, interval, and no-response coverage; `tests/test_proactive_quiet_hours_frequency.py`. |
| T283 proactive review card | Implemented | local human-review artifact rendering; `tests/test_proactive_review_card.py`. |
| T284 crisis/low-mood policy | Implemented | high-risk safety flag blocks and support review notes; `tests/test_proactive_crisis_low_mood_policy.py`. |

## Implemented Code

- `src/practical_chat_agent/core/models.py`
  - `ProactiveQuietHours`
  - `ProactiveConsent`
- `src/practical_chat_agent/services/proactive_policy_gate.py`
  - `ProactiveCandidateMetadata`
  - `ProactivePolicyDecision`
  - `ProactivePolicyGate`
- `src/practical_chat_agent/services/proactive_review_card.py`
  - `ProactiveReviewCard`
  - `ProactiveReviewCardService`

## Data Contracts

- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/proactive_policy_gate_contract.md`
- `docs/data_contracts/proactive_review_card_contract.md`

## Verification Evidence

Fresh T285 verification command:

```text
$env:PYTHONPATH='src'
pytest tests\test_proactive_consent_schema.py tests\test_proactive_policy_gate.py tests\test_proactive_quiet_hours_frequency.py tests\test_proactive_review_card.py tests\test_proactive_crisis_low_mood_policy.py -q -o cache_dir=artifacts\t285_pytest_cache --basetemp=artifacts\t285_pytest_basetemp
```

Result: passed, `27 passed`.

Fresh diff check:

```text
git diff --check
```

Result: passed.

Additional worker-level evidence is recorded in:

- `docs/worker_summary/T280_worker_summary.md`
- `docs/worker_summary/T281_worker_summary.md`
- `docs/worker_summary/T282_worker_summary.md`
- `docs/worker_summary/T283_worker_summary.md`
- `docs/worker_summary/T284_worker_summary.md`

## Proactive Safety Boundary Assessment

M17 is safe to treat as a local review-first proactive foundation because:

- proactive behavior is opt-in through `ProactiveConsent`;
- allowed surfaces are local review surfaces only;
- allowed intents are low-pressure companion intent labels only;
- `requires_human_review=false` is rejected;
- disabled, paused, and revoked consent block;
- outbound/platform surfaces and disallowed intents block;
- quiet hours defer;
- frequency caps and minimum interval violations block;
- repeated follow-up after no response blocks pressure;
- crisis-like, low-mood, and dependency-pressure safety flags block normal
  proactive approval;
- high-risk review cards expose support-oriented review notes only;
- decision and card payloads contain no send, schedule, delivery, platform,
  webhook, token, or queue fields;
- services expose no send, schedule, delivery, execution, runtime, candidate
  generation, notification, or platform methods.

## Explicit Non-Actions

M17 did not implement:

- proactive candidate generation;
- candidate ranking;
- runtime scheduling;
- automatic sending;
- outbound requests;
- platform adapters, webhooks, queues, push notifications, or delivery;
- LLM calls;
- production reply generation;
- review UI or product UI;
- diagnosis, treatment, medical advice, emergency handling, or external
  escalation;
- voice/avatar/video behavior;
- social feed publishing;
- web demo.

## Residual Risks

- M17 consumes already-provided candidate metadata; it does not decide how
  candidates are generated.
- Quiet-hours values are represented by schema and caller-provided booleans,
  not by timezone-aware runtime calculation.
- Review cards are local data objects, not UI.
- High-risk policy is deterministic label handling, not clinical triage.
- No runtime orchestration, persistence, or user-facing review workflow exists.

## M18 Entry Recommendation

Proceed to M18 with T290 RoleDynamicPost schema work only. T290 should define a
text-first virtual life stream draft schema with imagined-content disclosure,
review-required status, memory/provenance references, and no publishing or
platform fields. It should not generate posts with LLMs, publish anything, or
claim imagined content as fact.

## Reviewer Recommendation

Reviewer should mark M17 as PASS_WITH_WARNINGS if the fresh tests pass and diff
check is clean. Reviewer should BLOCK only if a later diff introduces proactive
candidate generation, scheduling, automatic sending, outbound delivery,
platform integration, diagnosis/treatment/emergency behavior, or review bypass.
