# Task Board

Updated: 2026-05-18

## Captain Current State Override

- T161 review decision: `PASS_WITH_WARNINGS`.
- T161 is complete as a deterministic, privacy-safe feedback clusterer task.
- T161 warning disposition:
  - Accepted: N01 `reason_tag_summary` naming is slightly misleading but documented well enough for current scope, N03 `counts_by_approach_label` may safely degrade to empty when plan files are unavailable, N05 `.claude/settings.json` is a workspace artifact rather than a T161 scope violation.
  - Deferred: N02 no committed automated tests yet cover `FeedbackClusterService` / `chat-feedback-cluster`, N04 raw `input_path` remains present in cluster stdout/output and stays tracked as project-wide path-handling/privacy debt.
  - Rejected: none.
- T160 review decision: `PASS_WITH_WARNINGS`.
- T160 is complete as a schema-only PreferencePatch candidate contract task.
- T160 warning disposition:
  - Accepted: N01 `instruction_scope` remains free-form at schema stage, N04 `schema_version` remains a plain string for consistency with existing patterns, N05 broader working-tree modifications are a hygiene note rather than a T160 scope violation.
  - Deferred: N02 `positive_examples` / `negative_examples` are not structurally constrained to safe-only summaries or references, N03 no committed automated tests yet cover `PreferencePatchCandidate` validation.
  - Rejected: none.
- Current Unique Task: T162 Patch Proposal CLI.
- Current task package: `docs/tasks/M5_feedback_to_patch/T162_patch_proposal_cli.md`.
- T162 must stay deterministic, candidate-only, review-only, and non-mutating: no auto-approve, no auto-apply, no runtime injection, no ContactSkill/Memory mutation, no outbound send behavior, and no LLM use unless a future task package explicitly changes that scope.
- T162 must consume T161 cluster outputs conservatively: enforce non-empty `supporting_feedback_ids`, preserve `supporting_cluster_ids`, skip ambiguous or unlabeled clusters rather than speculate, and keep all examples/summaries privacy-safe.
- T152 review decision: `PASS_WITH_WARNINGS`.
- T152 is complete as a committed feedback CLI regression-hardening task.
- T152 warning disposition:
  - Accepted: N03 `--validation-report` CLI wiring is covered at the service level rather than by a dedicated end-to-end CLI test, N04 no single append->validate->summarize integration test yet, N05 `test_approach_labels_loaded` is intentionally brittle as a regression guard.
  - Deferred: N01 validation `record_results` can still grow unboundedly on large logs, N02 service-level output-path confinement is still by warning/convention rather than hard enforcement.
  - Rejected: none.
- Gate M3 remains `Conditional` for quality/maturity claims.
- Gate M4.5 is now `Allow`.
- M4 review-only feedback infrastructure is now reproducible from committed repo contents.
- M5 is now authorized only at the review-only patch-candidate layer: no auto-apply, no runtime injection, no automatic ContactSkill/Memory mutation, no outbound send behavior, and no LLM use unless a future task package explicitly allows it.
- T151 review decision: `PASS_WITH_WARNINGS`.
- T151 is complete as a committed policy-fixture and direct policy-engine regression-hardening task.
- T151 warning disposition:
  - Accepted: N01 `_candidate_is_over_proactive` conservative fallback branch not independently covered, N02 confidence-penalty coverage not fully additive across every combination, N03 baseline fixture contamination found and corrected by the new direct tests.
  - Deferred: none.
  - Rejected: none.
- T150 review decision: `PASS_WITH_WARNINGS`.
- T150 is complete as a committed ReplyPlanner regression-hardening task.
- T150 warning disposition:
  - Accepted: N01 overlapping `not_configured` fixture coverage, N02 no direct `ReplyPlanPolicyEngine` unit tests yet, N03 summary-text assertion fragility, N04 false-negative probe asserts current absence rather than a gap marker, N05 helper constructors not tested independently, N06 no `notes_on_candidate_differences` assertion yet.
  - Deferred: none.
  - Rejected: none.
- T140 review decision: `PASS_WITH_WARNINGS`.
- T140 is complete as a review-only feedback capture task.
- T140 warning disposition:
  - Accepted: N03 redundant recount, N04 `reply_plan_id` proxy semantics, N06 `Literal` action type.
  - Deferred: N01 corrupted-log silent reset, N02 unstable `source_plan_path`, N05 missing private-path confinement.
