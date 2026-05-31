# Persona Growth Candidate Implementation Contract

Task: T372 Persona Growth Candidate Models
Status: worker draft for review

## Scope

This contract describes the implemented local persona-growth candidate records
in `src/practical_chat_agent/services/persona_growth.py`.

The records are review-first, patch-based, and non-mutating. They do not
modify `PersonaCard`, write `PersonaVersionStore`, call providers, read private
chat logs, generate dialogue, create proactive candidates, send messages,
connect to platform delivery, enable voice/avatar runtime, generate media, or
recreate real people.

## Implemented Records

### PersonaGrowthFieldChange

Implementation:

- `practical_chat_agent.services.persona_growth.PersonaGrowthFieldChange`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_growth_field_change_v1`. |
| `field_path` | Mutable PersonaCard field path. |
| `old_value_summary` | Human-readable current value summary. |
| `proposed_value_summary` | Human-readable proposed value summary. |
| `numeric_delta` | Optional numeric movement. |
| `change_reason` | Safe reason for the change. |
| `source_memory_ids` | Supporting memory ids. |
| `source_review_refs` | Supporting review refs. |
| `risk_labels` | Risk labels. |
| `requires_user_review` | Always true. |
| `blocks_approval` | True when blocking labels are present. |

Required invariants:

- frozen identity, source-policy, safety-policy, disclosure, persona id, user
  id, and default proactive fields cannot be changed;
- unknown field paths are rejected;
- single numeric trait movement cannot exceed `0.2`;
- `core_traits.jealousy` cannot increase by default;
- blocking risk labels set `blocks_approval=true`;
- all field changes require user review.

### PersonaGrowthPatchCandidate

Implementation:

- `practical_chat_agent.services.persona_growth.PersonaGrowthPatchCandidate`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_growth_patch_candidate_v1`. |
| `patch_id` | Generated `pgpatch_` id. |
| `user_id` | Owner user id. |
| `persona_id` | Source persona id. |
| `source_persona_version` | Source PersonaCard version. |
| `trigger_type` | `user_preference`, `user_correction`, `memory_pattern`, `relationship_signal`, `reviewer_note`, or `manual_edit`. |
| `trigger_summary` | Safe trigger summary. |
| `changes` | Field changes. |
| `evidence_memory_ids` | Supporting memory ids. |
| `relationship_context_refs` | Optional relationship refs. |
| `consent_scope_refs` | Consent refs. |
| `user_facing_explanation` | Plain-language explanation. |
| `safety_warnings` | Warning labels. |
| `clone_similarity_warnings` | Real-person likeness warnings. |
| `patch_status` | Candidate lifecycle state. |
| `review_required` | Always true. |
| `auto_apply_allowed` | Always false. |
| `writes_persona_version` | Always false. |
| `blocking_risk_labels` | Blocking labels collected from changes and similarity warnings. |
| `weekly_trait_delta_by_field` | Existing weekly movement by field. |
| `max_weekly_trait_delta` | Persona policy cap. |
| `created_at` | Creation timestamp. |

Helper:

- `from_persona_card(...)`

Required invariants:

- patch candidates cannot auto-apply;
- patch candidates cannot write persona versions;
- weekly movement by field cannot exceed the source PersonaCard growth policy;
- risk labels are deduplicated and blocking labels block approval in review;
- evidence from `PersonaGrowthEvidenceBundle` is referenced by id and warning
  labels only.

### PersonaGrowthPatchReview

Implementation:

