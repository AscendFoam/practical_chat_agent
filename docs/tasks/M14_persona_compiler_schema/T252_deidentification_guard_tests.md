# T252: Synthetic Deidentification Guard Tests

## Task ID

T252

## Goal

Define synthetic-only tests for a future `DeidentificationGuard` that prevents
L2 abstract style inspiration from preserving real-person identifiers, private
events, biometric cues, exact biography, or distinctive catchphrases.

## Why Now

T251 creates only L1 fictional PersonaCards. The project should not open
`style_inspiration` or any private-material path until deidentification failure
modes are captured as tests first.

## Allowed Files

Future T252 worker may create or modify only:

- `src/practical_chat_agent/services/deidentification_guard.py`
- `tests/test_deidentification_guard.py`
- `docs/data_contracts/deidentification_guard_contract.md`
- `docs/tasks/M14_persona_compiler_schema/T253_persona_review_card_contract.md`
- `docs/worker_summary/T252_worker_summary.md`
- `docs/07_handoff.md`

If the task needs `PersonaCard` schema changes, storage, CLI wiring, private
input readers, or runtime use, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement chat-log ingestion, style extraction, or similarity scoring
  against real private material.
- Do not enable real-person clone, public-figure clone, ex-partner/family
  clone, deceased-person mode, voice clone, face/avatar deepfake, or hidden
  impersonation.
- Do not wire PersonaCard into runtime dialogue, proactive behavior, outbound
  candidates, schedulers, or platform integration.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/persona_compiler.py`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/safety/M13_clone_and_persona_risk_tiers.md`
- `tests/test_persona_compiler.py`

## Expected Outputs

### 1. Synthetic Guard Contract

Create a contract for deidentification guard inputs and outputs. It should
distinguish:

- allowed abstract style signals;
- direct identifiers;
- biometric cues;
- exact biography;
- private event references;
- distinctive catchphrases;
- unsafe clone intent.

### 2. Failing-First Guard Tests

Add tests showing that a future guard:

- allows generic abstract style such as concise, warm, delayed-response, or
  dry-humor preferences;
- blocks names, phone numbers, addresses, employer/school identifiers, and
  exact handles;
- blocks voice, face, image, and real-person avatar cues;
- blocks exact relationship history or private event reconstruction;
- blocks distinctive catchphrases when presented as "make it talk exactly like
  this person";
- returns a machine-readable decision with risk flags and a safe transformed
  summary.

### 3. Minimal Guard Implementation

Implement only enough deterministic local logic to satisfy the synthetic tests.
The guard must not read files, call models, or access private corpora.

### 4. Next Task Package

Create `docs/tasks/M14_persona_compiler_schema/T253_persona_review_card_contract.md`
for review-card and edit-contract work. T253 should remain local and
review-first.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T252_worker_summary.md` and append a T252 worker
record to `docs/07_handoff.md`.

Do not mark T252 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\deidentification_guard.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_deidentification_guard.py tests\test_persona_compiler.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T252 remains synthetic, does not open private
sources, and does not turn L2 style inspiration into an identifiable clone
path.
