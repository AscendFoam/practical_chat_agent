# M37 Next Iteration Scope

Status: refined by T429 after M36 `PASS_WITH_WARNINGS`

## Purpose

M37 turns reviewed persona workbench candidates into controlled persona
evolution previews.

The milestone should demonstrate how a companion persona can change over time
through dry-run patch proposals, risk labels, and rollback notes without
writing PersonaCard, memory stores, review stores, runtime state, or outbound
surfaces.

M37 is still local, deterministic, synthetic-only, preview-only, and
non-mutating.

## Product Intent

M37 supports the requested companion-agent direction:

- personas should be deeply customizable;
- fuzzy or dialogue-like evidence should become clearer over time;
- the companion should be able to evolve, but not drift silently;
- users and reviewers should see what would change before anything is applied;
- real-person clone and deception boundaries must remain visible;
- persona growth should feel intentional, auditable, and reversible.

## Design Principles

- Patch proposals must be derived only from reviewed synthetic workbench trait
  candidates.
- Blocked clone/deception/private-import records must never become patch
  proposals.
- Every change must expose before summary, after summary, evidence refs, risk
  labels, and rollback notes.
- Risk labels must make persona drift and boundary weakening visible.
- Every output remains preview-only until a later explicit apply milestone.

## In Scope

- Define a local `persona_evolution_preview` payload.
- Use M36 workbench trait candidates as synthetic source inputs.
- Create preview-only persona patch proposals for:
  - tone;
  - pacing;
  - humor style;
  - boundary style;
  - memory-use preference;
  - growth hints.
- Include before/after summaries, changed field paths, confidence bands,
  evidence refs, risk labels, and rollback notes.
- Include blocked-source exclusion records proving that blocked workbench
  requests did not become patches.
- Preserve review-only and non-mutating flags.
- Render the evolution preview in the static demo after the payload contract
  lands.
- Link evolution preview cards into the Review Workspace only after static
  rendering is stable.

## Out Of Scope

- Reading `private/chat_history/`, `private/distilled/`, or private artifacts.
- Ingesting real chat exports, contact lists, user-uploaded logs, screenshots,
  audio, images, video, or production user content.
- Model-provider calls, prompt execution, embeddings, vector search, semantic
  ranking, similarity scoring, fine-tuning, or source readers.
- PersonaCard mutation, PersonaVersionStore writes, MemoryEventStore writes,
  review-store writes, runtime store writes, local databases, or automatic
  apply.
- Platform adapters, webhooks, queues, tokens, recipient ids, delivery state,
  scheduling, automatic outreach, or outbound messaging.
- Microphone, camera, ASR, TTS, voice cloning, Live2D, generated audio,
  generated image, generated video, or media capture.
- Payment processing, production pricing claims, legal advice, app-store
  approval, launch approval, clinical claims, compliance completion, regulator
  acceptance, or user-study validation.

## Payload Contract

The first implementation slice should introduce a
`persona_evolution_preview` payload with:

- `schema_version`;
- `preview_title`;
- `source_workbench_ref`;
- `source_trait_candidate_ids`;
- `persona_snapshot_before`;
- `proposed_patch_candidates`;
- `blocked_source_exclusions`;
- `risk_labels`;
- `rollback_notes`;
- `review_required`;
- `apply_policy`;
- `non_execution_flags`.

`schema_version` should identify the M37 contract, for example
`m37.persona_evolution_preview.v1`.

`apply_policy` must be preview-only and non-mutating. It must not imply that
patch candidates are written to PersonaCard, PersonaVersionStore, memory
stores, review stores, or runtime state.

## Persona Snapshot Requirements

`persona_snapshot_before` should include:

- stable synthetic persona id;
- display name;
- AI identity disclosure;
- current trait summaries;
- current boundary summary;
- current memory-use summary;
- source label set to synthetic fixture;
- `real_person_claim: false`;
- `runtime_state_ref: none`.

## Patch Candidate Requirements

Each `proposed_patch_candidates` entry should include:

- stable `patch_id`;
- `patch_kind`;
- `source_trait_candidate_ids`;
- `changed_field_path`;
- `before_summary`;
- `after_summary`;
- `rationale_summary`;
- `confidence_band`;
- `evidence_ref_ids`;
- `risk_label_ids`;
- `rollback_note_ids`;
- `review_status: needs_review`;
- `apply_status: preview_only`;
- `mutation_allowed: false`;

The initial payload should include at least six patch candidates covering:

- `style.tone`;
- `style.pacing`;
- `style.humor`;
- `relationship.boundary_style`;
- `memory.use_preference`;
- `growth.short_term_hint`.

## Risk Label Requirements

Each `risk_labels` entry should include:

- stable `risk_label_id`;
- `risk_code`;
- severity from `low`, `medium`, or `high`;
- safe summary;
- mitigation summary;
- `blocks_auto_apply: true`.

Required risk codes:

- `persona_drift`;
- `overattachment_risk`;
- `unclear_evidence`;
- `boundary_weakening`;
- `blocked_source_excluded`.

## Rollback Requirements

Each `rollback_notes` entry should include:

- stable `rollback_note_id`;
- target patch ids;
- prior summary;
- rollback summary;
- required reviewer action;
- `runtime_rollback_ready: false`.

Rollback notes are preview metadata only. They are not executable rollback
records.

## Blocked Source Exclusion Requirements

`blocked_source_exclusions` should show that M36 blocked request ids were
reviewed but excluded from patch generation.

Each exclusion should include:

- blocked request id;
- request type;
- exclusion reason;
- safe summary;
- `excluded_from_patch_generation: true`;
- `mutation_allowed: false`.

## Non-Execution Flags

`non_execution_flags` must include deterministic booleans:

- `local_only: true`;
- `synthetic_fixture: true`;
- `uses_model_provider: false`;
- `reads_private_sources: false`;
- `writes_persona_store: false`;
- `writes_memory_store: false`;
- `writes_review_store: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `uses_platform_adapter: false`;
- `uses_media_runtime: false`.

Tests should fail if any risky execution flag is missing or set to an unsafe
state.

## Later UI Expectations

After the payload contract lands, the static demo should render:

- persona snapshot before;
- patch candidate cards;
- before/after summaries;
- changed field paths;
- risk labels and mitigations;
- rollback notes;
- blocked-source exclusions;
- non-execution badges.

The UI must not render action controls that imply apply, commit, mutate,
clone, import, upload, record, connect, send, publish, media generation, or
runtime enablement.

## Browser QA Expectations

UI tasks after T430 should verify:

- evolution preview section is visible;
- patch candidate cards render;
- risk labels and rollback notes render;
- blocked-source exclusions render;
- no forbidden action controls appear;
- no horizontal overflow at the available narrow viewport;
- desktop responsiveness is covered by CSS/static tests if viewport control is
  unavailable.

## Suggested Task Sequence

1. T429: refine this M37 scope into a concrete persona evolution preview
   payload task.
2. T430: add local persona evolution preview payload and contract tests.
3. T431: render the evolution preview in the static demo.
4. T432: link evolution preview cards to Review Workspace.
5. T433: responsive/browser hardening for evolution preview.
6. T434: M37 milestone review and next iteration scope.

## Review Standard

M37 should be judged on whether it makes persona growth visible and reviewable
without creating hidden drift, automatic mutation, real-person imitation, or
runtime side effects.
