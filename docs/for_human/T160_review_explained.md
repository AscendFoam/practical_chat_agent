# T160 Review Explained

## 1. What is T160 trying to do?

T160 is about defining a **data structure** (a schema) for something called a "PreferencePatch" — a proposal to adjust how the chat agent communicates with a specific contact, based on repeated feedback from the human user.

To use an analogy: imagine you've been reviewing suggested reply drafts from an assistant, and you keep editing them to be shorter, or more casual, or to avoid certain topics. Over time, those edits accumulate into a pattern. A "PreferencePatch" is the system's way of packaging that pattern into a **reviewable proposal** that says: "Based on these feedback records, it seems like this contact prefers shorter replies. Should I adjust future drafts accordingly?"

The critical point is: T160 only defines the **shape** of that proposal. It does not generate proposals, approve them, apply them, or change any existing behavior. It's like designing a form before anyone fills it in.

## 2. What did the implementation change?

### 2.1 Code changes (`src/practical_chat_agent/core/models.py`)

Two things were added:

1. **`PreferencePatchType`** — a list of 8 allowed preference categories:
   - `tone_preference` (formal vs. casual vs. warm)
   - `length_preference` (short vs. medium vs. long)
   - `boundary_preference` (topics/patterns to avoid)
   - `topic_preference` (preferred or disliked subjects)
   - `question_style` (how to ask follow-up questions)
   - `humor_style` (whether humor is appropriate)
   - `repair_style` (how to recover from miscommunication)
   - `proactivity_preference` (initiate vs. wait)

2. **`PreferencePatchCandidate`** — a Pydantic model with 19 fields. The key design decisions:

   - **Evidence is mandatory**: `supporting_feedback_ids` must contain at least 1 feedback ID. You cannot create a patch with zero evidence — the Pydantic validator will reject it.
   - **Candidate-only by default**: new patches start with `status = "candidate"`, not `"approved"`. The `is_runtime_ready()` method returns `False` until a human has explicitly reviewed and approved the patch.
   - **Reuses existing review infrastructure**: the `review_metadata` field uses the same `DistilledArtifactReviewMetadata` type that was built in T120 and used throughout T121-T123. This means patches go through the same human-review-first lifecycle as memory facts and contact skills.
   - **No raw text**: no field stores raw chat transcripts, edited reply text, or private notes. The `positive_examples` and `negative_examples` fields are intended for safe summaries or references only.

### 2.2 New document (`docs/data_contracts/preference_patch_contract.md`)

This document defines the contract for the patch schema, including:
- The review-only lifecycle (feedback → cluster → candidate → human review → approved/rejected)
- Field semantics and constraints
- Safety constraints (evidence-backed, no raw text, candidate-only, no auto-mutation)
- Compatibility notes for future tasks T161-T164
- Explicit anti-patterns to avoid

### 2.3 Updated documents (`docs/07_handoff.md`, `docs/08_risks_and_open_questions.md`)

- Handoff: Added section 54 with the full T160 implementation record, including synthetic validation results and follow-up constraints.
- Risks: Added R047 (free-form string fields) and R048 (positive/negative examples safety), and closed question Q160.

### 2.4 Why this matters for the project

This is the **first M5 task**. M4 captured human feedback on reply drafts. M5 is about turning that feedback into actionable communication preferences — but only through a safe, reviewable pipeline.

The schema establishes a critical structural guardrail: patches cannot be auto-approved, cannot skip human review, and cannot exist without evidence. This means that even when future tasks add clustering (T161), proposal generation (T162), review CLI (T163), and compact context integration (T164), the data model itself enforces that patches stay candidate-only until a human says otherwise.

This is also architecturally important because it bridges M4 (feedback capture) and M6+ (ContactSkill decomposition, LLM planner, etc.) without requiring any of those downstream systems to exist yet. The patch schema is self-contained and compatible with the existing store/review pattern.

## 3. Why was the review verdict PASS_WITH_WARNINGS?

### What passed

- **Task completion**: The schema defines all fields specified in the task package: `patch_id`, `contact_id`, `patch_type`, `claim`, `behavior_instruction`, `supporting_feedback_ids` (with min_length=1), `positive_examples`, `negative_examples`, `affected_candidate_types`, `confidence`, `sensitivity`, `status`, timestamps, and review metadata.
- **Scope compliance**: Only allowed files were modified for T160 content. No clustering, proposal generation, review CLI, or runtime injection was implemented.
- **Evidence enforcement**: Empty `supporting_feedback_ids` is structurally rejected by Pydantic. This was verified.
- **Candidate-only guarantees**: Default status is `"candidate"`, `is_runtime_ready()` returns `False`, no auto-approve path exists.
- **No raw text**: No field stores raw transcript, edited text, or private notes.
- **Type reuse**: Correctly reuses `DistillationStatus`, `DistillationSensitivity`, and `DistilledArtifactReviewMetadata`.
- **No regressions**: All 176 existing tests pass.
- **Documentation**: The contract document is clear, honest, and does not claim future work as done. Anti-patterns are explicitly listed.

### What the warnings are about

The warnings are all **non-blocking** and follow the same pattern as previous tasks in this project:

1. **Free-form strings (N01, N02)**: `instruction_scope`, `affected_candidate_types`, `positive_examples`, and `negative_examples` are plain `list[str]` or `str` fields. They could theoretically be misused to store raw feedback text or inconsistent values. The contract document forbids this, but the model layer doesn't enforce it. This is acceptable for schema-only stage — T162 will be the enforcement point.

2. **No committed tests (N03)**: The worker verified the schema inline but did not add pytest tests. This is consistent with how T110-T142 were done (tests came later in T150-T152), but it means the PreferencePatchCandidate model doesn't yet have committed regression coverage. A future hardening pass should add this.

3. **Working tree hygiene (N05)**: Some files outside the allowed list have modifications in the working tree, but these are from prior Captain updates, not from T160 worker scope creep.

None of these warnings represent a real risk to the project. The schema is well-designed, safe, and compatible with the existing architecture.
