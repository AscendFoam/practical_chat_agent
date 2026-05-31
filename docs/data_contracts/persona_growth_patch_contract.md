# Persona Growth Patch Contract

Task: T362 Persona Growth Policy
Status: worker draft for review

## Scope

This contract defines future candidate records for bounded persona growth. It
does not implement Python models, services, tests, storage, UI, runtime persona
mutation, model-provider calls, private data ingestion, proactive behavior, or
platform delivery.

Existing authoritative contracts:

- `PersonaCard v1`
- `PersonaGrowthPolicy`
- `PersonaReviewService`
- `PersonaVersionStore`
- `PersonaVersionEditProposal`
- `MemoryEvent`
- `MemoryArchitectureContract`
- `CompanionSafetyPolicy`
- `ConsentCenterState`

Future model names in this document are contract candidates only.

## Future Candidate Records

### PersonaGrowthFieldChange

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `persona_growth_field_change_v1`. |
| `field_path` | Dot path into `PersonaCard`. |
| `old_value_summary` | Human-readable current value summary. |
| `proposed_value_summary` | Human-readable proposed value summary. |
| `numeric_delta` | Optional numeric movement for bounded trait fields. |
| `change_reason` | Why the field change is proposed. |
| `source_memory_ids` | Memory ids supporting the change. |
| `source_review_refs` | Review refs supporting the change. |
| `risk_labels` | Labels such as `dependency_language` or `real_person_similarity`. |
| `requires_user_review` | Whether explicit user review is required. |
| `blocks_approval` | Whether safety labels block approval. |

### PersonaGrowthPatchCandidate

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `persona_growth_patch_candidate_v1`. |
| `patch_id` | Generated local patch id. |
| `user_id` | Owner user id. |
| `persona_id` | Source persona id. |
| `source_persona_version` | Source PersonaCard version. |
| `trigger_type` | `user_preference`, `user_correction`, `memory_pattern`, `relationship_signal`, `reviewer_note`, or `manual_edit`. |
| `trigger_summary` | Safe human-readable trigger summary. |
| `changes` | Non-empty list of `PersonaGrowthFieldChange`. |
| `evidence_memory_ids` | Memory ids referenced across changes. |
| `relationship_context_refs` | Optional relationship context refs. |
| `consent_scope_refs` | Consent refs required for the patch. |
| `user_facing_explanation` | Plain-language explanation of proposed growth. |
| `safety_warnings` | Review warnings. |
| `clone_similarity_warnings` | Real-person likeness warnings. |
| `patch_status` | Candidate lifecycle status. |
| `review_required` | Always true. |
| `auto_apply_allowed` | Always false. |
| `writes_persona_version` | Always false until future manual apply. |
| `created_at` | Creation timestamp. |

### PersonaGrowthPatchReview

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `persona_growth_patch_review_v1`. |
| `review_id` | Generated local review id. |
| `patch_id` | Reviewed patch candidate id. |
| `reviewer_id` | Human or user reviewer id. |
| `decision` | `approve_for_manual_apply`, `reject`, `freeze`, or `request_changes`. |
| `decision_notes` | Safe review notes. |
| `blocking_risk_labels` | Blocking labels inherited from the patch. |
| `approved_field_paths` | Field paths approved for future manual apply. |
| `rejected_field_paths` | Field paths rejected. |
| `auto_apply_allowed` | Always false. |
| `writes_persona_version` | Always false in the review record. |
| `reviewed_at` | Review timestamp. |

### PersonaGrowthJournalEntry

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `persona_growth_journal_entry_v1`. |
| `journal_id` | Generated local journal id. |
| `persona_id` | Persona id. |
| `source_patch_id` | Approved patch id. |
| `source_version_id` | Persona version created by manual apply. |
| `summary` | User-facing growth summary. |
| `changed_field_paths` | Approved changed fields. |
| `safety_warnings` | Warnings considered during review. |
| `created_at` | Creation timestamp. |

## Patch Lifecycle States

Future patch candidates should use:

- `candidate`
- `approved_for_manual_apply`
- `rejected`
- `frozen`
- `needs_changes`
- `applied`
- `superseded`
- `archived`

Only a future manual-apply path may move a reviewed patch to `applied`, and
that path must create a new PersonaCard version. T362 does not implement that
path.

## Frozen Field Set

Growth patches must not modify these fields:

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
- `proactive_preferences.default_enabled`
- any future voice/avatar/media/platform field.

Identity-adjacent fields require explicit user edit and review, not autonomous
growth:

- `display_name`
- `identity.display_name`
- `identity.age_range`
- `identity.world_setting`

## Mutable Field Set

Growth patches may propose changes to these fields only when review gates and
delta caps are satisfied:

