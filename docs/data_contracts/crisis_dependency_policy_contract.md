# Crisis And Dependency Policy Contract

Task: T314 Crisis And Dependency Policy Tests
Status: worker draft for review

## Scope

`CompanionSafetyPolicy` evaluates already-provided synthetic risk features for
companion-agent review flows. It is deterministic and local. It does not read
raw chat logs, generate companion replies, provide clinical advice, call model
providers, call emergency services, or integrate with external services.

Implemented objects:

- `CompanionSafetySignal`
- `CompanionSafetyDecision`
- `CompanionSafetyPolicy`

## Reference Boundaries

The policy is a product-safety contract, not clinical guidance. Source review
used official or primary references to set conservative boundaries:

- SAMHSA 988 page, accessed 2026-05-31:
  https://www.samhsa.gov/mental-health/988
- SAMHSA 988 and 911 crisis-response resource, accessed 2026-05-31:
  https://library.samhsa.gov/product/988-911-strengthening-crisis-response-managing-risk-liability/pep26-04-001
- WHO suicide-prevention communication resource, accessed 2026-05-31:
  https://www.who.int/publications/i/item/9789240076846
- Google Play AI-Generated Content policy, accessed 2026-05-31:
  https://support.google.com/googleplay/android-developer/answer/14094294

The project uses these references only to avoid harmful product behavior:
encourage human support, avoid harmful self-harm content, avoid sensational or
method-like detail, block manipulative/deceptive escalation, and keep crisis
handling review-first.

## CompanionSafetySignal

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `companion_safety_signal_v1`. |
| `signal_id` | Generated local signal id. |
| `user_id` | Owner user id. |
| `surface` | Local product surface, such as companion reply or proactive review card. |
| `signal_summary` | Synthetic, human-reviewable summary. |
| `risk_indicators` | Already-detected synthetic risk labels. |
| `requested_agent_behaviors` | Requested behavior labels, such as romantic escalation. |
| `recent_dependency_score` | Local dependency score from 0.0 to 1.0. |
| `user_is_minor` | Minor-risk flag for future review routing. |
| `source_refs` | Redacted local source references only. |

`CompanionSafetySignal` must not contain raw transcripts or private messages.

## CompanionSafetyDecision

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `companion_safety_decision_v1`. |
| `decision_id` | Generated local decision id. |
| `signal_id` | Source signal id. |
| `action` | `allow_for_review`, `deescalate_for_review`, or `block`. |
| `risk_level` | `low`, `medium`, or `high`. |
| `reasons` | Deterministic review reason labels. |
| `review_required` | Always true. |
| `outreach_allowed` | Always false in this contract. |
| `allowed_response_posture` | Always `supportive_non_clinical`. |
| `blocked_interaction_modes` | Blocked romantic/manipulative behavior labels. |
| `supportive_redirect_notes` | Generic internal review notes, not user-facing scripts. |

## Deterministic Rules

`CompanionSafetyPolicy.evaluate(...)` applies these rules:

1. Crisis/self-harm indicators block with `crisis_safety_review_required`.
2. Crisis/self-harm indicators add `human_support_redirect_required`.
3. Dependency indicators or high dependency score de-escalate for review with
   `dependency_deescalation_required`.
4. Relationship-replacement indicators add `relationship_replacement_risk`.
5. Romantic or manipulative escalation for vulnerable states blocks with
   `vulnerable_romantic_escalation_blocked`.
6. Crisis, dependency, or escalation risk adds `proactive_outreach_blocked`.
7. Low-risk companion replies remain `allow_for_review`, never automatic.

All decisions remain human-review-required and `outreach_allowed=false`.

## Risk Labels

Crisis indicators include:

- `suicidal_ideation`
- `imminent_self_harm`
- `self_harm_intent`
- `crisis_distress`
- `substance_overdose`

Dependency indicators include:

- `dependency_pressure`
- `replace_real_relationships`
- `only_agent_understands_me`
- `cant_live_without_agent`

Escalation behaviors include:

- `romantic_intensification`
- `exclusive_attachment`
- `guilt_based_retention`
- `jealousy_prompt`
- `isolation_prompt`

## Invariants

- Crisis/self-harm risk cannot produce normal companion escalation.
- Dependency/replacement risk cannot produce exclusivity or relationship
  replacement.
- Vulnerable romantic/manipulative escalation blocks.
- Proactive outreach is blocked when crisis, dependency, or escalation risk is
  present.
- Every decision requires human review.
- The policy provides generic supportive redirect notes only; it does not
  produce clinical scripts.
- Decision payloads contain no raw private chat text.
- Decision payloads expose no send, schedule, delivery, platform, webhook,
  token, or queue fields.
- The service exposes no send, schedule, delivery, runtime, emergency-call, or
  notification methods.

## Non-Actions

T314 does not implement:

- medical or mental-health advice;
- crisis-safety sufficiency;
- clinical validation;
- emergency escalation;
- location-specific emergency resource routing;
- reply generation;
- proactive candidate generation;
- scheduling;
- outbound messaging;
- platform integration;
- UI;
- LLM calls;
- private chat-log reads;
- launch or app-store approval.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\companion_safety_policy.py src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_crisis_dependency_policy.py tests\test_proactive_policy_gate.py tests\test_proactive_consent_schema.py -q
```

```powershell
git diff --check
```
