# T293 Worker Summary

## Changed

- Added `tests/test_virtual_life_contamination.py`.
- Updated `src/practical_chat_agent/core/models.py`.
- Updated `docs/data_contracts/role_dynamic_post_contract.md`.
- Updated `docs/data_contracts/virtual_life_engine_contract.md`.
- Added `docs/tasks/M18_virtual_life_stream/T294_dynamic_review_card.md`.
- Appended the T293 handoff record to `docs/07_handoff.md`.
- Wrote this worker summary.

## TDD Evidence

- RED: `pytest tests\test_virtual_life_contamination.py -q` failed because
  factual memory could use `imagined_generation` provenance and
  `RoleDynamicPost` did not expose `memory_ref_usage`.
- GREEN: after adding the contamination guard and `memory_ref_usage`, the
  targeted T293 tests passed.

## Behavior Added

- Factual `MemoryEvent` records cannot use `imagined_generation` provenance.
- `RoleDynamicPost.memory_ref_usage` is fixed to `inspiration_only`.
- Engine-created posts retain imagined labels and not-real-world-activity
  labels.
- Serialized posts contain no factual-memory promotion fields.
- Factual retrieval bundles cannot include imagined post content as evidence.

## Explicit Non-Actions

- No LLM call, scheduler, publisher, outbound request, delivery adapter,
  platform integration, push notification, webhook, queue, review UI,
  voice/avatar/video behavior, Live2D, social feed publishing, web demo, or
  automatic sending was added.
- No `private/chat_history/`, `private/distilled/`, or private artifact content
  was read, quoted, summarized, or committed.
- No real-person clone, public-figure clone, deceased-person mode, or deceptive
  impersonation path was authorized.
- T293 does not mark itself complete in `docs/04_task_board.md`.

## Verification

Commands run:

```text
$env:PYTHONPATH='src'
pytest tests\test_virtual_life_contamination.py -q -o cache_dir=artifacts\t293_pytest_cache --basetemp=artifacts\t293_pytest_basetemp
```

Result: passed, `5 passed`.

```text
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\core\models.py src\practical_chat_agent\services\virtual_life_engine.py
```

Result: passed.

```text
$env:PYTHONPATH='src'
pytest tests\test_virtual_life_contamination.py tests\test_virtual_life_aigc_labeling.py tests\test_memory_retrieval_bundle_schema.py -q -o cache_dir=artifacts\t293_pytest_cache_min --basetemp=artifacts\t293_pytest_basetemp_min
```

Result: passed, `17 passed`.

```text
git diff --check
```

Result: passed with Windows line-ending conversion warnings.

## Remaining Risks

- T293 adds contamination guards and tests only.
- Dynamic review cards, M18 gate review, UI, and web demo remain unopened.

## Recommended Reviewer Type

Adversarial review.
