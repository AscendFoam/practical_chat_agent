# M35 Next Iteration Scope

Status: opened by T416 after M34 `PASS_WITH_WARNINGS`

## Purpose

M35 should move the companion demo from a static product-review surface toward
an inspectable local interaction loop. The goal is to show how a synthetic
companion can respond across a short session while carrying persona, memory,
review, proactive, life-stream, and trust controls through one coherent
experience.

This milestone should still avoid production runtime behavior. M35 should be a
deterministic local simulator over synthetic fixtures, not a provider-backed
chatbot, platform sender, real chat distiller, voice/avatar feature, or media
generation workflow.

## Product Intent

M35 should make the demo feel closer to the target user experience while
preserving explicit boundaries:

- the companion remains clearly labeled as AI and fictional where applicable;
- chat turns should show continuity from reviewed memory and persona state;
- post-turn changes should create reviewable memory/persona candidates rather
  than silently mutating runtime state;
- proactive suggestions should appear as consented review candidates, not sent
  messages;
- imagined life-stream content should remain labeled and separated from real
  claims;
- voice/avatar should stay locked or represented only as non-executing review
  boundaries;
- commercial notes should remain tied to user control, privacy, and review
  tooling rather than dependency pressure.

## In Scope

- Define a local synthetic companion session model or payload that captures a
  small sequence of user turns, companion draft replies, memory recalls,
  persona cues, review gates, and resulting candidates.
- Render the session in the local web demo as an operational review surface,
  not a marketing landing page.
- Show at least one continuity moment where a reply cites reviewed memory
  without exposing raw private logs.
- Show at least one safe persona adaptation candidate produced after the
  session, with review required before apply.
- Show at least one proactive suggestion candidate that is not sent and remains
  review-gated.
- Keep life-stream and voice/avatar surfaces labeled, locked, or non-executing.
- Add tests that enforce synthetic/local-only payloads and absence of
  provider/outbound/media/private-data surfaces.
- Continue Browser QA for meaningful UI changes.

## Implementation Slicing

M35 should split payload and UI work. The first code-facing task should add
only the deterministic session payload and tests. A follow-up task should render
that payload in the static web demo after the contract is stable.

This split is intentional: the session loop is the first M35 surface that
resembles an actual companion interaction, so the contract should prove the
non-execution and synthetic-only boundaries before UI polish adds more display
surface.

## Out Of Scope

- Reading `private/chat_history/`, `private/distilled/`, or private artifacts.
- Model-provider calls, prompt execution, remote inference, embeddings, vector
  search, semantic ranking, similarity scoring, or fine-tuning.
- Real source ingestion from chat logs or platform exports.
- PersonaCard synthesis from real user data.
- Runtime store mutation, automatic apply, or hidden persona/memory drift.
- Real platform adapters, webhooks, queues, tokens, recipient ids, delivery
  state, scheduling, automatic outreach, or outbound messaging.
- Microphone, camera, ASR, TTS, voice cloning, Live2D, generated audio,
  generated image, generated video, or media capture.
- Payment processing, production pricing, legal advice, app-store approval,
  launch approval, clinical claims, compliance completion, or regulator
  acceptance.

## Companion Session Requirements

The first implementation-facing slice should introduce a session spine with
the key `companion_session` on `TextFirstWebDemoState`.

Required top-level fields:

- `schema_version`: `local_companion_session_v1`;
- `session_title`: reviewer-facing title;
- `session_summary`: concise explanation of the synthetic scenario;
- `persona_snapshot`: fictional persona identity and stable traits used in the
  session;
- `turns`: ordered user/companion turns with safe synthetic text;
- `persona_cues`: current persona traits used in the replies;
- `memory_recalls`: reviewed memory summaries referenced by the replies;
- `safety_notes`: visible constraints that shaped the session;
- `post_turn_candidates`: memory/persona/proactive/life-stream candidates
  generated for review after the session;
- `non_execution_flags`: explicit local-only flags.

Required turn fields:

- `turn_id`;
- `speaker`: `user` or `companion`;
- `safe_text`;
- `used_memory_recall_ids`;
- `used_persona_cue_ids`;
- `safety_note_ids`;
- `review_trace`;
- `generated_by`: `deterministic_synthetic_fixture`.

Required memory recall fields:

- `recall_id`;
- `memory_kind`: factual, relational, procedural, or imagined;
- `truth_status`;
- `reviewed_summary`;
- `source_label`: synthetic source label only;
- `raw_source_available`: always false.

Required post-turn candidate fields:

- `candidate_id`;
- `candidate_kind`: memory_candidate, persona_growth_patch,
  proactive_suggestion, or life_stream_draft;
- `originating_turn_id`;
- `safe_summary`;
- `review_required`: always true;
- `preview_only`: always true;
- `changes_state`: always false;
- `automatic_apply`: always false;
- `sends_messages`: always false.

Required non-execution flags:

- `local_only`: always true;
- `synthetic_fixture`: always true;
- `calls_provider`: always false;
- `uses_private_source`: always false;
- `writes_runtime_store`: always false;
- `automatic_apply`: always false;
- `sends_messages`: always false;
- `media_runtime_enabled`: always false.

## Static UI Requirements

The session loop UI should be implemented after the payload task. It should make
it easy to scan the session as a product experience:

- show what the user said and how the companion responded;
- show which memory/persona cues shaped each reply;
- show visible safety notes for constrained turns;
- show post-session candidates as review cards or linked review summaries;
- keep proactive suggestions visibly unsent;
- keep life-stream drafts labeled as imagined;
- keep voice/avatar represented only as locked or non-executing boundaries;
- avoid action buttons for sending, scheduling, provider calls, platform
  connection, media generation, or automatic apply.

## Browser QA Expectations

Any M35 task that changes static HTML, JS, or CSS should run Browser QA through
a localhost preview after tests pass. The check should verify:

- the session loop is visible and readable;
- text wraps without horizontal overflow on the tested viewport;
- review candidates remain visible as non-executing surfaces;
- no provider, outbound, scheduling, platform, voice/avatar runtime, or media
  controls appear.

Payload-only tasks do not need Browser QA unless they also touch static assets.

## Expected User Value

M35 should help reviewers judge whether the product direction can support a
believable companion experience:

- a user can see continuity without hidden raw-log exposure;
- a user can see persona adaptation without uncontrolled drift;
- a user can see proactive ideas without unwanted outreach;
- a user can see how trust and monetization constraints remain present during
  the interaction, not only in a separate policy panel.

## Suggested Task Sequence

1. T417: refine this next-iteration scope into concrete local session payload
   and UI requirements.
2. T418: add the local companion session simulator payload and contract tests.
3. T419: render the session loop in the static web demo.
4. T420: add post-session review candidate linkage and static safety checks.
5. T421: run responsive/browser hardening for the session loop.
6. T422: run M35 milestone review and open the next iteration.

## Review Standard

M35 should be judged on whether it creates a more believable local companion
experience while keeping every risky operation review-gated, synthetic,
local-only, and non-executing.
