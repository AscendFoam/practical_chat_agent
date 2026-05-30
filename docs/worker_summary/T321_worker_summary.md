# T321 Worker Summary

## Changed

- Added `src/practical_chat_agent/ui/text_first_onboarding.py`.
- Added `tests/test_text_first_onboarding_prototype.py`.
- Added `docs/data_contracts/text_first_onboarding_contract.md`.
- Added
  `docs/tasks/M21_text_first_product_ux_prototype/T322_chat_memory_explanation_prototype.md`.
- Appended the T321 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## TDD Evidence

- RED: `pytest tests\test_text_first_onboarding_prototype.py -q` failed during
  collection because `text_first_onboarding` did not exist.
- GREEN: after adding the onboarding state projection module, the targeted T321
  tests passed.

## Behavior Added

- Initial onboarding state exposes AI-generated/synthetic/not-human disclosure.
- Detailed prompt, fuzzy preference, template, and random seed modes produce
  persona draft review states through `PersonaCompilerService`.
- Real-person clone/deceased-person style requests surface blocked persona
  states.
- Style inspiration remains locked by default.
- Persona and virtual-history previews carry AIGC label requirements.
- Consent review scopes are surfaced for memory, proactive messaging, AIGC
  export/share, and persona distillation where relevant.
- Payload and surface-area tests guard against raw private data and
  runtime/outbound methods.

## Explicit Non-Actions

- No frontend code, browser demo, chat runtime, reply generation, LLM call,
  private chat-log read, real persona distillation, deidentification,
  persistence, export/share/download writing, proactive candidate generation,
  automatic sending, scheduling, platform integration, voice/avatar/video
  behavior, or Live2D behavior was added.
- No legal advice, compliance completion, crisis-safety sufficiency, clinical
  validation, launch approval, app-store approval, or regulator acceptance was
  claimed.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- T321 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_onboarding_prototype.py -q -o cache_dir=artifacts\t321_pytest_cache_green --basetemp=artifacts\t321_pytest_basetemp_green
```

Result: passed, `10 passed`.

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_onboarding.py src\practical_chat_agent\services\persona_compiler.py src\practical_chat_agent\core\models.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_onboarding_prototype.py tests\test_persona_compiler.py tests\test_aigc_labeling_plan_contract.py tests\test_consent_center_data_model.py -q -o cache_dir=artifacts\t321_pytest_cache_final --basetemp=artifacts\t321_pytest_basetemp_final
```

Result: passed, `31 passed`.

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Remaining Risks

- T321 is a local state/projection contract, not a frontend.
- M21 still needs chat/memory, life stream, proactive settings, user study, and
  milestone review work.

## Recommended Reviewer Type

Product/safety UX review.
