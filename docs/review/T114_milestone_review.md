# Milestone Review: T114 M1 Gate

Review date: 2026-05-14
Author: Codex worker
Task package: `docs/tasks/M1_offline_distillation_mvp/T114_run_mvp_sample.md`
Status: worker draft, pending reviewer confirmation

## Scope

- 只做 M1 sample / milestone review，不修代码。
- 只检查现有 M1 pipeline 产物与治理文档。
- 不把 `private/distilled/**` 私密产物提交，不把真实联系人姓名、真实聊天原文或可识别平台 ID 写入 docs。

## Sample Used

- Sample run directory: `private/distilled/t102_smoke`
- Pipeline artifacts present:
  - `normalized_events.jsonl`
  - `chunks.jsonl`
  - `chunk_summaries.jsonl`
  - `memory_facts.jsonl`
  - `contact_skill.candidate.json`
  - `contact_skill.review.md`
  - `run_report.json`

## Verification Performed

1. Confirmed the sample run has a complete M1 artifact chain.
2. Re-ran ContactSkill consumption in safe mode:
   - `$env:PYTHONPATH='src'; & 'C:\ProgramData\anaconda3\envs\practical-chat-agent\python.exe' -m practical_chat_agent.app.main chatlog-build-contact-skill --input private/distilled/t102_smoke --dry-run`
3. Audited memory fact evidence refs against `normalized_events.jsonl`.
4. Reviewed `contact_skill.review.md` for:
   - human readability
   - evidence refs visibility
   - anti-impersonation boundary
   - absence of long raw chat excerpts in the review artifact

## M1 Artifact Summary

| Item | Result |
| --- | --- |
| Normalized events | 12 |
| Chunks | 1 |
| Chunk summaries | 1 |
| Memory facts | 7 |
| Contact-specific memory facts | 5 |
| User-side memory facts used for strategy only | 2 |
| ContactSkill candidate status | `candidate` |
| ContactSkill review artifact present | Yes |

## Evidence Accuracy Sample Audit

The task requires at least 5 sampled facts. This review audited all 7 memory facts in the sample.

| Memory ID | Type | Subject | Evidence support | Result |
| --- | --- | --- | --- | --- |
| `mem_010fed51a04f41c0` | `semantic` | contact | Single event directly supports the self-introduction claim. | PASS |
| `mem_118225641f834d7d` | `reflection` | contact | One forwarded-record event supports the study-background summary, but the claim compresses a long mixed event into a dense paraphrase. | PASS_WITH_CAUTION |
| `mem_f09f04bda56d4e36` | `semantic` | contact | Single event directly supports target-school claim. | PASS |
| `mem_5b038fa2fb4a49b1` | `semantic` | contact | Two events jointly support the estimated-score / 320-unreachable claim. | PASS |
| `mem_56a52ebb66b54f91` | `semantic` | contact | Single event directly supports worry about not passing the line. | PASS |
| `mem_b4731b7a6ce349ba` | `procedural` | user | Single user event supports offering practical tutoring/help. | PASS |
| `mem_240b70cbad024a8e` | `episodic` | user | Single user event supports “review materials first” intent. | PASS_WITH_CAUTION |

### Evidence audit notes

- All 7 memory facts have at least one event-level `evidence_ref`.
- No sampled memory fact relies on chunk-only evidence.
- No sampled memory fact has a missing evidence ref.
- The strongest caution is not missing evidence, but **compression**:
  - one forwarded/mixed event is being summarized into a fairly dense reflection fact
  - one brief user event is being normalized into a higher-level “review materials first” paraphrase

## ContactSkill Review Assessment

### What works

- The review artifact is readable by a human reviewer.
- `evidence_refs` are explicit at skill level and section level.
- `usage_boundary` is explicit and correctly forbids:
  - `persona_clone`
  - `impersonation`
  - `autonomous_contact_simulation`
- The artifact keeps `status="candidate"` and clearly says human review is required.
- The review artifact redacts the contact self-introduction name and does not contain long raw chat excerpts.

### Remaining concerns from T113 warnings

1. Heuristic generalization is still unproven.
   - This sample is strongly centered on exam pressure and practical study help.
   - Topic extraction and avoid-topic inference look reasonable here, but we still do not know how they behave on a different contact domain.

2. Confidence / closeness / trust numbers look more precise than the underlying evidence.
   - `0.77`, `0.82`, `0.62`, `0.61` read like measured values, but they are formulaic heuristics.
   - Candidate-only status reduces risk, but this should remain a visible limitation before M2.

3. Topic extraction coverage is narrow.
   - In this sample it produced one preferred topic and three avoid topics, which is usable.
   - It is still keyed to a small number of hardcoded patterns and should not yet be treated as robust cross-domain extraction.

## Gate M1 Checklist

Based on `docs/06_eval_protocol.md` Gate M1:

| Gate M1 requirement | Evidence | Result |
| --- | --- | --- |
| Generate chunks for one selected contact or small sample | `private/distilled/t102_smoke/chunks.jsonl` | PASS |
| Chunk summaries output as JSON and traceable | `chunk_summaries.jsonl` with `chunk_id`, `event_ids`, `evidence_refs` | PASS |
| Memory facts all carry `evidence_refs` | 7/7 facts checked | PASS |
| ContactSkill candidate has review Markdown | `contact_skill.candidate.json` and `contact_skill.review.md` present | PASS |
| Human audit of at least 5 facts with evidence support | 7 facts audited | PASS |
| No private raw chat text enters submit-able directories | docs updated with findings only; no raw excerpts copied into repo docs | PASS |

## Verdict

**Gate M1 verdict: `Conditional`**

## Why not `Block`

- The M1 artifact chain runs end to end on a real private sample.
- Evidence refs are present and, in this sample, they do point to supporting events.
- The ContactSkill review artifact is usable for human review and keeps anti-impersonation boundaries explicit.

## Why not `Allow`

- T113's main warnings remain materially true after this sample review:
  - heuristic generalization is still not demonstrated beyond the current exam-oriented sample
  - confidence / closeness / trust numbers still appear overly precise
  - topic extraction remains narrow and pattern-bound
- One reflection fact and one user-side episodic fact are acceptable, but they already show how quickly short or mixed evidence can be compressed into polished paraphrase.

## Conditions Before Or During M2

1. Treat all ContactSkill numeric confidence / closeness / trust values as reviewer-facing heuristics, not calibrated scores.
2. Keep ContactSkill in candidate-only / human-review-first mode until a broader sample shows the heuristics are not overfitting this domain.
3. In M2 or early M3 planning, revisit whether topic / relationship inference should stay heuristic or move to a better-audited inference layer.
4. Carry forward the forwarded-record / mixed-message caution from this sample when approving any skill derived from similar chunks.

## Recommended Next Action

If reviewer agrees with this draft:

- M2 may proceed only in `Conditional` mode.
- Captain should preserve the T113/T114 warnings in risks and governance docs rather than collapsing M1 into unconditional success.
