# Task T43: Approved Sources For Skills

## Task ID

T43

## Goal

确保 ContactSkill 生成优先使用 approved memory 和 trusted events，不直接依赖未审候选记忆。

## Why now

否则错误或未审记忆会污染联系人画像。

## Allowed files

- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/services/memory_retrieval.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不忽略 evidence refs。
- 不把 rejected/frozen/archived memory 用于 skill。

## Inputs to read

- T32 ContactSkill generation.
- T40 memory status implementation.

## Expected output

- Skill generation filters source memories by status.
- Output records source status and skipped counts.

## Verification

Fixture with approved and frozen memories; verify only approved facts influence skill.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

