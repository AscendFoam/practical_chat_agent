# T331 Worker Summary

## Changed

- Added `tests/test_voice_consent_data_model.py`.
- Updated `src/practical_chat_agent/core/models.py` with local voice consent
  models.
- Added `docs/data_contracts/voice_consent_contract.md`.
- Added
  `docs/tasks/M22_voice_and_avatar_exploration/T332_asr_tts_latency_benchmark.md`.
- Appended the T331 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## Implementation Result

T331 adds local, review-first voice consent state:

- voice defaults to disabled;
- `voice_avatar` consent is required for any non-disabled route;
- `non_real_synthetic_voice` can become `review_required` with active consent;
- runtime voice remains disabled even in review-required state;
- generated audio labeling maps to `audio` / `voice_avatar`;
- metadata labels are required before any future copy/download/export/share;
- real-person, deceased-person, public-figure, family-member, ex-partner, and
  voice-clone routes are blocked;
- recorded-user and third-party-authorized voice routes are represented but
  deferred behind future policy review;
- crisis/dependency safety decisions can block voice output.

## TDD Evidence

RED command:

```text
$env:PYTHONPATH='src'
pytest tests\test_voice_consent_data_model.py -q -o cache_dir=artifacts\t331_pytest_cache_red --basetemp=artifacts\t331_pytest_basetemp_red
```

Result: failed as expected because `VoiceConsentPolicy` did not exist.

GREEN command:

```text
$env:PYTHONPATH='src'
pytest tests\test_voice_consent_data_model.py -q -o cache_dir=artifacts\t331_pytest_cache_green --basetemp=artifacts\t331_pytest_basetemp_green
```

Result: passed, `7 passed`.

## Explicit Non-Actions

- No model-provider calls, TTS, ASR, voice cloning, voice conversion,
  microphone capture, audio upload, audio generation, audio processing,
  benchmark execution, UI, avatar/Live2D behavior, platform adapter, outbound
  messaging, or task-board edit was added.
- No legal advice, compliance completion, biometric compliance,
  synthetic-media compliance, crisis-safety sufficiency, app-store approval,
  launch approval, or regulator acceptance was claimed.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- T331 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_voice_consent_data_model.py -q -o cache_dir=artifacts\t331_pytest_cache_final --basetemp=artifacts\t331_pytest_basetemp_final
```

Result: passed, `7 passed`.

```text
$env:PYTHONPATH='src'
pytest tests\test_consent_center_data_model.py tests\test_aigc_labeling_plan_contract.py tests\test_crisis_dependency_policy.py tests\test_voice_consent_data_model.py -q -o cache_dir=artifacts\t331_pytest_cache_related --basetemp=artifacts\t331_pytest_basetemp_related
```

Result: passed, `25 passed`.

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Remaining Risks

- T331 is a local data model only; no voice runtime, benchmark, UI, provider
  review, legal review, or user study has been completed.
- Future ASR/TTS work must remain synthetic-fixture-only until provider,
  privacy, consent, and labeling review explicitly permits more.

## Recommended Reviewer Type

Adversarial voice/privacy/product-policy review.
