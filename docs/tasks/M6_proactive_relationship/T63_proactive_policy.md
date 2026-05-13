# Task T63: Proactive Policy

## Task ID

T63

## Goal

实现主动触发的退让、限频、禁用和 quiet-hours 验证。

## Why now

主动消息风险高，必须有退让机制才能进入 Gate 4。

## Allowed files

- `src/practical_chat_agent/services/policy.py`
- `src/practical_chat_agent/services/triggers.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`
- `docs/review/T63_milestone_review.md`

## Forbidden scope

- 不自动真实发送。
- 不忽略用户禁用的 trigger。

## Inputs to read

- T60-T62.
- `docs/06_eval_protocol.md` Gate 4.

## Expected output

- Consecutive no-reply lowers frequency or pauses trigger.
- quiet-hours produces draft-only/deferred action.
- user disable prevents new scheduled actions.

## Verification

Run fixture trigger scenarios and record Gate 4 review.

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/review/T63_milestone_review.md`

## Reviewer type

milestone

