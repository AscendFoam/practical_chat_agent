# RelationshipState Contract

Updated: 2026-05-24 (T192, T193, T194)

## Purpose

`RelationshipState` represents a conservative, multidimensional snapshot of the relationship between the user and a specific contact. It is **review-only** and **candidate-only** by default: no automatic state mutation, no automatic action, and no collapse into a single scalar score.

`RelationshipDeltaCandidate` represents a proposed change to one or more dimensions of a `RelationshipState`, backed by evidence and requiring explicit human review before any state update.

## Scope

This contract covers T190 (schema definition), T192 (delta generation), T193 (delta review), and T194 (compact context integration). The remaining M8 task — relationship-aware eval (T195) — is handled later. This contract must remain stable across those tasks without schema breakage.

## Review-Only Lifecycle

```text
approved ContactSkill / feedback / memory evidence
  -> relationship signal extraction (T191, future)
  -> RelationshipDeltaCandidate (status=candidate)
  -> human review CLI (T193)
  -> approved / rejected / frozen / archived
  -> RelationshipState update (only after approved delta)
  -> compact context integration (T194)
  -> relationship-aware reply eval (T195, future)
```

Status values follow the existing `DistillationStatus` convention:

- `candidate`: default, not yet reviewed
- `approved`: human-reviewed and accepted
- `rejected`: human-reviewed and declined
- `frozen`: temporarily held
- `archived`: no longer active

`is_runtime_ready()` returns `True` only when `status == "approved"` AND `review_metadata.reviewed_by_human == True` AND `review_metadata.last_decision == "approved"`.

## RelationshipState Dimensions

Each dimension is an independent float in [0.0, 1.0]. No single score or weighted combination is derived from these dimensions. Each dimension must be interpreted independently.

| Dimension | Range | Interpretation |
| --- | --- | --- |
| `familiarity` | 0.0–1.0 | How well the user knows the contact's habits, preferences, and communication patterns |
| `trust` | 0.0–1.0 | Degree of mutual reliability and openness in the relationship |
| `warmth` | 0.0–1.0 | Emotional closeness and friendliness level |
| `reciprocity` | 0.0–1.0 | Balance of effort and engagement between user and contact |
| `conflict_level` | 0.0–1.0 | Current level of disagreement, tension, or friction (higher = more conflict) |
| `boundary_risk` | 0.0–1.0 | Risk of overstepping contact's boundaries or comfort zone |
| `initiative_allowance` | 0.0–1.0 | How much proactive engagement the contact is likely to welcome |
| `intimacy_level` | 0.0–1.0 | Depth of personal disclosure and vulnerability the relationship supports |

### Interaction Temperature

| Value | Meaning |
| --- | --- |
| `warm` | Recent interactions show active engagement and positive tone |
| `neutral` | Recent interactions are normal-paced, neither warm nor cold |
| `cold` | Recent interactions show withdrawal, short replies, or disengagement |
| `mixed` | Recent interactions show inconsistent temperature signals |
| `unknown` | No recent interaction data available |

## RelationshipState Fields

### Required Fields

| Field | Type | Constraint | Description |
| --- | --- | --- | --- |
| `contact_id` | `str` | min_length=1 | Target contact |
| `familiarity` | `float` | 0.0–1.0 | Familiarity dimension |
| `trust` | `float` | 0.0–1.0 | Trust dimension |
| `warmth` | `float` | 0.0–1.0 | Warmth dimension |
| `reciprocity` | `float` | 0.0–1.0 | Reciprocity dimension |
| `conflict_level` | `float` | 0.0–1.0 | Conflict level dimension |
| `boundary_risk` | `float` | 0.0–1.0 | Boundary risk dimension |
| `initiative_allowance` | `float` | 0.0–1.0 | Initiative allowance dimension |
| `intimacy_level` | `float` | 0.0–1.0 | Intimacy level dimension |
| `uncertainty` | `float` | 0.0–1.0 | Overall uncertainty of the assessment |
| `evidence_refs` | `list[str]` | min_length=1 | Evidence backing this state; must not be empty |

### Optional Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `recent_interaction_temperature` | `InteractionTemperature` | `"unknown"` | Recent interaction signal |
| `first_interaction_at` | `datetime or None` | `None` | Earliest known interaction timestamp |
| `last_interaction_at` | `datetime or None` | `None` | Most recent interaction timestamp |
| `assessment_rationale` | `str or None` | `None` | Why the state was assessed this way |
| `source_type` | `str` | `"unknown"` | How this state was produced (heuristic, signal_extractor, manual, unknown) |
| `source_skill_record_id` | `str or None` | `None` | Link to the originating ContactSkill store record |

