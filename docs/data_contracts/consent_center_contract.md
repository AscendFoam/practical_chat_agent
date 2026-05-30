# Consent Center Contract

Task: T312 Consent Center Data Model
Status: worker draft for review

## Scope

Consent Center models represent local consent, withdrawal, minor/guardian state,
and data-rights request records for the companion-agent prototype. They do not
capture real consent, mutate user data, call legal services, call model
providers, enable training/fine-tuning, build UI, or integrate with platforms.

Implemented models:

- `ConsentGrantRecord`
- `ConsentWithdrawalRecord`
- `ConsentCenterState`
- `DataRightsRequestRecord`

`ConsentFeatureScope` is a literal feature-scope set used by the models.

## ConsentFeatureScope

Supported scopes:

- `memory`
- `persona_distillation`
- `proactive_messaging`
- `aigc_export_share`
- `voice_avatar`
- `analytics`
- `model_improvement`
- `payment_marketing`

Scopes are intentionally separated so users can grant or withdraw consent for
one feature without enabling unrelated data uses.

## ConsentGrantRecord

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `consent_grant_record_v1`. |
| `grant_id` | Generated local grant id. |
| `user_id` | Owner user id. |
| `feature_scope` | One `ConsentFeatureScope`. |
| `policy_version` | Policy/notice version accepted by the actor. |
| `actor_id` | User, guardian, reviewer, or system actor id. |
| `actor_type` | `user`, `guardian`, `reviewer`, or `system`. |
| `granted` | Always true. |
| `granted_at` | Grant timestamp. |
| `expires_at` | Optional expiration timestamp. |
| `evidence_refs` | Redacted consent evidence refs. |
| `review_required` | Whether the grant requires review. |

## ConsentWithdrawalRecord

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `consent_withdrawal_record_v1`. |
| `withdrawal_id` | Generated local withdrawal id. |
| `user_id` | Owner user id. |
| `feature_scope` | Withdrawn feature scope. |
| `supersedes_grant_ids` | Grant ids explicitly superseded by this withdrawal. |
| `actor_id` | Actor id. |
| `actor_type` | `user`, `guardian`, `reviewer`, or `system`. |
| `reason` | Human-readable reason. |
| `withdrawn_at` | Withdrawal timestamp. |
| `evidence_refs` | Redacted withdrawal evidence refs. |

## ConsentCenterState

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `consent_center_state_v1`. |
| `user_id` | Owner user id. |
| `grants` | Consent grants for the user. |
| `withdrawals` | Consent withdrawals for the user. |
| `is_minor` | Whether the user is represented as a minor. |
| `guardian_actor_id` | Optional guardian actor id. |
| `guardian_consent_required` | Defaults true. |
| `minor_access_allowed` | Always false in this contract. |
| `active_feature_scopes` | Derived active scopes after withdrawals. |
| `withdrawn_feature_scopes` | Derived withdrawn scopes. |
| `generated_at` | State generation timestamp. |

`ConsentCenterState.has_active_consent(scope)` is an inspection helper only. It
does not capture, mutate, send, or persist consent.

## DataRightsRequestRecord

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `data_rights_request_record_v1`. |
| `request_id` | Generated data-rights request id. |
| `user_id` | Owner user id. |
| `request_type` | `access`, `correction`, `deletion`, `export`, `withdrawal`, or `objection`. |
| `status` | `received`, `in_review`, `fulfilled`, `rejected`, or `cancelled`. |
| `actor_id` | Requesting actor id. |
| `actor_type` | `user`, `guardian`, `reviewer`, or `system`. |
| `reason` | Human-readable reason. |
| `target_scopes` | Feature scopes involved in the request. |
| `review_required` | Defaults true. |
| `submitted_at` | Submission timestamp. |
| `due_at` | Optional target due date. |
| `completed_at` | Optional completion timestamp. |
| `result_summary` | Redacted outcome summary. |
| `audit_refs` | Redacted audit refs. |

## Invariants

- Consent is feature-specific, versioned, timestamped, and actor-attributed.
- Withdrawals supersede prior grants for the same feature scope.
- Memory, persona distillation, proactive messaging, AIGC export/share,
  voice/avatar, analytics, model-improvement, and payment/marketing scopes are
  distinct.
- Minor/guardian state is represented, but minor access is not enabled by
  default.
- Data-rights requests cover access, correction, deletion, export, withdrawal,
  objection, and status tracking.
- Payloads contain no raw private chat text.
- Payloads expose no send, schedule, delivery, platform, webhook, token, or
  queue fields.

## Non-Actions

T312 does not implement:

- UI;
- APIs;
- persistence;
- real consent capture;
- legal sufficiency;
- production privacy workflows;
- data mutation;
- training/fine-tuning permission execution;
- model-provider calls;
- platform integration;
- sending or scheduling;
- web demo behavior.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_consent_center_data_model.py tests\test_proactive_consent_schema.py tests\test_delete_freeze_export_flow_contract.py -q
```

```powershell
git diff --check
```
