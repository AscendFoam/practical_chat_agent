# M37 Review

Verdict: PASS_WITH_WARNINGS

## Scope Reviewed

Reviewed M37 work from T429 through T433:

- M37 scope refinement;
- `persona_evolution_preview` adapter payload and contract;
- static evolution preview rendering;
- Review Workspace evolution linkage;
- responsive CSS hardening;
- worker summaries and handoff records.

Primary files reviewed:

- `docs/product/m37_next_iteration_scope.md`;
- `docs/contracts/persona_evolution_preview_payload.md`;
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`;
- T430 through T433 focused tests.

## Findings

No blocking defects were found in the reviewed M37 scope.

Warnings:

- M37 remains deterministic and synthetic. It demonstrates the shape of
  persona evolution, not real extraction from private records or provider
  output.
- Patch candidates are preview-only. They do not write PersonaCard,
  PersonaVersionStore, memory stores, review stores, or runtime state.
- Review Workspace linkage is display-only. It does not approve, apply, or
  persist a persona version change.
- Rollback notes are metadata only. They are not executable rollback records.
- Browser QA was limited to the available 642px viewport; wider desktop
  behavior is covered by static CSS/tests rather than direct viewport control.
- M37 does not add proactive sending, voice/avatar runtime, generated media,
  real private-source consent flows, billing, or launch/compliance approval.

## What Passed

- The M37 scope clearly framed persona growth as visible, reviewable, and
  reversible before any apply path exists.
- The adapter payload exposes `persona_evolution_preview` with source workbench
  linkage, source trait ids, persona snapshot before, six patch candidates,
  risk labels, rollback notes, blocked source exclusions, apply policy, and
  non-execution flags.
- Patch candidates cover `style.tone`, `style.pacing`, `style.humor`,
  `relationship.boundary_style`, `memory.use_preference`, and
  `growth.short_term_hint`.
- Risk labels cover persona drift, overattachment risk, unclear evidence,
  boundary weakening, and blocked source exclusion.
- Blocked clone/deception/private-import workbench requests remain excluded
  from patch generation.
- Static UI renders source linkage, snapshot before, patch cards, risks,
  rollbacks, blocked exclusions, and non-execution labels.
- Review Workspace renders 20 evolution review cards:
  - 6 patch cards;
  - 5 risk cards;
  - 6 rollback cards;
  - 3 blocked source exclusion cards.
- Responsive hardening prevents long changed-field paths, risk text, rollback
  ids, and detail rows from causing horizontal overflow in the available narrow
  viewport.

## Verification Evidence

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_evolution_preview_payload.py tests\test_persona_evolution_review_linkage.py tests\test_persona_evolution_responsive_hardening.py tests\test_static_persona_evolution_preview.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t434_pytest_cache --basetemp=artifacts\t434_pytest_basetemp
```

Result: passed, `34 passed`.

Additional verification from worker records:

- `python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py`:
  passed in T432;
- `node --check src\practical_chat_agent\ui\static\text_first_web_demo.js`:
  passed in T431, T432, and T433;
- `git diff --check`: passed with CRLF conversion warnings only in T431, T432,
  and T433.

## Browser QA Reviewed

T431 Browser QA:

- local static target rendered at the available 642px viewport;
- evolution section visible;
- 6 patch cards, 5 risk cards, 6 rollback cards, 3 exclusion cards, and 12
  non-execution labels;
- no forbidden action controls in the evolution section;
- no horizontal overflow.

T432 Browser QA:

- Review Workspace rendered `Evolution (20)`;
- 20 evolution review cards were present;
- patch details, risk mitigation, rollback metadata, and blocked source
  exclusion details were visible;
- no forbidden action controls in the Review Workspace list;
- no horizontal overflow;
- screenshot capture succeeded on a fresh browser tab.

T433 Browser QA:

- evolution preview had no overflowing nodes;
- Review Workspace evolution cards had no overflowing nodes;
- 20 evolution badge rows and 30 evolution detail lists were visible;
- no forbidden action controls were present;
- no document horizontal overflow;
- screenshot capture succeeded.

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

- A real persona version ledger and apply path still do not exist.
- Future real-source distillation still needs explicit consent, source
  handling, minimization, deidentification, and review gates.
- Future model-backed extraction needs provider policy, prompt audit traces,
  deterministic fallbacks, and adversarial clone/deception tests.
- Rollback remains explanatory metadata rather than an executable version
  restore.
- The demo still does not include proactive sending, voice/avatar runtime, or
  media generation.

## Recommendation

Open M38 as controlled persona version ledger and apply-readiness preview.

M38 should turn reviewed evolution patches into local persona version draft
records with review outcomes, conflict checks, and rollback references while
remaining synthetic, consent-forward, auditable, and non-mutating until an
explicit apply milestone is approved.
