# Review: T172

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01: `CommunicationPolicyBrief.evidence_refs` draws evidence only from `stable_preferences` entries. `ContactSkillReplyStrategy` and `ContactSkillUserSidePreferences` do not carry their own `evidence_refs`, so the policy brief's evidence trail is structurally thin — reply strategy and user-preference signals have no direct evidence pointer. This is correctly documented in the contract (Section 3.2 and Section 4) and acknowledged by the worker. Not blocking because this is a structural property of the upstream models, not a T172 design flaw. T173 projection should preserve this faithfully without inventing synthetic evidence.

N02: `BoundaryProfileBrief.sensitivity_summary` defaults to `"low"` in the Pydantic model definition (`sensitivity_summary: DistillationSensitivity = "low"`). The contract (Section 7) specifies that the actual value should be computed via the reduction rule `max(avoid_topics sensitivities, important_events sensitivities, parent aggregate sensitivity)`. The default will be overwritten by T173 projection in all real usage, but if someone constructs a brief manually without supplying `sensitivity_summary`, the model will silently produce `"low"` regardless of whether the parent record is `"medium"` or `"high"`. Not blocking because T173 must compute the value; the default is a safe schema-level lower bound.

N03: `important_event_summaries` is `list[str]` with no structural format constraint. The contract doc says summaries should be formatted as `"Event (date)"` (e.g., `"Graduation ceremony (2024-06)"`), but the model allows any string. This is acceptable at schema stage — T173 projection will control formatting — but a comment on the field noting the expected format would improve discoverability. Not blocking.

N04: `.claude/settings.json` was modified. Consistent with the pattern accepted across T150-T171 reviews (workspace artifact, not a task-scope violation).

## Missing Tests

None. The 31 committed synthetic tests cover:

- CommunicationPolicyBrief: minimal construction, full construction (2 tests)
- CommunicationPolicyBrief required fields: contact_id required/non-empty, source_skill_record_id required/non-empty (4 tests)
- CommunicationPolicyBrief safe defaults: approach fields None, user fields None, list fields empty (3 tests)
- CommunicationPolicyBrief patch-hint enrichment: type check, multiple patches, empty patches (3 tests)
- CommunicationPolicyBrief serialization: round-trip, exclude-none (2 tests)
- BoundaryProfileBrief: minimal construction, full construction (2 tests)
- BoundaryProfileBrief required fields: contact_id required/non-empty, source_skill_record_id required/non-empty (4 tests)
- BoundaryProfileBrief sensitivity: default "low", all valid values, invalid rejected (3 tests)
- BoundaryProfileBrief safe defaults: all lists empty, minimal serialization (2 tests)
- BoundaryProfileBrief serialization: round-trip (1 test)
- Cross-brief shared contract: shared source_skill_record_id, flat evidence_refs, shared contact_id, no schema_version, no approval status (5 tests)

## Suspicious Implementation Details

None. The models are pure additive Pydantic schemas with no runtime logic, no methods, no computed fields, and no mutations. The diff shows 44 lines added, 0 lines removed in `models.py`. No existing models were modified.

The contract document is thorough and well-structured: 9 sections covering models, source projection rules, evidence/traceability, fallback relationship, approval inheritance, sensitivity reduction, versioning, and non-goals.

## Recommended Next Action

Captain should accept T172 and advance the Current Unique Task to T173 (ContactSkill projection service). T173 can now assume:
- All three brief schemas are committed (PartnerPersonaBrief, CommunicationPolicyBrief, BoundaryProfileBrief).
- The sensitivity reduction rule is documented (contract Section 7).
- The `"unknown"` → `None` communication-style conversion rule is deferred to T173.
- The `relationship_state_summary` projection rule is deferred to T173.
- Patch enrichment uses existing `ApprovedPatchBrief` from T164.
