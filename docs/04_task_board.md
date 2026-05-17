# Task Board

Updated: 2026-05-17

## Captain Current State Override

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
- Gate M3 remains `Conditional`.
- Current Unique Task: T142 Feedback Summary Exporter.
- Current task package: `docs/tasks/M4_feedback_loop/T142_feedback_summary_exporter.md`.
- M4 remains review-only: no auto-send, no realtime platform integration, no automatic ContactSkill/Memory mutation, no feedback-to-patch behavior, and no relationship-aware maturity claim before regression hardening.
- T142 should stay aggregate-only and privacy-safe, and may surface the deferred T141 coherence gap only as summary metadata.
- T150 must add committed regression tests covering ReplyPlanner structure, boundary sensitivity, thin context, false positives, subtle false negatives, privacy leakage, contact alignment, candidate ranking, and feedback CLI safety.

## Current Unique Task

T142: Feedback Summary Exporter.

Task package: `docs/tasks/M4_feedback_loop/T142_feedback_summary_exporter.md`

Why now: T141 established read-only validation, and the next safe M4 step is aggregate visibility. T142 must summarize feedback patterns without exposing private text or mutating downstream state.

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
- [ ] T142: feedback summary exporter.

## Milestone 4.5: Regression Hardening

Goal: turn M3/M4 behavior into committed reproducible tests before feedback-to-patch or LLM drafting work.

- [ ] T150: ReplyPlanner regression tests.
- [ ] T151: policy fixture suite.
- [ ] T152: feedback CLI regression tests.

## Milestone 5: Feedback to Patch

Goal: convert repeated feedback into reviewable PreferencePatch candidates without automatic approval or mutation.

- [ ] T160: PreferencePatch schema.
- [ ] T161: feedback clusterer.
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

T140: Feedback Schema CLI.

It is now complete and accepted with `PASS_WITH_WARNINGS`. Its remaining deferred issues must be carried by T141/T152 rather than treated as blocking rework.

## Next Captain Output Required

When handing work to the next worker, Captain must output:

1. Current Unique Task
2. Why this task is next
3. Worker task package
4. Allowed files
5. Forbidden scope
6. Verification commands or acceptance criteria
7. Governance docs to update after completion
