# Persona Review Card Contract

Task: T253 Persona Review Card Contract
Status: worker draft for review

## Scope

The T253 review service renders `PersonaCard v1` records into local,
inspectable review payloads and applies explicit human review decisions. It
does not create personas, call LLMs, persist versions, wire personas into
dialogue, enable proactive behavior, or send anything to any platform.

Implementation entry points:

- `practical_chat_agent.services.persona_review.PersonaReviewService`
- `PersonaReviewService.render(card) -> PersonaReviewCard`
- `PersonaReviewService.review(card, decision, reviewer_id, ...) -> PersonaCard`

## Review Payload

`PersonaReviewCard` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_review_card_v1`. |
| `persona_id` | Source PersonaCard id. |
| `user_id` | Synthetic/local user id. |
| `display_name` | Persona display name. |
| `status` | Current PersonaCard status. |
| `truth_disclosure` | AI/fictional disclosure. |
| `source_policy` | Source type, risk tier, consent, block metadata. |
| `identity` | Fictional identity fields. |
| `traits` | Bounded trait values. |
| `speech_style` | Style labels and taboo phrases. |
| `virtual_history` | Imagined virtual-history fields. |
| `growth_policy` | Frozen/mutable fields and review triggers. |
| `proactive_preferences` | Proactive preferences, default-off. |
| `safety_policy` | Required safety flags. |
| `blocked_reason` | Prohibited reason when present. |
| `allowed_review_decisions` | `approve`, `reject`, `freeze`, `request_changes`. |
| `runtime_ready` | Current `PersonaCard.is_runtime_ready()` result. |
| `warnings` | Local warning labels such as prohibited request. |

## Redaction Behavior

For `source_policy.source_type="prohibited"`, the rendered review card replaces
virtual-history background with:

```text
[redacted_blocked_request]
```

The T253 service does not echo raw unsafe input. It may expose a generic
`blocked_reason` such as `real-person clone request prohibited` so reviewers can
understand why the card is blocked.

## Review Decisions

`review()` requires a non-empty `reviewer_id`.

Decision mapping:

| Input decision | PersonaCard status |
| --- | --- |
| `approve` | `approved` |
| `reject` | `rejected` |
| `freeze` | `frozen` |
| `request_changes` | `candidate` |

Review decisions update:

- `review_metadata.review_state="reviewed"`;
- `review_metadata.reviewed_by_human=true`;
- `review_metadata.last_decision`;
- `review_metadata.last_reviewed_at`;
- `review_metadata.last_reviewer_id`;
- `review_metadata.last_reviewer_name`;
- `review_metadata.history`;
- `updated_at`.

`review()` returns a new `PersonaCard` via copy semantics and does not mutate
the original card in place.

## Approval Gate

The service refuses to approve a card when:

- source type is `prohibited`;
- risk tier is not `L1` or `L2`;
- `blocked_real_person_similarity=true`;
- identity is not fictional;
- identity references a public or real person;
- no-deception or no-unauthorized-clone safety flags are disabled.

Even after approval, runtime readiness is still decided by
`PersonaCard.is_runtime_ready()`.

## Non-Actions

T253 does not implement:

- PersonaCard storage;
- version history;
- CLI or UI;
- LLM calls;
- private chat-log reads;
- runtime dialogue;
- memory retrieval;
- proactive candidates;
- schedulers;
- outbound requests;
- platform integration;
- voice/avatar/deepfake behavior.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_review.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_review.py tests\test_persona_compiler.py tests\test_deidentification_guard.py -q
```

```powershell
git diff --check
```
