# Local Companion Session Simulator Contract

Contract version: `local_companion_session_v1`

Owner task: T418

## Purpose

`companion_session` is a deterministic synthetic payload on
`TextFirstWebDemoState`. It lets reviewers inspect a short local companion
session that uses persona cues and reviewed memory summaries without calling a
model provider, reading private sources, writing runtime stores, applying
changes, or sending messages.

The payload is a product/demo contract. It is not a production chat runtime,
not a real chat distillation result, and not proof of delivery or media
capability.

## Top-Level Shape

Required fields:

- `schema_version`: literal `local_companion_session_v1`;
- `session_title`: non-empty string;
- `session_summary`: non-empty synthetic description;
- `persona_snapshot`: fictional persona identity and stable traits;
- `persona_cues`: list of cue records;
- `memory_recalls`: list of reviewed memory recall records;
- `safety_notes`: list of visible safety constraints;
- `turns`: ordered synthetic user/companion turn records;
- `post_turn_candidates`: review-only candidate records;
- `non_execution_flags`: explicit boundary flags.

## Persona Snapshot

`persona_snapshot` must include:

- `persona_id`;
- `display_name`;
- `ai_identity_disclosure`;
- `stable_traits`;
- `real_person_claim`: false.

The snapshot must describe a fictional/synthetic companion. It must not claim
to be a real person, deceased person, public figure, ex-partner, family member,
or indistinguishable human replacement.

## Persona Cues

Each cue must include:

- `cue_id`;
- `label`;
- `safe_summary`.

Cues are display/reference metadata only. They do not mutate a persona card and
do not authorize persona growth apply.

## Memory Recalls

Each recall must include:

- `recall_id`;
- `memory_kind`: factual, relational, procedural, or imagined;
- `truth_status`: evidence_backed, inferred, or imagined;
- `reviewed_summary`;
- `source_label`: synthetic source label only;
- `raw_source_available`: false.

Memory recalls must expose reviewed summaries only. They must not contain raw
message text, transcripts, private source paths, provider metadata, or private
chat artifacts.

## Turns

Each turn must include:

- `turn_id`;
- `speaker`: user or companion;
- `safe_text`;
- `used_memory_recall_ids`;
- `used_persona_cue_ids`;
- `safety_note_ids`;
- `review_trace`;
- `generated_by`: literal `deterministic_synthetic_fixture`.

At least one companion turn should reference a reviewed memory recall. At least
one companion turn should reference a persona cue.

## Post-Turn Candidates

Candidate kinds:

- `memory_candidate`;
- `persona_growth_patch`;
- `proactive_suggestion`;
- `life_stream_draft`.

Each candidate must include:

- `candidate_id`;
- `candidate_kind`;
- `originating_turn_id`;
- `safe_summary`;
- `review_required`: true;
- `preview_only`: true;
- `changes_state`: false;
- `automatic_apply`: false;
- `sends_messages`: false.

Candidates are review surfaces only. They must not write stores, create
PersonaVersion records, enqueue delivery, schedule outreach, or send messages.

## Non-Execution Flags

Required values:

- `local_only`: true;
- `synthetic_fixture`: true;
- `calls_provider`: false;
- `uses_private_source`: false;
- `writes_runtime_store`: false;
- `automatic_apply`: false;
- `sends_messages`: false;
- `media_runtime_enabled`: false.

## Forbidden Fields And Behavior

The payload must not include:

- raw message text, raw transcripts, private chat history, private messages, or
  private artifact paths;
- provider credentials, provider tokens, API keys, remote model invocation
  metadata, embeddings, vector search, semantic ranking, or fine-tuning hooks;
- platform recipients, send queues, scheduled delivery, webhooks, auth tokens,
  or delivery state;
- audio/image/video bytes, generated media paths, microphone/camera controls,
  ASR, TTS, voice cloning, Live2D, or media capture.

## Verification

T418 verifies the contract through:

- adapter payload tests;
- served `/demo-state.json` tests;
- focused local web demo regression tests;
- `py_compile`;
- `git diff --check`.
