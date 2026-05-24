# T191 Worker Summary

## Task

T191: Relationship Signal Extractor — extract conservative, evidence-backed relationship signals from approved feedback so later M8 tasks can propose reviewable state deltas without reading raw chat history.

## What Changed

### `src/practical_chat_agent/core/models.py`

Added 1 new Literal type and 1 new Pydantic model:

- `RelationshipSignalProvenance` = Literal["feedback_boundary", "feedback_action", "metadata_derived", "unknown"]
- `RelationshipSignal` — conservative, evidence-backed relationship observation with dimension_name, direction, strength, evidence_refs, provenance, signal_description, and review lifecycle. Includes `is_runtime_ready()` gate. `evidence_refs` requires `min_length=1`. `status` defaults to `"candidate"`.

### `src/practical_chat_agent/services/feedback.py`

Added `RelationshipSignalExtractor` class with `extract_from_feedback()` method. The extractor:

- Operates only on boundary-labeled feedback records with known high-confidence patterns.
- Maps `boundary_violation` → boundary_risk increase (0.7), `too_intimate` → boundary_risk increase (0.5) + intimacy_level decrease (0.4), `too_eager` → initiative_allowance decrease (0.5).
- Skips all non-boundary actions (accept, reject, edit), unlabeled boundary feedback, and unknown boundary labels.
- Optionally filters to a set of valid_record_ids.
- Stores no raw text (no boundary_note, user_note, edited_text, or draft_text in signals).
- Added `RelationshipSignal` and `RelationshipDeltaDirection` to imports.

### `tests/test_relationship_signals.py` (new)

21 committed tests covering:

- Clear boundary pattern extraction (boundary_violation, too_intimate, too_eager).
- No-signal behavior for accept, reject, edit, unlabeled boundary, unknown labels, empty logs.
- Evidence-ref preservation.
- valid_record_ids filtering.
- No raw private text in produced signals.
- Multi-contact support.
- RelationshipSignal model validation (valid signal, empty evidence_refs rejection, invalid dimension rejection, out-of-range strength rejection, negative strength rejection, default candidate status, default unknown direction).

### `docs/data_contracts/relationship_state_contract.md`

Added "RelationshipSignal (T191)" section documenting:

- How signals differ from state and delta layers.
- Extraction rules table (boundary label → dimensions, directions, strengths).
- Signal field tables (required, optional, metadata).
- Signal safety constraints (evidence-backed, no raw text, dimension-specific, conservative extraction, candidate-only default).
- Updated T191 compatibility note to describe signal_id referencing.

### `docs/07_handoff.md`

Added T191 Worker Completion Record documenting what changed, extraction design, relationship to T190, verification results, and explicit non-actions.

## Verification

1. Compile check passed: `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/feedback.py`
2. T191 test suite: 21 tests passed, 0 failures.
3. Full existing test suite: 462 tests passed (21 new + 441 existing), 0 failures, no regression.

## Remaining Risks

- The extractor covers only boundary-labeled feedback. Accept/reject/edit actions produce no signals. This is intentionally conservative but means many feedback records will not generate relationship signals.
- Strength values (0.4–0.7) are heuristic defaults, not calibrated against real data. T192 should decide how to aggregate multiple signals and whether to weight them.
- The `metadata_derived` provenance type is defined but not yet used. Future tasks could extract signals from approved ContactSkill or MemoryFact metadata, but this is out of scope for T191.
- Only 3 of 8 relationship dimensions are reachable through current extraction rules. Familiarity, trust, warmth, reciprocity, and conflict_level have no extraction rules yet. This is by design (no clear mapping from boundary labels), but means signals will be sparse for these dimensions.
