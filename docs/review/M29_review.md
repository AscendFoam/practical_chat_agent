# M29 Review Workspace UI Review

Task: T392 M29 Milestone Review
Verdict: PASS_WITH_WARNINGS

## Reviewed Scope

Reviewed M29 deliverables:

- `docs/product/m29_review_workspace_ui_scope.md`
- `docs/data_contracts/review_workspace_presentation_contract.md`
- `docs/data_contracts/review_workspace_static_panel_contract.md`
- `docs/data_contracts/review_workspace_local_server_payload_contract.md`
- `src/practical_chat_agent/ui/review_workspace_adapter.py`
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`
- `src/practical_chat_agent/ui/text_first_web_demo_local_server.py`
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`
- `tests/test_review_workspace_presentation_adapter.py`
- `tests/test_review_workspace_static_panel.py`
- `tests/test_review_workspace_local_server_payload.py`
- `tests/test_text_first_web_demo_adapter.py`
- `tests/test_text_first_web_demo_local_server.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_accessibility.py`

## Findings

### Warnings

1. Browser visual QA remains unavailable in this environment.

   T390 attempted direct file and local HTTP browser checks, but the browser
   client blocked local navigation. T392 verified static/accessibility and
   route-level behavior instead. This is acceptable for M29 because the panel
   is local, synthetic, and non-applying, but the next UI-facing milestone
   should collect screenshot/interaction evidence when local navigation is
   available.

2. Internal presentation records still carry review queue identifiers.

   `ReviewWorkspacePresentationCard` includes `queue_item_id` and the T389
   adapter fills it from workspace/impact records. T391 mitigates this for the
   public demo payload by projecting cards through `_safe_review_workspace_card`
   and omitting internal queue fields from `/demo-state.json` and embedded
   HTML. This is acceptable for M29, but future public/export surfaces should
   keep the same projection boundary rather than dumping presentation records
   directly.

3. Static review card rendering should be hardened before real data.

   The T390 static renderer builds review card markup through string
   concatenation. The current payload is synthetic and tests prove forbidden
   private/provider/outbound/media fields are absent, so this does not block
   M29. Before any user-provided or imported review data reaches this panel,
   the renderer should use text nodes or an explicit escaping helper.

## Safety Assessment

- Private data: PASS. No task read `private/chat_history/`,
  `private/distilled/`, or private artifacts.
- Provider calls: PASS. No model-provider call path was added.
- Outbound/platform behavior: PASS. No sending, scheduling, webhook, platform
  adapter, recipient id, or delivery state was added.
- Media/runtime behavior: PASS. No microphone, camera, ASR, TTS, voice/avatar
  runtime, generated audio, generated image, or generated video path was added.
- Apply/mutation behavior: PASS. No review decision apply path, memory store
  write, PersonaCard mutation, PersonaVersionStore write, or deletion executor
  was added.
- Server payload boundary: PASS_WITH_WARNINGS. T391 strips internal queue and
  executor/write fields from local server payloads, but this boundary should
  stay explicit in future public/export surfaces.

## Static And Server Contract Assessment

- T389 provides deterministic review workspace presentation cards, badges,
  filters, and safe export summaries.
- T390 adds an accessible static Review tab and fallback fixture.
- T391 exposes adapter-backed synthetic `review_workspace` data through the
  existing local server payload flow.
- Static JS uses server-provided `review_workspace` when present and fallback
  data when absent.
- Contracts accurately describe non-actions and residual risks.

## Verification

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\review_workspace_adapter.py src\practical_chat_agent\ui\text_first_web_demo_adapter.py src\practical_chat_agent\ui\text_first_web_demo_local_server.py
```

Result: passed.

```powershell
$env:PYTHONPATH='src'
pytest tests\test_review_workspace_presentation_adapter.py tests\test_review_workspace_static_panel.py tests\test_review_workspace_local_server_payload.py tests\test_text_first_web_demo_adapter.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_accessibility.py -q -o cache_dir=artifacts\t392_pytest_cache --basetemp=artifacts\t392_pytest_basetemp
```

Result: passed, `38 passed`.

```powershell
rg -n "private/chat_history|raw_text|raw_transcript|provider_credentials|platform_recipient|send_queue|webhook|microphone|camera|audio_bytes|image_bytes|video_bytes|apply_decision|mutate_store|write_persona_version|generate_audio|generate_image|generate_video" src\practical_chat_agent\ui tests\test_review_workspace_presentation_adapter.py tests\test_review_workspace_static_panel.py tests\test_review_workspace_local_server_payload.py
```

Result: hits are confined to safety-test forbidden-term lists.

```powershell
rg -n "call_provider|call_model|generate_reply|send\b|schedule\b|deliver\b|publish\b|open_webhook|mutate_store|mutate_persona|apply_decision|write_persona_version|capture_microphone|capture_camera|synthesize_audio|generate_video" src\practical_chat_agent\ui
```

Result: one docstring hit in `review_workspace_adapter.py`; no runtime method
definitions found.

```powershell
git diff --check
```

Result: passed.

## Residual Risks

- M29 remains synthetic and local-only; it does not prove real user trust or
  real-data review quality.
- No apply executor or real memory/persona mutation path exists.
- No real import/de-identification quality evaluation exists.
- Browser screenshot QA was blocked by local navigation policy.
- Voice/avatar, proactive messaging, platform delivery, monetization, and
  production persistence remain locked for later milestones.

## Recommendation

Close M29 as `PASS_WITH_WARNINGS`.

The next milestone should harden the review workspace before real data or
apply executors: replace string-built review card markup with text-node or
escaping-based rendering, preserve the server-safe projection boundary, and
then design a separately scoped manual-apply preview flow.
