# Review Decision Impact Preview Contract

Task: T385 Review Decision Impact Preview
Status: worker draft for review

## Scope

This contract describes the implemented deterministic impact preview records
in `src/practical_chat_agent/services/review_decision_impact_preview.py`.

The records combine a `ReviewQueueDecisionRecord` with a safe
`ReviewWorkspaceBundle` so local review surfaces can inspect what a decision
would mean. They do not apply decisions, mutate memory stores, write persona
versions, synthesize personas, call providers, generate replies, send
messages, create UI, connect to platform delivery, enable voice/avatar
runtime, generate media, or recreate real people.

## Implemented Records

### ReviewDecisionImpactIssue

Implementation:

- `practical_chat_agent.services.review_decision_impact_preview.ReviewDecisionImpactIssue`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_decision_impact_issue_v1`. |
| `issue_id` | Generated `rdiissue_` id. |
| `issue_code` | Stable impact issue code. |
| `severity` | `blocker` or `warning`. |
| `safe_summary` | Synthetic-safe issue summary. |
| `source_ref` | Optional safe source id. |
| `blocks_preview` | True for blocker issues. |
| `created_at` | Issue timestamp. |

Required invariants:

- extra fields are forbidden;
- blocker severity always blocks preview readiness.

### ReviewDecisionArtifactImpact

Implementation:

- `practical_chat_agent.services.review_decision_impact_preview.ReviewDecisionArtifactImpact`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_decision_artifact_impact_v1`. |
| `impact_id` | Generated `rdiart_` id. |
| `artifact_kind` | Workspace artifact kind. |
| `artifact_id` | Safe artifact id. |
| `candidate_binding_id` | Bound candidate binding id. |
| `queue_item_id` | Bound review queue item id. |
| `review_decision_ids` | Safe decision refs carried by the artifact binding. |
| `safe_summary` | Safe artifact summary. |
| `source_refs` | Redacted source refs. |
| `issue_codes` | Artifact issue codes. |
| `blocking_issue_codes` | Artifact blocker issue codes. |
| `preview_only` | Always true. |
| `review_required` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `runtime_ready` | Always false. |
| `created_at` | Impact timestamp. |

Supported artifact families:

- `memory_lifecycle_dry_run_plan`
- `persona_growth_dry_run_plan`
- `distillation_review_readiness_summary`

Required invariants:

- artifact impacts are review-required and preview-only;
- artifact impacts cannot apply changes;
- artifact impacts cannot write memory stores or persona versions;
- artifact impacts are never runtime-ready;
- refs and issue codes are deduplicated.

### ReviewDecisionImpactPreview

Implementation:

