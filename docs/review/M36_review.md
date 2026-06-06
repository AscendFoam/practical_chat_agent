# M36 Review

Verdict: PASS_WITH_WARNINGS

## Scope Reviewed

Reviewed M36 work from T423 through T427:

- M36 scope refinement;
- `persona_distillation_workbench` adapter payload;
- payload contract tests;
- static workbench rendering;
- Review Workspace linkage;
- responsive CSS hardening;
- worker summaries and handoff records.

Primary files reviewed:

- `docs/product/m36_next_iteration_scope.md`;
- `docs/contracts/persona_distillation_workbench_payload.md`;
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`;
- T424 through T427 focused tests.

## Findings

No blocking defects were found in the reviewed M36 scope.

Warnings:

- M36 is still deterministic and synthetic. It demonstrates the shape of
  persona intake/distillation, not real extraction from private or uploaded
  records.
- The workbench does not call a model provider, run semantic extraction, use
  embeddings, rank evidence, or infer traits from real user material.
- Trait candidates and blocked requests are reviewable previews only. They do
  not write PersonaCard, memory, review, or runtime stores.
- Review Workspace linkage is display-only. It does not create an apply path,
  final approval path, rollback artifact, or executor.
- Browser QA was limited to the available 642px viewport; desktop behavior is
  covered by static CSS/tests rather than direct viewport control.
- M36 does not address proactive sending, voice/avatar runtime, generated
  media, production privacy flows, billing, or launch/compliance approval.

## What Passed

- M36 scope clearly separated synthetic persona customization from real-person
  cloning, deception, and private-source import.
- The adapter payload exposes all required workbench fields:
  `input_modes`, `synthetic_inputs`, `evidence_refs`,
  `extracted_trait_candidates`, `blocked_requests`, `safety_gates`, and
  `non_execution_flags`.
- Four input modes are represented: detailed description, fuzzy seed,
  synthetic dialogue excerpt, and random fictional seed.
- The payload includes nine trait categories and three blocked request types.
- Evidence refs point to synthetic input ids and safe summaries only.
- Non-execution flags make provider calls, private-source reads, runtime
  writes, automatic apply, outbound messaging, platform adapters, and media
  runtime explicitly false.
- Static UI renders the workbench with modes, inputs, evidence, traits,
  blocked requests, gates, and non-execution badges.
- Review Workspace shows 12 distillation cards: 9 trait cards and 3 blocked
  request cards.
- Responsive CSS hardening prevents long ids and evidence details from causing
  horizontal overflow in the available narrow viewport.

## Verification Evidence

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_distillation_workbench_payload.py tests\test_static_persona_distillation_workbench.py tests\test_persona_workbench_review_linkage.py tests\test_persona_workbench_responsive_hardening.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py tests\test_text_first_web_demo_local_server.py -q -o cache_dir=artifacts\t428_pytest_cache --basetemp=artifacts\t428_pytest_basetemp
```

Result: passed, `33 passed`.

Additional verification:

- `python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py`:
  passed;
- `node --check src\practical_chat_agent\ui\static\text_first_web_demo.js`:
  passed;
- `git diff --check`: passed with CRLF conversion warnings only.

## Browser QA Reviewed

T425 Browser QA:

- local static target rendered at the available 642px viewport;
- workbench visible;
- 4 mode cards, 4 synthetic input cards, 4 evidence cards, 9 trait cards, 3
  blocked request cards, 6 safety gate cards, and 9 non-execution labels;
- no forbidden action controls in the workbench;
- no horizontal overflow.

T426 Browser QA:

- Review Workspace rendered `Distillation (12)`;
- 12 workbench review cards were present;
- trait and blocked request details were visible;
- mutation false, automatic apply false, sends messages false were visible;
- no forbidden action controls in the review panel;
- no horizontal overflow.

T427 Browser QA:

- workbench section and Review Workspace persona workbench cards had no
  horizontal overflow;
- 12 workbench review cards remained visible;
- no forbidden action controls were present.

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

- Real persona distillation from private records still requires a future
  consent, source-handling, privacy, deidentification, and review milestone.
- A future model-backed extractor will need prompt/provider policy, audit
  traces, deterministic fallbacks, and adversarial clone/deception tests.
- Review cards are not yet connected to a persona version patch preview.
- No production-grade persistence or rollback model exists for applying
  reviewed persona changes.
- The demo still does not include proactive sending, voice/avatar runtime, or
  media generation.

## Recommendation

Open M37 as controlled persona evolution preview.

M37 should show how reviewed workbench trait candidates can become proposed
persona version patches with dry-run diffs, risk labels, and rollback notes,
while remaining preview-only and non-mutating.
