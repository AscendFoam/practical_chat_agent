# ContactSkill-Compatible Decomposition Design

Task: T170
Status: design-only, no code, no migration, no deprecation
Date: 2026-05-22

## 1. Purpose

This document defines how approved `ContactSkill` records can project into smaller, more focused derived briefs without deleting, replacing, or deprecating the existing aggregate record. The goal is to reduce ContactSkill overload for downstream consumers (reply planner, policy engine, context assembler) while keeping the T120-T164 storage, approval, and runtime path fully operational.

ContactSkill remains the single source of truth. Derived briefs are projections, not replacements.

## 2. Current Pain Points

The all-in-one `ContactSkillCandidate` aggregate carries 20+ fields spanning at least four distinct responsibilities:

1. **Partner persona** — who is this person and how do they communicate (relationship_type, relationship_state, communication_style, preferred_topics, emotional_patterns).
2. **Communication policy** — how should we reply (reply_strategy, user_side_preferences, stable_preferences).
3. **Boundary profile** — what to avoid and what is sensitive (avoid_topics, usage_boundary, user_side_preferences.boundaries).
4. **Evidence and review metadata** — source traceability and approval state (evidence_refs, confidence, sensitivity, status, source_chunk_ids, source_memory_ids, review_notes, redaction_policy).

Consumers rarely need all four areas at once:

- `ReplyPlanner` primarily needs communication policy and boundary signals.
- `ReplyPlanPolicyEngine` primarily needs boundary profile and relationship-state summaries.
- `ChatContextAssembler` currently compresses everything into a single `ApprovedContactSkillBrief` with one `relationship_summary` string and flat `strategy_hints` / `boundary_reminders` lists. This compression is lossy and makes it hard to evolve policy signals independently of persona signals.

The aggregate also makes evidence ownership ambiguous: all evidence_refs are collected at the top level, but different areas (relationship_state vs. communication_style vs. avoid_topics) may have different evidence strengths. The current `ContactSkillRelationshipState` and `ContactSkillCommunicationStyle` sub-models already carry their own evidence_refs, but topics, patterns, and strategies do not have a clear per-area evidence boundary.

## 3. Proposed Derived-Brief Set

Three derived briefs, each with a narrow, well-defined responsibility:

### 3.1 PartnerPersonaBrief

Who this person is, how the relationship stands, and how they communicate.

Fields:
- `contact_id: str`
- `relationship_type: ContactRelationshipType`
- `relationship_state_summary: str` (compact, human-readable)
- `communication_style_snapshot: dict[str, str]` (message_length, tone, response_latency, directness)
- `preferred_topics: list[str]` (topic strings only, not full TopicPreference objects)
- `emotional_pattern_labels: list[str]` (pattern strings only)
- `evidence_refs: list[str]` (union of relationship_state + communication_style evidence)
- `source_skill_record_id: str` (traceability to the parent ContactSkill store record)

Responsibility: consumed by context assembly for relationship framing, and by the planner for understanding who the contact is.

### 3.2 CommunicationPolicyBrief

How the system should draft replies for this contact.

Fields:
- `contact_id: str`
- `default_approach: str`
- `cold_contact_approach: str | None`
- `topic_opener_approach: str | None`
- `sensitive_topic_approach: str | None`
- `user_goal: str | None`
- `preferred_reply_style: str | None`
- `stable_preference_hints: list[str]` (pattern strings from stable_preferences)
- `approved_patch_hints: list[ApprovedPatchBrief]` (from T164, already compact)
- `evidence_refs: list[str]` (union of reply_strategy + user_side_preferences + stable_preferences evidence)
- `source_skill_record_id: str`

Responsibility: consumed by `ReplyPlanner` to shape candidate drafts, and by `ChatContextAssembler` to build strategy hints.

### 3.3 BoundaryProfileBrief

What to avoid, what is sensitive, and what the hard limits are.

Fields:
- `contact_id: str`
- `avoid_topics: list[str]` (topic strings only)
- `boundary_rules: list[str]` (from user_side_preferences.boundaries)
- `disallowed_uses: list[str]` (from usage_boundary.disallowed_uses)
- `usage_notes: list[str]` (from usage_boundary.notes)
- `important_event_summaries: list[str]` (event descriptions with dates, if available)
- `sensitivity_summary: DistillationSensitivity` (highest sensitivity across all boundary-relevant areas)
- `evidence_refs: list[str]` (union of avoid_topics + boundaries + important_events evidence)
- `source_skill_record_id: str`

Responsibility: consumed by `ReplyPlanPolicyEngine` for boundary detection, and by `ChatContextAssembler` for boundary reminders.

## 4. Field Ownership Table

Maps current `ContactSkillCandidate` areas to future derived briefs. Fields that appear in the parent aggregate but are not projected into any brief remain accessible through the fallback aggregate.

