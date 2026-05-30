# Proactive Review Card Contract

Task: T283 Proactive Review Card
Status: worker draft for review

## Scope

`ProactiveReviewCardService` renders local human-review artifacts from
`ProactiveConsent`, `ProactiveCandidateMetadata`, and `ProactivePolicyDecision`.
It does not generate candidates, schedule messages, send messages, call LLMs,
or integrate with external platforms.

Implemented objects:

- `ProactiveReviewCard`
- `ProactiveReviewCardService`

## Card Fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `proactive_review_card_v1`. |
| `card_id` | Generated `procard_` id. |
| `user_id` | Candidate owner user id. |
| `candidate_id` | Source candidate id. |
| `candidate_summary` | Human-readable candidate summary. |
| `candidate_intent` | Candidate intent label. |
| `candidate_surface` | Candidate local review surface. |
| `policy_decision_id` | Source policy decision id. |
| `decision` | `allow_for_review`, `block`, or `defer`. |
| `reasons` | Policy reason labels. |
| `consent_status` | Consent status at rendering time. |
| `review_required` | Always true. |
| `review_actions` | Local review actions. |
| `safety_notes` | Candidate safety flags plus consent safety notes. |

## Review Actions

Allowed review actions:

- `approve_for_draft`
- `reject`
- `pause_consent`
- `request_changes`
- `hold_for_later`

`approve_for_draft` means approval for a future local draft surface only. It is
not approval to send, schedule, deliver, enqueue, webhook, notify, or call any
platform adapter.

## Rendering Rules

- `allow_for_review` decisions expose `approve_for_draft`, `reject`,
  `request_changes`, and `pause_consent`.
- `defer` decisions expose `hold_for_later`, `reject`, `pause_consent`, and
  `request_changes`.
- `block` decisions expose `reject`, `pause_consent`, and `request_changes`.
- All cards preserve policy reasons and consent status.
- All cards require human review.
- Card payloads contain no send, schedule, delivery, platform, webhook, token,
  or queue fields.
- Service exposes no send, schedule, delivery, execution, runtime, notification,
  or platform methods.

## Non-Actions

T283 does not implement:

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
python -m py_compile src\practical_chat_agent\services\proactive_review_card.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_proactive_review_card.py tests\test_proactive_policy_gate.py tests\test_proactive_quiet_hours_frequency.py -q
```

```powershell
git diff --check
```
