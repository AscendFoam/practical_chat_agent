# Task T33: Skill Review CLI

## Task ID

T33

## Goal

实现 `contact-list/show/skill-generate/skill-show/skill-review/skill-approve/skill-export` 最小 CLI。

## Why now

ContactSkill 必须可人工审阅和批准后才能进入建议链路。

## Allowed files

- `src/practical_chat_agent/app/main.py`
- `src/practical_chat_agent/app/container.py`
- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/exporters/contact_skill_markdown.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不绕过 review/approve。
- 不默认输出敏感证据原文。

## Inputs to read

- T30-T32 implementation.
- existing memory/profile CLI patterns.

## Expected output

- Human-readable and JSON outputs where appropriate.
- Export markdown suitable for review.

## Verification

Run CLI against fixture/generated contact skill.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