| ContactSkill Area | Fields | Projected Into |
|---|---|---|
| relationship_type | `relationship_type` | PartnerPersonaBrief |
| relationship_state | `current_status`, `closeness`, `trust_level`, `interaction_frequency`, `initiative_balance`, `confidence`, `evidence_refs` | PartnerPersonaBrief |
| communication_style | `message_length`, `tone`, `response_latency`, `directness`, `confidence`, `evidence_refs` | PartnerPersonaBrief |
| preferred_topics | `topic`, `reason` per entry | PartnerPersonaBrief |
| emotional_patterns | `pattern` per entry | PartnerPersonaBrief |
| reply_strategy | `default`, `when_contact_is_cold`, `when_contact_opens_topic`, `for_sensitive_topics` | CommunicationPolicyBrief |
| user_side_preferences | `user_goal`, `preferred_reply_style` | CommunicationPolicyBrief |
| user_side_preferences.boundaries | `boundaries` list | BoundaryProfileBrief |
| stable_preferences | `pattern` per entry | CommunicationPolicyBrief |
| avoid_topics | `topic`, `reason` per entry | BoundaryProfileBrief |
| important_events | `event`, `date`, `importance` per entry | BoundaryProfileBrief |
| usage_boundary | `allowed_uses`, `disallowed_uses`, `notes` | BoundaryProfileBrief |
| evidence_refs (top-level) | collected refs | Available via fallback aggregate |
| confidence (top-level) | aggregate confidence | Available via fallback aggregate |
| sensitivity (top-level) | aggregate sensitivity | BoundaryProfileBrief (highest across areas) |
| status | candidate/approved/rejected/frozen/archived | Approval gate, not projected into briefs |
| source_chunk_ids | chunk traceability | Available via fallback aggregate |
| source_memory_ids | memory traceability | Available via fallback aggregate |
| review_notes | human review annotations | Available via fallback aggregate |
| redaction_policy | privacy rules | Available via fallback aggregate |
| approved_patch_hints | from T164 compact context | CommunicationPolicyBrief (already separate) |

## 5. Fallback Strategy

The existing runtime path must continue to work if no derived briefs exist:

1. **Projection is optional.** `ChatContextAssembler` first checks whether derived briefs are available for the target contact.
2. **If derived briefs exist:** assembler uses them directly, producing richer, more structured context than the current single `ApprovedContactSkillBrief`.
3. **If derived briefs are absent:** assembler falls back to the existing `ApprovedContactSkillBrief` compression from T123, which reads the approved `ContactSkillStoreRecord` and produces a flat `relationship_summary` + `strategy_hints` + `boundary_reminders`. This path is unchanged.
4. **Mixed state.** If some briefs exist but not all (e.g., only PartnerPersonaBrief is available), the assembler uses what exists and fills gaps from the fallback aggregate. This prevents partial decomposition from breaking the runtime.

The fallback contract is explicit: `ApprovedContactSkillBrief` is the minimum guaranteed output. Derived briefs are a richer optional overlay.

## 6. Evidence-Ref Preservation Rules

1. Each derived brief carries its own `evidence_refs` list, projected from the relevant sub-models of the parent `ContactSkillCandidate`.
2. Sub-models that already have per-area evidence (`ContactSkillRelationshipState.evidence_refs`, `ContactSkillCommunicationStyle.evidence_refs`) contribute directly.
3. Sub-models without per-area evidence (`ContactSkillTopicPreference`, `ContactSkillPattern`, `ContactSkillImportantEvent`) contribute their individual `evidence_refs` to the brief that owns them.
4. Top-level `ContactSkillCandidate.evidence_refs` are not projected into any single brief. They remain accessible through the fallback aggregate and represent cross-cutting evidence that does not belong to a specific area.
5. Evidence validation (T121) continues to operate on the parent `ContactSkillStoreRecord`. Derived briefs do not require separate evidence validation because they are projections of an already-validated record.

## 7. Approval-Boundary Rules

1. Derived briefs are not independently approved. They inherit the approval status of their parent `ContactSkillStoreRecord`.
2. A brief can only be produced from a record where `is_runtime_ready() == True` (status=approved, reviewed_by_human=True, last_decision=approved).
3. If the parent record transitions to rejected/frozen/archived, all derived briefs derived from it become invalid and must not enter runtime context. The fallback aggregate is similarly excluded.
4. The projection service (T173) must check `is_runtime_ready()` before producing any brief.
5. Derived briefs carry `source_skill_record_id` for traceability but do not carry review metadata or review history. That information stays on the parent store record.

## 8. Compatibility and Migration Phases

### Phase 1: Schema Definition (T171-T172)

- Define `PartnerPersonaBrief` and `CommunicationPolicyBrief` as Pydantic models in `core.models`.
- Define `BoundaryProfileBrief` as a Pydantic model.
- No runtime integration. No projection logic. No CLI.
- Models are additive: they do not modify `ContactSkillCandidate` or any existing model.

