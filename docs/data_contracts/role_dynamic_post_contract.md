# Role Dynamic Post Contract

Task: T290 Role Dynamic Post Schema
Status: worker draft for review

## Scope

`RoleDynamicPost` defines text-first virtual life stream drafts for companion
personas. It is schema-only. It does not generate post text, publish posts,
send messages, call LLMs, or integrate with external platforms.

Implemented model:

- `RoleDynamicPost`

## Fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `role_dynamic_post_v1`. |
| `post_id` | Generated `rolepost_` id. |
| `user_id` | Owner user id. |
| `persona_id` | Persona id. |
| `content_text` | Reviewable draft text supplied by caller. |
| `content_status` | Always `imagined_ai_generated`. |
| `truth_disclosure` | Always `imagined_ai_generated_content`. |
| `review_status` | Defaults to `requires_review`. |
| `visibility` | Always `local_private_review`. |
| `memory_refs` | Optional memory ids used as inspiration references. |
| `relationship_context_refs` | Optional relationship context ids. |
| `source_prompt_summary` | Caller-supplied source summary. |
| `aigc_metadata` | Explicit AI-generated imagined-content disclosure metadata. |
| `contains_factual_claims` | Whether the draft contains factual claims. |
| `factual_claims_review_notes` | Required if factual claims are present. |
| `safety_notes` | Review labels or safety notes. |
| `created_at` / `updated_at` | Timestamps. |

## Invariants

- AIGC disclosure metadata includes `ai_generated`, `imagined_content`,
  `review_required`, and `not_real_world_activity`.
- AIGC disclosure text mentions AI-generated imagined content.
- Content status is imagined AI-generated.
- Truth disclosure is explicit.
- Review status defaults to review required.
- Visibility is local private review only.
- Empty content is rejected.
- Factual claims require review notes and do not promote the post to factual
  memory.
- Serialized posts contain no publish, send, schedule, delivery, platform,
  webhook, token, or queue fields.

## Non-Actions

T290 does not implement:

- post text generation;
- LLM calls;
- social-feed publishing;
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
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_role_dynamic_post_schema.py -q
```

```powershell
git diff --check
```