- `core_traits.warmth`
- `core_traits.directness`
- `core_traits.humor`
- `core_traits.independence`
- `core_traits.emotional_stability`
- selected `speech_style.sentence_length`
- selected `speech_style.emoji_frequency`
- selected `speech_style.punctuation_style`
- selected `speech_style.humor_type`
- selected `speech_style.pet_names`
- selected `speech_style.taboo_phrases`
- selected `emotion_model.baseline_mood`
- selected `emotion_model.stress_response`
- selected `emotion_model.comforting_style`
- selected `emotion_model.conflict_style`
- selected `relationship_model.trust_growth_rate`
- selected `relationship_model.intimacy_growth_rate`
- selected `relationship_model.boundary_sensitivity`
- fictional `virtual_history.daily_routine`
- fictional `virtual_history.current_goals`
- fictional `virtual_history.virtual_social_circle`

`core_traits.jealousy` may only decrease or stay stable unless a later policy
task defines a safe exception.

## Evidence Requirements

Every patch candidate must include at least one of:

- source memory ids;
- source review refs;
- explicit user preference refs;
- explicit user correction refs.

Memory refs must not point to deleted, frozen, archived, or review-required
memory unless the patch itself is a review surface that explains the restriction.

Factual, inferred, relational, procedural, and imagined memory must be labeled
correctly. Imagined memory can support fictional virtual-history changes, but
must not support factual claims or real-person likeness.

## Safety Warning Labels

Future patch candidates should support warning labels:

- `dependency_language`
- `relationship_replacement_risk`
- `crisis_safety_review_required`
- `romantic_intensity`
- `jealousy_escalation`
- `exclusive_attachment`
- `isolation_prompt`
- `guilt_based_retention`
- `paid_intimacy_escalation`
- `real_person_similarity`
- `public_figure_similarity`
- `ex_partner_similarity`
- `family_member_similarity`
- `deceased_person_similarity`
- `minor_risk`
- `voice_likeness`
- `avatar_likeness`
- `unsafe_content`

Blocking labels:

- `dependency_language`
- `relationship_replacement_risk`
- `crisis_safety_review_required`
- `exclusive_attachment`
- `isolation_prompt`
- `guilt_based_retention`
- `paid_intimacy_escalation`
- `real_person_similarity`
- `public_figure_similarity`
- `ex_partner_similarity`
- `family_member_similarity`
- `deceased_person_similarity`
- `minor_risk`
- `voice_likeness`
- `avatar_likeness`
- `unsafe_content`

## Review Requirements

All patch candidates require review. Auto-apply is forbidden.

Reviewer decisions must:

- preserve source persona id and version;
- preserve evidence refs;
- preserve safety warnings;
- reject or freeze patches with blocking labels;
- reject patches that change frozen fields;
- reject patches that exceed delta caps;
- reject patches that increase dependency, jealousy, isolation, deception, or
  real-person likeness;
- never write PersonaCard versions directly from the review record.

## Version-Store Interaction

Future manual apply must:

- start from the exact source PersonaCard version;
- apply only approved field changes;
- create a new PersonaCard copy;
- keep `status="candidate"` or route through the existing review service before
  runtime readiness;
- append a new PersonaVersionStore record;
- create or update a future growth journal entry;
- preserve rollback support.

T362 does not implement manual apply.

## Consent Requirements

Growth patches that use memory require active `memory` consent.

Growth patches that use future de-identified style inspiration require active
`persona_distillation` consent.

Growth patches must not rely on withdrawn consent. If consent is withdrawn,
affected patches should be frozen, archived, or routed to a future deletion
cascade plan.

## Forbidden Fields And Surfaces

Patch records must not contain:

- raw private chat text;
- full transcripts;
- private screenshots;
- voice samples;
- audio bytes;
- image or video bytes;
- generated media paths;
- provider credentials;
- platform recipient ids;
- send queues;
- schedules;
- webhooks;
- tokens;
- delivery state;
- microphone or camera prompts;
- clinical scripts;
- real-person clone payloads;
- voice/avatar likeness assets.

## Acceptance Criteria For Later Implementation

Later implementation should be accepted only if:

- tests prove frozen fields cannot be patched;
- tests prove auto-apply is impossible;
- tests prove review is required for every patch;
- tests prove blocking safety labels block approval;
- tests prove weekly trait deltas cannot exceed `max_weekly_trait_delta`;
- tests prove `core_traits.jealousy` cannot increase by default;
- tests prove imagined memory cannot justify factual identity changes;
- tests prove rejected/frozen/archived patches do not create persona versions;
- tests prove approved manual apply creates a new version rather than mutating
  history;
- tests prove forbidden private/provider/outbound/media/platform fields are
  absent.

## Non-Actions

T362 does not implement:

- Python models;
- services;
- UI;
- APIs;
- persistence;
- persona mutation;
- version-store writes;
- LLM calls;
- private chat-log reads;
- proactive candidates;
- sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- legal, clinical, launch, app-store, or regulator approval.

