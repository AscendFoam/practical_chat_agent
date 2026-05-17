# Task T233: WeChat Safety Mode

## Task ID

T233

## Goal

Add strict WeChat safety mode defaults.

## Required Defaults

- `manual_send_only = true`
- `proactive_send_disabled = true`
- strict rate limits
- kill switch enabled

## Forbidden Scope

- Do not relax safety defaults.
- Do not bypass OutboundSendGate.

## Allowed Files

- `src/practical_chat_agent/connectors/**`
- `src/practical_chat_agent/services/policy.py`
- `docs/07_handoff.md`

## Reviewer Type

adversarial
