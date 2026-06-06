# M40 Next Iteration Scope

Status: proposed by T446 after M39 `PASS_WITH_WARNINGS`

## Purpose

M40 should add a local `persona_source_evidence_matrix` for future persona
distillation from consent-gated source candidates.

The milestone should show how eligible source intake records can become
reviewable evidence rows and cautious trait hypotheses while blocked or
ineligible sources remain visible as exclusions.

M40 remains local, deterministic, synthetic-only, review-only, and
non-extracting.

## Product Intent

M40 advances the companion-agent direction by preparing the bridge between
safe source intake and persona shaping:

- users may eventually provide descriptions, fuzzy seeds, or chat-log exports;
- the product needs evidence provenance before traits are proposed;
- extraction eligibility must follow source consent and minimization gates;
- weak, fuzzy, or blocked evidence must remain visible;
- real-person replacement and deception risks must block evidence use;
- later distillation should be auditable from source candidate to trait
  hypothesis.

## Design Principles

- No real private records are read in M40.
- Evidence rows are deterministic fixtures, not model extraction outputs.
- Evidence must reference source intake candidate ids.
- Ineligible source candidates must become exclusion rows, not trait evidence.
- Trait hypotheses must carry confidence, uncertainty, and review gates.
- Non-execution flags remain first-class UI and payload data.

## In Scope

- Define a local `persona_source_evidence_matrix` payload.
- Represent deterministic synthetic evidence rows for eligible M39 source
  candidates.
- Represent exclusion rows for ineligible M39 source candidates.
- Include trait hypotheses for tone, pacing, humor, boundary style, memory use,
  and growth hints.
- Include evidence quality labels:
  - strong synthetic description;
  - fuzzy seed;
  - synthetic dialogue fixture;
  - blocked archive placeholder;
  - blocked third-party private source.
- Include review gates for consent, minimization, redaction, uncertainty, and
  anti-deception.
- Render the matrix in the static demo after payload contract lands.
- Link evidence matrix cards into Review Workspace after static rendering is
  stable.
- Harden responsive layout for dense evidence ids and trait hypothesis rows.

## Out Of Scope

- Reading `private/chat_history/`, `private/distilled/`, or private artifacts.
- Ingesting real chat exports, contact lists, user-uploaded logs, screenshots,
  audio, images, video, or production user content.
- Model-provider calls, prompt execution, embeddings, vector search, semantic
  ranking, similarity scoring, fine-tuning, source readers, or real extraction.
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
`persona_source_evidence_matrix` with:

- `schema_version`, for example `m40.persona_source_evidence_matrix.v1`;
- `matrix_title`;
- `source_intake_manifest_ref`;
- `eligible_source_ids`;
- `excluded_source_refs`;
- `evidence_rows`;
- `trait_hypotheses`;
- `quality_labels`;
- `review_gate_results`;
- `review_required`;
- `apply_policy`;
- `non_execution_flags`.

`apply_policy` must be preview-only and non-extracting. It must not imply
source files are read, raw content is retained, embeddings are created, model
providers are called, traits are extracted from real content, or personas are
mutated.

## T448 Implementation Slice

T448 should be payload-only.

It should update the text-first web demo adapter so serialized demo state
contains a deterministic `persona_source_evidence_matrix`, then cover the
contract with focused tests and `/demo-state.json` integration checks.

T448 should not render UI, edit JavaScript/CSS/HTML, read private files, add
source readers, call providers, create embeddings, extract traits from real
content, write stores, mutate personas, or create runtime distillation
behavior.

The implementation should prove only the matrix shape:

- evidence rows reference M39 source intake candidate ids;
- eligible source ids produce reviewable evidence rows;
- ineligible source ids remain exclusion rows;
- trait hypotheses cite evidence row ids;
- uncertainty and quality labels remain visible;
- review gates block extraction/apply when failed;
- non-execution flags make the payload local-only, synthetic-only, and
  non-extracting.

## Suggested Task Sequence

1. T447: refine this M40 scope into a concrete evidence matrix payload task.
2. Add local `persona_source_evidence_matrix` payload and contract tests.
3. Render the evidence matrix in the static demo.
4. Link evidence matrix cards to Review Workspace.
5. Responsive/browser hardening for matrix and review cards.
6. M40 milestone review and next iteration scope.

## Review Standard

M40 should be judged on whether it creates a safe, explicit evidence matrix
contract for later persona distillation without reading private records,
calling providers, or implying extraction has already occurred.
