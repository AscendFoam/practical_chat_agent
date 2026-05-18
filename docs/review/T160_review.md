# Review: T160

Verdict: PASS_WITH_WARNINGS

## Task Summary

T160 defines the `PreferencePatchCandidate` Pydantic model and its data contract. The task is schema-only: no clustering, proposal generation, review CLI, or runtime injection.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: `instruction_scope` is a free-form string with a default but no validation

The field defaults to `"per_contact"` but accepts any string. While this is acceptable for schema-only, T162 should observe actual usage before deciding whether to constrain to a Literal.

**Why non-blocking**: The task package explicitly lists this as an optional field and schema-only stage does not require enum tightening. R047 already tracks this risk.

### N02: `positive_examples` and `negative_examples` have no structural enforcement of safe-only content

These are `list[str]` fields with no constraint that they contain summaries or references rather than raw feedback text. The contract document says they should be safe references, but the model layer does not enforce this.

**Why non-blocking**: The contract document explicitly forbids storing raw feedback text. R048 already tracks this risk. T162 proposal generation is the enforcement point, not T160.

### N03: No committed automated tests for the new model

T160 adds `PreferencePatchType` and `PreferencePatchCandidate` to models.py but does not add any committed pytest tests. The worker's verification was inline/synthetic only.

**Why non-blocking**: The task package says "Validate one synthetic candidate patch" and "Validate that empty supporting feedback ids are rejected." The worker did this inline and reported results, which satisfies the stated verification requirement. However, unlike T150/T151/T152 which established the committed-test precedent, T160 does not carry that forward. This is consistent with T110-T142 pattern where committed tests were deferred to T150. A future regression-hardening pass should cover PreferencePatchCandidate validation.

### N04: `schema_version` is a plain string, not validated against a known version set

`schema_version: str = "preference_patch_candidate_v1"` has no constraint beyond being a string. If a future version is introduced, old and new versions would both pass silently.

**Why non-blocking**: This matches the existing pattern in `ReplyFeedbackLog`, `ContactSkillStoreFile`, etc. Consistency with the codebase is more important than introducing a new validation pattern here.

### N05: Some files outside the `Allowed files` list were modified in the working tree

The working tree contains modifications to `docs/00_raw_idea.md`, `docs/01_feasibility_report.md`, `docs/03_architecture.md`, `docs/04_task_board.md`, `docs/05_decision_log.md`, `docs/06_eval_protocol.md`, `docs/tasks/M5_feedback_to_patch/T160_preference_patch_schema.md`, and `.claude/settings.json`.

**Why non-blocking**: These appear to be prior Captain updates and worker environment artifacts that are not part of the T160 diff itself. The T160-specific changes are confined to the allowed files: `models.py`, `preference_patch_contract.md` (new), `07_handoff.md`, and `08_risks_and_open_questions.md`. The task package does not list these governance docs as modified by T160, but they appear to have been updated by prior Captain work in the same working tree. This is a working-tree hygiene note, not a T160 scope violation.

## Missing Tests

No committed pytest tests for `PreferencePatchCandidate` validation. This is consistent with the pre-T150 pattern but worth noting since T150/T151/T152 established a strong committed-test precedent. A future regression-hardening task should add:
- valid candidate construction
- empty `supporting_feedback_ids` rejection
- `is_runtime_ready()` default-false gate
- status lifecycle expectations
- confidence range enforcement
- JSON round-trip fidelity

## Suspicious Implementation Details

None found. The implementation is clean and narrow:

1. `PreferencePatchType` is a Literal with exactly the 8 values specified in the task package.
2. `PreferencePatchCandidate` reuses existing `DistillationStatus`, `DistillationSensitivity`, and `DistilledArtifactReviewMetadata` types correctly.
3. `supporting_feedback_ids` has `min_length=1`, structurally enforcing evidence.
4. `is_runtime_ready()` delegates to `DistilledArtifactReviewMetadata.is_runtime_ready()`, which requires `status == "approved"` AND `reviewed_by_human == True` AND `last_decision == "approved"`.
5. No field stores raw transcript text, edited text, or private note bodies.
6. No ContactSkill/Memory mutation path, no auto-approve, no LLM call, no runtime injection.
7. The model is placed correctly before `ChatContext.model_rebuild()`, so forward references resolve properly.
8. The data contract document is clear, does not claim future work as complete, and includes explicit anti-patterns.

## Verification

- Compile: `models.py` compiles cleanly.
- Existing tests: 176/176 pass, zero regressions.
- Synthetic validation: valid candidate created with `status == "candidate"`, `is_runtime_ready() == False`, `reviewed_by_human == False`.
- Empty `supporting_feedback_ids` correctly raises `ValidationError`.
- JSON round-trip preserves all fields.
- All 8 `PreferencePatchType` values accepted.

## Recommended Next Action

T160 is complete. Current Unique Task may advance to T161 (feedback clusterer), subject to Captain decision. T161 must:
- produce cluster IDs compatible with `supporting_cluster_ids`
- enforce that patches derive from clustered feedback, not single records
- not auto-generate patches directly
