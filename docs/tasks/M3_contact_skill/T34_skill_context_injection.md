# Task T34: Skill Context Injection

## Task ID

T34

## Goal

将 approved ContactSkill 的压缩摘要注入 `ChatContext` 和 `ChatSuggestionService` prompt。

## Why now

Skill 只有进入建议链路，才能验证它是否改善回复质量。

## Allowed files

- `src/practical_chat_agent/services/chat_context.py`
- `src/practical_chat_agent/services/chat_suggestions.py`
- `src/practical_chat_agent/runtime/agent_runtime.py`
- `src/practical_chat_agent/app/container.py`
- `docs/07_handoff.md`

## Forbidden scope

- 不注入未 approved skill。
- 不注入完整证据原文。
- 不改变无 skill 时的正常建议链路。

## Inputs to read

- T30-T33 implementation.
- `docs/02_experiment_plan.md` section 8.6.

## Expected output

- Context includes compact contact skill summary when approved.
- Suggestion prompt uses style/preferences/avoid topics/recent common events.
- Feature can be disabled or absent without failure.

## Verification

Run a fixture inbound event for a contact with approved skill and compare context/suggestion metadata.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

