# M20 Review: Compliance And Safety Baseline

## Status

Gate recommendation: PASS_WITH_WARNINGS for entering M21 text-first product UX
prototype work.

M20 established a local, review-first compliance and safety baseline for
commercial companion-agent exploration. It did not implement UI, real consent
capture, legal filings, app-store review, clinical crisis handling, emergency
escalation, platform integration, realtime delivery, sending, scheduling,
voice/avatar runtime behavior, Live2D, export/share writing, or launch
readiness.

## Task Coverage

| Task | Result | Evidence |
| --- | --- | --- |
| T310 China compliance checklist | Implemented | Official-source checklist for privacy, AIGC labeling, anthropomorphic interaction, minors, deletion/export, security, and closed-test gates. |
| T311 International privacy/platform checklist | Implemented | Official/primary-source checklist for privacy, AI transparency, companion risk, children/minors, voice/avatar/biometrics, app-store policy, payments, data transfer, and vendor controls. |
| T312 Consent Center data model | Implemented | Local consent, withdrawal, minor/guardian, and data-rights models; `tests/test_consent_center_data_model.py`. |
| T313 AIGC labeling plan | Implemented | AIGC labeling plan, reusable labeling requirement model, metadata-label rules; `tests/test_aigc_labeling_plan_contract.py`. |
| T314 Crisis/dependency policy tests | Implemented | Deterministic local crisis/dependency policy; `tests/test_crisis_dependency_policy.py`. |

## Implemented Code

- `src/practical_chat_agent/core/models.py`
  - `ConsentGrantRecord`
  - `ConsentWithdrawalRecord`
  - `ConsentCenterState`
  - `DataRightsRequestRecord`
  - `AIGCLabelingRequirement`
  - `AIGCContentModality`
  - `AIGCProductSurface`
- `src/practical_chat_agent/services/companion_safety_policy.py`
  - `CompanionSafetySignal`
  - `CompanionSafetyDecision`
  - `CompanionSafetyPolicy`

## Compliance And Safety Documents

- `docs/compliance/china_compliance_checklist.md`
- `docs/compliance/international_privacy_platform_policy_checklist.md`
- `docs/compliance/aigc_labeling_plan.md`

## Data Contracts

- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`

## Verification Evidence

Fresh T315 verification command:

```text
$env:PYTHONPATH='src'
pytest tests\test_consent_center_data_model.py tests\test_aigc_labeling_plan_contract.py tests\test_crisis_dependency_policy.py tests\test_proactive_policy_gate.py tests\test_proactive_consent_schema.py -q -o cache_dir=artifacts\t315_pytest_cache_final --basetemp=artifacts\t315_pytest_basetemp_final
```

Result: passed, `31 passed`.

Fresh diff check:

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

Additional worker-level evidence is recorded in:

- `docs/worker_summary/T310_worker_summary.md`
- `docs/worker_summary/T311_worker_summary.md`
- `docs/worker_summary/T312_worker_summary.md`
- `docs/worker_summary/T313_worker_summary.md`
- `docs/worker_summary/T314_worker_summary.md`

## Safety And Compliance Boundary Assessment

M20 is safe to use as a local prototype baseline because:

- China and international checklists cite official/primary sources and clearly
  avoid legal-sufficiency claims.
- consent records are feature-specific, versioned, actor-attributed, and
  reviewable;
- withdrawals supersede prior grants for the same feature scope;
- minor/guardian state is represented without enabling minor access by default;
- data-rights records cover access, correction, deletion, export, withdrawal,
  objection, and status tracking;
- generated/synthetic content receives visible labels;
- virtual history and role dynamic posts preserve imagined/not-real-world
  labels;
- export/share/media surfaces require implicit metadata labels before future
  copy/download/export/share behavior;
- crisis/self-harm indicators block normal companion behavior and require
  review;
- dependency/replacement risk de-escalates for review;
- vulnerable romantic/manipulative escalation blocks;
- proactive outreach remains blocked under crisis/dependency/escalation risk;
- tests check that key decision payloads do not expose raw private chat text or
  delivery/platform fields.

## Explicit Non-Actions

M20 did not implement:

- legal advice or legal sufficiency;
- regulator filing or approval;
- app-store approval;
- clinical validation;
- crisis-safety sufficiency;
- emergency escalation;
- location-specific emergency routing;
- real consent capture;
- production privacy workflow;
- authentication/access control;
- UI or web demo;
- export/share/download writing;
- watermarking or file metadata insertion;
- model-provider calls;
- private chat-log reads;
- persona distillation runtime changes;
- voice/avatar/deepfake behavior;
- Live2D behavior;
- automatic sending, scheduling, delivery, notifications, webhooks, queues, or
  platform adapters.

## Residual Risks

- M20 is a compliance/safety baseline, not legal clearance.
- Crisis/dependency policy is deterministic and conservative, but not clinical
  crisis handling.
- Consent Center contracts are local models, not production consent capture or
  data-rights fulfillment.
- AIGC labeling is a local contract and plan, not watermarking, file metadata,
  or platform publishing.
- No end-to-end user-facing UX consumes these artifacts yet.
- M21 must preserve AI identity disclosure, consent boundaries, AIGC labels,
  control-surface visibility, and crisis/dependency blocks in every prototype
  surface.

## M21 Entry Recommendation

Proceed to M21 with T320 UX information architecture. T320 should define the
text-first product navigation, states, and review-first UX contract before any
screen implementation. It must include persona creation, chat, memory
explanation, virtual life stream, proactive settings, consent/data controls,
AIGC labels, and crisis/dependency safety states.

## Reviewer Recommendation

Reviewer should mark M20 as PASS_WITH_WARNINGS if the fresh tests pass and diff
check is clean. Reviewer should BLOCK only if a later diff claims legal
sufficiency, clinical safety, platform approval, real consent capture,
emergency escalation, automatic sending, UI launch readiness, public deployment
readiness, or raw private-content exposure.
