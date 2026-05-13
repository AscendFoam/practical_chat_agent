# Task T31: Contact Resolution

## Task ID

T31

## Goal

实现 contact resolution，把 platform user id、channel id、aliases 映射到统一 contact。

## Why now

没有 contact 统一层，Skill、记忆和建议都无法稳定关联同一个人。

## Allowed files

- `src/practical_chat_agent/services/contact_resolution.py`
- `src/practical_chat_agent/services/ingestion.py` if integration is needed
- `src/practical_chat_agent/app/container.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不做复杂身份合并自动推断。
- 不合并低置信联系人。

## Inputs to read

- T30 models/repositories.
- existing event fields.

## Expected output

- Deterministic resolution for exact platform ids.
- Low-confidence ambiguous matches require manual review or remain separate.

## Verification

Use fixture events for same/different contact ids and show resolution output.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

normal

