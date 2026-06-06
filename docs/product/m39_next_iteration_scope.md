# M39 Next Iteration Scope

Status: proposed by T440 after M38 `PASS_WITH_WARNINGS`

## Purpose

M39 should add a consent-gated source intake manifest for future persona
distillation from user-provided material.

The milestone should show how the product can represent source type, consent,
minimization, redaction, blocked source categories, and review gates before any
real chat record is read or distilled.

M39 remains local, deterministic, synthetic-only, review-only, and
non-ingesting.

## Product Intent

M39 advances the companion-agent direction by preparing a safer path toward
real user-provided persona sources:

- users may eventually provide detailed descriptions, fuzzy seeds, or chat-log
  exports;
- the system must distinguish fictional persona shaping from real-person
  replacement or deception;
- source handling must be explicit before any extraction or model call;
- private-source material must be minimized and reviewed before use;
- blocked source categories must remain visible;
- later real distillation work should have a consent and evidence contract to
  build on.

## Design Principles

- No real private records are read in M39.
- Source manifests are review artifacts, not ingestion jobs.
- Consent state and source ownership must be explicit.
- Minimization and redaction status must be visible before extraction.
- Clone/deception/without-consent requests must be blocked before distillation.
- Non-execution flags remain first-class UI and payload data.

## In Scope

- Define a local `persona_source_intake_manifest` payload.
- Represent deterministic synthetic source candidates for:
  - detailed description;
  - fuzzy seed;
  - synthetic dialogue excerpt;
  - user-provided archive placeholder;
  - third-party private source placeholder.
- Include source metadata:
  - source id;
  - source kind;
  - declared owner;
  - consent status;
  - minimization status;
  - redaction summary;
  - extraction eligibility;
  - blocked reason ids;
  - review gate ids.
- Include source policy gates:
  - consent required;
  - private-source minimization;
  - real-person replacement blocker;
  - deception blocker;
  - sensitive data redaction required;
  - reviewer approval required.
- Render the manifest in the static demo after payload contract lands.
- Link intake manifest cards into Review Workspace after static rendering is
  stable.
- Harden responsive layout for dense source policy and redaction details.

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
`persona_source_intake_manifest` with:

- `schema_version`, for example `m39.persona_source_intake_manifest.v1`;
- `manifest_title`;
- `source_candidates`;
- `source_policy_gates`;
- `blocked_source_categories`;
- `redaction_profiles`;
- `review_required`;
- `apply_policy`;
- `non_execution_flags`.

`apply_policy` must be preview-only and non-ingesting. It must not imply source
files are read, stored, embedded, extracted, or sent to model providers.

## T442 Implementation Slice

T442 should be payload-only.

It should update the text-first web demo adapter so serialized demo state
contains a deterministic `persona_source_intake_manifest`, then cover the
contract with focused tests and `/demo-state.json` integration checks.

T442 should not render UI, edit JavaScript/CSS/HTML, read private files, add
source readers, call providers, extract traits, write stores, mutate personas,
or create runtime ingestion behavior.

The implementation should prove only the manifest shape:

- source candidates are synthetic fixtures;
- consent and ownership are explicit;
- raw source content is not retained;
- extraction eligibility is derived from safe manifest metadata;
- blocked source categories remain visible;
- redaction profiles are declared before extraction;
- review gates block extraction when failed;
- non-execution flags make the payload local-only, synthetic-only, and
  non-ingesting.

## Source Candidate Requirements

Each source candidate should include:

- stable `source_id`;
- `source_kind`;
- `fixture_label`;
- `declared_owner`;
- `consent_status`;
- `minimization_status`;
- `redaction_profile_id`;
- `safe_summary`;
- `raw_content_retained: false`;
- `extraction_eligible`;
- `blocked_reason_ids`;
- `review_gate_ids`;
- `review_required: true`.

## Policy Gate Requirements

Required gate codes:

- `explicit_consent_required`;
- `private_source_minimization_required`;
- `real_person_replacement_blocked`;
- `deception_blocked`;
- `sensitive_data_redaction_required`;
- `reviewer_approval_required`.

Each policy gate must include:

- `gate_id`;
- `gate_code`;
- `enabled: true`;
- `safe_summary`;
- `blocks_extraction_when_failed: true`.

## Review Workspace Direction

After the payload and static manifest render, Review Workspace should expose
source intake cards with:

- source surface: `persona_source_intake_manifest`;
- source kind and consent status;
- minimization and redaction summary;
- extraction eligibility;
- blocked reason ids;
- review gates;
- preview-only and non-ingesting status badges.

## Browser QA Expectations

UI tasks after the payload lands should verify:

- source intake manifest section is visible;
- source candidates and policy gates render;
- redaction profiles and blocked categories render;
- Review Workspace source intake cards render;
- no forbidden action controls appear;
- no horizontal overflow at the available narrow viewport;
- desktop responsiveness is covered by CSS/static tests if viewport control is
  unavailable.

## Suggested Task Sequence

1. T441: refine this M39 scope into a concrete source intake manifest payload
   task.
2. Add local `persona_source_intake_manifest` payload and contract tests.
3. Render the source intake manifest in the static demo.
4. Link source intake cards to Review Workspace.
5. Responsive/browser hardening for manifest and review cards.
6. M39 milestone review and next iteration scope.

## Review Standard

M39 should be judged on whether it creates a safe, explicit source-intake
contract for later real persona distillation without reading private records,
calling providers, or implying ingestion has already occurred.
