# Task T122: Skill Review CLI

## Task ID

T122

## Goal

实现 contact-skill review/approve/reject/export CLI。

## Why now

ContactSkill 必须人工审核后才能进入 reply planner。

## Allowed files

- `src/practical_chat_agent/app/main.py`
- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/exporters/contact_skill_markdown.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不默认 approve。
- 不输出私密原文。

## Inputs to read

- T120/T121 outputs.

## Expected output

- CLI can show candidate summary, approve/reject, export Markdown.
- Approval writes status change and audit metadata.

## Verification

Run on redacted fixture skill.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