- `practical_chat_agent.services.persona_growth.PersonaGrowthPatchReview`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_growth_patch_review_v1`. |
| `review_id` | Generated `pgreview_` id. |
| `patch_id` | Reviewed patch id. |
| `reviewer_id` | Reviewer id. |
| `decision` | `approve_for_manual_apply`, `reject`, `freeze`, or `request_changes`. |
| `decision_notes` | Safe notes. |
| `blocking_risk_labels` | Blocking labels inherited from the patch. |
| `approved_field_paths` | Field paths approved for later manual apply. |
| `rejected_field_paths` | Field paths rejected. |
| `auto_apply_allowed` | Always false. |
| `writes_persona_version` | Always false. |
| `reviewed_at` | Review timestamp. |

Helper:

- `from_patch(...)`

Required invariants:

- reviews cannot auto-apply;
- reviews cannot write persona versions;
- patches with blocking labels cannot be approved for manual apply.

### PersonaGrowthJournalEntry

Implementation:

- `practical_chat_agent.services.persona_growth.PersonaGrowthJournalEntry`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_growth_journal_entry_v1`. |
| `journal_id` | Generated `pgjournal_` id. |
| `persona_id` | Persona id. |
| `source_patch_id` | Approved patch id. |
| `source_version_id` | Persona version created by a later manual apply path. |
| `summary` | User-facing growth summary. |
| `changed_field_paths` | Changed fields. |
| `safety_warnings` | Warnings considered during review. |
| `writes_persona_version` | Always false. |
| `created_at` | Creation timestamp. |

Required invariant:

- journal entries describe growth history but do not write persona versions.

## Mutable Field Set

The implementation permits growth candidates only for:

- `core_traits.warmth`
- `core_traits.directness`
- `core_traits.humor`
- `core_traits.independence`
- `core_traits.emotional_stability`
- `core_traits.jealousy` only when decreasing or stable
- `speech_style.sentence_length`
- `speech_style.emoji_frequency`
- `speech_style.punctuation_style`
- `speech_style.humor_type`
- `speech_style.pet_names`
- `speech_style.taboo_phrases`
- `emotion_model.baseline_mood`
- `emotion_model.stress_response`
- `emotion_model.comforting_style`
- `emotion_model.conflict_style`
- `relationship_model.trust_growth_rate`
- `relationship_model.intimacy_growth_rate`
- `relationship_model.boundary_sensitivity`
- `virtual_history.daily_routine`
- `virtual_history.current_goals`
- `virtual_history.virtual_social_circle`

## Blocking Labels

The implementation blocks approval for:

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

## Shared Invariants

All implemented records:

- use `extra="forbid"`;
- preserve ids, safe summaries, and review refs only;
- are review-first;
- do not auto-apply;
- do not write persona versions;
- do not mutate `PersonaCard`;
- do not call providers;
- do not contain outbound delivery state;
- do not contain voice/avatar/media payloads.

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

- `tests/test_persona_growth_candidates.py`

Covered behavior:

- mutable field changes are reviewable;
- frozen fields are rejected;
- unknown field paths are rejected;
- single numeric deltas cannot exceed the global cap;
- `core_traits.jealousy` cannot increase by default;
- patch candidates preserve persona id/version and never auto-apply;
- weekly movement cannot exceed the source PersonaCard policy cap;
- blocking safety labels block approval;
- rejected, frozen, needs-changes, and archived patches do not write versions;
- imagined memory cannot justify factual identity changes;
- review records do not write PersonaCard versions;
- journal entries record manual-apply refs without writing versions;
- models reject extra private/provider/outbound/media fields;
- candidates do not expose runtime or delivery methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_growth.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_growth_candidates.py tests\test_memory_governance_candidates.py tests\test_persona_card_schema.py tests\test_persona_review.py tests\test_persona_version_store.py -q -o cache_dir=artifacts\t372_pytest_cache --basetemp=artifacts\t372_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T372 does not implement:

- private data ingestion;
- source readers;
- extraction;
- embeddings;
- vector search;
- similarity scoring;
- model-provider calls;
- PersonaCard mutation;
- PersonaVersionStore writes;
- final companion reply generation;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Growth patches are candidate records only; no user-facing approval UI exists.
- Manual apply and version creation remain future work.
- The mutable-field allowlist is intentionally conservative and may need
  product tuning.
- Synthetic tests do not validate real user trust, live dialogue quality, or
  de-identification quality.
