# Task T162: Patch Proposal CLI

## Task ID

T162

## Goal

Generate `PreferencePatchCandidate` records from validated feedback clusters.

This task may optionally use an LLM only if the task package is updated by Captain to allow it at execution time. Default implementation should be deterministic/rule-based.

## Why Now

After feedback is captured, validated, summarized, and clustered, repeated patterns can become reviewable preference/boundary patch candidates.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not auto-approve or apply patches.
- Do not modify ContactSkill, MemoryFact, approved store records, or planner templates.
- Do not add platform integration or sending.
- Do not read private chat history.
- Do not claim generated patches are true relationship facts; they are candidate communication preferences.

## Expected Output

CLI should produce candidate patch JSON under a private path:

```text
chat-feedback-propose-patch --feedback-log <path> --output <private path>
```

Each patch must reference supporting feedback ids and remain `status = candidate`.

## Verification

- Generate patch candidates from synthetic clusters.
- Confirm patches include supporting feedback ids.
- Confirm no patch is automatically approved or injected into runtime context.

## Reviewer Type

adversarial
