# M38 Next Iteration Scope

Status: proposed by T434 after M37 `PASS_WITH_WARNINGS`

## Purpose

M38 should add a controlled persona version draft ledger for reviewed persona
evolution patches.

The milestone should show how preview-only evolution patches can be grouped
into auditable version drafts with review outcomes, conflict checks, and
rollback references, without mutating PersonaCard, memory stores, review
stores, runtime state, or outbound surfaces.

M38 remains local, deterministic, synthetic-only, review-only, and
non-mutating.

## Product Intent

M38 advances the companion-agent direction by making persona growth feel
intentional instead of arbitrary:

- users can see a proposed persona version before anything changes;
- reviewers can compare current persona state, proposed patch set, conflicts,
  and rollback references;
- fuzzy growth hints remain low-confidence until reviewed;
- blocked clone/deception/private-source requests stay excluded;
- the system can explain why a persona version is accepted, deferred, or
  rejected;
- later production apply work has a safer local contract to build from.

## Design Principles

- A version draft is a review artifact, not a runtime mutation.
- Every draft must point back to M37 evolution patch ids and risk labels.
- Accepted/deferred/rejected outcomes must be explicit and deterministic.
- Conflicts must be visible before any apply path is considered.
- Rollback refs must be complete enough for a later executable store to use,
  but M38 must not implement that store.
- Non-execution flags remain first-class UI and payload data.

## In Scope

- Define a local `persona_version_draft_ledger` payload.
- Create deterministic synthetic version drafts from M37 evolution patch
  candidates.
- Include draft metadata:
  - draft id;
  - base persona snapshot ref;
  - source evolution preview ref;
  - included patch ids;
  - excluded patch ids;
  - risk label ids;
  - conflict notes;
  - reviewer outcome;
  - rollback refs;
  - non-execution flags.
- Add at least three draft outcomes:
  - accepted for future apply review;
  - deferred for unclear evidence;
  - rejected because of boundary or blocked-source risk.
- Render the ledger in the static demo.
- Link version draft cards into Review Workspace after static rendering is
  stable.
- Harden responsive layout for dense draft diffs and rollback refs.

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

## Payload Contract Direction

The first implementation slice should introduce
`persona_version_draft_ledger` with:

- `schema_version`, for example `m38.persona_version_draft_ledger.v1`;
- `ledger_title`;
- `source_evolution_preview_ref`;
- `base_persona_snapshot_ref`;
- `drafts`;
- `conflict_rules`;
- `review_outcome_labels`;
- `rollback_ref_index`;
- `apply_policy`;
- `non_execution_flags`.

`apply_policy` must stay preview-only and non-mutating. It must not imply that
drafts are written to PersonaCard, PersonaVersionStore, memory stores, review
stores, or runtime state.

## Draft Requirements

Each draft should include:

- stable `draft_id`;
- `draft_kind`;
- `source_patch_ids`;
- `excluded_patch_ids`;
- `risk_label_ids`;
- `before_snapshot_summary`;
- `after_version_summary`;
- `reviewer_outcome`: one of `accepted_for_future_apply_review`,
  `deferred_needs_more_evidence`, or `rejected_boundary_risk`;
- `conflict_note_ids`;
- `rollback_ref_ids`;
- `review_required: true`;
- `apply_status: preview_only`;
- `mutation_allowed: false`.

## Conflict Requirements

Conflict notes should make these risks visible:

- persona drift against the reviewed baseline;
- boundary weakening or hidden AI identity;
- weak or fuzzy evidence;
- overattachment or dependency reinforcement;
- blocked-source contamination.

Conflict records must be review metadata only.

## Review Workspace Direction

After the payload and static ledger render, Review Workspace should expose
version draft cards with:

- source surface: `persona_version_draft_ledger`;
- draft outcome;
- included and excluded patch ids;
- conflict notes;
- rollback refs;
- preview-only and non-mutating status badges.

## Browser QA Expectations

UI tasks after the payload lands should verify:

- version ledger section is visible;
- accepted/deferred/rejected draft cards render;
- conflict notes and rollback refs render;
- Review Workspace version draft cards render;
- no forbidden action controls appear;
- no horizontal overflow at the available narrow viewport;
- desktop responsiveness is covered by CSS/static tests if viewport control is
  unavailable.

## Suggested Task Sequence

1. T435: refine this M38 scope into a concrete version draft ledger payload
   task.
2. Add local `persona_version_draft_ledger` payload and contract tests.
3. Render the version draft ledger in the static demo.
4. Link version draft cards to Review Workspace.
5. Responsive/browser hardening for ledger and review cards.
6. M38 milestone review and next iteration scope.

## Review Standard

M38 should be judged on whether it makes proposed persona version changes
auditable and reversible without creating hidden drift, automatic mutation,
real-person imitation, or runtime side effects.

## T436 Implementation Entry

The first code task should be payload-only. It should add
`persona_version_draft_ledger` to the text-first demo adapter and cover it with
contract tests before any HTML, CSS, JavaScript rendering, or Review Workspace
linkage is attempted.

T436 should prove:

- source linkage to `persona_evolution_preview`;
- at least three draft outcomes;
- conflict notes for persona drift, boundary, weak evidence, overattachment,
  and blocked-source contamination;
- rollback ref index coverage;
- preview-only apply policy;
- non-execution flags with providers, private reads, store writes, automatic
  apply, outbound messaging, adapters, and media runtime disabled.
