# M38 Review

Verdict: PASS_WITH_WARNINGS

## Scope Reviewed

Reviewed M38 work from T435 through T439:

- M38 scope refinement;
- `persona_version_draft_ledger` adapter payload and contract;
- static version draft ledger rendering;
- Review Workspace version linkage;
- responsive CSS hardening;
- worker summaries and handoff records.

Primary files reviewed:

- `docs/product/m38_next_iteration_scope.md`;
- `docs/contracts/persona_version_draft_ledger_payload.md`;
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`;
- T436 through T439 focused tests.

## Findings

No blocking defects were found in the reviewed M38 scope.

Warnings:

- M38 remains deterministic and synthetic. It demonstrates the shape of a
  persona version draft ledger, not a real persona version store.
- Version drafts are preview-only. They do not write PersonaCard,
  PersonaVersionStore, memory stores, review stores, or runtime state.
- Review Workspace linkage is display-only. It does not approve, apply,
  persist, or execute rollback.
- Conflict notes and rollback refs are metadata only.
- Browser QA was limited to the available 642px viewport; wider desktop
  behavior is covered by static CSS/tests rather than direct viewport control.
- M38 does not add real private-source import, consented chat-log ingestion,
  model-backed extraction, proactive sending, voice/avatar runtime, generated
  media, billing, or launch/compliance approval.

## What Passed

- The M38 scope clearly framed version drafts as auditable review artifacts,
  not runtime mutations.
- The adapter payload exposes `persona_version_draft_ledger` with source
  evolution preview ref, base persona snapshot ref, three draft outcomes,
  conflict notes, review outcome labels, rollback ref index, apply policy, and
  non-execution flags.
- Draft outcomes cover accepted for future apply review, deferred for weak
  evidence, and rejected for boundary risk.
- Conflict notes cover persona drift, boundary weakening, weak evidence,
  overattachment risk, and blocked-source contamination.
- Rollback refs cite M37 rollback notes and remain metadata-only.
- Static UI renders source linkage, base snapshot, draft cards, conflict
  notes, rollback refs, outcome labels, and non-execution labels.
- Review Workspace renders 14 version review cards:
  - 3 draft cards;
  - 5 conflict cards;
  - 3 rollback cards;
  - 3 outcome cards.
- Responsive hardening prevents long patch ids, draft ids, conflict codes,
  mitigation summaries, rollback refs, and outcome labels from causing
  horizontal overflow in the available narrow viewport.

## Verification Evidence

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_version_draft_ledger_payload.py tests\test_static_persona_version_draft_ledger.py tests\test_persona_version_draft_review_linkage.py tests\test_persona_version_draft_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t440_pytest_cache --basetemp=artifacts\t440_pytest_basetemp
```

Result: passed, `33 passed`.

Additional verification from worker records:

- `python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py`:
  passed in T436 and T438;
- `node --check src\practical_chat_agent\ui\static\text_first_web_demo.js`:
  passed in T437, T438, and T439;
- `git diff --check`: passed with CRLF conversion warnings only in T436,
  T437, T438, and T439.

## Browser QA Reviewed

T437 Browser QA:

- local static target rendered at the available 642px viewport;
- version ledger visible;
- 3 draft cards, 5 conflict cards, 3 rollback cards, 3 outcome cards, and 13
  non-execution labels;
- accepted/deferred/rejected outcomes visible;
- no forbidden action controls in the version ledger;
- no horizontal overflow.

T438 Browser QA:

- Review Workspace rendered `Version (14)`;
- 14 version review cards were present;
- draft details, conflict mitigation, rollback metadata, and outcome label
  details were visible;
- no forbidden action controls in the Review Workspace list;
- no horizontal overflow.

T439 Browser QA:

- version ledger section and Review Workspace version cards had no overflowing
  nodes;
- 14 version review cards, 14 badge rows, and 29 detail lists remained visible;
- no forbidden action controls were present;
- no document horizontal overflow.

## Explicit Non-Actions

- No real private chat records were read, ingested, quoted, summarized,
  transformed, distilled, or committed.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was accessed.
- No model-provider calls, prompt execution, embeddings, vector search,
  semantic ranking, similarity scoring, fine-tuning, source readers, runtime
  stores, platform adapters, schedulers, queues, webhooks, tokens, recipient
  ids, delivery state, automatic outreach, outbound messaging, microphone,
  camera, ASR, TTS, voice cloning, Live2D, generated audio, generated image,
  generated video, or media capture was added.
- No payment processing, production pricing claim, legal advice, compliance
  completion, app-store approval, launch approval, clinical claim, real user
  evidence, or regulator acceptance was claimed.
- `docs/04_task_board.md` was not modified.

## Remaining Risks

- A real consented source intake flow still does not exist.
- Real chat-log distillation still needs consent, source minimization,
  redaction, private-source handling, and clone/deception safeguards.
- Version drafts are not connected to a real apply executor or version store.
- Rollback remains explanatory metadata rather than an executable restore.
- The demo still does not include proactive sending, voice/avatar runtime, or
  media generation.

## Recommendation

Open M39 as consent-gated source intake manifest.

M39 should define a local synthetic manifest for user-provided source material:
source type, consent state, minimization status, redaction summary, blocked
source categories, and review gates. This creates a safe entry point for later
real-person/chat-record distillation work without reading private records yet.
