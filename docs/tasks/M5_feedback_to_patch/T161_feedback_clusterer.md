# Task T161: Feedback Clusterer

## Task ID

T161

## Goal

Implement a deterministic, review-only feedback clusterer that groups similar validated T140-T142 feedback records into privacy-safe aggregate clusters for later patch proposal.

## Why Now

T160 now defines the candidate-only `PreferencePatchCandidate` contract, but one edit/reject still must not directly become a long-term communication-policy patch. T161 adds the conservative intermediate layer: repeated similar feedback can first become a reviewable cluster before T162 is allowed to generate any patch candidates.

T161 is therefore the next smallest safe M5 step: aggregate repeated evidence first, generate nothing patch-shaped yet, and keep the whole flow deterministic and privacy-safe.

## Inputs To Read

- `docs/review/T140_review.md`
- `docs/review/T141_review.md`
- `docs/review/T142_review.md`
- `docs/review/T152_review.md`
- `docs/review/T160_review.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- existing feedback models/services/CLI in:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`

## Allowed Files

- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/data_contracts/preference_patch_contract.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- Do not generate `PreferencePatchCandidate` yet.
- Do not call an LLM.
- Do not modify ContactSkill, MemoryFact, approved store records, or planner templates.
- Do not auto-approve or apply anything.
- Do not read private chat history.

## Expected Output

Add a deterministic clusterer plus CLI surface that:

- consumes validated feedback logs or safe feedback records only
- groups repeated feedback by rule-based signals such as action type, reason tags, edited-vs-rejected patterns, and safe aggregate labels
- emits only aggregate cluster data under a private path
- preserves supporting `feedback_id` membership for each cluster
- produces stable `cluster_id` values compatible with future `PreferencePatchCandidate.supporting_cluster_ids`
- keeps stdout aggregate-only and privacy-safe

Support safe rule-based cluster labels such as:

- `too_long`
- `too_cold`
- `too_eager`
- `too_formal`
- `too_intimate`
- `boundary_violation`
- `not_like_me`
- `good_tone`

The exact label set may stay small and deterministic if some suggested labels cannot be supported safely yet, but the output must stay explicit enough for T162 to turn clusters into patch candidates without schema breakage.

Cluster output should make the following explicit:

- `cluster_id`
- `contact_id`
- `cluster_label`
- `supporting_feedback_ids`
- aggregate counts such as total records / action counts
- optional safe summaries or reason-tag aggregates
- no raw draft text, edited text, user notes, boundary notes, or private feedback bodies

Suggested CLI shape:

```text
chat-feedback-cluster --feedback-log <path> --output <private path>
```

If a separate validation-report input materially improves safety, it may be added, but the task must remain clustering-only and deterministic.

## Verification

- Run on synthetic/redacted feedback log inputs.
- Confirm repeated reason tags/actions form stable clusters across repeated runs.
- Confirm cluster ids are stable for identical input ordering/content.
- Confirm stdout does not leak full draft/edit/note text.
- Confirm output does not generate or imply `PreferencePatchCandidate` records yet.

## Expected Handoff Update

Append a T161 implementation record to `docs/07_handoff.md` with:

- files changed
- cluster output shape and CLI name
- one synthetic clustering example
- how cluster ids relate to future `supporting_cluster_ids`
- any follow-up constraints T162-T164 must preserve

## Reviewer Type

adversarial

## Reviewer Focus

Reviewer should verify:

- clustering is deterministic and aggregate-only
- cluster output is explicit enough for later T162 patch generation without already becoming a patch proposal
- no raw feedback text, edited text, notes, or private paths leak into stdout or committed docs
- no ContactSkill/Memory mutation path or runtime injection behavior is smuggled into the clustering layer
