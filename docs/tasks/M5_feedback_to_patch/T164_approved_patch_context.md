# Task T164: Approved Patch Compact Context

## Task ID

T164

## Goal

Inject only approved, runtime-ready preference patches into `ChatContext` as compact communication hints.

## Why Now

T163 now provides explicit human review state for patch proposals. The next smallest safe M5 step is to let only approved, runtime-ready patches influence reply planning through a compact context layer rather than through raw proposal JSON or direct runtime prompt injection.

T164 must therefore stay strictly in the compact-context layer:

- it may read approved patch records only
- it may expose short, planner-usable communication hints only
- it may not bypass existing review gates or surface raw feedback/proposal internals

## Inputs To Read

- `docs/review/T160_review.md`
- `docs/review/T161_review.md`
- `docs/review/T162_review.md`
- `docs/review/T163_review.md`
- `docs/04_task_board.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`
- `docs/data_contracts/preference_patch_contract.md`
- existing context integration patterns in:
  - `src/practical_chat_agent/core/models.py`
  - `src/practical_chat_agent/services/chat_context.py`
  - `src/practical_chat_agent/services/feedback.py`

## Allowed Files

- `src/practical_chat_agent/core/models.py`
- `src/practical_chat_agent/services/chat_context.py`
- `src/practical_chat_agent/services/feedback.py`
- `docs/data_contracts/preference_patch_contract.md`
- `docs/07_handoff.md`
- `docs/08_risks_and_open_questions.md`

## Forbidden Scope

- Do not inject candidate/rejected/frozen/archived patches.
- Do not inject approved patches unless `is_runtime_ready() == True`.
- Do not inject full feedback notes, edited text, or raw draft text.
- Do not inject raw `claim` or `behavior_instruction` as unconstrained prompt text without a compact context structure.
- Do not mutate ContactSkill/MemoryFact/store records.
- Do not change patch review status or review history.
- Do not call an LLM.
- Do not send messages or integrate platforms.
- Do not read private chat history.

## Expected Output

Add compact approved-patch context integration that consumes reviewed patch reports and exposes only safe, compressed patch hints to the existing `ChatContext` layer.

Suggested output shape:

- a compact patch brief list or equivalent `ChatContext` field containing only approved/runtime-ready patch summaries
- each brief should preserve stable identifiers and enough traceability for audit, for example:
  - `patch_id`
  - `patch_type`
  - compact instruction or hint
  - sensitivity
  - supporting ids or counts in compact form

The integration must be conservative:

- include only patches where `status == "approved"` and `is_runtime_ready() == True`
- exclude candidate/rejected/frozen/archived patches even if other fields look usable
- keep review history present in the source record but do not expand it into runtime context
- avoid copying raw proposal internals if a shorter compact brief can represent the same guidance
- preserve privacy safety: no raw feedback text, edited text, draft text, user notes, or boundary notes in context

If the worker touches the patch contract or context models, the resulting doc/model language must stay aligned with the actual approval gate and must not imply that non-approved patches can influence runtime behavior.

## Verification

- Approved + runtime-ready patch enters context as a compact brief.
- Candidate/rejected/frozen/archived patch is excluded.
- Approved but not runtime-ready patch is excluded.
- Review history remains in stored patch data but is not expanded into context text.
- Full feedback text does not enter context.
- Existing non-patch context assembly behavior does not regress.

## Expected Handoff Update

Append a T164 implementation record to `docs/07_handoff.md` with:

- files changed
- context field or brief shape added
- approved/runtime-ready filtering rules used
- one synthetic context example
- any remaining follow-up constraints for later M5+ tasks

## Reviewer Type

adversarial

## Reviewer Focus

Reviewer should verify:

- only approved/runtime-ready patches enter context
- context output is compact and privacy-safe
- review history and source evidence are preserved but not dumped into runtime text
- no patch review/apply/send behavior is smuggled into the context layer
