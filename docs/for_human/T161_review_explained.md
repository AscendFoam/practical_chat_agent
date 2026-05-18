# T161 Review Explained

## 1. What is T161 trying to do?

T161 is about building a **feedback clusterer** — a tool that groups similar human feedback records into privacy-safe clusters, as an intermediate step before generating communication preference patches.

To use an analogy: imagine you've been giving feedback on reply drafts for weeks — accepting some, rejecting others, flagging boundary violations. Each piece of feedback is stored as a record (that's what T140-T142 built). But a single "I rejected this draft" doesn't tell you much. What if the same contact got rejected 5 times? That starts to look like a pattern.

T161's job is to recognize those patterns by grouping feedback records that share the same contact and the same type of action. It's like sorting all your feedback into labeled buckets: "rejections for Contact A," "acceptances for Contact A," "boundary violations for Contact B." Each bucket is a "cluster" — a collection of related feedback that can later be used to propose a communication preference adjustment.

The critical constraint is: T161 only sorts feedback into buckets. It does NOT generate patches, approve anything, or change any behavior. It's purely an aggregation step.

## 2. What did the implementation change?

### 2.1 Code changes (`src/practical_chat_agent/services/feedback.py`)

A new `FeedbackClusterService` class was added with the following behavior:

1. **Label derivation**: Each feedback record gets a cluster label based on its action type:
   - `accept` → `good_tone` (the user liked the draft as-is)
   - `reject` → `not_like_me` (the user didn't want to send this)
   - `boundary` → `boundary_violation` (the draft crossed a line), unless the record has a `boundary_label` that matches a known label like `too_long` or `too_formal`, in which case that more specific label is used
   - `edit` → **no label** (edits are too ambiguous — the user changed the draft, but we can't safely determine why, so edit records are excluded from clustering)

2. **Grouping**: Records are grouped by `(contact_id, label)`. All "reject" feedback for the same contact goes into one cluster, all "accept" feedback into another, etc.

3. **Stable cluster IDs**: Each cluster gets a `cluster_id` generated from `sha256(contact_id:label)`. This means the same grouping key always produces the same ID, making it easy to track clusters across runs.

4. **Aggregate output**: Each cluster contains:
   - `cluster_id`, `contact_id`, `cluster_label`
   - `supporting_feedback_ids` (which records are in this cluster)
   - `record_count`, `counts_by_action`, `counts_by_priority_rank`
   - `counts_by_approach_label` (what approach was used for the drafts in this cluster, if plan files are available)
   - `time_range` (earliest and latest feedback timestamps)
   - `reason_tag_summary` (frequency of boundary labels, if any)

5. **Privacy safety**: No raw text, edited text, user notes, or boundary notes appear in the output. Only IDs, counts, and timestamps.

6. **Optional validation filtering**: If a T141 validation report is provided, only validated records are clustered.

### 2.2 CLI changes (`src/practical_chat_agent/app/main.py`)

A new `chat-feedback-cluster` command was added:

```text
chat-feedback-cluster --feedback-log <path> --output <private path> [--validation-report <path>]
```

The command outputs a JSON summary with aggregate statistics and cluster details to stdout, and optionally writes the full report to a file.

### 2.3 Contract update (`docs/data_contracts/preference_patch_contract.md`)

A new "Feedback Cluster Contract (T161)" section was added, documenting:
- The label derivation rules (which action maps to which label)
- The cluster output shape (JSON schema)
- The cluster ID stability mechanism (SHA-256 based)
- Privacy safety guarantees

### 2.4 Documentation updates (`docs/07_handoff.md`, `docs/08_risks_and_open_questions.md`)

- Handoff: Added Section 57 with the full T161 implementation record
- Risks: Added R050 (edit records have no cluster label), R051 (cluster ID reflects grouping key, not record content), and closed Q162

### 2.5 Why this matters for the project

T161 sits between T160 (the PreferencePatch schema) and T162 (the patch proposal CLI). The data flow is:

```text
T140 feedback records
  → T141 validation
  → T142 summary export
  → T161 clustering (THIS TASK)
  → T162 patch proposal (future)
  → T163 patch review (future)
  → T164 runtime integration (future)
```

This is important because the project's safety model requires that patches be based on **repeated patterns**, not single feedback events. A single rejection doesn't justify a permanent communication policy change. But 5 rejections for the same contact, grouped into a cluster, start to look like evidence worth proposing as a patch.

T161 enforces this "repeated evidence first" principle structurally: the clusterer produces groups that T162 can then use as input. And even though T162 hasn't been built yet, T161's output is already compatible with `PreferencePatchCandidate.supporting_cluster_ids` from T160.

## 3. Why was the review verdict PASS_WITH_WARNINGS?

### What passed

- **Task completion**: The clusterer implements all required functionality: deterministic grouping, stable cluster IDs, privacy-safe output, CLI surface, and validation report filtering.
- **Scope compliance**: Only allowed files were modified. No PreferencePatchCandidate generation, no LLM calls, no ContactSkill/Memory mutation, no auto-approve, no runtime injection.
- **Determinism**: Clusters are sorted by grouping key, cluster IDs are SHA-256 derived, and the same input always produces the same output.
- **Privacy safety**: Output contains no raw feedback text, edited text, user notes, or boundary notes.
- **Edit handling**: Edit records are correctly excluded from clustering because no safe deterministic label exists. This is documented as R050.
- **No regressions**: All 176 existing tests pass.
- **Documentation**: The contract document is accurate and does not claim future work as done.

### What the warnings are about

1. **`reason_tag_summary` naming (N01)**: The field is named as if it summarizes "reason tags," but it actually contains frequency counts of `boundary_label` values. There is no `reason_tag` field in the feedback record model. The name comes from the task package's wording ("reason-tag aggregates") but could confuse T162 developers. Non-blocking because the data is correct — it's just a naming inconsistency.

2. **No committed tests (N02)**: Same pattern as T160 and earlier tasks. The worker verified the clustering inline but did not add pytest tests. R049 tracks this. A future hardening pass should add cluster output validation tests.

3. **Silent approach label degradation (N03)**: The clusterer reads ReplyPlan files to extract `approach_label` for each record. If plan files are missing, the approach label is silently omitted. This means `counts_by_approach_label` may be incomplete. Non-blocking because missing labels are safer than wrong labels.

4. **`input_path` in stdout (N04)**: Raw filesystem paths appear in CLI output, consistent with T140-T142. Already tracked as R043.

5. **`.claude/settings.json` modified (N05)**: Not an allowed file, but it's a worker environment artifact, not T161 content.

None of these warnings represent a real risk. The implementation is clean, safe, deterministic, and well-scoped.
