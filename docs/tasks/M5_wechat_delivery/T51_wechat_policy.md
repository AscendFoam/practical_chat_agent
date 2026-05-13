# Task T51: WeChat Policy

## Task ID

T51

## Goal

扩展 `PolicyEngine` 对微信平台的群聊草稿、安静时段、频率限制和 avoid topics 检查。

## Why now

真实发送必须先有平台特定安全规则。

## Allowed files

- `src/practical_chat_agent/services/policy.py`
- `src/practical_chat_agent/core/models.py` if policy decision needs fields
- `docs/07_handoff.md`

## Forbidden scope

- 不降低 Telegram 既有 policy 安全性。
- 不让 group chat 默认真实发送。

## Inputs to read

- existing PolicyEngine.
- `docs/02_experiment_plan.md` section 10.4.

## Expected output

- WeChat group chat defaults draft-only.
- quiet hours and frequency flags are explicit.
- ContactSkill avoid topics can add risk/block if available.

## Verification

Run policy checks for DM, group, quiet hour, high frequency, avoid topic fixtures.

## Docs to update

- `docs/07_handoff.md`

## Reviewer type

adversarial

