# T251 Worker Summary

## Changed

- Added `src/practical_chat_agent/services/persona_compiler.py`.
- Added `tests/test_persona_compiler.py`.
- Added `docs/data_contracts/persona_compiler_contract.md`.
- Added `docs/tasks/M14_persona_compiler_schema/T252_deidentification_guard_tests.md`.
- Appended the T251 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## TDD Evidence

- RED: `pytest tests\test_persona_compiler.py -q` failed during collection
  because `practical_chat_agent.services.persona_compiler` did not exist.
- GREEN: after adding `PersonaCompilerService`, the targeted T251 tests passed.

## Behavior Added

- `PersonaCompilerService.compile(payload)` converts synthetic mappings into
  `PersonaCard v1` records.
- Safe fictional inputs produce `status="candidate"`,
  `source_policy.source_type="original"`, and `risk_tier="L1"`.
- T251 supports `detailed_prompt`, `fuzzy_preference`, `template`, and
  `random_seed` creation modes.
- Fuzzy, template, and random-seed inputs use safe fictional defaults.
- Simple deterministic keyword mapping populates calm mood, concise speech,
  dry humor, warmth, independence, practical comfort style, imagined virtual
  history, growth policy, and safety defaults.
- Proactive preferences remain default-off with zero max daily messages.
- Requests containing real-person clone, voice/face/deepfake, hidden
  impersonation, or automatic-sending signals return rejected L5 prohibited
  PersonaCards.
- The compiler exposes only `compile()` and no send, schedule, deliver,
  execute, runtime, chat-history, or private extraction methods.

## Explicit Non-Actions

- No LLM call, model provider, external API, browser automation, network
  service, private chat-log read, style extraction, similarity scoring,
  runtime dialogue use, review UI, storage repository, migration, proactive
  candidate, platform integration, voice/avatar/deepfake behavior, or automatic
  sending was added.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- No real-person clone, public-figure clone, ex-partner/family clone,
  deceased-person mode, or deceptive impersonation path was authorized.
- T251 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_compiler.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_persona_compiler.py -q -o cache_dir=artifacts\t251_pytest_cache --basetemp=artifacts\t251_pytest_basetemp
```

Result: passed, `10 passed`.

```text
$env:PYTHONPATH='src'
pytest tests\test_persona_card_schema.py tests\test_persona_compiler.py -q -o cache_dir=artifacts\t251_pytest_cache_final --basetemp=artifacts\t251_pytest_basetemp_final
```

Result: passed, `23 passed`.

```text
git diff --check
```

Result: passed.

## Remaining Risks

- T251 keyword mapping is intentionally shallow and should not be treated as a
  production-quality persona authoring experience.
- `style_inspiration` remains unsupported until T252 deidentification guard
  tests and later review gates exist.
- L5 detection is deterministic keyword blocking, not a complete policy engine.
- Runtime dialogue and versioned PersonaCard storage remain unopened.

## Recommended Reviewer Type

Adversarial review.
