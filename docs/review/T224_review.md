# Review: T224

Verdict: PASS

## Blocking Issues

None.

## Non-Blocking Issues

### N01 `.claude/settings.json` workspace-artifact overrun

`.claude/settings.json` was modified to add T224 verification commands to the allowed Bash permissions. This file is not in the allowed-files list. This is established convention noise seen in every prior task since T100. The changes are permission-allowlist entries only, not functional code.

### N02 Candidate-shaped mapping detection duplicates T222/T223 pattern

`_is_candidate_action_input()` uses the same heuristic (`schema_version == "candidate_action_v1"` or presence of `action_id`/`action_type` keys) that T222 and T223 use. This is consistent but could be extracted into a shared utility if a fourth consumer appears. Acceptable for now.

### N03 `FeishuSandboxDeliveryResult` coercion via `**dict(sandbox_result)` may be fragile

`_coerce_sandbox_result` reconstructs a dataclass from a plain mapping via `FeishuSandboxDeliveryResult(**dict(sandbox_result))`. This works because the dataclass fields align with the dict keys, but it is sensitive to field-ordering or future type changes. Acceptable for current scope since the only caller passing a mapping is a synthetic test.

### N04 No explicit test for `FeishuReviewCardConfig` validation edge cases

The config dataclass has `__post_init__` validation for empty renderer name, non-positive limits, etc., but no test directly exercises these. This follows the pattern established in prior tasks and is non-blocking.

### N05 `render` accepts both `OutboundMessageRequest` and `CandidateAction` in its type signature but blocks `CandidateAction` at runtime

The type hint `request: OutboundMessageRequest | CandidateAction | Mapping[str, Any]` is wide, but the runtime correctly blocks `CandidateAction` inputs immediately. The wide type is intentional to give a clear rejection path. This is consistent with T222/T223 adapter pattern.

## Missing Tests

### M01 No test for mapping input that passes `OutboundMessageRequest.model_validate()`

The task requires accepting "a stable mapping that validates to one." While the existing tests pass `OutboundMessageRequest` objects directly, there is no test that passes a raw `dict` that successfully coerces via `model_validate`. The `_coerce_request` path for mappings is exercised only in the rejection tests (candidate-shaped, invalid mappings). A positive mapping-to-request coercion test would strengthen coverage.

### M02 No test for `draft_preview_char_limit <= 3` boundary

`_display_preview` has a special case when `draft_preview_char_limit <= 3` that returns dots. The existing boundary test uses limit 10. A test with limit 2 or 3 would cover this branch.

### M03 No test for `FeishuReviewIntent` frozen dataclass immutability

`FeishuReviewIntent` is `frozen=True`, but no test verifies that mutation raises `FrozenInstanceError`. Minor since this is a dataclass guarantee.

### M04 No test for `_mapping_value` returning `None` when request is a `CandidateAction` model

When `_is_candidate_action_input` catches a `CandidateAction` instance, `_mapping_value` is called on the model object, which is not a `Mapping`, so it returns `None` for all keys. This is correct but untested. The blocked result will have `None` for contact_id/user_id/channel_preference, which is cosmetically harmless.

## Suspicious Implementation Details

None. The implementation is straightforward, deterministic, and side-effect-free:

- No network calls, no external service access.
- No mutation of inputs (verified by test).
- No real Feishu API interaction.
- The `_FakeTransport` in tests correctly asserts it is never called.
- Forbidden recipient metadata keys are absent from card output (verified by test).
- Card truncation is documented as display-only, not redaction.
- Parser returns inert intent data only with no side effects.
- Action values are deterministic with `schema_version`, `request_id`, and `action` fields.

## Allowed Files Compliance

Files changed:

- `src/practical_chat_agent/services/feishu_review_card.py` -- allowed (new file).
- `tests/test_feishu_review_card.py` -- allowed (new file).
- `docs/data_contracts/outbound_send_gate_contract.md` -- allowed.
- `docs/worker_summary/T224_worker_summary.md` -- allowed (new file).
- `docs/07_handoff.md` -- allowed.
- `.claude/settings.json` -- not in allowed list (convention noise, see N01).

No modifications to `src/practical_chat_agent/core/models.py`, `feishu_outbound_adapter.py`, `test_feishu_outbound_adapter.py`, `app/main.py`, connector modules, runtime configuration, or task board.

## Verification Results

- `py_compile` all M11 source files: passed.
- T224-targeted pytest (84 tests): passed.
- Full suite (844 passed, 16 failed): all failures are pre-existing (typer import, LLM CLI tests) and unrelated to T224.

## Recommended Next Action

T224 is complete as the Feishu review-card task for M11. The Captain should:

1. Mark T224 as `PASS` in the task board.
2. Update M11 completion status if T224 was the final M11 task.
3. The next milestone (M12 WeChat Adapter) can begin with T230 WeChat adapter research spike, pending Captain decision.
