# Text-First Web Demo State Contract

Task: T341 Web Demo State Adapter
Status: worker draft for review

## Scope

`TextFirstWebDemoAdapter` assembles one local synthetic demo payload from
existing text-first companion contracts. It is an adapter for a future static
web shell. It does not build UI, start a server, call model providers, generate
replies, read private data, generate media, enable voice/avatar runtime,
schedule work, send messages, or integrate with platforms.

Implemented objects:

- `TextFirstWebDemoState`
- `TextFirstWebDemoAdapter`

Implementation entry point:

- `practical_chat_agent.ui.text_first_web_demo_adapter.TextFirstWebDemoAdapter`

## TextFirstWebDemoState

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `text_first_web_demo_state_v1`. |
| `demo_id` | Generated local demo state id. |
| `user_id` | Synthetic owner user id. |
| `onboarding` | Initial AI identity disclosure state. |
| `persona` | Safe persona draft and blocked real-person clone state. |
| `chat_memory` | Review chat state and crisis-blocked chat state. |
| `life_stream` | Private imagined life-stream review state. |
| `proactive` | Enabled review settings and dependency-blocked settings. |
| `controls` | Consent Center and web-demo AIGC label state. |
| `voice` | Disabled, review-required, and blocked voice states. |
| `avatar` | Locked/research-only avatar placeholder state. |
| `review_required` | Always true. |
| `created_at` | Demo state creation timestamp. |

All sections are JSON-serializable dictionaries generated from existing local
models or conservative locked-state metadata.

## Section Mapping

| Section | Source |
| --- | --- |
| `onboarding` | `TextFirstOnboardingPrototype.initial_state(...)` |
| `persona.safe_persona_state` | `TextFirstOnboardingPrototype.create_persona(...)` with safe fictional fixture |
| `persona.blocked_persona_state` | `TextFirstOnboardingPrototype.create_persona(...)` with blocked real-person clone fixture |
| `chat_memory.review_state` | `TextFirstChatMemoryPrototype.project(...)` with factual and imagined memory |
| `chat_memory.blocked_state` | `TextFirstChatMemoryPrototype.project(...)` with crisis safety decision |
| `life_stream` | `TextFirstLifeStreamPrototype.project(...)` with imagined post |
| `proactive.enabled_state` | `TextFirstProactiveSettingsPrototype.project(...)` with enabled local review consent |
| `proactive.blocked_state` | `TextFirstProactiveSettingsPrototype.project(...)` with dependency safety decision |
| `controls.consent_center` | `ConsentCenterState` with synthetic grants |
| `controls.aigc_label` | `AIGCLabelingRequirement` for web demo |
| `voice.*` | `VoicePreferenceState` and `VoiceConsentPolicy` |
| `avatar` | Locked placeholder derived from T333 survey boundary |

## Fixture Assumptions

Fixtures are synthetic and local:

- safe fictional persona named `Lin Qi`;
- blocked real-person clone request without private source text;
- one factual memory;
- one imagined memory;
- one imagined life-stream post;
- enabled proactive local review consent;
- crisis and dependency safety decisions from synthetic labels;
- voice disabled/review/blocked states;
- avatar locked/research-only placeholder.

No fixture is derived from `private/chat_history/` or private artifacts.

## Safety Gates

The adapter payload preserves:

- AI-generated/synthetic identity disclosure;
- persona and virtual-history AIGC labels;
- blocked real-person clone state;
- factual vs imagined memory separation;
- no generated reply text;
- crisis/dependency blocked states;
- imagined/not-real-world life-stream labels;
- proactive consent with `outreach_allowed=false`;
- AIGC export/share metadata requirement;
- voice disabled/review-required/blocked states with `voice_enabled=false`;
- avatar locked/research-only state with `avatar_enabled=false`.

## Invariants

- The adapter returns one serializable state.
- Every major section is present.
- The payload is synthetic and review-required.
- Existing local contracts are reused instead of bypassed.
- Voice is never runtime-enabled.
- Avatar is never runtime-enabled.
- Payloads contain no raw private chat text, transcripts, audio bytes, voice
  samples, generated media paths, provider credentials, send queues, schedules,
  webhooks, platform delivery, or runtime controls.
- The adapter exposes no server, model-provider, media-capture, media
  generation, sending, publishing, or scheduling methods.

## Non-Actions

T341 does not implement:

- frontend UI;
- browser demo;
- dev server;
- model-provider calls;
- final reply generation;
- private chat-log reads;
- real persona distillation;
- persistence;
- production memory mutation;
- export/share/download writing;
- proactive candidate generation;
- automatic sending or scheduling;
- platform integration;
- TTS/ASR;
- voice/avatar/video behavior;
- Live2D behavior;
- legal, clinical, app-store, user-study, or launch approval.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_adapter.py tests\test_text_first_onboarding_prototype.py tests\test_text_first_chat_memory_prototype.py tests\test_text_first_life_stream_prototype.py tests\test_text_first_proactive_settings_prototype.py tests\test_voice_consent_data_model.py -q
```

```powershell
git diff --check
```
