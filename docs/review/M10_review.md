# M10 Review: BehaviorPlanner

Reviewer: Codex Captain
Date: 2026-05-27
Scope: T210-T214, draft-only behavior schemas, deterministic candidate planning, deterministic draft enrichment, manual CandidateAction review, and behavior safety evaluation
Verdict: `Allow`

## 1. Current Functionality Completion

Yes, within the intended M10 scope.

M10 was not scoped to autonomous behavior, scheduling, platform delivery, or automatic sending. It was scoped to proving that the project can represent, generate, enrich, review, and evaluate proactive behavior candidates while keeping them non-executable.

That loop is complete:

- T210 defines `AgentSelfState`, `BehaviorPolicy`, `CandidateActionPayload`, and `CandidateAction` as draft-only, review-required contracts.
- T211 adds deterministic `BehaviorRulePlanner` candidate generation from compact approved/review-safe inputs.
- T212 adds deterministic `ProactiveDraftGenerator` enrichment for short review-only draft text.
- T213 adds `CandidateActionReviewService` and `chat-behavior-review-action` for manual approve/reject/freeze/archive review.
- T214 evaluates the T210-T213 slice and recommends `Gate M10 Allow`.

The completed feature is therefore review-only BehaviorPlanner infrastructure. It does not include outbound execution.

## 2. Clean Environment Run Readiness

The milestone has enough committed verification to be considered runnable from a clean project checkout with the normal test dependencies installed.

Current evidence:

- T214 reports `python -m py_compile src\practical_chat_agent\core\models.py src\practical_chat_agent\services\behavior_planner.py src\practical_chat_agent\app\main.py` passed.
- T214 reports targeted behavior verification passed: `pytest tests\test_behavior_schema.py tests\test_behavior_rule_planner.py tests\test_behavior_review_cli.py -q -o cache_dir=artifacts\t214_pytest_cache --basetemp=artifacts\t214_pytest_basetemp`, 58 tests.
- T214 reports full-suite verification passed: `pytest tests -q -o cache_dir=artifacts\t214_pytest_cache --basetemp=artifacts\t214_pytest_basetemp`, 780 tests.

The Windows sandbox needed workspace-local pytest temp/cache directories, which is an environment constraint rather than a feature gap. No private chat-history input is required for the committed behavior tests.

## 3. Tests, Demo, Or Experiment Results

Yes.

Committed tests cover:

- behavior schema validation and non-execution invariants
- policy allowed-action behavior
- deterministic rule planner output
- draft enrichment safety boundaries
- manual review service decisions
- CLI review and stdout safety
- approved candidates remaining non-sendable, non-schedulable, and non-platform-executable

Experiment/evaluation evidence exists in `docs/review/T214_behavior_safety_eval.md`:

- 8 scenario findings, exceeding the required 6
- safety matrix covering privacy, boundary sensitivity, frequency/quiet-hours, conflict handling, review-only status, CLI stdout, no-send/no-platform/no-scheduler, and state mutation
- explicit residual risks and next-milestone constraints

No demo is required for this milestone because M10 is not a user-facing runtime feature and must not create outbound behavior.

## 4. Pseudo-Completion Check

No blocking pseudo-completion found.

The documents and implementation do not claim that M10 can send messages, schedule actions, integrate platforms, or run autonomously. The safety eval explicitly limits M10 to review-only artifact creation and review metadata.

Important non-completed items are stated rather than hidden:

- `CandidateAction.status="approved"`, `review_state="reviewed"`, and `is_runtime_visible()` are not send authorization.
- CLI stdout still includes safe path metadata under the existing offline convention.
- The review CLI defaults to in-place overwrite when `--output` is omitted.
- Some minor test-strength gaps remain around repeated-review history growth and non-approve CLI round trips.
- Draft enrichment is deterministic and generic, not a quality-mature proactive conversation system.

These are residual constraints, not evidence that M10 is incomplete.

## 5. Next Milestone Permission

The project may enter M11 with `Gate M10 Allow`.

The required next task is `docs/tasks/M11_outbound_sendgate_feishu/T220_outbound_message_request_schema.md`.

M11 must start with a separate outbound request contract and then a send gate. It must not treat a reviewed `CandidateAction` as executable. T220/T221 must preserve these constraints:

- define `OutboundMessageRequest` separately from `CandidateAction`
- require explicit human approval and gate evaluation before any send-like artifact can become eligible
- keep all tests synthetic and private-content-free
- keep platform adapters out of T220 and behind later reviewed tasks
- keep Feishu/WeChat work disabled until the send gate exists and passes review
- keep quiet-hours/frequency semantics as policy data until a later scheduler task explicitly authorizes real scheduling

## Remaining Risks Carried Forward

- R093: future M11 code could accidentally interpret `CandidateAction.status="approved"`, `review_state="reviewed"`, or `is_runtime_visible()` as outbound authorization. T220/T221 must prevent this by using a separate outbound request model and explicit send-gate decision.
- R094: CLI path metadata and default in-place overwrite remain accepted offline CLI conventions, but future operational workflows should avoid private names in paths and prefer explicit output paths for review artifacts.
- R095: M10 has not evaluated real platform delivery, user notification ergonomics, send audit UX, or adapter failure recovery. These belong to M11+ and must not be backfilled into M10 claims.
