# ContactSkill Decomposition Contract

Task: T171, T172
Date: 2026-05-23

## 1. Purpose

This document defines the contract for three derived briefs from the T170 ContactSkill-compatible decomposition design: `PartnerPersonaBrief`, `CommunicationPolicyBrief`, and `BoundaryProfileBrief`. It is an additive, schema-only contract that does not modify, replace, or deprecate the existing `ContactSkillCandidate` or `ApprovedContactSkillBrief`.

## 2. Models

### 2.1 CommunicationStyleSnapshot

Compact, structured snapshot of a contact's communication style. Promoted from `dict[str, str]` (as sketched in the T170 design) to a named Pydantic model for type safety, self-documentation, and consistent validation with the rest of the codebase.

Fields:
- `message_length: str | None = None` — e.g. "short", "medium", "long", "mixed".
- `tone: str | None = None` — e.g. "polite", "casual", "reserved", "warm".
- `response_latency: str | None = None` — e.g. "fast", "slow", "unstable".
- `directness: str | None = None` — e.g. "low", "medium", "high".

All fields are optional because the brief may be projected from a `ContactSkillCommunicationStyle` where some dimensions are `"unknown"` or absent. The projection service (T173) will map `"unknown"` to `None` to keep the snapshot compact.

**Why a named model instead of `dict[str, str]`:**
1. The four keys (message_length, tone, response_latency, directness) are known and stable.
2. A named model enables Pydantic validation, IDE autocomplete, and schema documentation.
3. Projection from `ContactSkillCommunicationStyle` maps directly: each field is a 1:1 projection.
4. Free-form dict keys would allow typos and undefined dimensions to pass silently.

### 2.2 PartnerPersonaBrief

Who this person is, how the relationship stands, and how they communicate.

Fields:
- `contact_id: str` (required, min_length=1) — identifies the contact.
- `relationship_type: ContactRelationshipType` (required) — e.g. "friend", "colleague", "family". Projected directly from `ContactSkillCandidate.relationship_type`.
- `relationship_state_summary: str` (required, min_length=1) — compact, human-readable summary of the relationship state. Projected from `ContactSkillRelationshipState` fields by the T173 projection service.
- `communication_style_snapshot: CommunicationStyleSnapshot` (required, default=empty) — structured snapshot of communication style.
- `preferred_topics: list[str]` (default=empty) — topic strings only, projected from `ContactSkillTopicPreference.topic`. Reasons and evidence per-topic are not included in the brief.
- `emotional_pattern_labels: list[str]` (default=empty) — pattern strings only, projected from `ContactSkillPattern.pattern`.
- `evidence_refs: list[str]` (default=empty) — union of `ContactSkillRelationshipState.evidence_refs` and `ContactSkillCommunicationStyle.evidence_refs`, plus individual evidence_refs from `ContactSkillTopicPreference` and `ContactSkillPattern` entries that are projected into this brief. Top-level `ContactSkillCandidate.evidence_refs` are NOT included here; they remain accessible via the fallback aggregate.
- `source_skill_record_id: str` (required, min_length=1) — `ContactSkillStoreRecord.record_id` of the parent record. Provides traceability without carrying review metadata or approval status.

### 2.3 CommunicationPolicyBrief

How the system should draft replies for this contact.

Fields:
- `contact_id: str` (required, min_length=1) — identifies the contact.
- `default_approach: str | None = None` — projected from `ContactSkillReplyStrategy.default`.
- `cold_contact_approach: str | None = None` — projected from `ContactSkillReplyStrategy.when_contact_is_cold`.
- `topic_opener_approach: str | None = None` — projected from `ContactSkillReplyStrategy.when_contact_opens_topic`.
- `sensitive_topic_approach: str | None = None` — projected from `ContactSkillReplyStrategy.for_sensitive_topics`.
- `user_goal: str | None = None` — projected from `ContactSkillUserSidePreferences.user_goal`.
- `preferred_reply_style: str | None = None` — projected from `ContactSkillUserSidePreferences.preferred_reply_style`.
- `stable_preference_hints: list[str]` (default=empty) — pattern strings only, projected from `ContactSkillPattern.pattern` for entries in `ContactSkillCandidate.stable_preferences`.
- `approved_patch_hints: list[ApprovedPatchBrief]` (default=empty) — compact patch hints from T164 approved-patch context. Only approved, runtime-ready patches are included.
- `evidence_refs: list[str]` (default=empty) — union of evidence_refs from `stable_preferences` entries. `ContactSkillReplyStrategy` and `ContactSkillUserSidePreferences` do not carry their own evidence_refs.
- `source_skill_record_id: str` (required, min_length=1) — `ContactSkillStoreRecord.record_id` of the parent record.

**Why approved_patch_hints belongs to CommunicationPolicyBrief:**
1. Patches carry communication instructions (`behavior_instruction`) that shape how the system drafts replies.
2. Patches are already filtered to approved/runtime-ready by T164 `ApprovedPatchContextService`.
3. If a future patch type carries boundary signals (e.g. a `boundary_preference` patch with instruction "avoid mentioning X"), the boundary-aware consumer reads both `CommunicationPolicyBrief` and `BoundaryProfileBrief`. The patch instruction stays in the policy brief; the boundary brief does not duplicate it.
4. This is a conservative ownership decision: patches remain communication-policy-owned, and no new boundary-patch field is added to `BoundaryProfileBrief`. This avoids broadening T164's single-source patch contract.

