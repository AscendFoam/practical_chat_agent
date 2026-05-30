# T312: Consent Center Data Model

## Task ID

T312

## Goal

Define local data models for a Consent Center that can represent user consent,
withdrawal, feature-specific permissions, data-use preferences, minor/guardian
state, AIGC/synthetic-content acknowledgements, and deletion/export request
status for the companion-agent prototype.

## Why Now

T310 and T311 identify compliance and platform-policy requirements that depend
on granular, reviewable consent state. Before UI or closed-test workflows, the
project needs typed local consent artifacts that downstream memory, persona,
proactive, voice/avatar, export, and deletion flows can inspect.

## Allowed Files

Future T312 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `tests/test_consent_center_data_model.py`
- `docs/data_contracts/consent_center_contract.md`
- `docs/tasks/M20_compliance_and_safety_baseline/T313_aigc_labeling_plan.md`
- `docs/worker_summary/T312_worker_summary.md`
- `docs/07_handoff.md`

If T312 needs UI, external legal integrations, production persistence, platform
adapters, user-data processing changes, or task-board edits, Captain must
revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not build UI.
- Do not process real user consent.
- Do not enable training/fine-tuning on user data.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not claim legal advice, compliance completion, launch approval, app-store
  approval, or regulator acceptance.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/compliance/china_compliance_checklist.md`
- `docs/compliance/international_privacy_platform_policy_checklist.md`
- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/delete_freeze_export_flow_contract.md`
- `docs/data_contracts/persona_version_editor_contract.md`
- `src/practical_chat_agent/core/models.py`
- `tests/test_proactive_consent_schema.py`
- `tests/test_delete_freeze_export_flow_contract.py`

## Expected Outputs

### 1. Consent Center Models And Tests

Add contract models to `src/practical_chat_agent/core/models.py`.

Minimum expected objects:

- `ConsentFeatureScope`;
- `ConsentGrantRecord`;
- `ConsentWithdrawalRecord`;
- `ConsentCenterState`;
- `DataRightsRequestRecord`.

Minimum expected behavior:

- consent is feature-specific, versioned, timestamped, and actor-attributed;
- withdrawal supersedes prior grants for the same feature scope;
- memory, persona distillation, proactive messaging, AIGC export/share,
  voice/avatar, analytics, model-improvement, and payment/marketing scopes are
  distinct;
- minor/guardian state is represented without enabling minor access by default;
- data rights requests represent access, correction, deletion, export,
  withdrawal, and objection/status tracking;
- payloads contain no raw private chat text and no send, schedule, delivery,
  platform, webhook, token, or queue fields;
- models are local contracts only and expose no method that performs external
  consent capture, platform integration, or data mutation.

### 2. Data Contract

Create `docs/data_contracts/consent_center_contract.md` describing fields,
invariants, non-actions, and verification.

### 3. Next Task Package

Create `docs/tasks/M20_compliance_and_safety_baseline/T313_aigc_labeling_plan.md`
for AIGC labeling plan work.

### 4. Worker Summary And Handoff

Write `docs/worker_summary/T312_worker_summary.md` and append a T312 worker
record to `docs/07_handoff.md`.

Do not mark T312 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

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

## Reviewer Type

Adversarial legal/product-policy review recommended.

Reviewer should verify that T312 represents local consent state only and does
not claim legal sufficiency, capture real consent, mutate data, enable platform
integration, or authorize launch.
