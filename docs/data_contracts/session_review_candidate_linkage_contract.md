# Session Review Candidate Linkage Contract

Contract version: `review_workspace_session_candidate_card_v1`

Owner task: T420

## Purpose

Session review candidate linkage projects T418 `companion_session`
`post_turn_candidates` into the local review workspace. The projection connects
the session loop to review-first governance without approving, applying,
mutating, scheduling, or sending anything.

## Review Workspace Fields

`review_workspace` may include:

- `session_candidate_cards`: list of session candidate review cards;
- a `filter_tabs` entry with `key: "session"` and a count matching the linked
  session candidates.

## Session Candidate Card Shape

Each card must include:

- `schema_version`: `review_workspace_session_candidate_card_v1`;
- `card_kind`: `session_candidate_review`;
- `title`;
- `display_label`;
- `safe_summary`;
- `filter_keys`;
- `status_badges`;
- `candidate_id`;
- `candidate_kind`;
- `originating_turn_id`;
- `source_surface`: `companion_session`;
- `review_required`: true;
- `preview_only`: true;
- `changes_state`: false;
- `automatic_apply`: false;
- `sends_messages`: false;
- `runtime_ready`: false.

## Required Candidate Coverage

At minimum, the linked surface must include:

- one `memory_candidate`;
- one `persona_growth_patch`;
- one `proactive_suggestion`.

It may include a `life_stream_draft` if the draft is clearly imagined,
review-only, and non-executing.

## Static UI Requirements

Static review workspace rendering must:

- include `session_candidate_cards` when building the review card list;
- style cards with `session-candidate-review-card`;
- show source surface, originating turn, automatic apply status, and message
  sending status;
- avoid approve/reject/apply/send controls.

## Forbidden Behavior

The linkage must not add:

- automatic apply;
- PersonaVersionStore or MemoryEventStore writes;
- review-store writes;
- source ingestion or private-data reads;
- model-provider calls;
- platform recipients, send queues, scheduled outreach, webhooks, delivery
  state, or external adapters;
- microphone, camera, ASR, TTS, voice cloning, Live2D, generated media, or
  media capture.

## Verification

T420 verifies the contract through:

- adapter payload tests for `session_candidate_cards`;
- static asset tests for the review card renderer and style hook;
- local server safety tests for dangerous enabled states;
- regression checks that existing apply audit cards remain available.
