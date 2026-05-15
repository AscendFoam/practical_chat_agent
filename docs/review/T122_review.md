# T122 Review: Skill Review CLI

## Reviewer

Claude Code (adversarial review)

## Verdict

**PASS_WITH_WARNINGS**

## Scope Check

Worker modified exactly the 4 allowed files:

- `src/practical_chat_agent/app/main.py` (new `chatlog-review-store` CLI command + `_safe_cli_path` helper)
- `src/practical_chat_agent/services/contact_skill.py` (new `ContactSkillStoreReviewService`, dataclasses, stable record_id, store normalization fix)
- `src/practical_chat_agent/exporters/contact_skill_markdown.py` (new `render_store_review_markdown` + helpers)
- `docs/07_handoff.md` (T122 worker draft section, section renumbering)

No other tracked files were modified beyond allowed scope. No changes to `core/models.py`. No changes to upstream services outside allowed files. No new dependencies.

## What was done

1. **New `ContactSkillStoreReviewService`** (~530 lines in `contact_skill.py`):
   - `list_store_records()`: loads workspace (memory store + contact skill store), optional T121 validation report, builds per-record `StoreRecordSummary` with gate info.
   - `apply_record_decision()`: enforces human reviewer required, normalizes decision, loads validation report (required for approve), finds target record, asserts approval gate, applies decision, writes back, saves.
   - `export_review_artifact()`: lists records, filters optional `record_id`, renders safe markdown to `private/distilled/**`.
   - Approval gate (`_assert_approval_allowed`): requires report present, report status `passed`, target record present in report, 0 missing refs, >0 checked refs, target status not `rejected`/`frozen`/`archived`.
   - `_update_review_metadata()`: sets `review_state="reviewed"`, `reviewed_by_human=True`, `last_decision`, `last_reviewed_at`, reviewer fields, `evidence_validation_status`, appends notes and `DistilledArtifactReviewDecision` to history.
   - `_update_candidate_status()`: recursively walks serialized dict to update all `status` fields to the new decision status.
   - Path confinement: all inputs and outputs enforced within `private/distilled/`.

2. **New CLI command** `chatlog-review-store`:
   - Options: `--input`, `--action` (list/approve/reject/freeze/archive/export), `--record-id`, `--reviewer-id`, `--reviewer-name`, `--note` (repeatable), `--validation-report`, `--output`.
   - Stdout prints only safe JSON: record ids, status fields, counts, and relative private paths.
   - Errors surface as `typer.BadParameter` from `ContactSkillStoreReviewError`.

3. **New `render_store_review_markdown`** in exporter:
   - Safe markdown summary with record ids, statuses, gate values, block reasons.
   - No raw chat content, no private data.

4. **Stable `record_id` for legacy-wrapped records**:
   - `_stable_store_record_id()` using SHA-1 hash truncated to 16 hex chars, with prefix (`memstore_`/`skillstore_`).
   - Applied in `ContactSkillFileStoreService._wrap_memory_facts_to_store_records` and `_wrap_contact_skill_candidate_to_store_record`.

5. **Store normalization fix**:
   - `generated_at` now preserved during `normalize_memory_store` and `normalize_contact_skill_store`.

6. **Handoff update**: T122 worker draft with full verification details.

## Positives

- **Approval gate is thorough and correct**:
  - Requires T121 `evidence_validation_report.json` (auto-discovered from run dir or explicit `--validation-report`).
  - Requires report-level `evidence_validation_status = "passed"`.
  - Requires target record present in report (no silent skip).
  - Requires 0 missing refs on target.
  - Requires >0 checked refs (catches records with no evidence at all).
  - Blocks `rejected`/`frozen`/`archived` from re-approval.
  - All blocks raise clear error messages explaining why.

