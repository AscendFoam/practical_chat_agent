# T294: Dynamic Review Card

## Task ID

T294

## Goal

Create a local review-card schema/service for `RoleDynamicPost` drafts. The
card should expose post text, AIGC/imagined labels, factual-claim review notes,
memory-ref usage, and conservative review actions.

T294 must not publish posts, send messages, call LLMs, or integrate with any
platform.

## Why Now

T290-T293 define imagined virtual life drafts, deterministic generation, labels,
and contamination guards. Before the M18 gate review, dynamic posts need a
human-review artifact that makes the imagined/review-only boundary visible.

## Allowed Files

Future T294 worker may create or modify only:

- `src/practical_chat_agent/services/virtual_life_review_card.py`
- `tests/test_virtual_life_review_card.py`
- `docs/data_contracts/virtual_life_review_card_contract.md`
- `docs/tasks/M18_virtual_life_stream/T295_m18_gate_review.md`
- `docs/worker_summary/T294_worker_summary.md`
- `docs/07_handoff.md`

If T294 needs model changes, LLM calls, publishers, platform adapters, UI, or
task-board edits, Captain must revise this package before assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not call LLMs, model providers, external APIs, browser automation, or
  network services.
- Do not publish, send, deliver, enqueue, webhook, notify, or call platform
  adapters.
- Do not implement real social-feed integration, voice/avatar/video behavior,
  Live2D, web demo, or product UI.
- Do not implement real-person clone behavior, deceased-person simulation, or
  deceptive impersonation paths.
- Do not modify `docs/04_task_board.md`, `docs/05_decision_log.md`,
  `docs/06_eval_protocol.md`, or `docs/08_risks_and_open_questions.md`.

## Inputs To Read

Required:

- `docs/data_contracts/role_dynamic_post_contract.md`
- `docs/data_contracts/virtual_life_engine_contract.md`
- `src/practical_chat_agent/core/models.py` RoleDynamicPost section
- `src/practical_chat_agent/services/virtual_life_engine.py`
- `tests/test_virtual_life_contamination.py`
- `tests/test_virtual_life_aigc_labeling.py`

## Expected Outputs

### 1. Review Card

Create `src/practical_chat_agent/services/virtual_life_review_card.py`.

Minimum expected objects:

- `VirtualLifeReviewCard`;
- `VirtualLifeReviewCardService.render(post)`.

Minimum expected behavior:

- card preserves post id, persona id, text, labels, review status, and safety
  notes;
- card exposes review actions such as `approve_for_demo`, `reject`,
  `request_changes`, and `flag_factual_claims`;
- posts with factual claims expose `flag_factual_claims`;
- all cards preserve imagined/AIGC labels;
- card payload contains no publish, send, schedule, delivery, platform,
  webhook, token, or queue fields;
- service exposes no publish/send/schedule/delivery/runtime methods.

### 2. Tests

Add `tests/test_virtual_life_review_card.py` covering:

- card renders labels and review status;
- factual-claim cards expose conservative review action;
- memory refs remain inspiration-only;
- forbidden delivery/platform fields are absent;
- service exposes no publish/send/schedule/delivery/runtime methods.

### 3. Data Contract

Create `docs/data_contracts/virtual_life_review_card_contract.md` describing
card fields, rendering rules, non-actions, and verification.

### 4. Next Task Package

Create `docs/tasks/M18_virtual_life_stream/T295_m18_gate_review.md` for M18
milestone review.

### 5. Worker Summary And Handoff

Write `docs/worker_summary/T294_worker_summary.md` and append a T294 worker
record to `docs/07_handoff.md`.

Do not mark T294 complete in `docs/04_task_board.md`.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\services\virtual_life_review_card.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_virtual_life_review_card.py tests\test_virtual_life_contamination.py tests\test_virtual_life_aigc_labeling.py -q
```

```powershell
git diff --check
```

## Reviewer Type

Adversarial review recommended.

Reviewer should verify that T294 creates review artifacts only and cannot
publish, send, schedule, deliver, call LLMs, or integrate with platforms.
