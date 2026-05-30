# M16 Review: Relationship Dialogue Consumption Foundation

## Status

Gate recommendation: PASS_WITH_WARNINGS for entering M17 proactive consent
schema work.

M16 implemented a local, review-first dialogue consumption foundation. It did
not implement runtime AI chat, LLM reply generation, proactive candidates,
scheduling, automatic sending, platform integration, voice/avatar/video
behavior, product UI, or a web demo.

## Task Coverage

| Task | Result | Evidence |
| --- | --- | --- |
| T270 Relationship context bundle | Implemented | `RelationshipContextBundle` packages approved PersonaCard, RelationshipState, and MemoryRetrievalBundle data; `tests/test_relationship_context_bundle_schema.py`. |
| T271 Dialogue context planner | Implemented | `DialogueContextPlanner` converts context bundles into deterministic metadata; `tests/test_dialogue_context_planner.py`. |
| T272 Dialogue draft stub | Implemented | `DialogueDraftStubService` creates deterministic review-only draft objects; `tests/test_dialogue_draft_stub.py`. |

## Implemented Code

- `src/practical_chat_agent/core/models.py`
  - `RelationshipContextPersonaSnapshot`
  - `RelationshipContextMemorySnapshot`
  - `RelationshipContextBundle`
- `src/practical_chat_agent/services/dialogue_context_planner.py`
  - `DialogueContextPlan`
  - `DialogueContextPlanner`
- `src/practical_chat_agent/services/dialogue_draft_stub.py`
  - `DialogueDraftStub`
  - `DialogueDraftStubService`

## Data Contracts

- `docs/data_contracts/relationship_context_bundle_contract.md`
- `docs/data_contracts/dialogue_context_plan_contract.md`
- `docs/data_contracts/dialogue_draft_stub_contract.md`

## Verification Evidence

Fresh T273 verification command:

```text
$env:PYTHONPATH='src'
pytest tests\test_relationship_context_bundle_schema.py tests\test_dialogue_context_planner.py tests\test_dialogue_draft_stub.py -q -o cache_dir=artifacts\t273_pytest_cache --basetemp=artifacts\t273_pytest_basetemp
```

Result: passed, `16 passed`.

Fresh diff check:

```text
git diff --check
```

Result: passed.

Additional worker-level evidence is recorded in:

- `docs/worker_summary/T270_worker_summary.md`
- `docs/worker_summary/T271_worker_summary.md`
- `docs/worker_summary/T272_worker_summary.md`

## Review-First Dialogue Boundary Assessment

M16 is safe to treat as a local review-first dialogue foundation because:

- relationship context requires a runtime-ready PersonaCard;
- factual context rejects imagined memory;
- relationship dimensions reject retention, engagement, and manipulation score
  names;
- planner output is deterministic metadata, not final reply text;
- imagined memory produces explicit labeling and non-factual-use notes;
- high boundary risk produces caution and pressure-avoidance warnings;
- draft stubs are deterministic and always require review;
- services expose no send, schedule, delivery, runtime, platform, or LLM-call
  methods;
- tests check for absence of reply/delivery/platform fields and dependency
  language.

## Explicit Non-Actions

M16 did not implement:

- private chat-log ingestion;
- real-person clone behavior or identity simulation;
- LLM calls or model-provider integration;
- production reply generation;
- retrieval ranking or memory selection;
- proactive candidates;
- quiet-hours, frequency, or consent policy;
- schedulers, outbound requests, delivery adapters, platform integration, or
  automatic sending;
- voice, avatar, video, Live2D, or social-feed behavior;
- product UI or web demo.

## Residual Risks

- Context packaging, planning, and draft stubs are deterministic foundations,
  not product-quality dialogue.
- RelationshipState remains the earlier local schema and is not yet updated by
  live interaction loops.
- Memory retrieval input is accepted as a prebuilt bundle; M16 does not perform
  retrieval ranking or selection.
- Human review is represented by schema and service boundaries, but no review
  UI exists yet.
- Proactive behavior is completely unopened until M17.

## M17 Entry Recommendation

Proceed to M17 with T280 ProactiveConsent schema work only. The first M17 task
should define explicit consent, review-only surface limits, quiet-hours fields,
frequency caps, revocation/pause fields, and schema-level invariants. It should
not generate proactive candidates, schedule anything, send anything, call LLMs,
or integrate with platforms.

## Reviewer Recommendation

Reviewer should mark M16 as PASS_WITH_WARNINGS if the fresh tests pass and diff
check is clean. Reviewer should BLOCK only if a later diff introduces runtime
reply generation, LLM calls, private readers, proactive sending, scheduler or
delivery behavior, platform integration, deceptive identity simulation, or
imagined-to-factual contamination.
