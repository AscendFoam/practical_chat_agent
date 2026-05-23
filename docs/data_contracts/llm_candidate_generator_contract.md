# LLM Candidate Generator Contract

Updated: 2026-05-23

## Purpose

This document defines the input/output contract for an **optional LLM-assisted reply candidate generator** that may be implemented later (T181+). It does not call an LLM, does not replace the existing deterministic `ReplyPlanner`, and does not change any runtime behavior.

The contract is purely additive: it defines what a future LLM-based generator must produce to be compatible with the existing `ReplyPlan` (T130), `ChatContext` (T123/T164/T174), and review-only policy layer (T132).

## Scope

This contract covers only the **generator interface** — the shape of inputs it may consume and the shape of outputs it must produce.

What is **not** in scope:
- LLM implementation, provider selection, prompt engineering
- Hybrid planner logic (combining deterministic + LLM candidates)
- Changes to the existing `ReplyPlanner`, `ReplyPlanPolicyEngine`, or `ChatContextAssembler`
- Auto-approval, auto-send, runtime injection, or platform integration
- Storing, caching, or persisting LLM outputs beyond the generator call

## 1. Usage Boundary

Any LLM-based candidate generator must respect the following boundaries:

1. **Review-only input**: Generated candidates are review inputs only. They must never bypass policy review, boundary checks, or human approval.
2. **No impersonation**: The generator must never produce text that impersonates the contact, simulates the contact's voice, or claims to speak as the contact.
3. **Evidence-grounded**: Every candidate must reference supporting context refs from approved stores, recent events, or policy/boundary definitions. Unsupported speculation is forbidden.
4. **Conservative default**: When context is uncertain, sensitive, or thin, the generator must produce conservative candidates rather than guessing relationship details.
5. **Attributable**: Every candidate must be traceable to its generator type (e.g., `"llm_generated"`) and the specific context snapshot used.
6. **Rejectable**: The output must be structurally validatable so that invalid, unsafe, or ungrounded candidates can be rejected before any review or display.

## 2. Generator Type

The generator uses a literal type to identify which generator produced the output:

```python
LLMGeneratorType = Literal[
    "template_deterministic",   # existing T131/T132 ReplyPlanner
    "llm_generated",            # LLM-assisted generator (future T181+)
]
```

Each candidate in the output carries a `generator_type` field so downstream consumers can distinguish LLM-generated candidates from deterministic ones without inspecting content.

## 3. Input Contract

A future LLM generator may consume a bounded, privacy-safe subset of `ChatContext`. It must NOT access raw chat transcripts, full store JSON dumps, or any content outside the approved compact context boundary.

### 3.1 Permitted Input Fields

| Field | Source | Required | Notes |
|-------|--------|----------|-------|
| `contact_id` | Runtime routing | Yes | Contact identifier context is being planned for |
| `recent_event_texts` | Recent context window | No | Limited to last N messages, privacy-redacted or summarized |
| `approved_contact_skill_brief` | T123 ApprovedStoreContext | No | Compact relationship summary only |
| `approved_memory_briefs` | T123 ApprovedStoreContext | No | Compact memory fact summaries only |
| `derived_brief_context` | T174 DerivedBriefContext | No | Persona, policy, and boundary briefs |
| `approved_patch_hints` | T164 ApprovedPatchContext | No | Compact behavior instruction hints |
| `policy_boundary_summary` | T132 ReplyPlanPolicyEngine | No | Current policy risk summary |
| `approved_store_evidence_refs` | T123/T164/T174 context | No | Evidence reference ids for traceability |

### 3.2 Prohibited Input

The generator must NOT receive:
- Raw normalized event text or chat transcripts
- Full `ContactSkillStoreRecord` or `MemoryFactStoreFile` JSON dumps
- Candidate, rejected, frozen, or archived store records
- Raw feedback text, edited text, user notes, or boundary notes
- Any content from `private/chat_history/` or `private/distilled/` beyond the compact briefs

Input assembly must use the existing compact-context boundaries from T123, T164, and T174. No new input-assembly path is authorized.

## 4. Output Contract

The generator must produce output compatible with the T130 `ReplyPlan` schema. A dedicated `LLMReplyPlan` wrapper is defined to carry the generator identity alongside the plan.

### 4.1 Top-Level Shape

