# Task T141: Feedback To Proposal

## Task ID

T141

## Goal

把用户 edit/reject/boundary feedback 转成可审阅的 preference/boundary/memory update proposal。

## Why now

这让 agent 越用越贴合用户，而不是把反馈埋在日志里。

## Allowed files

- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/services/contact_skill.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不自动 approve proposal。
- 不用无证据反馈覆盖历史事实。

## Inputs to read

- T140 feedback records.
- ContactSkill schema.

## Expected output

- Proposal includes target skill/memory field, rationale, evidence feedback ref, status candidate.

## Verification

Run on redacted edited draft pair.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

