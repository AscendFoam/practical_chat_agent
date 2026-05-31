# T394 Worker Summary

Task: T394 Review Workspace Projection Boundary Tests
Status: worker draft for review

## Files Changed

- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `tests/test_review_workspace_local_server_payload.py`
- `docs/data_contracts/review_workspace_local_server_payload_contract.md`
- `docs/tasks/M30_review_workspace_hardening/T395_local_visual_qa_fallback.md`
- `docs/worker_summary/T394_worker_summary.md`
- `docs/07_handoff.md`

## Work Completed

- Added tests proving internal presentation records carry internal review
  refs while server-safe payloads strip internal ids and executor/write fields.
- Added an explicit `projection_policy` marker to server-safe
  `review_workspace` payloads.
- Corrected the policy marker to avoid sensitive forbidden substrings after
  regression tests caught the initial wording.
- Extended local server payload forbidden-field tests to include internal ids
  and executor/write fields.
- Updated the local server payload contract.
- Created T395 for local visual QA fallback.

## Verification

TDD record:

- RED:
  `$env:PYTHONPATH='src'; pytest tests\test_review_workspace_local_server_payload.py -q -o cache_dir=artifacts\t394_pytest_cache --basetemp=artifacts\t394_pytest_basetemp`
  failed with `1 failed, 6 passed` because `projection_policy` was absent.
- GREEN:
  after implementation and policy-string correction, focused adapter/server
  tests passed with `19 passed`.

Full T394 verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

Result: passed.

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_local_server_payload.py tests\test_text_first_web_demo_adapter.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t394_pytest_cache --basetemp=artifacts\t394_pytest_basetemp
```

Result: passed, `19 passed`.

```powershell
git diff --check
```

Result: passed with CRLF warnings only.

## Explicit Non-Actions

- No static layout change, local server route, private data reader, source
  ingestion from real logs, extraction, embedding, vector search, retrieval
  ranking, similarity scoring, model-provider call, PersonaCard synthesis,
  final reply generation, proactive candidate, scheduler, queue persistence,
  webhook, token, platform adapter, outbound messaging, voice/avatar runtime,
  media generation, package-manager dependency, or task-board edit was added.
- No review decision apply path, memory store mutation, PersonaCard mutation,
  PersonaVersionStore write, deletion executor, retrieval enablement, or
  provider-backed payload was added.
- No legal advice, compliance completion, app-store approval, launch approval,
  user-study validation, real user evidence, or regulator acceptance was
  claimed.
- No `private/chat_history/`, `private/distilled/`, or private artifact
  content was read, quoted, summarized, transformed, or committed.

## Remaining Risks

- Browser visual QA remains blocked by local navigation policy in this
  environment.
- T395 still needs a reproducible local visual QA fallback.
- Manual apply preview remains unscoped until T396.
