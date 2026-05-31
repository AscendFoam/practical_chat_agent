# M36 Next Iteration Scope

Status: opened by T422 after M35 `PASS_WITH_WARNINGS`

## Purpose

M36 should begin the persona intake and distillation workbench needed for deep
customization. The goal is to turn user-provided persona descriptions and safe
synthetic dialogue excerpts into structured, reviewable persona traits without
calling model providers, reading private chat history, or creating deceptive
real-person replicas.

This milestone should build the safe local contract layer before any real chat
import or model reasoning is considered.

## Product Intent

M36 should support the product direction requested for a companion-agent app:

- explicit user-described persona customization;
- fuzzy persona seeds that can become more concrete over time;
- synthetic dialogue-style evidence that can be distilled into traits;
- clear separation between fictional personas, inspired traits, and blocked
  real-person clone requests;
- reviewable outputs that can later feed persona cards or session behavior only
  after separate apply gates.

## In Scope

- Define a local persona intake/distillation workbench payload.
- Support synthetic input modes:
  - detailed persona description;
  - fuzzy persona seed;
  - synthetic dialogue excerpt;
  - random fictional persona seed.
- Extract structured review candidates such as tone, pacing, attachment style,
  humor style, boundaries, topics, taboo patterns, memory-use preferences, and
  growth hints.
- Preserve safe evidence references without exposing raw private chat logs.
- Mark clone/deception/real-person replacement requests as blocked.
- Add non-execution flags: local-only, synthetic fixture, no provider, no
  private source, no runtime store write, no automatic apply, no outbound
  messaging, no media runtime.
- Add static/demo review surfaces only after the payload contract is stable.

## Out Of Scope

- Reading `private/chat_history/`, `private/distilled/`, or private artifacts.
- Ingesting real chat exports, contact lists, user-uploaded logs, screenshots,
  audio, images, or video.
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
- Payment processing, production pricing, legal advice, app-store approval,
  launch approval, clinical claims, compliance completion, or regulator
  acceptance.

## Workbench Requirements

The first implementation-facing slice should introduce a
`persona_distillation_workbench` payload with:

- `schema_version`;
- `workbench_title`;
- `input_modes`;
- `synthetic_inputs`;
- `extracted_trait_candidates`;
- `blocked_requests`;
- `evidence_refs`;
- `review_required`;
- `non_execution_flags`.

Trait candidates should preserve:

- trait id;
- trait category;
- candidate value;
- confidence band;
- evidence ref ids;
- safe summary;
- review status;
- apply status set to preview-only/non-mutating.

Blocked requests should preserve:

- blocked request id;
- risk reason;
- safe summary;
- user-facing explanation;
- no raw private evidence.

## Expected User Value

M36 should make the demo more credible for deep customization:

- reviewers can see how a detailed description becomes structured traits;
- reviewers can see how vague settings remain tentative and reviewable;
- reviewers can see how dialogue-like evidence can inform style without
  exposing private logs;
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
