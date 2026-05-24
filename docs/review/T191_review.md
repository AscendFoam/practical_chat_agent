# Review: T191

Verdict: PASS_WITH_WARNINGS

## Summary

T191 adds a conservative `RelationshipSignal` model and a deterministic `RelationshipSignalExtractor` that turns boundary-labeled feedback records into evidence-backed relationship signals. The extractor covers three boundary labels (`boundary_violation`, `too_intimate`, `too_eager`) producing signals for three of eight relationship dimensions. Only boundary-labeled feedback with known high-confidence patterns produces signals; all other actions and labels are silently skipped. No raw text is stored, no relationship state is mutated, no LLM is called, and no delta candidates are generated.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: Worker handoff test count is inaccurate

The T191 Worker Completion Record in `docs/07_handoff.md` states "T191 test suite: 22 tests" but the actual committed test file contains 21 tests (confirmed by `pytest` output: 21 passed). The separate `docs/worker_summary/T191_worker_summary.md` correctly states 21. This is a documentation accuracy issue in the handoff, not a code issue.

### N02: `.claude/settings.json` workspace-artifact overrun

`.claude/settings.json` was modified to add compile and test commands to the allowed-tools list. This is the same pattern accepted in T160–T190 reviews: it is a workspace-level permission artifact rather than a T191 functional change. Accepted.

### N03: `RelationshipSignal` lacks `updated_at` field

`RelationshipState` and `RelationshipDeltaCandidate` both have `updated_at` fields for tracking review-lifecycle mutations, but `RelationshipSignal` only has `created_at`. When T193 approves a signal and updates `status` and `review_metadata`, there will be no timestamp recording when that update occurred. The `review_metadata` history entries carry their own timestamps, so the gap is bounded, but the asymmetry with the other M8 models is worth noting for T193.

### N04: `_BOUNDARY_RULES` uses `# type: ignore[arg-type]` to bypass Literal typing

The extraction rules dictionary stores `dimension` and `direction` as plain strings, then passes them to `RelationshipSignal()` fields typed as `RELATIONSHIP_DIMENSION_NAMES` and `RelationshipDeltaDirection`. The `# type: ignore[arg-type]` suppresses the type mismatch. This works correctly at runtime because Pydantic validates the Literal values, but it weakens static type safety. A future refactor could define a structured rule type or use the Literal values directly to avoid the ignore directives.

### N05: Only 3 of 8 relationship dimensions have extraction rules

The extractor covers `boundary_risk`, `intimacy_level`, and `initiative_allowance`. The remaining five dimensions (`familiarity`, `trust`, `warmth`, `reciprocity`, `conflict_level`) have no extraction rules. This is explicitly documented as intentional (no clear high-confidence mapping from current boundary labels), and the `metadata_derived` provenance type is defined but not yet used. Future tasks or rule expansions can address this, but consumers of T191 signals should expect sparse coverage.

## Missing Tests

### M01: No test exercises `is_runtime_ready() == True` on an approved `RelationshipSignal`

All model-level tests check the default `candidate` status where `is_runtime_ready()` returns `False`. No test constructs a signal with `status="approved"` and `review_metadata` set to simulate human approval, then asserts `is_runtime_ready() == True`. This is non-blocking because the approval lifecycle belongs to T193, but it means the approval→runtime-ready path on `RelationshipSignal` is untested in committed code.

### M02: No test for `signal_id` format or non-emptiness

No test asserts that `signal_id` is auto-generated, non-empty, or follows the `"relsig_"` prefix pattern produced by `new_id("relsig")`. This is low-risk because `new_id()` is well-tested elsewhere, but it means `RelationshipSignal`-specific ID generation has no dedicated coverage.

## Suspicious Implementation Details

None found. The implementation is clean, minimal, and deterministic. The extractor uses a static rule table, produces signals with no raw text, and skips all ambiguous inputs. No mocks, stubs, hardcoded outputs, LLM calls, or fake success paths exist.

## Recommended Next Action

T191 is complete as a conservative signal-extraction task. The next Current Unique Task should be T192 (relationship delta candidate generation), which will consume T191 signals and produce reviewable `RelationshipDeltaCandidate` instances. Captain should update `docs/04_task_board.md` to mark T191 complete and set T192 as the Current Unique Task.
