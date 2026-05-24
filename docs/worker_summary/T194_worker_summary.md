# T194 Worker Summary

## Task

T194: RelationshipState Compact Context — inject compact, approval-gated relationship-state guidance into `ChatContext` without exposing raw signal history, raw delta review history, or mutating state.

## What Changed

### `src/practical_chat_agent/core/models.py`

Added models for compact relationship context:

- `ApprovedRelationshipDeltaBrief` — compact brief for one runtime-ready delta, carrying only dimension changes (formatted strings like `"boundary_risk: 0.30->0.44 (increase)"`), a capped delta summary (max 200 chars), and limited evidence refs (max 6). No `signal_refs`, no `review_metadata`, no raw review history.
- `ApprovedRelationshipContext` — container with `status` (uses `ApprovedStoreContextStatus`), `source_path`, `contact_id`, `deltas`, and `notes`. Reflects `not_configured`, `store_path_missing`, `no_runtime_ready_records`, or `loaded`.
- `ChatContext.relationship_context` — additive field with `default_factory=ApprovedRelationshipContext`, independent from `approved_store_context`, `approved_patch_context`, and `derived_brief_context`.

### `src/practical_chat_agent/services/chat_context.py`

Extended `ChatContextAssembler` with relationship context loading:

- **New `__init__` parameter**: `approved_relationship_delta_path: Path | None = None` — optional path to a directory of `RelationshipDeltaCandidate` JSON files.
- **`_load_approved_relationship_context(contact_id)`**: resolves path, scans `*.json` files, validates each as `RelationshipDeltaCandidate`, filters for runtime-ready only.
- **`_try_load_runtime_ready_delta(path, contact_id)`**: per-file helper — try-parses JSON, checks `contact_id` match and `is_runtime_ready()`, returns `ApprovedRelationshipDeltaBrief` or `None`.
- **`_build_relationship_context_notes(context)`**: adds relationship delta hints to `memory_retrieval_notes` when loaded.
- **`_build_summary()`**: includes "Approved relationship guidance" with dimension change hints when context is loaded.
- **Filtering**: Only deltas with `status="approved"` AND `reviewed_by_human=True` AND `last_decision="approved"` enter context. Candidate, rejected, frozen, archived, not-human-reviewed, and wrong-contact deltas are excluded.

### `tests/test_relationship_context.py` (new)

31 tests covering:

- **Load success**: status_loaded, dimension_changes_populated, delta_summary_preserved, evidence_refs_preserved, delta_id_preserved, contact_id_preserved, multi_dimension_delta.
- **Fallback behavior**: not_configured, store_path_missing, candidate_delta_not_loaded, empty_directory, mixed_candidate_and_approved_filtered, approved_other_contact_not_loaded, approved_not_human_reviewed.
- **No raw content leakage**: no_signal_refs_in_brief, no_review_history_in_context, no_raw_rationale_overflow (summary capped), evidence_refs_limited (max 6).
- **Coexistence**: coexists_with_approved_store, relationship_loaded_others_not_configured.
- **Retrieval notes**: notes_present_when_loaded, notes_absent_when_not_configured, delta_hint_in_notes, notes_absent_when_no_runtime_ready.
- **Summary**: summary_includes_relationship_guidance, summary_excludes_when_not_loaded, summary_excludes_when_no_runtime_ready.
- **Determinism**: same_result_twice, no_disk_writes.

### `docs/data_contracts/relationship_state_contract.md`

- Updated date to "Updated: 2026-05-24 (T192, T193, T194)".
- Updated scope description to include T194.
- Updated lifecycle diagram: "compact context integration (T194)" (was "T194, future").
- Added "Relationship Context (T194)" section documenting context fields, safety constraints, and assembler configuration.
- Updated M8 compatibility table for T194.

### `docs/07_handoff.md`

Added T194 Worker Completion Record documenting what changed, models added, assembler logic, context design, verification results, and explicit non-actions.

## Verification

1. Compile check passed: `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/chat_context.py`
2. T194 test suite: 31 tests passed, 0 failures.
3. Full existing test suite: 541 tests passed (31 new + 510 existing), 0 failures, no regression.

## Remaining Risks

- The relationship context reads individual delta JSON files from a directory. There is no store-file abstraction (unlike `ContactSkillStoreFile`/`MemoryFactStoreFile`). This is acceptable for the current scope since approved deltas are produced as individual JSON files by T193.
- State application (approved delta -> `RelationshipState` update) remains deferred. T194 reads approved deltas directly and does not apply them to any stored state.
- The `approved_relationship_delta_path` parameter is not wired into `AppContainer` (unlike `approved_store_path` and `approved_patch_path`). Wiring can be added when a runtime configuration path for relationship deltas is needed.
