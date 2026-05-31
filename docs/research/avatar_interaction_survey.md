# Avatar Interaction Survey

Task: T333 Avatar Interaction Survey
Status: worker draft for review

## Scope And Disclaimer

This survey is a product and engineering planning artifact for later avatar and
Live2D-like companion exploration. It is not legal advice, does not prove
compliance, does not authorize face capture, avatar generation, generated
video, app-store submission, closed testing, or commercial launch.

Access date for online sources: 2026-05-31 (workspace date).

T333 did not call avatar providers, generate images/video, process face data,
capture camera input, run browser demos, implement Live2D, or read private chat
logs.

## Source Confidence Notes

| Source | URL | Confidence | Relevance |
| --- | --- | --- | --- |
| Live2D Cubism SDK for Web manual | https://docs.live2d.com/en/cubism-sdk-manual/cubism-sdk-for-web/ | Official technical docs | Web-based Live2D route and SDK distribution constraints. |
| Live2D SDK license | https://www.live2d.com/en/sdk/license/ | Official license docs | Commercial/public distribution needs license review. |
| VRM format docs | https://vrm.dev/en/vrm/gltf/format/ | Official/primary format docs | 3D humanoid avatar file format route. |
| Khronos glTF 2.0 | https://www.khronos.org/gltf | Official standards body | Runtime 3D asset delivery route used by many avatar pipelines. |
| Google MediaPipe Face Landmarker for Web | https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker/web_js | Official provider docs | Camera/image/video face landmark route and biometric/privacy risk boundary. |
| Ready Player Me overview | https://docs.readyplayer.me/ready-player-me/what-is-ready-player-me | Official provider docs | Third-party avatar creator and GLB avatar route. |
| Ready Player Me Avatar Creator docs | https://docs.readyplayer.me/ready-player-me/api-reference/avatar-creator | Official provider docs | iframe/WebView creator, postMessage events, account/session/vendor risks. |
| Apple App Review Guidelines | https://developer.apple.com/app-store/review/guidelines/ | Official platform policy | App safety, privacy, impersonation, metadata, and UGC review risk. |
| Google Play AI-Generated Content policy | https://support.google.com/googleplay/android-developer/answer/14094294 | Official platform policy | AI-generated restricted content, deceptive behavior, and reporting expectations. |
| China AIGC synthetic-content labeling measures | https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm | Official regulation source | Generated/synthetic image, video, audio, virtual-scene labeling. |
| China Deep Synthesis Provisions | https://www.cac.gov.cn/2022-12/11/c_1672221949318230.htm | Official regulation source | Deep synthesis and synthetic-media labeling/review risk. |
| EU AI Act, Regulation (EU) 2024/1689 | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | Official regulation source | AI interaction transparency and synthetic/deepfake disclosure review. |

Provider docs, SDK licenses, and platform policies can change quickly. Treat
this survey as dated routing guidance, not a launch decision.

## Product Goal Context

The product goal includes video-like or Live2D-style companion presence. For
the current project stage, the useful product question is not "can we animate a
person?" It is "can a transparent AI companion have a lightweight visual
presence without impersonating a person or increasing dependency risk?"

Avatar exploration should therefore preserve the text-first foundation:

- chat remains the primary surface;
- avatar is optional decoration or presence, not identity proof;
- AI/synthetic labels remain persistent;
- user can pause/hide animation;
- no face clone, real-person likeness, or deceased-person simulation;
- no camera capture or face tracking in early experiments;
- no generated video or fake video call;
- no platform publishing or outbound messaging.

## Avatar Route Taxonomy

| Route | Description | Product fit | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| Static fictional portrait | Original or licensed non-real persona image, clearly AI/synthetic if generated. | Good first visual anchor for text-first UX. | Low to medium: labeling and asset rights still matter. | Recommended first visual route. |
| Simple sprite / CSS / canvas animation | Blinking, idle, emotion-state sprite, or small loop using non-real art. | Good for lightweight presence without heavy runtime. | Medium: can still intensify attachment if too humanlike. | Recommended before Live2D. |
| Live2D-style 2D rig | Rigged 2D fictional model with idle and expression motions. | Strong companion feel with controllable style. | Medium: license, asset rights, attachment/deception risk. | Defer until text-first demo and consent/label review. |
| 3D stylized VRM/glTF avatar | Non-real stylized 3D character rendered with a web/native engine. | Useful later for interactive presence. | Medium to high: performance, licensing, uncanny likeness, data controls. | Defer; not M22 runtime. |
| Third-party avatar creator | Ready-made creator/SDK, potentially user-customizable avatars. | Useful for user self-expression or persona visuals. | High: accounts, URLs, public assets, selfie/camera options, vendor policy. | Defer behind vendor/privacy review. |
| Camera-driven expression tracking | User camera maps facial landmarks to avatar expressions. | Useful for video-call-like interaction. | Very high: face/camera data, biometric/sensitive inference, minors. | Block for MVP. |
| Generated talking-head video | Model creates video of an avatar speaking. | High visual realism. | Very high: deepfake/deception, compute, labels, dependency. | Block. |
| Real-person face clone | Avatar resembles a real person, family member, ex-partner, public figure, or deceased person. | Dangerous for this product goal. | Critical: impersonation, grief, dependency, biometric/likeness rights. | Block. |

## Route Details

### Static Fictional Portrait

Lowest-risk visual route for a future web demo:

- use original, licensed, or clearly generated non-real art;
- keep it stylized rather than photoreal;
- show persistent AI/synthetic label;
- do not claim the image is the companion's real body or camera feed;
- allow users to hide it;
- preserve generated-image metadata labels before any download/share.

