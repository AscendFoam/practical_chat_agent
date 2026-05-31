# Review Workspace Binding Contract

Task: T383 Review Workspace Binding Records
Status: worker draft for review

## Scope

This contract describes the implemented local review workspace binding records
in `src/practical_chat_agent/services/review_workspace.py`.

The records connect review queue items to source candidates and related
dry-run/readiness artifacts. They do not apply decisions, mutate memory
stores, write persona versions, synthesize personas, read private chat logs,
call providers, generate replies, send messages, create UI, persist data,
connect to platform delivery, enable voice/avatar runtime, generate media, or
recreate real people.

## Implemented Records

### ReviewWorkspaceBindingIssue

Implementation:

- `practical_chat_agent.services.review_workspace.ReviewWorkspaceBindingIssue`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_workspace_binding_issue_v1`. |
| `issue_id` | Generated `rwissue_` id. |
| `issue_code` | Stable binding issue code. |
| `severity` | `blocker` or `warning`. |
| `safe_summary` | Synthetic-safe issue summary. |
| `source_ref` | Optional source id. |
| `blocks_workspace` | True for blocker issues. |
| `created_at` | Issue timestamp. |

Required invariants:

- extra fields are forbidden;
- blocker severity always blocks workspace readiness.

### ReviewWorkspaceCandidateBinding

Implementation:

- `practical_chat_agent.services.review_workspace.ReviewWorkspaceCandidateBinding`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_workspace_candidate_binding_v1`. |
| `binding_id` | Generated `rwbind_` id. |
| `queue_item_id` | Bound review queue item id. |
| `candidate_kind` | Queue item candidate kind. |
| `queue_candidate_id` | Candidate id stored on the queue item. |
| `source_candidate_id` | Candidate id inferred from the source record. |
| `source_schema_version` | Source record schema version when available. |
| `owner_user_id` | Owner user id when available. |
| `persona_id` | Persona id when available. |
| `safe_summary` | Safe queue summary. |
| `reason_labels` | Review reason labels. |
| `source_refs` | Redacted source refs. |
| `priority_score` | Queue priority score. |
| `priority_band` | Queue priority band. |
| `issues` | Binding issues. |
| `issue_codes` | Deduplicated issue codes. |
| `blocking_issue_codes` | Deduplicated blocker issue codes. |
| `binding_ready` | True only when no blocker issue exists. |
| `review_required` | Always true. |
| `runtime_ready` | Always false. |
| `created_at` | Binding timestamp. |

Supported candidate families:

- `MemoryContradictionCandidate`
- `MemorySupersessionCandidate`
- `MemoryDeletionCascadePlan`
- `PersonaGrowthEvidenceBundle`
- `PersonaGrowthPatchCandidate`
- `SyntheticDistillationInputManifest`
- `DeidentifiedStyleFeatureCandidate`
- `MemoryRetrievalExplanationResult`

Required invariants:

- candidate-kind mismatch produces `candidate_kind_mismatch`;
- candidate-id mismatch produces `candidate_id_mismatch`;
- blocker issues force `binding_ready=false`;
- records require review and are never runtime-ready.

### ReviewWorkspaceArtifactBinding

Implementation:

- `practical_chat_agent.services.review_workspace.ReviewWorkspaceArtifactBinding`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_workspace_artifact_binding_v1`. |
| `binding_id` | Generated `rwart_` id. |
| `artifact_kind` | `memory_lifecycle_dry_run_plan`, `persona_growth_dry_run_plan`, or `distillation_review_readiness_summary`. |
| `artifact_id` | Source artifact id. |
| `source_candidate_kind` | Candidate kind the artifact belongs to. |
| `source_candidate_id` | Candidate id the artifact belongs to. |
| `candidate_binding_id` | Candidate binding id. |
| `queue_item_id` | Candidate binding queue item id. |
| `review_queue_item_ids` | Review queue refs carried by the artifact. |
| `review_decision_ids` | Review decision refs carried by the artifact. |
| `safe_summary` | Safe artifact summary. |
| `source_refs` | Redacted source refs. |
| `issues` | Artifact binding issues. |
| `issue_codes` | Deduplicated issue codes. |
| `blocking_issue_codes` | Deduplicated blocker issue codes. |
| `artifact_ready` | True only when no blocker issue exists. |
| `preview_only` | Always true. |
| `review_required` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `runtime_ready` | Always false. |
| `created_at` | Binding timestamp. |

Required invariants:

- artifact source kind mismatch produces `artifact_candidate_kind_mismatch`;
- artifact source candidate id mismatch produces
  `artifact_source_candidate_id_mismatch`;
- distillation readiness summaries must reference the bound review queue item
  or produce `review_queue_item_ref_mismatch`;
- artifact readiness blockers are copied into workspace blocker issues;
- artifact bindings remain preview-only, review-required, non-applying, and
  non-runtime-ready.

### ReviewWorkspaceBundle

Implementation:

- `practical_chat_agent.services.review_workspace.ReviewWorkspaceBundle`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_workspace_bundle_v1`. |
| `bundle_id` | Generated `rwbundle_` id. |
| `candidate_bindings` | Candidate bindings in the workspace. |
| `artifact_bindings` | Artifact bindings in the workspace. |
| `issue_codes` | Aggregated issue codes. |
| `blocking_issue_codes` | Aggregated blocker issue codes. |
| `workspace_ready` | True only when all bindings are ready. |
| `review_required` | Always true. |
| `preview_only` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `runtime_ready` | Always false. |
| `created_at` | Bundle timestamp. |

### ReviewWorkspaceService

Implementation:

- `practical_chat_agent.services.review_workspace.ReviewWorkspaceService`

Methods:

| Method | Behavior |
| --- | --- |
| `bind_candidate(queue_item, source_candidate)` | Creates a candidate binding and records mismatches. |
| `bind_artifact(candidate_binding, artifact)` | Creates a dry-run/readiness artifact binding and records mismatches. |
| `build_bundle(candidate_bindings=None, artifact_bindings=None)` | Aggregates readiness and issue codes. |

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
- generated media paths;
- runtime reply-generation methods;
- decision apply methods;
- persona synthesis methods;
- mutation methods;
- voice/avatar/media generation methods.

## Tests

Implemented tests:

- `tests/test_review_workspace_bindings.py`

Covered behavior:

- matching queue items and source candidates produce ready bindings;
- candidate-kind mismatch blocks workspace readiness;
- candidate-id mismatch blocks workspace readiness;
- memory lifecycle dry-run plans attach only to matching source candidate ids;
- persona growth dry-run plans attach only to matching patch ids;
- distillation readiness summaries preserve review queue refs and block
  mismatched queue refs;
- bundles are not ready when any binding blocks;
- extra private/provider/outbound/media fields are rejected;
- service exposes no runtime, delivery, provider, mutation, apply, synthesis,
  voice/avatar, or media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\review_workspace.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_bindings.py tests\test_review_queue_candidates.py tests\test_memory_lifecycle_dry_run_apply.py tests\test_persona_growth_dry_run_apply.py tests\test_distillation_review_readiness.py -q -o cache_dir=artifacts\t383_pytest_cache --basetemp=artifacts\t383_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T383 does not implement:

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
- runtime memory or persona mutation;
- decision apply paths;
- deletion executors;
- review UI;
- persistence or snapshot storage;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Binding records do not persist workspace snapshots.
- Binding records do not execute approved changes.
- Distillation readiness still does not prove real-data de-identification
  quality.
- T384 still needs local snapshot storage.
