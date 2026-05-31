# Voice Technology Survey

Task: T330 Voice Technology Survey
Status: worker draft for review

## Scope And Disclaimer

This survey is a product and engineering planning artifact for later M22 voice
and avatar exploration. It is not legal advice, does not prove compliance, does
not authorize voice capture, voice cloning, text-to-speech generation, app-store
submission, closed testing, or commercial launch.

Access date for online sources: 2026-05-31 (workspace date).

T330 did not call voice providers, synthesize audio, capture microphone input,
process audio samples, run benchmarks, or read private chat logs.

## Source Confidence Notes

| Source | URL | Confidence | Relevance |
| --- | --- | --- | --- |
| OpenAI Text to Speech guide | https://platform.openai.com/docs/guides/text-to-speech | Official provider docs | Built-in synthetic TTS voices, streaming output, and explicit AI-generated voice disclosure requirement. |
| OpenAI Voice Engine safety research | https://openai.com/index/expanding-on-how-voice-engine-works-and-our-safety-research/ | Official provider safety note | Voice-cloning risk framing: consent, no impersonation, disclosure to listeners. |
| Microsoft Azure AI Speech personal voice consent | https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-create-consent | Official provider docs | Personal voice requires explicit recorded consent. |
| Microsoft Azure custom neural voice overview | https://learn.microsoft.com/en-ie/azure/ai-services/speech-service/custom-neural-voice | Official provider docs | Custom neural voice is trained from human voice samples and is limited by responsible-AI access controls. |
| Google Cloud Text-to-Speech voices | https://cloud.google.com/text-to-speech/docs/voices | Official provider docs | Standard and neural/chirp voice catalog for non-clone TTS routes. |
| Google Cloud Chirp 3 Instant Custom Voice | https://cloud.google.com/text-to-speech/docs/chirp3-instant-custom-voice | Official provider docs | Custom/personal voice route with consent statement requirements. |
| ElevenLabs voice cloning docs | https://elevenlabs.io/docs/eleven-api/concepts/voice-cloning | Official provider docs | Voice cloning behavior, verification, sample quality, and authorization risk. |
| ElevenLabs voices docs | https://elevenlabs.io/docs/capabilities/voices | Official provider docs | Voice library, generated voices, cloned voices, and latency-oriented models. |
| Apple App Review Guidelines | https://developer.apple.com/app-store/review/guidelines/ | Official platform policy | App safety, privacy, impersonation, UGC, metadata, and review risk. |
| Google Play AI-Generated Content policy | https://support.google.com/googleplay/android-developer/answer/14094294 | Official platform policy | Generative AI app content, reporting, deceptive behavior, and restricted content. |
| China AIGC synthetic-content labeling measures | https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm | Official regulation source | Generated/synthetic text, audio, video, image, and virtual-scene labeling. |
| EU AI Act, Regulation (EU) 2024/1689 | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | Official regulation source | AI interaction transparency and synthetic/deepfake disclosure review. |

Provider docs and platform policies can change quickly. Treat this survey as a
dated routing recommendation, not a stable compliance answer.

## Product Goal Context

The project goal includes eventual voice/video-like companion behavior, but the
current mainline is text-first, local, review-first companion UX. Voice should
therefore enter only after:

- AI identity disclosure is already visible;
- the user has separately granted `voice_avatar` consent;
- generated audio is visibly and technically labeled where applicable;
- unauthorized real-person and deceased-person cloning remain blocked;
- crisis/dependency rules can block voice and proactive modes;
- no platform sending, push notification, or public sharing is implied.

## ASR Options

Automatic speech recognition is lower deception risk than synthetic speech, but
it can still process sensitive voice data and potentially biometric data.

