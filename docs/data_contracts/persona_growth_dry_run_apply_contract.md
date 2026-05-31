# Persona Growth Dry-Run Apply Contract

Task: T379 Persona Growth Dry-Run Apply Plans
Status: worker draft for review

## Scope

This contract describes the implemented preview-only persona growth dry-run
records in `src/practical_chat_agent/services/persona_growth_dry_run.py`.

The records preview `PersonaGrowthPatchCandidate` effects without applying
them. They do not mutate `PersonaCard`, write `PersonaVersionStore`, apply
review decisions, call providers, read private data, generate replies, send
messages, create UI, connect to platform delivery, enable voice/avatar runtime,
generate media, or recreate real people.

## Implemented Records

### PersonaGrowthDryRunFieldPreview

Implementation:

- `practical_chat_agent.services.persona_growth_dry_run.PersonaGrowthDryRunFieldPreview`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_growth_dry_run_field_preview_v1`. |
| `preview_id` | Generated `pgdfield_` id. |
| `field_path` | Previewed PersonaCard field path. |
| `old_value_summary` | Safe current value summary. |
| `proposed_value_summary` | Safe proposed value summary. |
| `numeric_delta` | Optional numeric movement. |
| `change_reason` | Safe reason summary. |
| `source_memory_ids` | Supporting memory ids. |
| `source_review_refs` | Supporting review refs. |
| `risk_labels` | Risk labels inherited from the change. |
| `blocks_apply` | True when the preview cannot be manually applied later. |
| `preview_only` | Always true. |
| `applies_changes` | Always false. |
| `writes_persona_version` | Always false. |
| `created_at` | Preview timestamp. |

Helper:

- `from_change(...)`

Required invariants:

- field previews are preview-only;
- field previews cannot apply changes;
- field previews cannot write persona versions;
- risk labels make the field block later manual apply readiness.

### PersonaGrowthDryRunPlan

Implementation:

- `practical_chat_agent.services.persona_growth_dry_run.PersonaGrowthDryRunPlan`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_growth_dry_run_plan_v1`. |
| `plan_id` | Generated `pgdplan_` id. |
| `patch_id` | Source growth patch id. |
| `user_id` | Owner user id. |
| `persona_id` | Source persona id. |
| `source_persona_version` | Source PersonaCard version. |
| `review_decision_id` | Optional review queue decision ref. |
| `review_decision` | Optional decision label. |
| `trigger_type` | Source patch trigger type. |
| `safe_summary` | User-facing explanation from the patch. |
| `field_previews` | Field preview records. |
| `blocked_field_paths` | Fields blocked from later manual apply. |
| `blocking_risk_labels` | Blocking labels from patch/fields. |
| `weekly_trait_delta_by_field` | Existing weekly movement. |
| `weekly_trait_delta_after` | Existing plus previewed movement. |
| `max_weekly_trait_delta` | Source patch policy cap. |
| `ready_for_later_manual_apply` | True only when no blocked fields and decision is absent or approve. |
| `blocked_reasons` | Reasons no real apply happens or readiness is blocked. |
| `preview_only` | Always true. |
| `review_required` | Always true. |
| `applies_changes` | Always false. |
| `writes_persona_version` | Always false. |
| `created_at` | Plan timestamp. |

Required invariants:

- plans are preview-only;
- plans require review;
- plans cannot apply changes;
- plans cannot write persona versions;
- non-approve decisions prevent later manual-apply readiness;
- blocking labels prevent later manual-apply readiness.

### PersonaGrowthDryRunService

Implementation:

- `practical_chat_agent.services.persona_growth_dry_run.PersonaGrowthDryRunService`

Method:

- `plan_from_patch(patch, source_persona=None, decision_record=None)`

Required behavior:

- preserves patch id, persona id, source version, field paths, safe summaries,
  numeric deltas, source refs, and risk labels;
- optionally references a review queue decision;
- validates optional `source_persona.persona_id` against the patch;
- never mutates the supplied PersonaCard.

## Forbidden Fields And Surfaces

The implemented records must not contain:

- raw private chat text;
- raw transcripts;
- private message bodies;
- provider credentials;
- platform recipient ids;
- send queues;
- schedules;
- webhooks;
- tokens;
- delivery state;
- microphone, camera, audio, image, or video payloads;
- runtime reply-generation methods;
- mutation/apply methods;
- voice/avatar/media generation methods.

## Tests

Implemented tests:

- `tests/test_persona_growth_dry_run_apply.py`

Covered behavior:

- dry-run plans preserve PersonaCard state;
- safe field previews are listed without writing versions;
- weekly delta after-preview is visible;
- blocking labels prevent apply readiness;
- review decisions are referenced but not applied;
- extra private/provider/outbound/media fields are rejected;
- service exposes no runtime, delivery, provider, mutation, voice/avatar, or
  media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_growth_dry_run.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_growth_dry_run_apply.py tests\test_persona_growth_candidates.py tests\test_review_queue_candidates.py -q -o cache_dir=artifacts\t379_pytest_cache --basetemp=artifacts\t379_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T379 does not implement:

- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- final companion reply generation;
- runtime memory or persona mutation;
- decision apply paths;
- persona version writes;
- review UI;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Dry-run plans do not execute approved changes.
- No user-facing review UI or approval workflow exists.
- No PersonaVersionStore apply path exists.
- T380 still needs synthetic distillation review readiness aggregation.
