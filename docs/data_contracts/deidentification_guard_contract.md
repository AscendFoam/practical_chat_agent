# Deidentification Guard Contract

Task: T252 Synthetic Deidentification Guard Tests
Status: worker draft for review

## Scope

The T252 `DeidentificationGuard` is a deterministic local classifier for
synthetic examples. It is a test-first safety boundary for future L2 abstract
style inspiration work. It does not authorize reading private chat logs, style
extraction from real people, similarity scoring, PersonaCard runtime use, or
LLM-assisted deidentification.

Implementation entry point:

- `practical_chat_agent.services.deidentification_guard.DeidentificationGuard`
- `DeidentificationGuard.assess(text) -> DeidentificationGuardDecision`

## Input

`assess(text)` accepts one synthetic text string that may describe abstract
style preferences or unsafe identifying source material.

Allowed abstract style examples:

- concise;
- warm;
- delayed response;
- dry humor;
- practical;
- gentle.

The guard treats the input as untrusted and never retains raw source text in the
decision object.

## Output

`DeidentificationGuardDecision` fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Always `deidentification_guard_decision_v1`. |
| `allowed` | `true` only when no risk flags are present. |
| `risk_flags` | Machine-readable synthetic risk flags. |
| `safe_summary` | Abstract style summary or a blocked placeholder. |
| `blocked_reason` | Human-readable reason when blocked. |
| `source_text_retained` | Always `false` in T252. |

## Risk Flags

The T252 guard can emit:

- `direct_identifier`
- `contact_identifier`
- `location_identifier`
- `org_school_identifier`
- `handle_identifier`
- `voice_biometric`
- `face_biometric`
- `image_biometric`
- `real_person_avatar`
- `private_event`
- `exact_biography`
- `clone_intent`
- `distinctive_catchphrase`

Any flag makes the decision blocked.

## Safe Summary Behavior

Allowed decisions summarize only abstract style labels, such as:

```text
concise, warm, delayed_response, dry_humor
```

Blocked decisions do not echo names, phone numbers, addresses, dates, private
events, voice/face terms, quoted catchphrases, or other source text. They return
either:

```text
blocked_identifying_input; retained abstract signals: ...
```

or:

```text
blocked_identifying_input; no safe abstract style summary available
```

## Non-Actions

T252 does not implement:

- private file reads;
- chat-log ingestion;
- real deidentification quality guarantees;
- similarity scoring against a real person;
- LLM calls;
- embeddings;
- PersonaCard generation;
- runtime dialogue;
- proactive behavior;
- outbound sending;
- platform integration;
- voice/avatar/deepfake processing.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\deidentification_guard.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_deidentification_guard.py tests\test_persona_compiler.py -q
```

```powershell
git diff --check
```
