# Review: T162

Verdict: PASS_WITH_WARNINGS

## Blocking Issues

None.

## Non-Blocking Issues

### N01: Determinism guarantee in contract contains false claim about `patch_id`

`docs/data_contracts/preference_patch_contract.md` "Determinism Guarantee" section states:

> Given identical cluster report input, repeated runs produce identical `patch_id` values...

This is false. `patch_id` is generated via `new_id("patch")` which is UUID-based and non-deterministic. The handoff record (Section 60) correctly notes the exception ("除 patch_id 和时间戳外"), and R053 correctly flags the non-determinism. But the contract makes a claim that directly contradicts the implementation. The contract should remove `patch_id` from the determinism list or add an explicit exception note.

### N02: Raw `input_path` in CLI stdout without sanitization

In `main.py` `chat_feedback_propose_patch`, the `safe_stdout` dict includes `report["input_path"]` directly (from `cluster_data.get("input_path", str(cluster_report_path))`) without passing through `_safe_cli_path()`. This is consistent with the project-wide pattern deferred as R043 and T161 N04, but remains path-handling/privacy debt. The `output_path` is correctly sanitized via `_safe_cli_path()`.

### N03: No committed automated tests

No committed test files cover `PatchProposalService` or `chat-feedback-propose-patch`. R054 already tracks this. Worker performed manual synthetic verification with 4 clusters, which is adequate for current scope but does not prevent regression. This follows the same pattern as T160/T161 and is acceptable pending a future hardening task.

### N04: Missing defensive guard for empty `contact_id`

In `_process_cluster`, if a cluster has a valid label, `record_count >= 2`, and non-empty `supporting_feedback_ids`, but `contact_id` is empty (or missing, defaulting to `""`), the method will attempt to construct a `PreferencePatchCandidate` with `contact_id=""`. This triggers a Pydantic `ValidationError` because the model enforces `min_length=1`. The exception is unhandled and would crash mid-processing.

This edge case is likely unreachable in practice because T161 groups clusters by `(contact_id, label)`, so clusters with valid labels should always have non-empty `contact_id`. However, the lack of a defensive guard means a malformed or manually edited cluster report could cause an ungraceful failure. A `skip_reason: "insufficient_support"` or `"missing_contact"` guard before patch construction would be safer.

### N05: `.claude/settings.json` includes worker session permission artifacts

`.claude/settings.json` has 9 new permission entries from the worker's interactive session. Per T160 review precedent (N05 accepted), this is a workspace artifact rather than a T162 scope violation, but should be noted.

## Missing Tests

- No committed automated tests for `PatchProposalService.propose()`.
- No committed tests for `chat-feedback-propose-patch` CLI command.
- No committed tests for: label-to-type mapping correctness, skip-reason coverage, confidence formula, privacy-safety output verification, determinism verification, or JSON round-trip.
- R054 already tracks this gap. The manual synthetic verification described in the handoff is adequate for T162 scope but does not prevent regression.

## Suspicious Implementation Details

None. The implementation is straightforward, conservative, and well-aligned with the task specification:

- Deterministic label-to-type mapping is a class-level constant dict — no hidden logic.
- Claim and behavior templates are static strings — no LLM involvement.
- `positive_examples` / `negative_examples` are always empty lists — no raw text leakage.
- Skip reasons are explicit and documented.
- Confidence formula is simple and monotonic.
- No auto-approve, no runtime injection, no ContactSkill/Memory mutation, no outbound behavior.

## Recommended Next Action

1. Fix N01: update the determinism guarantee in `docs/data_contracts/preference_patch_contract.md` to remove `patch_id` from the determinism claim or add an explicit exception.
2. Optionally fix N04: add a defensive `contact_id` empty-check before patch construction in `_process_cluster`.
3. Proceed to T163 (Patch Review CLI) under the constraint that T163 must preserve candidate-only, review-only interpretation and must not auto-approve patches.
