# RelationshipState Contract

Updated: 2026-05-24

## Purpose

`RelationshipState` represents a conservative, multidimensional snapshot of the relationship between the user and a specific contact. It is **review-only** and **candidate-only** by default: no automatic state mutation, no automatic action, and no collapse into a single scalar score.

`RelationshipDeltaCandidate` represents a proposed change to one or more dimensions of a `RelationshipState`, backed by evidence and requiring explicit human review before any state update.

## Scope

This contract covers T190 (schema definition) only. Later M8 tasks handle signal extraction (T191), delta generation (T192), review CLI (T193), compact context integration (T194), and relationship-aware eval (T195). This contract must remain stable across those tasks without schema breakage.

## Review-Only Lifecycle

```text
approved ContactSkill / feedback / memory evidence
  -> relationship signal extraction (T191, future)
  -> RelationshipDeltaCandidate (status=candidate)
  -> human review CLI (T193, future)
  -> approved / rejected / frozen / archived
  -> RelationshipState update (only after approved delta)
  -> compact context integration (T194, future)
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
- T194 (compact context) reads only `status="approved"` states where `is_runtime_ready() == True`, producing a compact brief for `ChatContext` without exposing full dimension values.
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

## Relationship to Existing ContactSkillRelationshipState

The existing `ContactSkillRelationshipState` (T111) uses simple string labels and scalar floats (`closeness`, `trust_level`, `confidence`). It remains the compatibility fallback inside `ContactSkillCandidate`. The new `RelationshipState` is a separate, more structured model for the dedicated M8 relationship tracking layer. They are not merged or replaced by this schema.