### 2.4 BoundaryProfileBrief

What to avoid, what is sensitive, and what the hard limits are.

Fields:
- `contact_id: str` (required, min_length=1) — identifies the contact.
- `avoid_topics: list[str]` (default=empty) — topic strings only, projected from avoid-topics `ContactSkillTopicPreference.topic`. Reasons and evidence per-topic are not included.
- `boundary_rules: list[str]` (default=empty) — projected from `ContactSkillUserSidePreferences.boundaries`.
- `disallowed_uses: list[str]` (default=empty) — projected from `ContactSkillUsageBoundary.disallowed_uses`.
- `usage_notes: list[str]` (default=empty) — projected from `ContactSkillUsageBoundary.notes`.
- `important_event_summaries: list[str]` (default=empty) — compact event descriptions with dates, projected from `ContactSkillImportantEvent`. Each summary is a short string (e.g. "Graduation ceremony (2024-06)") rather than the full event object.
- `sensitivity_summary: DistillationSensitivity` (default="low") — highest sensitivity across boundary-relevant areas. See Section 7 for the reduction rule.
- `evidence_refs: list[str]` (default=empty) — union of evidence_refs from `avoid_topics` entries and `important_events` entries. `ContactSkillUserSidePreferences.boundaries` and `ContactSkillUsageBoundary` do not carry their own evidence_refs.
- `source_skill_record_id: str` (required, min_length=1) — `ContactSkillStoreRecord.record_id` of the parent record.

**Why important_event_summaries stays in BoundaryProfileBrief (T170 N03 resolution):**
1. Important events can be sensitive (e.g. health events, family changes, financial milestones). The boundary profile is the appropriate layer for sensitivity-aware handling.
2. The `ReplyPlanPolicyEngine` consumes the boundary brief and needs event context to enforce careful handling around sensitive life events.
3. If the planner needs event context for tone shaping, it accesses it through the boundary brief — the same brief that carries the sensitivity_summary governing how aggressively to reference those events.
4. Moving events to PartnerPersonaBrief would expose potentially sensitive information to a layer that does not carry a sensitivity signal, risking tone decisions that treat sensitive events casually.

## 3. Source Projection Rules

Derived briefs are projected from an approved `ContactSkillStoreRecord` by the T173 projection service.

### 3.1 PartnerPersonaBrief

| Brief Field | Source |
|---|---|
| `contact_id` | `record.contact_skill.contact_id` |
| `relationship_type` | `record.contact_skill.relationship_type` |
| `relationship_state_summary` | Computed from `record.contact_skill.relationship_state` fields by T173 |
| `communication_style_snapshot` | Projected from `record.contact_skill.communication_style` |
| `preferred_topics` | `[t.topic for t in record.contact_skill.preferred_topics]` |
| `emotional_pattern_labels` | `[p.pattern for p in record.contact_skill.emotional_patterns]` |
| `evidence_refs` | Union of relationship_state, communication_style, topic, and pattern evidence_refs |
| `source_skill_record_id` | `record.record_id` |

### 3.2 CommunicationPolicyBrief

| Brief Field | Source |
|---|---|
| `contact_id` | `record.contact_skill.contact_id` |
| `default_approach` | `record.contact_skill.reply_strategy.default` |
| `cold_contact_approach` | `record.contact_skill.reply_strategy.when_contact_is_cold` |
| `topic_opener_approach` | `record.contact_skill.reply_strategy.when_contact_opens_topic` |
| `sensitive_topic_approach` | `record.contact_skill.reply_strategy.for_sensitive_topics` |
| `user_goal` | `record.contact_skill.user_side_preferences.user_goal` |
| `preferred_reply_style` | `record.contact_skill.user_side_preferences.preferred_reply_style` |
| `stable_preference_hints` | `[p.pattern for p in record.contact_skill.stable_preferences]` |
| `approved_patch_hints` | From T164 `ApprovedPatchContextService` (approved, runtime-ready patches only) |
| `evidence_refs` | Union of `stable_preferences[i].evidence_refs` for each stable preference |
| `source_skill_record_id` | `record.record_id` |

### 3.3 BoundaryProfileBrief

| Brief Field | Source |
|---|---|
| `contact_id` | `record.contact_skill.contact_id` |
| `avoid_topics` | `[t.topic for t in record.contact_skill.avoid_topics]` |
| `boundary_rules` | `record.contact_skill.user_side_preferences.boundaries` |
| `disallowed_uses` | `record.contact_skill.usage_boundary.disallowed_uses` |
| `usage_notes` | `record.contact_skill.usage_boundary.notes` |
| `important_event_summaries` | Formatted from `record.contact_skill.important_events` by T173 |
| `sensitivity_summary` | Computed per Section 7 reduction rule |
| `evidence_refs` | Union of `avoid_topics[i].evidence_refs` and `important_events[i].evidence_refs` |
| `source_skill_record_id` | `record.record_id` |