```json
{
  "schema_version": "llm_reply_plan_v1",
  "generator_type": "llm_generated",
  "generator_id": "llm_gen_abc123",
  "contact_id": "contact_xxx",
  "source_context_snapshot": {
    "approved_store_status": "loaded",
    "approved_contact_skill_record_id": "skillstore_001",
    "approved_memory_record_ids": ["memstore_001"],
    "recent_event_count": 3,
    "policy_boundary_summary": ["Drafts are for human review only."]
  },
  "generation_metadata": {
    "provider": "openai|anthropic|local|unknown",
    "model": "gpt-4o|claude-sonnet-4-6|...",
    "temperature": 0.7,
    "prompt_template_hash": "sha256_prefix_16",
    "generated_at": "2026-05-23T12:00:00+08:00",
    "latency_ms": 2340
  },
  "candidates": [
    {
      "candidate_id": "llmcand_001",
      "generator_type": "llm_generated",
      "approach_label": "conservative_acknowledgment",
      "priority_rank": 1,
      "draft_text": "收到，我先跟上你这个点。",
      "rationale": "Uses the approved persona brief and policy boundary to keep the tone light and non-pushy.",
      "supporting_context_refs": [
        {
          "ref_type": "approved_contact_skill_record",
          "ref_id": "skillstore_001",
          "note": "relationship summary and boundary reminders"
        }
      ],
      "risk_flags": [],
      "boundary_reminders": [
        "Do not sound overly intimate.",
        "Do not assume unverified emotional state."
      ],
      "confidence": 0.78
    }
  ],
  "refusal": null
}
```

### 4.2 `LLMReplyPlanCandidate` Fields

Each candidate extends the T130 `ReplyPlanCandidate` contract with one additional required field:

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| `candidate_id` | Yes | `str` | Stable unique id within this plan |
| `generator_type` | Yes | `LLMGeneratorType` | Must be `"llm_generated"` for LLM output |
| `approach_label` | Yes | `str` | Strategy label for review |
| `priority_rank` | Yes | `int` | 1-based ranking, unique within plan |
| `draft_text` | Yes | `str` | Candidate reply draft |
| `rationale` | Yes | `str` | Why this draft is suggested |
| `supporting_context_refs` | Yes | `list[...]` | At least 1 ref; must reference approved context only |
| `risk_flags` | No | `list[str]` | Optional risk flags |
| `boundary_reminders` | Yes | `list[str]` | At least 1 reminder |
| `confidence` | No | `float` | 0-1辅助信号，不代表确定性 |

### 4.3 Refusal Shape

When the LLM generator cannot produce valid candidates (e.g., input violates safety constraints, required context is missing, or provider returns an error), it must return a structured refusal rather than silently degrading:

```json
{
  "schema_version": "llm_reply_plan_v1",
  "generator_type": "llm_generated",
  "generator_id": "llm_gen_def456",
  "contact_id": null,
  "source_context_snapshot": {},
  "generation_metadata": {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.7,
    "prompt_template_hash": null,
    "generated_at": "2026-05-23T12:00:00+08:00",
    "latency_ms": 500
  },
  "candidates": [],
  "refusal": {
    "refusal_code": "PROVIDER_ERROR|INPUT_TOO_LARGE|MISSING_REQUIRED_CONTEXT|SAFETY_FILTER|INVALID_OUTPUT_SCHEMA",
    "refusal_reason": "Human-readable explanation of why generation was skipped or failed.",
    "is_retryable": true
  }
}
```

Refusal codes:

| Code | Meaning | Retryable |
|------|---------|-----------|
| `PROVIDER_ERROR` | Provider returned an error or timed out | Yes |
| `INPUT_TOO_LARGE` | Context exceeds provider token limits | No (must compact input) |
| `MISSING_REQUIRED_CONTEXT` | `contact_id` or other required input absent | No (fix caller) |
| `SAFETY_FILTER` | Input triggered a safety/content filter | No |
| `INVALID_OUTPUT_SCHEMA` | Provider response failed structural validation | Yes (may degrade) |

The refusal must be structured (not a thrown exception) so callers can distinguish "generator actively refused" from "generator crashed."

## 5. Validation Boundary

A critical design constraint is the **deterministic validation boundary** between "candidate generation" (which may use an LLM) and "candidate acceptance" (which must be deterministic).

### 5.1 Generation Side (May Use LLM)

The generator call may involve non-deterministic LLM inference. This side:
- Accepts compact, privacy-safe context input
- Produces `LLMReplyPlan` with 0-3+ candidates or a refusal
- May fail, timeout, or refuse
- Must NOT persist its output or modify any runtime state

### 5.2 Acceptance Side (Must Be Deterministic)

Before any candidate enters review or display, a deterministic validator must check:

1. **Schema compliance**: Output validates against `LLMReplyPlan` Pydantic model
2. **Ref count**: Each candidate has at least 1 `supporting_context_ref` and 1 `boundary_reminder`
3. **Ref scope**: All refs reference approved-store ids, evidence refs, recent event ids, memory hit ids, or policy-boundary ids only. Non-approved ids (candidate/rejected/frozen/archived) must be rejected.
4. **Rank uniqueness**: `priority_rank` values are unique and form a stable `1..N` sequence
5. **Generator type**: `generator_type` is `"llm_generated"` for all LLM candidates
6. **No raw content**: Draft text does not echo raw input context verbatim (privacy leakage check)
7. **No impersonation**: Draft text does not contain first-person contact impersonation patterns

