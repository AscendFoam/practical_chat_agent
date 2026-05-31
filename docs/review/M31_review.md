# M31 Manual Apply Preview Review

Task: T400 M31 Milestone Review
Verdict: PASS_WITH_WARNINGS

## Reviewed Scope

Reviewed M31 deliverables:

- `docs/product/m31_manual_apply_preview_scope.md`
- `docs/data_contracts/manual_apply_preview_contract.md`
- `docs/data_contracts/manual_apply_eligibility_gate_contract.md`
- `docs/data_contracts/review_workspace_apply_preview_panel_contract.md`
- `src/practical_chat_agent/services/manual_apply_preview.py`
- `src/practical_chat_agent/services/manual_apply_eligibility_gate.py`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_manual_apply_preview_records.py`
- `tests/test_manual_apply_eligibility_gate.py`
- `tests/test_review_workspace_apply_preview_panel.py`
- `tests/test_review_workspace_local_server_payload.py`
- `tests/test_review_workspace_static_panel.py`

## Findings

### Warnings

1. Manual apply preview eligibility is not executable authority.

   M31 correctly keeps preview records, eligibility decisions, and UI cards
   non-mutating. Any future executor must be a separately scoped and reviewed
   milestone with fresh gates immediately before execution.

2. Review workspace apply preview UI remains synthetic/local-only.

   The UI proves local read-only display of gates, effects, blockers, and
   rollback notes. It does not validate real imported data, real user trust, or
   production review quality.

3. Browser screenshot QA remains unavailable in this environment.

   M30 added a local structured QA fallback, but M31 still lacks rendered
   browser screenshot evidence because local navigation was previously blocked.

## Safety Assessment

- Private data: PASS. No task read `private/chat_history/`,
  `private/distilled/`, or private artifacts.
- Provider calls: PASS. No model-provider call path was added.
- Outbound/platform behavior: PASS. No sending, scheduling, webhook, platform
  adapter, recipient id, or delivery state was added.
- Media/runtime behavior: PASS. No microphone, camera, ASR, TTS, voice/avatar
  runtime, generated audio, generated image, or generated video path was added.
- Apply/mutation behavior: PASS. No review decision apply path, memory store
  write, PersonaCard mutation, PersonaVersionStore write, deletion executor,
  or retrieval index mutation was added.
- Manual apply preview clarity: PASS_WITH_WARNINGS. Preview/gate/UI records are
  explicit and tested, but they are not executable authority.

## Verification

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\manual_apply_preview.py src\practical_chat_agent\services\manual_apply_eligibility_gate.py src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

Result: passed.

```powershell
$env:PYTHONPATH='src'
pytest tests\test_manual_apply_preview_records.py tests\test_manual_apply_eligibility_gate.py tests\test_review_workspace_apply_preview_panel.py tests\test_review_workspace_local_server_payload.py tests\test_review_workspace_static_panel.py -q -o cache_dir=artifacts\t400_pytest_cache --basetemp=artifacts\t400_pytest_basetemp
```

Result: passed, `28 passed`.

Forbidden-field scan:

- Hits are confined to safety-test forbidden-term lists.

Forbidden method definition scan:

- No runtime method definitions found for apply, mutation, provider, outbound,
  or media methods.

Action-control scan:

- Hits are confined to safety-test forbidden-term lists.

```powershell
git diff --check
```

Result: passed.

## Residual Risks

- M31 does not implement a real apply executor.
- M31 does not prove real-data import/de-identification quality.
- M31 does not prove live companion quality or user trust.
- Browser screenshot QA remains unavailable in this environment.
- Future apply executor design remains high-risk and must be separately
  reviewed.

## Recommendation

Close M31 as `PASS_WITH_WARNINGS`.

The next milestone should not jump straight to mutation. It should first define
a narrow executor-risk assessment and approval-gate design, including rollback,
cache/index invalidation, final consent confirmation, and audit logging.
