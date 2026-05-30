# T311 Worker Summary

## Changed

- Added `docs/compliance/international_privacy_platform_policy_checklist.md`.
- Added
  `docs/tasks/M20_compliance_and_safety_baseline/T312_consent_center_data_model.md`.
- Appended the T311 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## Research Evidence

- Used official/primary sources from EUR-Lex, FTC, UK ICO, California AG/CPPA,
  Illinois General Assembly, Apple Developer, and Google Play where available.
- Included access date and source URLs in the checklist.
- Identified companion-chatbot child/teen safety, AI deception, voice/biometric
  misuse, AI transparency, and app-store policy as core international risks.

## Checklist Added

- Privacy, consent, and data rights.
- AI transparency and generated content.
- Companion, dependency, and crisis risk.
- Children and minors.
- Voice, avatar, biometrics, and synthetic media.
- Platform and app-store policy.
- Payments, monetization, and commercial claims.
- Data transfer, security, and vendors.
- Open legal/product review questions.
- Required gates before closed test.

## Explicit Non-Actions

- No legal advice, compliance completion, filing, registration, launch approval,
  app-store approval, or regulator acceptance was claimed.
- No code, tests, UI, platform integration, sending, scheduling, model-provider
  integration, or user-data processing change was added.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- T311 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Remaining Risks

- T311 is a checklist for review, not legal clearance.
- Consent Center model, AIGC labeling plan, crisis/dependency tests, UI, and web
  demo remain future work.

## Recommended Reviewer Type

Adversarial legal/product-policy review.
