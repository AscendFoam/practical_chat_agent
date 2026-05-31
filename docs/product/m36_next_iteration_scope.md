# M36 Next Iteration Scope

Status: refined by T423 after M35 `PASS_WITH_WARNINGS`

## Purpose

M36 starts the persona intake and distillation workbench for deep companion
customization. It must show how user-facing persona material can become
structured, reviewable trait candidates while staying local, deterministic,
synthetic-only, non-mutating, and non-deceptive.

M36 is a contract and demo milestone. It does not authorize real private chat
import, model-provider reasoning, clone generation, automatic apply, outbound
messaging, voice/avatar runtime, or generated media.

## Product Intent

M36 supports the product direction requested for a companion-agent app:

- explicit user-described persona customization;
- fuzzy persona seeds that can become more concrete over time;
- dialogue-like evidence that can inform style without exposing private logs;
- random fictional persona seeds for low-effort exploration;
- clear separation between fictional personas, inspired traits, and blocked
  real-person clone or deception requests;
- reviewable outputs that can later feed persona cards or session behavior only
  after separate apply gates.

## Design Principles

- Treat every M36 source as a synthetic fixture.
- Preserve evidence references, not raw private records.
- Make uncertainty visible through confidence bands and review statuses.
- Block clone, replacement, deception, and unauthorized real-person imitation
  before any persona synthesis.
- Keep every output preview-only until a later explicit apply milestone.
- Prefer deterministic local fixtures and tests over provider calls or hidden
  inference.

## In Scope

- Add a local `persona_distillation_workbench` payload.
- Support four synthetic input modes:
  - `detailed_description`;
  - `fuzzy_seed`;
  - `synthetic_dialogue_excerpt`;
  - `random_fictional_seed`.
- Include synthetic example inputs for all supported modes.
- Extract structured review candidates for:
  - tone;
  - pacing;
  - attachment style;
  - humor style;
  - boundary style;
  - topic affinity;
  - taboo pattern;
  - memory-use preference;
  - growth hint.
- Preserve safe evidence refs that point to synthetic input ids and safe
  summaries.
- Include blocked request records for clone/deception/real-person replacement
  requests.
- Include non-execution flags proving that the payload is local-only,
  synthetic-only, no-provider, no-private-source, no-runtime-store,
  no-automatic-apply, no-outbound, and no-media-runtime.
- Add static/demo UI and review linkage only after the payload contract is
  stable.

## Out Of Scope

- Reading `private/chat_history/`, `private/distilled/`, or private artifacts.
- Ingesting real chat exports, contact lists, user-uploaded logs, screenshots,
  audio, images, video, or production user content.
- Model-provider calls, prompt execution, remote inference, embeddings, vector
  search, semantic ranking, similarity scoring, fine-tuning, or source readers.
- Creating an unauthorized clone of a real person, deceased person, public
  figure, ex-partner, family member, or indistinguishable human replacement.
- PersonaCard mutation, PersonaVersionStore writes, MemoryEventStore writes,
  review-store writes, runtime store writes, or automatic apply.
- Platform adapters, webhooks, queues, tokens, recipient ids, delivery state,
  scheduling, automatic outreach, or outbound messaging.
- Microphone, camera, ASR, TTS, voice cloning, Live2D, generated audio,
  generated image, generated video, or media capture.
- Payment processing, production pricing claims, legal advice, app-store
  approval, launch approval, clinical claims, compliance completion, regulator
  acceptance, or user-study validation.

## Payload Contract

The first implementation-facing slice must add a
`persona_distillation_workbench` payload to the text-first demo state. The
payload should include:

- `schema_version`;
- `workbench_title`;
- `review_required`;
- `apply_policy`;
- `input_modes`;
- `synthetic_inputs`;
- `evidence_refs`;
- `extracted_trait_candidates`;
- `blocked_requests`;
- `safety_gates`;
- `non_execution_flags`.

`schema_version` should identify the M36 contract, for example
`m36.persona_distillation_workbench.v1`.

`apply_policy` must be preview-only and non-mutating. It must not imply that
trait candidates are written to PersonaCard, memory stores, review stores, or
runtime state.

## Input Mode Requirements

Each `input_modes` entry should include:

- stable `mode_id`;
- user-facing `label`;
- `description`;
- `source_policy`;
- `accepted_fixture_kind`;
- `requires_review` set to true;
- `private_source_allowed` set to false.

Required modes:

- `detailed_description`: a direct fictional persona description supplied by
  the user.
- `fuzzy_seed`: a vague or partial preference that remains tentative.
- `synthetic_dialogue_excerpt`: a short invented exchange used only as
  style-like evidence.
