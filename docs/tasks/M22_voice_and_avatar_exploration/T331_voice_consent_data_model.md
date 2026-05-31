# T331: Voice Consent Data Model

## Task ID

T331

## Goal

Add local voice consent and voice-mode preference data contracts so future voice
experiments can remain disabled-by-default, consent-gated, clearly labeled, and
blocked for real-person cloning.

## Why Now

T330 recommends only non-real synthetic voice routes for the first M22
experiments. Before any ASR/TTS benchmark or UI work, the repository needs a
small, testable data model that encodes consent, labeling, blocked routes, and
review-required state without handling audio.

## Allowed Files

Future T331 worker may create or modify only:

- `src/practical_chat_agent/core/models.py`
- `tests/test_voice_consent_data_model.py`
- `docs/data_contracts/voice_consent_contract.md`
- `docs/tasks/M22_voice_and_avatar_exploration/T332_asr_tts_latency_benchmark.md`
- `docs/worker_summary/T331_worker_summary.md`
- `docs/07_handoff.md`

If T331 needs runtime TTS/ASR, audio files, microphone capture, provider calls,
UI, avatar/Live2D code, private data processing, task-board edits, platform
adapters, or outbound messaging, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call model providers, synthesize audio, clone voices, convert voices,
  capture microphone input, upload audio, or process voice samples.
- Do not create generated audio files or voice fixtures.
- Do not build UI, browser demo, avatar, Live2D behavior, or playback controls.
- Do not add platform delivery, push notification, send, schedule, queue,
  webhook, token, adapter, or realtime fields.
- Do not mark T331 complete in `docs/04_task_board.md`.
- Do not claim legal advice, biometric compliance, synthetic-media compliance,
  app-store approval, launch approval, or regulator acceptance.

## Inputs To Read

Required:

- `docs/research/voice_technology_survey.md`
- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`
- `docs/compliance/aigc_labeling_plan.md`
- `docs/compliance/china_compliance_checklist.md`
- `docs/compliance/international_privacy_platform_policy_checklist.md`

## Expected Outputs

### 1. Tests First

Create `tests/test_voice_consent_data_model.py` before implementation.

Minimum test coverage:

- default voice state is disabled;
- voice/avatar consent is separate and required;
- non-real synthetic voice can become review-ready only with active
  `voice_avatar` consent and required AIGC labels;
- unauthorized real-person, deceased-person, public-figure, family, or
  ex-partner voice routes are blocked;
- generated audio labels include AI-generated, synthetic, audio, voice-avatar,
  and review-required markers;
- metadata label is required before future copy/download/export/share;
- crisis/dependency safety can block voice output;
- payloads contain no audio bytes, transcripts, raw private text, provider
  tokens, send/schedule/delivery/platform/webhook/queue fields, or generated
  audio paths.

### 2. Local Data Model

Implement only local models in `src/practical_chat_agent/core/models.py`.

Recommended objects:

- `VoiceMode`
- `VoiceSourceRoute`
- `VoiceConsentPolicy`
- `VoicePreferenceState`

Recommended route values:

- `disabled`
- `non_real_synthetic_voice`
- `generated_fictional_voice`
- `recorded_user_voice`
- `third_party_authorized_voice`
- `blocked_voice_clone`

Recommended decision values:

- `disabled`
- `blocked`
- `review_required`

The model should default to disabled and should make the first allowed route
`non_real_synthetic_voice`.

### 3. Contract

Create `docs/data_contracts/voice_consent_contract.md` explaining:

- schema purpose;
- consent dependency on `voice_avatar`;
- route vocabulary;
- labeling requirements;
- blocked real-person/deceased-person/public-figure likeness routes;
- crisis/dependency interaction;
- privacy-safe payload constraints;
- non-actions.

### 4. Next Task Package

Create
`docs/tasks/M22_voice_and_avatar_exploration/T332_asr_tts_latency_benchmark.md`
for a future synthetic-fixture-only benchmark design. T332 must not run provider
calls unless Captain explicitly allows it.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T331_worker_summary.md` and append a T331 worker
record to `docs/07_handoff.md`.

Do not mark T331 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_voice_consent_data_model.py -q -o cache_dir=artifacts\t331_pytest_cache --basetemp=artifacts\t331_pytest_basetemp
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial voice/privacy/product-policy review recommended.

Reviewer should block if T331 permits unauthorized voice cloning, stores raw
audio/transcripts, omits labels, enables runtime voice output, adds delivery
fields, or weakens the existing consent/AIGC/crisis-dependency boundaries.
