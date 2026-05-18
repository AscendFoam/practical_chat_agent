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

- T161 (feedback clusterer) outputs cluster IDs that map to `supporting_cluster_ids`.
- T162 (patch proposal CLI) creates `PreferencePatchCandidate` instances and must enforce `supporting_feedback_ids` non-empty.
- T163 (patch review CLI) updates `status` and `review_metadata`, using the same `DistilledArtifactReviewMetadata` pattern as T122.
- T164 (approved patch compact context) reads only `status="approved"` patches with `is_runtime_ready() == True`.

## Anti-Patterns

Do NOT:

- Auto-generate patches from single feedback records without clustering.
- Auto-approve patches based on confidence thresholds.
- Inject patch instructions directly into runtime prompts without the T164 compact context layer.
- Store raw feedback text, edited text, or private notes in any patch field.
- Treat `positive_examples` or `negative_examples` as a replacement for `supporting_feedback_ids`.
