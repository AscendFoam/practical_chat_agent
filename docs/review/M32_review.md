# M32 Apply Executor Risk Review

Task: T405 M32 Milestone Review
Verdict: PASS_WITH_WARNINGS

## Reviewed Scope

Reviewed M32 deliverables:

- `docs/product/m32_apply_executor_risk_scope.md`
- `docs/data_contracts/apply_executor_risk_contract.md`
- `docs/data_contracts/apply_executor_approval_gate_contract.md`
- `docs/data_contracts/review_workspace_apply_risk_panel_contract.md`
- `src/practical_chat_agent/services/apply_executor_risk.py`
- `src/practical_chat_agent/services/apply_executor_approval_gate.py`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_apply_executor_risk_records.py`
- `tests/test_apply_executor_approval_gate.py`
- `tests/test_review_workspace_apply_risk_panel.py`
- `tests/test_review_workspace_apply_preview_panel.py`
- `tests/test_review_workspace_local_server_payload.py`
- `tests/test_review_workspace_static_panel.py`

## Findings

### Warnings

1. Approval outcomes are not executable authority.

   M32 correctly models risk and approval evidence, but
   `ready_for_separately_scoped_executor_design` is still only a review
   recommendation. A future executor must run fresh gates immediately before
   any mutation and must be separately scoped.

2. Review workspace risk UI remains synthetic/local-only.

   T404 proves read-only display of risk factors, approval outcomes, blockers,
   and non-execution flags in the local demo. It does not validate real
   imported data, production review quality, or user trust.

3. T405 found and repaired one server-safe projection drift.

   The first M32 combined verification run caught T404 risk cards exposing
   internal executor/write flag fields in the served review workspace payload.
   Commit `ff2c474` removed those fields from served cards and added a focused
   regression. No remaining blocker is present, but future UI projections
   should keep payload-level forbidden-field tests close to the projection
   boundary.

4. Browser screenshot QA remains unavailable in this environment.

   M30 added a local structured QA fallback, and T404 includes static asset
   assertions, but M32 still lacks rendered browser screenshot evidence because
   local browser navigation has previously been unavailable here.

## Safety Assessment

- Private data: PASS. No task read `private/chat_history/`,
  `private/distilled/`, or private artifacts.
- Provider calls: PASS. No model-provider call path was added.
- Outbound/platform behavior: PASS. No sending, scheduling, webhook, platform
  adapter, recipient id, or delivery state was added.
- Media/runtime behavior: PASS. No microphone, camera, ASR, TTS, voice/avatar
  runtime, generated audio, generated image, or generated video path was added.
- Apply/mutation behavior: PASS_WITH_WARNINGS. No review decision apply path,
  memory store write, PersonaCard mutation, PersonaVersionStore write,
  deletion executor, or retrieval index mutation was added. Internal risk
  records intentionally carry non-executing flags; served UI payloads strip
  executor/write fields.
- Risk-record clarity: PASS. T402 covers critical, high, approval, rollback,
  audit, serialization, forbidden fields, and rejected executing flags.
- Approval-gate correctness: PASS. T403 covers ready, blocked, high-risk,
  stale, mismatch, forbidden fields, missing gates, and rejected executing
  flags.
- Read-only UI: PASS_WITH_WARNINGS. T404 displays local synthetic risk cards
  with no action controls, but browser screenshot QA remains unavailable.

## Verification

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\apply_executor_risk.py src\practical_chat_agent\services\apply_executor_approval_gate.py src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

Result: passed.

```powershell
$env:PYTHONPATH='src'
pytest tests\test_apply_executor_risk_records.py tests\test_apply_executor_approval_gate.py tests\test_review_workspace_apply_risk_panel.py tests\test_review_workspace_apply_preview_panel.py tests\test_review_workspace_local_server_payload.py tests\test_review_workspace_static_panel.py -q -o cache_dir=artifacts\t405_pytest_cache --basetemp=artifacts\t405_pytest_basetemp
```

Result: passed, `36 passed`.

T404 repair regression:

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_apply_risk_panel.py -q -o cache_dir=artifacts\t404_repair_pytest_cache --basetemp=artifacts\t404_repair_pytest_basetemp
```

Result: passed, `5 passed`.

Forbidden method definition scan:

- No runtime method definitions found for apply, mutation, provider, outbound,
  or media methods.

Action-control scan:

- No action-control hits found in the static review workspace assets.

Forbidden-field scan:

- Hits are confined to internal synthetic review queue construction, internal
  non-executing risk-record schema flags, and safety-test forbidden-term lists.
- Served review workspace payload tests verify queue refs and executor/write
  fields are stripped from the server-safe projection.

```powershell
git diff --check
```

Result: passed.

## Residual Risks

- M32 does not implement a real apply executor.
- M32 does not prove real-data import/de-identification quality.
- M32 does not prove user trust for real apply flows.
- Browser screenshot QA remains unavailable in this environment.
- Any future executor remains high-risk and must be separately scoped with
  fresh consent, rollback, audit, and projection tests.

## Recommendation

Close M32 as `PASS_WITH_WARNINGS`.

The next milestone may begin a narrowly scoped apply-executor design preflight,
but it must start with an explicit safety scope and must not jump directly to
runtime mutation without fresh review gates.
