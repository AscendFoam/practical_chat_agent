# Review Workspace Safe Export Contract

Task: T386 Review Workspace Safe Export Manifest
Status: worker draft for review

## Scope

This contract describes the implemented safe export manifest records in
`src/practical_chat_agent/services/review_workspace_export.py`.

The records package safe `ReviewWorkspaceBundle` summaries and
`ReviewDecisionImpactPreview` summaries for local review/audit surfaces. They
do not apply decisions, mutate memory stores, write persona versions,
synthesize personas, call providers, generate replies, send messages, create
UI, connect to platform delivery, enable voice/avatar runtime, generate media,
or recreate real people.

## Implemented Records

### ReviewWorkspaceExportItem

Implementation:

- `practical_chat_agent.services.review_workspace_export.ReviewWorkspaceExportItem`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_workspace_export_item_v1`. |
| `export_item_id` | Generated `rwexpitem_` id. |
| `bundle_id` | Source workspace bundle id. |
| `queue_item_id` | Bound review queue item id. |
| `candidate_binding_id` | Source candidate binding id. |
| `candidate_kind` | Review candidate kind. |
| `candidate_id` | Safe candidate id. |
| `safe_summary` | Safe candidate summary. |
| `reason_labels` | Safe review reason labels. |
| `source_refs` | Redacted source refs. |
| `artifact_kinds` | Safe artifact kind labels attached to the candidate binding. |
| `artifact_ids` | Safe artifact ids attached to the candidate binding. |
| `issue_codes` | Workspace and binding issue codes. |
| `blocking_issue_codes` | Workspace and binding blocker codes. |
| `workspace_ready` | True only when source bundle and binding are ready. |
| `review_required` | Always true. |
| `preview_only` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `runtime_ready` | Always false. |
| `created_at` | Export item timestamp. |

Required invariants:

- export items are review-required and preview-only;
- export items cannot apply changes;
- export items cannot write memory stores or persona versions;
- export items are never runtime-ready;
- safe labels, refs, artifact ids, and issue codes are deduplicated.

### ReviewWorkspaceImpactExportItem

Implementation:

- `practical_chat_agent.services.review_workspace_export.ReviewWorkspaceImpactExportItem`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_workspace_impact_export_item_v1`. |
| `export_item_id` | Generated `rwimpactexp_` id. |
| `bundle_id` | Source workspace bundle id. |
| `preview_id` | Source decision impact preview id. |
| `decision_id` | Source review queue decision id. |
| `item_id` | Reviewed queue item id. |
| `candidate_kind` | Reviewed candidate kind. |
| `candidate_id` | Reviewed candidate id. |
| `decision` | Review decision label. |
| `preview_outcome` | Non-applying impact outcome. |
| `future_manual_apply_eligible` | True only for unblocked approve previews. |
| `safe_summary` | Safe impact summary. |
| `reason_labels` | Safe reason labels. |
| `source_refs` | Redacted source refs. |
| `artifact_ids` | Safe artifact ids summarized by the preview. |
| `issue_codes` | Impact issue codes. |
| `blocking_issue_codes` | Impact blocker codes. |
| `review_required` | Always true. |
| `preview_only` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `runtime_ready` | Always false. |
| `created_at` | Export item timestamp. |

Required invariants:

- impact export items are review-required and preview-only;
- impact export items cannot apply changes;
- impact export items cannot write memory stores or persona versions;
- impact export items are never runtime-ready;
- safe labels, refs, artifact ids, and issue codes are deduplicated.

### ReviewWorkspaceSafeExportManifest

Implementation:

- `practical_chat_agent.services.review_workspace_export.ReviewWorkspaceSafeExportManifest`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_workspace_safe_export_manifest_v1`. |
| `manifest_id` | Generated `rwexport_` id. |
| `workspace_items` | Safe workspace candidate export items. |
| `impact_items` | Safe review decision impact export items. |
| `counts_by_candidate_kind` | Deterministic counts by candidate kind. |
| `counts_by_artifact_kind` | Deterministic counts by artifact kind. |
| `counts_by_decision_outcome` | Deterministic counts by impact preview outcome. |
| `counts_by_blocker_code` | Deterministic counts by blocker code across exported workspace and impact items. |
| `review_required` | Always true. |
| `preview_only` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `runtime_ready` | Always false. |
| `generated_at` | Manifest timestamp. |

Required invariants:

- manifests are review-required and preview-only;
- manifests cannot apply changes;
- manifests cannot write memory stores or persona versions;
- manifests are never runtime-ready;
- workspace items are sorted by bundle id, queue item id, and candidate id;
- impact items are sorted by bundle id, item id, candidate id, decision id,
  and preview id;
- counts are recomputed deterministically on validation.

### ReviewWorkspaceSafeExportService

Implementation:

- `practical_chat_agent.services.review_workspace_export.ReviewWorkspaceSafeExportService`

Methods:

| Method | Behavior |
| --- | --- |
| `build_manifest(bundles, impact_previews=None)` | Builds a safe export manifest from workspace bundles and optional impact previews. |
| `write_manifest(manifest, root, file_name=None)` | Writes manifest JSON under a caller-supplied local export root. |

Path-safety invariants:

- export roots are caller supplied;
- parent directories are created as needed;
- absolute file names are rejected;
- path traversal outside the export root is rejected;
- export files must use `.json`.

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

- `tests/test_review_workspace_safe_export.py`

Covered behavior:

- safe export manifests include workspace bundle summaries and impact preview
  summaries without raw private content;
- counts by candidate kind, artifact kind, decision outcome, and blocker code
  are deterministic;
- workspace and impact item ordering is deterministic;
- optional JSON writing rejects path traversal;
- serialized exports do not contain forbidden private/provider/outbound/media
  fields;
- service exposes no runtime, delivery, provider, mutation, apply, synthesis,
  voice/avatar, or media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\review_workspace_export.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_safe_export.py tests\test_review_decision_impact_preview.py tests\test_review_workspace_snapshot_store.py tests\test_review_workspace_bindings.py -q -o cache_dir=artifacts\t386_pytest_cache --basetemp=artifacts\t386_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T386 does not implement:

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
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Export manifests are local prototype records, not production audit exports.
- Exports summarize already-created safe workspace and impact records; they do
  not independently validate source candidate contents.
- No user-facing review UI or apply executor exists.
- T387 still needs adversarial milestone review for M28.
