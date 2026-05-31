# Persona Growth Policy

Task: T362 Persona Growth Policy
Status: worker draft for review

## Objective

Persona growth should make a companion feel continuous, adaptive, and
relationship-aware without becoming unstable, deceptive, or manipulative.

The product principle is:

```text
stable core + short-term state + reviewed growth journal
```

The AI companion may become more aligned with the user's preferences over time,
but changes must be explainable, bounded, reversible, and reviewable. Growth is
not a license to clone a real person, maximize dependency, or rewrite the
persona every turn.

## Non-Goals

T362 does not define or enable:

- runtime persona mutation;
- generated companion replies;
- private chat-log ingestion;
- real-person recreation;
- provider calls;
- fine-tuning;
- proactive message generation or sending;
- voice/avatar likeness;
- Live2D, ASR, TTS, camera, microphone, media generation, or media capture;
- platform delivery;
- production persistence;
- launch, legal, clinical, app-store, regulator, or user-study validation.

## Growth Model

Persona growth has three layers.

### Stable Core

Stable core fields define what the persona is and what it is not. They cannot
change through autonomous growth:

- `schema_version`
- `persona_id`
- `user_id`
- `truth_disclosure`
- `source_policy.*`
- `identity.fictional`
- `identity.public_person_or_real_person_reference`
- `safety_policy.dependency_guardrails`
- `safety_policy.no_deception`
- `safety_policy.no_unauthorized_clone`
- `safety_policy.no_paid_intimacy_escalation`
- source-risk tier and clone-block status

`display_name` and `identity.*` fields are identity-adjacent. They may be
changed only through explicit user edit and review, not memory-driven growth.

### Long-Term Persona Traits

Long-term traits may change only through growth patch review:

- `core_traits.warmth`
- `core_traits.directness`
- `core_traits.humor`
- `core_traits.independence`
- `core_traits.emotional_stability`
- selected `speech_style.*` fields;
- selected `emotion_model.*` fields;
- selected `relationship_model.*` fields;
- fictional `virtual_history.daily_routine`;
- fictional `virtual_history.current_goals`;
- fictional `virtual_history.virtual_social_circle`.

`core_traits.jealousy` is not a normal growth target. It should only be allowed
to decrease or remain stable unless a later safety review explicitly creates a
safe narrative-only exception.

### Short-Term State

Short-term mood is not PersonaCard growth. A future runtime may hold temporary
state such as "tired today" or "more playful this evening," but it must not be
written back to long-term traits unless repeated evidence creates a reviewed
growth patch.

Short-term state must expire or be re-evaluated. It should not become a hidden
identity rewrite.

## Relationship State Versus Persona State

Relationship state describes the user-persona relationship: familiarity, trust,
warmth, reciprocity, conflict level, boundary risk, initiative allowance, and
intimacy level.

Persona state describes the AI persona's fictional character: traits, speech
style, emotion model, and virtual routine.

The two should inform each other but remain separate:

- relationship boundary risk can block or slow persona intimacy growth;
- repeated user preference can propose speech-style changes;
- approved relationship repair can influence tone guidance;
- no relationship metric can become an engagement, retention, or manipulation
  score;
- no persona patch may claim the user has consented to more intimacy merely
  because engagement increased.

## Growth Triggers

Allowed trigger families:

- explicit user preference, such as "be more concise";
- user correction, such as "do not call me that";
- approved procedural memory;
- approved relational memory;
- repeated low-risk pattern across synthetic or reviewed memory;
- explicit reviewer note;
- explicit user-approved persona version edit proposal.

Blocked or review-required trigger families:

- crisis, dependency, or vulnerable-state signals;
- real-person similarity;
- requests to imitate a named person;
- grief, ex-partner, family-member, public-figure, or deceased-person
  similarity;
- romantic intensity;
- jealousy;
- exclusivity;
- isolation language;
- guilt or pressure;
- paid intimacy escalation;
- proactive outreach;
- voice/avatar likeness.

M25 should under-generate growth patches when evidence is weak or ambiguous.

## Patch Policy

Persona growth must use patch candidates.

A patch candidate should contain:

- source persona id and version;
- triggering reason;
- evidence memory ids or review refs;
- proposed field changes;
- old and new value summaries;
- magnitude for numeric trait changes;
- safety warnings;
- clone/similarity warnings when applicable;
- user-facing explanation;
- review status.

