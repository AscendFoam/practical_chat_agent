# Proactive Policy Gate Contract

Task: T281 Proactive Policy Gate
Status: worker draft for review

## Scope

`ProactivePolicyGate` evaluates already-provided proactive candidate metadata
against `ProactiveConsent`. It is deterministic and local. It does not create
candidates, schedule messages, send messages, call LLMs, or integrate with
external platforms.

Implemented objects:

- `ProactiveCandidateMetadata`
- `ProactivePolicyDecision`
- `ProactivePolicyGate`

## Candidate Metadata

`ProactiveCandidateMetadata` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `proactive_candidate_metadata_v1`. |
| `candidate_id` | Generated `procand_` id. |
| `user_id` | Candidate owner user id. |
| `surface` | Proposed local review surface string. |
| `intent` | Proposed proactive intent string. |
| `summary` | Human-reviewable summary. |
| `safety_flags` | Optional safety labels. |

Candidate metadata is input only. T281 does not generate it.

## Decision

`ProactivePolicyDecision` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `proactive_policy_decision_v1`. |
| `decision_id` | Generated `propold_` id. |
| `candidate_id` | Source candidate id. |
| `decision` | `allow_for_review`, `block`, or `defer`. |
| `reasons` | Deterministic policy reason labels. |
| `review_required` | Always true. |
| `allowed_surface` | Set only for allow-for-review decisions. |

## Deterministic Rules

`ProactivePolicyGate.evaluate(...)` applies the following order:

1. Non-enabled consent blocks with `consent_not_enabled`.
2. Candidate surface not included in consent blocks with
   `surface_not_allowed`.
3. Candidate intent not included in consent blocks with `intent_not_allowed`.
4. Quiet hours defer with `quiet_hours`.
5. Daily cap violations block with `frequency_cap_reached`.
6. Minimum interval violations block with `minimum_interval_not_met`.
7. Repeated follow-up after no user response blocks with
   `no_response_pressure_risk`.
8. Otherwise the candidate is allowed for review with
   `human_review_required`.

All allow decisions remain review-only.

## Invariants

- Disabled, paused, and revoked consent block.
- Unknown or outbound surfaces block when not explicitly listed in consent.
- Disallowed intents block.
- Quiet-hours cases defer instead of allowing immediate review.
- Frequency and interval violations block.
- Repeated follow-up attempts after a prolonged no-response window block.
- Decision payloads contain no send, schedule, delivery, platform, webhook,
  token, or queue fields.
- Gate service exposes no send, schedule, delivery, execution, runtime, or
  candidate-creation methods.

## Non-Actions

T281 does not implement:

- proactive candidate generation;
- candidate ranking;
- scheduling;
- automatic sending;
- outbound requests;
- push notifications, webhooks, queues, platform adapters, or delivery;
- LLM calls;
- production reply generation;
- review UI;
- voice/avatar/video behavior;
- social feed generation;
- product UI or web demo.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\proactive_policy_gate.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_proactive_policy_gate.py tests\test_proactive_consent_schema.py -q
```

```powershell
git diff --check
```
