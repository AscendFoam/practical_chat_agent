# Review: T163

Verdict: PASS_WITH_WARNINGS

## Blocking Issues

None.

## Non-Blocking Issues

### N01: Contract determinism claim about `patch_id` still unfixed

`docs/data_contracts/preference_patch_contract.md` "Determinism Guarantee" section (line 256) still states:

> Given identical cluster report input, repeated runs produce identical `patch_id` values...

This was flagged as T162 N01 (deferred). The T163 worker added the "Patch Review Contract (T163)" section to the same file, which means the contract was touched — and the T163 task package explicitly states:

> if the worker touches the contract doc, any determinism guarantee text must match the actual UUID-based `patch_id` behavior

The determinism guarantee was not corrected. The new T163 section correctly avoids making determinism claims about patch_id, but the existing false claim remains in the file. This is a missed opportunity for a one-line fix and the task instruction was not followed.

### N02: No committed automated tests

No committed test files cover `PatchReviewService` or `chat-feedback-review-patch`. R054 already tracks this gap across the M5 patch layer (T160/T161/T162/T163). The worker performed manual synthetic verification with 10 test cases described in the handoff record, which is adequate for current scope but does not prevent regression. This follows the established M5 pattern and is acceptable pending a future hardening task.

### N03: Write-back to input file by default (R057)

`PatchReviewService._finalize` defaults `write_path` to `input_path` when `--output` is not specified. If the write fails mid-operation (partial write, disk full, crash), the input file may be corrupted. The implementation writes the full JSON atomically only in the sense that `write_text` is a single call — it does not use a temp-file-rename pattern. R057 correctly documents this.

### N04: Review history unbounded growth (R058)

`_apply_decision` appends to `review_metadata.history` on every review call without any cap. Over many repeated review cycles, `history` could grow unboundedly. R058 correctly documents this. A reasonable cap (e.g., keep last N history entries) could be added later.

### N05: `.claude/settings.json` permission entries

`.claude/settings.json` has 5 new permission entries from the worker's interactive session. Per T160/T161/T162 review precedent (all accepted), this is a workspace artifact rather than a task-scope violation.

## Missing Tests

- No committed automated tests for `PatchReviewService.review()`.
- No committed tests for `chat-feedback-review-patch` CLI command.
- No committed tests for: approval gate semantics, history accumulation, evidence preservation across decisions, invalid decision rejection, privacy-safe stdout validation, re-approval after rejection/freeze, or output-to-separate-file non-destructive behavior.
- R054 already tracks this gap. The manual synthetic verification described in the handoff (10 test cases) is adequate for T163 scope but does not prevent regression.
- 176 existing committed tests pass with zero regressions.

## Suspicious Implementation Details

None. The implementation is straightforward, conservative, and well-aligned with the task specification:

- `PatchReviewService` is a single class with clear separation of load → find → apply → finalize.
- Uses existing model types (`DistilledArtifactReviewDecision`, `DistillationStatus`, `DistilledArtifactReviewMetadata`) consistent with T122 review patterns.
- Evidence fields (`supporting_feedback_ids`, `supporting_cluster_ids`, `claim`, `behavior_instruction`, `confidence`, `sensitivity`) are never modified during review — the implementation only updates status and review metadata fields.
- `_apply_decision` correctly appends to history rather than replacing, and updates the last-decision fields to reflect the most recent decision.
- `_finalize` correctly constructs a privacy-safe stdout dict with only aggregate ids, statuses, and safe metadata — no raw feedback text, edited text, notes, or private paths exposed.
- CLI uses `_safe_cli_path()` for path sanitization in stdout, consistent with existing project patterns.
- CLI enforces `--input` existence and readability via Typer options, reducing the chance of silent errors.
- Error handling covers: invalid decision strings, missing proposal files, unreadable files, invalid JSON, wrong schema version, missing patch_id (with helpful listing of available ids), and invalid patch data (Pydantic validation failure).
- No auto-approve, no auto-apply, no runtime injection, no LLM invocation, no ContactSkill/MemoryFact mutation, no outbound behavior.

One minor observation: `_finalize` re-searches the report for the updated patch and re-validates it via `PreferencePatchCandidate.model_validate()`, even though `_apply_decision` already mutated `candidate_entry["patch"]` in-place and the data was just written. The re-validation is defensive (it would catch serialization/deserialization round-trip issues) and the code is clear, so this is not a problem — merely noted for completeness.

## Recommended Next Action

1. Fix N01: update the "Determinism Guarantee" in `docs/data_contracts/preference_patch_contract.md` to remove `patch_id` from the determinism claim, or add an explicit exception noting UUID-based non-determinism. The task package explicitly required this if the contract was touched.
2. Proceed to T164 (Approved Patch Compact Context) under the constraint that T164 must only consume patches with `status == "approved"` and `is_runtime_ready() == True`, must preserve review history, and must not claim approved patches are already active in runtime behavior.
3. R054, R057, and R058 should be carried forward and eventually addressed in a future hardening task.
