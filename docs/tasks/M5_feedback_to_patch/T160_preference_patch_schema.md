# Task T160: PreferencePatch Schema

## Task ID

T160

## Goal

Define `PreferencePatchCandidate` schema for turning repeated human feedback into reviewable communication-policy patches.

This task only defines models/contracts. It must not generate, approve, or apply patches.

## Why Now

M4 captures and summarizes feedback. The next safe step is to define a candidate patch shape that can later connect feedback to communication preferences without training, automatic memory mutation, or ContactSkill overwrite.

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/preference_patch_contract.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not call an LLM.
- Do not implement clustering, proposal generation, review CLI, or runtime injection.
- Do not modify ContactSkill/MemoryFact/store records.
- Do not auto-approve or apply patches.
- Do not read private chat history.

## Expected Output

Schema should support:

- `patch_id`
- `contact_id`
- `patch_type`
- `claim`
- `behavior_instruction`
- `positive_examples` / `negative_examples` as optional safe references or summaries
- `supporting_feedback_ids`
- `affected_candidate_types`
- `confidence`
- `sensitivity`
- `status = candidate`
- timestamps and review metadata placeholders

Suggested `patch_type` values:

- `tone_preference`
- `length_preference`
- `boundary_preference`
- `topic_preference`
- `question_style`
- `humor_style`
- `repair_style`
- `proactivity_preference`

## Verification

- Compile changed Python files.
- Validate one synthetic candidate patch with supporting feedback ids.
- Validate that empty supporting feedback ids are rejected or explicitly represented as unsafe.

## Reviewer Type

normal
