# Persona Version Editor Contract

Task: T302 Persona Version Editor Contract
Status: worker draft for review

## Scope

The persona version editor contract represents local, draft-only edit
proposals for `PersonaCard` records. It gives a future UI or control surface a
typed payload for review, but it does not mutate `PersonaCard`, write
`PersonaVersionStore` records, call an LLM, read private chat logs, or create
outbound/platform actions.

Implementation objects:

- `PersonaEditFieldChange`
- `PersonaVersionEditProposal`
- `PersonaVersionEditReview`

## PersonaEditFieldChange

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_edit_field_change_v1`. |
| `field_path` | Dot path to the proposed `PersonaCard` field. |
| `old_value_summary` | Human-readable summary of the current value. |
| `proposed_value_summary` | Human-readable summary of the proposed value. |
| `reason` | Human-readable reason for the change. |
| `risk_labels` | Review labels such as `tone_shift`, `real_person_similarity`, or `unsafe_content`. |
| `requires_review` | Derived true when the field path or labels require human review. |
| `review_required_reasons` | Derived reasons such as `identity_field_change` or `safety_policy_change`. |
| `blocks_auto_approval` | Derived true when blocking risk labels are present. |
| `blocking_risk_labels` | Derived subset of risk labels that block approval. |

Identity, source-policy, and safety-policy paths require review:

- `display_name`
- `identity.*`
- `source_policy.*`
- `safety_policy.*`

The contract rejects field paths that target delivery or platform surfaces such
as send, schedule, delivery, platform, webhook, token, or queue fields.

## PersonaVersionEditProposal

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_version_edit_proposal_v1`. |
| `proposal_id` | Generated local proposal id. |
| `user_id` | Source persona owner. |
| `source_persona_id` | Source `PersonaCard.persona_id`. |
| `source_persona_version` | Source `PersonaCard.version`. |
| `source_persona_schema_version` | Source card schema version. |
| `requested_by` | Local actor that requested the draft proposal. |
| `proposal_reason` | Human-readable proposal reason. |
| `changes` | Non-empty list of `PersonaEditFieldChange` records. |
| `proposal_state` | Always `draft_review_only`. |
| `human_review_required` | Always true. |
| `auto_approval_allowed` | Always false. |
| `auto_approval_blocked` | Always true for this review-only contract. |
| `auto_apply_allowed` | Always false. |
| `writes_persona_version` | Always false. |
| `blocking_risk_labels` | Aggregated blocking labels from changes. |
| `review_required_reasons` | Aggregated review reasons from changes. |
| `created_at` | Creation timestamp. |

`PersonaVersionEditProposal.from_persona_card()` copies only id, version, user,
and schema metadata from the source card. It does not edit the source object and
does not write a new version.

## PersonaVersionEditReview

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `persona_version_edit_review_v1`. |
| `review_id` | Generated local review id. |
| `proposal_id` | Reviewed proposal id. |
| `reviewer_id` | Human reviewer id. |
| `decision` | `approved_for_manual_apply`, `rejected`, or `needs_changes`. |
| `notes` | Human review notes. |
| `blocking_risk_labels` | Blocking labels inherited from the proposal. |
| `auto_apply_allowed` | Always false. |
| `approved_for_auto_apply` | Always false. |
| `writes_persona_version` | Always false. |
| `reviewed_at` | Review timestamp. |

`PersonaVersionEditReview.from_proposal()` carries proposal risk labels into the
review. A proposal with blocking labels such as `real_person_similarity` or
`unsafe_content` cannot receive `approved_for_manual_apply` under this contract.

## Invariants

- Proposals are draft/review-only and cannot apply changes.
- Reviews are review records only and cannot write persona versions.
- The source persona id and source version are preserved.
- Old and proposed values are summaries, not raw private chat content.
- Identity/source-policy/safety changes require review.
- Unsafe content, real-person similarity, unauthorized clone, deception, and
  public-person reference labels block approval.
- Payloads expose no send, schedule, delivery, platform, webhook, token, or
  queue fields.

## Non-Actions

T302 does not implement:

- UI;
- APIs;
- persistence;
- version-store writes;
- actual persona mutation;
- automatic approval;
- LLM calls;
- private chat-log reads;
- memory retrieval changes;
- proactive candidates;
- schedulers;
- outbound requests;
- platform integration;
- voice/avatar/deepfake behavior;
- web demo behavior.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_version_editor_contract.py tests\test_persona_card_schema.py tests\test_persona_version_store.py -q
```

```powershell
git diff --check
```
