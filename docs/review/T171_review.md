# Review: T171

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01: `.claude/settings.json` was modified to add T171-related permission entries. This is consistent with the pattern established across T150-T170 reviews (accepted as workspace artifact rather than task-scope violation).

N02: `CommunicationStyleSnapshot` fields are `str | None` without constrained values (e.g., no `Literal["short", "medium", "long", "mixed", None]`). This is acceptable for schema-only work — the contract doc lists expected values, and T173 projection can decide whether to validate or coerce. But note that `ContactSkillCommunicationStyle` uses plain `str` defaults of `"unknown"` for the same dimensions, so the mapping from `"unknown"` → `None` in T173 will need an explicit conversion rule. This is already documented in the contract (Section 2.1), so no action needed now.

N03: `relationship_state_summary` is a free-form `str` with only `min_length=1`. The contract correctly identifies this as a T173 concern. The field is structurally sound but semantically broad — there is no structural guarantee that the summary will actually reflect relationship state rather than arbitrary text. Acceptable at schema stage; T173 projection should document what fields from `ContactSkillRelationshipState` feed into this summary.

N04: `evidence_refs` at the brief level merges evidence from multiple sub-models (relationship_state, communication_style, topics, patterns) into a flat list, losing per-area attribution. The contract explains the design (Section 4), and the flat list is simpler for consumers. This is a valid trade-off, but if T173 or T174 consumers need to know *which* sub-model produced a given evidence ref, they would need to reconstruct attribution. Not blocking; document for awareness.

N05: `PartnerPersonaBrief` does not carry a `schema_version` field, unlike `ContactSkillCandidate` which has `"contact_skill_v1"`. If the brief schema evolves, there is no built-in version marker. The parent `ContactSkillStoreRecord` has its own versioning through the approved-store path, so this is low risk. Noted for potential T172+ consideration.

## Missing Tests

None. The 21 committed synthetic tests cover:

- Valid construction: minimal, full, all relationship types (3 tests)
- Required traceability fields: contact_id, relationship_state_summary, source_skill_record_id (required + non-empty), relationship_type required (7 tests)
- Safe defaults / optional fields: communication_style defaults, topics, patterns, evidence refs, partial snapshot (5 tests)
- Communication style snapshot typing: structured-not-dict, field access, round-trip, exclude-none, brief-level round-trip (5 tests)
- Invalid relationship type rejection (1 test)

The coverage is appropriate for a schema-only task. No mocks, stubs, or hardcoded behavior was found.

## Suspicious Implementation Details

None found. Specific checks:

1. **Additive only**: The diff adds exactly two new Pydantic models (`CommunicationStyleSnapshot` and `PartnerPersonaBrief`) at lines 924-939 in `models.py`, placed immediately before the `ChatContext.model_rebuild()` call. No existing models were modified.

2. **No ContactSkill mutation**: `ContactSkillCandidate`, `ContactSkillStoreRecord`, `ContactSkillCommunicationStyle`, and all other existing models remain untouched.

3. **No runtime integration**: No new service, CLI entrypoint, `ChatContext` integration, or `ReplyPlanner` wiring.

4. **No storage/migration/approval logic**: The models are pure Pydantic schemas with no file IO, database, or approval behavior.

5. **Type correctness**: `ContactRelationshipType` is correctly reused from the existing type alias. The `CommunicationStyleSnapshot` field mapping is a clean subset of `ContactSkillCommunicationStyle` (4/4 dimensions projected, with `confidence`/`evidence_refs`/`sensitivity`/`status` intentionally excluded as sub-model metadata).

6. **Contract documentation**: The new `docs/data_contracts/contactskill_decomposition_contract.md` is thorough, covering fields, source projection rules, evidence traceability, fallback relationship, and approval inheritance. It explicitly resolves T170 review N02 (dict vs. named model).

7. **Handoff record**: Section 70 is a complete implementation record with verification results and clear forward pointers to T172.

## Verification Checklist

| Verification Criterion | Result |
|---|---|
| Task goal met (additive PartnerPersonaBrief schema) | Yes: two Pydantic models added, no existing models modified |
| T170 N02 resolved (communication_style_snapshot typing) | Yes: named sub-model chosen, rationale documented in contract Section 2.1 |
| Within allowed files | Yes: `models.py`, contract doc, test file, handoff |
| No forbidden scope violation | Yes: no projection service, no runtime integration, no ContactSkill mutation, no CLI entrypoint, no storage/migration |
| No mocks/stubs/hardcoded behavior | Yes: pure Pydantic models + synthetic validation tests |
| Tests adequate | Yes: 21 committed synthetic tests, all passing |
| No regression | Yes: 210 tests pass (189 existing + 21 new) |
| Contract documentation complete | Yes: fields, source projection, evidence, fallback, approval inheritance, non-goals |
| Handoff updated | Yes: Section 70 implementation record |
| Evidence/source traceability explicit | Yes: `source_skill_record_id` required + non-empty, `evidence_refs` per-area union documented |
| Fallback relationship preserved | Yes: `ApprovedContactSkillBrief` remains minimum guaranteed output |
| No deprecation/replacement claim | Yes: contract Sections 5 and 7 explicitly state non-replacement |

## Recommended Next Action

T171 is complete and accepted. The next task is T172 (`CommunicationPolicyBrief` + `BoundaryProfileBrief` schemas). T172 should:

- Define the `CommunicationPolicyBrief` schema (reply strategy + user-side preferences + stable preferences + approved patch hints).
- Define the `BoundaryProfileBrief` schema (avoid topics + boundary rules + usage notes + important events + sensitivity_summary).
- Resolve T170 N01: formalize the `sensitivity_summary` reduction semantics.
- Address T170 N04: document how boundary-signaling patch hints relate to boundary ownership.
