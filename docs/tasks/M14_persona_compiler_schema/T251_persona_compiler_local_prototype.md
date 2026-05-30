# T251: Local Prompt-To-Schema Persona Compiler Prototype

## Task ID

T251

## Goal

Implement a deterministic local Persona Compiler prototype that converts
synthetic user-provided persona descriptions into `PersonaCard v1` draft
records without LLM calls, private reads, real-person cloning, runtime dialogue
changes, proactive behavior, or platform integration.

## Why Now

T250 defines `PersonaCard v1` and source/consent policy. The next safe step is
a local deterministic compiler that proves the schema can be populated from
ordinary L1 fictional persona inputs before any LLM-assisted generation,
deidentification guard, review card, version store, or UX work.

## Allowed Files

Future T251 worker may create or modify only:

- `src/practical_chat_agent/services/persona_compiler.py`
- `tests/test_persona_compiler.py`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/tasks/M14_persona_compiler_schema/T252_deidentification_guard_tests.md`
- `docs/worker_summary/T251_worker_summary.md`
- `docs/07_handoff.md`

If CLI wiring, storage, or additional models are needed, Captain must revise
this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not implement live platform integration, outbound requests, proactive
  candidates, schedulers, or automatic sending.
- Do not implement real-person style extraction, voice/face/avatar work,
  public-figure cloning, ex-partner/family cloning, deceased-person mode, or
  any deceptive impersonation path.
- Do not mutate memory, ContactSkill, RelationshipState, outbound requests, or
  approved stores.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/safety/M13_clone_and_persona_risk_tiers.md`
- `docs/safety/M13_proactive_companionship_redlines.md`
- `docs/architecture/M13_persona_memory_relationship_architecture.md`
- `tests/test_persona_card_schema.py`

## Expected Outputs

### 1. Deterministic Compiler Service

Create a local service that accepts a synthetic description payload such as:

```json
{
  "user_id": "user_synthetic",
  "display_name": "Lin Qi",
  "description": "fictional calm companion, concise, dry humor",
  "creation_mode": "detailed_prompt"
}
```

and returns a `PersonaCard(status="candidate")`.

The compiler may use simple deterministic keyword/phrase mapping for T251. It
must not pretend to be an LLM or a full compiler.

### 2. Safety Handling

The service must reject or mark prohibited:

- requests containing public-figure / real-person clone signals;
- ex-partner/family/deceased-person clone requests;
- voice/face/deepfake requests;
- hidden impersonation requests;
- automatic sending requests.

L5/prohibited results must never be runtime-ready.

### 3. Contract Doc

Create `docs/data_contracts/persona_compiler_contract.md` describing inputs,
outputs, deterministic limitations, safety blocks, and non-actions.

### 4. Tests

Add focused tests for:

- detailed fictional description compiles to L1 candidate PersonaCard;
- fuzzy preference compiles to safe defaults;
- template/random seed uses synthetic fictional defaults;
- real-person clone request is blocked/prohibited;
- voice/face/deepfake request is blocked/prohibited;
- compiler does not enable proactive behavior by default;
- compiler does not expose send/schedule/runtime methods.

### 5. Next Task Package

Create `docs/tasks/M14_persona_compiler_schema/T252_deidentification_guard_tests.md`
for synthetic deidentification guard tests only. T252 should not read private
chat logs.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T251_worker_summary.md` and append a T251 worker
record to `docs/07_handoff.md`.

Do not mark T251 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_compiler.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_card_schema.py tests\test_persona_compiler.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T251 is deterministic, synthetic, L1-first, and
does not smuggle LLM behavior, private reads, real-person cloning, proactive
sending, or platform integration into the compiler.
