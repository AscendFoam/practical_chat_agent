# Text-First Life Stream Contract

Task: T323 Life Stream Prototype
Status: worker draft for review

## Scope

`TextFirstLifeStreamPrototype` projects already-created `RoleDynamicPost`
records into private, review-only text-first life-stream states. It is local and
deterministic.

It does not create posts, publish content, share content, export files, schedule
work, send messages, call model providers, mutate memory/persona records, or
integrate with external platforms.

Implemented objects:

- `TextFirstLifeStreamRequest`
- `TextFirstLifeStreamItem`
- `TextFirstLifeStreamState`
- `TextFirstLifeStreamPrototype`

Implementation entry point:

- `practical_chat_agent.ui.text_first_life_stream.TextFirstLifeStreamPrototype`

## TextFirstLifeStreamRequest

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `text_first_life_stream_request_v1`. |
| `user_id` | Owner user id. |
| `posts` | Existing `RoleDynamicPost` records. |
| `aigc_export_share_consent_active` | Whether future leave-local-review consent is active. |
| `metadata_label_ready` | Whether implicit/metadata labeling is ready. |

## TextFirstLifeStreamItem

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `text_first_life_stream_item_v1`. |
| `post_id` | Source role dynamic post id. |
| `persona_id` | Source persona id. |
| `content_text` | Synthetic imagined post text. |
| `content_status` | Must remain `imagined_ai_generated`. |
| `truth_disclosure` | Must disclose imagined AI-generated content. |
| `review_status` | Source review status. |
| `visibility` | Must remain local/private review. |
| `memory_refs` | Source memory refs. |
| `memory_ref_usage` | Must remain `inspiration_only`. |
| `relationship_context_refs` | Source relationship context refs. |
| `source_prompt_summary` | Redacted seed summary. |
| `aigc_label` | Visible AIGC label requirement. |
| `contains_factual_claims` | Whether the draft contains factual claims. |
| `factual_claims_review_notes` | Required review notes for factual claims. |
| `review_required` | Always true. |
| `review_notes` | Local review reason labels. |
| `leaving_local_review_blocked` | Whether copy/download/export/share is blocked. |
| `block_reasons` | Missing consent/metadata reason labels. |

## State Rules

- Every post becomes a private `life_stream_review` item.
- Every item carries `AIGCLabelingRequirement` with
  `content_modality=role_dynamic_post` and `product_surface=role_dynamic_post`.
- AIGC labels include imagined/not-real-world disclosure.
- Memory refs remain inspiration only.
- Factual-claim posts preserve factual-claim review notes and remain imagined.
- Leaving local review is blocked unless both AIGC export/share consent and
  metadata labeling are ready.

## Invariants

- Life-stream items remain private review artifacts.
- Generated posts are imagined AI-generated content.
- Not-real-world labels are visible.
- Memory refs are never factual proof of a real event.
- Factual claims require review notes and do not promote the post to factual
  memory.
- Copy/download/export/share states default to blocked.
- Payloads contain no publish, send, schedule, delivery, platform, webhook,
  token, or queue fields.
- The prototype exposes no publish, share, export, send, schedule, delivery,
  execution, or runtime methods.

## Non-Actions

T323 does not implement:

- frontend code;
- browser demo;
- post generation;
- LLM calls;
- private chat-log reads;
- real-world activity claims;
- memory/persona mutation;
- persistence;
- copy/download/export/share writing;
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
python -m py_compile src\practical_chat_agent\ui\text_first_life_stream.py src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_life_stream_prototype.py tests\test_role_dynamic_post_schema.py tests\test_virtual_life_engine_text_generator.py tests\test_aigc_labeling_plan_contract.py -q
```

```powershell
git diff --check
```
