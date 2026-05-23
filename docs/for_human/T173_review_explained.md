# T173 Review Explained

## 1. What is this task about?

T171 and T172 defined the *shapes* of three focused "brief" schemas that can be derived from a `ContactSkill`:

- `PartnerPersonaBrief` (T171) — who is this person and how do they communicate
- `CommunicationPolicyBrief` (T172) — how should the system draft replies
- `BoundaryProfileBrief` (T172) — what to avoid, what is sensitive

But those tasks only created empty containers — Pydantic models with fields and defaults. They did not include any logic to actually *fill* those containers from real data.

T173 is the task that builds the **projection service**: the code that takes an approved `ContactSkillStoreRecord` (the full, reviewed dossier about a contact) and deterministically produces all three briefs from it. Think of it as a lens that focuses the full dossier into three sharp, purpose-specific summaries — one for understanding the person, one for guiding replies, and one for enforcing boundaries.

Key constraint: the projection must be **lazy** and **pure**. It doesn't store the briefs anywhere. Every time the system needs them, it re-derives them from the parent record. Same input always produces the same output. No disk writes, no LLM calls, no mutations.

## 2. Implementation details

### 2.1 Goal

Implement a `ContactSkillProjectionService` that takes a runtime-ready `ContactSkillStoreRecord` and produces a `ContactSkillProjectionResult` containing all three briefs. Non-runtime-ready records (candidate, rejected, frozen, archived, or approved-but-unreviewed) are excluded — they return a result with empty briefs.

### 2.2 What changed

**`src/practical_chat_agent/services/contact_skill.py`** — 182 lines added, 0 removed.

New code added at the end of the file (after `ContactSkillStoreReviewService`):

- `ContactSkillProjectionResult` — a frozen dataclass holding `record_id`, `contact_id`, `runtime_ready`, and three optional briefs (`persona`, `policy`, `boundary`).
- `ContactSkillProjectionService` — a stateless service with one public method:
  - `project_all(record, approved_patch_hints=None)` — gates on `is_runtime_ready()`, then delegates to three private projection methods.
- Four module-level helper functions:
  - `_build_relationship_state_summary(state)` — formats the five relationship dimensions into a compact string like `"active_exchange, closeness=0.72, trust=0.65, freq=high, initiative=balanced"`.
  - `_project_communication_style(style)` — converts `"unknown"` values to `None` for the compact `CommunicationStyleSnapshot`.
  - `_format_event_summaries(events)` — formats events as `"Event (date)"` or `"Event"` if no date.
  - `_max_sensitivity(values, default)` — picks the highest sensitivity level from a list, using the ordering `"low" < "medium" < "high"`.

No existing code in the file was modified.

**`tests/test_contactskill_projection.py`** — new file, 47 synthetic tests in 13 categories. All fixtures are synthetic with no real data.

**`docs/07_handoff.md`** — added Section 74 (T173 Implementation Record), renumbered old Section 74 to Section 75.

### 2.3 How projection works

The projection is a straightforward field-by-field mapping, following the contract's source projection tables (Sections 3.1–3.3):

**PartnerPersonaBrief** is built from:
- Direct fields: `contact_id`, `relationship_type`
- Computed: `relationship_state_summary` (formatted from 5 relationship-state dimensions)
- Converted: `communication_style_snapshot` (4 style dimensions with `"unknown"` → `None`)
- Extracted: `preferred_topics` (topic strings), `emotional_pattern_labels` (pattern strings)
- Collected: `evidence_refs` (union of relationship_state + communication_style + topic + pattern refs, deduplicated)

**CommunicationPolicyBrief** is built from:
- Reply strategy: 4 approach fields projected from `ContactSkillReplyStrategy`
- User preferences: `user_goal`, `preferred_reply_style` from `ContactSkillUserSidePreferences`
- Stable preferences: pattern strings from `ContactSkillPattern` entries
- Patch hints: passed through from the optional `approved_patch_hints` parameter (empty by default — T174 will wire the T164 patch loading)
- Evidence: only from `stable_preferences` entries (deliberately thin — reply strategy and user preferences have no evidence fields upstream)

