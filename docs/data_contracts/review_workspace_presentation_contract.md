# Review Workspace Presentation Contract

Task: T389 Review Workspace Presentation Adapter
Status: worker draft for review

## Scope

This contract describes the implemented UI-ready presentation records in
`src/practical_chat_agent/ui/review_workspace_adapter.py`.

The records project safe M28 review workspace records into deterministic cards,
badges, filters, and summaries for a later local static panel. They do not
apply decisions, mutate memory stores, write persona versions, synthesize
personas, call providers, generate replies, send messages, create static UI
assets, connect to platform delivery, enable voice/avatar runtime, generate
media, or recreate real people.

## Implemented Records

### ReviewWorkspaceStatusBadge

Implementation:

- `practical_chat_agent.ui.review_workspace_adapter.ReviewWorkspaceStatusBadge`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_workspace_status_badge_v1`. |
| `badge_id` | Generated `rwbadge_` id. |
| `label` | UI-ready status label. |
| `tone` | `blocked`, `eligible`, `review`, or `info`. |
| `issue_codes` | Safe issue codes. |
| `blocking_issue_codes` | Safe blocker codes. |
| `review_required` | Always true. |
| `preview_only` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `runtime_ready` | Always false. |
| `created_at` | Badge timestamp. |

### ReviewWorkspacePresentationCard

Implementation:

- `practical_chat_agent.ui.review_workspace_adapter.ReviewWorkspacePresentationCard`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_workspace_presentation_card_v1`. |
| `card_id` | Generated `rwcard_` id. |
| `card_kind` | `workspace_item`, `decision_impact`, or `export_summary`. |
| `title` | UI-ready title. |
| `display_label` | UI-ready compact label. |
| `safe_summary` | Safe summary text. |
| `filter_keys` | Deterministic filter keys. |
| `status_badges` | UI-ready badges. |
| `bundle_id` | Optional source bundle id. |
| `queue_item_id` | Optional source review queue item id. |
| `candidate_kind` | Optional review candidate kind. |
| `candidate_id` | Optional safe candidate id. |
| `decision_id` | Optional review decision id. |
| `preview_outcome` | Optional decision impact outcome. |
| `reason_labels` | Safe reason labels. |
| `source_refs` | Redacted source refs. |
| `issue_codes` | Safe issue codes. |
| `blocking_issue_codes` | Safe blocker codes. |
| `counts` | Export summary counts. |
| `urgency_rank` | Sorting rank, with blocked cards before eligible cards. |
| `review_required` | Always true. |
| `preview_only` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `runtime_ready` | Always false. |
| `created_at` | Card timestamp. |

Card kinds:

- `workspace_item`: one safe candidate binding card.
- `decision_impact`: one safe review decision impact card.
- `export_summary`: one safe export-manifest count card.

### ReviewWorkspacePresentationPanel

Implementation:

- `practical_chat_agent.ui.review_workspace_adapter.ReviewWorkspacePresentationPanel`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `review_workspace_presentation_panel_v1`. |
| `panel_id` | Generated `rwpanel_` id. |
| `cards` | Sorted presentation cards. |
| `filter_tabs` | Fixed UI filter metadata. |
| `review_required` | Always true. |
| `preview_only` | Always true. |
| `applies_changes` | Always false. |
| `writes_memory_store` | Always false. |
| `writes_persona_version` | Always false. |
| `runtime_ready` | Always false. |
| `created_at` | Panel timestamp. |

Filter tab order:

1. `all`
2. `blocked`
3. `eligible`
4. `memory`
5. `persona`
6. `distillation`

### ReviewWorkspacePresentationAdapter

Implementation:

- `practical_chat_agent.ui.review_workspace_adapter.ReviewWorkspacePresentationAdapter`

Method:

| Method | Behavior |
| --- | --- |
| `build_panel(bundles, impact_previews=None, export_manifest=None)` | Builds a deterministic presentation panel from safe M28 records. |

## Required Invariants

- Presentation records are review-required and preview-only.
- Presentation records cannot apply changes.
- Presentation records cannot write memory stores or persona versions.
- Presentation records are never runtime-ready.
- Cards contain only safe ids, display labels, safe summaries, reason labels,
  redacted source refs, issue codes, blocker codes, counts, and flags.
- Cards sort deterministically by urgency, bundle id, queue item id, candidate
  id, decision id, and card id.
- Blocked cards sort before eligible routine cards.
- Filter tabs are deterministic and count cards by filter key.

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

The adapter must not expose methods for:

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

- `tests/test_review_workspace_presentation_adapter.py`

Covered behavior:

- workspace bundles produce safe presentation cards;
- decision impact previews produce outcome/status badges;
- export manifests produce safe count summaries;
- tabs and filter metadata are deterministic;
- blocked cards sort before eligible routine cards;
- serialized presentation panels do not contain forbidden
  private/provider/outbound/media fields;
- adapter exposes no runtime, delivery, provider, mutation, apply, synthesis,
  voice/avatar, or media methods.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\review_workspace_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_presentation_adapter.py tests\test_review_workspace_safe_export.py tests\test_review_decision_impact_preview.py -q -o cache_dir=artifacts\t389_pytest_cache --basetemp=artifacts\t389_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T389 does not implement:

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
- static UI assets;
- local server routes;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Presentation records are local UI view models, not a user-validated UI.
- No static review panel has been added yet.
- The adapter trusts already-created safe M28 records and does not
  independently validate source candidate contents.
- No apply executor or real-data import/de-identification quality evaluation
  exists.
