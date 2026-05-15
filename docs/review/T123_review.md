# T123 Review: Context Integration

## Reviewer

Claude Code (adversarial review)

## Verdict

**PASS_WITH_WARNINGS**

## Scope Check

Worker modified exactly the 4 allowed files:

- `src/practical_chat_agent/core/models.py` (new compact brief models + `approved_store_context` field on `ChatContext`)
- `src/practical_chat_agent/services/chat_context.py` (extended `ChatContextAssembler` with approved-store loading)
- `src/practical_chat_agent/app/container.py` (optional env-var injection for `ChatContextAssembler`)
- `docs/07_handoff.md` (T123 completion record)

No other tracked files were modified. No changes to `app/main.py`, `services/contact_skill.py`, or any file outside allowed scope.

## What was done

1. **New compact brief models in `core/models.py`**:
   - `ApprovedMemoryFactBrief`: record_id, memory_id, memory_type, claim, evidence_refs.
   - `ApprovedContactSkillBrief`: record_id, contact_id, relationship_type, relationship_summary, strategy_hints, boundary_reminders, evidence_refs.
   - `ApprovedStoreContext`: status (`not_configured` / `store_path_missing` / `validation_report_missing` / `no_runtime_ready_records` / `loaded`), source_path, validation_report_path, contact_id, contact_skill, memory_facts, source_record_ids, evidence_refs, notes.
   - `ApprovedStoreContextStatus` literal type.
   - `ChatContext.approved_store_context` field with `ApprovedStoreContext` default.

2. **Extended `ChatContextAssembler`** (~250 new lines):
   - `__init__` gains optional `approved_store_path` and `approved_memory_limit`.
   - `assemble()` now calls `_load_approved_store_context(contact_id=event.actor_id)` and includes result in summary and retrieval notes.
   - `_load_approved_store_context()`: resolves path, loads validation report, loads memory/skill stores, filters for runtime-ready records, builds briefs.
   - Eligibility methods (`_memory_record_eligible`, `_contact_skill_record_eligible`): 5-gate filter — contact_id match, status="approved", `is_runtime_ready()`, evidence_validation_status="passed", validation record evidence-ready (0 missing refs, >0 checked refs).
   - Brief builders: compact relationship summary, strategy hints, boundary reminders, limited evidence refs.
   - Path confinement: `_ensure_within_private_distilled`.
   - Graceful degradation: missing path → `not_configured`, missing file → `store_path_missing`, no report → `validation_report_missing`, no eligible records → `no_runtime_ready_records`.

3. **Container injection in `app/container.py`**:
   - Reads `PRACTICAL_CHAT_APPROVED_STORE_PATH` and `PRACTICAL_CHAT_APPROVED_MEMORY_LIMIT` env vars.
   - Passes to `ChatContextAssembler` constructor.
   - Defaults to `None` (no store) and `4` memory limit.

4. **Handoff update**: T123 completion record with verification results.

## Positives

