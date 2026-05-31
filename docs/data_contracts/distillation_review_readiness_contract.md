# Distillation Review Readiness Contract

Task: T380 Distillation Review Readiness Aggregator
Status: worker draft for review

## Scope

This contract describes the implemented local synthetic distillation readiness
records in
`src/practical_chat_agent/services/distillation_review_readiness.py`.

The records aggregate a `SyntheticDistillationInputManifest`, optional
`DeidentifiedStyleFeatureCandidate` records, and optional review queue refs
into a safe review-only summary. They do not synthesize personas, read private
chat logs, retain source text, apply review decisions, call providers, compute
embeddings, score similarity, generate replies, create proactive candidates,
send messages, connect to platform delivery, enable voice/avatar runtime,
generate media, or recreate real people.

## Implemented Records

### DistillationReadinessIssue

Implementation:

- `practical_chat_agent.services.distillation_review_readiness.DistillationReadinessIssue`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `distillation_readiness_issue_v1`. |
| `issue_id` | Generated `sdissue_` id. |
| `issue_code` | Stable readiness issue code. |
| `severity` | `blocker` or `warning`. |
| `safe_summary` | Synthetic-safe issue summary. |
| `source_ref` | Optional manifest, clone-risk, or feature id. |
| `blocks_readiness` | True for blocker issues. |
| `created_at` | Issue timestamp. |

Required invariants:

- extra fields are forbidden;
- blocker severity always blocks readiness;
- summaries must be safe and synthetic-only.

### DistillationReviewReadinessSummary

Implementation:

- `practical_chat_agent.services.distillation_review_readiness.DistillationReviewReadinessSummary`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `distillation_review_readiness_summary_v1`. |
| `summary_id` | Generated `sdready_` id. |
| `manifest_id` | Source synthetic manifest id. |
| `user_id` | Owner user id from the manifest. |
| `feature_ids` | De-identified style feature ids included in the summary. |
| `review_queue_item_ids` | Optional review queue item refs. |
| `safe_summary` | Synthetic-safe summary text. |
| `issues` | Readiness issues. |
| `issue_codes` | Deduplicated issue codes derived from issues. |
| `blocking_issue_codes` | Deduplicated blocker issue codes. |
| `source_text_retained` | True only when a supplied invalid feature retained source text. |
| `ready_for_persona_synthesis` | True only when all review-only prerequisites are structurally satisfied. |
| `review_required` | Always true. |
| `runtime_ready` | Always false. |
| `created_at` | Summary timestamp. |

Required invariants:

- summaries require review;
- summaries are never runtime-ready;
- blocking issues force `ready_for_persona_synthesis=false`;
- retained source text forces `ready_for_persona_synthesis=false`;
- ids and issue codes are deduplicated.

### DistillationReviewReadinessService

Implementation:

- `practical_chat_agent.services.distillation_review_readiness.DistillationReviewReadinessService`

Method:

- `build_summary(manifest, features=None, review_items=None)`

Required behavior:

- preserves manifest id, owner user id, feature ids, and review queue item ids;
- blocks readiness for manifest blocking reasons;
- blocks readiness for missing active `persona_distillation` consent;
- blocks readiness for withdrawn consent;
- blocks readiness for clone-risk decisions that do not allow safe
  transformation;
- blocks readiness for non-synthetic source categories;
- blocks readiness when no de-identified style feature is supplied;
- blocks readiness for feature/manifest mismatch, retained source text,
  missing review requirement, blocked features, and feature blocking reasons;
- does not apply review queue decisions.

## Readiness Issue Codes

Implemented issue codes include:

- manifest blocking reasons such as
  `persona_distillation_consent_missing_or_withdrawn`, `withdrawn_consent`,
  and `clone_risk_blocked`;
- `blocked_real_person_request` for non-synthetic source categories currently
  accepted only as blocked records;
- `no_style_features`;
- `feature_manifest_mismatch`;
- `feature_not_review_required`;
- `source_text_retained`;
- `feature_blocked_from_persona_synthesis`;
- de-identified feature blocking reasons such as
  `identifier_or_third_party_review_required`.

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
- voice/avatar/media generation methods.

## Tests

Implemented tests:

- `tests/test_distillation_review_readiness.py`

Covered behavior:

- active synthetic manifest plus safe feature can produce a review-ready
  summary;
- withdrawn consent blocks readiness;
- clone-risk block prevents readiness;
- retained source text or blocked features prevent readiness;
- missing active persona-distillation consent prevents readiness;
- review queue refs are preserved without applying decisions;
- extra private/provider/outbound/media fields are rejected;
- service exposes no runtime, delivery, provider, synthesis, voice/avatar, or
  media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\distillation_review_readiness.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_distillation_review_readiness.py tests\test_synthetic_distillation_input_candidates.py tests\test_review_queue_candidates.py -q -o cache_dir=artifacts\t380_pytest_cache --basetemp=artifacts\t380_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T380 does not implement:

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
- review UI;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Readiness summaries are local review records only; no user-facing review UI
  or persistence exists.
- Readiness does not prove de-identification quality on real data.
- Readiness does not approve real-person recreation or digital-twin behavior.
- Persona synthesis remains future work and must stay separately reviewed.
