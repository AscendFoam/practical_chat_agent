# Relationship Context Bundle Contract

Task: T270 Relationship Context Bundle
Status: worker draft for review

## Scope

`RelationshipContextBundle` packages approved PersonaCard, RelationshipState,
and MemoryRetrievalBundle data into a local reviewable context object. It is
schema-only. It does not call LLMs, generate replies, schedule proactive
messages, send messages, or integrate with external platforms.

Implemented models:

- `RelationshipContextPersonaSnapshot`
- `RelationshipContextMemorySnapshot`
- `RelationshipContextBundle`

## Persona Snapshot

Fields:

- `persona_id`
- `display_name`
- `truth_disclosure`
- `source_risk_tier`
- `runtime_ready`
- `safety_warnings`

`from_persona_card(...)` copies source policy and safety warnings from
PersonaCard. The bundle rejects snapshots where `runtime_ready=false`.

## Memory Snapshot

Fields:

- `bundle_id`
- `purpose`
- `selected_memory_ids`
- `truth_status_counts`
- `imagined_memory_count`
- `safety_warnings`

For `purpose="factual_response"`, imagined memory count must be zero.

## Relationship Dimensions

`relationship_dimensions` stores the existing RelationshipState dimensions:

- familiarity;
- trust;
- warmth;
- reciprocity;
- conflict_level;
- boundary_risk;
- initiative_allowance;
- intimacy_level.

The schema rejects retention/manipulation/engagement score names.

## Invariants

- Non-runtime-ready PersonaCard is rejected.
- Imagined memory cannot be included as factual context.
- Relationship dimensions cannot include retention or manipulation scores.
- Bundle contains no draft reply, send, schedule, delivery, platform, or webhook
  fields.

## Non-Actions

T270 does not implement:

- LLM calls;
- reply generation;
- dialogue planning;
- retrieval ranking;
- private readers;
- proactive candidates;
- outbound sending;
- platform integration;
- voice/avatar/video behavior;
- web demo.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_relationship_context_bundle_schema.py tests\test_persona_card_schema.py tests\test_memory_retrieval_bundle_schema.py -q
```

```powershell
git diff --check
```