### Metadata Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `state_id` | `str` | auto-generated | Unique identifier |
| `status` | `DistillationStatus` | `"candidate"` | Review lifecycle status |
| `review_metadata` | `DistilledArtifactReviewMetadata` | default factory | Compatible with existing store/review pattern |
| `assessed_at` | `datetime` | utc_now | When the assessment was made |
| `created_at` | `datetime` | utc_now | Creation timestamp |
| `updated_at` | `datetime` | utc_now | Last update timestamp |

## RelationshipDeltaCandidate Fields

### Required Fields

| Field | Type | Constraint | Description |
| --- | --- | --- | --- |
| `contact_id` | `str` | min_length=1 | Target contact |
| `source_state_id` | `str` | min_length=1 | The `state_id` of the current `RelationshipState` this delta applies to |
| `dimension_changes` | `list[RelationshipDeltaDimension]` | min_length=1 | At least one dimension must change |
| `delta_rationale` | `str` | min_length=1 | Why this delta is proposed |
| `evidence_refs` | `list[str]` | min_length=1 | Evidence backing this delta; must not be empty |

### Optional Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `signal_refs` | `list[str]` | `[]` | References to T191 signal records backing this delta |

### Metadata Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `delta_id` | `str` | auto-generated | Unique identifier |
| `status` | `DistillationStatus` | `"candidate"` | Review lifecycle status |
| `review_metadata` | `DistilledArtifactReviewMetadata` | default factory | Compatible with existing store/review pattern |
| `created_at` | `datetime` | utc_now | Creation timestamp |
| `updated_at` | `datetime` | utc_now | Last update timestamp |

## RelationshipDeltaDimension Fields

| Field | Type | Constraint | Description |
| --- | --- | --- | --- |
| `dimension_name` | `RELATIONSHIP_DIMENSION_NAMES` | enum | Which dimension is changing |
| `current_value` | `float` | 0.0–1.0 | Value in the source state |
| `proposed_value` | `float` | 0.0–1.0 | Proposed new value |
| `direction` | `RelationshipDeltaDirection` | enum | increase / decrease / stable / unknown |
| `magnitude` | `float` | 0.0–1.0 | Absolute change magnitude |
| `rationale` | `str or None` | optional | Why this specific dimension is changing |

## Safety Constraints

1. **Evidence-backed**: Both `RelationshipState` and `RelationshipDeltaCandidate` require `evidence_refs` with `min_length=1`. A state or delta without evidence is structurally invalid.
2. **No single score collapse**: The eight dimensions are independent floats. No weighted combination, overall score, or derived scalar is encoded in the schema.
3. **No raw text**: No field stores raw chat transcript, raw feedback text, edited reply text, or private notes.
4. **Candidate-only by default**: `status` defaults to `"candidate"`. `review_metadata.reviewed_by_human` defaults to `False`. `is_runtime_ready()` returns `False` until all three conditions are met.
5. **No auto-mutation**: This schema does not provide or imply any path to automatically update relationship state, modify ContactSkill, MemoryFact, or trigger outbound behavior.
6. **Review-first delta model**: `RelationshipDeltaCandidate` is the only mechanism to propose state changes, and it requires human review before the change takes effect.

## Compatibility with Later M8 Tasks

- T191 (signal extractor) produces `RelationshipSignal` records from boundary-labeled feedback. Each signal has a `signal_id` that `RelationshipDeltaCandidate.signal_refs` can reference.
- T192 (delta candidate generation) creates `RelationshipDeltaCandidate` instances with at least one `dimension_changes` entry and non-empty `evidence_refs`.
- T193 (review CLI) updates `status` and `review_metadata`, using the same `DistilledArtifactReviewMetadata` pattern as T122/T163.
- T194 (compact context) reads `RelationshipDeltaCandidate` instances with `status="approved"` and `is_runtime_ready() == True`, producing compact `ApprovedRelationshipContext` with dimension-change hints for `ChatContext`. No raw signal history, no raw review history, and no full dimension dump.
- T195 (relationship-aware eval) evaluates whether the dimension model improves reply quality over the flat `ContactSkillRelationshipState`.

## RelationshipSignal (T191)

A `RelationshipSignal` is a single, conservative, evidence-backed observation about one relationship dimension. Signals are intermediate artifacts: they are **not** state snapshots and **not** delta proposals. They exist so that T192 delta generation can aggregate multiple signals into a reviewable `RelationshipDeltaCandidate` without reading raw chat history or feedback text.

### How Signals Differ from State and Delta

| Layer | Model | Purpose |
| --- | --- | --- |
| Observation | `RelationshipSignal` | One dimension, one direction, one strength; evidence-backed |
| State snapshot | `RelationshipState` | Full multidimensional snapshot; requires approved deltas |
| Proposed change | `RelationshipDeltaCandidate` | Reviewable change proposal referencing signals |

### Signal Extraction Rules

The extractor operates only on boundary-labeled feedback records with known high-confidence patterns. Unknown labels, non-boundary actions, and ambiguous inputs produce **no signals** (under-generation preferred).

