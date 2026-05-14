# T121 Review: Evidence Validator

## Reviewer

Claude Code (adversarial review)

## Verdict

**PASS_WITH_WARNINGS**

## Scope Check

Worker modified exactly the 3 allowed files:

- `src/practical_chat_agent/services/evidence_validation.py` (new file)
- `src/practical_chat_agent/app/main.py` (new CLI command only)
- `docs/07_handoff.md` (status update, T120 completion record, T121 worker draft, section renumbering)

No other tracked files were modified beyond allowed scope. No changes to `core/models.py`. No changes to upstream services. The new file is untracked and within allowed scope.

## What was done

1. **New `EvidenceValidationService`** (~785 lines):
   - Loads memory/contact-skill store records via T120's `ContactSkillFileStoreService`.
   - Builds an evidence ID index from same-run artifacts: `normalized_events.jsonl`, `chunks.jsonl`, `chunk_summaries.jsonl`, `memory_facts.jsonl`, `contact_skill.candidate.json`, plus the store records themselves.
   - Recursively walks the serialized model payload (`model_dump(mode="json")`) to find all `evidence_refs` keys at every nesting level.
   - Validates every store record's refs against the index.
   - Enforces status rules:
     - `candidate`: blocked from approval and runtime by default.
     - `approved` with missing refs: blocked from approval and runtime.
     - `rejected` / `frozen` / `archived`: blocked from approval and runtime.
     - `approved` without missing refs but without human review: runtime blocked (but approval-ready).
   - Runtime readiness also depends on T120's `is_runtime_ready()` gate.
   - Does NOT write back to store metadata. Reports only.

2. **New CLI command** `chatlog-validate-evidence`:
   - `--input`, `--output`, `--dry-run`.
   - Output defaults to `private/distilled/<run_id>/evidence_validation_report.json`.
   - Stdout prints only counts and safe relative paths.

3. **Handoff updates**: T120 completion record, T121 worker draft with verification results.

## Positives

- **Status rules are correct and complete**:
  - `candidate` → blocked by default (correct).
  - `approved` + missing refs → blocked (correct).
  - `rejected`/`frozen`/`archived` → never runtime-ready (correct).
  - `approved` + refs OK + human-reviewed → both approval- and runtime-ready (correct).
  - `approved` + refs OK + NOT human-reviewed → approval-ready but runtime-blocked (correct — distinguishes evidence validity from human review gate).
- **Nested evidence_refs collection** (`_collect_evidence_ref_locations`) is thorough — it recursively walks the entire serialized model dict, finding `evidence_refs` at every nesting level (top-level, `relationship_state`, `communication_style`, each topic/preference/pattern, etc.). This correctly handles the deeply nested `ContactSkillCandidate` structure.
- **Evidence index is comprehensive**: indexes IDs from normalized events, chunks, chunk summaries, memory facts, contact skill candidate, plus the store records themselves.
- **BOM handling**: `_load_jsonl_objects` strips UTF-8 BOM on first line, handling PowerShell-created fixtures.
- **No auto-approve**: validator only reports, never mutates store records.
- **No runtime integration**: does not inject into `ChatContext`, does not call `ChatContextAssembler`.
- **No LLM calls**: purely structural existence checks.
- **Path confinement**: `_ensure_within_root` on both input and output.
- **Report provenance**: each record result includes provenance snapshot and review metadata snapshot.
- **No private data leakage**: stdout is limited to counts and relative paths. Report written only to `private/distilled/`.

## Blocking Issues

None.

## Non-blocking Issues

### N01: `_extract_contact_skill_ids` always returns empty list for current schema

**Severity**: Low
**Location**: `evidence_validation.py` lines 714-719
**Detail**: The method looks for `contact_skill_id`, `skill_id`, and `candidate_id` fields, but `ContactSkillCandidate` has none of these — it only has `contact_id`. The method will always return an empty list for current data. The fallback at line 159 (`record.contact_skill.contact_id`) is used instead, which is functionally correct. However, this means:
- The `"contact_skill_ids"` count in the evidence index will always be 0.
- No contact skill artifact IDs are indexed for cross-referencing.
- The method is effectively dead code for the current schema.

The worker acknowledged this in the handoff: "contact_skill.candidate.json has no dedicated stable skill artifact id today."

**Recommendation**: Acceptable for MVP. If a stable skill artifact ID is added later, the method can be updated. Alternatively, `contact_id` could be used as a fallback index key if cross-referencing skills is desired.

