# Task T40: Memory Status CLI

## Task ID

T40

## Goal

为记忆增加 status/metadata 过渡能力，并实现 freeze/archive/correct CLI。

## Why now

长期运行必须支持纠错和冻结错误记忆，否则 ContactSkill 和建议会持续使用错误事实。

## Allowed files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/storage/mysql/models.py`
- `src/practical_chat_agent/storage/mysql/repositories.py`
- `src/practical_chat_agent/services/memory_lifecycle.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不删除原始 events。
- 不让 frozen/archived memory 继续进入 prompt。

## Inputs to read

- `docs/02_experiment_plan.md` section 9.
- existing memory lifecycle service.

## Expected output

- `memory-freeze`
- `memory-archive`
- `memory-correct`
- status metadata preserved.

## Verification

Create or use fixture memory, freeze/correct it, then show it no longer appears in active context.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

