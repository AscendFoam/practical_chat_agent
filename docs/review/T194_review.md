# Review: T194

Verdict: PASS_WITH_WARNINGS

## Task Goal

Inject compact, approval-gated relationship-state guidance into `ChatContext` without exposing raw signal history, raw delta review history, or mutating state.

## What Changed

### `src/practical_chat_agent/core/models.py`

Added three models:

- `ApprovedRelationshipDeltaBrief` — compact brief for one runtime-ready delta, carrying formatted dimension-change strings (e.g. `"boundary_risk: 0.30->0.44 (increase)"`), a capped delta summary (max 200 chars), and limited evidence refs (max 6). No `signal_refs`, no `review_metadata`.
- `ApprovedRelationshipContext` — container with `status` (reuses `ApprovedStoreContextStatus`), `source_path`, `contact_id`, `deltas`, and `notes`.
- `ChatContext.relationship_context` — additive field with `default_factory=ApprovedRelationshipContext`, independent from `approved_store_context`, `approved_patch_context`, and `derived_brief_context`.

### `src/practical_chat_agent/services/chat_context.py`

Extended `ChatContextAssembler` with relationship context loading:

- New `__init__` parameter: `approved_relationship_delta_path: Path | None = None` — optional path to a directory of `RelationshipDeltaCandidate` JSON files.
- `_load_approved_relationship_context(contact_id)` — resolves path, scans `*.json` files, validates each as `RelationshipDeltaCandidate`, filters for runtime-ready only.
- `_try_load_runtime_ready_delta(path, contact_id)` — per-file helper: try-parses JSON, checks `contact_id` match and `is_runtime_ready()`, returns `ApprovedRelationshipDeltaBrief` or `None`.
- `_build_relationship_context_notes(context)` — adds relationship delta hints to `memory_retrieval_notes` when loaded.
- `_build_summary()` — includes "Approved relationship guidance" with dimension change hints when context is loaded.
- Filtering: Only deltas with `status="approved"` AND `reviewed_by_human=True` AND `last_decision="approved"` enter context. Candidate, rejected, frozen, archived, not-human-reviewed, and wrong-contact deltas are excluded.

### `tests/test_relationship_context.py` (new)

31 tests covering:

- **Load success** (7 tests): status_loaded, dimension_changes_populated, delta_summary_preserved, evidence_refs_preserved, delta_id_preserved, contact_id_preserved, multi_dimension_delta.
- **Fallback behavior** (8 tests): not_configured (3), store_path_missing (1), no_runtime_ready (5: candidate excluded, empty dir, mixed filtered, wrong contact, not human-reviewed).
- **No raw leakage** (4 tests): no_signal_refs_in_brief, no_review_history_in_context, no_raw_rationale_overflow (capped), evidence_refs_limited (max 6).
- **Coexistence** (2 tests): coexists_with_approved_store, relationship_loaded_others_not_configured.
- **Retrieval notes** (4 tests): notes_present_when_loaded, notes_absent_when_not_configured, delta_hint_in_notes, notes_absent_when_no_runtime_ready.
- **Summary** (3 tests): summary_includes_relationship_guidance, summary_excludes_when_not_loaded, summary_excludes_when_no_runtime_ready.
- **Determinism** (2 tests): same_result_twice, no_disk_writes.

### `docs/data_contracts/relationship_state_contract.md`

- Updated date to "Updated: 2026-05-24 (T192, T193, T194)".
- Updated scope description to include T194.
- Updated lifecycle diagram: "compact context integration (T194)" from future to current.
- Added "Relationship Context (T194)" section documenting context fields, safety constraints, assembler configuration.

### `docs/07_handoff.md`

Added T194 Worker Completion Record documenting models added, assembler logic, context design, verification results, and explicit non-actions.

### `.claude/settings.json`

Workspace-artifact permission entries added (consistent with all prior tasks).

## Verification

1. Compile check: `python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/chat_context.py` — passed.
2. T194 test suite: 31 tests passed, 0 failures.
3. Full existing test suite: 541 tests passed (31 new + 510 existing), 0 regressions.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: `.claude/settings.json` workspace-artifact overrun

Permission entries for T194 verification commands were added. This is consistent with every prior task (T193 N04, T192 N03, etc.).

### N02: No test for unparseable JSON in delta directory

