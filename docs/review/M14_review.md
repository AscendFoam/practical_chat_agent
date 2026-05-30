# M14 Review: Persona Compiler Foundation

## Status

Gate recommendation: PASS_WITH_WARNINGS for entering M15 Memory OS v2.

M14 implemented a local, synthetic, review-first Persona Compiler foundation.
It did not implement a runtime companion product, real-person clone system,
proactive engine, voice/avatar system, or platform integration.

## Task Coverage

| Task | Result | Evidence |
| --- | --- | --- |
| T250 PersonaCard v1 schema | Implemented | `PersonaCard` and policy models in `core/models.py`; `tests/test_persona_card_schema.py`. |
| T251 local Persona Compiler prototype | Implemented | `PersonaCompilerService`; `tests/test_persona_compiler.py`. |
| T252 synthetic deidentification guard | Implemented | `DeidentificationGuard`; `tests/test_deidentification_guard.py`. |
| T253 Persona review card | Implemented | `PersonaReviewService`; `tests/test_persona_review.py`. |
| T254 local version store | Implemented | `PersonaVersionStore`; `tests/test_persona_version_store.py`. |

## Implemented Code

- `src/practical_chat_agent/core/models.py`
  - `PersonaCard`
  - `PersonaSourcePolicy`
  - `PersonaIdentity`
  - `PersonaTraitProfile`
  - `PersonaSpeechStyle`
  - `PersonaEmotionModel`
  - `PersonaRelationshipModel`
  - `PersonaVirtualHistory`
  - `PersonaGrowthPolicy`
  - `PersonaProactivePreferences`
  - `PersonaSafetyPolicy`
- `src/practical_chat_agent/services/persona_compiler.py`
- `src/practical_chat_agent/services/deidentification_guard.py`
- `src/practical_chat_agent/services/persona_review.py`
- `src/practical_chat_agent/services/persona_version_store.py`

## Data Contracts

- `docs/data_contracts/persona_card_v1_contract.md`
- `docs/data_contracts/persona_compiler_contract.md`
- `docs/data_contracts/deidentification_guard_contract.md`
- `docs/data_contracts/persona_review_card_contract.md`
- `docs/data_contracts/persona_version_store_contract.md`

## Verification Evidence

Fresh T255 verification command:

```text
$env:PYTHONPATH='src'
pytest tests\test_persona_card_schema.py tests\test_persona_compiler.py tests\test_deidentification_guard.py tests\test_persona_review.py tests\test_persona_version_store.py -q -o cache_dir=artifacts\t255_pytest_cache --basetemp=artifacts\t255_pytest_basetemp
```

Result: passed, `44 passed`.

Additional worker-level evidence is recorded in:

- `docs/worker_summary/T250_worker_summary.md`
- `docs/worker_summary/T251_worker_summary.md`
- `docs/worker_summary/T252_worker_summary.md`
- `docs/worker_summary/T253_worker_summary.md`
- `docs/worker_summary/T254_worker_summary.md`

## Safety Boundary Assessment

M14 is safe to treat as a local foundation because:

- PersonaCard v1 is AI/fictional-disclosed by default.
- L1 original fictional personas are the only compiled happy path.
- L2 style inspiration remains guarded by synthetic tests and is not wired into
  PersonaCard compilation.
- L3/L4 are not runtime-ready in v1.
- L5 prohibited requests are rejected and never runtime-ready.
- Proactive preferences are default-off and cannot enable sending.
- Review-card approval requires explicit reviewer id and blocks unsafe cards.
- Version store is caller-path local JSON and has no runtime or delivery hooks.
- Tests assert no send, schedule, delivery, runtime, private corpus, or private
  chat-history extraction methods on new services.

## Explicit Non-Actions

M14 did not implement:

- LLM persona generation;
- private chat-log reads;
- real-person style extraction;
- real deidentification quality guarantees;
- similarity scoring against a real person;
- runtime dialogue consumption;
- Memory OS v2;
- proactive candidates;
- schedulers;
- outbound requests;
- external platform delivery;
- voice clone;
- face/avatar deepfake;
- Live2D or video simulation;
- product UI or web demo.

## Residual Risks

- Persona quality is still shallow because the compiler is deterministic keyword
  mapping.
- The deidentification guard is synthetic and conservative, not a production
  deidentification system.
- Review and version store services are local APIs, not user-facing UX.
- Approval can make safe L1 cards runtime-ready under schema rules, but no
  dialogue engine consumes PersonaCard yet.
- Storage lacks encryption, concurrency control, access control, retention
  policy, and cloud sync.
- Legal/compliance interpretation remains non-authoritative.

## M15 Entry Recommendation

Proceed to M15 Memory OS v2 with a schema-first, test-first task. M15 should
define memory events and strict separation among:

- factual memory;
- inferred memory;
- relational memory;
- procedural memory;
- imagined memory.

M15 must preserve the core rule that imagined persona or virtual-life content
cannot be retrieved as factual evidence about a real user or real person.

## Reviewer Recommendation

Reviewer should mark M14 as PASS_WITH_WARNINGS if the fresh tests pass and
diff check is clean. Reviewer should BLOCK only if a later diff introduces
private reads, runtime persona consumption, proactive sending, platform
integration, or real-person clone capability into M14.
