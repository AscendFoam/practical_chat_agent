# Review: T214

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

N01 The safety matrix row for "Conflict handling" says "Pass with limitation" but does not explicitly name what the limitation is beyond "conservative notes or `do_nothing`, not outbound action." The limitation is that conflict-heavy inputs can only produce conservative candidates (review notes, do-nothing) rather than nuanced conflict-resolution drafts. This is acceptable for M10 scope — the pipeline is intentionally conservative — but the matrix could be clearer that the "limitation" is a design choice, not a defect.

N02 The scenario finding for "Already-reviewed candidate" notes "Pass with minor coverage risk" and references the T213 review gap (M02: no repeated-review history-count test). The eval correctly carries this forward but does not propose a concrete repair task. This is acceptable for an evaluation-only task, and the risk is properly categorized as non-blocking test-strength debt.

N03 The safety matrix row for "CLI stdout" says "Pass with known convention risk" and the residual risks section mentions CLI path metadata. This is consistent with the project-wide observation across T140-T213 reviews about `_safe_cli_path()` exposing caller-controlled paths. The eval does not propose a fix, which is appropriate for an evaluation-only task, but the risk remains unaddressed at the project level.

N04 The `Scope Evaluated` section lists `README.md` and `docs/02_experiment_plan.md` as inspected files, but the task spec's `Inputs To Inspect` section does not include these. This is harmless — reading additional docs for context is reasonable in an evaluation — but the scope section should ideally note which files were required vs. supplementary.

N05 The eval doc mentions "The pytest temp/cache directories used for this evaluation were removed after verification." This is fine cleanup, but no evidence is provided that the directories actually existed (e.g., no `ls` or directory listing). This is cosmetic — the verification commands are documented and the tests are committed — so the trust anchor is the committed test suite, not the temp directory.

## Missing Tests

M01 The eval does not include a scenario for "draft enrichment with boundary-sensitive action type produces impersonation-free text." While the eval answer to question 3 addresses this at a high level ("short fixed review-only strings"), a specific scenario tracing boundary-sensitive enrichment through `ProactiveDraftGenerator` to confirm no impersonation/pressure would strengthen the safety matrix. The existing test suite covers this implicitly, but an explicit eval scenario would make the safety argument more traceable.

M02 The eval does not include a scenario for "policy-disallowed action type suppresses all candidate output." The existing scenario "Policy-disallowed action type" covers this, but it references "tests cover policy-disallowed fallback" rather than tracing the specific code path. Minor traceability gap for future reviewers.

## Suspicious Implementation Details

None. This is a documentation-only evaluation task. No code, tests, schemas, services, CLIs, or configuration files were modified. The eval correctly:

- Stays within the three allowed files (`docs/review/T214_behavior_safety_eval.md`, `docs/worker_summary/T214_worker_summary.md`, `docs/07_handoff.md`).
- Runs the required verification commands and reports results.
- Answers all 8 evaluation questions explicitly.
- Provides 8 scenarios (minimum required: 6).
- Includes the required report structure (Verdict, Scope Evaluated, Safety Matrix, Scenario Findings, Residual Risks, Gate Recommendation, Next-Milestone Constraints).
- Distinguishes implemented behavior from intended future behavior.
- Names concrete residual risks.
- Does not treat `approved` status as send authorization.
- Does not start M11 implementation or authorize outbound work.
- Does not read private chat history or commit private artifacts.

Spot-checks against the source code confirm the eval's factual claims:

- `AgentSelfState` (models.py:811-829) stores only identifiers, safe summaries, and artifact refs — no raw text. Claim confirmed.
- `BehaviorPolicy` and `CandidateAction` fields use `Literal[True]` / `Literal[False]` / `None` for non-execution invariants (models.py:855-858, 932-936). Claim confirmed.
- `BehaviorRulePlanner.plan()` (behavior_planner.py:48-53) consumes only `AgentSelfState`, `BehaviorPolicy`, and `safe_context_labels` — all compact/label-based inputs. Claim confirmed.
- `CandidateActionReviewService` uses `model_copy(deep=True)` (behavior_planner.py:382). Claim confirmed.
- `chat-behavior-review-action` CLI stdout (main.py:2667-2683) prints only safe metadata fields (action_id, contact_id, action_type, status, review metadata) — no draft text. Claim confirmed.

## Recommended Next Action

T214 is complete with a well-supported `Gate M10 Allow` recommendation. The project may now advance to M11 (OutboundSendGate + Feishu Sandbox), beginning with T220 (OutboundMessageRequest schema). T220 must define a separate outbound message request contract rather than reusing `CandidateAction`, and must require an explicit send gate that does not infer send permission from review status.