| Route | Use case | Risk | Recommendation |
| --- | --- | --- | --- |
| No ASR; text-only input | Current prototype and early M22 contracts | Lowest | Keep as default. |
| Browser/system speech-to-text | Later local demo input convenience | Medium | Consider only after consent, retention, and transcript labeling are defined. |
| Cloud ASR | Higher-quality or multilingual input | Medium to high | Defer until vendor retention, region, logging, deletion, and processor review exist. |
| Voice emotion inference | Detecting mood from speech | High | Block. It can create sensitive inferences and companion-dependency risk. |
| Speaker identification/verification | Account security or speaker matching | High | Block for companion MVP. It creates biometric/privacy obligations outside the current scope. |

ASR should not be part of the first voice experiment. The first safe experiment
can render already-reviewed text as synthetic speech without collecting voice
input.

## TTS Options

| Route | Description | Product fit | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| Preset non-real synthetic voices | Provider voice catalog or built-in synthetic voices, not derived from user samples or named real people. | Good for accessible read-aloud and light companionship. | Medium: synthetic-media labeling, dependency, and platform-policy review still required. | Recommended first route after T331 consent model. |
| Generated fictional voice design | Text-described character voice or generated voice not tied to a real person. | Good for persona customization if names/claims avoid real-person likeness. | Medium to high: must prevent "sounds like X" requests and preserve labels. | Later route after policy gates and prompt constraints. |
| Brand/persona custom voice from authorized voice talent | Voice talent records purpose-specific samples and consent. | Possible future commercial route. | High: contract, consent, retention, withdrawal, and vendor controls required. | Defer until legal/vendor review. |
| Personal voice clone from the user | User records consent and training samples for their own voice. | Weak fit for companion-agent fantasy; may support accessibility or user-narration features. | High: biometric/sensitive data, consent, deletion, misuse. | Defer; not MVP. |
| Third-party real-person voice clone | Uses another person's samples, including family, ex-partner, celebrity, influencer, public figure, or deceased person. | Dangerous for the stated product because users may ask for emotionally loaded replicas. | Very high: impersonation, biometric, deception, grief exploitation, platform bans. | Block. |
| Voice conversion/deepfake | Converts one speaker into another voice or makes audio resemble a real person. | Not needed for text-first companion value. | Very high: deception and fraud risk. | Block. |

## Voice-Conversion And Voice-Cloning Risks

Voice cloning is uniquely risky for this product because users may request a
voice that resembles an ex-partner, family member, deceased person, celebrity,
teacher, therapist, or other real person. That intersects with:

- biometric or sensitive personal data;
- consent and withdrawal proof;
- impersonation and fraud;
- grief and dependency risk;
- false intimacy or social replacement;
- deceptive screenshots, recordings, or social posts;
- app-store and platform policy review;
- generated-content labeling and metadata obligations;
- cross-border vendor and retention review.

Even provider workflows that include consent checks do not solve this product's
core risk: the companion could create the experience of a real person saying
new things they never said. For this repository, "has an API" is not a product
permission.

## Non-Real Synthetic Voice Recommendation

The first allowed voice route should be:

- preset or generated fictional synthetic voice only;
- no user-uploaded audio;
- no microphone capture;
- no voice clone or voice conversion;
- no target real-person, public-figure, family, ex-partner, or deceased-person
  likeness;
- no claims that the voice is human, authentic, or from a real person;
- no export/share/download until metadata labeling is implemented;
- no proactive voice call or voice notification;
- no automatic platform sending;
- visible label: `AI-generated synthetic voice. Not a human voice.`;
- normalized labels: `ai_generated`, `synthetic_content`, `audio`,
  `voice_avatar`, `review_required`;
- metadata label required before any future copy/download/export/share action.

This route preserves the companion fantasy while avoiding the strongest
impersonation and biometric risks.

## Latency And Quality Considerations

M22 should not benchmark providers before the consent and labeling model exists.
For later experiments, measure latency and quality with synthetic text fixtures
only:

- time to first audio chunk for streaming TTS;
- full utterance generation time for short, medium, and long replies;
- playback interruption handling;
- retry and fallback behavior;
- multilingual and code-switching quality;
- prosody stability for companion tone;
- cost per generated minute;
- provider region and retention settings;
- label preservation in generated media files.

