# T324 Worker Summary

## Changed

- Added `src/practical_chat_agent/ui/text_first_proactive_settings.py`.
- Added `tests/test_text_first_proactive_settings_prototype.py`.
- Added `docs/data_contracts/text_first_proactive_settings_contract.md`.
- Added
  `docs/tasks/M21_text_first_product_ux_prototype/T325_user_study_protocol.md`.
- Appended the T324 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## TDD Evidence

- RED: `pytest tests\test_text_first_proactive_settings_prototype.py -q` failed
  during collection because `text_first_proactive_settings` did not exist.
- GREEN: after adding the proactive settings state projection module, the
  targeted T324 tests passed.

## Behavior Added

- Projects disabled, enabled, paused, and revoked proactive consent into visible
  settings states.
- Shows local review surfaces, low-pressure intents, quiet hours, frequency
  caps, and minimum intervals.
- Projects proactive policy decisions into allow-for-review, deferred, or
  blocked settings states.
- Crisis/dependency safety decisions override proactive states and keep
  outreach blocked.
- Keeps all states review-required with no pending action.
- Payload and surface-area tests guard against raw private data and
  runtime/outbound methods.

## Explicit Non-Actions

- No frontend code, browser demo, proactive candidate generation, candidate
  ranking, consent mutation, persistence, LLM call, private chat-log read,
  scheduling, automatic sending, notification, webhook, platform integration,
  voice/avatar/video behavior, or Live2D behavior was added.
- No legal advice, compliance completion, crisis-safety sufficiency, clinical
  validation, launch approval, app-store approval, or regulator acceptance was
  claimed.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- T324 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_proactive_settings_prototype.py -q -o cache_dir=artifacts\t324_pytest_cache_green --basetemp=artifacts\t324_pytest_basetemp_green
```

Result: passed, `6 passed`.

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_proactive_settings.py src\practical_chat_agent\core\models.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_text_first_proactive_settings_prototype.py tests\test_proactive_consent_schema.py tests\test_proactive_policy_gate.py tests\test_crisis_dependency_policy.py -q -o cache_dir=artifacts\t324_pytest_cache_final --basetemp=artifacts\t324_pytest_basetemp_final
```

Result: passed, `26 passed`.

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Remaining Risks

- T324 is a local state/projection contract, not a frontend or proactive
  runtime.
- M21 still needs user study protocol and milestone review work.

## Recommended Reviewer Type

Product/safety UX review.