`_try_load_runtime_ready_delta` catches all exceptions (`except Exception: return None`) when reading or parsing delta JSON files. This is correct defensive behavior, but no test confirms that a non-delta JSON file (or entirely invalid JSON) in the directory is silently skipped rather than raising an error. The existing `test_empty_directory` covers the empty-directory case, and `test_mixed_candidate_and_approved_filtered` covers valid JSON filtering, but the invalid-JSON skip path is untested.

## Missing Tests

### M01: Summary truncation edge case not directly tested

The `_build_summary` method truncates dimension changes when they exceed 200 characters (`if len(dim_changes) > 200: dim_changes = f"{dim_changes[:197].rstrip()}..."`). This edge case is not directly tested. The practical trigger (sufficiently many long dimension names) is unlikely given the standard formatting (~40 chars per dimension), so this is a low-risk gap.

### M02: Path-is-directory check not tested

The code checks `resolved.is_dir()` and returns `status="store_path_missing"` with note "Relationship delta path must be a directory." when the path exists but points to a file. The existing test `test_status_store_path_missing` only tests a non-existent path. This is a very narrow edge case, but it is an uncovered branch.

### M03: No test for empty `delta_rationale` input

If a `RelationshipDeltaCandidate` has an empty `delta_rationale`, `_compact_text` would produce an empty string, and the `ApprovedRelationshipDeltaBrief.delta_summary` (which has `max_length=200`) would accept it. This is correct behavior — empty rationale → empty summary — but it's not explicitly tested.

## Suspicious Implementation Details

### S01: `_build_relationship_context_notes` fallback returns `list(context.notes)`

When `status != "loaded"`, `_build_relationship_context_notes` returns `list(context.notes)`, which can contain diagnostic messages like "Configured relationship delta path does not exist." or "No delta JSON files found in relationship delta path." This is identical to the pattern used by `_build_approved_store_notes` (T123) and `_build_approved_patch_notes` (T164), so it's a project-wide convention rather than a T194-specific concern. The diagnostic messages are implementation details that end up in `memory_retrieval_notes`.

### S02: `ApprovedStoreContextStatus` reused for relationship context

`ApprovedRelationshipContext` uses `ApprovedStoreContextStatus` (from T123) rather than a dedicated status enum. The values (`not_configured`, `store_path_missing`, `no_runtime_ready_records`, `loaded`) are semantically appropriate, but this introduces a cross-domain coupling between the approved-store and relationship-context domains.

### S03: No `AppContainer` wiring

As documented in the worker summary, `approved_relationship_delta_path` is not wired into `AppContainer` (unlike `approved_store_path` and `approved_patch_path`). This is outside the allowed files and task scope, but it means the relationship context is only configurable programmatically, not through environment variables. This is acceptable for the current scope.

## Scope Compliance

- Allowed files check:
  - `src/practical_chat_agent/core/models.py`: Changed. Within allowed scope.
  - `src/practical_chat_agent/services/chat_context.py`: Changed. Within allowed scope.
  - `tests/test_relationship_context.py`: New file. Within allowed scope.
  - `docs/data_contracts/relationship_state_contract.md`: Changed. Within allowed scope.
  - `docs/07_handoff.md`: Changed. Within allowed scope.
  - `.claude/settings.json`: Changed. Consistent workspace-artifact pattern.

- Forbidden scope compliance:
  - No raw signal history injected. Verified.
  - No `RelationshipState` auto-update. Verified.
  - No send-behavior change. Verified.
  - No delta review semantics reopened. Verified.
  - No ContactSkill, MemoryFact, or approved store modification. Verified.

## Recommended Next Action

T194 is complete and passes the review gate. It correctly provides compact, approval-gated relationship-state guidance to `ChatContext` without exposing raw signal history, raw review history, or mutating state. The next M8 task is:

1. **T195: Relationship-aware reply eval** — evaluate how the relationship context integrates with the reply planner.

Key deferred concerns to carry forward:

- T194's `approved_relationship_delta_path` is not wired into runtime configuration (AppContainer); this is acceptable for current scope but should be addressed before production use.
- T194 reads individual delta JSON files from a directory without a store-file abstraction; this is acceptable since T193 produces individual JSON files, but may need revisiting if delta volume grows.
- The empty `_build_relationship_context_notes` / diagnostic-into-retrieval pattern (S01) is a project-wide convention, not T194-specific, but should be noted for eventual cleanup.
