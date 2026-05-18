# Review: T161

Verdict: PASS_WITH_WARNINGS

## Task Summary

T161 implements a deterministic, review-only feedback clusterer that groups similar validated T140-T142 feedback records into privacy-safe aggregate clusters. The task is clustering-only: no patch generation, no LLM, no ContactSkill/Memory mutation, no auto-approve, no runtime injection.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: `reason_tag_summary` field name is misleading

The field named `reason_tag_summary` actually contains a frequency count of `boundary_label` values from feedback records. The `ReplyFeedbackRecord` model has no `reason_tag` field. While the task package uses the phrase "reason-tag aggregates," a T162 developer looking at the cluster output might search for a `reason_tag` field that does not exist in the source model.

**Why non-blocking**: The task package explicitly names this concept "reason-tag aggregates," and the field is populated from the closest available signal (`boundary_label`). The semantics are documented in the contract example. No data is lost or misrepresented — the name is simply inconsistent with the source model field.

### N02: No committed automated tests for cluster output

T161 adds `FeedbackClusterService` and the `chat-feedback-cluster` CLI command but does not add any committed pytest tests. The worker's verification was inline/synthetic only.

**Why non-blocking**: This follows the established pattern from T110-T142 and T160, where committed tests came later (T150-T152 for M3/M4, deferred for M5). R049 already tracks this. A future regression-hardening pass should cover: valid clustering, cluster ID stability, edit-record exclusion, validation-report filtering, privacy-safe output, and JSON round-trip.

### N03: `counts_by_approach_label` silently degrades when plan files are missing

`_get_approach_label` reads ReplyPlan files from `source_plan_path` to extract `approach_label`. If plan files are missing, unreadable, or not co-located, the approach label is silently omitted from counts. The `counts_by_approach_label` field may be empty or None without any indication of why.

**Why non-blocking**: The task package says cluster output should include "aggregate counts such as total records / action counts" and "optional safe summaries." `approach_label` is an optional enrichment. Silent degradation is the safest failure mode — it does not produce wrong labels, just missing ones. T162 can observe actual usage before deciding whether to add a completeness metric.

### N04: `input_path` included in stdout output

The raw filesystem path is included in both the report dict and the CLI stdout. This is consistent with the T140-T142 pattern where the same issue was noted (N01 in T140 review, N02 in T141 review, N02 in T142 review) and tracked as R043.

**Why non-blocking**: This is a known, project-wide pattern. R043 is already tracked and deferred.

### N05: `.claude/settings.json` modified outside allowed list

The working tree contains a modification to `.claude/settings.json`, which is not in the allowed files list.

**Why non-blocking**: This is a worker environment artifact, not T161 content. All T161-specific changes are confined to the 5 allowed files: `feedback.py`, `main.py`, `preference_patch_contract.md`, `07_handoff.md`, `08_risks_and_open_questions.md`.

## Missing Tests

No committed pytest tests for `FeedbackClusterService` or `chat-feedback-cluster` CLI. A future regression-hardening task should cover:

- valid multi-contact clustering with correct label assignment
- cluster ID stability across identical inputs
- edit records excluded from clustering (unlabeled)
- validation-report filtering
- privacy: output contains no `edited_text`, `user_note`, `boundary_note`, or draft text
- boundary_label normalization and known-label matching
- corrupted/missing input file handling
- JSON round-trip fidelity
- single-record cluster edge case

## Suspicious Implementation Details

None found. The implementation is clean and narrow:

1. `_LABEL_BY_ACTION` maps exactly 3 of 4 action types (accept→good_tone, reject→not_like_me, boundary→boundary_violation). Edit is intentionally omitted with no safe deterministic label.
2. `_KNOWN_LABELS` contains exactly the 8 labels specified in the task package.
3. `cluster_id` is derived from `sha256(contact_id:label)[:16]`, ensuring stability for identical grouping keys regardless of record content.
4. Output ordering is deterministic via `sorted(groups.items())`.
5. No field in the output stores raw transcript text, edited text, user notes, boundary notes, or draft text.
6. No PreferencePatchCandidate generation, no ContactSkill/Memory mutation, no LLM call, no auto-approve, no runtime injection.
7. `_get_approach_label` correctly matches on both `candidate_id` and `priority_rank` to avoid misidentification.
8. Plan loading uses safe exception handling and caching to avoid redundant I/O.
9. The contract document accurately describes the label derivation rules, output shape, and safety constraints without claiming future work as done.

## Verification

- Compile: `feedback.py` and `main.py` compile cleanly.
- Existing tests: 176/176 pass, zero regressions.
- Worker's synthetic verification (10 records → 4 clusters): labels correct, edit unlabeled, contact isolation correct.
- Cluster ID stability: confirmed by worker (identical inputs → identical cluster IDs).
- Privacy: output JSON confirmed to contain no raw text fields.
- CLI: `chat-feedback-cluster --feedback-log <path>` functional.

## Recommended Next Action

T161 is complete. Current Unique Task may advance to T162 (patch proposal CLI), subject to Captain decision. T162 must:

- consume T161 cluster output and produce `PreferencePatchCandidate` instances
- enforce `supporting_feedback_ids` non-empty
- handle edit records that were not clustered (R050)
- use `supporting_cluster_ids` to reference T161 cluster IDs
- not auto-approve patches
