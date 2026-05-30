# Dialogue Context Plan Contract

Task: T271 Dialogue Context Planner
Status: worker draft for review

## Scope

`DialogueContextPlanner` converts a `RelationshipContextBundle` into
non-generative planning metadata. It does not call LLMs, generate final replies,
schedule proactive messages, send messages, or connect to external platforms.

Implementation entry point:

- `practical_chat_agent.services.dialogue_context_planner.DialogueContextPlanner`
- `DialogueContextPlanner.plan(bundle) -> DialogueContextPlan`

## Plan Model

`DialogueContextPlan` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `dialogue_context_plan_v1`. |
| `plan_id` | Generated `dlgplan_` id. |
| `context_bundle_id` | Source relationship context bundle id. |
| `tone_guidance` | Deterministic tone label. |
| `response_length_guidance` | Length guidance label. |
| `boundary_reminders` | Boundary reminders. |
| `memory_use_notes` | Memory truth/provenance usage notes. |
| `relationship_pacing_notes` | Pacing notes derived from relationship dimensions. |
| `safety_warnings` | Safety warning labels. |

## Deterministic Rules

- High `boundary_risk` -> `cautious_warm`, boundary-sensitive reminder, and
  pressure/escalation warning.
- High trust and warmth -> `warm_personal` plus slow-warmth pacing.
- Otherwise -> `steady_warm` plus gradual pacing.
- Factual memory context adds `use_evidence_backed_memory_only`.
- Any imagined memory context adds `imagined_memory_label_required`.
- All plans include `do_not_treat_imagined_memory_as_fact`.

## Non-Actions

T271 does not implement:

- reply text generation;
- LLM calls;
- retrieval ranking;
- memory selection;
- proactive candidates;
- outbound sending;
- platform integration;
- voice/avatar/video behavior;
- web demo.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\dialogue_context_planner.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_dialogue_context_planner.py tests\test_relationship_context_bundle_schema.py -q
```

```powershell
git diff --check
```
