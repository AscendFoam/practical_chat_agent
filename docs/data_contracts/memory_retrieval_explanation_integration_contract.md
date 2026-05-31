# Memory Retrieval Explanation Integration Contract

Task: T374 Memory Retrieval Explanation Integration
Status: worker draft for review

## Scope

This contract describes the implemented local retrieval packaging and
explanation helper in
`src/practical_chat_agent/services/memory_retrieval_explanation.py`.

The helper accepts already-created `MemoryEvent` records and produces
`MemoryRetrievalBundle` records plus `MemoryExplanationTrace` records. It also
creates review-first governance candidate records for contradiction,
supersession, consent-withdrawal deletion cascades, and persona-growth
evidence. It does not read private data, run source extraction, call model
providers, rank vector search, generate companion replies, mutate stores,
mutate PersonaCard records, schedule messages, connect to platform delivery,
or implement voice/avatar/media behavior.

## Implemented Records

### MemoryRetrievalExplanationResult

Implementation:

- `practical_chat_agent.services.memory_retrieval_explanation.MemoryRetrievalExplanationResult`

Fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `memory_retrieval_explanation_result_v1`. |
| `bundle` | `MemoryRetrievalBundle` with selected and excluded memory ids. |
| `explanation_traces` | Include/exclude trace records keyed by memory id. |
| `deletion_cascade_plan` | Optional review-required consent-withdrawal plan. |

Helper:

- `trace_by_memory_id(memory_id)` returns the matching trace or raises
  `KeyError`.

### MemoryRetrievalExplanationService

Implementation:

- `practical_chat_agent.services.memory_retrieval_explanation.MemoryRetrievalExplanationService`

Methods:

| Method | Behavior |
| --- | --- |
| `build_bundle(...)` | Selects eligible events for a requested retrieval purpose and emits traces for every input event. |
| `create_contradiction_candidate(...)` | Creates a review-required `MemoryContradictionCandidate` without overwriting memory. |
| `create_supersession_candidate(...)` | Creates a review-required `MemorySupersessionCandidate` without applying lifecycle changes. |
| `prepare_persona_growth_evidence(...)` | Builds review-required `PersonaGrowthEvidenceBundle` from eligible memory. |
| `is_distillation_feature_review_only(...)` | Confirms a de-identified style feature remains review-required with no retained source text. |

## Retrieval Purpose Mapping

`build_bundle(...)` maps retrieval purposes to contexts as follows:

| Purpose | Retrieval context |
| --- | --- |
| `factual_response` | `factual` |
| `inferred_context` | `inferred` |
| `relationship_context` | `relational` |
| `procedural_context` | `procedural` |
| `imagined_context` | `imagined` |
| `review_surface` | source event type context |

`review_surface` can include review-required memory only when
`include_review_required=true`; otherwise review-required memory is excluded
with an explanation trace.

## Inclusion And Exclusion Rules

Included events:

- must be allowed for the resolved retrieval context;
- must not be withdrawn by the caller;
- must not be `deleted`, `frozen`, `archived`, or `superseded`;
- must not be review-required unless `include_review_required=true`;
- must not be imagined memory in a `factual_response` bundle.

Exclusion reasons:

| Reason | Meaning |
| --- | --- |
| `withdrawn_consent` | Caller supplied the memory id in `withdrawn_memory_ids`. |
| `imagined_memory_excluded_from_factual_response` | Imagined memory was supplied for factual response packaging. |
| `{state}_memory_excluded` | Lifecycle state was `deleted`, `frozen`, `archived`, or `superseded`. |
| `review_required_memory_excluded` | Sensitive/review-required memory was supplied outside review inclusion. |
| `retrieval_permission_excluded` | Event route was not allowed for the resolved context. |

Included trace reason:

- `included_for_{purpose}`

Trace provenance refs are copied from memory provenance refs only; raw source
text is not retained.

## Consent Withdrawal

When `withdrawn_memory_ids` contains one or more input event ids,
`build_bundle(...)` excludes those memories and emits a
`MemoryDeletionCascadePlan.for_consent_withdrawal(...)` candidate.

The plan is review-required, incomplete, and recommends retrieval suppression
and training exclusion only. It does not delete records directly.

## Governance Candidate Boundaries

Contradiction candidates:

- require at least one input event;
- preserve the supplied memory ids;
- use `preference_change` as the default conflict type in T374;
- propose `request_clarification`;
- remain review-required.

Supersession candidates:

- preserve source and replacement memory ids;
- keep `applies_lifecycle_update=false`;
- remain review-required.

Persona-growth evidence:

- uses `PersonaGrowthEvidenceBundle.from_events(...)`;
- blocks imagined memory for factual persona growth;
- blocks inactive and review-required memory;
- does not mutate PersonaCard records.

Synthetic distillation features:

- are considered review-only when `review_required=true`,
  `source_text_retained=false`, and `blocked_from_persona_synthesis=false`;
- are not converted into PersonaCard records in T374.

## Forbidden Fields And Surfaces

The helper result and service must not expose or store:

- raw private chat text;
- raw transcripts;
- private message bodies;
- provider credentials;
- platform recipient ids;
- send queues;
- schedules;
- webhooks;
- tokens;
- delivery state;
- microphone, camera, audio, image, or video payloads;
- runtime reply-generation methods;
- persona mutation or automatic growth-apply methods;
- voice/avatar/media generation methods.

## Tests

Implemented tests:

- `tests/test_memory_retrieval_explanation_integration.py`

Covered behavior:

- imagined memory cannot enter factual response bundles;
- deleted, frozen, archived, and superseded memory is excluded;
- review-required memory is excluded outside review inclusion;
- withdrawn-consent memory creates a deletion cascade plan;
- contradiction and supersession helpers do not mutate stores;
- persona-growth evidence blocks ineligible memory and does not mutate
  PersonaCard;
- synthetic distillation features remain review-only;
- include/exclude explanation traces preserve reasons and provenance refs;
- forbidden private/provider/outbound/platform/media fields are absent;
- runtime and delivery method names are not exposed.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\memory_retrieval_explanation.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_retrieval_explanation_integration.py tests\test_memory_governance_candidates.py tests\test_persona_growth_candidates.py tests\test_synthetic_distillation_input_candidates.py tests\test_memory_retrieval_bundle_schema.py tests\test_text_first_chat_memory_prototype.py -q -o cache_dir=artifacts\t374_pytest_cache --basetemp=artifacts\t374_pytest_basetemp
```

```powershell
git diff --check
```

## Non-Actions

T374 does not implement:

- private data ingestion;
- source readers;
- extraction from real logs;
- memory consolidation writes;
- embeddings;
- vector search;
- semantic ranking;
- similarity scoring;
- model-provider calls;
- final companion reply generation;
- runtime PersonaCard mutation;
- automatic persona-growth apply;
- proactive candidates;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- generated media;
- legal, clinical, launch, app-store, or regulator approval.

## Residual Risks

- Retrieval helper selection is deterministic and rule-based; it is not a
  semantic retriever or ranker.
- No real private-data import, user-facing review UI, consent UI, or deletion
  executor exists.
- Persona-growth and distillation integration remains candidate/review-only.
- Real de-identification, similarity-risk scoring, and abuse-resistance need
  future implementation and review before any production workflow.