- `practical_chat_agent.services.review_decision_impact_preview.ReviewDecisionImpactPreview`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_decision_impact_preview_v1`. |
| `preview_id` | Generated `rdiprev_` id. |
| `bundle_id` | Source workspace bundle id. |
| `decision_id` | Review queue decision id. |
| `item_id` | Reviewed queue item id. |
| `candidate_kind` | Reviewed candidate kind. |
| `candidate_id` | Reviewed candidate id. |
| `reviewer_id` | Reviewer id from the decision record. |
| `decision` | `approve`, `reject`, `freeze`, or `request_changes`. |
| `candidate_binding_id` | Matched candidate binding id when available. |
| `safe_summary` | Safe candidate summary or mismatch summary. |
| `reason_labels` | Safe reason labels from the matched candidate binding. |
| `source_refs` | Redacted source refs from the matched candidate binding. |
| `artifact_impacts` | Safe artifact impact summaries. |
| `issues` | Decision impact issues. |
| `issue_codes` | Deduplicated issue codes. |
| `blocking_issue_codes` | Deduplicated blocker issue codes. |
| `preview_outcome` | Non-applying outcome label. |
| `future_manual_apply_eligible` | True only for unblocked approve decisions. |
| `review_required` | Always true. |
| `preview_only` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `runtime_ready` | Always false. |
| `created_at` | Preview timestamp. |

Outcome mapping:

| Decision State | Outcome |
| --- | --- |
| Any blocker | `blocked_before_apply` |
| Unblocked `approve` | `future_manual_apply_eligible` |
| Unblocked `reject` | `rejected_for_future_apply` |
| Unblocked `freeze` | `frozen_for_later_reconsideration` |
| Unblocked `request_changes` | `changes_requested_before_apply` |

Required invariants:

- future manual apply eligibility is true only for unblocked approve
  decisions;
- blocker issues force `blocked_before_apply`;
- previews are review-required and preview-only;
- previews cannot apply changes;
- previews cannot write memory stores or persona versions;
- previews are never runtime-ready;
- reason labels, source refs, and issue codes are deduplicated.

### ReviewDecisionImpactPreviewService

Implementation:

- `practical_chat_agent.services.review_decision_impact_preview.ReviewDecisionImpactPreviewService`

Methods:

| Method | Behavior |
| --- | --- |
| `preview_decision(bundle, decision_record)` | Builds a non-applying preview for one review decision and one workspace bundle. |

Binding behavior:

- matches candidate bindings by queue item id first;
- reports `decision_item_not_in_workspace` when no queue item id matches;
- reports `decision_candidate_kind_mismatch` when the item matches but the
  candidate kind differs;
- reports `decision_candidate_id_mismatch` when the item matches but the
  candidate id differs;
- carries candidate binding blocker issues into the preview;
- summarizes artifact bindings attached to the matched candidate binding;
- carries artifact blocker issue codes into preview blocker state.

## Forbidden Fields And Surfaces

The implemented records must not contain:

- raw private chat text;
- raw transcripts;
- private message bodies;
- private chat history paths;
- provider credentials;
- platform recipient ids;
- send queues;
- schedules;
- webhooks;
- tokens;
- delivery state;
- microphone, camera, audio, image, or video payloads;
- generated media paths;
- runtime reply-generation fields;
- decision apply executor fields;
- persona synthesis fields;
- mutation executor fields.

The service must not expose methods for:

- sending or scheduling;
- delivery;
- provider calls;
- webhooks;
- memory or persona mutation;
- review decision apply;
- PersonaVersionStore writes;
- deletion executors;
- retrieval enablement;
- persona synthesis;
- reply generation;
- voice/avatar/audio/image/video generation.

## Tests

Implemented tests:

- `tests/test_review_decision_impact_preview.py`

Covered behavior:

- approve decisions on ready bundles produce preview-only future manual-apply
  eligibility without applying changes;
- reject, freeze, and request-changes decisions produce non-applying outcome
  labels;
- mismatched decision item ids, candidate kinds, and candidate ids produce
  blocker issues;
- candidate binding blockers are carried into previews;
- artifact impacts preserve safe refs without applying dry-run plans;
- artifact blockers are carried into preview blocker state;
- serialized previews do not contain forbidden private/provider/outbound/media
  fields;
- service exposes no runtime, delivery, provider, mutation, apply, synthesis,
  voice/avatar, or media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\review_decision_impact_preview.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_decision_impact_preview.py tests\test_review_workspace_snapshot_store.py tests\test_review_workspace_bindings.py -q -o cache_dir=artifacts\t385_pytest_cache --basetemp=artifacts\t385_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T385 does not implement:

- private data ingestion;
- source readers;
- extraction from real logs;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- de-identification quality validation;
- PersonaCard synthesis;
- final companion reply generation;
- runtime memory or persona mutation;
- decision apply paths;
- deletion executors;
- review UI;
- snapshot export manifests;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Impact previews are local prototype records, not an apply executor.
- The preview trusts already-created safe workspace bindings and does not
  independently validate source candidate contents.
- Future manual apply eligibility is only a preview label, not permission to
  mutate production stores.
- T386 still needs a safe export manifest for workspace snapshots and impact
  previews.