Any candidate failing deterministic validation must be excluded silently. The caller receives only the validated subset.

### 5.3 Disallowed Bypasses

The following are explicitly disallowed:
- Skipping deterministic validation before displaying candidates
- Allowing candidates with non-approved refs to reach review
- Allowing structural schema violations to be silently normalized
- Falling back to LLM output when deterministic validation fails (must fall back to empty/refusal instead)
- Merging LLM candidates with existing deterministic `ReplyPlan` before policy review

## 6. Privacy and No-Impersonation Rules

### 6.1 Privacy

- The generator input must use the same compact-context boundaries as T123/T164/T174
- Raw normalized events, full store JSON dumps, and `private/chat_history/` content are prohibited inputs
- Draft text must not echo input context verbatim; this is checked by the deterministic validator
- The generator itself should be instructed (via prompt/system message) not to reproduce input text

### 6.2 No-Impersonation

The generator must be instructed — both in this contract and in any future prompt template — that impersonation is forbidden:

1. **No first-person contact voice**: The generator must never produce draft text that sounds like "I (the contact) would say..."
2. **No contact simulation**: The generator must not be asked to "think like the contact" or "respond as the contact"
3. **No relationship speculation**: The generator must not claim knowledge beyond what is present in approved context refs
4. **Attribution boundary**: Any generated candidate is attributed to the LLM generator (via `generator_type`), not to the contact or to the user

These rules must be encoded in:
- The generator prompt template (as instructions)
- The deterministic validator (as structural checks)
- The review UI/CLI (as visible labels)

## 7. Schema Validation Expectations

A future T182 validator (or equivalent) must implement:

1. **Structural validation**: `LLMReplyPlan` and each `LLMReplyPlanCandidate` conform to Pydantic models
2. **Ref validation**: All refs reference known approved-store scopes and no non-approved ids leak in
3. **Rank coherence**: Priority ranks are unique, 1-based, contiguous
4. **Boundary compliance**: Each candidate has ≥1 boundary reminder; the plan itself carries `policy_boundary_summary`
5. **Refusal coherence**: A refusal must have either 0 candidates or a refusal with explicit code/reason; never both
6. **Generator type consistency**: All candidates in an LLM-generated plan have `generator_type="llm_generated"`
7. **Privacy leakage**: Draft text does not reproduce input context verbatim (exact substring match against prohibited input sources)
8. **Impersonation detection**: Draft text does not contain first-person contact impersonation patterns

Failed validations must be reported per-candidate so valid candidates are not discarded due to an invalid sibling.

## 8. Future Task Constraints (T181+)

### 8.1 What T181 May Implement

- An offline CLI that consumes a `ChatContext` JSON and produces an `LLMReplyPlan`
- A generator service that calls an LLM provider through an OpenAI-compatible adapter
- Deterministic validation of LLM output before writing or displaying results
- Input assembly using existing compact-context boundaries (no new input paths)
- Structured refusal handling for provider errors, safety filters, and schema failures

### 8.2 What Remains Forbidden After T180

- Hybrid `ReplyPlanner` that merges deterministic and LLM candidates (T183)
- Auto-approval or auto-injection of LLM candidates into any runtime path
- Changes to the existing deterministic `ReplyPlanner` or `ReplyPlanPolicyEngine`
- Storing or caching LLM outputs beyond the generator's output file
- Supplying raw chat transcript, full store JSON, or non-compact context as input
- Bypassing policy/boundary review or human approval for any LLM-generated candidate
- Any claim that LLM candidates are enabled, production-ready, or quality-proven

## 9. Relationship to Existing Contracts

| Contract | Relationship |
|----------|-------------|
| T130 `ReplyPlan` | LLM output wraps `ReplyPlanCandidate`-compatible candidates; extends with `generator_type` and `refusal` |
| T123 `ApprovedStoreContext` | LLM input uses the same compact approved-store boundaries |
| T164 `ApprovedPatchContext` | LLM input may optionally include compact patch hints |
| T174 `DerivedBriefContext` | LLM input may optionally include derived briefs (persona, policy, boundary) |
| T132 `ReplyPlanPolicyEngine` | LLM candidates remain subject to the same policy review; must not bypass |
| T140 `ReplyFeedbackRecord` | LLM candidates are reviewable through the same feedback flow |

## 10. Non-Goals

This contract explicitly does not:

- Call any LLM
- Change the existing `ReplyPlanner`, `ChatContextAssembler`, or `ReplyPlanPolicyEngine`
- Add sending, platform integration, DB, vector DB, or UI
- Modify policy-engine rules, approved-store semantics, or context-assembly behavior
- Claim that LLM candidates are enabled, production-ready, or quality-proven
