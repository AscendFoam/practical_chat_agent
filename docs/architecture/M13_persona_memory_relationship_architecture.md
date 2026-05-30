# M13 Persona / Memory / Relationship Architecture

## Status

This is a T240 architecture draft. It describes target boundaries for M14-M22
and does not claim implementation.

## Seven-Engine Target Architecture

```text
Persona Compiler
  -> Memory OS v2
  -> Relationship Engine
  -> Dialogue Engine
  -> Proactive Engine
  -> Virtual Life Engine
  -> Safety & Compliance Engine
```

### Persona Compiler

Transforms user inputs into a versioned `PersonaCard` with source policy,
fictional identity disclosure, traits, speech style, relationship model,
growth policy, proactive preferences, and safety policy.

Initial inputs:

- detailed user description;
- fuzzy preference;
- template;
- random seed.

Future gated input:

- de-identified style inspiration from user-provided material.

Non-goals:

- unauthorized clone;
- real-person replica;
- voice/face identity;
- private raw chat-log committed output.

### Memory OS v2

Separates memory by type, truth status, provenance, lifecycle, sensitivity, and
retrieval permission.

Required memory state separation:

- factual memory: evidence-backed claims about user/persona interactions;
- inferred memory: model/user-approved inference with confidence and source;
- relational memory: relationship state, rituals, conflicts, repairs, trust;
- procedural memory: preferences for interaction and workflow;
- imagined memory: dreams, virtual-life events, fictional diary, role dynamics.

Imagined memory must never be retrieved as evidence for factual claims.

### Relationship Engine

Maintains relationship semantics without turning them into a manipulation
lever. It should guide tone, boundary, pacing, repair, and proactive
eligibility only through explicit policies.

Possible dimensions:

- familiarity;
- trust;
- intimacy;
- boundary comfort;
- conflict/repair state;
- initiative balance;
- dependency risk;
- shared rituals.

### Dialogue Engine

Generates reviewable or runtime-visible chat responses from persona, current
conversation, retrieved memory, relationship state, and safety policy.

Near-term rule:

- preserve review-first discipline when introducing new behavior;
- do not collapse dialogue generation with outbound sending;
- do not roleplay as a real third party.

### Proactive Engine

Creates proactive candidates only after consent and policy checks. It should
start as review-first and in-app/sandbox only.

Inputs:

- proactive consent;
- persona preferences;
- relationship state;
- calendar/memory events if user-approved;
- no-response and quiet-hours state;
- safety and dependency risk.

Outputs:

- candidate message;
- reason;
- consent basis;
- risk flags;
- review card data.

### Virtual Life Engine

Creates text-first role dynamics, AI-labeled virtual diary entries, fictional
posts, worldline events, and optional synthetic media placeholders in later
milestones.

Rule:

- virtual life content is imagined memory unless explicitly linked to factual
  user interaction as provenance.
- It must never imply a real person performed a real-world action.

### Safety & Compliance Engine

Cross-cuts every engine:

- AI identity labels;
- source and consent policy;
- L1-L5 clone/persona risk tiering;
- AIGC labeling;
- memory deletion/freeze/export;
- minor protection;
- dependency and crisis policy;
- platform policy readiness;
- audit trail.

## Data Flow

```text
User creation input
  -> source/risk classification
  -> Persona Compiler
  -> PersonaCard draft
  -> user preview / edit / approve
  -> versioned PersonaCard
  -> Dialogue Engine
  -> Memory OS v2 retrieval bundle
  -> Relationship Engine context
  -> Safety & Compliance checks
  -> response candidate or proactive candidate
  -> review / user control surface
```

Virtual life flow:

```text
PersonaCard + imagined-memory policy
  -> Virtual Life Engine
  -> RoleDynamicPost / VirtualDiaryEntry
  -> AIGC label + imagined-memory link
  -> review / user-visible life stream
  -> no factual-memory contamination
```

Proactive flow:

```text
Consent settings + relationship state + memory event
  -> Proactive Engine
  -> ProactivePolicy gate
  -> review card candidate
  -> in-app/sandbox only
  -> no external automatic sending
```

## M14-M22 Dependency Map

| Milestone | Depends on | Unlocks |
| --- | --- | --- |
| M14 Persona Compiler | T240 boundary pack | Safe L1 persona schemas and local creation |
| M15 Memory OS v2 | M14 persona source policy | Provenance-safe memory separation and imagined-memory isolation |
| M16 Relationship Engine Consumption | M15 memory semantics and existing M8 state | Relationship-aware dialogue/proactive adapters |
| M17 Proactive Engine Consent | M16 relationship policy | Consent-based in-app/sandbox proactive candidates |
| M18 Virtual Life Stream | M15 imagined memory + M17 proactive consent | AI-labeled role dynamics and life stream |
| M19 Memory/Persona Control Surface | M14-M18 state models | Inspect/edit/delete/freeze/export/audit flows |
| M20 Compliance And Safety Baseline | M14-M19 data models | Consent center, labeling, minor/crisis policy baseline |
| M21 Text-First Product UX Prototype | M20 safety baseline | End-to-end closed test UX |
| M22 Voice And Avatar Exploration | M20 baseline + M21 UX evidence | Authorized voice and non-real avatar sandbox |

## Non-Goals

- No live platform delivery.
- No external automatic sending.
- No unauthorized clone or deceptive impersonation.
- No voice cloning, face deepfake, or real-person avatar.
- No raw private-content commit.
- No claim that legal compliance, app-store readiness, or commercial launch is
  complete.

## Architecture Review Rules

Future reviewers should block changes that:

- merge imagined memory into factual retrieval;
- treat relationship state as a retention/manipulation score;
- treat proactive consent as implied by chat usage;
- treat dry-run/sandbox artifacts as live delivery;
- copy private/raw content into committed docs, examples, tests, or summaries;
- add real-person clone capability without a later explicitly approved legal
  and safety task.
