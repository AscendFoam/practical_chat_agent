# Review: T193

Verdict: PASS_WITH_WARNINGS

## Task Goal

Implement explicit human review over `RelationshipDeltaCandidate` records with approve/reject/freeze/archive actions, while keeping review separate from state application.

## What Changed

### `src/practical_chat_agent/services/feedback.py`

Added `RelationshipDeltaReviewService` class with `review_delta()` method (~80 lines). Design:

1. Accepts a `RelationshipDeltaCandidate`, decision string, reviewer identity, and optional note.
2. Returns a **new** delta via `model_copy(deep=True)` — the original delta is not mutated.
3. Validates decisions: `approve`, `reject`, `freeze`, `archive`. Case-insensitive, whitespace-tolerant via `strip().lower()`.
4. Reuses existing `DistilledArtifactReviewDecision` / `DistilledArtifactReviewMetadata` patterns from T120/T163.
5. Appends a review decision to `review_metadata.history`, updates `status`, `review_state`, `reviewed_by_human`, `last_decision`, reviewer fields, and `updated_at`.
6. Approved deltas with `reviewed_by_human=True` and `last_decision="approved"` report `is_runtime_ready() == True`.
7. Evidence refs, signal refs, dimension changes, and delta rationale are preserved unchanged.
8. All-or-nothing review: all dimensions in a delta are reviewed together.

### `src/practical_chat_agent/app/main.py`

Added `relationship-review-delta` CLI command with:
- `--input` (required): Path to a `RelationshipDeltaCandidate` JSON file.
- `--output` (optional): Output path; defaults to overwriting input.
- `--decision` (required): `approve`, `reject`, `freeze`, or `archive`.
- `--reviewer` (required): Reviewer identity.
- `--note` (optional): Human review note.

The CLI reads the delta JSON, calls the service, writes the updated delta, and outputs a safe JSON summary using `_safe_cli_path()`.

### `tests/test_relationship_review_cli.py` (new)

22 tests covering:
- Valid review actions (approve, reject, freeze, archive, with note — 5 tests).
- Invalid action handling (invalid decision error, case-insensitive, whitespace tolerance — 3 tests).
- Runtime-ready path (approved is ready, candidate is not, rejected is not — 3 tests).
- Preservation through review (evidence_refs, signal_refs, dimension_changes, contact_id/source_state_id, delta_rationale — 5 tests).
- Review metadata updates (approve metadata, reject metadata, updated_at advances — 3 tests).
- No state mutation / deep copy (original not mutated, history accumulation — 2 tests).
- All-or-nothing semantics (multi-dimension reviewed as whole — 1 test).

### `docs/data_contracts/relationship_state_contract.md`

Updated scope to include T193, updated lifecycle diagram, added "RelationshipDeltaCandidate Review (T193)" section documenting review actions, flow, safety constraints, and metadata pattern.

### `docs/07_handoff.md`

Added T193 Worker Completion Record documenting what changed, service design, CLI command, relationship to T192, verification results, and explicit non-actions.

### `.claude/settings.json`

Workspace-artifact permission entries added (consistent with all prior tasks).

## Verification

1. Compile check: `python -m py_compile src/practical_chat_agent/app/main.py src/practical_chat_agent/services/feedback.py src/practical_chat_agent/core/models.py` — passed.
2. T193 test suite: 22 tests passed, 0 failures.
3. Full existing test suite: 510 tests passed (22 new + 488 existing), 0 regressions, no regressions detected.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: No CLI-level (Typer) integration tests

All 22 tests target `RelationshipDeltaReviewService` directly. The `relationship-review-delta` Typer command — including file I/O, JSON deserialization error handling, `_safe_cli_path()`, and the write-back path — is not exercised by any committed test. This is consistent with the deferred-test pattern seen in T163 N02, T162 N03, and T161 N02. The service layer is well-covered, but the CLI wiring is verified only by the worker's private verification, not by committed regression tests.

### N02: Default input file overwrite has no safety mechanism

