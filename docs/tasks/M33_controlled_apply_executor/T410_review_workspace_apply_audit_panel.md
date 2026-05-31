# T410: Review Workspace Apply Audit Panel

## Task ID

T410

## Goal

Expose completed local apply audit manifest entries in the review workspace.

T410 should add a static/demo review workspace panel that displays normalized
apply audit manifest entries from T409. The panel should help reviewers inspect
what changed, which gates approved it, and which rollback references exist,
without exposing private data, provider/platform details, outbound delivery
state, or media payloads.

## Allowed Files

Future T410 worker may create or modify only:

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_review_workspace_apply_audit_panel.py`
- `docs/data_contracts/review_workspace_apply_audit_panel_contract.md`
- `docs/tasks/M33_controlled_apply_executor/T411_controlled_apply_executor_review.md`
- `docs/worker_summary/T410_worker_summary.md`
- `docs/07_handoff.md`

If T410 needs private data, source readers, model-provider calls, package
changes, platform adapters, outbound messaging, voice/avatar runtime, media
generation, automatic apply triggers, PersonaVersionStore writes, or
MemoryEventStore writes, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers.
- Do not implement source readers, extraction from real logs, embeddings,
  vector search, semantic ranking, fine-tuning, similarity scoring, persona
  synthesis, final companion reply generation, or runtime mutation.
- Do not write PersonaVersionStore or MemoryEventStore.
- Do not add CLIs, schedulers, queues, webhooks, auth, tokens, recipient ids,
  delivery state, or platform persistence behavior.
- Do not implement proactive candidates, automatic outreach, sending,
  scheduling, notifications, platform delivery, microphone, camera, ASR, TTS,
  voice cloning, voice/avatar likeness, Live2D, generated audio, generated
  image, generated video, or media capture.
- Do not modify `docs/04_task_board.md`.

## Expected Outputs

### 1. Server Payload Projection

Update the text-first web demo adapter so the review workspace payload includes
synthetic apply audit manifest entries suitable for display. The served payload
must strip executor-only fields, raw paths, provider/platform details,
outbound delivery state, and media payloads.

### 2. Static UI Panel

Update the static review workspace UI to display apply audit entries with:

- apply type;
- source artifact id;
- review decision id;
- eligibility id;
- approval id;
- reviewer id;
- changed field paths or affected memory ids;
- rollback references;
- safe summary.

### 3. Tests

Create `tests/test_review_workspace_apply_audit_panel.py` proving:

- the server payload includes apply audit manifest cards;
- persona growth and memory lifecycle entries render separately;
- rollback references are present;
- private/provider/outbound/media fields are absent from served payload JSON;
- static JS/CSS contains the expected panel hooks without platform delivery or
  media-generation actions.

### 4. Data Contract

Create `docs/data_contracts/review_workspace_apply_audit_panel_contract.md`.

### 5. Next Task Package

Create
`docs/tasks/M33_controlled_apply_executor/T411_controlled_apply_executor_review.md`.

### 6. Worker Summary And Handoff

Write `docs/worker_summary/T410_worker_summary.md` and append a T410 worker
record to `docs/07_handoff.md`.

Do not mark T410 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_apply_audit_panel.py tests\test_apply_executor_audit_manifest.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial review workspace projection review for audit completeness,
rollback visibility, privacy, static UI safety, and no platform/provider/media
surface expansion.
