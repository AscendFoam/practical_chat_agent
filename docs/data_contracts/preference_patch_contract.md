# PreferencePatch Candidate Contract

Updated: 2026-05-18

## Purpose

`PreferencePatchCandidate` represents a reviewable proposal to adjust communication behavior toward a specific contact, derived from repeated human feedback on ReplyPlan candidates.

Patches are **candidate-only**. They must not be auto-approved, auto-applied, or injected into runtime context without explicit human review.

## Scope

This contract covers T160 (schema definition) only. Later tasks (T161-T164) handle clustering, proposal generation, review CLI, and compact context integration. This contract must remain stable across those tasks without schema breakage.

## Review-Only Lifecycle

```text
feedback records (T140)
  -> aggregated feedback summary (T142)
  -> clustering (T161, future)
  -> PreferencePatchCandidate (status=candidate)
  -> human review CLI (T163, future)
  -> approved / rejected / frozen / archived
  -> compact context integration (T164, future)
```

Status values follow the existing `DistillationStatus` convention:

- `candidate`: default, not yet reviewed
- `approved`: human-reviewed and accepted (required for runtime readiness)
- `rejected`: human-reviewed and declined
- `frozen`: temporarily held from application
- `archived`: no longer active

`is_runtime_ready()` returns `True` only when `status == "approved"` AND `review_metadata.reviewed_by_human == True` AND `review_metadata.last_decision == "approved"`. By default, a new `PreferencePatchCandidate` is NOT runtime-ready.

## Patch Types

| Value | Meaning |
| --- | --- |
| `tone_preference` | How formal, casual, warm, or reserved the reply should be |
| `length_preference` | Whether replies should be short, medium, or long |
| `boundary_preference` | Topics or interaction patterns to avoid or approach cautiously |
| `topic_preference` | Subjects the contact prefers or dislikes discussing |
| `question_style` | Whether and how to ask follow-up questions |
| `humor_style` | Whether and what kind of humor is appropriate |
| `repair_style` | How to recover from miscommunication or awkward moments |
| `proactivity_preference` | Whether to initiate topics or wait for the contact |

## Field Semantics

### Required Fields

| Field | Type | Constraint | Description |
| --- | --- | --- | --- |
| `patch_id` | `str` | auto-generated | Unique identifier |
| `contact_id` | `str` | min_length=1 | Target contact |
| `patch_type` | `PreferencePatchType` | enum | Category of communication preference |
| `claim` | `str` | min_length=1 | One-sentence summary of the observed preference |
| `behavior_instruction` | `str` | min_length=1 | Concrete instruction for how the planner should adjust |
| `supporting_feedback_ids` | `list[str]` | min_length=1 | Feedback record IDs backing this patch; must not be empty |
| `confidence` | `float` | 0.0-1.0 | How strongly the evidence supports this patch |
| `sensitivity` | `DistillationSensitivity` | enum | low/medium/high |

### Optional Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `instruction_scope` | `str` | `"per_contact"` | Granularity: per_contact, per_topic, per_relationship_state, etc. |
| `rationale_summary` | `str or None` | `None` | Why this patch was proposed |
| `supporting_cluster_ids` | `list[str]` | `[]` | Optional cluster IDs if T161 clustering produced them |
| `positive_examples` | `list[str]` | `[]` | Safe references or summaries of feedback supporting the preference |
| `negative_examples` | `list[str]` | `[]` | Safe references or summaries of feedback contradicting the preference |
| `affected_candidate_types` | `list[str]` | `[]` | Which approach labels or candidate shapes this patch would influence |

### Metadata Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `status` | `DistillationStatus` | `"candidate"` | Review lifecycle status |
| `review_metadata` | `DistilledArtifactReviewMetadata` | default factory | Compatible with existing store/review pattern |
| `created_at` | `datetime` | utc_now | Creation timestamp |
| `updated_at` | `datetime` | utc_now | Last update timestamp |

## Safety Constraints

1. **Evidence-backed**: `supporting_feedback_ids` must contain at least 1 ID. A patch without supporting feedback is structurally invalid and cannot be created.
2. **No raw text**: No field stores raw transcript text, edited reply text, private notes, or private note bodies. `positive_examples` and `negative_examples` contain only safe references or summaries.
3. **Candidate-only by default**: `status` defaults to `"candidate"`. `review_metadata.reviewed_by_human` defaults to `False`. `is_runtime_ready()` returns `False` until all three conditions are met.
4. **No auto-mutation**: This schema does not provide or imply any path to mutate ContactSkill, MemoryFact, approved store records, planner templates, or outbound behavior. Approved patches may later influence compact context (T164), but only after explicit human review.
5. **No LLM**: This schema does not require or imply LLM use. T161 clustering and T162 proposal generation may optionally use LLMs under separate task authorization.

## Compatibility with Later M5 Tasks

- T161 (feedback clusterer) outputs cluster IDs that map to `supporting_cluster_ids`. Cluster contract defined below.
- T162 (patch proposal CLI) creates `PreferencePatchCandidate` instances and must enforce `supporting_feedback_ids` non-empty.
- T163 (patch review CLI) updates `status` and `review_metadata`, using the same `DistilledArtifactReviewMetadata` pattern as T122.
- T164 (approved patch compact context) reads only `status="approved"` patches with `is_runtime_ready() == True`.

## Feedback Cluster Contract (T161)

Updated: 2026-05-18

### Purpose

`FeedbackClusterService` groups validated T140 feedback records into deterministic, privacy-safe aggregate clusters by rule-based signals. Clusters are intermediate artifacts between raw feedback and patch candidates.

### Cluster Label Derivation

