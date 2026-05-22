# Review: T170

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01: `BoundaryProfileBrief.sensitivity_summary` is typed as `DistillationSensitivity` and described as "highest sensitivity across all boundary-relevant areas." The max-across-areas reduction rule is stated in prose but not formalized. T171-T172 should define whether the projection takes `max()` of sub-model sensitivities or inherits the parent aggregate's top-level sensitivity. Low risk for a design document; implementation tasks will resolve this.

N02: `PartnerPersonaBrief.communication_style_snapshot` is typed as `dict[str, str]` rather than a structured sub-model. This is a deliberate simplification in the design doc and is acceptable, but T171 should decide whether to keep the dict form or promote it to a named model for type safety.

N03: `important_event_summaries` is placed in `BoundaryProfileBrief` rather than `PartnerPersonaBrief`. The rationale (important events may be sensitive and should be handled with boundary awareness) is defensible, but it means the persona brief lacks contextual events that could shape tone and topic selection. This is a design trade-off worth revisiting during T171 if the planner turns out to need event context in the persona layer.

N04: The field ownership table maps `approved_patch_hints` to `CommunicationPolicyBrief`, which is reasonable since patches are communication hints. However, a patch could also carry boundary signals (e.g., a patch that says "avoid mentioning X"). If a future patch type has boundary semantics, it may need to be reflected in `BoundaryProfileBrief` as well. This is an edge case that can be deferred to T172 or later.

N05: The handoff Section 68 (T170 Implementation Record) replaces what was previously Section 68 (T170 Kickoff Notes) and renumbers the kickoff notes to Section 69. This is correct but means the handoff document structure relies on section numbering that shifts. Not a functional issue, just a note for future handoff maintenance.

## Missing Tests

None required. T170 is a design-only task with no code changes.

## Suspicious Implementation Details

None. The task produces only documentation. The two modified files (`docs/architecture/contactskill_decomposition.md` and `docs/07_handoff.md`) are both within the `Allowed files` scope. No code was touched, no migration was defined, and no deprecation was claimed.

## Verification Checklist

| Verification Criterion | Result |
|---|---|
| References T120-T123 pipeline | Yes, Section 9 subsection "T120-T123" |
| References T130-T133 pipeline | Yes, Section 9 subsection "T130-T133" |
| References T160-T164 pipeline | Yes, Section 9 subsection "T160-T164" and `CommunicationPolicyBrief.approved_patch_hints` |
| Existing approved data remains runnable | Yes, Section 1 and Section 5 explicitly state fallback to `ApprovedContactSkillBrief` |
| Decomposition is projection/addition, not replacement | Yes, stated in Section 1 ("Derived briefs are projections, not replacements"), Section 5 (fallback), Section 8 (additive phases), Section 10 (non-goals) |
| Handoff updated with follow-up tasks and open questions | Yes, Section 68 in handoff |
| Only allowed files modified | Yes: `docs/architecture/contactskill_decomposition.md` (new), `docs/07_handoff.md` |
| No code changes | Confirmed: no changes in `src/` or `tests/` |
| No deprecation/replacement claim | Confirmed: document explicitly states "not replacements" in Section 1 and non-goal #4 in Section 10 |
| No forbidden scope violation | Confirmed: no LLM, platform, send-gate, realtime, or migration scope |

## Recommended Next Action

T170 is complete and accepted. The next tasks in sequence are:

- **T171**: `PartnerPersonaBrief` schema (Pydantic model definition, no runtime integration).
- **T172**: `CommunicationPolicyBrief` + `BoundaryProfileBrief` schemas.
- **T173**: `ContactSkillProjectionService` (lazy projection from approved store records).
- **T174**: Derived-brief context integration in `ChatContextAssembler`.

T171 may proceed under normal review constraints. It should resolve N01 (sensitivity reduction rule) and N02 (dict vs. model for communication_style_snapshot) during schema definition.
