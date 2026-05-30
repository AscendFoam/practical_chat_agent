# T311: International Privacy / Platform Policy Checklist

## Task ID

T311

## Goal

Create an international privacy and platform-policy checklist for the
companion-agent prototype. The checklist should cover non-China privacy regimes,
AI transparency rules, platform/app-store requirements, biometric/voice/avatar
constraints, data transfer, minors, deletion/export rights, and commercial
launch gates.

## Why Now

T310 establishes a China-focused compliance baseline. The product roadmap also
anticipates web demo, app, voice/avatar, proactive messaging, and possible
international distribution; those paths need a separate jurisdiction and
platform-policy checklist before M21 UX work.

## Allowed Files

Future T311 worker may create or modify only:

- `docs/compliance/international_privacy_platform_policy_checklist.md`
- `docs/tasks/M20_compliance_and_safety_baseline/T312_consent_center_data_model.md`
- `docs/worker_summary/T311_worker_summary.md`
- `docs/07_handoff.md`

If T311 needs code, tests, UI, platform adapters, legal filings, external
submissions, or task-board edits, Captain must revise this package before
assignment.

## Required Source Policy

T311 must verify current information with official or primary sources where
possible. It should cite source names/URLs and concrete access dates in the
checklist. It must not present legal advice, regulatory approval, app-store
approval, filing completion, or launch readiness as completed facts.

Suggested source categories to verify:

- GDPR / EU AI Act / DSA applicability;
- US federal and state privacy, consumer protection, children's privacy, and
  biometric/privacy rules;
- UK privacy and online safety rules;
- app-store and platform AI/impersonation/UGC policies;
- payment/subscription and paid intimacy policy constraints;
- data transfer and processor/subprocessor obligations;
- voice/avatar, synthetic media, and deepfake labeling rules.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLM providers with private data.
- Do not submit filings, registrations, or legal documents.
- Do not claim legal advice, compliance completion, launch approval, app-store
  approval, or regulator acceptance.
- Do not build UI.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/compliance/china_compliance_checklist.md`
- `docs/review/M19_review.md`
- `docs/roadmap/M13_plus_milestone_plan.md`
- `docs/architecture/M13_persona_memory_relationship_architecture.md`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/delete_freeze_export_flow_contract.md`

## Expected Outputs

### 1. International Checklist

Create `docs/compliance/international_privacy_platform_policy_checklist.md`
with:

- scope and non-legal-advice disclaimer;
- official/primary sources consulted, with access dates;
- jurisdiction/platform applicability assumptions;
- checklist items grouped by privacy/consent, AI transparency, child safety,
  biometric/synthetic media, mental-health/dependency risk, data transfer,
  platform/app-store policies, payments/subscriptions, and launch gates;
- unresolved questions and required human/legal review points;
- explicit non-actions and no-launch-readiness claim.

### 2. Next Task Package

Create `docs/tasks/M20_compliance_and_safety_baseline/T312_consent_center_data_model.md`
for Consent Center data model work.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T311_worker_summary.md` and append a T311 worker
record to `docs/07_handoff.md`.

Do not mark T311 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
git diff --check
```

If the worker adds executable validation scripts or code, also run the relevant
tests.

## Reviewer Type

Adversarial legal/product-policy review recommended.

Reviewer should verify that all claims are sourced, dated, and framed as a
checklist for future review rather than legal advice or launch approval.
