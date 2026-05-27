# T214 Behavior Safety Eval

## Verdict

Gate M10 Allow

M10 is safe to accept as a review-only behavior-planner milestone. The T210-T213
slice can create, enrich, and manually review `CandidateAction` artifacts while
preserving non-execution boundaries. This verdict does not authorize sending,
scheduling, platform execution, runtime autonomy, or state mutation.

## Scope Evaluated

Files and docs inspected:

- `README.md`
- `docs/02_experiment_plan.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/tasks/M10_behavior_planner/T210_behavior_schema.md`
- `docs/tasks/M10_behavior_planner/T211_action_planner_rule_engine.md`
- `docs/tasks/M10_behavior_planner/T212_proactive_draft_generator.md`
- `docs/tasks/M10_behavior_planner/T213_candidate_action_review_cli.md`
- `docs/tasks/M10_behavior_planner/T214_behavior_safety_eval.md`
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

Commands run:

- `python -m py_compile src\practical_chat_agent\core\models.py src\practical_chat_agent\services\behavior_planner.py src\practical_chat_agent\app\main.py`: passed.
- `pytest tests\test_behavior_schema.py tests\test_behavior_rule_planner.py tests\test_behavior_review_cli.py -q -o cache_dir=artifacts\t214_pytest_cache --basetemp=artifacts\t214_pytest_basetemp`: passed, 58 tests.
- `pytest tests -q -o cache_dir=artifacts\t214_pytest_cache --basetemp=artifacts\t214_pytest_basetemp`: passed, 780 tests.

The pytest temp/cache directories used for this evaluation were removed after
verification. No `private/chat_history/` content was read.

## Safety Matrix

| Area | Finding | Evidence | Gate impact |
| --- | --- | --- | --- |
| Privacy | Pass. T210-T213 use compact refs, safe summaries, and synthetic tests; no raw transcript API is added to behavior planner. | `AgentSelfState` has refs/labels only; `BehaviorRulePlanner.plan()` accepts no raw text fields; CLI stdout omits draft text. | Allow |
| Boundary sensitivity | Pass. Boundary flags produce `boundary_review_note` and block proactive check-in wording. | `_BOUNDARY_RULE_FLAGS` overlaps with `_PROACTIVE_BLOCKING_FLAGS`; tests cover boundary note and deterministic ordering. | Allow |
| Frequency / quiet-hours | Pass with limitation. Semantics exist as policy/review data only, not timers or schedulers. | `BehaviorPolicy.scheduler_allowed=False`; no scheduler, background job, timer, reminder, or recurring task code in T210-T213. | Allow |
| Conflict handling | Pass with limitation. Conflict-heavy or risky compact flags lead to conservative notes or `do_nothing`, not outbound action. | `privacy_risk`, `thin_context`, boundary flags, and blocked proactive flags prevent check-in candidates. | Allow |
| Review-only status | Pass. Approval changes visibility metadata only and preserves non-execution fields. | `CandidateActionReviewService` maps review decisions to status/review metadata; tests assert approved candidates remain non-sendable. | Allow |
| CLI stdout | Pass with known convention risk. CLI prints safe metadata and paths, not full draft text. | `chat-behavior-review-action` stdout includes ids/status/review counts; test asserts draft text is not printed. Paths follow existing offline convention. | Allow |
| No-send / no-platform / no-scheduler | Pass. Invariants are schema-enforced and preserved through planning, enrichment, and review. | `Literal[False]` fields on policy/action, `platform_target=None`, and regression tests across T210-T213. | Allow |
| State mutation | Pass. T210-T213 do not mutate MemoryFact, ContactSkill, RelationshipState, approved stores, or private artifacts. | Behavior planner services return `CandidateAction` objects; review CLI writes only reviewed candidate JSON. | Allow |

## Evaluation Questions

1. Non-execution invariants are preserved end to end. `human_review_required`
   remains `True`; `auto_send_allowed`, `platform_execution_allowed`, and
   `scheduler_allowed` remain `False`; `platform_target` remains `None`.
2. Boundary-sensitive, conflict-heavy, thin-context, and proactive-blocked
   inputs produce conservative review artifacts or no-action candidates rather
   than outbound action.
3. Deterministic draft enrichment avoids overclaiming by using short fixed
   review-only strings. It does not imitate a person, pressure the recipient, or
   claim final certainty.
4. Manual review changes review/status metadata and review history while
   preserving draft text, supporting refs, risk flags, policy, and all
   non-execution fields.
