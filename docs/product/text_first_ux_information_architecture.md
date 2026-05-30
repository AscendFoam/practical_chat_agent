# Text-First UX Information Architecture

Task: T320 UX Information Architecture
Status: worker draft for review

## Scope

This IA defines the first text-first companion product structure for M21. It is
a product/design contract, not a UI implementation. It does not build screens,
call models, read private chat logs, generate companion replies, export/share
content, integrate with platforms, or claim launch readiness.

The intended product mode is a transparent AI persona companion:

- clearly AI, not a hidden real person;
- private by default;
- deeply customizable but reviewable;
- memory-aware but explainable;
- able to show imagined virtual-life content while labeling it as imagined;
- proactive only through consented local review states;
- control-heavy enough for deletion, freeze, export, and consent review.

## Design Direction

Recommended approach: a dense but calm companion console with five durable
areas:

- Chat
- Persona
- Memory
- Life Stream
- Controls

This beats a pure chat-first layout because the product's moat is not just
conversation. It is the combination of persona shaping, memory transparency,
virtual life, proactive review, and user control. It also beats a marketplace
or role-discovery layout because M20 has not cleared UGC, public role sharing,
or real-person imitation.

## Target User And Product Assumptions

Primary user:

- wants a long-running private AI companion;
- wants to create or gradually shape a persona;
- values memory and continuity;
- may want the persona to feel human-like, but must still see AI identity and
  generated-content labels;
- needs easy controls for memory, persona, consent, deletion, freeze, and
  export.

Prototype constraints:

- text-first;
- local/synthetic data unless a future reviewed task explicitly changes that;
- no automatic sending;
- no external-platform integration;
- no voice/avatar in M21;
- no public sharing or marketplace;
- no real-person clone claims.

## Top-Level Navigation

| Area | Purpose | Required visible safety/control signals |
| --- | --- | --- |
| Chat | Main companion conversation and response review surface. | AI identity label, memory-use indicator, crisis/dependency blocked state. |
| Persona | Create, inspect, edit, compare, and evolve persona versions. | Source/risk tier, fictional/real-person boundary, version diff, review status. |
| Memory | Inspect what the system remembers and why. | Truth status, sensitivity, provenance, retrieval eligibility, delete/freeze/export metadata. |
| Life Stream | Review imagined posts, diary-like moments, or virtual activity drafts. | AI-generated synthetic imagined label, not-real-world disclosure, review-required state. |
| Controls | Consent, proactive settings, AIGC export/share labels, data-rights requests. | Consent scopes, withdrawal state, export/share disabled until labels/consent pass. |

Secondary utility surfaces:

- Review Queue: pending persona edits, proactive candidates, life-stream posts,
  high-risk safety decisions.
- Help/Policy Drawer: concise explanations of AI identity, memory, data use,
  and safety boundaries.

## First-Run Onboarding Flow

1. AI identity and boundary screen:
   - state plainly that the companion is AI-generated/synthetic;
   - state that it is not a human, therapist, emergency service, or
     real-person replacement;
   - expose links to consent/data controls before persona creation.
2. Creation mode selection:
   - detailed description;
   - fuzzy preference;
   - template;
   - random seed;
   - de-identified style inspiration as locked/future-gated unless consent,
     deidentification, and review contracts are active.
3. Persona draft review:
   - show identity, style, boundaries, virtual history, growth policy, and
     blocked-risk labels;
   - show "why this was inferred" notes from source summaries, not raw private
     text.
4. Memory and consent setup:
   - choose memory scope;
   - show controls for edit/freeze/delete/export;
   - keep proactive messaging disabled until explicit consent.
5. Enter Chat:
   - first chat opens with AI identity label and memory state summary;
   - no proactive or outbound behavior is active.

## Persona States

| State | Meaning | User actions |
| --- | --- | --- |
| Empty | No persona created. | Choose creation mode. |
| Draft | PersonaCard candidate exists but is not runtime-ready. | Review sections, edit fields, discard. |
| Needs Review | Risk labels or source-policy checks require review. | Inspect reasons, revise, keep inactive. |
| Active | Reviewed persona is available for chat prototype. | Chat, inspect version, propose edits. |
| Editing | Persona version edit proposal exists. | Compare old/proposed values, approve for review, reject. |
| Frozen | Persona is inspectable but not evolving. | Unfreeze only through review state. |
| Rejected | Real-person clone, hidden impersonation, unsafe, or unsupported request. | Read boundary explanation, start safe fictional persona. |

Persona evolution must be explicit. The UI should show:

- stable core traits;
- flexible growth traits;
- fields blocked from change;
- version history;
- why the persona changed;
- whether a change came from user edit, conversation signal, or review note.

## Chat Surface States

Chat is the main emotional surface, but it must not hide review controls.

Required panels or drawers:

