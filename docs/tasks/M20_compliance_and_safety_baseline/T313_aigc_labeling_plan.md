# T313: AIGC Labeling Plan

## Task ID

T313

## Goal

Create a product and data-contract plan for AIGC/synthetic-content labeling
across companion replies, persona cards, virtual histories, role dynamic posts,
exports, shared content, voice/avatar outputs, and future web-demo surfaces.

## Why Now

T310 and T311 identify AIGC and synthetic-content labeling as a core compliance
gate. T312 defines Consent Center state. Before UI/demo work, the project needs
a clear labeling plan that maps existing models and future surfaces to explicit
visible labels, metadata labels, and review requirements.

## Allowed Files

Future T313 worker may create or modify only:

- `docs/compliance/aigc_labeling_plan.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `src/practical_chat_agent/core/models.py`
- `tests/test_aigc_labeling_plan_contract.py`
- `docs/tasks/M20_compliance_and_safety_baseline/T314_crisis_dependency_policy_tests.md`
- `docs/worker_summary/T313_worker_summary.md`
- `docs/07_handoff.md`

If T313 needs UI, production export writing, platform adapters, external legal
submissions, or task-board edits, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build UI.
- Do not publish or share generated content.
- Do not write real export files.
- Do not claim legal advice, compliance completion, launch approval, app-store
  approval, or regulator acceptance.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/compliance/china_compliance_checklist.md`
- `docs/compliance/international_privacy_platform_policy_checklist.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/role_dynamic_post_contract.md`
- `docs/data_contracts/virtual_life_review_card_contract.md`
- `docs/data_contracts/delete_freeze_export_flow_contract.md`
- `src/practical_chat_agent/core/models.py`
- `tests/test_virtual_life_aigc_labeling.py`
- `tests/test_role_dynamic_post_schema.py`
- `tests/test_consent_center_data_model.py`

## Expected Outputs

### 1. AIGC Labeling Plan

Create `docs/compliance/aigc_labeling_plan.md` with:

- source review notes and access dates;
- surfaces requiring visible labels;
- surfaces requiring metadata/implicit labels before copy/download/export/share;
- label wording guidance;
- review-required and blocked cases;
- mapping from existing model labels to product surfaces;
- explicit non-actions and no-compliance-completion claim.

### 2. Data Contract And Tests

If needed, add lightweight contract models/tests for reusable labeling metadata.
Minimum expected behavior:

- generated text, image, audio, video, virtual scene, persona, virtual history,
  role dynamic post, export, and shared content labels are distinct;
- labels preserve `ai_generated`, `synthetic_content`, `imagined_content`,
  `not_real_world_activity`, and `review_required` where applicable;
- payloads contain no raw private chat text and no send, schedule, delivery,
  platform, webhook, token, or queue fields.

### 3. Next Task Package

Create
`docs/tasks/M20_compliance_and_safety_baseline/T314_crisis_dependency_policy_tests.md`
for crisis/dependency policy tests.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T313_worker_summary.md` and append a T313 worker
record to `docs/07_handoff.md`.

Do not mark T313 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
git diff --check
```

If the worker changes code or tests:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_aigc_labeling_plan_contract.py tests\test_virtual_life_aigc_labeling.py tests\test_consent_center_data_model.py -q
```

## Reviewer Type

Adversarial legal/product-policy review recommended.

Reviewer should verify that labels are explicit, persistent across export/share
paths, and do not claim legal sufficiency or platform approval.