Labels are derived deterministically from feedback record fields:

| Action | Default Label | Override Condition |
| --- | --- | --- |
| `accept` | `good_tone` | None |
| `reject` | `not_like_me` | None |
| `boundary` | `boundary_violation` | If `boundary_label` normalizes to a known label, use that instead |
| `edit` | _unlabeled_ | No safe deterministic label exists yet; edits are not clustered |

Known labels: `too_long`, `too_cold`, `too_eager`, `too_formal`, `too_intimate`, `boundary_violation`, `not_like_me`, `good_tone`.

### Cluster Output Shape

```json
{
  "schema_version": "feedback_cluster_v1",
  "generated_at": "...",
  "input_path": "...",
  "is_readable": true,
  "total_records": 10,
  "labeled_records": 8,
  "unlabeled_records": 2,
  "clustered_records": 8,
  "unclustered_records": 2,
  "skipped_invalid_records": 0,
  "cluster_count": 3,
  "clusters": [
    {
      "cluster_id": "cluster_<sha256_hex_16>",
      "contact_id": "...",
      "cluster_label": "not_like_me",
      "supporting_feedback_ids": ["fb_...", "fb_..."],
      "record_count": 3,
      "counts_by_action": {"reject": 3},
      "counts_by_approach_label": {"warm_casual": 2},
      "counts_by_priority_rank": {"1": 2, "2": 1},
      "time_range": {"earliest": "...", "latest": "..."},
      "reason_tag_summary": null
    }
  ]
}
```

### Cluster ID Stability

`cluster_id` is derived from `sha256(contact_id:cluster_label)[:16]`. Identical `(contact_id, cluster_label)` always produces the same `cluster_id`, regardless of which records are present. Adding or removing records does not change the cluster ID for an existing grouping key.

### Privacy Safety

Cluster output contains NO raw feedback text, edited text, user notes, boundary notes, or draft text. All fields are aggregate counts, IDs, or timestamps.

## Patch Proposal Output Contract (T162)

Updated: 2026-05-18

### Purpose

`PatchProposalService` consumes T161 cluster output and produces deterministic, candidate-only `PreferencePatchCandidate` proposals. Proposals are not auto-approved, not auto-applied, and not injected into runtime context.

### CLI Shape

```text
chat-feedback-propose-patch --cluster-report <path> --output <private path>
```

### Proposal Output Shape

```json
{
  "schema_version": "patch_proposal_v1",
  "generated_at": "...",
  "input_path": "...",
  "candidate_count": 2,
  "skipped_cluster_count": 3,
  "candidates": [
    {
      "patch": {
        "schema_version": "preference_patch_candidate_v1",
        "patch_id": "patch_...",
        "contact_id": "...",
        "patch_type": "tone_preference",
        "instruction_scope": "per_contact",
        "claim": "...",
        "behavior_instruction": "...",
        "rationale_summary": "...",
        "supporting_feedback_ids": ["fb_...", "fb_..."],
        "supporting_cluster_ids": ["cluster_..."],
        "positive_examples": [],
        "negative_examples": [],
        "affected_candidate_types": ["warm_casual"],
        "status": "candidate",
        "confidence": 0.6,
        "sensitivity": "low",
        "review_metadata": {
          "reviewed_by_human": false,
          "last_decision": null,
          "notes": []
        },
        "created_at": "...",
        "updated_at": "..."
      },
      "source_cluster_id": "cluster_..."
    }
  ],
  "skipped_clusters": [
    {
      "cluster_id": "cluster_...",
      "skip_reason": "insufficient_support",
      "record_count": 1
    }
  ]
}
```

### Deterministic Label-to-Type Mapping

| Cluster Label | Patch Type | Sensitivity |
| --- | --- | --- |
| `too_long` | `length_preference` | low |
| `too_formal` | `tone_preference` | low |
| `too_cold` | `tone_preference` | low |
| `too_eager` | `proactivity_preference` | medium |
| `too_intimate` | `boundary_preference` | high |
| `boundary_violation` | `boundary_preference` | high |

Labels not in this table (`good_tone`, `not_like_me`, unknown labels) produce no patch candidate. They are skipped with reason `no_safe_mapping`.

### Skip Reasons

| Reason | Meaning |
| --- | --- |
| `insufficient_support` | `record_count < 2` or `supporting_feedback_ids` empty |
| `unlabeled_cluster` | Cluster has no `cluster_label` |
| `no_safe_mapping` | Label does not map to any `PreferencePatchType` |
| `ambiguous_label` | Reserved for future use if multi-label conflicts arise |

### Confidence Formula

`confidence = min(0.3 + 0.15 * (record_count - 1), 0.9)`, bounded to [0.0, 1.0]. Monotonically increasing with evidence count, capped at 0.9. Does not claim calibrated probability.

### Privacy Safety

Proposal output contains NO raw feedback text, edited text, user notes, boundary notes, or draft text. `positive_examples` and `negative_examples` are always empty lists at proposal generation time. All field content is derived deterministically from cluster labels and aggregate metadata.

### Determinism Guarantee

Given identical cluster report input, repeated runs produce identical `patch_id` values, `claim` text, `behavior_instruction` text, `confidence` values, and `skipped_clusters` entries. Only `generated_at`, `created_at`, and `updated_at` differ between runs.

## Anti-Patterns

Do NOT:

- Auto-generate patches from single feedback records without clustering.
- Auto-approve patches based on confidence thresholds.
- Inject patch instructions directly into runtime prompts without the T164 compact context layer.
- Store raw feedback text, edited text, or private notes in any patch field.
- Treat `positive_examples` or `negative_examples` as a replacement for `supporting_feedback_ids`.
