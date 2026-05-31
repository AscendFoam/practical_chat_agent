# T398: Manual Apply Eligibility Gate

## Task ID

T398

## Goal

Create a deterministic non-mutating eligibility gate for manual apply preview
records.

T398 should read a `ManualApplyPreviewRecord` and related decision/workspace
context, then return an eligibility decision such as eligible, blocked, or
stale. It must not apply anything.

## Allowed Files

Future T398 worker may create or modify only:

- `src/practical_chat_agent/services/manual_apply_eligibility_gate.py`
- `tests/test_manual_apply_eligibility_gate.py`
- `docs/data_contracts/manual_apply_eligibility_gate_contract.md`
- `docs/tasks/M31_manual_apply_preview/T399_review_workspace_apply_preview_panel.md`
- `docs/worker_summary/T398_worker_summary.md`
- `docs/07_handoff.md`

If T398 needs UI changes beyond the next task package, local server routes,
private data, model-provider calls, package changes, platform adapters,
outbound messaging, voice/avatar runtime, media generation, persistence
outside local records, or apply executors, Captain must revise this package
before assignment.

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

- Non-mutating eligibility gate records/service.
- Tests proving eligible, blocked, stale, and gate-mismatch outcomes.
- Contract documenting that eligibility is not executable authority.
- T399 next task package exists.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\manual_apply_eligibility_gate.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_manual_apply_eligibility_gate.py tests\test_manual_apply_preview_records.py -q
```

```powershell
git diff --check
```

Use project-local pytest cache and basetemp paths if the default user temp
directory is not writable.

## Reviewer Type

Adversarial non-mutating gate review for eligibility correctness, stale-state
detection, privacy, apply-safety, and documentation accuracy.
