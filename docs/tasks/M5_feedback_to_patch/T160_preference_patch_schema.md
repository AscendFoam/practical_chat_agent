# Task T160: PreferencePatch Schema

## Task ID

T160

## Goal

Define `PreferencePatchCandidate` schema for turning repeated human feedback into reviewable communication-policy patches.

This task only defines models/contracts. It must not generate, approve, or apply patches.

## Why Now

M4 captures and summarizes feedback. The next safe step is to define a candidate patch shape that can later connect feedback to communication preferences without training, automatic memory mutation, or ContactSkill overwrite.

M4.5 is now complete, so T160 becomes the first authorized M5 task. It must keep M5 narrow: schema only, candidate only, review only.

## Inputs To Read

- `docs/review/M4_5_review.md`
- `docs/review/T140_review.md`
- `docs/review/T141_review.md`
- `docs/review/T142_review.md`
- `docs/review/T152_review.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- existing review/store/runtime models in `src/practical_chat_agent/core/models.py`

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `docs/data_contracts/preference_patch_contract.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- Do not call an LLM.
- Do not implement clustering, proposal generation, review CLI, or runtime injection.
- Do not modify ContactSkill/MemoryFact/store records.
- Do not auto-approve or apply patches.
- Do not read private chat history.

## Expected Output

Schema should support:

- `patch_id`
- `contact_id`
- `patch_type`
- `claim`
- `behavior_instruction`
- `positive_examples` / `negative_examples` as optional safe references or summaries
- `supporting_feedback_ids`
- `affected_candidate_types`
- `confidence`
- `sensitivity`
- `status = candidate`
- timestamps and review metadata placeholders

Suggested `patch_type` values:

- `tone_preference`
- `length_preference`
- `boundary_preference`
- `topic_preference`
- `question_style`
- `humor_style`
- `repair_style`
- `proactivity_preference`

Schema should also make the following explicit:

- review-only lifecycle: candidate now, approved/rejected/frozen/archived later
- provenance via `supporting_feedback_ids`
- optional safe references to feedback aggregates or cluster ids, without embedding raw feedback text
- review metadata placeholders compatible with the existing store/review style
- enough structure for later T161-T164 tasks without requiring schema breakage

Suggested supporting fields:

- `patch_id`
- `contact_id`
- `patch_type`
- `instruction_scope`
- `claim`
- `behavior_instruction`
- `rationale_summary`
- `supporting_feedback_ids`
- `supporting_cluster_ids` optional
- `affected_candidate_types`
- `status`
- `confidence`
- `sensitivity`
- `created_at`
- `updated_at`
- `review_metadata`

## Verification

- Compile changed Python files.
- Validate one synthetic candidate patch with supporting feedback ids.
- Validate that empty supporting feedback ids are rejected or explicitly represented as unsafe.
- Confirm the schema does not imply runtime readiness by default.
- Confirm no field requires raw transcript text, edited text, or private note bodies.

## Expected Handoff Update

Append a T160 implementation record to `docs/07_handoff.md` with:

- files changed
- model/enum names added
- one synthetic validation example
- how the schema keeps M5 candidate-only
- any follow-up constraints T161-T164 must preserve

## Reviewer Type

adversarial

## Reviewer Focus

Reviewer should verify:

- the schema is genuinely candidate-only and not silently runtime-ready
- supporting feedback evidence is structurally required or clearly marked unsafe when absent
- no ContactSkill/Memory mutation path is smuggled into the model layer
- the contract is compatible with later clustering/review tasks without overcommitting to implementation details
