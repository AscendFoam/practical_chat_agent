# M26 Review: Memory Persona Implementation Foundation

## Status

Gate recommendation: PASS_WITH_WARNINGS for entering the next implementation
milestone.

M26 implemented the first local, deterministic, synthetic-only foundation for
memory governance candidates, persona-growth candidates, synthetic
distillation input candidates, and retrieval/explanation integration. The
review found one retrieval boundary issue: review-required memory could be
included in `factual_response` bundles when `include_review_required=True`.
That issue was fixed during review with a regression test; review-required
memory is now eligible only for `review_surface` with explicit inclusion.

The milestone is not launch-ready product behavior. It still does not include
private-data import, semantic retrieval ranking, embeddings, de-identification
quality validation, user-facing review UI, deletion execution, proactive
behavior, voice/avatar runtime, media generation, platform delivery, payment
flows, legal approval, clinical validation, or real user evidence.

## Task Coverage

| Task | Result | Evidence |
| --- | --- | --- |
| T370 M26 scope | Implemented as implementation scope | `docs/product/m26_memory_persona_implementation_scope.md`. |
| T371 Memory governance candidates | Implemented and tested | `src/practical_chat_agent/services/memory_governance.py`, `tests/test_memory_governance_candidates.py`, `docs/data_contracts/memory_governance_candidate_contract.md`. |
| T372 Persona growth candidates | Implemented and tested | `src/practical_chat_agent/services/persona_growth.py`, `tests/test_persona_growth_candidates.py`, `docs/data_contracts/persona_growth_candidate_implementation_contract.md`. |
| T373 Synthetic distillation input candidates | Implemented and tested | `src/practical_chat_agent/services/synthetic_distillation_input.py`, `tests/test_synthetic_distillation_input_candidates.py`, `docs/data_contracts/synthetic_distillation_input_implementation_contract.md`. |
| T374 Retrieval explanation integration | Implemented, tested, and review-boundary fix added | `src/practical_chat_agent/services/memory_retrieval_explanation.py`, `tests/test_memory_retrieval_explanation_integration.py`, `docs/data_contracts/memory_retrieval_explanation_integration_contract.md`. |

## Review Findings

### Fixed During Review

P1: `include_review_required=True` could force review-required memory into a
`factual_response` bundle.

- Evidence: the new regression
  `test_review_required_memory_cannot_be_forced_into_factual_response` first
  failed with `1 failed, 14 passed`.
- Fix: `MemoryRetrievalExplanationService` now excludes review-required memory
  unless the purpose is `review_surface` and `include_review_required=True`.
- Verification: the focused T374 test file passed with `15 passed` after the
  fix.

### Open Warnings

- M26 is still candidate/review-only. It does not include an apply path for
  deletion cascades, supersession, contradiction resolution, or persona-growth
  patches.
- Retrieval explanation is deterministic rule-gating, not semantic search,
  ranking, embedding, or long-context memory evaluation.
- T374 references the consolidation boundary, but the new helper does not
  perform consolidation writes or invoke ranking/consolidation workflows. That
  is acceptable for this foundation milestone but should be explicit in M27.
- Synthetic distillation records prove structural boundaries, not real
  de-identification quality, consent UX, source authenticity, speaker mapping,
  or similarity-risk scoring.
- No user-facing review UI exists for approving or rejecting candidate records.

## Implemented Behavior Summary

M26 now has executable local records for:

- memory contradiction candidates;
- memory supersession candidates;
- consent-withdrawal deletion cascade plans;
- memory explanation traces;
- persona-growth evidence bundles;
- persona-growth field changes, patch candidates, patch reviews, and journal
  entries;
- synthetic speaker aliases, consent refs, source segments, redaction refs,
  clone-risk decisions, de-identified style feature candidates, synthetic input
  manifests, and fictional persona synthesis inputs;
- retrieval explanation results and deterministic memory bundle construction.

The implemented tests cover:

- review-required governance records;
- non-mutating store/persona behavior;
- imagined/factual separation;
- inactive and superseded memory exclusion;
- review-required exclusion outside review surfaces;
- withdrawn-consent cascade planning;
- persona-growth frozen-field and trait-delta limits;
- no auto-apply and no persona version writes;
- clone-risk and source-text retention blocking;
- forbidden private/provider/outbound/platform/media fields;
- absence of runtime delivery and media-generation methods.

## Safety Boundary Assessment

The M26 implementation preserves the main M25 invariants:

- factual, inferred, relational, procedural, and imagined memory remain
  separated;
- imagined memory cannot enter factual response bundles;
- review-required memory is excluded outside review surfaces;
- deleted, frozen, archived, and superseded memory is excluded from retrieval
  bundles;