**BoundaryProfileBrief** is built from:
- Topics to avoid: topic strings from avoid-topic entries
- Rules: from `user_side_preferences.boundaries`
- Disallowed uses and notes: from `usage_boundary`
- Important events: formatted summaries from `ContactSkillImportantEvent`
- Sensitivity: computed as `max(avoid_topics sensitivities, important_events sensitivities, parent aggregate sensitivity)` — the parent aggregate always acts as a floor
- Evidence: union of avoid_topics and important_events refs

### 2.4 Key design decisions

1. **Runtime-ready gating**: Uses `record.is_runtime_ready()` which checks status=approved + reviewed_by_human + last_decision=approved. Non-ready records get a result with `runtime_ready=False` and all briefs as `None`.

2. **Thin policy evidence**: `CommunicationPolicyBrief.evidence_refs` draws only from `stable_preferences`. This is structurally correct — `ContactSkillReplyStrategy` and `ContactSkillUserSidePreferences` don't carry evidence fields. The projection does not invent synthetic evidence.

3. **Sensitivity computation**: The `max` rule with parent floor ensures the boundary brief is always at least as sensitive as the parent record, and more sensitive if specific boundary areas warrant it.

4. **Patch passthrough**: `approved_patch_hints` is an optional parameter. The projection service doesn't load patches itself — T174 will connect the T164 `ApprovedPatchContextService` to provide them.

5. **Deterministic output**: Same `ContactSkillStoreRecord` always produces the same briefs. No randomness, no time-dependence, no external state.

### 2.5 Significance for future development

With T173 complete, M6 now has a working projection pipeline:

1. T170 defined the decomposition design
2. T171 defined the `PartnerPersonaBrief` schema
3. T172 defined the `CommunicationPolicyBrief` and `BoundaryProfileBrief` schemas
4. T173 implements the projection service that fills all three schemas from real data

T174 can now integrate these briefs into the `ChatContext` assembly. When the system prepares context for reply planning, it will:

1. Load the approved `ContactSkillStoreRecord` for the relevant contact
2. Call `ContactSkillProjectionService.project_all()` to get the three briefs
3. Load T164 approved patches and pass them through
4. Assemble the typed briefs into the `ChatContext` alongside memory facts and recent conversation

The fallback remains intact: if briefs aren't available (e.g. the record isn't runtime-ready), the system falls back to the existing `ApprovedContactSkillBrief` flat format. No existing functionality breaks.

## 3. Why this review verdict (PASS)?

The task is clean, well-scoped, and thoroughly tested:

- **Task goal met**: The projection service produces all three briefs from approved store records, gates on `is_runtime_ready()`, preserves evidence boundaries, computes sensitivity explicitly, and formats event summaries deterministically.
- **No scope violations**: Changes are limited to allowed files. `contact_skill.py` is additive-only (182 insertions, 0 deletions). `models.py` was not touched. No ChatContext integration, no ReplyPlanner changes, no storage, no CLI commands, no platform work.
- **No fake implementation**: All projection logic is real — field-by-field mappings, sensitivity computation, evidence union, format conversion. No mocks, no stubs, no hardcoded outputs.
- **Adequate tests**: 47 synthetic tests cover all required categories: projection success, non-runtime-ready exclusion (5 status variants), traceability, unknown-to-None conversion, relationship state summary, thin policy evidence, sensitivity computation (including parent floor), event formatting, policy/boundary field mapping, patch passthrough, evidence deduplication, and determinism. Full suite passes (288/288, zero regressions).
- **Contract compliance**: Every projection rule matches the contract's source tables. Top-level evidence is correctly excluded from all briefs. Sensitivity reduction matches Section 7. Patch ownership stays in CommunicationPolicyBrief only.
- **No documentation overclaims**: The handoff accurately describes what was implemented and what T174 must do next.

The four non-blocking notes (N01–N04) are minor observations:

- N01: `.claude/settings.json` follows the accepted workspace-noise pattern.
- N02: A few persona-brief fields (`relationship_type`, `preferred_topics`, `emotional_pattern_labels`) lack dedicated single-field projection tests. The projections are trivial and implicitly covered.
- N03: `_max_sensitivity`'s `default` parameter is unreachable dead code (the parent sensitivity is always in the list). Harmless.
- N04: `relationship_state_summary` format is a T173 convention, not a contract guarantee. M8 may replace it.

## 4. No prior worker review/explanation to supplement

The worker did not produce review or explanation documents for T173 (those are the reviewer's responsibility). The worker's summary in the handoff is accurate and matches the actual implementation.
