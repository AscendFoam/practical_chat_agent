# Dialogue Draft Stub Contract

Task: T272 Dialogue Draft Stub
Status: worker draft for review

## Scope

`DialogueDraftStubService` creates deterministic review-only draft objects from
`DialogueContextPlan` metadata. It is a local stub for future UI/demo rendering.
It does not call LLMs, send messages, schedule proactive behavior, or integrate
with external platforms.

Implementation entry point:

- `practical_chat_agent.services.dialogue_draft_stub.DialogueDraftStubService`
- `DialogueDraftStubService.create(plan) -> DialogueDraftStub`

## Draft Model

`DialogueDraftStub` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `dialogue_draft_stub_v1`. |
| `draft_id` | Generated `dlgstub_` id. |
| `plan_id` | Source DialogueContextPlan id. |
| `generator_type` | Always `deterministic_stub`. |
| `draft_text` | Deterministic stub text. |
| `tone_guidance` | Copied from plan. |
| `boundary_reminders` | Copied from plan. |
| `memory_use_notes` | Copied from plan. |
| `safety_warnings` | Copied from plan. |
| `requires_review` | Always true. |
| `review_notes` | Includes `review`. |

## Deterministic Draft Text

The stub selects a fixed phrase from plan tone guidance and appends a memory
use phrase. If imagined memory is present, draft text explicitly says imagined
context must be labeled as imagined.

This is not production dialogue quality and not LLM generation.

## Non-Actions

T272 does not implement:

- LLM calls;
- final user-visible reply generation;
- runtime dialogue;
- proactive candidates;
- outbound sending;
- scheduling;
- delivery adapters;
- platform integration;
- web demo.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\dialogue_draft_stub.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_dialogue_draft_stub.py tests\test_dialogue_context_planner.py -q
```

```powershell
git diff --check
```
