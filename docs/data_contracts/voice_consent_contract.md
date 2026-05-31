# Voice Consent Contract

Task: T331 Voice Consent Data Model
Status: worker draft for review

## Scope

Voice consent models represent local voice preference, consent dependency,
synthetic-audio labeling, and blocked voice routes for the companion-agent
prototype. They do not generate audio, capture microphone input, clone voices,
process audio samples, call model providers, build UI, play audio, benchmark
latency, or integrate with platforms.

Implemented objects:

- `VoicePreferenceState`
- `VoiceConsentPolicy`

Implemented literal sets:

- `VoiceMode`
- `VoiceSourceRoute`
- `VoiceRequestedLikenessType`
- `VoiceConsentDecision`
- `VoiceSafetyDecisionAction`

## VoiceMode And VoiceSourceRoute

Supported values:

- `disabled`
- `non_real_synthetic_voice`
- `generated_fictional_voice`
- `recorded_user_voice`
- `third_party_authorized_voice`
- `blocked_voice_clone`

The first allowed route is `non_real_synthetic_voice`, and even that route is
review-required rather than runtime-enabled. `generated_fictional_voice`,
`recorded_user_voice`, and `third_party_authorized_voice` are represented only
so future policy work can identify them; they are blocked in this contract.
`blocked_voice_clone` is always blocked.

## VoiceRequestedLikenessType

Supported values:

- `none`
- `self`
- `authorized_voice_talent`
- `real_person`
- `deceased_person`
- `public_figure`
- `family_member`
- `ex_partner`

The following likeness types are blocked:

- `real_person`
- `deceased_person`
- `public_figure`
- `family_member`
- `ex_partner`

T331 does not approve `self` or `authorized_voice_talent` routes. They remain
future review concepts and cannot enable runtime voice behavior in this
contract.

## VoicePreferenceState

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `voice_preference_state_v1`. |
| `preference_id` | Generated local voice preference id. |
| `user_id` | Owner user id. |
| `voice_mode` | One `VoiceMode`. Defaults to `disabled`. |
| `source_route` | One `VoiceSourceRoute`. Defaults to `disabled`. |
| `requested_likeness_type` | One `VoiceRequestedLikenessType`. |
| `required_consent_scope` | Always `voice_avatar`. |
| `has_active_voice_avatar_consent` | Whether the consent center currently exposes active voice/avatar consent. |
| `decision` | `disabled`, `blocked`, or `review_required`. |
| `voice_enabled` | Always false. |
| `review_required` | Always true. |
| `visible_label_text` | Visible synthetic voice disclosure text. |
| `disclosure_labels` | Normalized labels including audio and voice-avatar markers. |
| `metadata_label_required` | Always true for generated audio routes. |
| `metadata_labels` | Includes `implicit_metadata_label`. |
| `copy_download_export_share_requires_metadata` | Always true. |
| `aigc_labeling_requirement` | Optional reusable `AIGCLabelingRequirement` for audio / voice-avatar surface. |
| `safety_decision_action` | Existing safety decision action projected into voice gating. |
| `safety_reason_labels` | Redacted safety reason labels. |
| `blocked_reason_labels` | Deterministic blocking reasons. |
| `consent_evidence_refs` | Redacted consent evidence refs only. |
| `created_at` | Preference state creation timestamp. |

Default state is disabled, review-required, and not runtime-enabled.

## VoiceConsentPolicy

`VoiceConsentPolicy.evaluate(...)` builds a local `VoicePreferenceState` from:

- `user_id`;
- requested `source_route`;
- optional `ConsentCenterState`;
- requested likeness type;
- safety decision action and reason labels.

Rules:

1. `voice_avatar` consent is required for any non-disabled route.
2. Consent is user-specific; mismatched consent state blocks the route.
3. `non_real_synthetic_voice` with active `voice_avatar` consent becomes
   `review_required`.
4. Runtime voice remains disabled even in `review_required` state.
5. `generated_fictional_voice`, `recorded_user_voice`, and
   `third_party_authorized_voice` are blocked with
   `future_voice_route_requires_policy_review`.
6. `blocked_voice_clone` is blocked with `voice_clone_blocked`.
7. Real-person, deceased-person, public-figure, family-member, and ex-partner
   likeness requests are blocked with `real_person_voice_likeness_blocked`.
8. `block` or `deescalate_for_review` safety decisions block voice output with
   `voice_blocked_by_safety_decision`.

## Labeling Requirements

Visible label baseline:

```text
AI-generated synthetic voice. Not a human voice.
```

Required labels:

- `ai_generated`
- `synthetic_content`
- `audio`
- `voice_avatar`
- `review_required`
- `implicit_metadata_label`

`VoicePreferenceState.aigc_labeling_requirement`, when present, uses:

- `content_modality=audio`;
- `product_surface=voice_avatar`;
- `metadata_label_required=true`;
- `copy_download_export_share_requires_metadata=true`.

## Invariants

- Voice defaults to disabled.
- Voice/avatar consent is separate from memory, persona distillation, proactive
  messaging, AIGC export/share, analytics, model improvement, and marketing.
- Review-ready voice still does not enable runtime audio.
- Synthetic audio requires visible labels and metadata labels.
- Unauthorized real-person/deceased-person/public-figure/family/ex-partner
  likeness routes are blocked.
- Crisis/dependency safety decisions can block voice.
- Payloads contain no raw private chat text, transcripts, audio bytes, voice
  samples, microphone state, provider credentials, generated audio paths, send
  queues, schedules, webhooks, platform delivery, or runtime controls.

## Non-Actions

T331 does not implement:

- legal advice;
- biometric or synthetic-media compliance completion;
- voice consent capture UI;
- TTS;
- ASR;
- voice cloning;
- voice conversion;
- audio file creation;
- microphone capture;
- provider calls;
- playback;
- latency benchmarks;
- avatar or Live2D behavior;
- proactive voice outreach;
- platform integration;
- sending or scheduling;
- private chat-log reads;
- launch or app-store approval.

## Verification

Expected minimum verification:

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
