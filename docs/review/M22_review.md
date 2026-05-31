# M22 Review: Voice And Avatar Exploration

## Status

Gate recommendation: PASS_WITH_WARNINGS for entering M23 integrated text-first
web demo work.

M22 established voice/avatar research boundaries plus a local, review-first
voice consent data model. It did not implement voice runtime, avatar runtime,
provider calls, generated media, microphone/camera capture, browser UI,
platform delivery, private data processing, or launch readiness.

## Task Coverage

| Task | Result | Evidence |
| --- | --- | --- |
| T330 Voice technology survey | Implemented | `docs/research/voice_technology_survey.md`. |
| T331 Voice consent data model | Implemented | `VoicePreferenceState`, `VoiceConsentPolicy`, `tests/test_voice_consent_data_model.py`. |
| T332 ASR/TTS latency benchmark plan | Implemented | `docs/research/asr_tts_latency_benchmark_plan.md`. |
| T333 Avatar interaction survey | Implemented | `docs/research/avatar_interaction_survey.md`. |

## Implemented Code

- `src/practical_chat_agent/core/models.py`
  - `VoiceMode`
  - `VoiceSourceRoute`
  - `VoiceRequestedLikenessType`
  - `VoiceConsentDecision`
  - `VoiceSafetyDecisionAction`
  - `VoicePreferenceState`
  - `VoiceConsentPolicy`

## Product And Research Documents

- `docs/research/voice_technology_survey.md`
- `docs/research/asr_tts_latency_benchmark_plan.md`
- `docs/research/avatar_interaction_survey.md`

## Data Contracts

- `docs/data_contracts/voice_consent_contract.md`

M22 also depends on existing contracts:

- `docs/data_contracts/consent_center_contract.md`
- `docs/data_contracts/aigc_labeling_contract.md`
- `docs/data_contracts/crisis_dependency_policy_contract.md`

## Verification Evidence

Fresh T334 verification command:

```text
$env:PYTHONPATH='src'
pytest tests\test_voice_consent_data_model.py tests\test_consent_center_data_model.py tests\test_aigc_labeling_plan_contract.py tests\test_crisis_dependency_policy.py -q -o cache_dir=artifacts\t334_pytest_cache --basetemp=artifacts\t334_pytest_basetemp
```

Result: passed, `25 passed`.

Fresh diff check:

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

Additional worker-level evidence is recorded in:

- `docs/worker_summary/T330_worker_summary.md`
- `docs/worker_summary/T331_worker_summary.md`
- `docs/worker_summary/T332_worker_summary.md`
- `docs/worker_summary/T333_worker_summary.md`

## Safety Boundary Assessment

M22 is safe to treat as a research and contract milestone because:

- voice defaults to disabled;
- `voice_avatar` consent is required for any non-disabled voice route;
- review-ready voice still does not enable runtime audio;
- first eligible voice route is non-real synthetic voice only;
- generated audio labels map to `audio` and `voice_avatar`;
- metadata labels are required before future copy/download/export/share;
- unauthorized real-person, deceased-person, public-figure, family-member,
  ex-partner, and voice-clone routes are blocked;
- recorded-user and third-party-authorized voice routes are represented but
  deferred behind future policy review;
- crisis/dependency safety decisions can block voice;
- ASR/TTS benchmarking remains synthetic-fixture-only planning;
- no provider, audio, microphone, or benchmark runtime was added;
- avatar research recommends static fictional portrait first and simple
  low-realism animation before Live2D;
- Live2D and 3D avatar routes are deferred behind license, consent, labeling,
  asset-provenance, and safety review;
- camera capture, face landmark tracking, generated talking-head video, and
  real-person/deceased-person avatar likeness remain blocked;
- future UI posture remains text-first with persistent AI/synthetic labels and
  pause/hide controls.

## Explicit Non-Actions

M22 did not implement:

- TTS;
- ASR;
- voice cloning;
- voice conversion;
- generated audio;
- microphone capture;
- audio processing;
- provider account setup;
- provider selection;
- latency benchmark execution;
- generated image/video;
- face clone;
- avatar runtime;
- Live2D runtime;
- camera capture;
- face tracking;
- browser UI or web demo;
- user research execution;
- private chat-log reads;
- real persona distillation;
- platform integration;
- automatic sending or scheduling;
- proactive voice/avatar outreach;
- legal, biometric, synthetic-media, clinical, app-store, user-study, or launch
  validation.

## Residual Risks

- M22 is still research and local state-contract work, not a usable web demo.
- No real user has tested whether voice/avatar labels are understood.
- Provider docs, SDK licenses, costs, retention behavior, and platform policies
  can change.
- Voice and avatar runtime remain high-risk and should stay blocked until after
  text-first demo validation.
- The next product risk is integration quality: existing contracts need one
  coherent UI that users can understand.

## M23 Entry Recommendation

Proceed to M23 with a text-first web demo milestone. M23 should:

- integrate existing local state contracts into a single transparent UI;
- keep voice/avatar runtime disabled;
- show voice/avatar as locked or research-only capabilities;
- preserve AI identity, memory provenance, AIGC labels, consent controls,
  crisis/dependency safety states, and no outbound sending;
- use synthetic fixtures only;
- avoid model-provider calls and private chat logs until later reviewed tasks.

## Reviewer Recommendation

Reviewer should mark M22 as PASS_WITH_WARNINGS if the fresh tests pass and diff
check is clean. Reviewer should BLOCK only if a later diff hides AI identity,
weakens consent/labeling/crisis-dependency gates, or implies voice/avatar
runtime readiness, legal sufficiency, app-store approval, real-person clone
support, camera/microphone capture, media generation, platform delivery, or
launch readiness.