### Simple Sprite Or Canvas Animation

Recommended before full Live2D:

- idle blink, subtle breathing, expression state, typing state;
- no lip-sync to real-person voice;
- no camera input;
- no face tracking;
- no high-realism video;
- animation can pause automatically during crisis/dependency states;
- text remains primary, so failure falls back cleanly.

This route can deliver emotional presence while keeping implementation,
licensing, and deception risk lower.

### Live2D-Style 2D Rig

Live2D is a plausible later route for an anime/stylized companion. Risks:

- SDK and distribution license review;
- model asset ownership and creator permissions;
- attachment/dependency intensity;
- lip-sync and gaze behavior can feel more intimate than text;
- generated or user-customized character assets still need labels;
- mobile/web performance and accessibility need testing.

Recommendation: do not implement in M22. If a later milestone uses Live2D,
start with a non-real fictional model, local idle animation only, visible AI
label, pause control, no camera, no face tracking, no voice clone, and no
export/share.

### 3D VRM/glTF Avatar

VRM/glTF routes are useful when the product needs reusable 3D characters, but
they add:

- asset loading/performance work;
- animation state complexity;
- licensing and model provenance requirements;
- more realistic embodiment and attachment risk;
- accessibility and mobile battery concerns.

Recommendation: defer until after a text-first web demo proves that avatar
presence improves comprehension and companionship without increasing deception.

### Third-Party Avatar Creator

Avatar creator services can reduce asset work, but they introduce vendor and
privacy risk:

- account/session handling;
- public avatar URLs or downloadable GLB assets;
- local browser storage or WebView state;
- selfie or camera-based creation paths;
- SDK license and commercial terms;
- platform permissions such as camera, microphone, photo library, or storage.

Recommendation: do not use a third-party avatar creator until vendor review,
privacy review, and asset-rights review are complete.

### Camera Tracking And Face Landmarks

Face landmark systems can enable avatar expression tracking, but they process
camera images/video and may reveal sensitive biometric or emotional information.

Recommendation: block for MVP and M22. A future task would need separate
camera/face consent, retention/deletion controls, local-vs-cloud processing
decision, minor policy, and security review.

### Generated Video / Talking Head

Generated talking-head video is too realistic and too expensive for the next
product step. It also creates the strongest synthetic-media and deepfake
labeling burden.

Recommendation: block until the product has a reviewed reason, strict labels,
export metadata, impersonation controls, and adversarial policy review.

## Consent And Labeling Requirements

Before any avatar runtime:

- avatar/visual consent must be separate or explicitly covered by a reviewed
  `voice_avatar` scope;
- visual avatar must default to disabled or hidden in safety-sensitive states;
- user must be able to hide/pause animation without deleting the persona;
- generated image/video/virtual-scene labels must be visible;
- metadata labels are required before copy/download/export/share;
- asset provenance and license refs must be tracked;
- real-person likeness requests must be blocked;
- camera/face tracking needs separate consent and retention controls;
- crisis/dependency policy must be able to suppress intimate animation, gaze,
  lip-sync, or proactive visual prompts.

Suggested visible label for a future avatar surface:

```text
AI-generated synthetic fictional avatar. Not a real person or live video.
```

## Dependency And Minor Risks

Avatar features increase perceived presence. Conservative boundaries:

- block minors for early avatar features;
- no romantic/sexual avatar modes for minors;
- no full-screen fake video-call mode;
- no "I am watching you" copy or gaze behavior;
- no manipulative sad/jealous animations;
- no dependency-oriented reactions when the user leaves;
- no avatar behavior that claims real-world activity;
- no crisis support avatar that looks like a clinician, authority figure, or
  real person.

Avatar animation should become calmer or hidden, not more intense, when
dependency or crisis risk is present.

## UI Safety Posture For Future Demo

If a later milestone builds a web demo, start with:

- text-first layout;
- small optional avatar panel;
- persistent AI/synthetic label near the avatar;
- pause/hide button;
- no camera permission prompt;
- no microphone prompt;
- no fake video-call chrome;
- no download/share;
- no photoreal human imagery;
- no real-person names or likeness settings;
- safety state can replace avatar with a neutral label or hidden state.

This keeps the avatar subordinate to the transparent chat/memory/control UX.

## Blocked Routes

Blocked until a future explicitly approved task, legal/product review, and
reviewer PASS:

- real-person face clone;
- deceased-person avatar simulation;
- public figure, celebrity, influencer, politician, teacher, therapist, or
  employer likeness;
- "make it look exactly like my ex/family member/friend" requests;
- camera capture;
- face landmark tracking;
- emotion inference from face;
- generated talking-head video;
- photoreal fake video call;
- unlabeled generated image/video/avatar;
- downloadable/shareable avatar media without metadata labeling;
- avatar for minors;
- avatar marketed as therapy, emergency support, or real human contact;
- platform publishing or social-feed posting of generated avatar media.

## Recommendation For T334

T334 should review M22 as a milestone:

- T330 voice route survey;
- T331 voice consent data model;
- T332 benchmark plan;
- T333 avatar interaction survey.

If M22 passes with warnings, the next milestone should shift from research to a
text-first web demo that uses only already-reviewed contracts. Voice/avatar
runtime should remain optional and blocked until later.

## Explicit Non-Actions

T333 does not implement:

- legal advice;
- compliance completion;
- provider selection;
- provider account setup;
- generated image/video;
- face clone;
- avatar runtime;
- Live2D runtime;
- camera capture;
- face tracking;
- audio/video processing;
- UI;
- browser demo;
- proactive visual messages;
- platform integration;
- private chat-log reads;
- launch, app-store, or regulator approval.