- `random_fictional_seed`: a deterministic fictional starter persona.

## Synthetic Input Requirements

Each `synthetic_inputs` entry should include:

- stable `input_id`;
- `mode_id`;
- `fixture_label`;
- `safe_summary`;
- `detail_level`;
- `contains_private_content` set to false;
- `real_person_reference` set to false unless the input exists only to show a
  blocked request;
- `raw_content_retained` set to false.

Raw synthetic snippets may be short and generic, but tests should not require
private or production content. Real private chat text must never be introduced
as an M36 fixture.

## Evidence Requirements

Each `evidence_refs` entry should include:

- stable `evidence_id`;
- `source_input_id`;
- `source_mode_id`;
- `source_kind` set to `synthetic_fixture`;
- `safe_summary`;
- `raw_private_content_included` set to false.

Trait candidates may reference evidence ids, but they must not embed private
raw transcripts, recipient names, contact ids, phone numbers, handles, or
source file paths.

## Trait Candidate Requirements

Each `extracted_trait_candidates` entry should include:

- stable `trait_id`;
- `category`;
- `candidate_value`;
- `confidence_band` from `low`, `medium`, or `high`;
- `evidence_ref_ids`;
- `safe_summary`;
- `review_status` set to `needs_review`;
- `apply_status` set to `preview_only`;
- `mutation_allowed` set to false.

The initial payload should include at least one candidate for every required
trait category in the In Scope section. Fuzzy or dialogue-like evidence should
use lower confidence when the candidate is tentative.

## Blocked Request Requirements

Each `blocked_requests` entry should include:

- stable `blocked_request_id`;
- `request_type`;
- `risk_reason`;
- `safe_summary`;
- `user_facing_explanation`;
- `source_mode_id`;
- `status` set to `blocked`;
- `raw_private_content_included` set to false;
- `mutation_allowed` set to false.

The initial payload should include blocked examples for:

- real-person clone or replacement;
- deception or impersonation;
- private chat import without consent and source-handling gates.

## Safety Gates

The payload should expose explicit safety gates so the UI and review workspace
can show why a candidate is preview-only:

- `synthetic_only_gate`;
- `clone_deception_blocker`;
- `private_source_blocker`;
- `human_review_gate`;
- `non_mutation_gate`;
- `outbound_blocker`.

Each gate should include a stable id, enabled status, short label, and safe
summary.

## Non-Execution Flags

`non_execution_flags` must include deterministic booleans:

- `local_only: true`;
- `synthetic_fixture: true`;
- `uses_model_provider: false`;
- `reads_private_sources: false`;
- `writes_runtime_store: false`;
- `automatic_apply: false`;
- `sends_messages: false`;
- `uses_platform_adapter: false`;
- `uses_media_runtime: false`;

Tests should fail if any risky execution flag is missing or set to an unsafe
state.

## Later UI Expectations

After the payload contract lands, the static demo should render:

- a workbench section for synthetic inputs and supported modes;
- trait candidate cards grouped by category;
- safe evidence summaries linked by evidence ids;
- blocked request cards with user-facing explanations;
- non-execution badges for local-only, synthetic-only, no-provider,
  no-private-source, no-automatic-apply, no-outbound, and no-media-runtime;
- clear preview-only language without action controls that would apply,
  schedule, send, clone, upload, import, record, or generate media.

## Browser QA Expectations

UI tasks after T424 should verify the workbench through the in-app Browser when
a static page or local server is available:

- workbench section is visible;
- all four input modes are visible;
- trait candidates and blocked requests render;
- no forbidden action controls appear;
- no horizontal overflow at the available narrow viewport;
- desktop responsiveness is covered by CSS/static tests if viewport control is
  unavailable.

## Expected User Value

M36 should make the demo more credible for deep customization:

- reviewers can see how a detailed description becomes structured traits;
- reviewers can see how vague settings remain tentative and reviewable;
- reviewers can see how dialogue-like evidence can inform style without
  exposing private logs;
- reviewers can see random fictional persona seeds for fast exploration;
- reviewers can see clone/deception boundaries trigger blocking before persona
  synthesis.

## Suggested Task Sequence

1. T423: refine this scope into concrete persona intake/distillation payload
   and task requirements.
2. T424: add local persona distillation workbench payload and contract tests.
3. T425: render the workbench in the static demo.
4. T426: link workbench trait candidates to review workspace surfaces.
5. T427: responsive/browser hardening for the workbench.
6. T428: M36 milestone review and next iteration scope.

## Review Standard

M36 should be judged on whether it safely advances deep persona customization
and distillation while keeping every risky operation synthetic, local-only,
review-required, non-mutating, and non-deceptive.
