# T290 Worker Summary

## Changed

- Added `RoleDynamicPost` to `src/practical_chat_agent/core/models.py`.
- Added `tests/test_role_dynamic_post_schema.py`.
- Added `docs/data_contracts/role_dynamic_post_contract.md`.
- Added
  `docs/tasks/M18_virtual_life_stream/T291_virtual_life_engine_text_generator.md`.
- Appended the T290 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## TDD Evidence

- RED: `pytest tests\test_role_dynamic_post_schema.py -q` failed during
  collection because `RoleDynamicPost` did not exist in
  `practical_chat_agent.core.models`.
- GREEN: after adding `RoleDynamicPost`, the targeted T290 tests passed.

## Behavior Added

- `RoleDynamicPost` stores review-only virtual life stream draft text.
- Content status is fixed to `imagined_ai_generated`.
- Truth disclosure is fixed to `imagined_ai_generated_content`.
- Review status defaults to `requires_review`.
- Visibility is fixed to `local_private_review`.
- Empty content is rejected.
- Factual claims require review notes and remain imagined content.
- Serialized posts contain no publish, send, schedule, delivery, platform,
  webhook, token, or queue fields.

## Explicit Non-Actions

- No post generator, LLM call, scheduler, publisher, outbound request, delivery
  adapter, platform integration, push notification, webhook, queue, review UI,
  voice/avatar/video behavior, Live2D, social feed publishing, web demo, or
  automatic sending was added.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- No real-person clone, public-figure clone, deceased-person mode, or deceptive
  impersonation path was authorized.
- T290 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
$env:PYTHONPATH='src'
pytest tests\test_role_dynamic_post_schema.py -q -o cache_dir=artifacts\t290_pytest_cache --basetemp=artifacts\t290_pytest_basetemp
```

Result: passed, `5 passed`.

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_role_dynamic_post_schema.py tests\test_proactive_consent_schema.py -q -o cache_dir=artifacts\t290_pytest_cache_min --basetemp=artifacts\t290_pytest_basetemp_min
```

Result: passed, `12 passed`.

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Remaining Risks

- T290 is schema-only.
- Deterministic text generation, AIGC metadata hardening, contamination tests,
  review cards, UI, and web demo remain unopened.

## Recommended Reviewer Type

Adversarial review.