- contradiction and supersession remain review candidates rather than silent
  overwrites;
- deletion cascade plans are review-required and incomplete;
- persona growth is patch-based, user-review-required, and cannot auto-apply;
- frozen identity, safety, source-policy, disclosure, persona id, user id, and
  default proactive fields cannot be patched by growth candidates;
- synthetic distillation remains abstract, de-identified, text-only,
  review-required, and not runtime-ready;
- no private transcript, provider, platform delivery, outbound messaging,
  voice/avatar, or media payload surfaces were introduced.

## Verification Evidence

Focused regression verification during review:

```text
$env:PYTHONPATH='src'; pytest tests\test_memory_retrieval_explanation_integration.py -q -o cache_dir=artifacts\t375_fix_pytest_cache --basetemp=artifacts\t375_fix_pytest_basetemp
```

Result before fix: failed, `1 failed, 14 passed`.

Result after fix: passed, `15 passed`.

Final milestone verification:

```text
$env:PYTHONPATH='src'; python -m py_compile src\practical_chat_agent\services\memory_retrieval_explanation.py
```

Result: passed.

```text
$env:PYTHONPATH='src'; pytest tests\test_memory_governance_candidates.py tests\test_persona_growth_candidates.py tests\test_synthetic_distillation_input_candidates.py tests\test_memory_retrieval_explanation_integration.py -q -o cache_dir=artifacts\t375_pytest_cache --basetemp=artifacts\t375_pytest_basetemp
```

Result: passed, `58 passed`.

Expanded regression verification:

```text
$env:PYTHONPATH='src'; pytest tests\test_memory_retrieval_explanation_integration.py tests\test_memory_governance_candidates.py tests\test_persona_growth_candidates.py tests\test_synthetic_distillation_input_candidates.py tests\test_memory_retrieval_bundle_schema.py tests\test_text_first_chat_memory_prototype.py -q -o cache_dir=artifacts\t375_full_pytest_cache --basetemp=artifacts\t375_full_pytest_basetemp
```

Result: passed, `73 passed`.

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings for modified files.

## Explicit Non-Actions

M26 did not implement:

- private chat ingestion;
- raw private transcript reads;
- source readers for `private/chat_history/` or `private/distilled/`;
- model-provider calls;
- LLM extraction;
- embeddings, vector search, semantic ranking, or fine-tuning;
- de-identification quality guarantees;
- real-person recreation or authorized digital twin support;
- public-figure, ex-partner, family-member, deceased-person, coworker,
  classmate, minor, voice, face, or avatar likeness workflows;
- final companion reply generation;
- runtime memory/persona mutation without review;
- proactive candidate generation;
- automatic sending, scheduling, notifications, queues, webhooks, tokens, or
  platform delivery;
- voice, ASR, TTS, voice cloning, microphone capture, generated audio, camera
  capture, avatar runtime, Live2D runtime, face tracking, generated images, or
  generated video;
- public hosting, production persistence, payment flows, analytics, launch
  approval, legal compliance completion, app-store acceptance, clinical
  validation, regulator acceptance, user-study validation, or real user
  evidence.

M26 also did not read, quote, summarize, transform, or commit content from
`private/chat_history/`, `private/distilled/`, or private artifacts.

## Residual Risks

- Local deterministic tests do not validate live companion quality.
- No real-data import, redaction pipeline, de-identification evaluator, consent
  UI, or review UI exists.
- No deletion executor or cache/index cascade exists beyond candidate plans.
- No semantic retrieval quality benchmark exists.
- No abuse-resistance, poisoning defense, similarity-risk scorer, source
  authenticity checker, or third-party consent workflow exists.
- No platform delivery, proactive messaging, voice/avatar, virtual social feed,
  commercial packaging, or production persistence exists.

## M27 Entry Recommendation

Proceed to M27 only with another conservative implementation milestone.

Recommended M27 scope:

- build a local review queue/view model for memory governance, persona-growth,
  and distillation candidates;
- add deterministic apply simulators or dry-run executors for approved memory
  lifecycle changes without touching private data;
- add synthetic retrieval ranking fixtures and explanation scoring without
  provider calls;
- keep all import/de-identification, proactive outreach, voice/avatar, media,
  platform delivery, and payment work out of scope until the review UI and
  consent controls are executable.

Reviewer should BLOCK any future milestone that claims humanlike runtime
companionship, real-person distillation, proactive outreach, voice/avatar
interaction, platform delivery, launch readiness, or monetization readiness
without separately scoped implementation, safety review, and verification.