- **Five-gate eligibility filter is correct and complete**:
  1. `contact_id` match (memory `subject_id` / skill `contact_id` must equal `event.actor_id`)
  2. `status == "approved"` (explicit string check, not trusting anything else)
  3. `is_runtime_ready()` (T120's triple gate: approved + human-reviewed + last_decision=approved)
  4. `evidence_validation_status == "passed"` (review metadata carries T122's validation result)
  5. `_validation_record_is_evidence_ready()` (re-checks the T121 report: 0 missing refs, >0 checked refs)
  - All five gates must pass. Candidate/rejected/frozen/archived records fail at gate 2 or 3. Missing-evidence records fail at gate 4 or 5.

- **Brief stays genuinely compact**:
  - Memory claim truncated to 140 chars.
  - Relationship summary truncated to 160 chars.
  - Strategy hints limited to 4, each truncated to 120 chars.
  - Boundary reminders limited to 4 (2 from usage_boundary.notes + 2 from user_side_preferences.boundaries).
  - Evidence refs limited to 6 per record.
  - Memory facts limited by `approved_memory_limit` (default 4).
  - Summary text only includes brief relationship summary + at most 2 memory claim fragments.
  - No raw transcript, no full JSON, no long quotes.

- **Graceful degradation is well-designed**:
  - No store path → `not_configured`, existing behavior unchanged.
  - Missing path → `store_path_missing`, clear note.
  - Missing validation report → `validation_report_missing`, no records loaded.
  - No eligible records → `no_runtime_ready_records`.
  - In all failure cases, `ChatContext` is still valid, just without approved-store content.

- **Path confinement**: `_ensure_within_private_distilled` checks store path stays under `private/distilled/`.

- **No runtime integration, no ReplyPlanner, no LLM, no DB, no vector DB, no auto-send**: pure file-reading + Pydantic validation.

- **Container injection is non-breaking**: env vars are optional, defaults keep existing behavior.

## Blocking Issues

None.

## Non-blocking Issues

### N01: `contact_id=event.actor_id` assumes the inbound event actor is the contact

**Severity**: Medium
**Location**: `chat_context.py` line 68
**Detail**: `_load_approved_store_context(contact_id=event.actor_id)` uses the inbound event's `actor_id` as the contact_id to match against store records. In the current system, `InboundEvent.actor_id` is the user who sent the message. For a contact-skill scenario, the "contact" is the person the user is chatting with, which may not be `actor_id` — it depends on the context assembly call site.

In the existing runtime flow, `event.actor_id` is the external user talking to the agent. The agent then uses `ChatContext` to decide how to reply. If the user is chatting with "contact_A", the `event.actor_id` would be "contact_A"'s ID, and the store should have a matching `contact_id=contact_A` skill. This mapping is correct IF the external platform uses the same IDs. However, there is no explicit documentation or contract that guarantees this alignment.

This is acceptable for MVP since the approved-store context is loaded from private files that the user controls, and the contact_id in the store is derived from the same WeFlow export pipeline that feeds the normalized events. But it should be validated when connecting to a real platform.

**Recommendation**: Acceptable for MVP. T130/T131 should verify the contact_id alignment when implementing the ReplyPlanner.

### N02: Dead code in `_load_approved_store_context` (lines 185-187)

**Severity**: Low
**Location**: `chat_context.py` lines 185-187
**Detail**: When execution reaches the `no_runtime_ready_records` branch (line 184), `validation_report_path` is guaranteed to be non-`None` because the function returns early at lines 156-162 if the report is missing. Therefore, the condition `if validation_report_path is None:` at line 186 is dead code — it will never be `True` at this point.

Additionally, `notes or [...]` at line 193 will always evaluate to the fallback `["No approved runtime-ready store records matched this contact."]` because `notes` is initialized as `[]` and the dead-code append never fires, so `[] or [...]` → `["..."]`.

The behavior is correct (the right message is shown), but the dead conditional is misleading.

**Recommendation**: Remove the dead conditional. Replace with `notes=["No approved runtime-ready store records matched this contact."]`.

### N03: `_build_approved_store_notes` includes claim text in retrieval notes

**Severity**: Low
**Location**: `chat_context.py` lines 234-237
**Detail**: When `context.memory_facts` is present, `_build_approved_store_notes` appends `approved_memory_facts=<claims>` to the retrieval notes. These notes are part of `ChatContext.memory_retrieval_notes`, which could be exposed in logs, prompts, or debug output. The claims come from approved store records, so they have been human-reviewed, but they may still contain semi-sensitive relationship observations.

The truncation is already handled (claims are compacted to 140 chars in the brief, and only 2 are shown), and the claims are from approved records that passed human review, so this is consistent with the T123 design.

**Recommendation**: Acceptable. The claims are from human-approved records and are already compacted.

### N04: `_read_json_model` uses bare `except Exception`

**Severity**: Low
**Location**: `chat_context.py` lines 414-425
**Detail**: `_read_json_model` wraps `model_type.model_validate(payload)` in `except Exception:`. This catches all exceptions including `KeyboardInterrupt` subclasses in some edge cases (though not `BaseException` subclasses like `SystemExit`). The intent is to gracefully handle malformed store files, which is correct for the use case. However, it also silently swallows Pydantic validation errors that might indicate data corruption.

**Recommendation**: Acceptable for MVP. The graceful degradation pattern (return None → context stays without store data) is the right trade-off. T150 could add logging for validation failures.

### N05: No committed automated tests

**Severity**: Deferred (per project convention)
**Location**: N/A
**Detail**: Verification was done against private synthetic fixtures (`t123_approved_fixture`, `t123_exclusion_fixture`, `t123_memory_only_fixture`), not committed unit tests. Consistent with project convention of deferring tests to T150.

**Recommendation**: T150 should include tests for: five-gate eligibility filter (each gate independently), compact brief construction, path confinement, graceful degradation (missing path/file/report/records), memory limit enforcement, evidence ref limit, and no-store-path compatibility.

### N06: Approved memory-only positive path not verified

**Severity**: Low
**Location**: Worker's own admission in handoff
**Detail**: The worker noted: "Current private fixtures verify the positive contact-skill path and the exclusion path. They do not yet provide a runtime-ready approved memory-only sample, so the positive memory-brief branch remains unobserved."

The `_load_runtime_ready_memory_briefs` code path is structurally identical to `_load_runtime_ready_contact_skill_brief` and uses the same eligibility gates. The risk of a bug is low, but the path is unobserved.

**Recommendation**: Acceptable. The memory-brief path should be re-checked when a safe approved-memory-only fixture is available, or in T150.

## Forbidden Scope Check

| Forbidden action | Status |
|---|---|
| Inject candidate records | NOT present. Eligibility requires `status="approved"`. |
| Inject rejected/frozen/archived | NOT present. Eligibility requires `status="approved"` + `is_runtime_ready()`. |
| Inject missing-evidence records | NOT present. Requires `evidence_validation_status="passed"` + validation record evidence-ready. |
| Inject not-human-reviewed records | NOT present. `is_runtime_ready()` requires `reviewed_by_human=True`. |
| Full skill JSON / all memory / raw transcript | NOT present. Briefs are compact with truncation and limits. |
| ReplyPlanner | NOT present. |
| Auto-send | NOT present. |
| DB migration | NOT present. |
| Vector DB | NOT present. |
| LLM call | NOT present. Pure file reading + Pydantic validation. |
| Read `private/chat_history/` | NOT present. Only reads `private/distilled/`. |
| Private data in docs/stdout | NOT present. |

## Verification Assessment

- **Compile**: passed (3 files).
- **Approved fixture**: `t123_approved_fixture` → `status=loaded`, approved contact-skill brief entered summary and retrieval notes. Correct.
- **Exclusion fixture**: `t123_exclusion_fixture` → `status=no_runtime_ready_records`, rejected record excluded. Correct.
- **Memory-only fixture**: `t123_memory_only_fixture` → approved skill loaded, approved memory with missing refs excluded. Correct.
- **No-store compatibility**: direct `ChatContextAssembler()` with no store path → `status=not_configured`, existing behavior unchanged. Correct.

Four verification scenarios cover: positive path, exclusion, mixed eligibility, and compatibility. The memory-only positive path (N06) is the only uncovered branch.

## Warnings Classification

| ID | Classification | Rationale |
|---|---|---|
| N01 | Accepted | `contact_id` alignment assumption is documented; correct for current pipeline; T130/T131 validates. |
| N02 | Accepted | Dead code is misleading but harmless; behavior is correct; low priority cleanup. |
| N03 | Accepted | Claims from human-approved records, already compacted, consistent with design. |
| N04 | Accepted | Graceful degradation pattern is correct for MVP; logging improvement deferred. |
| N05 | Deferred | Automated tests scheduled for T150 per project convention. |
| N06 | Accepted | Memory-only positive path structurally sound but unobserved; low risk. |

## Recommended Next Action

T123 completes M2. Captain should decide:

1. Whether M2 needs a milestone review (T120-T123 collectively) before proceeding to M3.
2. If proceeding to M3, T130 (ReplyPlan schema) can begin. T130 should verify that the `ApprovedStoreContext` / `ApprovedContactSkillBrief` fields provide sufficient information for the ReplyPlanner.
3. T150 should cover the five-gate eligibility filter, compact brief construction, path confinement, graceful degradation, and the memory-only positive path (N06).
4. N02 (dead code) can be cleaned up in a future pass or in T150.
