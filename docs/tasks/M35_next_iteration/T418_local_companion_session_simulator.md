# T418: Local Companion Session Simulator

## Task ID

T418

## Goal

Add a deterministic synthetic companion session payload to the local web demo
state.

T418 should add `companion_session` to `TextFirstWebDemoState` and
`TextFirstWebDemoAdapter.build_synthetic_demo_state()`. The payload should
show a short local session with user/companion turns, reviewed memory recalls,
persona cues, visible safety notes, and post-turn review candidates. It must be
contract-first and non-executing: no model calls, no private data, no runtime
store writes, no sending, and no static UI rendering yet.

## Allowed Files

Future T418 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_local_companion_session_simulator.py`
- `docs/data_contracts/local_companion_session_simulator_contract.md`
- `docs/tasks/M35_next_iteration/T419_static_companion_session_loop.md`
- `docs/worker_summary/T418_worker_summary.md`
- `docs/07_handoff.md`

If T418 needs private data, source readers, model-provider calls, package
changes, static HTML/JS/CSS rendering, platform adapters, outbound messaging,
voice/avatar runtime, media generation, automatic apply triggers,
PersonaVersionStore writes, MemoryEventStore writes, or task-board edits,
Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or remote inference.
- Do not implement prompt execution, embeddings, vector search, semantic
  ranking, similarity scoring, fine-tuning, source readers, or real chat
  distillation.
- Do not write PersonaVersionStore, MemoryEventStore, review stores, runtime
  stores, files under `private/`, or any persistent user data.
- Do not modify static HTML, JS, or CSS in this task.
- Do not add schedulers, queues, webhooks, auth, tokens, recipient ids,
  delivery state, platform adapters, automatic outreach, outbound messaging,
  or delivery simulation.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  or regulator acceptance.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Payload

Add `companion_session` to `TextFirstWebDemoState`.

The payload must include:

- `schema_version`: `local_companion_session_v1`;
- `session_title`;
- `session_summary`;
- `persona_snapshot`;
- `turns`;
- `persona_cues`;
- `memory_recalls`;
- `safety_notes`;
- `post_turn_candidates`;
- `non_execution_flags`.

The payload should use a helper such as `_companion_session_payload()` so the
synthetic session is easy to inspect and later render.

### 2. Session Turns

Each turn must include:

- `turn_id`;
- `speaker`: `user` or `companion`;
- `safe_text`;
- `used_memory_recall_ids`;
- `used_persona_cue_ids`;
- `safety_note_ids`;
- `review_trace`;
- `generated_by`: `deterministic_synthetic_fixture`.

At least one companion turn must reference reviewed memory through
`used_memory_recall_ids`. At least one companion turn must reference persona
cues through `used_persona_cue_ids`.

### 3. Memory Recalls

Each memory recall must include:

- `recall_id`;
- `memory_kind`;
- `truth_status`;
- `reviewed_summary`;
- `source_label`;
- `raw_source_available`: false.

The payload must not include raw text, raw transcripts, private messages, or
private source paths.

### 4. Post-Turn Candidates

Include at least three post-turn candidates:

- one memory candidate;
- one persona growth patch;
- one proactive suggestion.

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

A life-stream draft candidate may be included if it is clearly labeled as
imagined and non-executing.

### 5. Non-Execution Flags

Add a `non_execution_flags` object with:

- `local_only`: true;
- `synthetic_fixture`: true;
- `calls_provider`: false;
- `uses_private_source`: false;
- `writes_runtime_store`: false;
- `automatic_apply`: false;
- `sends_messages`: false;
- `media_runtime_enabled`: false.

### 6. Tests

Create `tests/test_local_companion_session_simulator.py` proving:

- adapter state includes `companion_session`;
- top-level session fields are present and use the expected schema version;
- turns are ordered, synthetic, and contain at least one companion memory
  recall and one companion persona cue;
- memory recalls expose reviewed summaries only and set
  `raw_source_available` to false;
- post-turn candidates are review-required, preview-only, non-sending, and
  non-mutating;
- non-execution flags preserve local-only/no-provider/no-private/no-store/no
  outbound/no-media boundaries;
- served `/demo-state.json` includes the session payload without forbidden
  private/provider/outbound/media fields.

### 7. Data Contract

Create `docs/data_contracts/local_companion_session_simulator_contract.md`.

### 8. Next Task Package

Create `docs/tasks/M35_next_iteration/T419_static_companion_session_loop.md`.

T419 should be scoped to rendering the session loop in the static web demo and
performing Browser QA.

### 9. Worker Summary And Handoff

Write `docs/worker_summary/T418_worker_summary.md` and append a T418 worker
record to `docs/07_handoff.md`.

Do not mark T418 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_local_companion_session_simulator.py tests\test_integrated_demo_scenario_spine.py tests\test_trust_commercial_positioning_panel.py tests\test_text_first_web_demo_local_server.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Browser QA

Browser QA is not required for T418 if it only changes the adapter payload and
tests. T419 must perform Browser QA after rendering the session payload.

## Reviewer Type

Adversarial local session contract review for synthetic-only data, believable
companion continuity, review-candidate linkage, and no provider/outbound/media
surface expansion.
