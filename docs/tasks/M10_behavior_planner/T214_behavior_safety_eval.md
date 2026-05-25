# Task T214: Behavior Safety Eval

## Task ID

T214

## Goal

Produce the M10 behavior safety evaluation for the T210-T213 slice:

```text
Behavior schemas
  -> deterministic rule planner
  -> deterministic draft enrichment
  -> manual CandidateAction review
  -> reviewed candidate artifacts only
```

The evaluation must answer whether this slice is safe to accept as a review-only behavior-planner milestone, without authorizing sending, scheduling, platform execution, runtime autonomy, or state mutation.

## Why Now

T213 is accepted with `PASS`: the repo can manually review enriched `CandidateAction` records through a service and CLI while preserving no-send/no-scheduler/no-platform invariants.

T214 is the correct next step because M10 now needs a milestone-level safety evaluation, not another implementation layer. The eval should consolidate what T210-T213 actually provide, identify residual risks, and recommend the M10 gate status before any OutboundSendGate or platform work begins.

## Allowed Files

- `docs/review/T214_behavior_safety_eval.md`
- `docs/worker_summary/T214_worker_summary.md`
- `docs/07_handoff.md`

## Forbidden Scope

- Do not modify code.
- Do not modify tests, fixtures, schemas, services, CLIs, config, package metadata, or task-board/governance docs other than `docs/07_handoff.md`.
- Do not read `private/chat_history/` or commit private content.
- Do not create or commit private artifacts.
- Do not call LLM/provider APIs, embedding services, vector DBs, Mem0/Zep services, webhooks, platform APIs, browser automation, desktop automation, schedulers, timers, reminders, background jobs, or notification systems.
- Do not send messages, schedule actions, integrate Feishu/WeChat/desktop/email/web adapters, or create outbound requests.
- Do not treat `CandidateAction.status="approved"`, `review_state="reviewed"`, or `is_runtime_visible()` as sendable/schedulable/executable.
- Do not change policy, implement mitigation code, add a gate, or start Milestone 11 work.

## Inputs To Inspect

Use committed/repo-local material only:

- `docs/tasks/M10_behavior_planner/T210_behavior_schema.md`
- `docs/tasks/M10_behavior_planner/T211_action_planner_rule_engine.md`
- `docs/tasks/M10_behavior_planner/T212_proactive_draft_generator.md`
- `docs/tasks/M10_behavior_planner/T213_candidate_action_review_cli.md`
- `docs/review/T210_review.md`
- `docs/review/T211_review.md`
- `docs/review/T212_review.md`
- `docs/review/T213_review.md`
- `docs/worker_summary/T210_worker_summary.md`
- `docs/worker_summary/T211_worker_summary.md`
- `docs/worker_summary/T212_worker_summary.md`
- `docs/worker_summary/T213_worker_summary.md`
- `docs/data_contracts/behavior_planner_contract.md`
- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/behavior_planner.py`
- `src/practical_chat_agent/app/main.py`
- `tests/test_behavior_schema.py`
- `tests/test_behavior_rule_planner.py`
- `tests/test_behavior_review_cli.py`

Reading these files is allowed for evaluation. Editing them is not allowed unless they are listed under `Allowed Files`.

## Evaluation Questions

Answer each question explicitly in `docs/review/T214_behavior_safety_eval.md`:

1. Does the T210-T213 pipeline preserve the non-execution invariants end to end?
   - `human_review_required=True`
   - `auto_send_allowed=False`
   - `platform_execution_allowed=False`
   - `scheduler_allowed=False`
   - `platform_target=None`
2. Can boundary-sensitive, conflict-heavy, thin-context, or proactive-blocked inputs produce only conservative review artifacts rather than outbound action?
3. Does deterministic draft enrichment avoid overclaiming, impersonation, pressure, escalation, or false certainty?
4. Does manual review change only review/status metadata while preserving draft/supporting refs and no-send/no-platform/no-scheduler policy?
5. Are CLI/report stdout surfaces reasonably safe from private text leakage under the current offline path-output convention?
6. Are quiet-hours/frequency semantics represented only as policy/review data, not as schedulers or timers?
7. Are relationship-state and memory inputs consumed only through approved/review-safe compact surfaces rather than raw transcripts?
8. What residual risks remain before Milestone 11 can begin?

## Required Report Structure

`docs/review/T214_behavior_safety_eval.md` must include:

- `Verdict`: one of `Gate M10 Allow`, `Gate M10 Conditional`, or `Gate M10 Block`
- `Scope Evaluated`: exact files/docs inspected and commands run
- `Safety Matrix`: rows for privacy, boundary sensitivity, frequency/quiet-hours, conflict handling, review-only status, CLI stdout, no-send/no-platform/no-scheduler, and state mutation
- `Scenario Findings`: at least six synthetic scenarios, including:
  - thin context / no proactive signal
  - boundary-sensitive context
  - memory review prompt
  - relationship check-in
  - already-reviewed candidate
  - approved candidate remains non-sendable
- `Residual Risks`: concrete risks that remain after T213
- `Gate Recommendation`: what M10 does and does not authorize
- `Next-Milestone Constraints`: constraints T220/T221 must respect if M11 starts later

## Verification Commands

Run read-only/local verification where available. At minimum, attempt:

```powershell
python -m py_compile src/practical_chat_agent/core/models.py src/practical_chat_agent/services/behavior_planner.py src/practical_chat_agent/app/main.py
pytest tests/test_behavior_schema.py tests/test_behavior_rule_planner.py tests/test_behavior_review_cli.py -q
```

If the local environment needs workspace-local temp/cache paths, use the established artifacts temp/cache pattern from T213. If a command cannot run, record the exact command, failure reason, and whether it affects the gate recommendation.

## Expected Output

Produce:

- a committed M10 behavior safety eval at `docs/review/T214_behavior_safety_eval.md`
- a worker summary at `docs/worker_summary/T214_worker_summary.md`
- an appended T214 completion record in `docs/07_handoff.md`

The worker must not update `docs/04_task_board.md`; only Captain marks T214 complete after review.

## Acceptance Criteria

- The report is specific enough that a reviewer can validate the gate recommendation without guessing which files, commands, or scenarios were inspected.
- The report distinguishes implemented behavior from intended future behavior.
- Any `Conditional` or `Block` finding names the exact residual risk and the later task or repair type needed.
- No code or test files are changed.
- No private content is read, quoted, or committed.
- No outbound/send/platform/scheduler behavior is introduced or authorized.

## Reviewer Type

milestone
