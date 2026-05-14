# Milestone Review: M1 Offline Distillation MVP

Review date: 2026-05-14
Reviewer: Codex Captain
Milestone: M1 offline distillation MVP

## Verdict

**Conditional**

M1 is complete enough to enter M2 conditionally. The pipeline runs end to end on a real private sample:

```text
normalized_events.jsonl
  -> chunks.jsonl
  -> chunk_summaries.jsonl
  -> memory_facts.jsonl
  -> contact_skill.candidate.json
  -> contact_skill.review.md
```

The next task may be T120, but M2 must preserve candidate-only / human-review-first semantics and carry forward M1's evidence-quality and heuristic-generalization risks.

## 1. 当前功能是否真的完成

**Yes, for the M1 MVP scope.**

- T110 produced conversation chunks from normalized events and preserved uncertainty signals.
- T111 defined schema contracts for chunk summaries, memory fact candidates, and ContactSkill candidates.
- T112 produced schema-validated chunk summaries and memory facts with evidence refs.
- T113 produced a ContactSkill candidate and Markdown review artifact, without auto-approval or impersonation behavior.
- T114 audited all 7 memory facts in the sample, exceeding the requirement to audit at least 5 facts.

M1 does **not** prove broad robustness. It proves the offline MVP can run on one small private sample with traceable evidence.

## 2. 是否能从干净环境运行

**Partially proven.**

The worker and reviewer records show the relevant modules compile and the CLIs run in the current conda environment:

- `chatlog-chunk`
- `chatlog-distill`
- `chatlog-build-contact-skill`

The pipeline has not yet been proven from a fresh clone plus clean dependency install. That clean-environment requirement should remain for later hardening, especially T150.

## 3. 是否有测试、demo 或实验结果

**Yes, but mostly sample/demo-level rather than automated tests.**

Evidence:

- T114 used `private/distilled/t102_smoke` as the milestone sample.
- The sample has 12 normalized events, 1 chunk, 1 chunk summary, 7 memory facts, and a ContactSkill candidate/review artifact.
- T114 worker audited all 7 memory facts.
- T114 reviewer independently rechecked all 7 facts against raw normalized events.
- Gate M1 checklist requirements were all marked PASS by the reviewer.

Automated tests are still weak. T150 must add parser/chunker/evidence/privacy/provider-shape tests.

## 4. 是否存在伪完成

**No blocking pseudo-completion found.**

The main capabilities are real enough for the milestone:

- LLM calls were real in T112; the worker did not use mock output when sandboxed network failed.
- Evidence refs were checked against event/chunk scope before accepted writes.
- Private outputs stayed under `private/distilled/**`.
- ContactSkill remained `candidate`; no auto-approval was introduced.
- No realtime platform, database migration, auto-send, fine-tuning, or persona clone behavior was introduced.

Residual caution:

- Some facts show "short evidence -> polished paraphrase" compression.
- T113 confidence/closeness/trust values are formulaic and may look over-precise.
- T113 heuristics are tuned to the current exam-prep sample and are not proven cross-domain.

These are not fake completion, but they are why the milestone is Conditional rather than Allow.

## 5. 是否允许进入下一里程碑

**Yes, conditionally.**

M2 may start with T120, but with these conditions:

1. Treat ContactSkill numeric values as reviewer-facing heuristics, not calibrated scores.
2. Keep ContactSkill candidate-only / human-review-first until broader samples validate the heuristics.
3. Preserve evidence refs and status across any file store or model changes.
4. Do not move rejected/frozen/candidate items into runtime prompt paths.
5. Carry R028, R029, and R030 forward into M2 planning.

## Required Next Task

T120: File Store Models

Task package: `docs/tasks/M2_memory_skill_store/T120_file_store_models.md`

T120 should not add database migrations or vector storage. It should first stabilize file-based loading/saving of memory/skill artifacts while preserving status and evidence refs.
