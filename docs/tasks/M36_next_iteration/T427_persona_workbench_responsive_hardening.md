# T427: Persona Workbench Responsive Hardening

## Task ID

T427

## Goal

Harden the persona workbench and workbench-linked Review Workspace cards for
narrow and desktop static-demo layouts.

T427 should keep the M36 workbench readable under long trait values, evidence
refs, blocked request explanations, safety gate labels, and review-card detail
rows without adding new product capabilities.

## Context

T424 added the workbench payload. T425 rendered the static workbench. T426
linked workbench outputs into Review Workspace cards. The next slice should
focus on layout resilience and Browser QA.

## Allowed Files

Future T427 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_persona_workbench_responsive_hardening.py`
- `tests/test_static_persona_distillation_workbench.py`
- `tests/test_persona_workbench_review_linkage.py`
- `docs/tasks/M36_next_iteration/T428_m36_milestone_review.md`
- `docs/worker_summary/T427_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires adapter payload changes, JavaScript behavior
changes, HTML structure changes, private data, source readers, model providers,
runtime stores, platform adapters, outbound messaging, media runtime,
automatic apply, or task-board edits, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed docs/test/CSS files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

Add focused CSS hardening only if tests show a gap. Likely checks:

- workbench mode/input/evidence/gate cards use `min-width: 0`;
- workbench trait and blocked grids collapse to one column at narrow widths;
- review workspace workbench cards wrap long evidence refs and request types;
- status badges, label rows, and detail rows align without horizontal overflow;
- long ids can wrap without resizing cards.

## Test Requirements

Use TDD:

1. Add failing tests in
   `tests/test_persona_workbench_responsive_hardening.py`.
2. Run focused tests and capture RED output.
3. Add the minimal CSS hardening.
4. Re-run focused tests and capture GREEN output.

Tests should inspect static CSS for concrete selectors rather than relying on
visual assumptions.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_workbench_responsive_hardening.py tests\test_static_persona_distillation_workbench.py tests\test_persona_workbench_review_linkage.py -q -o cache_dir=artifacts\t427_pytest_cache --basetemp=artifacts\t427_pytest_basetemp
```

```powershell
git diff --check
```

If a local static target is available, perform Browser QA:

- workbench section has no horizontal overflow at the available narrow
  viewport;
- Review Workspace distillation cards have no horizontal overflow;
- long evidence refs and blocked request labels wrap;
- no forbidden action controls appear.

## Reviewer Type

Static CSS and Browser QA review for layout hardening only.