- **Review metadata is complete**:
  - `reviewed_by_human=True` always set on any decision.
  - `last_decision`, `last_reviewed_at`, `last_reviewer_id`, `last_reviewer_name` all updated.
  - `evidence_validation_status` resolved from validation report and written back.
  - `DistilledArtifactReviewDecision` appended to `history` with all fields.
  - `decision_notes` appended, not replaced.

- **No auto-approve / no bulk default**: every decision requires explicit action + record-id + reviewer.

- **Rejected/frozen/archived never become runtime-ready**: `_build_gate_summary` hardcodes block reasons for these statuses.

- **Export is safe**: `_resolve_markdown_output_path` enforces `_ensure_within_root` against `_private_distilled_root`. Markdown contains only metadata.

- **Path confinement**: `_load_workspace` resolves and validates paths. `_resolve_markdown_output_path` validates export output.

- **`_update_candidate_status` recursion handles nested status fields**: correctly updates `status` at all nesting levels in the serialized payload, so deeply nested sub-objects (relationship_state, communication_style, etc.) also get updated.

- **Validation report run_dir cross-check**: prevents accidental use of a report from a different run directory.

- **Stable record_id**: deterministic SHA-1-derived IDs mean T121 report record_ids and T122 CLI targets stay aligned across reloads.

## Blocking Issues

None.

## Non-blocking Issues

### N01: `_resolve_evidence_validation_status` deletes `current_status` parameter

**Severity**: Low
**Location**: `contact_skill.py` line 1971
**Detail**: The method accepts `current_status: DistillationStatus` but immediately does `del current_status`. This is a code smell — the parameter is part of the public interface (called from `_build_record_summary` and `apply_record_decision`) but is unused. The `del` statement is used to avoid "unused parameter" linter warnings, but it makes the interface misleading.

**Recommendation**: Acceptable for MVP. If `current_status` becomes useful later (e.g., for status-aware validation resolution), the parameter is already there. Alternatively, it could be removed in a cleanup pass.

### N02: `_update_candidate_status` recurses through entire serialized payload to change all `status` keys

**Severity**: Low
**Location**: `contact_skill.py` lines 1986-2004
**Detail**: The method walks the entire `model_dump(mode="json")` output and changes every string value under a key named `"status"` that matches one of the 5 valid statuses. This means:
- It changes `status` at all nesting levels, which is intentional (deeply nested sub-objects should match the parent).
- It could theoretically change a `status` field in a sub-object that should NOT change (e.g., if a future model adds a `status` field with different semantics). However, for the current `MemoryFactCandidate` and `ContactSkillCandidate` schemas, this is correct — all nested `status` fields inherit the parent's status.
- The alternative would be to explicitly set known status fields, but that would require knowing the schema structure at every level, which is fragile in a different way.

**Recommendation**: Acceptable for current schemas. If future model changes add `status` fields with different semantics, this method must be revisited.

### N03: `store_runtime_ready` variable is computed but only used in one branch

**Severity**: Negligible
**Location**: `contact_skill.py` line 1688
**Detail**: `store_runtime_ready = record.is_runtime_ready()` is computed at the top of `_build_gate_summary` but is only used in the `elif status == "approved"` branch at line 1710. This is not a bug — the value is correct when it's used. But it's a minor style note that the variable is computed even for non-approved records.

**Recommendation**: No action needed.

### N04: `_load_workspace` accesses private methods of `ContactSkillFileStoreService`

**Severity**: Low
**Location**: `contact_skill.py` lines 1482-1486, 1547, 1571-1572, etc.
**Detail**: `ContactSkillStoreReviewService` accesses `self._store_service._resolve_existing_path`, `_ensure_within_root`, `_safe_relative_path`, `_read_json_object`, and other private methods. This creates a tight coupling between the review service and the file store service's internals. If the file store service refactors its private API, the review service breaks.

**Recommendation**: Acceptable for MVP. A future refactor could expose a public API for path resolution and validation on the store service, or extract shared utilities.

### N05: `_StoreWorkspace` is a mutable dataclass but used as quasi-immutable state

