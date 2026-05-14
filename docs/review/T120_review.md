# T120 Review: File Store Models

## Reviewer

Claude Code (adversarial review)

## Verdict

**PASS_WITH_WARNINGS**

## Scope Check

Worker modified exactly the 3 allowed files:

- `src/practical_chat_agent/core/models.py` (new models and helpers)
- `src/practical_chat_agent/services/contact_skill.py` (new `ContactSkillFileStoreService`)
- `docs/07_handoff.md` (status update, new section 12, section renumbering)

No other tracked files were modified. No CLI additions (T122's job). No DB migration. No vector DB. No `app/main.py` changes. Upstream services (`chatlog_ingestion.py`, `conversation_chunking.py`, `chatlog_distillation.py`, `exporters/contact_skill_markdown.py`) are untouched.

## What was done

1. **New store record models** in `core.models`:
   - `MemoryFactStoreRecord` / `MemoryFactStoreFile`: wraps each `MemoryFactCandidate` with source metadata, review metadata, record ID, and timestamps.
   - `ContactSkillStoreRecord` / `ContactSkillStoreFile`: wraps each `ContactSkillCandidate` with the same provenance and review envelope.
   - `DistilledArtifactReviewDecision`: single review decision with reviewer, status, notes, evidence validation status.
   - `DistilledArtifactReviewMetadata`: tracks review state, human review flag, last decision, decision history.
   - `DistilledArtifactSourceMetadata`: tracks `source_run_id`, artifact paths, source chunk/memory/event IDs.
   - `ContactSkillRedactionPolicy`: replaces the previous `dict[str, Any]` with a typed Pydantic model.

2. **New type literals**: `DistillationReviewState`, `DistillationEvidenceValidationStatus`.

3. **`MemoryFactCandidate` helpers**: `to_runtime_memory_type()` maps `DistillationMemoryType` to runtime `MemoryType`; `to_memory_fact()` constructs a runtime `MemoryFact` from the candidate. Neither is wired into runtime — just mapping utilities for T121/T123.

4. **`ContactSkillFileStoreService`** in `contact_skill.py`:
   - `load_memory_store()` / `load_contact_skill_store()`: can load from either the new store JSON format or from legacy T112/T113 outputs (`memory_facts.jsonl`, `contact_skill.candidate.json`).
   - `save_memory_store()` / `save_contact_skill_store()`: writes to store JSON under `private/distilled/`.
   - Legacy artifacts are wrapped into store records with conservative default review metadata.
   - All I/O paths enforce `private/distilled/` confinement via `_ensure_within_root()`.

5. **`is_runtime_ready()` gate**: Both `DistilledArtifactReviewMetadata.is_runtime_ready()` and record-level `is_runtime_ready()` require `status == "approved"` AND `reviewed_by_human == True` AND `last_decision == "approved"`. This preserves the Gate M1 Conditional candidate-only / human-review-first semantics.

6. **`redaction_policy` tightening**: `ContactSkillCandidate.redaction_policy` changed from `dict[str, Any]` to `ContactSkillRedactionPolicy`. Default values are identical, so existing JSON files remain compatible.

7. **Documentation**: `docs/07_handoff.md` updated with T120 worker draft record. Task is not marked as complete — explicitly noted as awaiting review.

## Positives

- **Human-review-first enforced**: `is_runtime_ready()` is a triple gate (status + human review + last decision). No candidate can accidentally become runtime-ready.
- **Legacy compatibility**: The service can ingest T112/T113 outputs directly, avoiding a migration step.
- **Provenance chain complete**: `DistilledArtifactSourceMetadata` preserves `source_run_id`, artifact paths, source chunk/memory/event IDs through load/save cycles.
- **Evidence refs preserved**: Verified through the load/save round-trip.
- **Conservative legacy handling**: Non-candidate legacy artifacts get `review_state="unknown"` and a note requiring re-approval, rather than being treated as pre-approved.
- **No scope creep**: No CLI, no DB migration, no vector DB, no runtime injection, no auto-approve.
- **Path safety**: All input/output confined to `private/distilled/`.

## Blocking Issues

None.

## Non-blocking Issues

### N01: `save_memory_store` / `save_contact_skill_store` no-op normalization

**Severity**: Low
**Location**: `contact_skill.py` lines 1009-1014, 1060-1065
**Detail**: Both save methods do `record.model_copy(update={"updated_at": record.updated_at})` — this copies the existing `updated_at` value to itself, which is a no-op. The intent appears to be updating `updated_at` to `utc_now()` on save, but the current code leaves the timestamp unchanged. Not a correctness issue (the value is still written correctly), but the normalization pass is wasted work and the comment/variable name `normalized_store` is misleading.

**Recommendation**: Either update to `utc_now()` or remove the normalization step entirely if the intent is to preserve original timestamps.

### N02: Code duplication between `ContactSkillBuilderService` and `ContactSkillFileStoreService`

**Severity**: Low
**Location**: `contact_skill.py`
**Detail**: The following private methods are duplicated between the two service classes with identical or near-identical implementations:
- `_resolve_existing_path`
- `_ensure_within_root`
- `_safe_relative_path`
- `_load_memory_facts_jsonl` (in `ContactSkillFileStoreService`) vs `_load_memory_facts` (in `ContactSkillBuilderService`)

Both classes also share the same `_repo_root` / `_private_distilled_root` initialization pattern.

**Recommendation**: Acceptable for MVP. A shared base class or module-level helpers could be extracted later if a third service needs the same pattern.

### N03: `_load_memory_store_file` and `_load_contact_skill_store_file` accept single-record shapes silently

**Severity**: Negligible
**Location**: `contact_skill.py` lines 1074-1088
**Detail**: When the JSON file contains `"memory_fact"` or `"contact_skill"` as a top-level key (instead of `"records"`), the code wraps it as a single-element list. This is convenient for migration but means a malformed file that happens to have the right key name will be silently accepted rather than raising an error. The Pydantic validation downstream provides sufficient type safety, so this is not a real risk.

**Recommendation**: No action needed.

### N04: `DistillationMemoryType` to `MemoryType` mapping collapses two types

**Severity**: Negligible
**Location**: `models.py` lines 343-350
**Detail**: Both `"semantic"` and `"episodic"` map to `MemoryType.FACT`. This is a reasonable simplification given the runtime model's coarser granularity, but it means the distinction is lost when converting to runtime format. T111 reviewer N03 noted this mapping as deferred to T120.

**Recommendation**: The mapping is defensible for MVP. If finer granularity is needed later, `MemoryType` can be extended or a new runtime type added.

### N05: No committed automated tests

**Severity**: Deferred (per project convention)
**Location**: N/A
**Detail**: Verification was done via ad-hoc script writing to `private/distilled/t120_store_smoke/`, not committed unit tests. This is consistent with the project's convention of deferring automated tests to T150.

**Recommendation**: T150 should include tests for: store record model validation, legacy wrapping, load/save round-trip, `is_runtime_ready()` gate logic, and path confinement.

## Forbidden Scope Check

| Forbidden action | Status |
|---|---|
| Database migration | NOT present. |
| Vector DB | NOT present. |
| Runtime prompt injection | NOT present. |
| Auto-approve | NOT present. `is_runtime_ready()` requires explicit human review. |
| CLI addition | NOT present. T122's job. |
| Candidate → runtime bypass | NOT present. Triple gate enforced. |

## Verification

- Compile: `python -m compileall` on both changed source files — passed.
- Load/save round-trip on synthetic fixture — verified by worker (not re-run by reviewer as private/ is not committed).
- No modifications to upstream services or exporters.
- No private data in docs or stdout.

## Warnings Classification

| ID | Classification | Rationale |
|---|---|---|
| N01 | Accepted | No-op normalization is wasted work but not incorrect. |
| N02 | Accepted/Deferred | Duplication is manageable for two services; revisit if pattern repeats. |
| N03 | Accepted | Single-record shape handling is convenient; Pydantic validates downstream. |
| N04 | Accepted | Mapping is reasonable for MVP granularity. |
| N05 | Deferred | Automated tests scheduled for T150 per project convention. |

## Recommended Next Action

Proceed to T121. During T121 implementation, pay attention to:

1. Whether `_default_review_metadata` for legacy artifacts needs to integrate with the evidence validator's output.
2. Whether N01's `updated_at` no-op should be fixed when T122 adds the review CLI (which will need to update timestamps on status changes).
3. Whether the `DistillationMemoryType` → `MemoryType` mapping holds up when T123 integrates approved records into `ChatContext`.