### Phase 2: Projection Service (T173)

- Implement a `ContactSkillProjectionService` that takes an approved `ContactSkillStoreRecord` and produces zero or more derived briefs.
- The projection is a pure function of the store record: same input always produces the same briefs.
- Projection is lazy: briefs are computed at context-assembly time, not stored separately. This avoids a new storage format and a new approval workflow.
- If the approved store record is absent or not runtime-ready, no briefs are produced and the assembler falls back.

### Phase 3: Context Integration (T174)

- Extend `ChatContextAssembler` to consume derived briefs when available.
- `ChatContext.approved_store_context` gains optional fields for the three brief types.
- The existing `ApprovedContactSkillBrief` field remains as the fallback.
- `ReplyPlanner` and `ReplyPlanPolicyEngine` are updated to read from the richer brief structure when present, falling back to current behavior when absent.

### Phase constraints

- Each phase is a separate task with its own allowed files and forbidden scope.
- No phase may modify `ContactSkillCandidate`, `ContactSkillStoreRecord`, `ContactSkillStoreFile`, or the T120-T122 review/approval pipeline.
- No phase introduces a new storage format for derived briefs.
- No phase claims ContactSkill is deprecated or replaced.

## 9. Relationship to Existing Pipeline

### T113 (ContactSkill Builder)

Unchanged. T113 produces `ContactSkillCandidate` which remains the authoritative shape. Derived briefs are projections from the approved store record, not from the candidate directly.

### T120-T123 (Store, Evidence, Review, Context)

Unchanged. The approved store and runtime-ready gate remain the source of truth. Derived briefs inherit the approval status of their parent record.

### T130-T133 (ReplyPlan Schema, Planner, Policy, Eval)

Structurally unchanged. T174 may offer richer context to `ReplyPlanner` and `ReplyPlanPolicyEngine`, but the `ReplyPlan` contract and the review-only mode are not affected.

### T160-T164 (PreferencePatch Pipeline)

Unchanged. `ApprovedPatchBrief` from T164 is already a separate compact context. In the decomposition design, approved patch hints are attached to `CommunicationPolicyBrief` as an optional enrichment. This is additive: if patches exist, they complement the contact-skill-derived policy; if not, the policy brief works without them.

## 10. Non-Goals and Forbidden Scope

1. No code changes in this task (T170).
2. No ContactSkill behavior changes.
3. No data migration.
4. No deprecation or replacement claim for ContactSkill.
5. No LLM, platform, send-gate, or realtime integration.
6. No new storage format for derived briefs. Briefs are computed at assembly time, not persisted.
7. No separate approval workflow for derived briefs. They inherit parent approval.
8. No persona-clone, impersonation, or autonomous-contact behavior. The existing `ContactSkillUsageBoundary.disallowed_uses` (persona_clone, impersonation, autonomous_contact_simulation) remains enforced.

## 11. Persona-Clone / Impersonation / Autonomous-Contact Boundaries

The following boundaries are unchanged by this decomposition:

1. ContactSkill is a user-reply-assistance strategy, not a contact persona simulator. No derived brief may change this.
2. `disallowed_uses` in `ContactSkillUsageBoundary` explicitly forbids `persona_clone`, `impersonation`, and `autonomous_contact_simulation`. These prohibitions propagate to all derived briefs via `BoundaryProfileBrief.disallowed_uses`.
3. The reply planner continues to produce review-only candidate drafts. No derived brief may bypass this constraint.
4. The `ReplyPlanPolicyEngine` impersonation-risk detection (T132) continues to operate regardless of which brief structure feeds the planner.
5. No derived brief contains raw chat transcript text, real contact names, real platform IDs, or unredacted PII.

## 12. Open Questions for Later Tasks

1. **Lazy vs. materialized briefs.** This design chooses lazy projection (computed at assembly time) to avoid a new storage format. If performance profiling later shows projection is a bottleneck for a large number of approved contacts, a materialized cache with invalidation-on-review-change could be considered. This is explicitly deferred beyond T174.

2. **Cross-contact briefs.** This design is per-contact. Whether some brief fields (e.g., boundary rules that apply across all contacts) should be extracted into a global policy brief is an open question for M8 (RelationshipState) or later.

3. **Brief versioning.** Derived briefs carry `source_skill_record_id` for traceability but no independent `schema_version`. If brief shapes evolve, a version field may be needed. This is deferred until Phase 1 (T171-T172) when actual schemas are defined.

4. **PartnerPersonaBrief + RelationshipState overlap.** M8 (T190-T195) introduces a separate RelationshipState model. The relationship-state fields in PartnerPersonaBrief may eventually delegate to RelationshipState rather than duplicating them. This overlap is acknowledged and deferred to the M8 design.
