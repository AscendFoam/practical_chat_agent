# Task T163: Patch Review CLI

## Task ID

T163

## Goal

Implement explicit manual review actions for `PreferencePatchCandidate` proposal reports: approve, reject, freeze, archive.

## Why Now

T162 now produces candidate-only patch proposals, but they still cannot influence any runtime behavior. The next smallest safe M5 step is to add explicit human review decisions and preserved review metadata before any approved-patch context integration exists.

T163 must therefore stay strictly in the review layer:

- it may change review status only through explicit human decisions
- it may not rewrite proposal semantics, invent evidence, or inject approved patches into runtime context
- it must preserve the candidate-only and non-mutating M5 architecture

## Inputs To Read

- `docs/review/T160_review.md`
- `docs/review/T161_review.md`
- `docs/review/T162_review.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/data_contracts/preference_patch_contract.md`
- existing review/store patterns in:
  - `src/practical_chat_agent/services/feedback.py`
  - `src/practical_chat_agent/app/main.py`

## Allowed Files

- `src/practical_chat_agent/services/feedback.py`
- `src/practical_chat_agent/app/main.py`
- `docs/data_contracts/preference_patch_contract.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- Do not auto-approve patches.
- Do not batch-approve by default or infer approval from confidence alone.
- Do not modify ContactSkill/MemoryFact directly.
- Do not inject approved patches into `ChatContext`; that is T164.
- Do not rewrite `claim`, `behavior_instruction`, `supporting_feedback_ids`, `supporting_cluster_ids`, `confidence`, or proposal skip decisions as part of review.
- Do not modify `src/practical_chat_agent/core/models.py` unless Captain opens a follow-up bug-fix task.
- Do not call an LLM.
- Do not add sending or platform integration.
- Do not read private chat history.
- Do not claim approved patches are already active in runtime behavior.

## Expected Output

Add a manual review CLI surface that consumes T162 proposal output and writes reviewed proposal JSON under a private path.

Suggested CLI shape:

```text
chat-feedback-review-patch --input <path> --output <path> --decision <approve|reject|freeze|archive> --patch-id <id> --reviewer <name> [--note <text>]
```

Exact flags may differ if the worker finds a cleaner existing project pattern, but the resulting behavior must make the following explicit:

- input proposal report path
- selected patch id or equivalent unambiguous target selector
- explicit human decision
- reviewer identity
- review timestamp/history
- updated per-patch status and review metadata

Review semantics must be conservative:

- only existing candidate patches may be approved
- approval must preserve the original evidence fields
- rejected/frozen/archived patches must not become runtime-ready
- review actions must not silently alter proposal meaning
- stdout must remain privacy-safe and aggregate/id-oriented

T163 should also account for current T162 caveats:

- do not claim `patch_id` is deterministic across repeated T162 runs
- do not rely on `patch_id` alone to interpret evidence changes
- if the worker touches the contract doc, any determinism guarantee text must match the actual UUID-based `patch_id` behavior

## Verification

- Approve/reject/freeze/archive synthetic patches from a T162-style proposal report.
- Confirm approved patches require explicit human review metadata and preserve `supporting_feedback_ids` / `supporting_cluster_ids`.
- Confirm rejected/frozen/archived patches cannot become runtime-ready.
- Confirm review history is preserved across repeated decisions.
- Confirm stdout/output do not leak raw feedback text, edited text, draft text, notes, or private paths beyond the existing accepted path pattern.
- Confirm T163 does not inject approved patches into runtime context.

## Expected Handoff Update

Append a T163 implementation record to `docs/07_handoff.md` with:

- files changed
- review CLI name and decision surface
- status-transition rules used
- approval/runtime-ready gating behavior
- one synthetic review example
- any follow-up constraints T164 must preserve

## Reviewer Type

adversarial

## Reviewer Focus

Reviewer should verify:

- review actions are explicit, auditable, and human-gated
- evidence fields survive review unchanged
- rejected/frozen/archived patches do not become runtime-ready
- approved status is not silently treated as runtime injection
- stdout/artifacts remain privacy-safe and non-mutating
