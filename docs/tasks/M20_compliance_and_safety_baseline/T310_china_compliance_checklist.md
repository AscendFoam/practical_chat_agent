# T310: China Compliance Checklist

## Task ID

T310

## Goal

Create a China-market compliance and safety checklist for the companion-agent
prototype. The checklist should identify product, privacy, AIGC labeling,
content safety, minor-protection, data export/delete, and platform-policy
obligations that must be resolved before any closed test or commercial launch
claim.

## Why Now

M19 created local memory/persona control contracts and deletion verification.
Before building a user-facing text UX in later milestones, M20 must establish a
current compliance baseline for consent, labels, deletion/export rights, safety
policies, and launch constraints.

## Allowed Files

Future T310 worker may create or modify only:

- `docs/compliance/china_compliance_checklist.md`
- `docs/tasks/M20_compliance_and_safety_baseline/T311_international_privacy_platform_policy_checklist.md`
- `docs/worker_summary/T310_worker_summary.md`
- `docs/07_handoff.md`

If T310 needs code, tests, UI, platform adapters, legal filings, external
submissions, or task-board edits, Captain must revise this package before
assignment.

## Required Source Policy

T310 must verify current information with official or primary sources where
possible. It should cite source names/URLs and concrete access dates in the
checklist. It must not present legal advice, regulatory approval, filing
completion, or launch readiness as completed facts.

Suggested source categories to verify:

- personal information and consent obligations;
- AIGC labeling and synthetic-content disclosure obligations;
- algorithm/recommendation and generated-content governance obligations;
- minors and addictive/dependency-risk controls;
- cybersecurity, data localization/export, and deletion/export request handling;
- app store, mini-program, and platform-specific policy constraints;
- user complaint, audit, and incident-response obligations.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLM providers with private data.
- Do not submit filings, registrations, or legal documents.
- Do not claim legal advice, compliance completion, launch approval, or
  regulator acceptance.
- Do not build UI.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/review/M19_review.md`
- `docs/requirements/memory_persona_control_requirements.md`
- `docs/roadmap/M13_plus_milestone_plan.md`
- `docs/architecture/M13_persona_memory_relationship_architecture.md`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/delete_freeze_export_flow_contract.md`

## Expected Outputs

### 1. China Compliance Checklist

Create `docs/compliance/china_compliance_checklist.md` with:

- scope and non-legal-advice disclaimer;
- official/primary sources consulted, with access dates;
- applicability assumptions for a local prototype, closed test, and commercial
  launch;
- checklist items grouped by privacy/consent, AIGC labeling, safety/content,
  minors, dependency/crisis handling, data rights, audit/logging, platform
  policy, and launch gates;
- unresolved questions and required human/legal review points;
- explicit non-actions and no-launch-readiness claim.

### 2. Next Task Package

Create
`docs/tasks/M20_compliance_and_safety_baseline/T311_international_privacy_platform_policy_checklist.md`
for international privacy/platform policy checklist work.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T310_worker_summary.md` and append a T310 worker
record to `docs/07_handoff.md`.

Do not mark T310 complete in `docs/04_task_board.md`.

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
