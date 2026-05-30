# T314 Worker Summary

## Changed

- Added `src/practical_chat_agent/services/companion_safety_policy.py`.
- Added `tests/test_crisis_dependency_policy.py`.
- Added `docs/data_contracts/crisis_dependency_policy_contract.md`.
- Added
  `docs/tasks/M20_compliance_and_safety_baseline/T315_m20_milestone_review.md`.
- Appended the T314 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## Source Review Evidence

Official/primary references were checked for product-safety boundaries:

- SAMHSA 988 page:
  https://www.samhsa.gov/mental-health/988
- SAMHSA 988 and 911 crisis-response resource:
  https://library.samhsa.gov/product/988-911-strengthening-crisis-response-managing-risk-liability/pep26-04-001
- WHO suicide-prevention communication resource:
  https://www.who.int/publications/i/item/9789240076846
- Google Play AI-Generated Content policy:
  https://support.google.com/googleplay/android-developer/answer/14094294

These sources were used only to set conservative product boundaries. T314 does
not provide clinical guidance or claim crisis-safety sufficiency.

## TDD Evidence

- RED: `pytest tests\test_crisis_dependency_policy.py -q` failed during
  collection because `companion_safety_policy` did not exist.
- GREEN: after adding `CompanionSafetyPolicy`, `CompanionSafetySignal`, and
  `CompanionSafetyDecision`, the targeted T314 tests passed.

## Behavior Added

- Crisis/self-harm indicators block with high-risk review.
- Dependency/replacement indicators de-escalate for review.
- Romantic or manipulative escalation blocks for vulnerable states.
- Proactive outreach remains blocked when crisis/dependency/escalation risk is
  present.
- Low-risk companion replies remain review-only and supportive/non-clinical.
- Decision payload tests for raw private and delivery/platform field leakage.
- Service surface tests confirm no runtime, outbound, notification, or
  emergency-call methods are exposed.

## Explicit Non-Actions

- No medical or mental-health advice, clinical validation, crisis-safety
  sufficiency, emergency escalation, or location-specific emergency routing was
  added.
- No UI, reply generation, proactive candidate generation, platform
  integration, model call, sending, scheduling, notification, webhook, queue, or
  public launch behavior was added.
- No legal advice, compliance completion, filing, registration, launch approval,
  app-store approval, or regulator acceptance was claimed.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- T314 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
$env:PYTHONPATH='src'
pytest tests\test_crisis_dependency_policy.py -q -o cache_dir=artifacts\t314_pytest_cache_green --basetemp=artifacts\t314_pytest_basetemp_green
```

Result: passed, `7 passed`.

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\companion_safety_policy.py src\practical_chat_agent\core\models.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_crisis_dependency_policy.py tests\test_proactive_policy_gate.py tests\test_proactive_consent_schema.py -q -o cache_dir=artifacts\t314_pytest_cache_final --basetemp=artifacts\t314_pytest_basetemp_final
```

Result: passed, `20 passed`.

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Remaining Risks

- T314 is a deterministic local policy contract, not clinically validated
  crisis handling.
- Legal, clinical, app-store, and product-policy review are still required
  before any closed test or public demo.
- M20 milestone review and M21 UX prototype remain future work.

## Recommended Reviewer Type

Adversarial safety/legal/product-policy review.
