# T451: Persona Source Evidence Responsive Hardening

## Task ID

T451

## Goal

Harden dense source evidence matrix and Review Workspace evidence-card layouts
for narrow viewports and long ids.

This task is CSS/static-test hardening only. It must not change adapter payload
semantics, add source readers, read private data, call model providers, extract
traits, write stores, apply persona changes, send messages, connect platform
adapters, or enable media runtime.

## Context

T448 added `persona_source_evidence_matrix`, T449 rendered it in the static
demo, and T450 linked source evidence records into Review Workspace. Evidence
row ids, source ids, quality labels, gate ids, trait paths, uncertainty notes,
and support/conflict evidence ids can be long. T451 should make wrapping and
width constraints explicit before M40 review.

## Allowed Files

Future T451 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_persona_source_evidence_responsive_hardening.py`
- `tests/test_static_persona_source_evidence_matrix.py`
- `tests/test_persona_source_evidence_review_linkage.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/tasks/M40_next_iteration/T452_m40_milestone_review.md`
- `docs/worker_summary/T451_worker_summary.md`
- `docs/07_handoff.md`

If implementation requires adapter payload changes, JavaScript behavior
changes, source readers, model providers, private data, runtime stores,
platform adapters, outbound messaging, media runtime, automatic apply, package
changes, or task-board edits, Captain must revise this package before
assignment.

## Forbidden Scope

- Do not read `private/chat_history/`, `private/distilled/`, or private
  artifacts.
- Do not ingest, summarize, transform, quote, or commit real private chat
  records.
- Do not call model providers or prompt execution layers.
- Do not add source readers, embeddings, vector search, semantic ranking,
  similarity scoring, fine-tuning, or remote inference.
- Do not modify Python adapter payload code or JavaScript renderer behavior.
- Do not write PersonaCard, PersonaVersionStore, MemoryEventStore, review
  stores, runtime stores, local databases, queues, schedulers, or files outside
  the allowed CSS/test/docs files.
- Do not add platform adapters, webhooks, auth, tokens, recipient ids, delivery
  state, automatic outreach, or outbound messaging.
- Do not add microphone, camera, ASR, TTS, voice cloning, Live2D, generated
  audio, generated image, generated video, or media capture.
- Do not add payment processing, production pricing claims, legal advice,
  compliance completion, app-store approval, launch approval, clinical claims,
  regulator acceptance, or user-study validation.
- Do not modify `docs/04_task_board.md`.

## Expected Implementation

- Add explicit wrapping guards for source evidence matrix cards, excluded
  source refs, trait hypothesis cards, quality cards, gate cards, and Review
  Workspace evidence cards.
- Constrain evidence grids, labels, meta rows, and review detail rows to
  `min-width: 0` and `overflow-wrap: anywhere`.
- Extend mobile rules for evidence section heads, non-execution labels,
  manifest summary, eligible source labels, and Review Workspace evidence
  detail lists.
- Add focused static tests that fail unless these responsive selectors exist.
- Create the T452 M40 milestone review task package.

## Browser QA

After tests pass, verify at the available viewport:

- source evidence section has no overflowing nodes;
- Review Workspace evidence cards have no overflowing nodes;
- `Evidence` filter is visible with the expected count;
- no forbidden action controls appear;
- no document horizontal overflow.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_source_evidence_responsive_hardening.py tests\test_static_persona_source_evidence_matrix.py tests\test_persona_source_evidence_review_linkage.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t451_pytest_cache --basetemp=artifacts\t451_pytest_basetemp
```

```powershell
git diff --check
```

## Reviewer Type

Responsive CSS review for source evidence matrix cards, Review Workspace
evidence cards, long-id wrapping, mobile layout stability, and absence of
action controls.