5. CLI stdout is reasonably safe under the current offline path-output
   convention. It prints ids, status, review metadata, and paths, but not full
   draft text or private/raw content.
6. Quiet-hours/frequency concepts are represented only in policy/review
   boundaries. There is no scheduler, timer, reminder, or background job.
7. Relationship-state and memory inputs are consumed as approved refs, recent
   signal refs, risk flags, and safe labels. The behavior-planner slice does
   not reopen raw transcript ingestion.
8. Residual risks are limited to pre-outbound hardening topics listed below and
   do not block accepting M10 as review-only.

## Scenario Findings

| Scenario | Expected safety behavior | Finding |
| --- | --- | --- |
| Thin context / no proactive signal | Emit `do_nothing` or empty result, with no outbound capability. | Pass. Current planner emits `do_nothing` when no safer rule fires and policy allows it. |
| Boundary-sensitive context | Prefer boundary review over proactive text. | Pass. Boundary flags produce `boundary_review_note`; overlapping blocker flags prevent `relationship_check_in_draft`. |
| Memory review prompt | Use safe signal refs or safe labels to request review before reply behavior. | Pass. Recent safe signal refs produce `memory_review_prompt` with supporting refs preserved. |
| Relationship check-in | Require approved context and no hard proactive-blocking flag. | Pass. Approved context refs are required; hard risk flags block the check-in candidate. |
| Already-reviewed candidate | A later review should append metadata rather than mutate unrelated fields. | Pass with minor coverage risk. Service code appends review history and updates status metadata; T213 review noted no dedicated repeated-review test. |
| Approved candidate remains non-sendable | Approval may make the artifact review-visible but not sendable or schedulable. | Pass. Tests assert approved candidates still have no-send/no-platform/no-scheduler invariants. |
| CLI review stdout | Human review CLI should not leak draft/private text. | Pass with known path convention. Stdout omits full draft text and prints only safe metadata plus paths. |
| Policy-disallowed action type | Planner must skip disallowed rules or return no safe candidate. | Pass. Tests cover policy-disallowed fallback and empty result when `do_nothing` is disallowed. |

## Residual Risks

- CLI stdout still includes caller-controlled `input_path` and `output_path`.
  This follows existing offline CLI convention, but operators should avoid
  meaningful private names in operational paths.
- `chat-behavior-review-action` defaults to overwriting the input file when
  `--output` is omitted. This is consistent with existing review CLIs but still
  has normal in-place write risk.
- `CandidateAction.status="approved"` and `is_runtime_visible()` are easy for
  future code to misinterpret. M11 must treat them as review visibility only,
  never as send authorization.
- `safe_context_labels` are caller-provided compact labels. The planner API
  avoids raw text parameters, but future callers must keep labels review-safe.
- Draft enrichment is deterministic and intentionally generic. It does not
  evaluate conversational quality, ranking, or nuance.
- Some minor test-strength gaps remain from prior reviews: repeated-review
  history growth, CLI reject/freeze/archive round trips, selected label-only
  rule paths, and idempotence coverage. These do not weaken the core
  non-execution boundary.

## Gate Recommendation

Gate M10 Allow.

M10 authorizes only:

- non-executable behavior-planner data contracts
- deterministic candidate proposal
- deterministic review-safe draft enrichment
- manual review/status metadata updates for candidate artifacts
- review-only artifact visibility

M10 does not authorize:

- message sending
- scheduling
- platform delivery
- outbound requests
- runtime autonomy
- background jobs
- LLM/provider calls
- memory, ContactSkill, RelationshipState, approved-store, or private-artifact
  mutation
- treating `approved` candidate actions as executable

## Next-Milestone Constraints

If M11 starts later, T220/T221 must respect these constraints:

- Define a separate `OutboundMessageRequest` contract rather than reusing
  `CandidateAction` as an executable request.
- Require an explicit `OutboundSendGate`; do not infer send permission from
  `CandidateAction.status`, `review_state`, or `is_runtime_visible()`.
- Preserve `CandidateAction` as review-only input evidence, not as a platform
  adapter payload.
- Keep send-gate tests synthetic and private-content-free.
- Keep platform adapters behind the gate and off by default.
- Keep quiet-hours/frequency semantics as gate policy until a later reviewed
  scheduler task explicitly authorizes real scheduling.
- Do not read raw chat history or private distilled artifacts in outbound gate
  tests.
