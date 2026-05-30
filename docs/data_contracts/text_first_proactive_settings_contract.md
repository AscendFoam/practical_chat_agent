# Text-First Proactive Settings Contract

Task: T324 Proactive Settings Prototype
Status: worker draft for review

## Scope

`TextFirstProactiveSettingsPrototype` projects `ProactiveConsent`,
`ProactivePolicyDecision`, and optional `CompanionSafetyDecision` metadata into
a reviewable proactive settings state. It is local and deterministic.

It does not generate proactive candidates, mutate consent, schedule work, send
messages, notify users, call model providers, or integrate with external
platforms.

Implemented objects:

- `TextFirstProactiveSettingsRequest`
- `TextFirstProactiveSettingsState`
- `TextFirstProactiveSettingsPrototype`

Implementation entry point:

- `practical_chat_agent.ui.text_first_proactive_settings.TextFirstProactiveSettingsPrototype`

## TextFirstProactiveSettingsRequest

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `text_first_proactive_settings_request_v1`. |
| `user_id` | Owner user id. |
| `consent` | Existing `ProactiveConsent`. |
| `policy_decision` | Optional `ProactivePolicyDecision`. |
| `safety_decision` | Optional `CompanionSafetyDecision`. |

## TextFirstProactiveSettingsState

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `text_first_proactive_settings_state_v1`. |
| `state_id` | Generated local settings state id. |
| `user_id` | Owner user id. |
| `screen` | Consent/policy/safety settings state. |
| `consent_status` | `disabled`, `enabled`, `paused`, or `revoked`. |
| `allowed_surfaces` | Local review surfaces from consent. |
| `allowed_intents` | Low-pressure intents from consent. |
| `quiet_hours_timezone` | Quiet-hours timezone. |
| `quiet_hours_start` | Optional quiet-hours start. |
| `quiet_hours_end` | Optional quiet-hours end. |
| `max_suggestions_per_day` | Daily cap from consent. |
| `min_interval_hours` | Minimum interval from consent. |
| `policy_reasons` | Proactive policy reasons. |
| `safety_reasons` | Crisis/dependency safety reasons. |
| `allowed_review_surface` | Set only for allow-for-review policy decisions. |
| `outreach_allowed` | Always false in this contract. |
| `has_pending_action` | Always false in this contract. |
| `review_required` | Always true. |

## State Rules

- Disabled consent -> `proactive_disabled`.
- Paused consent -> `proactive_paused`.
- Revoked consent -> `proactive_revoked`.
- Enabled consent without candidate decision -> `proactive_enabled_review`.
- Policy allow-for-review -> `proactive_allowed_for_review`.
- Policy defer -> `proactive_deferred`.
- Policy block -> `proactive_blocked`.
- Crisis/dependency block or de-escalation -> `proactive_blocked`.

All states keep `outreach_allowed=false` and `has_pending_action=false`.

## Invariants

- Consent state is always visible.
- Enabled consent surfaces and intents remain local/review-only.
- Quiet hours, frequency cap, and minimum interval are visible.
- Policy decisions are reflected without implying any action occurred.
- Crisis/dependency reasons override allow/defer and block proactive outreach.
- Every state requires human review.
- Payloads contain no raw private chat text.
- Payloads expose no send, schedule, delivery, platform, webhook, token, or
  queue fields.
- The prototype exposes no candidate-generation, send, schedule, delivery,
  execution, runtime, or notification methods.

## Non-Actions

T324 does not implement:

- frontend code;
- browser demo;
- proactive candidate generation;
- candidate ranking;
- consent mutation;
- persistence;
- LLM calls;
- private chat-log reads;
- scheduling;
- automatic sending;
- notifications;
- webhooks;
- platform integration;
- voice/avatar/video behavior;
- Live2D behavior;
- legal, clinical, app-store, or launch approval.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_proactive_settings.py src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_proactive_settings_prototype.py tests\test_proactive_consent_schema.py tests\test_proactive_policy_gate.py tests\test_crisis_dependency_policy.py -q
```

```powershell
git diff --check
```
