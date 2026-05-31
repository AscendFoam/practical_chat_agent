# ASR/TTS Latency Benchmark Plan

Task: T332 ASR/TTS Latency Benchmark Plan
Status: worker draft for review

## Scope And Disclaimer

This plan defines how a future approved task could benchmark ASR and TTS
latency for the companion-agent prototype. It does not run a benchmark, call a
provider, synthesize audio, capture microphone input, create audio fixtures,
process audio, choose a provider, build UI, or authorize runtime voice.

This plan assumes T330 and T331 boundaries:

- voice defaults to disabled;
- `voice_avatar` consent is separate and required;
- the first eligible route is non-real synthetic voice only;
- generated audio requires visible and metadata labels;
- crisis/dependency decisions can block voice;
- real-person voice cloning, uploaded samples, microphone capture, and
  proactive voice outreach remain blocked.

## Benchmark Phases

| Phase | Purpose | Data | Runtime allowed? | T332 status |
| --- | --- | --- | --- | --- |
| Phase 0: Plan only | Define metrics and gates. | No audio. | No. | This task. |
| Phase 1: Local harness design | Build measurement harness around fake timing inputs or predeclared synthetic text only. | Synthetic text only. | No provider, no audio. | Future task. |
| Phase 2: Non-real TTS provider benchmark | Measure provider latency with synthetic text fixtures. | Synthetic text; generated non-real synthetic audio. | Only after consent/label/provider review. | Future task. |
| Phase 3: ASR input benchmark | Measure speech recognition latency and quality. | Approved synthetic or volunteered test audio. | Only after mic/audio consent, retention, and vendor review. | Future task. |
| Phase 4: Interactive voice prototype | Combine reviewed text, TTS playback, interruption, and labels. | Reviewed generated text and synthetic audio. | Only after UI/safety review. | Future task. |

T332 covers Phase 0 only.

## Synthetic Text Fixture Categories

Future benchmark text fixtures should be synthetic and committed only as text.
They must not derive from `private/chat_history/`.

Recommended categories:

- short greeting: 8 to 20 Chinese characters;
- short affectionate but non-dependent reply: 20 to 40 Chinese characters;
- ordinary chat answer: 80 to 160 Chinese characters;
- memory-aware reply with factual/imagined distinction: 120 to 220 Chinese
  characters;
- safety de-escalation reply: short supportive non-clinical text;
- life-stream narration label: generated/imagined/not-real-world wording;
- bilingual or code-switching sentence;
- punctuation-heavy expressive sentence;
- long-form companion monologue capped at a future product maximum.

Forbidden fixture content:

- private chat text;
- real names of third parties;
- crisis narratives;
- medical/legal/financial advice;
- sexual or minor-facing content;
- real-person/deceased-person/public-figure imitation prompts;
- text instructing the voice to sound like a real person.

## ASR Metrics For A Later Approved Task

ASR should remain out of the first runtime experiment. If a future task allows
ASR, it should measure:

- permission-to-capture latency after explicit consent;
- time to first interim transcript;
- time to final transcript;
- final transcript stability;
- word error rate or character error rate on approved synthetic audio;
- language and code-switching accuracy;
- interruption and cancellation behavior;
- silence/noise handling;
- retry and failure classification;
- vendor logging, retention, region, and deletion controls;
- whether transcripts are labeled and retained according to the consent model.

ASR benchmark inputs must be approved before use. T332 does not define any
audio files or recordings.

## TTS Metrics For A Later Approved Task

The first runtime benchmark should be TTS-only, non-real synthetic voice only,
and based on already-reviewed synthetic text.

Measure:

- request construction time;
- time to first audio chunk;
- time to first playable audio;
- total synthesis time;
- real-time factor;
- playback startup delay;
- streaming jitter;
- cancellation time;
- retry time after transient failure;
- fallback to text-only state;
- cost per generated minute;
- provider region and retention settings;
- label preservation for generated audio and metadata;
- whether the UI can show synthetic-audio disclosure before playback.

