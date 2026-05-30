# T250 Worker Summary

## Changed

- Added `PersonaCard v1` models and source/consent policy models to
  `src/practical_chat_agent/core/models.py`.
- Added `tests/test_persona_card_schema.py`.
- Added `docs/data_contracts/persona_card_v1_contract.md`.
- Added `docs/tasks/M14_persona_compiler_schema/T251_persona_compiler_local_prototype.md`.
- Appended the T250 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## TDD Evidence

- RED: `pytest tests\test_persona_card_schema.py -q` failed during collection
  because `PersonaCard` did not exist in `practical_chat_agent.core.models`.
- GREEN: after adding the schema models and runtime-readiness gate, the targeted
  T250 tests passed.

## Schema Behavior Added

- `PersonaCard` is a versioned `persona_card_v1` record with generated
  `persona_` ids, source policy, fictional identity, traits, speech style,
  emotion model, relationship model, imagined virtual history, bounded growth
  policy, proactive preferences, safety policy, status, and review metadata.
- `PersonaSourcePolicy` maps source types to L1-L5 tiers:
  - `original` -> `L1`
  - `deidentified_style` -> `L2`
  - `self_authorized` -> `L3`
  - `third_party_authorized` -> `L4`
  - `prohibited` -> `L5`
- Non-original non-prohibited sources require `consent_artifact_ids`.
- L5 prohibited sources require `prohibited_reason` and blocked real-person
  similarity on the containing `PersonaCard`.
- `PersonaIdentity` is fictional-only in v1 and rejects public/real-person
  references.
- `PersonaVirtualHistory` is always `imagined_ai_generated` and rejects factual
  claims.
- `PersonaGrowthPolicy` rejects overlapping frozen and mutable fields and caps
  weekly trait delta.
- `PersonaProactivePreferences` rejects default-enabled proactive behavior.
- `PersonaSafetyPolicy` requires dependency, no-deception,
  no-unauthorized-clone, and no-paid-intimacy guardrails.
- `PersonaCard.is_runtime_ready()` requires approved human review and blocks
  L3/L4/L5, prohibited sources, real-person similarity blocks, non-fictional
  identity, and disabled core safety flags.

## Explicit Non-Actions

- No Persona Compiler service, LLM call, private chat-log read, runtime dialogue
  use, CLI command, storage repository, migration, proactive behavior, platform
  integration, voice/avatar/deepfake behavior, or automatic sending was added.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- No real-person clone, public-figure clone, ex-partner/family clone,
  deceased-person mode, or deceptive impersonation path was authorized.
- T250 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_persona_card_schema.py -q
```

Result: passed, `13 passed`; pytest emitted cache-provider warnings because
`.pytest_cache` could not be written in this environment.

```text
$env:PYTHONPATH='src'
pytest tests\test_persona_card_schema.py tests\test_behavior_schema.py tests\test_contactskill_persona_brief.py tests\test_relationship_context.py tests\test_outbound_message_request_schema.py -q -o cache_dir=artifacts\t250_pytest_cache --basetemp=artifacts\t250_pytest_basetemp
```

Result: passed, `109 passed`. This rerun used repository-local pytest temp and
cache directories because the first broader attempt failed only while creating
`C:\Users\26410\AppData\Local\Temp\pytest-of-26410`.

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Remaining Risks

- `PersonaCard v1` is schema-only; no compiler quality or user experience has
  been proven.
- L2 de-identified style inspiration is represented only as policy metadata;
  no deidentification guard or similarity test exists yet.
- Runtime use is not wired. Future tasks must explicitly decide how PersonaCard
  influences dialogue without bypassing safety gates.
- Legal/compliance interpretation remains non-authoritative and must be refined
  in later M20 work.

## Recommended Reviewer Type

Adversarial review.
