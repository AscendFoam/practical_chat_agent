# Review: T152

Verdict: PASS_WITH_WARNINGS

## Summary

T152 adds 60 committed deterministic regression tests covering the T140-T142 feedback capture, validation, and summary CLI loop. All tests pass. The coverage maps back to all 15 required areas from the T152 task package. No implementation files were modified. No mocks, stubs, or fake success paths were introduced.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: `record_results` in validation report still grows unboundedly

The `TestCompactOutput` tests verify that `edited_text`, `user_note`, and `boundary_note` values do not appear in the serialized validation report JSON. However, the `record_results` list itself (containing `feedback_id`, `candidate_id`, `priority_rank`, `action`, `is_valid`, `issues` per record) is still present in the report dict and is not tested for size bounding. On very large feedback logs, this list could become verbose even without private text.

This was already flagged as R045 and noted in T141 review (N06). The compact-output tests here verify the *content* safety (no private text leakage) but do not assert a size limit on `record_results`. Acceptable for MVP but worth noting.

### N02: `TestPrivateOutputConfinement::test_service_allows_any_output_path` documents a by-design gap

This test explicitly verifies that `FeedbackService` will write to any path the caller requests, including paths outside `private/`. The test correctly documents this as by-design for a single-user offline workflow. However, this means the confinement guarantee is only at the CLI/validator warning level, not at the service enforcement level. If a future caller wraps `FeedbackService` incorrectly, private data could be written outside `private/`.

This was already acknowledged in T140 review (N05) and is carried as R043. The test is honest about the current behavior.

### N03: CLI regression tests do not cover `--validation-report` flag end-to-end

`TestCLISummarizeRegression` covers basic summary, corrupted input, and output-file paths. However, the `--validation-report` flag is only tested through the service-level `TestSummaryValidationMerge`. There is no end-to-end CLI test that invokes `chat-reply-feedback-summary --input ... --validation-report ...` through the Typer CLI runner. The service-level coverage is adequate for regression purposes, but the CLI wiring is untested for this flag.

### N04: No test for append-then-validate-then-summarize pipeline integration

Each test class tests one service in isolation. There is no single test that exercises the full pipeline: append feedback -> validate log -> summarize log with validation report -> verify output. The individual pieces are well-covered, and a pipeline integration test would add marginal value, but it would prove the three services compose correctly.

### N05: `test_approach_labels_loaded` assertion is fragile

`TestSummaryAggregateCounts::test_approach_labels_loaded` asserts that `counts_by_approach_label["conservative_acknowledgment"] == 2`. This depends on both the synthetic plan fixture having specific `approach_label` values AND the feedback records referencing the right `candidate_id` + `priority_rank` pairs. If the fixture changes, this test breaks. This is an intentional regression guard, similar to T150's brittle assertion strategy, and is acceptable.

## Missing Tests

None blocking. All 15 required coverage areas from the T152 task package are addressed.

The test for coverage area 12 (private output confinement) is present and correctly tests the current behavior: validator warns but does not enforce, and service allows any output path. This is documented as by-design.

## Suspicious Implementation Details

None found. The test file:

- Uses only synthetic fixtures with safe ids and text.
- Does not read `private/chat_history/` or any real data.
- Does not mock or stub service behavior; it exercises real services directly.
- CLI tests use `typer.testing.CliRunner` to exercise the real CLI entry point.
- No implementation files were modified.
- No ContactSkill, MemoryFact, approved store record, or planner template is modified by any test.

## Verification

```
PYTHONPATH='src' pytest tests/test_feedback_cli.py -v
60 passed in 0.97s

PYTHONPATH='src' pytest tests/
176 passed in 1.44s (60 T152 + 67 T151 + 49 T150)
```

## Coverage Mapping to T140/T141/T142 Obligations

| Obligation | Test Coverage |
|---|---|
| T140: accept/edit/reject/boundary append | TestFeedbackAppendAccept (2), TestFeedbackAppendEdit (3), TestFeedbackAppendReject (2), TestFeedbackAppendBoundary (3) |
| T140: invalid rank rejected | TestFeedbackInvalidInputs (2: rank=99, rank=0) |
| T140: invalid plan path | TestFeedbackInvalidInputs (2: missing file, invalid JSON) |
| T140: edit-without-text rejected | TestFeedbackAppendEdit::test_edit_without_text_rejected |
| T140: boundary-without-details rejected | TestFeedbackAppendBoundary::test_boundary_without_label_or_note_rejected |
| T140: output privacy | TestPrivacySafety (7) |
| T140: non-mutation | TestNonMutation::test_feedback_does_not_modify_plan_file, test_append_does_not_mutate_existing_records |
| T141: action-specific validation | TestValidationActionSpecific (3) |
| T141: plan reference detection | TestValidationPlanReference (3: missing plan, missing candidate, contact mismatch) |
| T141: corrupted input surfacing | TestCorruptedInput (3 validator tests) |
| T141: privacy warnings | TestPrivateOutputConfinement (2: W_PRIVACY_INPUT, W_PRIVACY_REF) |
| T141: read-only | TestNonMutation::test_validation_is_read_only |
| T142: aggregate counts | TestSummaryAggregateCounts (5) |
| T142: validation report merge | TestSummaryValidationMerge (3) |
| T142: compact output | TestCompactOutput (4) |
| T142: corrupted input | TestCorruptedInput (3 summary tests) |
| T142: read-only | TestNonMutation::test_summary_is_read_only |
| CLI e2e: append | TestCLIAppendRegression (3) |
| CLI e2e: validate | TestCLIValidateRegression (2) |
| CLI e2e: summarize | TestCLISummarizeRegression (3) |

## Remaining Gaps in M4 Feedback Validation

- R044: `reply_plan_id` coherence is regression-guarded for the paths T142 covers but is still not cross-checked against loaded plan context at the service level.
- R038: feedback log may still be mistaken for automatic learning; this is a design-constraint issue, not a test-gap issue.
- R035: relationship-aware quality remains template-driven; T152 does not address this.
- R037: keyword-only policy false-negative limitation; documented in T151 tests but not fixed.

## Recommended Next Action

T152 is complete. M4.5 regression hardening is now structurally complete (T150/T151/T152). Captain should:

1. Update `docs/04_task_board.md` to mark T152 as complete.
2. Reconsider whether R046 can be closed for M4.5, allowing M5 to be authorized.
3. Carry forward R035, R037, R038, R044 into the appropriate future milestone.
