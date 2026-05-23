# T172 Review Explained

## 1. What is this task about?

This task defines two new "brief" data schemas that will later be derived from the existing `ContactSkill` — a structured profile the system builds for each contact after reviewing chat history.

Think of `ContactSkill` as a comprehensive dossier about how you relate to someone. It contains a lot of detail: communication style, relationship state, reply strategies, boundaries, important events, and more. But when the system needs to actually *use* this information to help draft a reply, it doesn't need the full dossier — it needs focused summaries.

T171 already created the first focused summary: `PartnerPersonaBrief` ("who is this person and how do they communicate?").

T172 creates the remaining two:

- **CommunicationPolicyBrief**: "how should the system draft replies for this contact?" — carries reply strategy approaches, the user's goal, preferred reply style, stable preference hints, and approved patch hints from the feedback system.
- **BoundaryProfileBrief**: "what should the system avoid, what is sensitive, and what are the hard limits?" — carries topics to avoid, boundary rules, disallowed uses, usage notes, important event summaries, and an overall sensitivity level.

These are *schemas only* — they define the shape of the data. The actual logic to project/fill them from a `ContactSkill` will come in T173.

## 2. Implementation details

### 2.1 Goal

Define additive Pydantic models for `CommunicationPolicyBrief` and `BoundaryProfileBrief`, document their field meanings and source projections, and resolve four open design questions from earlier task reviews.

### 2.2 What changed

**`src/practical_chat_agent/core/models.py`** — 44 lines added, 0 removed. Two new models:

- `CommunicationPolicyBrief` (11 fields):
  - 4 reply-strategy approach fields (default, cold-contact, topic-opener, sensitive-topic)
  - 2 user-preference fields (user_goal, preferred_reply_style)
  - 1 stable preference hints list
  - 1 approved patch hints list (reusing `ApprovedPatchBrief` from T164)
  - `contact_id`, `evidence_refs`, `source_skill_record_id` for traceability

- `BoundaryProfileBrief` (9 fields):
  - `avoid_topics`, `boundary_rules`, `disallowed_uses`, `usage_notes`
  - `important_event_summaries` (compact strings like "Graduation (2024-06)")
  - `sensitivity_summary` (DistillationSensitivity, defaults to "low")
  - `contact_id`, `evidence_refs`, `source_skill_record_id` for traceability

No existing models were touched.

**`docs/data_contracts/contactskill_decomposition_contract.md`** — expanded from T171's 7 sections to 9 sections. Key additions:
- Section 2.3: CommunicationPolicyBrief field definitions and the rationale for why `approved_patch_hints` belongs to the policy brief.
- Section 2.4: BoundaryProfileBrief field definitions and the rationale for why `important_event_summaries` stays in the boundary brief (events can be sensitive; boundary profile carries the sensitivity signal).
- Section 3.2/3.3: Source projection tables showing exactly which `ContactSkill` sub-model fields map to each brief field.
- Section 7: The sensitivity reduction rule — `max(avoid_topics sensitivities, important_events sensitivities, parent aggregate sensitivity)`, with parent as a floor.
- Section 8: The versioning decision — derived briefs do NOT carry their own `schema_version`; versioning is inherited through `source_skill_record_id`.

**`tests/test_contactskill_policy_briefs.py`** — 31 new synthetic tests covering construction, required fields, safe defaults, patch-hint enrichment, sensitivity values, serialization, and cross-brief contract properties.

**`docs/07_handoff.md`** — added Section 72 (T172 Implementation Record).

### 2.3 Key design decisions resolved

| Review Note | Decision |
|---|---|
| T170 N01 (sensitivity reduction) | `max(avoid_topics, important_events, parent aggregate)` with parent as floor |
| T170 N03 (important_events ownership) | Stays in BoundaryProfileBrief — events can be sensitive and need sensitivity governance |
| T170 N04 (patch hints + boundary) | Patches remain in CommunicationPolicyBrief only; no new boundary-patch field |
| T171 N05 (schema_version) | No `schema_version` on derived briefs; versioning inherited via parent store record |

### 2.4 Significance for future development

With T172 complete, M6 now has all three brief schemas committed:

1. `PartnerPersonaBrief` (T171) — who is this person, how do they communicate
2. `CommunicationPolicyBrief` (T172) — how should we draft replies
3. `BoundaryProfileBrief` (T172) — what to avoid, what is sensitive

T173 can now implement the **projection service**: the logic that takes an approved `ContactSkillStoreRecord` and produces these three briefs. This is where the documented projection rules (field-by-field mappings in the contract) become running code.

T174 will then integrate these briefs into the `ChatContext` assembly, replacing the current flat `ApprovedContactSkillBrief` with structured, typed briefs when available.

The design preserves backward compatibility: `ApprovedContactSkillBrief` remains the fallback. If briefs aren't available, consumers get the old flat format. This means no existing functionality breaks.

## 3. Why this review verdict (PASS)?

The task is clean and well-executed:

- **Task goal met**: Both schemas are defined, all four reviewer notes are resolved with explicit documented decisions, and the contract covers field definitions, source projections, evidence traceability, sensitivity reduction, versioning, and non-goals.
- **No scope violations**: Changes are limited to allowed files. models.py is additive-only (44 insertions, 0 deletions). No projection service, no ChatContext integration, no ReplyPlanner changes, no ContactSkill mutation.
- **No fake implementation**: Pure Pydantic schemas with no runtime logic, no mock data, no hardcoded outputs.
- **Adequate tests**: 31 synthetic tests exercise construction, required fields, safe defaults, patch-hint enrichment, sensitivity values, serialization, and cross-brief contract invariants. Full test suite passes (241/241).
- **No documentation overclaims**: The contract explicitly lists non-goals and defers projection logic to T173.

The four non-blocking notes (N01-N04) are structural observations and follow-up reminders, not defects:

- N01: The policy brief's evidence trail is thin because upstream models lack per-area evidence — this is a structural constraint, not a design flaw.
- N02: The `sensitivity_summary` default of `"low"` will always be overwritten by T173 projection — safe as a lower bound.
- N03: `important_event_summaries` format is documented but not structurally enforced — T173 controls formatting.
- N04: `.claude/settings.json` modification follows the accepted workspace-noise pattern.

## 4. No prior worker review/explanation to supplement

The worker did not produce review or explanation documents for T172 (those are the reviewer's responsibility). The worker's summary in the handoff is accurate and matches the actual implementation.
