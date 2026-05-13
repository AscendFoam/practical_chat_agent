# Task T113: ContactSkill Builder

## Task ID

T113

## Goal

实现 ContactSkill builder 与 Markdown review exporter，从 chunk summaries 和 memory facts 生成 candidate skill。

## Why now

ContactSkill 是关系感知回复的核心资产，需要先以可审阅形式落地。

## Allowed files

- `src/practical_chat_agent/services/contact_skill.py`
- `src/practical_chat_agent/exporters/contact_skill_markdown.py`
- `src/practical_chat_agent/app/main.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不自动 approve。
- 不保存大段原文。
- 不生成“模拟联系人说话”的内容。

## Inputs to read

- T111/T112 outputs.
- ContactSkill schema in `docs/02_experiment_plan.md`.

## Expected output

- `contact_skill.candidate.json`
- `contact_skill.review.md`
- Candidate has evidence_refs and status.

## Verification

Build skill from a small private sample and check review artifact.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

