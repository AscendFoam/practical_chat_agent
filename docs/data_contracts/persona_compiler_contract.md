# Persona Compiler Contract

Task: T251 Local Prompt-To-Schema Persona Compiler Prototype
Status: worker draft for review

## Scope

The T251 Persona Compiler is a deterministic local service that converts
synthetic user persona descriptions into `PersonaCard v1` records. It exists to
prove the T250 schema can be populated safely for L1 fictional personas before
any LLM-assisted generation, private style extraction, deidentification guard,
version store, runtime dialogue, proactive behavior, or platform integration.

Implementation entry point:

- `practical_chat_agent.services.persona_compiler.PersonaCompilerService`
- `PersonaCompilerService.compile(payload) -> PersonaCard`

## Input Payload

The compiler accepts a mapping with these fields:

| Field | Required | Notes |
| --- | --- | --- |
| `user_id` | Yes | Synthetic user id for the generated card. |
| `display_name` | No | Defaults to `Fictional Companion` for safe L1 cards. |
| `creation_mode` | No | Defaults to `detailed_prompt`. T251 supports `detailed_prompt`, `fuzzy_preference`, `template`, and `random_seed`. |
| `description` | No | Synthetic free text used only for deterministic keyword mapping and safety blocking. |

`style_inspiration` is intentionally not accepted in T251 because L2
deidentification tests do not exist yet.

## Safe Output

For safe fictional input, `compile()` returns:

- `PersonaCard.schema_version="persona_card_v1"`;
- `status="candidate"`;
- `source_policy.source_type="original"`;
- `source_policy.risk_tier="L1"`;
- `identity.fictional=true`;
- `identity.public_person_or_real_person_reference=false`;
- imagined virtual history only;
- proactive preferences disabled by default;
- required safety flags enabled.

Keyword mapping is deliberately simple:

- calm descriptions set a calm baseline mood;
- concise or short descriptions set short-to-medium sentence length;
- dry humor maps to `speech_style.humor_type="dry"`;
- warm, kind, gentle, and comfort terms raise warmth;
- independent terms raise independence;
- practical or comfort terms choose practical comfort style.

The compiler does not claim full persona quality. It only creates an editable
candidate card for later review and UX tasks.

## Blocked Output

If the description contains high-risk signals, `compile()` returns a rejected
L5 `PersonaCard` instead of raising or generating a clone.

Blocked categories:

- real-person clone requests;
- public-figure, ex-partner, family, coworker, classmate, deceased-person, or
  chat-history clone signals;
- voice clone, face clone, real-person avatar, or deepfake requests;
- hidden impersonation requests;
- automatic sending or sending-without-review requests.

Blocked cards use:

- `status="rejected"`;
- `source_policy.source_type="prohibited"`;
- `source_policy.risk_tier="L5"`;
- `source_policy.blocked_real_person_similarity=true`;
- a `prohibited_reason`;
- fictional `Blocked Persona` identity.

L5 cards are never runtime-ready under `PersonaCard.is_runtime_ready()`.

## Surface Area

The T251 compiler exposes only `compile()`.

It does not expose:

- `send`;
- `schedule`;
- `deliver`;
- `execute`;
- `run_runtime`;
- `compile_from_chat_history`;
- `extract_from_private_chat`.

## Non-Actions

T251 does not implement:

- LLM calls;
- model provider access;
- browser or network automation;
- private chat-log reads;
- real-person style extraction;
- deidentification or similarity scoring;
- review UI;
- version persistence;
- runtime dialogue consumption;
- proactive candidates;
- platform delivery;
- voice/avatar/deepfake behavior.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\persona_compiler.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_persona_card_schema.py tests\test_persona_compiler.py -q
```

```powershell
git diff --check
```