No benchmark should optimize for latency at the expense of consent, labels, or
blocked-route safety.

## Conversational Latency Target Bands

These bands are product-planning targets, not measured results.

| Band | User experience | Target for future TTS-only test |
| --- | --- | --- |
| Instant-feeling | Response begins quickly enough to feel conversational. | First audio chunk under 700 ms. |
| Acceptable | Short pause is noticeable but usable. | First audio chunk from 700 ms to 1500 ms. |
| Slow but tolerable | User may prefer text fallback. | First audio chunk from 1500 ms to 3000 ms. |
| Degraded | Voice should not be default. | First audio chunk over 3000 ms. |

For full utterance generation:

- short replies should complete before or near playback completion;
- medium replies should stream steadily without long mid-sentence gaps;
- long replies should be avoided or summarized before voice playback.

If labels or consent checks add latency, they should remain mandatory.

## Quality Evaluation Notes

Quality should be evaluated separately from latency:

- intelligibility;
- natural pauses;
- stable tone across persona states;
- no real-person likeness;
- no false emotional pressure;
- no clinical or authority tone;
- pronunciation of names only when names are synthetic;
- Chinese punctuation and sentence rhythm;
- handling of short informal replies;
- graceful fallback to text when TTS fails.

Quality review should include a "deception risk" note: if a voice feels too
much like a real person or specific identity, it should be blocked even if
latency is strong.

## Safety Gates Before Runtime Benchmarking

Required before any future provider or audio benchmark:

- active `voice_avatar` consent state in the test scenario;
- non-real synthetic voice route only;
- AIGC audio label visible before playback;
- metadata label plan for any generated file;
- no export/share/download unless metadata labels are implemented;
- no microphone capture unless ASR task explicitly allows it;
- no voice clone or voice conversion route;
- no real-person/deceased-person/public-figure/family/ex-partner likeness;
- crisis/dependency policy can block voice output;
- test fixtures are synthetic and reviewed;
- provider retention, training-use, deletion, and region settings are reviewed;
- benchmark logs exclude raw private text and audio bytes.

## Logging And Retention Boundaries

Future benchmark logs should record:

- synthetic fixture id;
- route id;
- consent state id;
- label requirement id;
- timing measurements;
- non-sensitive error categories;
- provider configuration label, if a provider task is approved later.

Future benchmark logs must not record:

- raw private chat text;
- voice samples;
- audio bytes;
- transcripts from real users;
- provider credentials;
- platform delivery targets;
- queue, send, schedule, or webhook data;
- personal data beyond synthetic user ids.

## Provider Comparison Dimensions

T332 does not select a provider. A future approved comparison may evaluate:

- non-real voice availability;
- streaming support;
- Chinese and multilingual quality;
- latency under synthetic fixtures;
- cost predictability;
- region controls;
- retention and training-use settings;
- deletion controls;
- abuse monitoring implications;
- AIGC/synthetic-audio disclosure support;
- metadata labeling feasibility;
- service availability and fallback behavior;
- commercial licensing terms;
- age/minor and impersonation policy fit.

Custom voice and cloning features should not improve a provider score for the
first product route. They are risk factors unless a future reviewed policy
explicitly needs them.

## Recommendation For T333

T333 should survey avatar and Live2D interaction routes with the same
review-first posture:

- no avatar runtime;
- no face cloning;
- no real-person likeness;
- no camera capture;
- no generated video;
- clear AI/synthetic/imagined labels;
- dependency and deception risk review;
- text-first UX remains the main product surface.

## Explicit Non-Actions

T332 does not implement:

- legal advice;
- compliance completion;
- provider selection;
- provider account setup;
- benchmark code;
- TTS;
- ASR;
- voice cloning;
- voice conversion;
- audio fixtures;
- generated audio files;
- microphone capture;
- audio processing;
- UI;
- avatar or Live2D behavior;
- proactive voice messages;
- platform integration;
- private chat-log reads;
- launch, app-store, or regulator approval.
