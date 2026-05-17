# Review: T141

Verdict: PASS_WITH_WARNINGS

## Summary

T141 implements a read-only validator for T140 feedback logs. The implementation checks log readability, JSON/schema validity, action-specific required fields, source-plan reference existence, candidate alignment, contact-id alignment, and private-path confinement. All output is safe summaries (ids, counts, warning codes) with no private text leakage. The validator does not mutate any files. No proposals, memory updates, ContactSkill changes, LLM calls, or platform integration were added.

## Blocking Issues

None.

## Non-Blocking Issues

### N01: `input_path` in CLI output is the raw user-supplied string

The CLI `safe_output` dict at main.py:2110 emits `report["input_path"]` directly, which is `str(input_path)` from the user-supplied `--input` option. Other CLI commands in this project use `_safe_cli_path()` to normalize paths to relative-from-CWD. This is a minor inconsistency — the path is a file-system path the user already knows, not private content — but it differs from the established pattern.

**Why:** Low risk since the user chose the path. Consistency with `_safe_cli_path` would be a style improvement.

### N02: `reply_plan_id` coherence check is not implemented

The task package says to check "reply_plan_id / candidate metadata are internally coherent enough for later review use." The worker's handoff note acknowledges this gap: the validator does not verify that `record.reply_plan_id` matches the loaded plan's `source_context.approved_contact_skill_record_id`. This is a lightweight semantic gap.

**Why:** The `reply_plan_id` field is a T140 proxy (using `approved_contact_skill_record_id`) rather than a stable plan identifier. Cross-checking it would require loading the plan for every record, even those without `source_plan_path`. The worker correctly notes this can be addressed in T142 if needed. Not blocking because the field is optional and the primary purpose (candidate alignment) is already covered.

### N03: `_is_private_path` uses a simple directory-name heuristic

The `_is_private_path` method at feedback.py:198-203 checks whether any path component is named `private` (case-insensitive). This matches a directory anywhere in the path tree, not just a specific root-relative prefix like `private/`. For example, `/home/user/project/private_data/output.json` would pass the check even though it's not the intended `private/` directory.

**Why:** The project only uses `private/` at the repo root, so false positives are unlikely in practice. A stricter check (e.g., `resolved.is_relative_to(repo_root / "private")`) would be more precise but would require knowing the repo root. Acceptable for MVP.

### N04: `_resolve_plan_path` depends on CWD for relative paths

The `_resolve_plan_path` method at feedback.py:205-212 first tries the raw relative path against CWD, then falls back to log-directory-relative resolution. If the user runs the CLI from a different directory than where `chat-reply-feedback` was run, the relative path may not resolve even though the plan file exists elsewhere.

**Why:** The worker's handoff note already documents this risk. It's inherent to storing relative paths as strings. The two-step resolution (CWD then log-dir) is a reasonable mitigation.

### N05: `strict_mode` is stored in the report dict but never read

The `_init_report` method stores `strict_mode` in the report dict, but nothing in `FeedbackValidationService` reads it. The strict behavior is handled entirely in the CLI layer (main.py:2133-2136).

**Why:** Minor dead data. Not harmful since the CLI uses `strict` directly. The field is harmless documentation of the mode used.

### N06: `record_results` list could grow large

Each validated record produces a dict in `record_results` with feedback_id, candidate_id, priority_rank, action, is_valid, and issues. For a large feedback log, this list could produce very large JSON output on stdout.

**Why:** Expected log sizes are small (single-user offline tool). Not a practical concern now. T142 summary exporter may provide a more compact alternative.

## Missing Tests

- No committed automated tests. Worker verified via manual CLI invocations on synthetic fixtures. This is consistent with the project convention of deferring committed tests to T150/T152.
- Missing test coverage:
  - Good log validation (all four actions valid)
  - Bad log validation (edit without text, boundary without details)
  - Missing plan reference
  - Corrupted JSON input
  - Schema-invalid input
  - Privacy warnings (input outside `private/`, plan ref outside `private/`)
  - Read-only confirmation (no file mutation)
  - stdout privacy (no private text leaked)
  - `--strict` exit code behavior
  - Contact-id mismatch detection
  - Missing candidate detection

All deferred to T150/T152 per project convention.

## Suspicious Implementation Details

None found. The implementation is straightforward and uses standard patterns. No mocks, stubs, hardcoded outputs, or fake success paths detected.

Specific checks:
- Corrupted/unreadable input is explicitly reported with `corrupted_reason` and `corrupted_input_count=1`, never silently treated as success (directly addresses T140 N01).
- Plan loading uses `ReplyPlan.model_validate_json` for real validation, not a stub.
- Candidate matching checks both `candidate_id` and `priority_rank`, matching the T140 record semantics.
- The validator never writes to any file or calls any mutating method.
- Privacy checks (`_is_private_path`) are applied to both input log and resolved plan references.
- `--strict` only affects exit code, not validation logic — the report is always the same.

## Scope Compliance

- **Allowed files checked:** `feedback.py`, `main.py`, `07_handoff.md` — all within scope. `models.py` was not modified, which is correct since T140 already defined the schema.
- **No forbidden files modified.**
- **No `private/chat_history/` reads.**
- **No ContactSkill/MemoryFact/approved store mutation.**
- **No feedback log, ReplyPlan, or planner template mutation (read-only confirmed).**
- **No auto-send, DB, vector DB, LLM, or realtime integration.**
- **No private content in stdout (only ids, counts, warning codes, and safe paths).**
- **No T142/T160/T162 proposal behavior.**

## T140 Deferred Warning Resolution

- **N01 (corrupted-log silent reset):** Resolved. T141 explicitly reports corrupted/unreadable input via `corrupted_reason` and `corrupted_input_count`, never silently normalizes it.
- **N02 (stale `source_plan_path`):** Partially addressed. T141 detects missing plan files and reports `missing_plan`, surfacing staleness. Path resolution uses CWD-first then log-dir-relative fallback (N04 above).
- **N05 (no private-path enforcement):** Resolved. T141 adds `_is_private_path` checks and surfaces `W_PRIVACY_INPUT` / `W_PRIVACY_REF` warnings.

## Recommended Next Action

- Captain should accept T141 as complete with warnings.
- T142 (feedback summary exporter) should address N02 (reply_plan_id coherence) if cross-referencing is needed for summary output.
- T150/T152 should add committed regression tests covering all validator paths.
- Update `docs/04_task_board.md` to mark T141 complete when Captain decides.
