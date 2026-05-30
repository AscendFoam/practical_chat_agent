# Virtual Life Review Card Contract

Task: T294 Dynamic Review Card
Status: worker draft for review

## Scope

`VirtualLifeReviewCardService` renders local review artifacts from
`RoleDynamicPost` drafts. It does not generate posts, call LLMs, publish posts,
send messages, schedule work, or integrate with external platforms.

Implemented objects:

- `VirtualLifeReviewCard`
- `VirtualLifeReviewCardService`

## Card Fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `virtual_life_review_card_v1`. |
| `card_id` | Generated `vlcard_` id. |
| `post_id` | Source role dynamic post id. |
| `user_id` | Owner user id. |
| `persona_id` | Persona id. |
| `content_text` | Reviewable post draft text. |
| `content_status` | Imagined content status. |
| `truth_disclosure` | Imagined-content disclosure. |
| `review_status` | Source post review status. |
| `aigc_label` | AIGC label. |
| `disclosure_labels` | Explicit disclosure labels. |
| `disclosure_text` | Human-readable disclosure text. |
| `memory_refs` | Inspiration-only memory refs. |
| `memory_ref_usage` | Always `inspiration_only`. |
| `factual_claims_review_notes` | Review notes for factual claims. |
| `safety_notes` | Safety labels. |
| `review_actions` | Local review actions. |

## Review Actions

Allowed review actions:

- `approve_for_demo`
- `reject`
- `request_changes`
- `flag_factual_claims`

`approve_for_demo` means approval for local demo/review surfaces only. It is
not approval to publish, send, schedule, deliver, enqueue, webhook, notify, or
call any platform adapter.

## Rendering Rules

- Cards preserve post id, persona id, text, review status, AIGC labels,
  disclosure labels, memory refs, memory-ref usage, and safety notes.
- Posts with factual claims expose `flag_factual_claims`, `reject`, and
  `request_changes`.
- Posts without factual claims expose `approve_for_demo`, `reject`, and
  `request_changes`.
- Card payloads contain no publish, send, schedule, delivery, platform, webhook,
  token, or queue fields.
- Service exposes no publish, send, schedule, delivery, execution, runtime, or
  LLM-call methods.

## Non-Actions

T294 does not implement:

- post generation;
- LLM calls;
- publishing;
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
python -m py_compile src\practical_chat_agent\services\virtual_life_review_card.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_virtual_life_review_card.py tests\test_virtual_life_contamination.py tests\test_virtual_life_aigc_labeling.py -q
```

```powershell
git diff --check
```
