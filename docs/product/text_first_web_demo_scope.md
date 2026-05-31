# Text-First Web Demo Scope

Task: T340 Text-First Web Demo Scope
Status: worker draft for review

## Scope

This document scopes M23: an integrated local web demo for the transparent AI
companion prototype. It is a product and engineering scope, not an
implementation. It does not build UI, start a server, call models, read private
chat logs, generate media, enable voice/avatar runtime, integrate platforms, or
claim launch readiness.

## Target User Experience

The demo should let a reviewer experience the companion as one coherent local
product:

1. See AI identity and safety boundaries immediately.
2. Create or inspect a safe fictional persona.
3. Enter a chat-like surface with persona and memory explanations.
4. Inspect factual vs imagined memory.
5. Review imagined life-stream content with not-real-world labels.
6. Inspect proactive settings without any sent or scheduled message.
7. Open controls for consent, AIGC labels, deletion/freeze/export previews, and
   future voice/avatar state.

The demo should feel like a practical companion console, not a marketing
landing page. It should be dense, calm, and easy to scan.

## Implementation Direction

Recommended direction for M23:

- dependency-light local web demo;
- static HTML/CSS/JavaScript shell or small Python-served static assets;
- Python state adapter that emits synthetic JSON payloads from existing local
  contracts;
- no large frontend framework until the UX contract is validated;
- no model-provider calls;
- no private data;
- no runtime voice/avatar;
- no outbound platform behavior.

This fits the current repository, which is Python-first and has no committed
frontend package manager setup.

## Surfaces And Routes

| Surface | Demo route | Source contract |
| --- | --- | --- |
| Onboarding | `/onboarding` or initial panel | `TextFirstOnboardingState` |
| Persona | `/persona` or persistent persona drawer | `PersonaCard`, onboarding contract |
| Chat | `/chat` main surface | `TextFirstChatMemoryState` |
| Memory | `/memory` panel | `TextFirstMemoryExplanation`, memory viewer contracts |
| Life Stream | `/life` panel | `TextFirstLifeStreamState` |
| Proactive | `/proactive` panel | `TextFirstProactiveSettingsState` |
| Controls | `/controls` panel | Consent, AIGC labeling, data rights, voice consent |
| Review Queue | `/review` panel | Pending/blocked/review-required states |

The first usable screen may be a single-page app with internal tabs rather than
separate server routes. The important product route is the information
architecture, not URL shape.

## Synthetic Fixture Strategy

T341 should create a synthetic demo payload builder. It should include:

- safe fictional persona fixture;
- blocked real-person clone fixture;
- chat memory fixture with factual and imagined memory;
- crisis/dependency blocked chat fixture;
- life-stream draft fixture;
- proactive enabled/deferred/blocked fixture;
- consent center fixture;
- AIGC label fixture;
- voice consent disabled/review-required/blocked fixture;
- future avatar locked-state fixture.

Fixtures must not include:

- private chat history;
- real third-party names;
- real ex/family/persona clone content;
- crisis narratives beyond synthetic labels;
- audio bytes;
- transcripts;
- generated image/video;
- provider credentials;
- platform delivery fields.

## State-Contract Integration Map

| Demo need | Existing object or task |
| --- | --- |
| AI identity disclosure | `TextFirstOnboardingState.ai_identity_disclosure_text` |
| Persona draft and blocked state | `TextFirstOnboardingPrototype` |
| Persona summary | `TextFirstPersonaSummary` |
| Chat/memory screen | `TextFirstChatMemoryPrototype` |
| Memory provenance | `TextFirstMemoryExplanation` |
| Life-stream item | `TextFirstLifeStreamPrototype` |
| Proactive settings | `TextFirstProactiveSettingsPrototype` |
| Consent scopes | `ConsentCenterState` |
| AIGC visible/metadata labels | `AIGCLabelingRequirement` |
| Crisis/dependency block | `CompanionSafetyPolicy` / `CompanionSafetyDecision` |
| Voice locked/review state | `VoiceConsentPolicy` / `VoicePreferenceState` |
| Avatar locked state | T333 survey until a future avatar contract exists |

T341 should adapt these into one serializable demo state. It should not invent
parallel contracts that bypass the existing models.

## Explicitly Blocked Demo Features

The M23 web demo must not include:

- model-provider calls;
- generated final companion replies from an LLM;
- private chat-log ingestion;
- persona distillation from real chat records;
- automatic memory mutation;
- automatic persona evolution;
- export/share/download writing;
- proactive candidate generation;
- sending, scheduling, notifications, webhooks, queues, or platform delivery;
- TTS/ASR;
- voice cloning;
- microphone capture;
- avatar runtime;
- Live2D runtime;
- camera capture;
- generated images/video;
- face or voice biometric processing;
- public role marketplace;
- launch, app-store, clinical, legal, or compliance sufficiency claims.

## Accessibility And Responsive Layout

Minimum expectations for a future UI task:

- desktop and mobile layouts;
- keyboard-accessible tabs and controls;
- visible focus states;
- text does not overlap or truncate in compact panels;
- labels remain visible in all screen widths;
- controls have stable dimensions;
- no interaction depends only on color;
- pause/hide control for any future animation placeholder;
- reduced-motion friendly behavior;
- readable contrast for labels, warnings, and blocked states.

## Visual And Design Posture

The demo should look like a working companion console:

- restrained, content-forward layout;
- no oversized marketing hero;
- no decorative gradient-orb background;
- no nested cards;
- compact tabs for major areas;
- icon buttons where an icon is clear, with tooltips later;
- persistent status strip for AI identity, consent, and safety state;
- small optional future-avatar placeholder marked locked/research-only;
- no photoreal person imagery;
- no fake video-call frame.

## Safety And Consent Gates

Every demo payload should surface these gates:

- AI-generated/synthetic identity;
- fictional persona boundary;
- real-person clone blocked state;
- memory truth/provenance;
- imagined/not-real-world life-stream label;
- proactive consent and no-send state;
- crisis/dependency de-escalation or block;
- AIGC metadata required before export/share;
- voice/avatar future scope disabled or review-required;
- minors not supported for early companion/voice/avatar flows.

## Local-Only Run Assumption

The demo should run locally with synthetic data. Acceptable future run shapes:

- open a static HTML file directly when no server is required;
- use Python's local static file server if asset loading requires it;
- use a tiny Python app only if T341/T342 explicitly scopes it.

No external services, accounts, tunnels, webhooks, or platform credentials are
allowed in M23 unless a later task explicitly changes scope.

## Implementation Sequence

Recommended M23 task sequence:

1. T341: create local demo state adapter and synthetic JSON payload contract.
2. T342: build static web demo shell consuming the adapter payload.
3. T343: add local state switching for safe, blocked, and review scenarios.
4. T344: add visual QA and browser smoke checks.
5. T345: write web demo user walkthrough and study update.
6. T346: M23 milestone review.

Voice/avatar runtime should not resume until after M23 proves that users
understand the text-first transparency and control model.

## Explicit Non-Actions

T340 does not implement:

- frontend code;
- browser demo;
- dev server;
- model-provider calls;
- private chat-log reads;
- real persona distillation;
- production memory mutation;
- export/share/download writing;
- proactive candidate generation;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- Live2D behavior;
- legal, clinical, app-store, user-study, or launch approval.
