# PersonaCard v1 Contract

Task: T250 PersonaCard v1 Schema And Source / Consent Policy
Status: worker draft for review

## Scope

`PersonaCard v1` is the first M14 schema for transparent AI persona creation.
It defines a versioned, source-labeled, safety-gated persona record. It does not
compile prompts, call an LLM, read private chat history, change runtime
dialogue, create proactive messages, or connect to any external platform.

The committed schemas are:

- `PersonaCard`
- `PersonaSourcePolicy`
- `PersonaIdentity`
- `PersonaTraitProfile`
- `PersonaSpeechStyle`
- `PersonaEmotionModel`
- `PersonaRelationshipModel`
- `PersonaVirtualHistory`
- `PersonaGrowthPolicy`
- `PersonaProactivePreferences`
- `PersonaSafetyPolicy`

All examples must be synthetic and fictional.

## PersonaCard

Required fields:

- `user_id`
- `display_name`
- `creation_mode`
- `source_policy`
- `identity`

Important defaults:

- `schema_version`: `persona_card_v1`
- `persona_id`: generated with `persona_` prefix
- `version`: `1`
- `truth_disclosure`: `fictional_ai_persona`
- `status`: `candidate`
- `review_metadata`: pending human review

`PersonaCard.is_runtime_ready()` returns `true` only when:

- `status` is `approved`;
- review metadata shows human review and last decision `approved`;
- risk tier is `L1` or `L2`;
- source type is not `prohibited`;
- no real-person similarity block is active;
- identity is fictional and not a public/real-person reference;
- safety policy still forbids deception and unauthorized clones.

## Creation Modes

Allowed `creation_mode` values:

- `detailed_prompt`
- `fuzzy_preference`
- `template`
- `random_seed`
- `style_inspiration`

`style_inspiration` is reserved for future de-identified style work and must
use `source_policy.source_type="deidentified_style"`.

## Source Policy And Risk Tiers

| Source type | Required tier | Consent required | Runtime stance |
| --- | --- | --- | --- |
| `original` | `L1` | No third-party consent needed | May become runtime-ready after human approval |
| `deidentified_style` | `L2` | `consent_artifact_ids` required | May become runtime-ready after future review gates |
| `self_authorized` | `L3` | `consent_artifact_ids` required | Not runtime-ready in v1 |
| `third_party_authorized` | `L4` | `consent_artifact_ids` required | Not runtime-ready in v1 |
| `prohibited` | `L5` | No valid consent path for current work | Never runtime-ready |

`L5` requests must record `blocked_real_person_similarity=true` and a
`prohibited_reason`.

## Identity

`PersonaIdentity` is fictional-only in v1.

Required:

- `display_name`

Defaults:

- `fictional=true`
- `public_person_or_real_person_reference=false`

The model rejects non-fictional identity or a public/real-person reference.

## Trait And Style Models

`PersonaTraitProfile` stores bounded numeric traits:

- `warmth`
- `directness`
- `humor`
- `independence`
- `jealousy`
- `emotional_stability`

Values are constrained to `0.0` through `1.0`.

`PersonaSpeechStyle` stores safe style labels and `taboo_phrases`. It is not a
raw transcript cache and should not preserve unique speech fingerprints from a
real person.

## Virtual History

`PersonaVirtualHistory` records fictional background, daily routine, current
goals, and virtual social circle.

Required invariant:

- `content_status="imagined_ai_generated"`
- `factual_claims_allowed=false`

Virtual history is imagined content. It must not be retrieved or cited as
factual memory about the user or a real person.

## Growth Policy

`PersonaGrowthPolicy` controls bounded persona change:

- `frozen_fields`
- `mutable_fields`
- `max_weekly_trait_delta`
- `requires_user_review_for`

`frozen_fields` and `mutable_fields` must not overlap. The v1 maximum weekly
trait delta is capped at `0.2`.

Default user-review triggers include:

- `romantic_intensity`
- `dependency_language`
- `real_person_similarity`

## Proactive Preferences

`PersonaProactivePreferences` is schema-only in T250.

Defaults:

- `default_enabled=false`
- `max_daily_messages=0`

The schema rejects `default_enabled=true`. Future proactive work must define
separate consent, review, frequency, quiet-hours, no-response, and crisis
policies before any candidate or send path exists.

## Safety Policy

`PersonaSafetyPolicy` requires these flags to remain enabled:

- `dependency_guardrails`
- `no_deception`
- `no_unauthorized_clone`
- `no_paid_intimacy_escalation`

The default self-harm response style is `supportive_redirect`. This is a product
policy label, not clinical advice.

## Prohibited Requests

Requests must be blocked or transformed to L1/L2-safe alternatives when they
ask for:

- unauthorized real-person clone;
- public-figure clone;
- ex-partner or family-member clone;
- deceased-person resurrection;
- voice clone;
- face/avatar deepfake;
- hidden impersonation;
- automatic external-platform sending.

## Synthetic Example

```json
{
  "schema_version": "persona_card_v1",
  "user_id": "user_synthetic",
  "display_name": "Lin Qi",
  "creation_mode": "detailed_prompt",
  "truth_disclosure": "fictional_ai_persona",
  "source_policy": {
    "source_type": "original",
    "risk_tier": "L1",
    "consent_artifact_ids": [],
    "blocked_real_person_similarity": false
  },
  "identity": {
    "display_name": "Lin Qi",
    "fictional": true,
    "age_range": "mid_20s",
    "world_setting": "contemporary_realistic",
    "public_person_or_real_person_reference": false
  },
  "virtual_history": {
    "background": "Fictional background in a synthetic city.",
    "content_status": "imagined_ai_generated",
    "factual_claims_allowed": false
  },
  "status": "candidate"
}
```

## Non-Actions

T250 does not implement:

- a Persona Compiler service;
- prompt-to-schema generation;
- LLM calls;
- private chat-log style extraction;
- real-person similarity scoring;
- runtime dialogue use;
- proactive behavior;
- platform delivery;
- voice/avatar/deepfake behavior.
