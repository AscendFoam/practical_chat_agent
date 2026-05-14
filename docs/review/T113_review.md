# T113 Review: ContactSkill Builder

## Reviewer

Claude Code (adversarial review)

## Verdict

**PASS_WITH_WARNINGS**

## Scope Check

Worker modified exactly the 4 allowed files:

- `src/practical_chat_agent/services/contact_skill.py` (rewritten)
- `src/practical_chat_agent/exporters/contact_skill_markdown.py` (new)
- `src/practical_chat_agent/app/main.py` (CLI addition only)
- `docs/07_handoff.md` (status update only)

No other tracked files were modified. The new `exporters/` directory is untracked and within allowed scope. Upstream services (`chatlog_ingestion.py`, `conversation_chunking.py`, `chatlog_distillation.py`) are untouched.

## What was done

1. `ContactSkillBuilderService` consumes only T112's `chunk_summaries.jsonl` and `memory_facts.jsonl`, validates via Pydantic `model_validate`, and produces a `ContactSkillCandidate`.
2. Candidate always has `status="candidate"`, enforced by `_assert_candidate()`.
3. Candidate always has `evidence_refs`, enforced by `_assert_candidate()`.
4. Markdown review exporter renders all sections with evidence refs, usage boundary, and anti-impersonation reminder.
5. CLI `chatlog-build-contact-skill` supports `--input`, `--output`, `--contact-id`, `--dry-run`.
6. Output restricted to `private/distilled/` via `_ensure_within_root`.
7. Redaction in both `redact_review_text()` and `_safe_text()` masks emails, phones, URLs, long numbers, and names; text is truncated at 120 chars.

## Positives

- **No auto-approve**: `status="candidate"` is hardcoded and asserted.
- **Evidence chain preserved**: `evidence_refs`, `source_chunk_ids`, `source_memory_ids` all populated from upstream T112 outputs.
- **No LLM call**: builder is heuristic-only; no prompt leakage risk.
- **No raw chat text**: markdown exporter shows only `summary`/`claim` fields, redacted and truncated.
- **No impersonation content**: all generated text is about the contact (observations, strategies), never pretending to be the contact speaking.
- **Input validation**: JSONL parsing, Pydantic schema validation, path confinement.
- **Anti-impersonation guardrails explicit**: `usage_boundary.disallowed_uses` defaults include `persona_clone`, `impersonation`, `autonomous_contact_simulation`. Review notes and markdown both contain explicit anti-impersonation reminders.

## Blocking Issues

None.

## Non-blocking Issues

### N01: `_build_report` called twice in non-dry-run path

**Severity**: Low  
**Location**: `contact_skill.py` lines 112-120 vs 122-132  
**Detail**: When `dry_run=False`, `_build_report()` is invoked once to write `run_report.json` and once to return in the result dataclass. The two calls produce identical output, so no correctness issue, but it is unnecessary work.

**Recommendation**: Build the report once, use it for both write and return.

### N02: Heuristic tokens hardcoded to current small sample

**Severity**: Low  
**Location**: `_CONCERN_TOKENS`, `_PRACTICAL_SUPPORT_TOKENS`, `_extract_topic()`  
**Detail**: The token lists (`"worry"`, `"concern"`, `"tutoring"`, `"review the materials first"`, etc.) and topic mapping (`"target school" -> "school plans"`, etc.) are clearly tailored to the exam-preparation sample. For a different contact (family, colleague), many of these heuristics will produce empty or misleading results. `_infer_relationship_type()` falls through to `"friend"` whenever any data exists, which is not wrong but is uninformative.

**Recommendation**: Acceptable for MVP. T114 should test with a different contact to expose gaps. T120+ should consider whether LLM-assisted inference replaces these heuristics or supplements them.

### N03: Confidence formula is formulaic, not evidence-weighted

**Severity**: Low  
**Location**: `_build_relationship_state()` closeness/trust formulas, `_build_candidate()` confidence averaging  
**Detail**: `closeness = 0.22 + min(len(contact_facts), 6) * 0.08` is a fixed ramp based on fact count, not evidence quality. Similarly, `initiative_balance` is inferred from fact count by `subject_id`, not from actual message direction data. These will not generalize.

**Recommendation**: Acceptable for candidate-only status. Reviewer and T114 should verify the numbers don't look spuriously precise. T120+ should revisit.

### N04: `__init__.py` missing from `exporters/` directory

**Severity**: Negligible  
**Location**: `src/practical_chat_agent/exporters/`  
**Detail**: The directory has no `__init__.py`. Python 3 implicit namespace packages handle this, and the import uses a deferred `from ... import` inside a function body, so it works. But it deviates from the convention used in other `src/practical_chat_agent/` sub-packages.

**Recommendation**: Add a minimal `__init__.py` for consistency, but not blocking.

### N05: `collect_reference_fact_ids` defined but unused

**Severity**: Negligible  
**Location**: `contact_skill.py` lines 935-944  
**Detail**: `collect_reference_fact_ids()` is a standalone helper that is never called within the module or imported elsewhere.

**Recommendation**: Remove or use in T114+.

## Forbidden Scope Check

| Forbidden action | Status |
|---|---|
| Auto-approve | NOT present. `status="candidate"` enforced. |
| Save raw chat text | NOT present. Only summaries/claims used. |
| Generate "contact speaking" content | NOT present. All text is observational. |
| DB migration | NOT present. |
| Realtime platform | NOT present. |
| Auto-send | NOT present. |

## Verification

- Compile: passed (all 3 files).
- Import: passed with conda env.
- CLI registration: `chatlog-build-contact-skill` visible in app.
- No modifications to upstream services.
- No private data in stdout or docs.

## Warnings Classification

| ID | Classification | Rationale |
|---|---|---|
| N01 | Accepted | Cosmetic duplication, no functional impact. |
| N02 | Accepted/Deferred | Known heuristic limitation; T114 to expose; T120+ to revisit. |
| N03 | Accepted/Deferred | Formulaic but conservative; candidate-only status limits blast radius. |
| N04 | Accepted | No functional impact; convention-only. |
| N05 | Accepted | Dead code, no harm. |

## Recommended Next Action

Proceed to T114. During T114 sample run, pay attention to:
1. Whether the small-sample heuristics produce reasonable results on a larger or different contact.
2. Whether confidence numbers look spuriously precise.
3. Whether `_extract_topic` returns `None` for most facts (indicating the mapping is too narrow).