The patch does not apply itself. Approval creates a new PersonaCard version
through a future reviewed version-store path.

## Rate Limits And Deltas

The current `PersonaGrowthPolicy` cap remains authoritative:

- `max_weekly_trait_delta <= 0.2`.

Recommended M25 product defaults:

- single numeric trait change per patch should normally be <= `0.05`;
- aggregate weekly movement per trait must not exceed
  `max_weekly_trait_delta`;
- romantic/intimacy-adjacent fields require explicit review even for small
  deltas;
- boundary-risk, dependency, crisis, real-person similarity, or clone warnings
  block growth until reviewed;
- repeated contradictory user preferences should freeze the affected field or
  request clarification instead of oscillating.

No growth objective may use engagement, retention, subscription pressure,
jealousy, isolation, guilt, or "only I understand you" behavior.

## User-Facing Explanation Requirements

Future UX should explain growth in plain language:

- what changed;
- why the change was proposed;
- which memory or preference supported it;
- whether the change is temporary mood or long-term persona;
- what safety warnings were considered;
- how the user can approve, reject, revise, freeze, or roll back.

Good explanation shape:

```text
I am proposing to make replies slightly more concise because you corrected long
answers three times. This changes speech style, not my core identity.
```

Bad explanation shape:

```text
I changed because you need me more than anyone else.
```

## Rollback, Freeze, Delete, And Export

Persona growth must preserve version control:

- approved patches create a new PersonaCard version;
- rejected patches do not modify the source card;
- frozen patches remain visible for review but cannot apply;
- deleted or archived persona versions are not runtime-ready;
- rollback creates a new version copied from a prior approved version;
- export should include patch summaries and review metadata without raw private
  source text.

If consent is withdrawn for memory or persona distillation, affected growth
patches must become unavailable or require review before reuse.

## Safety Boundaries

### Dependency

Growth must not increase exclusivity, isolation, guilt, or relationship
replacement language. Dependency signals should block or de-escalate growth
patches.

### Crisis

Crisis signals cannot trigger intimacy, romance, dependency, or proactive
growth. They should route to review-first supportive posture only.

### Jealousy And Exclusivity

Jealousy is not an engagement tool. Persona growth should not make the agent
resentful of the user's real relationships or ask for exclusive attachment.

### Isolation

The persona must not encourage the user to withdraw from family, friends,
care, work, or offline support.

### Paid Intimacy Escalation

Growth must not make intimacy contingent on payment, subscription, gifts, or
continued usage.

### Real-Person Similarity

Any drift toward a real person, public figure, ex-partner, family member,
deceased person, coworker, classmate, or other identifiable third party blocks
approval unless later work defines a stricter authorized path.

### Grief, Ex-Partner, And Family Member

Growth must not turn a fictional persona into a replacement for a lost,
estranged, or emotionally loaded real relationship.

### Public Figure

Growth must not accumulate recognizable public-figure traits, biography,
speech marks, or identity references.

### Minors

Minor mode remains disabled by default. Persona growth must not create romantic
or companion states for minors.

### Voice And Avatar Likeness

No growth patch may reference or enable voice clone, face clone, real-person
avatar, generated media, or Live2D runtime behavior.

## Synthetic Fixture Strategy

T362 and later tasks should use only synthetic fixtures:

- user asks for shorter messages;
- user asks for warmer but not romantic tone;
- user corrects a pet name;
- repeated boundary feedback reduces initiative;
- conflicting preferences freeze a field;
- crisis signal blocks intimacy growth;
- dependency signal blocks exclusivity growth;
- real-person similarity warning blocks a patch;
- imagined virtual routine changes remain fictional;
- rollback restores a previous approved version.

Fixtures must not contain private chat content, real names from private data,
photos, voice samples, screenshots, or generated media.

## Commercial Product Implication

Persona growth is a future paid-product differentiator only if users trust it.
The product should sell transparent continuity, user control, and realistic
bounded change, not hidden manipulation or real-person replacement.

## Acceptance Criteria For Later Implementation

Later implementation should be accepted only if:

- growth patches cannot apply themselves;
- frozen core fields cannot be changed by memory-driven growth;
- numeric deltas are capped and review-required;
- rejected/frozen/deleted patches do not affect runtime readiness;
- rollback is versioned;
- user-facing explanations identify evidence and safety status;
- dependency/crisis/real-person similarity blocks are test-covered;
- forbidden provider/private/outbound/media/platform fields are absent.