| Boundary Label | Dimension(s) | Direction | Strength |
| --- | --- | --- | --- |
| `boundary_violation` | `boundary_risk` | increase | 0.7 |
| `too_intimate` | `boundary_risk` | increase | 0.5 |
| `too_intimate` | `intimacy_level` | decrease | 0.4 |
| `too_eager` | `initiative_allowance` | decrease | 0.5 |

Labels not listed above (`too_cold`, `too_formal`, `too_long`, `good_tone`, `not_like_me`, or any unknown label) produce no signal. Non-boundary actions (`accept`, `reject`, `edit`) also produce no signal.

### RelationshipSignal Fields

#### Required Fields

| Field | Type | Constraint | Description |
| --- | --- | --- | --- |
| `contact_id` | `str` | min_length=1 | Target contact |
| `dimension_name` | `RELATIONSHIP_DIMENSION_NAMES` | enum | Which relationship dimension |
| `strength` | `float` | 0.0–1.0 | How strong the observed signal is |
| `evidence_refs` | `list[str]` | min_length=1 | References to feedback records backing this signal |

#### Optional Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `direction` | `RelationshipDeltaDirection` | `"unknown"` | increase / decrease / stable / unknown |
| `provenance` | `RelationshipSignalProvenance` | `"unknown"` | How this signal was produced |
| `signal_description` | `str or None` | `None` | Brief generic description of the observation |

#### Metadata Fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `signal_id` | `str` | auto-generated | Unique identifier |
| `status` | `DistillationStatus` | `"candidate"` | Review lifecycle status |
| `review_metadata` | `DistilledArtifactReviewMetadata` | default factory | Compatible with existing review pattern |
| `created_at` | `datetime` | utc_now | Creation timestamp |

### Signal Safety Constraints

1. **Evidence-backed**: `evidence_refs` is required with `min_length=1`. A signal without evidence is structurally invalid.
2. **No raw text**: No field stores raw chat transcript, raw feedback text, edited reply text, boundary notes, or user notes.
3. **Dimension-specific**: Each signal targets exactly one dimension. Multi-dimension observations produce separate signals.
4. **Conservative extraction**: Only boundary labels with clear, high-confidence relationship implications produce signals.
5. **Candidate-only by default**: `status` defaults to `"candidate"`. `is_runtime_ready()` returns `False` until human review approves.

## RelationshipDeltaCandidate Generation (T192)

T192 introduces `RelationshipDeltaGenerator` which consumes T191 `RelationshipSignal` records and a current `RelationshipState` to produce reviewable `RelationshipDeltaCandidate` records. No auto-approve, no auto-apply, no state mutation.

### Delta Generation Rules

1. **Contact filtering**: Only signals matching `current_state.contact_id` are considered.
2. **Dimension grouping**: Signals are grouped by `dimension_name`.
3. **Direction consistency**: All signals for a dimension must agree on direction (`increase` or `decrease`). Contradictory or all-unknown/all-stable directions skip the dimension.
4. **Strength aggregation**: The maximum signal strength in each dimension group is used as the effective delta magnitude (attenuated by a scale factor).
5. **Minimum strength**: Dimensions where the maximum signal strength falls below a configurable threshold (default 0.3) are skipped.
6. **Magnitude attenuation**: Signal strength is scaled by a configurable factor (default 0.2) to produce dimension-scale delta values.
7. **Magnitude recomputation**: The final `magnitude` in `RelationshipDeltaDimension` is recomputed as `abs(proposed_value - current_value)`, not copied from signal strength.
8. **Direction validation**: The final `direction` is derived from the actual `proposed_value` vs `current_value` comparison, not blindly trusted from signal direction.
9. **Boundary clamping**: Proposed values are clamped to [0.0, 1.0]. If clamping produces no effective change (magnitude < 1e-6), the dimension is skipped.
10. **Evidence deduplication**: `evidence_refs` from all contributing signals are collected and deduplicated. State evidence refs are not included.
11. **Signal refs**: All contributing `signal_id` values are collected into `signal_refs`.

### Delta Generation Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `_MAGNITUDE_SCALE` | 0.2 | Scale factor from signal strength to dimension-scale delta |
| `_MIN_STRENGTH` | 0.3 | Minimum signal strength required to produce a dimension change |

### Example Delta Generation

Given signals from a `boundary_violation` feedback record:

- Signal A: `boundary_risk`, direction=`increase`, strength=0.7
- Current state: `boundary_risk=0.3`

Result: `RelationshipDeltaDimension` with `current_value=0.3`, `proposed_value=0.44`, `direction=increase`, `magnitude=0.14`.

### Delta Safety Constraints

