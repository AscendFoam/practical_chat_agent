# Memory Event v2 Contract

Task: T260 Memory Event Schema
Status: worker draft for review

## Scope

`MemoryEvent v2` is the base schema for Memory OS v2. It records typed memory
events with explicit truth status, provenance, sensitivity, lifecycle, and
retrieval permissions. It does not implement storage, retrieval ranking,
dialogue generation, proactive behavior, private chat-log ingestion, or
platform integration.

Implemented models:

- `MemoryEvent`
- `MemoryTruthStatus`
- `MemoryEventType`
- `MemoryProvenance`
- `MemoryLifecycleState`
- `MemoryRetrievalPermission`

## Memory Types And Truth Status

| Event type | Required truth status | Purpose |
| --- | --- | --- |
| `factual` | `evidence_backed` | Evidence-backed claim about user/persona interactions. |
| `inferred` | `inferred` | Explicit inference with confidence and rationale. |
| `relational` | `relationship_state` | Relationship dimensions such as trust, repair state, warmth, or boundaries. |
| `procedural` | `procedural_preference` | Preferences, habits, or behavior rules for interaction. |
| `imagined` | `imagined` | Fictional dreams, virtual-life events, role dynamics, or counterfactual simulations. |

The schema rejects mismatched event type and truth status.

## MemoryProvenance

Fields:

- `source_type`: `conversation`, `persona_card`, `user_edit`,
  `system_generated`, `imagined_generation`, or `synthetic_test`.
- `evidence_refs`
- `source_event_ids`
- `source_memory_ids`
- `source_persona_ids`
- `source_summary`

Factual memory requires at least one `evidence_ref`.

## MemoryRetrievalPermission

Fields:

- `allow_factual_retrieval`
- `allow_inferred_retrieval`
- `allow_relational_retrieval`
- `allow_procedural_retrieval`
- `allow_imagined_retrieval`
- `review_required`

If no explicit retrieval route is supplied, `MemoryEvent` assigns a default
route based on event type:

- factual -> factual retrieval;
- inferred -> inferred retrieval;
- relational -> relational retrieval;
- procedural -> procedural retrieval;
- imagined -> imagined retrieval.

Medium and high sensitivity memory defaults to `review_required=true`, making
it not retrieval-eligible until a later review flow explicitly changes policy.

## Required Invariants

- Factual memory requires `evidence_refs`.
- Inferred memory requires `confidence` and `inference_rationale`.
- Relational memory requires `relationship_dimensions`.
- Procedural memory requires `preference_labels` and does not become factual.
- Imagined memory requires `imagined_context_label`.
- Imagined memory cannot enable factual retrieval.
- Frozen, deleted, and archived memory is not retrieval-eligible.
- Raw transcript/private chat fields are not part of the schema.

## Retrieval Eligibility

`MemoryEvent.is_retrieval_eligible(context)` returns false when:

- lifecycle is `frozen`, `deleted`, or `archived`;
- `retrieval_permission.review_required=true`;
- the requested context is not allowed by retrieval permission.

This method is a schema-level gate only. T260 does not implement ranking,
selection, search, vector indexing, or runtime prompt construction.

## Non-Actions

T260 does not implement:

- memory store;
- retrieval ranking;
- vector search;
- private chat-log ingestion;
- LLM extraction;
- background consolidation;
- dreaming or virtual-life generation;
- dialogue runtime consumption;
- proactive candidates;
- outbound sending;
- platform integration.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_memory_event_schema.py tests\test_persona_card_schema.py -q
```

```powershell
git diff --check
```