- T141 review decision: `PASS_WITH_WARNINGS`.
- T141 is complete as a read-only feedback log validator.
- T141 warning disposition:
  - Accepted: N01 raw `input_path` in CLI output, N03 coarse private-path heuristic, N04 CWD-dependent relative path resolution, N05 stored-but-unused `strict_mode`.
  - Deferred: N02 `reply_plan_id` coherence not cross-checked, N06 `record_results` may get large.
  - Rejected: none.
- T142 review decision: `PASS_WITH_WARNINGS`.
- T142 is complete as a privacy-safe aggregate feedback summary exporter.
- T142 warning disposition:
  - Accepted: N01 duplicated plan-loading helpers, N02 raw `input_path` in stdout, N03 aggregate presence counts expose low-risk existence patterns, N04 unreadable input can still produce an output artifact, N05 untyped summary `dict`, N06 no `reason_tag` / `policy_risk_flag` aggregation because those fields do not yet exist.
  - Deferred: none.
  - Rejected: none.
- Gate M4 was `Conditional` at milestone review time and is now satisfied through completed M4.5 regression hardening.
- M4 remains review-only: no auto-send, no realtime platform integration, no automatic ContactSkill/Memory mutation, no feedback-to-patch behavior, and no relationship-aware maturity claim before regression hardening.
- M4.5 is complete: T150/T151/T152 together provide committed deterministic coverage for ReplyPlanner, direct policy behavior, and the feedback CLI loop.
- The project may now continue within M5, but only under review-only patch-candidate constraints.

## Current Unique Task

T162: Patch Proposal CLI.

Task package: `docs/tasks/M5_feedback_to_patch/T162_patch_proposal_cli.md`

Why now: T161 is now complete and accepted. The next smallest safe M5 step is to turn clustered aggregate evidence into candidate-only patch proposals before any review CLI or runtime-context work.

## Board Rules

- Current mainline is WeFlow-export-driven offline distillation and review-only reply planning.
- Only the `Current Unique Task` may be assigned to a worker.
- Worker must stay within the task package `Allowed files`.
- `private/` chat history and private distilled artifacts must never be committed.
- Fixtures, tests, and docs must stay redacted.
- Do not resume T01 or restart WeChat scan / SDK / realtime platform work on the current mainline.
- Do not add fine-tuning, automatic sending, or digital-clone behavior.

## Paused Legacy Track: WeChat SDK / Scan

- [x] T00: SDK install and QR-stage probe. Review `PASS`.
- [ ] T01: login/session validation. Review `BLOCK`. User chose not to repair it; legacy track remains paused.

Conclusion: the old iLink / scan track no longer drives the next stage of development.

## Milestone 0: WeFlow Data Contract and Privacy Guardrails

Goal: confirm WeFlow JSONL is parseable and define a normalized event contract plus redacted fixture.

- [x] T100: WeFlow JSONL schema profiling + normalized event contract. Review `PASS`.
- [x] T101: privacy redaction rules + source-ref rules + minimal redacted fixture. Review `PASS`.
- [x] T102: minimal WeFlow normalize CLI. Review `PASS`.
- [x] T103: M0 review. Gate M0 `Conditional`, accepted for M1.

## Milestone 1: Offline Distillation MVP

Goal: generate chunks, memory facts, ContactSkill candidate, and review artifact from one contact or a small sample.

- [x] T110: conversation chunker v0. Review `PASS`.
- [x] T111: distillation schemas. Review `PASS`.
- [x] T112: summary + fact extraction pipeline. Review `PASS`.
- [x] T113: ContactSkill builder + markdown review exporter. Review `PASS_WITH_WARNINGS`.
- [x] T114: MVP sample run + gate review. Gate M1 `Conditional`.

## Milestone 2: Memory / Skill Store and Evidence Validation

Goal: move offline artifacts into project models, storage, and review flow.

- [x] T120: file-store models for memory/skill records. Review `PASS_WITH_WARNINGS`.
- [x] T121: evidence validator. Review `PASS_WITH_WARNINGS`.
- [x] T122: review / approve / export CLI. Review `PASS_WITH_WARNINGS`.
- [x] T123: approved/runtime-ready context integration. Review `PASS_WITH_WARNINGS`.

## Milestone 3: Relationship Reply Planner

Goal: generate interpretable, multi-candidate, safety-aware reply drafts from approved ContactSkill + memory.

- [x] T130: ReplyPlan schema + prompt contract. Review `PASS_WITH_WARNINGS`.
- [x] T131: review-only ReplyPlanner. Review `PASS_WITH_WARNINGS`.
- [x] T132: policy / boundary layer. Review `PASS_WITH_WARNINGS`.
- [x] T133: anonymized holdout eval. Review `PASS_WITH_WARNINGS`. Gate M3 `Conditional`.

