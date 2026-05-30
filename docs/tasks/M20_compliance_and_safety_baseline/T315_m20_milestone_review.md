# T315: M20 Milestone Review

## Task ID

T315

## Goal

Perform an adversarial M20 milestone review for the Compliance And Safety
Baseline work. The review should verify that M20 provides compliance
checklists, consent contracts, AIGC labeling contracts, and crisis/dependency
policy tests without claiming legal sufficiency, platform approval, clinical
safety, UI readiness, or launch readiness.

## Why Now

T310-T314 define the first commercial-governance baseline. M20 needs a gate
review before entering M21 text-first product UX prototype work, because M21
will begin composing user-facing flows around persona creation, chat, memory
explanations, virtual life stream, proactive settings, and data controls.

## Allowed Files

Future T315 worker may create or modify only:

- `docs/review/M20_review.md`
- `docs/tasks/M21_text_first_product_ux_prototype/T320_ux_information_architecture.md`
- `docs/worker_summary/T315_worker_summary.md`
- `docs/07_handoff.md`

If T315 needs code, tests, UI, runtime behavior, model-provider calls, platform
adapters, outbound messaging, legal filings, or task-board edits, Captain must
revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build UI.
- Do not mutate consent, memory, persona, or safety records.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not claim legal advice, compliance completion, crisis-safety sufficiency,
  clinical validation, launch approval, app-store approval, or regulator
  acceptance.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/compliance/china_compliance_checklist.md`
- `docs/compliance/international_privacy_platform_policy_checklist.md`
- `docs/compliance/aigc_labeling_plan.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `docs/worker_summary/T310_worker_summary.md`
- `docs/worker_summary/T311_worker_summary.md`
- `docs/worker_summary/T312_worker_summary.md`
- `docs/worker_summary/T313_worker_summary.md`
- `docs/worker_summary/T314_worker_summary.md`
- `tests/test_consent_center_data_model.py`
- `tests/test_aigc_labeling_plan_contract.py`
- `tests/test_crisis_dependency_policy.py`
- `tests/test_proactive_policy_gate.py`
- `tests/test_proactive_consent_schema.py`

## Expected Outputs

### 1. M20 Review

Create `docs/review/M20_review.md` with:

- gate recommendation: `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`;
- task coverage table for T310-T314;
- implemented code, data contracts, and compliance documents;
- verification evidence;
- safety/compliance boundary assessment;
- explicit non-actions;
- residual risks;
- M21 entry recommendation.

### 2. M21 Entry Task Package

Create
`docs/tasks/M21_text_first_product_ux_prototype/T320_ux_information_architecture.md`
for UX information architecture work.

### 3. Worker Summary And Handoff

Write `docs/worker_summary/T315_worker_summary.md` and append a T315 worker
record to `docs/07_handoff.md`.

Do not mark T315 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_consent_center_data_model.py tests\test_aigc_labeling_plan_contract.py tests\test_crisis_dependency_policy.py tests\test_proactive_policy_gate.py tests\test_proactive_consent_schema.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial safety/legal/product-policy review required.

Reviewer should mark M20 as `PASS_WITH_WARNINGS` only if the work remains local,
review-first, test-covered, and explicit about non-compliance-completion.
Reviewer should `BLOCK` if a later diff claims legal sufficiency, clinical
safety, platform approval, real consent capture, emergency escalation,
automatic sending, UI launch readiness, or public deployment readiness.
