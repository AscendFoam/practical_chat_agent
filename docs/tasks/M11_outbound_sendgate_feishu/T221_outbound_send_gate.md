# Task T221: OutboundSendGate

## Task ID

T221

## Goal

Implement send gate policy before any real adapter can send.

## Required Features

- manual-only mode
- rate limit
- duplicate suppression
- kill switch
- quiet hours
- self-echo prevention
- audit log

## Forbidden Scope

- Do not integrate real platforms.
- Do not bypass human approval.

## Allowed Files

- `src/practical_chat_agent/services/policy.py`
- `src/practical_chat_agent/core/models.py`
- `docs/07_handoff.md`

## Reviewer Type

adversarial