## 4. Evidence and Traceability

1. Each brief carries its own `evidence_refs` list, projected from the relevant sub-models of the parent `ContactSkillCandidate`.
2. Sub-models that already have per-area evidence (`ContactSkillRelationshipState.evidence_refs`, `ContactSkillCommunicationStyle.evidence_refs`) contribute directly.
3. Sub-models without dedicated evidence fields (`ContactSkillUserSidePreferences`, `ContactSkillUsageBoundary`, `ContactSkillReplyStrategy`) contribute no evidence to their owning brief. This is structurally correct: these sub-models derive their authority from the parent record's overall evidence rather than from per-field evidence.
4. Top-level `ContactSkillCandidate.evidence_refs` are NOT projected into any single brief. They represent cross-cutting evidence and remain accessible through the fallback aggregate (`ApprovedContactSkillBrief`).
5. `source_skill_record_id` provides a single traceability pointer to the parent store record for each brief.
6. Derived briefs do not require separate evidence validation (T121). They inherit the validation status of their parent record.
7. Derived briefs are not independently approved. They inherit the approval status of their parent record.

## 5. Fallback Relationship

Derived briefs are richer optional overlays on top of the existing `ApprovedContactSkillBrief`:

1. If all derived briefs are available, consumers get structured, typed persona, policy, and boundary context.
2. If some briefs exist but not all (e.g. only PartnerPersonaBrief), the assembler uses what exists and fills gaps from the fallback aggregate.
3. If no derived briefs are available, consumers fall back to `ApprovedContactSkillBrief` which provides a flat `relationship_summary` + `strategy_hints` + `boundary_reminders`.
4. `ApprovedContactSkillBrief` remains the minimum guaranteed output of context assembly.
5. Derived briefs do not replace or deprecate `ApprovedContactSkillBrief`.

## 6. Approval Inheritance

1. Derived briefs do not carry their own `status`, `review_metadata`, or approval fields.
2. Approval is inherited from the parent `ContactSkillStoreRecord`.
3. The T173 projection service must check `record.is_runtime_ready()` before producing any brief.
4. If the parent record transitions to rejected/frozen/archived, all derived briefs become invalid and must not enter runtime context.

## 7. Sensitivity Reduction Rule (T170 N01 Resolution)

`BoundaryProfileBrief.sensitivity_summary` is computed by the T173 projection service using the following rule:

1. Collect all `sensitivity` values from boundary-relevant sub-models:
   - Each entry in `ContactSkillCandidate.avoid_topics` carries `sensitivity: DistillationSensitivity` (inherited from `DistillationClaim`).
   - Each entry in `ContactSkillCandidate.important_events` carries `sensitivity: DistillationSensitivity` (inherited from `DistillationClaim`).
2. Include the parent aggregate's top-level `ContactSkillCandidate.sensitivity` as a floor.
3. Compute the maximum: `sensitivity_summary = max(avoid_topics sensitivities, important_events sensitivities, parent aggregate sensitivity)`.
4. The ordering is `"low" < "medium" < "high"`.
5. If no avoid_topics and no important_events exist, the result is the parent aggregate sensitivity (which is always present because it is a required field on `ContactSkillCandidate`).

**Why max-of-relevant-areas plus parent floor:**
- Taking only sub-model sensitivities would produce `"low"` when there are no avoid_topics or important_events, even if the parent record is `"high"` sensitivity. The parent floor prevents under-reporting.
- Using only the parent aggregate sensitivity would ignore per-area sensitivity detail when specific boundary areas are more sensitive than the aggregate.
- The combined rule ensures the boundary brief is always at least as sensitive as the parent aggregate, and potentially more sensitive if specific boundary-relevant areas warrant it.

## 8. Derived-Brief Versioning Decision (T171 N05 Resolution)

Derived briefs do NOT carry their own `schema_version` field:

1. Versioning is inherited through `source_skill_record_id`, which points to the parent `ContactSkillStoreRecord`. The parent record carries `schema_version` (e.g. `"contact_skill_store_record_v1"`).
2. If brief shapes evolve, the parent record's version determines which projection logic applies. T173 can branch on `record.schema_version` to handle different projection rules for different parent schema versions.
3. Adding per-brief versioning would create a three-way versioning problem (3 brief schemas to version independently vs. 1 parent version).
4. This is consistent with the T171 decision to not include `schema_version` on `PartnerPersonaBrief`.

## 9. Non-Goals

1. No runtime integration (T174).
2. No projection service logic (T173).
3. No ContactSkill mutation or deprecation.
4. No storage format for briefs (lazy projection at assembly time).
5. No persona-clone, impersonation, or autonomous-contact behavior.
6. No raw chat transcript text, real contact names, or unredacted PII.
7. No new boundary-patch field on `BoundaryProfileBrief` (patches remain communication-policy-owned).
8. No auto-approve, auto-apply, or runtime injection of patch or policy semantics.
