# T250: PersonaCard v1 Schema And Source / Consent Policy

## Task ID

T250

## Goal

Define the first `PersonaCard v1` schema and source/consent policy for the M14
Persona Compiler milestone.

The task should make transparent fictional AI persona creation concrete enough
for later local compiler work, while preserving M13 boundaries: no real-person
clone, no private reads, no LLM calls, no runtime dialogue changes, no proactive
sending, and no platform integration.

## Why Now

T240 defines the commercial companion product boundary and recommends that M13
allow only M14 Persona Compiler schema/local creation work. The first M14 step
should be schema and policy, not a full compiler.

`PersonaCard v1` is the shared contract future tasks need before prompt-to-
schema generation, deidentification guard tests, version diff/rollback, review
cards, Memory OS v2, relationship adapters, or UX prototypes can safely depend
on persona state.

## Allowed Files

Future T250 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/tasks/M14_persona_compiler_schema/T251_persona_compiler_local_prototype.md`
- `docs/worker_summary/T250_worker_summary.md`
- `tests/test_persona_card_schema.py`
- `docs/07_handoff.md`

If the implementation needs a new small service file, Captain must revise this
task package before assigning the worker.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call an LLM, external API, model provider, browser, platform API, or
  network service.
- Do not add compiler runtime behavior, CLI commands, app UI, storage
  repositories, migrations, config, connectors, adapters, schedulers, or
  platform delivery.
- Do not implement automatic sending or proactive message generation.
- Do not implement voice, avatar, image, video, deepfake, or biometric flows.
- Do not create a real-person clone, public-figure clone, ex-partner/family
  clone, deceased-person mode, or deceptive impersonation path.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`; those
  remain Captain-owned after review.
- Do not describe future Persona Compiler capabilities as implemented.

## Inputs To Read

Required:

- `README.md`
- `AGENTS.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/product/M13_commercial_companion_positioning.md`
- `docs/safety/M13_clone_and_persona_risk_tiers.md`
- `docs/architecture/M13_persona_memory_relationship_architecture.md`
- `docs/roadmap/M13_plus_milestone_plan.md`
- existing schema style in `src/practical_chat_agent/core/models.py`
- existing model tests under `tests/`

Recommended:

- `docs/data_contracts/contactskill_decomposition_contract.md`
- `docs/data_contracts/distillation_output_contract.md`
- `docs/data_contracts/relationship_state_contract.md`
- `docs/data_contracts/behavior_planner_contract.md`

## Expected Outputs

### 1. PersonaCard v1 Models

Add Pydantic models consistent with existing code style. Exact names may be
adjusted to match local conventions, but the schema must cover:

- `PersonaCard`
- `PersonaSourcePolicy`
- `PersonaIdentity`
- `PersonaTraitProfile`
- `PersonaSpeechStyle`
- `PersonaEmotionModel`
- `PersonaRelationshipModel`
- `PersonaVirtualHistory`
- `PersonaGrowthPolicy`
- `PersonaProactivePreferences`
- `PersonaSafetyPolicy`
- `PersonaReviewMetadata` or equivalent review/gate metadata

Required fields/concepts:

- stable `persona_id`;
- schema version;
- creation mode: detailed prompt, fuzzy preference, template, random seed, and
  future de-identified style inspiration;
- truth disclosure: AI and fictional unless future tasks add another reviewed
  mode;
- source type: original, deidentified style, self-authorized, third-party
  authorized, prohibited;
- risk tier: L1-L5;
- consent artifact ids;
- blocked real-person similarity flag;
- frozen fields and mutable fields;
- max trait delta or equivalent bounded growth policy;
- safety flags for no deception, no unauthorized clone, and no dependency
  language;
- status values that keep drafts/rejected/frozen records out of runtime use.

### 2. Source / Consent Policy Contract

Create `docs/data_contracts/persona_card_v1_contract.md`.

Must include:

- field descriptions;
- allowed creation modes;
- L1-L5 risk tier mapping;
- source/consent requirements;
- runtime-readiness rules;
- prohibited requests and required safe transformations;
- examples using synthetic fictional personas only;
- explicit statement that T250 does not implement compiler logic or real-person
  style extraction.

### 3. Tests

Add focused schema tests for:

- L1 fictional persona can validate;
- L5 unauthorized clone or prohibited source is not runtime-ready;
- missing consent blocks non-original source types;
- imagined/virtual history is represented as fictional/AI content, not factual
  memory;
- frozen/mutable field policy validates;
- rejected/frozen/draft status does not become runtime-ready;
- serialized examples do not require private content.

### 4. Next Task Package

Create `docs/tasks/M14_persona_compiler_schema/T251_persona_compiler_local_prototype.md`
as a placeholder or complete package only if Captain expects it. T251 should
remain local and synthetic: no private reads, no external LLM calls unless
explicitly authorized later, and no clone behavior.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T250_worker_summary.md` and append a T250 worker
record to `docs/07_handoff.md`.

Do not mark T250 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_card_schema.py -q
```

```powershell
git diff --check
```

If modifying `core.models.py` breaks unrelated tests during collection, report
the failure and the suspected dependency surface in the worker summary.

## Docs To Update

Worker updates only:

- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/tasks/M14_persona_compiler_schema/T251_persona_compiler_local_prototype.md`
- `docs/worker_summary/T250_worker_summary.md`
- `docs/07_handoff.md`

Captain updates after review:

- `docs/00_raw_idea.md`
- `docs/01_feasibility_report.md`
- `docs/03_architecture.md`
- `docs/04_task_board.md`
- `docs/05_decision_log.md`
- `docs/06_eval_protocol.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Reviewer Type

Adversarial review recommended.

Reviewer should verify:

- schema enforces transparency and L1/L5 safety boundaries;
- no real-person clone path is implemented or implied;
- non-original source types cannot become runtime-ready without consent
  metadata;
- tests cover blocked/prohibited statuses;
- no private artifacts are read or quoted;
- no future compiler/proactive/platform behavior is described as implemented.
