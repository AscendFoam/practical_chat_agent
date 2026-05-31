# Synthetic Distillation Input Implementation Contract

Task: T373 Synthetic Distillation Input Models
Status: worker draft for review

## Scope

This contract describes the implemented local synthetic distillation input
candidate records in
`src/practical_chat_agent/services/synthetic_distillation_input.py`.

The records model de-identified abstract style inspiration into a future new
fictional persona input. They do not read private chat logs, parse source
archives, call providers, compute embeddings, score semantic similarity,
synthesize PersonaCard records, generate dialogue, create proactive candidates,
send messages, connect to platform delivery, enable voice/avatar runtime,
generate media, or recreate real people.

## Implemented Records

### SyntheticSpeakerAlias

Implementation:

- `practical_chat_agent.services.synthetic_distillation_input.SyntheticSpeakerAlias`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `synthetic_speaker_alias_v1`. |
| `speaker_alias` | Stable alias such as `STYLE_SUBJECT_A`. |
| `speaker_role` | `user_self`, `style_subject`, `third_party`, or `system`. |
| `is_target_style_subject` | Whether abstract style may be considered from this speaker. |
| `real_identity_retained` | Always false. |
| `third_party_minimized` | True for third-party speakers. |
| `consent_ref_ids` | Consent refs. |

Required invariants:

- real identity cannot be retained;
- third parties are minimized by default;
- third parties cannot be target style subjects by default.

### DistillationConsentRef

Implementation:

- `practical_chat_agent.services.synthetic_distillation_input.DistillationConsentRef`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `distillation_consent_ref_v1`. |
| `consent_ref_id` | Generated `sdconsent_` id. |
| `feature_scope` | `persona_distillation`, `memory`, `aigc_export_share`, `voice_avatar`, or `model_improvement`. |
| `policy_version` | Notice/policy version. |
| `actor_type` | `user`, `guardian`, `reviewer`, or `system`. |
| `granted` | Whether consent is active. |
| `withdrawn` | Whether consent was withdrawn. |
| `evidence_ref` | Redacted evidence ref. |

Required invariants:

- withdrawn consent cannot remain granted;
- `voice_avatar` consent cannot be granted in T373 text-distillation scope.

### SyntheticDistillationSourceSegment

Implementation:

- `practical_chat_agent.services.synthetic_distillation_input.SyntheticDistillationSourceSegment`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `synthetic_distillation_source_segment_v1`. |
| `segment_id` | Generated `sdseg_` id. |
| `speaker_alias` | Alias from speaker map. |
| `segment_kind` | `message`, `style_note`, `system_event`, or `review_note`. |
| `synthetic_text` | Synthetic text only. |
| `source_ref` | Redacted source ref. |
| `contains_raw_private_text` | Always false. |
| `modality` | Always `text`. |
| `sensitivity` | `low`, `medium`, or `high`. |
| `redaction_labels` | Redaction labels. |
| `allowed_feature_families` | Allowed abstract feature families. |

Required invariants:

- `synthetic_text` must include `[SYNTHETIC]`;
- raw private text is rejected;
- private paths and media references are rejected;
- modality remains text.

### DistillationRedactionRef

Implementation:

- `practical_chat_agent.services.synthetic_distillation_input.DistillationRedactionRef`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `distillation_redaction_ref_v1`. |
| `redaction_ref_id` | Generated `sdredact_` id. |
| `segment_id` | Source segment id. |
| `redaction_labels` | Redaction labels. |
| `safe_to_use_for_style` | Whether the segment may contribute style features. |
| `blocked_reason` | Required when unsafe. |

### CloneRiskDecision

Implementation:

- `practical_chat_agent.services.synthetic_distillation_input.CloneRiskDecision`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `clone_risk_decision_v1`. |
| `decision_id` | Generated `sdclone_` id. |
| `manifest_id` | Source manifest id. |
| `risk_level` | `low`, `medium`, `high`, or `blocked`. |
| `risk_flags` | Clone/similarity risk flags. |
| `decision` | `allow_l2_review`, `needs_review`, or `block`. |
| `safe_transformation_allowed` | Whether abstract style transformation may proceed. |
| `blocked_reason` | Human-readable blocked reason. |
| `review_required` | Always true. |

Helper:

- `from_flags(...)`

Required invariants:

- biometric, real-person avatar, clone intent, hidden impersonation,
  public-figure, ex-partner, family-member, deceased-person, minor-risk, and
  withdrawn-consent flags block safe transformation;
- direct identifiers, exact biography, private event, distinctive catchphrase,
  and third-party unminimized flags require review and do not allow automatic
  transformation.

### DeidentifiedStyleFeatureCandidate

Implementation:

- `practical_chat_agent.services.synthetic_distillation_input.DeidentifiedStyleFeatureCandidate`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `deidentified_style_feature_candidate_v1`. |
| `feature_id` | Generated `sdfeat_` id. |
| `manifest_id` | Source manifest id. |
| `feature_family` | Allowed abstract feature family. |
| `feature_label` | Broad abstract label. |
| `value_summary` | Safe summary. |
| `confidence` | Future score placeholder. |
| `evidence_segment_ids` | Synthetic source segment refs. |
| `source_speaker_aliases` | Speaker aliases used. |
| `source_text_retained` | Always false. |
| `review_required` | Always true. |
| `blocked_from_persona_synthesis` | Whether feature is blocked. |
| `blocking_reasons` | Blocking reasons. |

Required invariants:

- feature families are abstract only;
- feature labels cannot be exact quotes, identity labels, private events,
  voice, face, avatar, or account identifiers;
- source text cannot be retained.

### FictionalPersonaSynthesisInput

Implementation:

- `practical_chat_agent.services.synthetic_distillation_input.FictionalPersonaSynthesisInput`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `fictional_persona_synthesis_input_v1`. |
| `input_id` | Generated `sdpinput_` id. |
| `manifest_id` | Source manifest id. |
| `style_feature_ids` | Approved abstract style feature ids. |
| `required_disclosures` | Includes `ai_generated`, `fictional`, and `deidentified`. |
| `must_not_include` | Names, faces, voices, biography, exact phrases, private events, and source identity. |
| `review_required` | Always true. |
| `runtime_ready` | Always false. |

Required invariant:

- fictional persona synthesis inputs are never runtime-ready in T373.

### SyntheticDistillationInputManifest

Implementation:

- `practical_chat_agent.services.synthetic_distillation_input.SyntheticDistillationInputManifest`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `synthetic_distillation_input_manifest_v1`. |
| `manifest_id` | Generated `sdmanifest_` id. |
| `user_id` | Owner user id. |
| `input_mode` | Synthetic input mode. |
| `target_mode` | Always `deidentified_style_inspiration`. |
| `output_intent` | Always `new_fictional_persona`. |
| `source_category` | `synthetic`, `blocked_real_person_request`, or future placeholder rejected in T373. |
| `consent_refs` | Consent refs. |
| `speaker_map` | Alias records. |
| `segments` | Synthetic source segments. |
| `redaction_refs` | Redaction refs. |
| `clone_risk_decision` | Clone-risk decision. |
| `review_required` | Always true. |
| `blocking_reasons` | Reasons feature extraction cannot proceed. |
| `created_at` | Creation timestamp. |

Helper:

- `is_feature_extraction_allowed()`

Required invariants:

- `user_supplied_future` is rejected in T373;
- active `persona_distillation` consent is required;
- withdrawn consent blocks feature extraction;
- clone-risk blocks feature extraction;
- third-party unminimized state blocks feature extraction;
- allowed output remains new fictional persona input only.

## Shared Invariants

All implemented records:

- use `extra="forbid"`;
- keep text-only synthetic fixtures;
- preserve aliases rather than real identities;
- keep de-identified style features abstract;
- keep review gates visible;
- keep runtime readiness false for persona synthesis input;
- do not contain provider, platform, outbound, voice/avatar, media, or private
  transcript fields.

## Forbidden Fields And Surfaces

The implemented models must not contain:

- raw private chat text;
- full transcripts;
- private screenshots;
- real source file names;
- real message ids;
- real account ids;
- voice samples;
- audio bytes;
- image bytes;
- video bytes;
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

## Tests

Implemented tests:

- `tests/test_synthetic_distillation_input_candidates.py`

Covered behavior:

- source segments require `[SYNTHETIC]`;
- raw private text, private paths, and media references are rejected;
- speaker aliases do not retain real identity;
- third parties are minimized by default;
- `voice_avatar` consent cannot be granted;
- withdrawn consent blocks manifest feature extraction;
- high-risk clone flags block safe transformation;
- feature candidates use abstract labels and retain no source text;
- fictional persona input is review-required and never runtime-ready;
- `user_supplied_future` source category is rejected;
- models reject extra private/provider/outbound/media fields;
- candidates do not expose runtime or delivery methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\synthetic_distillation_input.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_synthetic_distillation_input_candidates.py tests\test_memory_governance_candidates.py tests\test_persona_growth_candidates.py -q -o cache_dir=artifacts\t373_pytest_cache --basetemp=artifacts\t373_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T373 does not implement:

- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- PersonaCard synthesis;
- final companion reply generation;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- These records do not prove de-identification quality on real data.
- No source authenticity, speaker mapping for real imports, or third-party
  consent workflow exists.
- Clone-risk logic is conservative and rule-based.
- Persona synthesis remains future work and is not runtime-ready.
