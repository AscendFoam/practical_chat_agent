# T174 Review Explanation (for humans)

## 1. What T174 is about, in plain language

The project has been building a chat agent that can help you reply to contacts in a more relationship-aware way. Earlier work (T170–T173) designed and implemented a system that takes a large "ContactSkill" (a comprehensive profile of a contact relationship) and breaks it down into three smaller, more focused "briefs":

- **PartnerPersonaBrief**: Who is this person and what's the relationship like?
- **CommunicationPolicyBrief**: How should I communicate with them?
- **BoundaryProfileBrief**: What topics to avoid and what boundaries exist?

T173 created a "projection service" that produces these three briefs from a ContactSkill. But until T174, those briefs existed in isolation — they weren't wired into the actual chat context that the system uses when generating replies.

**T174's job**: Plug those derived briefs into the `ChatContext` (the bundle of information assembled before any reply planning happens), while making absolutely sure nothing that already works gets broken.

## 2. Detailed implementation explanation

### Goal

Integrate derived briefs into the context assembly pipeline as additive, optional overlays. If derived briefs are unavailable, the existing behavior must work exactly as before.

### Task flow

1. **New model** (`models.py`): Added `DerivedBriefContext`, a simple wrapper that holds:
   - A `status` field (not_configured / loaded / etc.)
   - The three briefs (persona, policy, boundary) — each optional
   - A `source_skill_record_id` for traceability
   - A `notes` list

2. **New field on ChatContext** (`models.py`): `ChatContext.derived_brief_context` with a default of `DerivedBriefContext()` (status="not_configured"). This means every existing code path that constructs a `ChatContext` continues to work without changes.

3. **Assembler integration** (`chat_context.py`): The `ChatContextAssembler.assemble()` method now:
   - Extracts the eligible `ContactSkillStoreRecord` from the approved-store loading step (modified return type of `_load_approved_store_context` and `_load_runtime_ready_contact_skill_brief` to also return the record)
   - Calls the committed `ContactSkillProjectionService.project_all()` to derive all three briefs from that record
   - Passes approved T164 patches into the projection so the policy brief can carry patch hints
   - Adds derived-brief notes to `memory_retrieval_notes`
   - Includes derived persona and boundary-sensitivity lines in the context summary
   - Returns everything in `ChatContext.derived_brief_context`

4. **Fallback behavior**: When no approved store is configured, when no records match, or when records aren't runtime-ready — the derived brief context stays at `not_configured` with all briefs set to `None`. The existing `ApprovedContactSkillBrief` path is completely untouched.

5. **Patch coexistence**: `ApprovedPatchContext` (from T164) and `DerivedBriefContext` are structurally independent fields on `ChatContext`. They load from separate paths and don't replace each other. Approved patches are also passed through to the projection service so the policy brief is patch-aware.

### What changed in code/config

| File | Change |
|------|--------|
| `src/practical_chat_agent/core/models.py` | Added `DerivedBriefContext` model (+8 lines); added `derived_brief_context` field on `ChatContext` (+1 line) |
| `src/practical_chat_agent/services/chat_context.py` | Modified return types for `_load_approved_store_context` and `_load_runtime_ready_contact_skill_brief` to carry the eligible record; added `_load_derived_brief_context` and `_build_derived_brief_notes` methods; extended `_build_summary` and `assemble()` to wire derived briefs |
| `tests/test_chat_context_decomposition.py` | New file with 39 tests in 10 classes covering load success, fallback scenarios, partial behavior, patch coexistence, projection output preservation, notes, summary, and determinism |
| `docs/07_handoff.md` | Added Section 76: T174 Implementation Record |
| `.claude/settings.json` | Permission allowlist entries for test commands (workspace artifact) |

### Significance for future development

This completes the M6 milestone (ContactSkill-Compatible Decomposition). The three derived briefs are now available at runtime alongside the existing aggregate brief and approved patches. Future M7+ work (e.g., T180 LLM candidate contract) can consume `ChatContext.derived_brief_context` fields for richer relationship-aware planning without needing to re-derive anything — the projection has already happened by the time the context is assembled.

## 3. Why the review verdict is PASS

The implementation is clean, additive, and correctly fulfills every requirement in the T174 task package:

- **Fallback preservation**: When no store is configured or no eligible records exist, `derived_brief_context` stays `not_configured` and all briefs are `None`. The existing `ApprovedContactSkillBrief` path is structurally unchanged. Tests verify this across three fallback scenarios (not configured, no runtime-ready records, contact mismatch).

- **No fake implementation**: The code calls the real `ContactSkillProjectionService.project_all()` from T173. There are no mocks, stubs, or hardcoded outputs. The projection service itself was committed and reviewed in T173.

- **Projection output preservation**: The assembler does not reformat `relationship_state_summary`, `important_event_summaries`, or `sensitivity_summary`. It passes them through as-is. Tests explicitly verify that `sensitivity_summary` reflects the projected max-sensitivity computation ("medium" from mixed-sensitivity topics), not a schema default.

- **Patch coexistence**: `ApprovedPatchContext` and `DerivedBriefContext` are independent fields. Tests verify both can be loaded simultaneously, that patches flow into the policy brief's `approved_patch_hints`, and that patches load independently when derived briefs are unavailable.

- **Test coverage**: 39 synthetic tests in 10 classes cover the full spectrum: load success (5 tests), fallback not-configured (3), fallback no-runtime-ready (3), fallback contact-mismatch (2), partial without patches (3), patch coexistence (5), projection output preservation (5), retrieval notes (4), summary inclusion (3), approved-brief fallback coexistence (4), and determinism/no-disk-writes (2). Zero regressions against the existing 288 tests.

- **Within scope**: Only allowed files were modified. No planner behavior changes, no ContactSkill mutations, no new persistence, no CLI changes, no raw transcript injection.

The non-blocking issues (unused `contact_id` parameter, per-assembly projection instantiation, status enum breadth) are minor and consistent with prior task dispositions.

## 4. Notes on Worker's own review/explanation

The Worker did not write separate review/explanation documents (which is expected — the Worker produces implementation and a handoff record, while the Reviewer produces the review documents). The Worker's handoff summary in `docs/07_handoff.md` Section 76 is accurate and matches the actual code changes. No corrections needed.
