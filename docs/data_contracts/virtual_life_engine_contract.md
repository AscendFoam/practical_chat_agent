# Virtual Life Engine Contract

Task: T291 Virtual Life Engine Text Generator
Status: worker draft for review

## Scope

`VirtualLifeEngine` creates deterministic local `RoleDynamicPost` drafts from
already-provided seed metadata. It does not call LLMs, publish posts, send
messages, schedule work, or integrate with external platforms.

Implemented objects:

- `VirtualLifeSeedContext`
- `VirtualLifeEngine`

## Seed Context

`VirtualLifeSeedContext` fields:

| Field | Meaning |
| --- | --- |
| `user_id` | Owner user id. |
| `persona_id` | Persona id. |
| `mood_label` | Caller-provided mood label. |
| `activity_label` | Caller-provided activity label. |
| `topic_label` | Caller-provided topic label. |
| `memory_refs` | Memory ids used as inspiration references only. |
| `relationship_context_refs` | Relationship context ids. |
| `safety_notes` | Optional review labels. |

## Deterministic Output

`VirtualLifeEngine.create_post(context)` returns `RoleDynamicPost` with:

- deterministic text from mood/activity/topic labels;
- imagined AI-generated content status;
- explicit imagined-content truth disclosure;
- explicit AIGC disclosure metadata;
- review-required status;
- local private review visibility;
- copied memory and relationship context refs;
- `memory_ref_usage=inspiration_only`;
- caller labels copied as safety notes.

## Invariants

- The engine consumes seed metadata only.
- The engine does not retrieve memories.
- Memory refs are inspiration references only.
- Engine-created posts cannot be promoted to factual memory via
  `imagined_generation` provenance.
- Output remains imagined and review-only.
- Output preserves AIGC disclosure metadata for downstream review surfaces.
- Payloads contain no publish, send, schedule, delivery, platform, webhook,
  token, or queue fields.
- Service exposes no publish, send, schedule, delivery, execution, runtime, or
  LLM-call methods.

## Non-Actions

T291 does not implement:

- LLM calls;
- post publishing;
- social-feed integration;
- scheduling;
- automatic sending;
- outbound requests;
- platform adapters, webhooks, queues, push notifications, or delivery;
- review UI;
- voice/avatar/video behavior;
- Live2D behavior;
- product UI or web demo.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\virtual_life_engine.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_virtual_life_engine_text_generator.py tests\test_role_dynamic_post_schema.py -q
```

```powershell
git diff --check
```
