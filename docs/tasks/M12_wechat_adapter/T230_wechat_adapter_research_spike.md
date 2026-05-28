# Task T230: WeChat Adapter Research Spike

## Task ID

T230

## Goal

Produce a docs-only research decision for whether M12 may safely pursue any WeChat adapter path after M11's reviewed outbound gate, sandbox adapter, and review-card layers.

This task is intentionally research-only. It must not implement, install, vendor, log in, scan, send, receive, automate, or wire any WeChat integration.

## Background

Current mainline remains WeFlow-export-driven offline distillation and review-only reply planning. The old WeChat scan / SDK / realtime personal-account track is paused and must not be resumed by accident.

M11 completed a safe outbound boundary stack:

- T220 `OutboundMessageRequest` schema.
- T221 deterministic `OutboundSendGate`.
- T222 local fake adapter.
- T223 Feishu sandbox adapter.
- T224 local Feishu review card and inert review-intent parser.

M12 can begin only as a research spike. The research must decide whether a future WeChat adapter is feasible, legal/compliant enough for this repo's boundaries, and technically compatible with the existing send gate. If the answer is uncertain or unsafe, the report should recommend blocking or deferring implementation rather than inventing a risky adapter.

## Required Research Questions

The research report must answer:

- Which WeChat-family surfaces are candidates, if any? Consider personal WeChat, WeCom/企业微信, Official Account/公众号, Mini Program/customer-service style APIs, desktop automation/manual-copy workflows, and continuing to use Feishu/manual handoff instead of WeChat.
- For each candidate surface, what are the authentication, recipient identity, inbound event, outbound message, rate limit, audit, and operational requirements?
- Which options are official/supported versus unofficial/fragile/prohibited for this repository?
- Can any option respect `OutboundSendGate`, human approval, manual-send-only policy, explicit recipient mapping, audit logging, no private transcript reads, and no automatic proactive sends?
- What cannot be verified without live credentials, official tenant/app setup, or current platform documentation?
- What should T231/T232/T233 do next, or should they remain blocked until a safer platform path exists?

If current external documentation is consulted, prefer official WeChat/WeCom/Tencent documentation and cite links in the report. If network access is unavailable, the report must state that current external facts were not verified and mark those points as open risks rather than completed facts.

## Required Output

Create `docs/review/T230_wechat_adapter_research.md` with these sections:

- `Executive Decision`: one of `Gate M12 Research Allow`, `Gate M12 Conditional`, or `Gate M12 Block`.
- `Scope Audited`: files/docs read, external docs consulted if any, and explicit note that no private chat content was read.
- `Option Matrix`: candidate surfaces with support status, fit, risks, and recommendation.
- `Compatibility With Existing Architecture`: how any acceptable path would map to `InboundEvent`, `OutboundMessageRequest`, `OutboundSendGate`, explicit recipient mapping, review-card/manual approval, and audit.
- `Rejected Paths`: explicit rejection or deferral of unofficial SDK vendoring, scan-login resurrection, realtime personal-account automation, automatic sending, and hidden memory writes unless the evidence says otherwise and the user later approves.
- `Recommended Next Task`: whether T231 should proceed, be rewritten, or be blocked. If proceeding, describe the exact safe scope.
- `Risks And Open Questions`: cite unresolved compliance, credential, callback, delivery, and safety questions.

Also create `docs/worker_summary/T230_worker_summary.md` with:

- what was researched,
- sources used,
- final gate recommendation,
- explicit non-actions,
- verification performed.

Update `docs/07_handoff.md` with a T230 worker completion record, but do not update `docs/04_task_board.md`.

## Forbidden Scope

- Do not implement login, scan, session validation, inbound polling, outbound sending, callbacks, webhooks, desktop automation, browser automation, or runtime loops.
- Do not install packages, clone SDKs, vendor SDK code, copy unofficial SDK snippets, or commit third-party code.
- Do not call WeChat, WeCom, Tencent, Feishu, or any other platform API.
- Do not use real credentials, tokens, cookies, QR codes, personal accounts, tenant ids, app ids, open ids, chat ids, or private recipients.
- Do not read `private/chat_history/` or commit private content.
- Do not modify `src/`, `tests/`, runtime config, `app/main.py`, connector modules, send-gate behavior, memory stores, feedback logs, or task board.
- Do not claim production readiness for any WeChat path.
- Do not treat Feishu review-card intent parsing as approval application or delivery authorization.

## Allowed Files

Worker may edit only:

- `docs/review/T230_wechat_adapter_research.md`
- `docs/worker_summary/T230_worker_summary.md`
- `docs/07_handoff.md`

## Acceptance Criteria

- The report is docs-only and contains no private content.
- The report clearly separates official/supported options from unofficial or prohibited options.
- The report explicitly states whether T231/T232/T233 should proceed, be narrowed, or be blocked.
- The report preserves all M11 boundaries: send gate, human approval, explicit recipient mapping, no automatic sending, no hidden memory writes, no production delivery claim.
- The report does not resume the paused T01 scan-login track.
- The worker summary records explicit non-actions and verification.

## Suggested Verification Commands

```powershell
git diff --check
git status --short
```

If the worker consults external sources, the report itself must include citations and retrieval dates. If external access is unavailable, the verification section should say so and treat current API/compliance facts as unresolved.

## Reviewer Type

milestone
