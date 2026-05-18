# T162 Review Explained

## 1. What T162 Is Trying to Accomplish (Plain Language)

Imagine you're building a chat assistant that helps you write replies to your contacts. You've already built a system where, after the assistant suggests some reply drafts, you can give feedback like "too long", "too formal", "too cold", etc. (that was M4).

Earlier in M5, you also built a system that groups similar feedback together — for example, three people all saying "too long" get clustered together (that was T161).

**T162 is the bridge between "grouped feedback" and "actionable improvement proposals".** Specifically, it takes those grouped feedback clusters and says: "Based on this cluster of 3 'too long' feedbacks, I propose we should adjust reply length for this contact. Here's the proposal — please review it before we do anything."

The key design principle is **conservative safety**: the system would rather skip a cluster than guess wrong. It only generates proposals for feedback patterns it can confidently interpret (like "too long" meaning "prefer shorter replies"), and it **never** auto-approves or auto-applies anything. Every proposal stays as "candidate" until a human explicitly reviews it.

## 2. Implementation Details

### 2.1 Task Goal

Generate deterministic, review-only `PreferencePatchCandidate` records from T161 feedback clusters, using a CLI command.

### 2.2 Task Flow

```
T161 Cluster Report (JSON)
  → PatchProposalService reads clusters
  → For each cluster:
      1. Check: does it have a label? (skip if unlabeled)
      2. Check: does it have ≥2 records? (skip if insufficient support)
      3. Check: is the label in our safe mapping table? (skip if no safe mapping)
      4. Check: does it have supporting feedback IDs? (skip if empty)
      5. Map label → patch type + generate claim + generate behavior instruction
      6. Compute deterministic confidence score
      7. Construct PreferencePatchCandidate with status="candidate"
  → Output proposal report JSON
```

### 2.3 Code Changes

#### `src/practical_chat_agent/services/feedback.py` — New `PatchProposalService`

Added a new service class with:

- **6 label-to-patch-type mappings** (deterministic dictionary):
  - `too_long` → `length_preference`
  - `too_formal` / `too_cold` → `tone_preference`
  - `too_eager` → `proactivity_preference`
  - `too_intimate` / `boundary_violation` → `boundary_preference`

- **Skip logic** for clusters that don't meet safety thresholds:
  - `insufficient_support` — fewer than 2 records or empty feedback IDs
  - `unlabeled_cluster` — no label provided
  - `no_safe_mapping` — label exists but isn't in the safe mapping table (includes `good_tone`, `not_like_me`, and any unknown labels)

- **Confidence formula**: `min(0.3 + 0.15 * (record_count - 1), 0.9)` — simple, monotonic, capped at 0.9. More evidence = higher confidence, but never claims probability.

- **Privacy-safe by construction**: `positive_examples` and `negative_examples` are always empty lists. All text is generated from static templates. No raw feedback text, edit text, user notes, or boundary notes appear anywhere in the output.

#### `src/practical_chat_agent/app/main.py` — New CLI command

Added `chat-feedback-propose-patch` with:
- `--cluster-report` (required): path to T161 cluster report JSON
- `--output` (optional): path to write proposal JSON

The CLI sanitizes the output path via `_safe_cli_path()` and produces a structured JSON summary to stdout.

#### `docs/data_contracts/preference_patch_contract.md` — New contract section

Added "Patch Proposal Output Contract (T162)" documenting the output shape, mapping table, skip reasons, confidence formula, privacy constraints, and determinism guarantee.

#### `docs/07_handoff.md` — Section 60

Full implementation record with mapping rules, skip rules, synthetic verification example, and T163-T164 constraints.

#### `docs/08_risks_and_open_questions.md` — New risks

Added R053 (non-deterministic `patch_id`), R054 (no committed tests), R055 (un-calibrated confidence).

### 2.4 Significance for Future Development

T162 establishes the **proposal generation layer** in the M5 feedback-to-patch pipeline. It is deliberately narrow and conservative:

- **T163** (Patch Review CLI) will consume these proposals and allow human review/approval. T162 guarantees every proposal starts as `status="candidate"` with `reviewed_by_human=False`.
- **T164** (Approved Patch Compact Context) will only consume patches that have passed T163 review (`status="approved"`, `is_runtime_ready()=True`). T162 ensures no proposal can bypass this gate.
- The 6-label mapping table is intentionally small. As the feedback system matures, future tasks can expand the mapping, but T162 proves the conservative pattern works.

This task also demonstrates that the M5 feedback loop is progressing correctly: feedback → clustering → proposal → review → application, with human review gates at every step.

## 3. Why I Gave This Review Result

**Verdict: PASS_WITH_WARNINGS**

The task goal is met. The implementation is clean, conservative, and well-aligned with the task specification. No mocks, stubs, hardcoded outputs, or fake success paths exist. No existing functionality was broken (176 existing tests still pass). The documentation does not claim future work as completed.

However, I flagged several non-blocking warnings:

1. **Contract documentation has a false determinism claim (N01)**: The contract says `patch_id` is deterministic across repeated runs, but it's actually UUID-based. The handoff note and risk register correctly describe this, creating an inconsistency. This is a documentation error, not a code bug, but it could mislead future developers.

2. **Raw path in CLI stdout (N02)**: The `input_path` field appears unsanitized in stdout, consistent with a known project-wide pattern (R043) but still worth tracking.

3. **No committed automated tests (N03/R054)**: The worker performed thorough manual verification but didn't commit any test files. This follows the T160/T161 pattern and is acceptable for current scope, but regression coverage is missing.

4. **Missing edge-case guard for empty `contact_id` (N04)**: If a cluster report has a valid label but empty `contact_id`, the service would crash with an unhandled Pydantic validation error instead of skipping gracefully. This is likely unreachable via T161 output but lacks a defensive guard.

None of these are blocking because:
- The false claim is already contradicted by correct documentation elsewhere.
- The path exposure is known project-wide debt.
- The test gap is tracked and consistent with project precedent.
- The edge case is practically unreachable via normal T161 output.

The implementation is solid, conservative, and ready for T163 to build on top of.
