# Text-First Chat Memory Contract

Task: T322 Chat Plus Memory Explanation Prototype
Status: worker draft for review

## Scope

`TextFirstChatMemoryPrototype` projects persona, memory viewer items, dialogue
planning metadata, AIGC labels, and crisis/dependency safety decisions into a
reviewable chat surface state. It is local and deterministic.

It does not build UI, generate final companion replies, mutate memory or persona
records, call LLMs, persist state, export/share content, schedule work, send
messages, or integrate with external platforms.

Implemented objects:

- `TextFirstPersonaSummary`
- `TextFirstMemoryExplanation`
- `TextFirstChatMemoryRequest`
- `TextFirstChatMemoryState`
- `TextFirstChatMemoryPrototype`

Implementation entry point:

- `practical_chat_agent.ui.text_first_chat_memory.TextFirstChatMemoryPrototype`

## TextFirstChatMemoryRequest

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `text_first_chat_memory_request_v1`. |
| `user_id` | Owner user id. |
| `persona` | Existing `PersonaCard` to summarize. |
| `memory_items` | Existing read-only `MemoryViewerItem` records. |
| `dialogue_plan` | Optional `DialogueContextPlan`. |
| `safety_decision` | Optional `CompanionSafetyDecision`. |

The request is metadata-only. It must not contain raw chat transcripts.

## TextFirstChatMemoryState

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `text_first_chat_memory_state_v1`. |
| `state_id` | Generated local state id. |
| `user_id` | Owner user id. |
| `screen` | `chat_review`, `chat_deescalated`, or `chat_blocked`. |
| `ai_identity_label` | AIGC label requirement for companion reply surfaces. |
| `persona_summary` | Compact persona id/name/truth/risk/review status. |
| `memory_explanations` | Memory summaries with truth/provenance and safety notes. |
| `factual_memory_ids` | Memory ids safe to treat as factual evidence. |
| `imagined_memory_ids` | Imagined memory ids. |
| `tone_guidance` | Dialogue tone guidance when supplied. |
| `memory_use_notes` | Memory-use safety notes. |
| `relationship_pacing_notes` | Pacing notes when supplied. |
| `safety_reasons` | Crisis/dependency safety reasons when supplied. |
| `allowed_response_posture` | Non-clinical response posture. |
| `has_generated_response` | Always false. |
| `review_required` | Always true. |

## State Rules

### Normal Chat Review

When no high-risk `CompanionSafetyDecision` is supplied:

- `screen=chat_review`;
- AI identity/AIGC label is visible;
- persona summary is present;
- memory explanations preserve truth status and provenance;
- no final reply text is generated.

### Memory Explanation

Every `MemoryViewerItem` becomes a `TextFirstMemoryExplanation`.

Rules:

- factual memory can appear in `factual_memory_ids` only if it is factual
  evidence and not imagined;
- imagined memory appears in `imagined_memory_ids`;
- imagined memory is forced to `is_factual_evidence=false`;
- `do_not_treat_imagined_memory_as_fact` is always present in memory-use notes;
- imagined memory adds `imagined_memory_label_required`.

### Safety Decisions

When `CompanionSafetyDecision.action=block`:

- `screen=chat_blocked`;
- safety reasons are copied;
- no final response is generated.

When `CompanionSafetyDecision.action=deescalate_for_review`:

- `screen=chat_deescalated`;
- safety reasons are copied;
- no final response is generated.

## Invariants

- AI identity label is present on every chat state.
- Persona summary is compact and does not embed raw persona source text.
- Memory explanations preserve provenance refs without raw transcripts.
- Imagined memory cannot be factual evidence.
- Dialogue notes are planning metadata only.
- Crisis/dependency decisions block or de-escalate the chat state.
- `has_generated_response=false` for every state.
- Payloads contain no raw private chat text.
- Payloads expose no draft reply, reply text, send, schedule, delivery,
  platform, webhook, token, or queue fields.
- The prototype exposes no chat, send, schedule, delivery, execution, runtime,
  reply-generation, or message-creation methods.

## Non-Actions

T322 does not implement:

- frontend code;
- browser demo;
- final reply generation;
- LLM calls;
- private chat-log reads;
- memory retrieval ranking;
- memory/persona mutation;
- persistence;
- export/share/download writing;
- proactive candidate generation;
- automatic sending or scheduling;
- platform integration;
- voice/avatar/video behavior;
- Live2D behavior;
- legal, clinical, app-store, or launch approval.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_chat_memory.py src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_chat_memory_prototype.py tests\test_memory_viewer_contract.py tests\test_dialogue_context_planner.py tests\test_crisis_dependency_policy.py -q
```

```powershell
git diff --check
```
