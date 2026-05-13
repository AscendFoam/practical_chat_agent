# Task T32: Skill Generation

## Task ID

T32

## Goal

实现 ContactSkill 生成服务，基于事件摘要、approved memories 和证据引用生成可审阅 Skill。

## Why now

这是联系人理解能力的第一版，但必须防止把全量原文直接塞给模型。

## Allowed files

- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/exporters/contact_skill_markdown.py`
- `src/practical_chat_agent/app/container.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不保存大段聊天原文到 skill。
- 不把 skill 用于冒充联系人。
- 不自动 approve。

## Inputs to read

- `docs/02_experiment_plan.md` section 8.4
- chat memory and profile services.

## Expected output

- Generate candidate ContactSkill with evidence refs and confidence.
- Redaction policy applied.
- status defaults to review/candidate.

## Verification

Generate from脱敏 fixture contact and inspect exported fields.

## Docs to update

- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md` if LLM unavailable

## Reviewer type

adversarial

