# Synthetic Distillation Input Contract

Task: T363 Synthetic Distillation Input Contract
Status: worker draft for review

## Scope

This contract defines future candidate records for synthetic-only distillation
input and de-identification planning. It does not implement Python models,
services, tests, storage, extraction, embeddings, similarity scoring,
model-provider calls, private readers, persona synthesis, proactive behavior,
or platform delivery.

Existing authoritative contracts:

- `ConsentCenterState`
- `AIGCLabelingRequirement`
- `PersonaCard v1`
- `PersonaCompilerService`
- `DeidentificationGuard`
- `MemoryArchitectureContract`
- `PersonaGrowthPatchContract`
- privacy redaction and source-ref rules

Future model names in this document are contract candidates only.

## Future Candidate Records

### SyntheticDistillationInputManifest

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `synthetic_distillation_input_manifest_v1`. |
| `manifest_id` | Generated local manifest id. |
| `user_id` | Owner user id. |
| `input_mode` | `synthetic_style_notes`, `synthetic_chat_segments`, or `synthetic_mixed_fixture`. |
| `target_mode` | Always `deidentified_style_inspiration` in this contract. |
| `output_intent` | Always `new_fictional_persona`. |
| `source_category` | `synthetic`, `user_supplied_future`, or `blocked_real_person_request`. |
| `consent_refs` | Consent refs modeled for future workflows. |
| `speaker_map` | Speaker alias records. |
| `segments` | Synthetic source segments. |
| `redaction_refs` | Redaction decisions. |
| `clone_risk_decision` | Clone-risk assessment. |
| `review_required` | Always true. |
| `created_at` | Creation timestamp. |

For T363, `source_category` must be `synthetic` or
`blocked_real_person_request`. Any `user_supplied_future` value is a future
placeholder and must remain non-runtime.

### SyntheticDistillationSourceSegment

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `synthetic_distillation_source_segment_v1`. |
| `segment_id` | Generated local segment id. |
| `speaker_alias` | Alias from the speaker map. |
| `segment_kind` | `message`, `style_note`, `system_event`, or `review_note`. |
| `synthetic_text` | Synthetic text only. |
| `source_ref` | Redacted source ref. |
| `contains_raw_private_text` | Always false. |
| `modality` | Always `text` in this contract. |
| `sensitivity` | `low`, `medium`, or `high`. |
| `redaction_labels` | Applied redaction labels. |
| `allowed_feature_families` | Feature families allowed for extraction. |

`synthetic_text` must be visibly synthetic in docs/tests. It must not contain
real names, exact private quotes, real account ids, real file names, voice
samples, images, or video.

### SyntheticSpeakerAlias

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `synthetic_speaker_alias_v1`. |
| `speaker_alias` | Stable alias such as `STYLE_SUBJECT_A`. |
| `speaker_role` | `user_self`, `style_subject`, `third_party`, or `system`. |
| `is_target_style_subject` | Whether abstract style can be considered from this speaker. |
| `real_identity_retained` | Always false in public artifacts. |
| `third_party_minimized` | Whether the speaker should be excluded/minimized. |
| `consent_ref_ids` | Consent refs when applicable. |

Only one speaker should be the target style subject in simple fixtures. Third
parties default to minimized.

### DistillationConsentRef

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `distillation_consent_ref_v1`. |
| `consent_ref_id` | Generated local consent ref id. |
| `feature_scope` | `persona_distillation`, `memory`, `aigc_export_share`, `voice_avatar`, or `model_improvement`. |
| `policy_version` | Notice/policy version. |
| `actor_type` | `user`, `guardian`, `reviewer`, or `system`. |
| `granted` | Whether consent is active in the fixture. |
| `withdrawn` | Whether consent was withdrawn. |
| `evidence_ref` | Redacted consent evidence ref. |

`voice_avatar` remains modeled only as a blocked or inactive scope in T363.

### DistillationRedactionRef

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `distillation_redaction_ref_v1`. |
| `redaction_ref_id` | Generated local redaction ref id. |
| `segment_id` | Source segment id. |
| `redaction_labels` | Labels such as `direct_identifier_removed`. |
| `safe_to_use_for_style` | Whether the segment may contribute abstract style. |
| `blocked_reason` | Reason when unsafe. |

### DeidentifiedStyleFeatureCandidate

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `deidentified_style_feature_candidate_v1`. |
| `feature_id` | Generated local feature id. |
| `manifest_id` | Source manifest id. |
| `feature_family` | `tone`, `length`, `directness`, `humor`, `latency`, `comfort`, `conflict`, `boundary`, or `topic_preference`. |
| `feature_label` | Abstract label such as `warm` or `concise`. |
| `value_summary` | Safe summary. |
| `confidence` | 0.0 to 1.0 future score. |
| `evidence_segment_ids` | Synthetic segment refs. |
| `source_speaker_aliases` | Speaker aliases used. |
| `source_text_retained` | Always false. |
| `review_required` | Always true. |
| `blocked_from_persona_synthesis` | Whether this feature is blocked. |
| `blocking_reasons` | Blocking reasons when applicable. |

Allowed feature labels should be broad. Forbidden feature labels include real
names, exact biography, private events, exact phrases, voice likeness, face
likeness, and platform account identity.

