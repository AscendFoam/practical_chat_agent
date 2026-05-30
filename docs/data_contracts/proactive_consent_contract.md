# Proactive Consent Contract

Task: T280 Proactive Consent Schema
Status: worker draft for review

## Scope

`ProactiveConsent` defines explicit, review-first permissions for future
proactive companion suggestions. It is schema-only. It does not generate
proactive candidates, schedule messages, send messages, call LLMs, or integrate
with external platforms.

Implemented models:

- `ProactiveQuietHours`
- `ProactiveConsent`

## Consent Fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `proactive_consent_v1`. |
| `consent_id` | Generated `proconsent_` id. |
| `user_id` | Owner user id. |
| `status` | `disabled`, `enabled`, `paused`, or `revoked`. |
| `allowed_surfaces` | Local review surfaces only. |
| `allowed_intents` | Low-pressure proactive intent labels only. |
| `quiet_hours` | Timezone plus optional start/end local quiet-hour strings. |
| `max_suggestions_per_day` | Non-negative cap, currently at most 3. |
| `min_interval_hours` | Non-negative minimum interval. |
| `requires_human_review` | Must remain true. |
| `pause_reasons` | Human-readable pause reasons. |
| `revoked_at` | Required when `status=revoked`. |
| `safety_notes` | Review notes or safety labels. |

## Allowed Local Surfaces

- `in_app_review_card`
- `local_sandbox_preview`

Outbound surfaces such as WeChat, Feishu, push notification, SMS, email, and
webhook are not allowed by the schema.

## Allowed Low-Pressure Intents

- `gentle_check_in`
- `memory_follow_up`
- `care_routine`
- `shared_interest`
- `relationship_repair_note`

Retention, dependency, sales, pressure, or engagement-manipulation intent names
are not part of the allowed literal set.

## Invariants

- Enabled consent requires at least one local review surface.
- Enabled consent requires at least one low-pressure intent.
- `requires_human_review=false` is rejected.
- Negative frequency caps and intervals are rejected.
- Revoked consent requires `revoked_at`.
- Paused and revoked consent states are representable without enabling runtime
  behavior.
- Serialized consent contains no send, schedule, delivery, platform, webhook,
  token, or queue fields.

## Non-Actions

T280 does not implement:

- proactive candidate generation;
- candidate ranking;
- scheduling;
- automatic sending;
- outbound requests;
- push notification, webhook, platform, or adapter behavior;
- LLM calls;
- production reply generation;
- voice/avatar/video behavior;
- social feed generation;
- product UI or web demo.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_proactive_consent_schema.py -q
```

```powershell
git diff --check
```
