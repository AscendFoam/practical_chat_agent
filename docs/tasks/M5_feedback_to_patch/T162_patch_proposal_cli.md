# Task T162: Patch Proposal CLI

## Task ID

T162

## Goal

Generate deterministic, review-only `PreferencePatchCandidate` records from T161 feedback clusters.

## Why Now

T161 now provides stable, privacy-safe aggregate clusters. The next smallest safe M5 step is to convert only sufficiently supported, safely interpretable clusters into candidate-only patch proposals before any human review CLI or runtime-context integration exists.

T162 is therefore the first task that may emit `PreferencePatchCandidate` objects, but it must still remain conservative: under-generate rather than speculate, and stay fully deterministic and privacy-safe.

## Inputs To Read

- `docs/review/T160_review.md`
- `docs/review/T161_review.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/data_contracts/preference_patch_contract.md`
- existing feedback proposal/cluster code in:
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`

## Allowed Files

- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/data_contracts/preference_patch_contract.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- Do not auto-approve or apply patches.
- Do not modify ContactSkill, MemoryFact, approved store records, or planner templates.
- Do not modify `src/practical_chat_agent/core/models.py` unless Captain opens a follow-up bug-fix task.
- Do not add platform integration or sending.
- Do not call an LLM.
- Do not read private chat history.
- Do not claim generated patches are true relationship facts; they are candidate communication preferences only.
- Do not copy raw feedback text, edited text, draft text, user notes, or boundary notes into any patch field.
- Do not assume unlabeled `edit` records were already covered by T161 clustering.

## Expected Output

Add a deterministic proposal generator plus CLI surface that consumes T161 cluster output and emits candidate patch JSON under a private path.

Suggested CLI shape:

```text
chat-feedback-propose-patch --cluster-report <path> --output <private path>
```

Proposal output should make the following explicit:

- `schema_version`
- `generated_at`
- `input_path`
- `candidate_count`
- `skipped_cluster_count`
- `candidates`
- `skipped_clusters`

Each candidate must satisfy all of the following:

- validate as a `PreferencePatchCandidate`
- remain `status = "candidate"`
- preserve default unapproved `review_metadata`
- include non-empty `supporting_feedback_ids`
- include the source cluster via `supporting_cluster_ids`
- keep `positive_examples` / `negative_examples` limited to safe aggregate summaries or identifiers only

The generator must be conservative:

- prefer `record_count >= 2` as the minimum support threshold
- skip ambiguous or unlabeled clusters rather than inventing patch instructions
- make skip reasons explicit, for example:
  - `insufficient_support`
  - `ambiguous_label`
  - `unlabeled_cluster`
  - `no_safe_mapping`

Safe deterministic mappings may stay narrow. At minimum, support obvious conservative cases such as:

- `too_long` -> `length_preference`
- `too_formal` / `too_cold` -> `tone_preference`
- `too_eager` -> `proactivity_preference`
- `too_intimate` / `boundary_violation` -> `boundary_preference`

`good_tone` and `not_like_me` may be skipped if the aggregate signals are not specific enough to produce a safe `behavior_instruction` without speculation.

Confidence must be deterministic, bounded to `0.0-1.0`, and monotonic with evidence strength. It does not need to claim calibrated probability.

## Verification

- Run on synthetic/redacted cluster inputs.
- Confirm at least one cluster can become a candidate and at least one ambiguous or low-support cluster is skipped explicitly.
- Confirm every emitted patch has non-empty `supporting_feedback_ids`.
- Confirm repeated runs on identical input produce identical output.
- Confirm stdout/output do not leak raw feedback text, edited text, draft text, notes, or private paths beyond the existing project-wide accepted path pattern.
- Confirm no emitted patch is automatically approved, runtime-ready, or injected into runtime context.

## Expected Handoff Update

Append a T162 implementation record to `docs/07_handoff.md` with:

- files changed
- proposal CLI name and output shape
- deterministic mapping rules used
- explicit skip reasons used
- one synthetic proposal example
- any follow-up constraints T163-T164 must preserve

## Reviewer Type

adversarial

## Reviewer Focus

Reviewer should verify:

- proposal generation is deterministic, candidate-only, and non-mutating
- ambiguous or edit-only signals are skipped rather than over-interpreted
- `supporting_feedback_ids` and `supporting_cluster_ids` are preserved correctly
- `positive_examples` / `negative_examples` stay privacy-safe
- no review/apply/runtime-injection behavior is smuggled into the proposal layer