**Severity**: Negligible
**Location**: `contact_skill.py` lines 508-517
**Detail**: `_StoreWorkspace` is a `@dataclass` (mutable) and is mutated in `_write_back_record` (lines 1840-1848). This works correctly, but mixing mutable workspace state with frozen result dataclasses could be confusing. The alternative would be to return a new workspace copy.

**Recommendation**: No action for MVP. The mutation is localized and controlled.

### N06: No committed automated tests

**Severity**: Deferred (per project convention)
**Location**: N/A
**Detail**: Verification was done against private synthetic fixtures (`t122_pass_fixture`, `t122_reject_fixture`, `t122_freeze_fixture`, `t121_missing_ref_fixture`, `t120_store_smoke`), not committed unit tests. Consistent with project convention of deferring tests to T150.

**Recommendation**: T150 should include tests for: approval gate enforcement (report required, passed, no missing refs, checked refs >0, status not rejected/frozen/archived), reject/freeze/archive flow, review metadata history, `_update_candidate_status` recursion, export path confinement, stable record_id determinism, and no-auto-approve guarantee.

## Forbidden Scope Check

| Forbidden action | Status |
|---|---|
| Auto-approve / bulk default approve | NOT present. Every decision is explicit. |
| Bypass T121 evidence validation | NOT present. Approve requires report + passed + 0 missing refs. |
| Runtime integration / ChatContext | NOT present. |
| DB migration | NOT present. |
| Vector DB | NOT present. |
| LLM call | NOT present. |
| Auto-send / realtime platform | NOT present. |
| Read `private/chat_history/` | NOT present. Only reads `private/distilled/`. |
| Private data in docs/stdout | NOT present. Safe ids, counts, paths only. |
| Reopen rejected/frozen/archived | NOT present. Explicitly blocked with error message. |

## Verification Assessment

- **Compile**: passed (3 files).
- **Happy path approve**: fixture `t122_pass_fixture`, evidence validation `passed`, CLI approve → status updated to `approved`, `reviewed_by_human=True`, `last_decision=approved`, reviewer fields set, history appended, `evidence_validation_status=passed`. Correct.
- **Missing-ref block**: fixture `t121_missing_ref_fixture`, approve → blocked with clear error message. Fixture file unchanged. Correct.
- **Reject path**: fixture `t122_reject_fixture`, status set to `rejected`, history appended, runtime-ready remained false. Correct.
- **Freeze path**: fixture `t122_freeze_fixture`, status set to `frozen`, history appended, runtime-ready remained false. Correct.
- **Export path**: output written only under `private/distilled/**`, markdown contains only safe metadata. Correct.
- **List**: stdout only safe ids, status fields, counts, relative paths. Correct.

Verification covers all 5 required scenarios from T122 task package (good approval, missing-ref block, reject, freeze, export).

## Warnings Classification

| ID | Classification | Rationale |
|---|---|---|
| N01 | Accepted | `del current_status` is a linter-workaround; no correctness issue. |
| N02 | Accepted | Recursive status update is correct for current schemas; future-proof note recorded. |
| N03 | Accepted | Minor style note; no correctness or performance impact. |
| N04 | Accepted/Deferred | Private method access is coupling; acceptable for MVP, refactor when shared utilities extracted. |
| N05 | Accepted | Mutable workspace works correctly for current usage. |
| N06 | Deferred | Automated tests scheduled for T150 per project convention. |

## Recommended Next Action

Proceed to T123 (context integration). During T123, pay attention to:

1. T123 will read approved + runtime-ready records from the store. Verify it checks `is_runtime_ready()` and does not load `rejected`/`frozen`/`archived`/`candidate` records.
2. Whether `_update_candidate_status` (N02) needs adjustment if future models add `status` fields with different semantics.
3. Whether the review service's private method coupling (N04) should be cleaned up before T123 adds more consumers.
4. Whether T150 should test the full approval gate lifecycle: validate → approve → re-validate approved record.