### N02: JSONL/JSON loading code is the third copy

**Severity**: Low
**Location**: `evidence_validation.py` `_load_jsonl_objects`, `_read_json_object`, `_write_json`
**Detail**: This is now the third service class with nearly identical JSONL/JSON loading helpers (after `ContactSkillBuilderService` and `ContactSkillFileStoreService`). The BOM handling is a minor improvement over the earlier copies, but it has not been backported.

**Recommendation**: Acceptable for MVP. T150 or a future refactor task could extract shared file I/O utilities.

### N03: `_collect_evidence_ref_locations` recurses through entire serialized payload

**Severity**: Negligible
**Location**: `evidence_validation.py` lines 665-692
**Detail**: The method walks the entire `model_dump()` output to find all `evidence_refs` keys. For a `ContactSkillCandidate` with many nested topics, patterns, and events, this means traversing a large dict tree. Performance is not a concern for current data volumes, but it is worth noting that this is O(total dict nodes) rather than O(evidence_refs).

**Recommendation**: No action needed for MVP.

### N04: `approval_ready` and `runtime_ready` are locally computed, not persisted

**Severity**: Informational
**Location**: `evidence_validation.py` lines 215-216
**Detail**: The validator computes `approval_ready_after_validation` and `runtime_ready_after_validation` as report fields, but does not write these back to the store records. This is by design — the worker explicitly noted: "Validator currently reports outcomes only; it does not write back `review_metadata.evidence_validation_status`." This keeps the validator read-only and leaves status transitions for T122's review CLI.

**Recommendation**: Correct design choice. T122 should use the validation report as input when deciding whether to allow approval.

### N05: No committed automated tests

**Severity**: Deferred (per project convention)
**Location**: N/A
**Detail**: Verification was done against `private/distilled/t102_smoke` (good case) and a private synthetic fixture (bad case), not committed unit tests. Consistent with project convention of deferring tests to T150.

**Recommendation**: T150 should include tests for: evidence index building, nested `evidence_refs` collection, status rule enforcement (candidate/approved/rejected/frozen/archived), missing refs blocking approval/runtime, human review gate interaction, and path confinement.

## Forbidden Scope Check

| Forbidden action | Status |
|---|---|
| Auto-approve | NOT present. Validator is read-only. |
| Approve/reject/freeze CLI | NOT present. T122's job. |
| Rewrite claims/summaries | NOT present. |
| DB migration | NOT present. |
| Vector DB | NOT present. |
| Runtime prompt injection | NOT present. |
| LLM call | NOT present. Pure structural checks. |
| Read `private/chat_history/` | NOT present. Only reads `private/distilled/`. |
| Private data in docs/stdout | NOT present. Counts and paths only. |

## Verification

- Compile: passed.
- Good case (`t102_smoke`): `evidence_validation_status = passed`, 0 missing refs, all 8 records blocked (all candidate). Correct.
- Bad case (synthetic fixture): `evidence_validation_status = failed`, 1 approved record with missing ref blocked from both approval and runtime. Correct.
- Store-only fixture (`t120_store_smoke/store`): `evidence_validation_status = failed`, 5 missing refs. Correct — store without same-run evidence artifacts is evidence-incomplete.

## Warnings Classification

| ID | Classification | Rationale |
|---|---|---|
| N01 | Accepted | `_extract_contact_skill_ids` returns empty for current schema; fallback to `contact_id` works. No correctness issue. |
| N02 | Accepted/Deferred | Third copy of JSONL helpers; acceptable for MVP, refactor when pattern repeats further. |
| N03 | Accepted | Performance not a concern for current data volumes. |
| N04 | Accepted | Read-only validator is correct design; T122 handles mutations. |
| N05 | Deferred | Automated tests scheduled for T150 per project convention. |

## Recommended Next Action

Proceed to T122. During T122 implementation, pay attention to:

1. Whether T122's review CLI should require a passed evidence validation report before allowing approval. The current validator is read-only, so T122 will need to read the validation report and enforce the gate.
2. Whether `_extract_contact_skill_ids` (N01) should be updated if a stable skill artifact ID is introduced.
3. Whether the BOM handling improvement should be backported to `ContactSkillBuilderService` and `ContactSkillFileStoreService` to avoid inconsistencies.
4. Whether T122 should write back `review_metadata.evidence_validation_status` based on the validator output, or leave that for a separate concern.