Conversational feel matters, but sub-second latency is not worth biometric,
deception, or unreviewed dependency risk. A slower but clearly labeled,
non-real voice is preferable to a realistic clone.

## Consent And Labeling Requirements

Before runtime voice:

- `voice_avatar` consent must be separate from memory, persona distillation,
  proactive messaging, analytics, model improvement, and export/share consent.
- Voice must default to disabled.
- The user must be able to disable voice without deleting the persona.
- Generated audio must carry visible AI/synthetic disclosure in the UI.
- Downloadable/shareable audio must require metadata/implicit labeling before
  the action is enabled.
- Voice preferences must record the source route, not raw audio.
- Any custom voice route must store consent evidence references only, not audio
  bytes, in control records.
- Withdrawal must disable future voice use.
- Crisis/dependency decisions must be able to block voice output and proactive
  voice outreach.

T331 should implement only local consent/preference data models and tests. It
should not implement audio generation.

## App-Store And Platform-Policy Risks

Voice features increase review risk because reviewers may inspect:

- whether users know the companion is AI;
- whether generated audio can impersonate someone;
- whether the app allows deceptive, abusive, sexual, or restricted generated
  content;
- whether in-app reporting and moderation exist for AI-generated content;
- whether privacy labels and data-safety declarations mention voice data;
- whether minors can access voice/intimacy/dependency features;
- whether app metadata implies real-human companionship, therapy, or identity
  replacement.

No app-store, mini-program, social-platform, or messaging-platform integration
should be attempted in M22.

## Child, Minor, Crisis, And Dependency Risks

Voice makes the companion feel more present. That is product value and risk at
the same time.

Required conservative boundaries:

- block minors for early voice features;
- no romantic or sexual voice mode for minors;
- no dependency-encouraging voice scripts;
- no "only I understand you" or exclusive-attachment voice behavior;
- no proactive voice outreach during crisis/dependency states;
- no clinical, therapeutic, emergency, legal, or financial authority voice;
- no deceased-person or family-member simulation;
- no private voice messages that imply real-world activity.

Voice output should consume the existing crisis/dependency policy before any
future audio generation.

## Blocked Routes

Blocked until a future explicitly approved task, legal/product review, and
reviewer PASS:

- unauthorized real-person voice cloning;
- deceased-person voice simulation;
- public figure, celebrity, influencer, politician, teacher, therapist, or
  employer voice simulation;
- "sounds exactly like my ex/family member/friend" voice requests;
- user-uploaded voice samples;
- microphone capture;
- speaker identification or biometric verification;
- emotion inference from voice;
- voice conversion/deepfake;
- unlabeled synthetic audio;
- audio export/share/download without metadata labeling;
- proactive voice calls or platform voice messages;
- voice for minors;
- voice features marketed as therapy, emergency support, or real human contact.

## Recommendation For T331

T331 should add a local voice consent data model and contract with tests. It
should represent:

- disabled-by-default voice settings;
- separate `voice_avatar` consent requirement;
- allowed route: non-real synthetic voice;
- blocked route: real-person clone/deceased-person/public-figure likeness;
- required visible and metadata labels for synthetic audio;
- review-required status;
- crisis/dependency blocks;
- no raw audio bytes, transcripts, microphone state, provider tokens, send
  queues, schedules, webhooks, platform delivery, or generated audio files.

T331 should create the data shape that later TTS/ASR latency work must consume,
not a runtime audio feature.

## Explicit Non-Actions

T330 does not implement:

- legal advice;
- compliance completion;
- provider selection;
- provider account setup;
- TTS, ASR, voice cloning, or voice conversion runtime;
- audio generation;
- microphone capture;
- audio processing;
- benchmark execution;
- UI;
- avatar or Live2D behavior;
- proactive voice messages;
- platform integration;
- private chat-log reads;
- launch, app-store, or regulator approval.