When `--output` is omitted, the reviewed delta overwrites the input file in place. If the write is interrupted or corrupted, the original candidate is lost. This follows the same pattern as T163 N03 (`chat-feedback-review-patch`). The worker summary documents this risk.

### N03: No evidence pre-validation gate before approval

Unlike T122 which requires a passed `evidence_validation_report.json` before approving store records, T193's `review_delta()` accepts any decision without pre-validating evidence refs. This is by design per the task scope ("The reviewer decides without automated evidence pre-validation"), but it means an approved delta could have dangling `evidence_refs` that no longer resolve. This creates a dependency: later state-application tasks (T194/T195) may need to re-validate evidence before applying approved deltas.

### N04: `.claude/settings.json` workspace-artifact overrun

Permission entries for T193 verification commands were added. This is consistent with every prior task and is a workspace artifact, not a task-scope violation.

## Missing Tests

### M01: No CLI test exercises the Typer command

As noted in N01, the CLI layer is untested by committed tests. Specifically missing:
- Valid delta JSON → successful review and output.
- Invalid delta JSON → `BadParameter` exit.
- Unreadable input path → error handling.
- `--output` to a new directory → `mkdir` behavior.
- `--note` propagation through the CLI to the service.

### M02: No test for empty-string `note`

If `--note ""` is passed, the service receives `note=""` which is falsy (`if note:` is False), so neither `history[-1].notes` nor `decision_notes` gets the note. This is correct behavior but is not explicitly tested. The tested path (`note="Looks reasonable."`) is the happy path.

## Suspicious Implementation Details

### S01: `DistilledArtifactReviewDecision(reviewer_name=None)`

The service always passes `reviewer_name=None` to `DistilledArtifactReviewDecision`. The `reviewer` CLI parameter is treated as a reviewer ID stored in both `last_reviewer_id` and `reviewer_id` in the history entry. The `reviewer_name` field is never populated. This works correctly but means the name/ID distinction (available in T122's `--reviewer-id` / `--reviewer-name` split) is collapsed into a single field. The design is simpler and acceptable for T193's scope, but if a future task needs distinct reviewer name vs. ID, it would need to add a new CLI parameter.

### S02: `write_path.parent.mkdir(parents=True, exist_ok=True)`

The CLI ensures the output parent directory exists before writing. In the default case (output = input_path), this is a no-op since the parent already exists. This is safe but slightly unnecessary in the common case.

## Scope Compliance

- Allowed files check:
  - `src/practical_chat_agent/app/main.py`: Changed. Within allowed scope.
  - `src/practical_chat_agent/services/feedback.py`: Changed. Within allowed scope.
  - `src/practical_chat_agent/core/models.py`: No changes needed. Correct — T190 schemas were sufficient.
  - `tests/test_relationship_review_cli.py`: New file. Within allowed scope.
  - `docs/data_contracts/relationship_state_contract.md`: Changed. Within allowed scope.
  - `docs/07_handoff.md`: Changed. Within allowed scope.
  - `.claude/settings.json`: Changed. Consistent workspace-artifact pattern.

- Forbidden scope compliance:
  - No auto-approve of relationship changes. Verified.
  - No auto-apply of approved deltas to `RelationshipState`. Verified.
  - No unrelated memory/ContactSkill records mutation. Verified.
  - No messages sent. Verified.
  - No state mutation occurs. Verified (deep copy tested).

## Recommended Next Action

T193 is complete and passes the review gate. It correctly produces an auditable review layer over delta candidates without state application. The next M8 tasks remain:

1. **T194: RelationshipState compact context** — wire approved deltas into compact context (context-only, no state mutation).
2. **T195: Relationship-aware reply eval** — evaluate how the review/approval flow integrates with the reply planner.

Key deferred concerns to carry forward:
- The no-CLI-test pattern (N01/M01) is consistent with project history but should eventually be addressed.
- T194/T195 designers should note T193's lack of evidence pre-validation (N03) — approved deltas may have stale evidence refs that need validation at application time.
- T194 should clarify whether `relationship-review-delta --output` overwrite risk (N02) warrants a backup convention or copy-on-write default.
