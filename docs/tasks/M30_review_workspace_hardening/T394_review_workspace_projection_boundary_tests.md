# T394: Review Workspace Projection Boundary Tests

## Task ID

T394

## Goal

Harden the boundary between internal review workspace presentation records and
served local demo payloads.

T394 should add focused tests and, if necessary, small adapter refactors proving
that internal queue identifiers and executor/write fields can exist in internal
presentation records but cannot appear in `/demo-state.json`, embedded HTML, or
the static panel payload contract.

## Allowed Files

Future T394 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_review_workspace_local_server_payload.py`
- `docs/data_contracts/review_workspace_local_server_payload_contract.md`
- `docs/tasks/M30_review_workspace_hardening/T395_local_visual_qa_fallback.md`
- `docs/worker_summary/T394_worker_summary.md`
- `docs/07_handoff.md`

If T394 needs static layout changes, local server route additions, private
data, Browser runs beyond local QA, model-provider calls, package changes,
platform adapters, outbound messaging, voice/avatar runtime, media generation,
persistence outside local synthetic payloads, or apply executors, Captain must
revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, runtime persona mutation, or
  runtime memory mutation.
- Do not apply review decisions or dry-run plans.
- Do not mutate memory stores, PersonaCard objects, or PersonaVersionStore.
- Do not add routes, CLIs, schedulers, queues, webhooks, auth, tokens,
  recipient ids, delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

- Tests prove internal presentation records may contain internal queue refs.
- Tests prove server-safe payloads omit `queue`, `queue_item_id`,
  `applies_changes`, `writes_memory_store`, `writes_persona_version`,
  `send`, `schedule`, `delivery`, `platform`, `webhook`, provider fields, and
  media fields.
- Contract documents the boundary and why direct presentation dumps are not
  served.
- T395 next task package exists.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_local_server_payload.py tests\test_text_first_web_demo_adapter.py tests\test_text_first_web_demo_local_server.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial projection-boundary review for internal identifier leaks,
non-apply safety, synthetic-only payloads, and documentation accuracy.