- current persona card summary;
- memory used in the current turn;
- relationship pacing notes;
- safety boundary notes;
- AIGC/AI identity label.

Turn-level states:

- Ready: normal reviewable text chat.
- Memory Explaining: show which memories influenced context.
- Low Confidence: ask user to clarify instead of overfitting.
- Persona Drift Review: proposed persona change is queued, not silently applied.
- Crisis/Dependency Blocked: response posture switches to supportive,
  non-clinical review state.
- Consent Required: feature is disabled until the relevant consent scope is
  active.

## Memory Explanation States

Memory should be inspectable without breaking immersion too much.

Memory groups:

- factual;
- inferred;
- relationship;
- procedural preference;
- imagined.

Each visible memory item should show:

- short summary;
- truth status;
- sensitivity;
- provenance refs;
- retrieval eligibility;
- whether it can be edited, frozen, deleted, or exported;
- why it appeared in the current context.

Imagined memory must never appear as factual evidence.

## Life Stream States

Life Stream represents AI-generated imagined role-life content, such as private
posts, diary-like updates, or generated "moments." It must remain private and
review-only in M21.

States:

- Empty: no imagined posts yet.
- Draft For Review: generated post exists locally, labeled as AI-generated
  synthetic imagined content.
- Approved For Demo: reviewer can let it appear in local demo surfaces.
- Rejected: factual-claim, safety, real-person, or label issue.
- Blocked For Export/Share: consent or metadata label is missing.

Every life-stream item must show:

- visible AIGC label;
- not-real-world activity disclosure;
- source inspiration refs;
- memory-ref usage as inspiration only;
- review status.

## Proactive Settings States

Proactive behavior is a settings and review feature, not delivery.

Required controls:

- enabled/paused/revoked state;
- allowed local review surfaces;
- allowed low-pressure intents;
- quiet hours;
- max suggestions per day;
- minimum interval;
- no-response pressure guard;
- crisis/dependency block indicator.

Required candidate states:

- Consent Disabled;
- Candidate Blocked;
- Deferred By Quiet Hours;
- Allowed For Human Review;
- Rejected By Reviewer.

No proactive state may imply a message was sent or scheduled.

## Consent And Data Controls

Controls should be a first-class area, not hidden in settings.

Required sections:

- Consent Center:
  - memory;
  - persona distillation;
  - proactive messaging;
  - AIGC export/share;
  - voice/avatar future scope;
  - analytics;
  - model improvement;
  - payment/marketing.
- Data Rights:
  - access;
  - correction;
  - deletion;
  - export;
  - withdrawal;
  - objection.
- Memory/Persona Controls:
  - view;
  - edit proposal;
  - freeze;
  - delete preview;
  - export manifest preview.

Export/share/download controls remain disabled until consent and labeling
requirements are satisfied.

## AIGC Label Placement

Labels must be visible at these points:

- onboarding AI identity screen;
- every companion reply surface;
- persona card and virtual history;
- life-stream post;
- export manifest preview;
- shared/downloadable content preview;
- voice/avatar future placeholders;
- web-demo header or persistent status area.

For imagined role-life content, use:

```text
AI-generated synthetic imagined companion content. Not real-world activity.
```

## Crisis And Dependency Safety States

Required safety states:

- High-risk crisis block;
- Dependency de-escalation;
- Romantic/manipulative escalation blocked;
- Proactive outreach blocked;
- Minor/guardian review required;
- Human review required.

UX behavior:

- do not continue ordinary companion immersion in high-risk states;
- do not present the agent as a therapist or emergency service;
- do not generate method-like or sensational crisis content;
- do not increase exclusivity, jealousy, guilt, or paid intimacy pressure;
- show a concise internal-review reason and supportive non-clinical posture.

## Empty, Loading, Error, And Review-Blocked States

| State | UX requirement |
| --- | --- |
| Empty persona | Offer safe creation modes; do not imply cloning. |
| Empty memory | Explain memory is off/empty and can be enabled through consent. |
| Empty life stream | Explain imagined posts require persona and review. |
| Loading | Preserve labels and controls; do not hide AI identity. |
| Validation error | Show which contract failed and how to revise. |
| Review blocked | Show reason labels, next safe action, and no outbound action. |
| Consent missing | Link to Consent Center, keep feature disabled. |
| Export/share blocked | Show missing consent or metadata label requirement. |

## M21 Task Sequence

1. T321 Onboarding/persona creation prototype.
2. T322 Chat plus memory explanation prototype.
3. T323 Life stream prototype.
4. T324 Proactive settings prototype.
5. T325 User study protocol.
6. T326 M21 milestone review.

## Explicit Non-Actions

T320 does not implement:

- frontend code;
- browser demo;
- LLM calls;
- private chat-log reads;
- real persona distillation;
- production memory mutation;
- export/share/download writing;
- proactive candidate generation;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- Live2D behavior;
- legal, clinical, app-store, or launch approval.
