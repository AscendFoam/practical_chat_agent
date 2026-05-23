# Review: T173

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01: `.claude/settings.json` was modified. Consistent with the pattern accepted across T150-T172 reviews (workspace artifact, not a task-scope violation).

N02: Missing direct field-projection assertions for `PartnerPersonaBrief.relationship_type`, `preferred_topics`, and `emotional_pattern_labels`. These projections are trivial (direct field assignment or `[x.field for x in list]`), and any field-name mismatch would surface as a compile-time `AttributeError`. The determinism test (`TestDeterminism`) and evidence-ref union tests (`TestPersonaEvidenceRefUnion`) implicitly exercise these paths. Not blocking because the risk of an incorrect trivial projection is negligible and the existing tests would catch regressions.

N03: `_max_sensitivity` accepts a `default` parameter that is unreachable in practice. The caller always includes `skill.sensitivity` (a required field on `ContactSkillCandidate`) in the `values` list, so `filtered` can never be empty. The `default=skill.sensitivity` is dead-code safety. Not blocking — harmless redundancy.

N04: `relationship_state_summary` format is a T173-internal convention not specified in the contract (contract Section 3.1 delegates: "Computed from record.contact_skill.relationship_state fields by T173"). The format is deterministic, documented in the handoff, and tested. However, if M8 (T190+) introduces a standalone `RelationshipState` model, this format string would likely be replaced. Not blocking — the worker correctly noted this in remaining risks.

## Missing Tests

None. The 47 committed synthetic tests cover all categories required by the task package:

- Approved/runtime-ready projection success (4 tests)
- Non-runtime-ready exclusion (5 tests: candidate, rejected, frozen, archived, approved-without-human-review)
- Contact-id/traceability preservation (4 tests)
- "unknown" -> None communication-style conversion (3 tests)
- relationship_state_summary projection (3 tests)
- Thin policy evidence (3 tests)
- Sensitivity_summary computation (5 tests, including parent-floor)
- important_event_summaries formatting (4 tests: with-date, without-date, mixed, empty)
- Policy-field mapping (3 tests)
- Boundary-field mapping (4 tests)
- Approved-patch-hints passthrough (3 tests)
- Persona evidence-ref union (2 tests, including deduplication)
- Boundary evidence-ref union (2 tests)
- Determinism (2 tests: same-result, writes-nothing-to-disk)

## Suspicious Implementation Details

None. The implementation is clean, pure, and deterministic:

- `ContactSkillProjectionService` is stateless — no `__init__` state, no side effects.
- `project_all` gates on `record.is_runtime_ready()` which checks `status="approved"`, `reviewed_by_human=True`, `last_decision="approved"`.
- Non-runtime-ready records return a result with `runtime_ready=False` and all three briefs set to `None` — no partial projection.
- Evidence-refs unions match the contract exactly: persona brief collects from relationship_state + communication_style + topics + patterns; policy brief collects from stable_preferences only; boundary brief collects from avoid_topics + important_events. Top-level `ContactSkillCandidate.evidence_refs` are correctly excluded from all three briefs.
- `_unique` helper deduplicates while preserving insertion order and filtering empty strings.
- `_project_communication_style` converts only the literal string `"unknown"` to `None` — other values pass through unchanged.
- `_format_event_summaries` produces `"{event} ({date})"` when date exists, `"{event}"` when absent.
- `_max_sensitivity` computes `max(avoid_topics + important_events + parent)` with parent as floor, exactly matching contract Section 7.
- No disk I/O, no LLM calls, no ContactSkill mutation, no ChatContext integration, no new storage.

## Recommended Next Action

Captain should accept T173 and advance the Current Unique Task to T174 (derived briefs context integration). T174 can now assume:

- `ContactSkillProjectionService.project_all()` produces all three briefs from a runtime-ready parent record.
- `approved_patch_hints` is an optional parameter (T174 wires the T164 patch loading).
- `ContactSkillProjectionResult` carries `record_id`, `contact_id`, `runtime_ready`, and optional typed briefs.
- All briefs carry `contact_id`, `evidence_refs`, and `source_skill_record_id`.
- `BoundaryProfileBrief.sensitivity_summary` is explicitly computed (not the schema default).
- The projection is pure/additive: `ApprovedContactSkillBrief` fallback remains intact and untouched.
