# Task T233: WeChat-Family Provider Constraint Safety Design

## Status

Blocked placeholder. Do not assign this task to a worker yet.

## Task ID

T233

## Current Decision

T230 recommends rewriting T233 as provider-constraint safety design, not
delivery. This task is intentionally not executable until T231 is reviewed and
Captain chooses whether M12 continues with the selected official surface.

## Future Goal

Design the provider-specific safety layer that would sit after
`OutboundSendGate` and before any future dry-run or live official-surface
adapter.

The design should cover:

- manual-send-only defaults;
- proactive-send disabled defaults;
- provider service-window checks;
- provider quota/rate-limit checks;
- reviewed recipient-map ownership;
- audit redaction and provider ID aliasing;
- kill-switch behavior;
- provider acceptance versus delivery/failure semantics;
- rollback / disable instructions for the chosen surface.

## Forbidden Until Rewritten

- No code implementation unless a future Captain task explicitly authorizes
  exact files and tests.
- No outbound delivery, live API calls, credentials, callback registration,
  polling, scheduler, runtime loop, or CLI send path.
- No relaxation of `OutboundSendGate`, human approval, manual-only policy,
  explicit recipient mapping, or no-automatic-send boundaries.
- No personal-WeChat automation, unofficial SDKs, scan-login resurrection, or
  desktop automation.
- No memory, feedback, ContactSkill, RelationshipState, approved-store, or
  private-artifact mutation.

## Reviewer Type

adversarial