## Milestone 4: Feedback Capture

Goal: record, validate, and summarize human feedback on ReplyPlan candidates without applying it automatically.

- [x] T140: feedback log schema + CLI. Review `PASS_WITH_WARNINGS`.
- [x] T141: feedback log validator. Review `PASS_WITH_WARNINGS`.
- [x] T142: feedback summary exporter. Review `PASS_WITH_WARNINGS`. Gate M4 `Conditional`.

## Milestone 4.5: Regression Hardening

Goal: turn M3/M4 behavior into committed reproducible tests before feedback-to-patch or LLM drafting work.

- [x] T150: ReplyPlanner regression tests. Review `PASS_WITH_WARNINGS`.
- [x] T151: policy fixture suite. Review `PASS_WITH_WARNINGS`.
- [x] T152: feedback CLI regression tests. Review `PASS_WITH_WARNINGS`. Gate M4.5 `Allow`.

## Milestone 5: Feedback to Patch

Goal: convert repeated feedback into reviewable PreferencePatch candidates without automatic approval or mutation.

- [x] T160: PreferencePatch schema. Review `PASS_WITH_WARNINGS`.
- [x] T161: feedback clusterer. Review `PASS_WITH_WARNINGS`.
- [ ] T162: patch proposal CLI.
- [ ] T163: patch review CLI.
- [ ] T164: approved patch compact context.

## Milestone 6: ContactSkill-Compatible Decomposition

Goal: keep ContactSkill compatible while deriving more focused briefs.

- [ ] T170: ContactSkill decomposition design.
- [ ] T171: PartnerPersonaBrief schema.
- [ ] T172: CommunicationPolicyBrief schema.
- [ ] T173: ContactSkill projection service.
- [ ] T174: derived briefs context integration.

## Milestone 7: LLM-Assisted ReplyPlanner

Goal: add optional LLM candidate generation only after regression safety net is in place.

- [ ] T180: LLM candidate contract.
- [ ] T181: LLM candidate offline CLI.
- [ ] T182: candidate validator.
- [ ] T183: hybrid ReplyPlanner.
- [ ] T184: planner holdout eval.

## Milestone 8: RelationshipState

Goal: model multi-axis relationship state with human-reviewed deltas rather than a single scalar affinity score.

- [ ] T190: RelationshipState schema.
- [ ] T191: relationship signal extractor.
- [ ] T192: RelationshipDeltaCandidate.
- [ ] T193: relationship review CLI.
- [ ] T194: RelationshipState compact context.
- [ ] T195: relationship-aware reply eval.

## Milestone 9: Memory Retrieval Layer

Goal: define a retriever abstraction before evaluating external memory adapters.

- [ ] T200: MemoryRetriever interface.
- [ ] T201: local approved-store retriever.
- [ ] T202: retrieval eval set.
- [ ] T203: optional Mem0 adapter spike.

## Milestone 10: BehaviorPlanner

Goal: generate draft-only proactive action candidates without automatic sending.

- [ ] T210: behavior schema.
- [ ] T211: action-planner rule engine.
- [ ] T212: proactive draft generator.
- [ ] T213: CandidateAction review CLI.
- [ ] T214: behavior safety eval.

## Milestone 11: OutboundSendGate + Feishu Sandbox

Goal: build a platform-independent send gate before any real adapter work.

- [ ] T220: OutboundMessageRequest schema.
- [ ] T221: OutboundSendGate.
- [ ] T222: local fake adapter.
- [ ] T223: Feishu adapter.
- [ ] T224: Feishu review card.

## Milestone 12: WeChat Adapter

Goal: keep WeChat as a thin final adapter behind the send gate.

- [ ] T230: WeChat adapter research spike.
- [ ] T231: WeChat inbound adapter.
- [ ] T232: WeChat outbound adapter.
- [ ] T233: WeChat safety mode.

## Historical Current Unique Task

T161: Feedback Clusterer.

It is now complete and accepted with `PASS_WITH_WARNINGS`. The next worker task is T162, because the cluster layer now exists and the next safe step is deterministic candidate-only patch proposal generation before any review CLI or runtime-context wiring.

## Next Captain Output Required

When handing work to the next worker, Captain must output:

1. Current Unique Task
2. Why this task is next
3. Worker task package
4. Allowed files
5. Forbidden scope
6. Verification commands or acceptance criteria
7. Governance docs to update after completion
