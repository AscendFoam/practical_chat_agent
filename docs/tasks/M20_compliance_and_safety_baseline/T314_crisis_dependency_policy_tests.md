# T314: Crisis And Dependency Policy Tests

## Task ID

T314

## Goal

Add local crisis and emotional-dependency policy tests for the companion-agent
prototype, then implement the smallest reviewed policy contract needed to make
those tests pass.

## Why Now

T310 and T311 identify companion-chatbot crisis, dependency, deception,
manipulation, and youth-safety risk as closed-test blockers. T313 defines AIGC
labeling. Before UI/demo work, the project needs executable policy checks that
prevent the agent from acting like a therapist, replacing real relationships,
intensifying dependence, or proactively escalating vulnerable users.

## Allowed Files

Future T314 worker may create or modify only:

- `src/practical_chat_agent/services/companion_safety_policy.py`
- `src/practical_chat_agent/core/models.py`
- `tests/test_crisis_dependency_policy.py`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `docs/tasks/M20_compliance_and_safety_baseline/T315_m20_milestone_review.md`
- `docs/worker_summary/T314_worker_summary.md`
- `docs/07_handoff.md`

If T314 needs UI, model-provider calls, real emergency resources by location,
browser automation, platform adapters, outbound messaging, or task-board edits,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not provide medical, mental-health, legal, or emergency advice as project
  policy.
- Do not build UI.
- Do not send, schedule, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not implement automatic emergency escalation.
- Do not claim crisis-safety sufficiency, clinical validation, compliance
  completion, launch approval, app-store approval, or regulator acceptance.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/compliance/china_compliance_checklist.md`
- `docs/compliance/international_privacy_platform_policy_checklist.md`
- `docs/data_contracts/proactive_policy_gate_contract.md`
- `docs/data_contracts/proactive_consent_contract.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `src/practical_chat_agent/services/proactive_policy_gate.py`
- `src/practical_chat_agent/core/models.py`
- `tests/test_proactive_policy_gate.py`
- `tests/test_proactive_consent_schema.py`

Optional:

- `docs/reference/gpt-pro关于后续从M13开始的计划分析.md`

## Expected Outputs

### 1. Policy Tests

Create `tests/test_crisis_dependency_policy.py`.

Minimum expected behavior:

- crisis/self-harm indicators produce a blocked/high-risk decision;
- dependency/replacement indicators produce a de-escalation decision;
- romantic or manipulative escalation is blocked for vulnerable states;
- proactive outreach is blocked when crisis or dependency risk is present;
- responses must include supportive, non-clinical redirection notes;
- decisions require human review for crisis/dependency high-risk cases;
- payloads contain no raw private chat text and no send, schedule, delivery,
  platform, webhook, token, or queue fields.

### 2. Policy Contract

Implement the smallest local policy contract needed for the tests. Prefer a
pure deterministic service function or model that accepts synthetic features
and returns a reviewable decision object.

The contract should not generate user-facing crisis scripts beyond generic
supportive redirection notes.

### 3. Data Contract

Create `docs/data_contracts/crisis_dependency_policy_contract.md` describing
fields, decisions, invariants, non-actions, and verification.

### 4. Next Task Package

Create
`docs/tasks/M20_compliance_and_safety_baseline/T315_m20_milestone_review.md`
for M20 review.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T314_worker_summary.md` and append a T314 worker
record to `docs/07_handoff.md`.

Do not mark T314 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

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

## Reviewer Type

Adversarial safety/product-policy review recommended, with special attention to
crisis, emotional dependency, deceptive attachment, proactive outreach, youth
safety, and no-clinical-claims boundaries.