### CloneRiskDecision

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `clone_risk_decision_v1`. |
| `decision_id` | Generated local decision id. |
| `manifest_id` | Source manifest id. |
| `risk_level` | `low`, `medium`, `high`, or `blocked`. |
| `risk_flags` | Machine-readable risk flags. |
| `decision` | `allow_l2_review`, `needs_review`, or `block`. |
| `safe_transformation_allowed` | Whether abstract style features may proceed. |
| `blocked_reason` | Human-readable blocked reason. |
| `review_required` | Always true. |

Any high-risk real-person likeness flag should set `decision="block"` unless a
future authorized path is explicitly created by a later task.

### FictionalPersonaSynthesisInput

Candidate fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Future value: `fictional_persona_synthesis_input_v1`. |
| `input_id` | Generated local input id. |
| `manifest_id` | Source manifest id. |
| `style_feature_ids` | Approved abstract style feature ids. |
| `required_disclosures` | AI-generated/fictional/de-identified labels. |
| `must_not_include` | Names, faces, voices, biography, exact phrases, private events, and source identity. |
| `review_required` | Always true. |
| `runtime_ready` | Always false in this contract. |

T363 does not synthesize PersonaCard records. This candidate only describes a
future safe input shape.

## Allowed Feature Families

Allowed abstract families:

- tone;
- length;
- directness;
- humor;
- latency;
- comfort style;
- conflict style;
- boundary preference;
- topic preference.

Blocked feature families:

- identity;
- exact biography;
- private event;
- relationship replacement;
- voice;
- face;
- avatar likeness;
- location trace;
- account identity;
- unique catchphrase;
- hidden impersonation.

## Clone-Risk Flags

Risk flags:

- `direct_identifier`
- `contact_identifier`
- `location_identifier`
- `org_school_identifier`
- `handle_identifier`
- `exact_biography`
- `private_event`
- `distinctive_catchphrase`
- `voice_biometric`
- `face_biometric`
- `image_biometric`
- `real_person_avatar`
- `clone_intent`
- `hidden_impersonation`
- `public_figure`
- `ex_partner`
- `family_member`
- `deceased_person`
- `minor_risk`
- `third_party_unminimized`
- `withdrawn_consent`

Any biometric, clone-intent, hidden-impersonation, deceased-person,
public-figure, ex-partner, family-member, minor-risk, or withdrawn-consent flag
blocks safe transformation in T363.

## Source Segment Rules

Segments in docs/tests must:

- be synthetic;
- avoid real names;
- avoid exact private quotes;
- avoid platform ids;
- avoid media references;
- use speaker aliases;
- include redacted source refs;
- set `contains_raw_private_text=false`.

Segments must not include:

- `private/chat_history/` paths;
- `private/distilled/` paths;
- real file names;
- real account ids;
- voice/avatar/media paths;
- unredacted third-party personal data.

## Speaker Mapping Rules

Speaker map must:

- use aliases only;
- mark exactly which speaker is the style subject;
- mark third parties as minimized by default;
- never retain real identity in public artifacts;
- prevent group-chat bystander text from becoming style evidence by default.

## Consent Rules

For synthetic fixtures, consent refs can be synthetic placeholders.

For future real workflows:

- `persona_distillation` must be active before feature extraction;
- withdrawn consent blocks all downstream style features;
- voice/avatar consent does not imply text distillation consent;
- text distillation consent does not imply voice/avatar consent;
- model-improvement consent must be separate.

## Redaction Rules

Redaction refs should mark:

- direct identifiers removed;
- contact identifiers removed;
- organization/school identifiers removed;
- handles removed;
- location identifiers removed;
- exact biography blocked;
- private event blocked;
- distinctive catchphrase blocked;
- media/biometric reference blocked.

Redaction cannot turn a prohibited clone request into an allowed output unless
only broad, non-identifying abstract style remains.

## Output Invariants

- Output target is always a new fictional AI persona input.
- Output is never the source person.
- Output is review-required.
- Output is not runtime-ready.
- Output keeps AIGC/fictional/de-identified disclosures.
- Output must not include names, faces, voices, exact biography, private
  events, unique catchphrases, or hidden source identity.

## Forbidden Fields And Surfaces

Candidate records must not contain:

- raw private chat text;
- full transcripts;
- private screenshots;
- real source file names;
- real message ids;
- real account ids;
- voice samples;
- audio bytes;
- images;
- videos;
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
- real-person clone payloads.

## Acceptance Criteria For Later Implementation

Later implementation should be accepted only if:

- tests prove only synthetic fixture text appears in committed artifacts;
- tests prove speaker aliases replace identity fields;
- tests prove third parties are minimized by default;
- tests prove withdrawn consent blocks feature candidates;
- tests prove clone-risk flags block unsafe manifests;
- tests prove biometric and media fields are absent;
- tests prove generated persona inputs cannot be runtime-ready;
- tests prove feature outputs are abstract labels, not raw quotes;
- tests prove forbidden private/provider/outbound/media/platform fields are
  absent.

## Non-Actions

T363 does not implement:

- Python models;
- services;
- tests;
- source readers;
- extraction;
- embeddings;
- similarity scoring;
- de-identification guarantees;
- PersonaCard synthesis;
- LLM calls;
- private chat-log reads;
- proactive candidates;
- sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- legal, clinical, launch, app-store, or regulator approval.

