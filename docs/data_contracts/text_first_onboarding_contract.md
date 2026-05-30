# Text-First Onboarding Contract

Task: T321 Onboarding And Persona Creation Prototype
Status: worker draft for review

## Scope

`TextFirstOnboardingPrototype` projects local onboarding and persona creation
requests into reviewable text-first states. It is a state/projection contract,
not a frontend, chat runtime, persistence layer, model-provider integration, or
platform connector.

Implemented objects:

- `OnboardingPersonaRequest`
- `TextFirstOnboardingState`
- `TextFirstOnboardingPrototype`

Implementation entry point:

- `practical_chat_agent.ui.text_first_onboarding.TextFirstOnboardingPrototype`

## OnboardingPersonaRequest

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `onboarding_persona_request_v1`. |
| `user_id` | Owner user id. |
| `creation_mode` | One `PersonaCreationMode`. |
| `display_name` | Optional requested persona display name. |
| `description` | Synthetic persona description. |
| `ai_identity_acknowledged` | Whether the AI identity disclosure was acknowledged. |
| `style_inspiration_gate_refs` | Reserved future deidentification/consent gate refs. |

Supported active creation modes:

- `detailed_prompt`
- `fuzzy_preference`
- `template`
- `random_seed`

`style_inspiration` remains locked by default in T321.

## TextFirstOnboardingState

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `text_first_onboarding_state_v1`. |
| `state_id` | Generated local onboarding state id. |
| `user_id` | Owner user id. |
| `screen` | `ai_identity_disclosure`, `persona_draft_review`, `persona_blocked`, or `style_inspiration_locked`. |
| `ai_identity_disclosure_required` | Always true. |
| `ai_identity_disclosure_text` | Visible AI/synthetic/not-human boundary copy. |
| `creation_mode` | Current creation mode when applicable. |
| `persona_preview` | Candidate or rejected `PersonaCard` preview. |
| `persona_label` | AIGC label requirement for the persona card. |
| `virtual_history_label` | AIGC label requirement for imagined virtual history. |
| `blocked_reasons` | Deterministic blocked-state reason labels. |
| `consent_review_required_scopes` | Consent scopes to review before enabling related features. |
| `review_required` | Always true. |

## State Transitions

### Initial State

`TextFirstOnboardingPrototype.initial_state(user_id=...)` returns:

- `screen=ai_identity_disclosure`;
- AI-generated/synthetic/not-human boundary text;
- `review_required=true`;
- no persona preview.

### Safe Persona Creation

`create_persona(...)` with a safe creation mode:

- calls `PersonaCompilerService.compile(...)`;
- returns `screen=persona_draft_review`;
- includes a candidate `PersonaCard`;
- includes `persona_label` with `content_modality=persona`;
- includes `virtual_history_label` with `content_modality=virtual_history`;
- requires review for memory, proactive messaging, and AIGC export/share
  consent scopes.

### Blocked Persona Creation

Real-person clone, deceased-person, public-figure, voice/face/deepfake,
impersonation, or automatic outbound-like requests return:

- `screen=persona_blocked`;
- rejected L5 persona preview;
- deterministic blocked reason;
- no runtime-ready persona.

### Style Inspiration

`creation_mode=style_inspiration` returns:

- `screen=style_inspiration_locked`;
- no persona preview;
- `style_inspiration_gate_required`;
- consent review requirement for persona distillation, memory, and AIGC
  export/share.

## Invariants

- AI identity disclosure is the first state.
- Every state remains human-review-required.
- Safe creation modes produce draft persona review states, not runtime-ready
  companions.
- Style inspiration remains locked by default.
- Rejected `PersonaCard` previews remain L5 and not runtime-ready.
- Persona and virtual-history previews carry visible AIGC labels.
- Virtual history labels include imagined/not-real-world disclosure.
- Payloads contain no raw private chat text.
- Payloads expose no send, schedule, delivery, platform, webhook, token, or
  queue fields.
- The prototype exposes no chat, send, schedule, delivery, execution, export,
  share, or runtime methods.

## Non-Actions

T321 does not implement:

- frontend code;
- browser demo;
- chat runtime;
- reply generation;
- LLM calls;
- private chat-log reads;
- real persona distillation;
- deidentification or similarity scoring;
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
python -m py_compile src\practical_chat_agent\ui\text_first_onboarding.py src\practical_chat_agent\services\persona_compiler.py src\practical_chat_agent\core\models.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_onboarding_prototype.py tests\test_persona_compiler.py tests\test_aigc_labeling_plan_contract.py tests\test_consent_center_data_model.py -q
```

```powershell
git diff --check
```
