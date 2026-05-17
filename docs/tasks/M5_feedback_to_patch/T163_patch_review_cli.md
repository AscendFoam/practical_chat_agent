# Task T163: Patch Review CLI

## Task ID

T163

## Goal

Implement manual review actions for `PreferencePatchCandidate`: approve, reject, freeze, archive.

## Why Now

Preference patches can influence future reply behavior only after human review. This mirrors the existing ContactSkill review philosophy.

## Allowed Files

- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not auto-approve patches.
- Do not modify ContactSkill/MemoryFact directly.
- Do not inject approved patches into `ChatContext`; that is T164.
- Do not call an LLM.
- Do not add sending or platform integration.

## Expected Output

CLI should support manual patch status transitions and preserve review metadata/history.

## Verification

- Approve/reject/freeze/archive synthetic patches.
- Confirm rejected/frozen/archived patches cannot become runtime-ready.
- Confirm review history is preserved.

## Reviewer Type

adversarial