1. **No auto-approve**: Generated deltas always have `status="candidate"`.
2. **No state mutation**: The `RelationshipState` passed to the generator is never modified.
3. **No raw text**: Delta rationale contains only signal counts and strength values, never raw feedback text.
4. **Evidence-backed**: Delta `evidence_refs` come from signal evidence, not state evidence.
5. **Conservative aggregation**: Weak or ambiguous signal sets produce no delta rather than a speculative one.

## RelationshipDeltaCandidate Review (T193)

T193 introduces `RelationshipDeltaReviewService` which applies explicit human review decisions to `RelationshipDeltaCandidate` records without modifying `RelationshipState` or auto-applying deltas.

### Review Actions

| Decision | Status | Runtime-Ready |
| --- | --- | --- |
| `approve` | `approved` | `True` (if human-reviewed) |
| `reject` | `rejected` | `False` |
| `freeze` | `frozen` | `False` |
| `archive` | `archived` | `False` |

### Review Flow

1. A `RelationshipDeltaCandidate` (generated by T192) is serialized as JSON.
2. The reviewer runs `relationship-review-delta --input <delta.json> --decision <action> --reviewer <name> [--note <text>] [--output <path>]`.
3. The service reads the delta, applies the decision, and writes the updated delta (defaults to overwriting the input file).
4. The delta's `status` and `review_metadata` are updated; `evidence_refs`, `signal_refs`, and `dimension_changes` are preserved unchanged.
5. An approved delta with `reviewed_by_human=True` reports `is_runtime_ready() == True`, but **no state update or auto-apply occurs** in this task.

### Review Safety Constraints

1. **No auto-apply**: Approved deltas do not modify `RelationshipState`.
2. **No state mutation**: The service never reads or writes `RelationshipState`.
3. **No partial approval**: All dimensions in a delta are reviewed together (all-or-nothing).
4. **Content preservation**: Evidence refs, signal refs, dimension changes, and rationale are preserved through review.
5. **Auditable history**: Each review action appends a `DistilledArtifactReviewDecision` to the delta's review history.

### Review Metadata Pattern

The service reuses the existing `DistilledArtifactReviewMetadata` and `DistilledArtifactReviewDecision` patterns from T120/T122/T163. Each review decision appends a history entry recording the status, reviewer identity, timestamp, and optional notes. The `review_metadata.review_state` transitions from `"pending_human_review"` to `"reviewed"` after the first decision.

## Relationship Context (T194)

T194 introduces compact, approval-gated relationship-state guidance into `ChatContext`. The assembler reads approved `RelationshipDeltaCandidate` JSON files from a configured directory, filters for runtime-ready entries, and produces compact `ApprovedRelationshipContext` with dimension-change hints.

### Context Fields Added

| Field | Type | Description |
| --- | --- | --- |
| `ChatContext.relationship_context` | `ApprovedRelationshipContext` | Container for approved relationship guidance |
| `ApprovedRelationshipContext.status` | `ApprovedStoreContextStatus` | `loaded`, `not_configured`, `store_path_missing`, or `no_runtime_ready_records` |
| `ApprovedRelationshipContext.deltas` | `list[ApprovedRelationshipDeltaBrief]` | Compact briefs for each runtime-ready delta |
| `ApprovedRelationshipDeltaBrief.dimension_changes` | `list[str]` | e.g. `"boundary_risk: 0.30->0.44 (increase)"` |
| `ApprovedRelationshipDeltaBrief.delta_summary` | `str` | Compact rationale (max 200 chars) |
| `ApprovedRelationshipDeltaBrief.evidence_refs` | `list[str]` | Limited evidence refs (max 6) |

### Context Safety Constraints

1. **Approval-gated**: Only deltas with `status="approved"` AND `reviewed_by_human=True` AND `last_decision="approved"` enter context.
2. **Contact-filtered**: Only deltas matching the assembled contact's `contact_id` are included.
3. **No raw history**: `signal_refs`, `review_metadata.history`, reviewer identities, and review timestamps are excluded from the compact brief.
4. **Content-bounded**: `delta_summary` is capped at 200 characters; `evidence_refs` at 6 entries.
5. **No state mutation**: The assembler never reads or writes `RelationshipState` records.
6. **Coexistence**: Relationship context is independent from `approved_store_context`, `approved_patch_context`, and `derived_brief_context`.

### Assembler Configuration

The `ChatContextAssembler` accepts an optional `approved_relationship_delta_path` parameter pointing to a directory of `RelationshipDeltaCandidate` JSON files. When omitted, the relationship context stays `not_configured`.

## Relationship to Existing ContactSkillRelationshipState

The existing `ContactSkillRelationshipState` (T111) uses simple string labels and scalar floats (`closeness`, `trust_level`, `confidence`). It remains the compatibility fallback inside `ContactSkillCandidate`. The new `RelationshipState` is a separate, more structured model for the dedicated M8 relationship tracking layer. They are not merged or replaced by this schema.
