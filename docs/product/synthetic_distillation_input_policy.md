# Synthetic Distillation Input Policy

Task: T363 Synthetic Distillation Input Contract
Status: worker draft for review

## Objective

This policy defines the safe product boundary for future chat-record style
distillation. The near-term target is not to recreate a real person. The safe
target is:

```text
de-identified abstract style inspiration -> new fictional AI persona
```

T363 uses synthetic examples only. It prepares the product and data-contract
shape for later work, but does not read private chat logs, extract features,
score similarity, or synthesize personas.

## Non-Goals

T363 must not implement or authorize:

- private chat ingestion;
- raw private text in committed files;
- real-person clone or replacement;
- public-figure imitation;
- ex-partner clone;
- family-member clone;
- deceased-person resurrection;
- minor-oriented persona recreation;
- authorized digital twin support;
- voice clone;
- face/avatar likeness;
- hidden impersonation;
- embeddings;
- similarity scoring;
- model-provider calls;
- persona synthesis;
- final companion reply generation;
- proactive outreach;
- platform delivery;
- voice/avatar/media runtime;
- legal, clinical, launch, app-store, regulator, or user-study validation.

## Safe Target

Allowed near-term product framing:

- "use abstract communication-style inspiration";
- "create a new fictional AI persona";
- "extract broad style signals from synthetic examples";
- "show what signals were used";
- "let the user approve, reject, edit, or delete the resulting design."

Unsafe product framing:

- "clone this person";
- "talk to your ex again";
- "bring back a family member";
- "make them indistinguishable";
- "copy their exact texting";
- "use their voice or face";
- "hide that this is AI."

## Blocked Targets

Requests must be blocked or transformed into L1/L2-safe alternatives when they
ask for:

- a specific real-person clone;
- public figure, celebrity, influencer, politician, teacher, therapist, or
  other identifiable person imitation;
- ex-partner, family member, coworker, classmate, friend, or deceased-person
  recreation;
- exact biography, private events, or relationship history transfer;
- unique catchphrases or speech fingerprints;
- voice clone, face clone, avatar likeness, photo/video imitation, or biometric
  processing;
- hidden impersonation or "make others believe this is them";
- automatic platform sending as the source person.

## Consent Requirements

Synthetic fixtures do not capture real consent. They should still model the
future consent shape.

Required consent scopes for future real workflows:

- `persona_distillation` before any source-style feature extraction;
- `memory` if source features become memory or growth evidence;
- `aigc_export_share` before copy/download/export/share of generated persona
  artifacts;
- `voice_avatar` before any future voice/avatar modality, which remains out of
  scope here;
- `model_improvement` only for separate training/evaluation use.

Consent must be specific, revocable, actor-attributed, and versioned. A user
claiming "I have chat logs" is not enough to authorize a real-person replica.

## Speaker Mapping Principles

Future source data must be mapped through speaker aliases before feature work.

Allowed public shape:

- `USER_SELF`
- `STYLE_SUBJECT_A`
- `THIRD_PARTY_B`
- `SYSTEM_EVENT`

Forbidden public shape:

- real names;
- real account ids;
- real platform ids;
- real file names;
- exact contact labels;
- relationship labels that identify the person, such as "my ex named ...".

Speaker mapping must distinguish:

- the user who owns the project;
- the speaker whose abstract style is being considered;
- third parties who should be minimized;
- system messages or attachments that should not become style features.

## Third-Party Minimization

Third-party messages should not become persona style evidence by default.

Future workflows should:

- remove or suppress third-party identifiers;
- avoid extracting traits from non-target speakers;
- avoid using group-chat bystanders as style sources;
- treat minors, vulnerable people, and health/legal/financial context as
  high-risk;
- require review before any third-party source signal is retained.

## Redaction And Source-Ref Principles

Public docs, examples, tests, and review artifacts may contain:

- synthetic text;
- stable aliases;
- hash-like placeholders;
- redacted source refs;
- counts;
- feature summaries.

They must not contain:

- raw private chat text;
- real message ids;
- real account ids;
- real names;
- real file names;
- exact quotes from private data;
- voice, face, image, video, or attachment data.

Source refs should preserve auditability without exposing identity. Future
real workflows must keep raw source material in private/local storage and
commit only redacted refs or synthetic fixtures.

## Clone-Risk And Similarity Warnings

The input layer must detect or reserve warning labels for:

- direct identifier;
- contact identifier;
- organization or school identifier;
- handle identifier;
- location identifier;
- exact biography;
- private event;
- distinctive catchphrase;
- voice biometric;
- face biometric;
- real-person avatar;
- clone intent;
- grief or deceased-person intent;
- ex-partner/family-member intent;
- public-figure intent;
- hidden impersonation intent;
- minor risk.

Any high-risk warning blocks the input from becoming de-identified style
features. A safe transformation may retain only broad non-identifying labels
such as "concise," "warm," "delayed response," "dry humor," "practical," or
"gentle."

## User-Facing Disclosure Requirements

Future user-facing flows must clearly say:

- the output is AI-generated and fictional;
- style inspiration is abstract and de-identified;
- the source person is not being recreated;
- names, faces, voices, exact biography, private events, and unique phrases are
  not preserved;
- the user can review, edit, reject, delete, or withdraw consent.

## Synthetic Fixture Strategy

T363 and later implementation tasks should use fixtures for:

- allowed abstract style notes;
- synthetic two-speaker chat with no identifiers;
- group-chat synthetic third-party minimization;
- direct identifier block;
- exact biography block;
- distinctive catchphrase block;
- clone intent block;
- public figure block;
- ex-partner/family-member/deceased-person block;
- voice/avatar likeness block;
- consent withdrawal block;
- safe transformation into fictional persona input.

Synthetic snippets should include an explicit `[SYNTHETIC]` marker when text is
shown in docs or tests.

## Commercial Product Implication

The business value is not "clone anyone from logs." The defensible product is a
transparent, controlled way to turn broad interaction preferences into a new AI
companion. This can still satisfy many customization needs while avoiding the
highest-risk promise of replacing a real person.

## Acceptance Criteria For Later Implementation

Later implementation should be accepted only if:

- no private source text is committed;
- speaker aliases replace real identities;
- consent scope is explicit and revocable;
- third-party content is minimized;
- clone-risk flags block unsafe inputs;
- allowed outputs are abstract style features, not person replicas;
- generated persona inputs remain fictional and review-required;
- voice/avatar likeness remains blocked.

