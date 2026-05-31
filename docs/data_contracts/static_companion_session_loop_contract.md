# Static Companion Session Loop Contract

Contract version: `static_companion_session_loop_v1`

Owner task: T419

## Purpose

The static companion session loop renders the T418 `companion_session` payload
in the local text-first web demo. It is an operational review surface for a
deterministic synthetic session, not a production chat runtime.

The UI must help reviewers inspect:

- user and companion turns;
- reviewed memory recalls;
- persona cues;
- safety notes;
- post-turn review candidates;
- explicit non-execution status.

## Static HTML Hooks

Required section:

- `#companion-session` with `aria-label="Companion session loop"`.

Required child hooks:

- `#session-title`;
- `#session-schema`;
- `#session-summary`;
- `#session-turn-list`;
- `#session-memory-list`;
- `#session-persona-cue-list`;
- `#session-safety-list`;
- `#session-candidate-list`;
- `#session-non-execution`.

## JavaScript Rendering

Static JS must:

- include a safe fallback `companion_session` fixture;
- render adapter-backed `companion_session` when the local server embeds or
  serves it;
- use `drawCompanionSession` as the main renderer;
- render turns through a helper such as `appendSessionTurn`;
- show non-execution status from `non_execution_flags`;
- avoid network calls, model calls, platform calls, action controls, automatic
  apply, and outbound behavior.

## CSS Requirements

Required layout classes:

- `.companion-session`;
- `.session-layout`;
- `.session-context`;
- `.session-turn-list`;
- `.session-turn-head`;
- `.session-turn-text`;
- `.session-chip-row`;
- `.session-safety-list`;
- `.session-candidate-grid`.

Mobile CSS must keep the session loop single-column and readable on narrow
viewports.

## Forbidden Behavior

The static surface must not add:

- controls or action hooks for sending, scheduling, provider calls, platform
  connection, media generation, or automatic apply;
- dynamic network calls;
- microphone, camera, ASR, TTS, voice cloning, Live2D, generated media, or
  media capture;
- hidden source ingestion, private-data rendering, or runtime store writes.

The UI may display false non-execution fields such as `sends_messages: false`.
Tests should forbid dangerous enabled states and real action surfaces, not safe
field names by substring alone.

## Browser QA

T419 Browser QA should verify:

- the session-loop section is visible;
- session turns, recall/cue chips, safety notes, and candidate summaries are
  readable;
- text does not overflow horizontally on the tested viewport;
- no provider/outbound/platform/media controls appear.
