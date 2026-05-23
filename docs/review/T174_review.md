# Review: T174

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01 — `.claude/settings.json` is a workspace artifact (permission allowlist entries) rather than a T174 scope violation. Consistent with prior task dispositions (T161–T164, T173).

N02 — `_load_derived_brief_context` instantiates `ContactSkillProjectionService()` on every call. This is a per-assembly cost that is acceptable for the current offline workflow but would benefit from injection or caching if assembly frequency increases. Not a blocker.

N03 — `DerivedBriefContext.status` reuses the `ApprovedStoreContextStatus` enum. This is slightly broader than strictly necessary (e.g., `"store_path_missing"` will never appear on `DerivedBriefContext`) but is harmless and consistent with the project pattern established by `ApprovedStoreContext` and `ApprovedPatchContext`.

N04 — The `contact_id` parameter in `_load_derived_brief_context` is accepted but never used. The projection operates entirely on the `skill_record` which already carries the correct `contact_id`. The parameter is not harmful but adds dead surface area.

N05 — `_build_derived_brief_notes` truncates `stable_preference_hints` to `[:2]`. This is a reasonable compact-context budget, but the magic number is not explained. Very minor.

## Missing Tests

M01 — No test for the edge case where the projection result has `runtime_ready=False` despite the record passing `_contact_skill_record_eligible`. Currently this path is unreachable in practice because `_load_approved_store_context` already checks eligibility before returning the record, but a defensive test would document the invariant.

M02 — No test for `_build_derived_brief_notes` when `policy` is `None` but `status == "loaded"` (the note builder skips `stable_preference_hints` correctly, but this branch is not independently covered).

M03 — No end-to-end test with real `private/distilled/` files, but this is consistent with the T164 synthetic-test approach and is acceptable at the current offline-workflow stage.

## Suspicious Implementation Details

None found. The implementation is straightforward and correctly delegates all projection logic to the committed `ContactSkillProjectionService`. The assembler does not reinterpret, reformat, or backfill any projection output. The approved-patch context path (T164) and the derived-brief context path are structurally independent and coexist without overlap.

## Recommended Next Action

Update `docs/04_task_board.md` to mark T174 complete and advance to T180 (LLM Candidate Contract, M7) or another milestone per captain judgment. The M6 milestone is now functionally complete: T170 design → T171/T172 schemas → T173 projection → T174 context integration.
