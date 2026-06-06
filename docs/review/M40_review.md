# M40 Milestone Review

## Verdict

`PASS_WITH_WARNINGS`.

M40 safely demonstrates a deterministic, synthetic, preview-only persona source
evidence matrix for future consented distillation work. It links M39 source
intake candidates to eligible source ids, excluded source refs, evidence rows,
trait hypotheses, quality labels, review gate results, static UI rendering, and
Review Workspace cards.

The warning is important: M40 does not implement real source ingestion,
private-chat reading, raw content retention, model extraction, embeddings,
persona mutation, store writes, outbound messaging, platform integration, or
media runtime. T451 browser-level responsive QA also remains unclaimed because
no callable browser DOM inspection tool was available in that turn.

## Scope Reviewed

Tasks reviewed:

- T447 M40 next-iteration scope;
- T448 persona source evidence matrix payload;
- T449 static source evidence matrix UI;
- T450 source evidence Review Workspace linkage;
- T451 source evidence responsive hardening.

Primary artifacts reviewed:

- `docs/product/m40_next_iteration_scope.md`;
- `docs/contracts/persona_source_evidence_matrix_payload.md`;
- `docs/tasks/M40_next_iteration/T448_persona_source_evidence_matrix_payload.md`;
- `docs/tasks/M40_next_iteration/T449_persona_source_evidence_matrix_ui.md`;
- `docs/tasks/M40_next_iteration/T450_persona_source_evidence_review_linkage.md`;
- `docs/tasks/M40_next_iteration/T451_persona_source_evidence_responsive_hardening.md`;
- `docs/worker_summary/T447_worker_summary.md`;
- `docs/worker_summary/T448_worker_summary.md`;
- `docs/worker_summary/T449_worker_summary.md`;
- `docs/worker_summary/T450_worker_summary.md`;
- `docs/worker_summary/T451_worker_summary.md`;
- `src/practical_chat_agent/ui/text_first_web_demo_adapter.py`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.html`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.css`;
- `src/practical_chat_agent/ui/static/text_first_web_demo.js`;
- M40 focused tests listed below.

No `private/chat_history/`, `private/distilled/`, private artifacts,
credentials, provider accounts, platform callbacks, or platform APIs were read
or used.

## Task Matrix

| Task | Result | What it proves | What it does not prove |
| --- | --- | --- | --- |
| T447 scope | PASS | M40 was narrowed to a payload-first source evidence matrix slice. | Implementation, UI, Review Workspace linkage, or runtime behavior. |
| T448 payload | PASS | Adapter state and served JSON expose `persona_source_evidence_matrix` with M39 manifest linkage, eligible/excluded sources, evidence rows, trait hypotheses, quality labels, gates, apply policy, and non-execution flags. | Real source ingestion, model extraction, embeddings, raw retention, persona mutation, or store writes. |
| T449 static UI | PASS_WITH_WARNINGS | Static assets render source evidence matrix anchors, fallback payload, lists, cards, labels, and non-execution details. | Browser layout QA; real extraction UI; import/upload/read controls. |
| T450 review linkage | PASS | Review Workspace exposes source evidence review cards and `Evidence` filter tab with safe detail rows. | Applying evidence to PersonaCard, runtime mutation, or extraction execution. |
| T451 responsive hardening | PASS_WITH_WARNINGS | CSS/static tests cover long-id wrapping and mobile selectors for source evidence matrix and evidence review cards. | Browser-level responsive QA. |

## Review Answers

1. Does M40 expose a deterministic source evidence matrix linked to M39? Yes.
   Tests verify the schema version, M39 intake manifest reference, eligible
   source ids, excluded source refs, evidence rows, trait hypotheses, quality
   labels, review gates, apply policy, and non-execution flags.
2. Are eligible and excluded sources visible and reviewable? Yes. Static UI
   renders eligible ids and excluded refs, and Review Workspace exposes
   exclusion cards.
3. Do evidence rows and trait hypotheses remain local synthetic previews? Yes.
   The payload and review cards keep `review_required`, `preview_only`, no raw
   retention, no extraction, no embeddings, no store writes, and no mutation.
4. Are source evidence records visible in Review Workspace? Yes. T450 adds
   cards for excluded refs, evidence rows, trait hypotheses, quality labels,
   and gate results, plus an `Evidence` filter tab.
5. Do responsive rules cover long ids and narrow viewports? Partially. Static
   CSS tests verify explicit wrapping selectors. Browser QA is not claimed for
   T451.
6. Do tests prove no private/provider/runtime surfaces? Within the local
   focused scope, yes. The tests recursively scan unsafe flags and static
   surfaces for private-source, provider, outbound, platform, and media terms.
7. Is the next milestone scoped without pretending real distillation exists?
   Yes. M41 is scoped as local source-evidence-to-persona-proposal preview, not
   extraction or runtime mutation.

## Verification Results

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_source_evidence_matrix_payload.py tests\test_static_persona_source_evidence_matrix.py tests\test_persona_source_evidence_review_linkage.py tests\test_persona_source_evidence_responsive_hardening.py tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t452_pytest_cache --basetemp=artifacts\t452_pytest_basetemp
```

Result: passed, `35 passed`.

```powershell
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_adapter.py
```

Result: passed.

```powershell
node --check src\practical_chat_agent\ui\static\text_first_web_demo.js
```

Result: passed.

## Safety Boundary

M40 allows the source evidence matrix to stand as local synthetic review
evidence. It does not authorize:

- reading `private/chat_history/` or private artifacts;
- importing uploaded archives;
- retaining raw source content;
- extracting traits from real content;
- calling model providers;
- creating embeddings or vector indexes;
- writing PersonaCard, PersonaVersionStore, MemoryEventStore, review stores,
  runtime stores, or databases;
- automatic apply;
- outbound messaging;
- platform adapters;
- voice/avatar/media runtime;
- payment processing;
- launch, compliance, legal, clinical, app-store, or regulator approval
  claims.

## Residual Risks

- Browser-level responsive QA for T451 remains outstanding.
- M40 evidence rows are fixture summaries, not extraction outputs.
- Source quality and gate labels are deterministic examples, not validated
  policy decisions over real records.
- M41 must not overread M40 as permission to ingest private chat archives.
- Future real distillation needs stronger consent, minimization, redaction,
  source ownership, and anti-deception gates.

## Next Step

Proceed to M41 only as local preview work:
`source_evidence_persona_proposal` should convert reviewed synthetic source
evidence into persona proposal candidates without reading sources, extracting
real traits, calling providers, mutating persona state, writing stores, or
sending messages.
