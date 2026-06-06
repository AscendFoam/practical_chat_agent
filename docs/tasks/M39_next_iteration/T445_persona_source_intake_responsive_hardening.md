# T445: Persona Source Intake Responsive Hardening

## Task ID

T445

## Goal

Harden dense source intake manifest and Review Workspace source-card layouts
for narrow viewports and long ids.

This task is CSS/static-test hardening only. It must not change adapter
payload semantics, add source readers, read private data, call model
providers, extract traits, write stores, apply persona changes, send messages,
connect platform adapters, or enable media runtime.

## Context

T442 added `persona_source_intake_manifest`, T443 rendered it in the static
demo, and T444 linked source intake records into Review Workspace. Source ids,
gate ids, blocked reason ids, redaction profile ids, consent labels, and
minimization labels can be long. T445 should make wrapping and width
constraints explicit before M39 review.

## Allowed Files

Future T445 worker may create or modify only:

- `src/practical_chat_agent/ui/static/text_first_web_demo.css`
- `tests/test_persona_source_intake_responsive_hardening.py`
- `tests/test_static_persona_source_intake_manifest.py`
- `tests/test_persona_source_intake_review_linkage.py`
- `tests/test_text_first_web_demo_static.py`
- `tests/test_text_first_web_demo_state_switching.py`
- `docs/tasks/M39_next_iteration/T446_m39_milestone_review.md`
- `docs/worker_summary/T445_worker_summary.md`
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

- Add explicit wrapping guards for source candidate cards, policy gate cards,
  blocked category cards, redaction profile cards, and source review cards.
- Constrain source intake grids, labels, meta rows, and detail rows to
  `min-width: 0` and `overflow-wrap: anywhere`.
- Extend mobile rules for source intake section heads, non-execution labels,
  policy summary, and Review Workspace source detail lists.
- Add focused static tests that fail unless these responsive selectors exist.
- Create the T446 M39 milestone review task package.

## Browser QA

After tests pass, verify at the available viewport:

- source intake section has no overflowing nodes;
- Review Workspace source cards have no overflowing nodes;
- `Source (21)` filter is visible;
- no forbidden action controls appear;
- no document horizontal overflow.

## Verification

Minimum commands:

```powershell
$env:PYTHONPATH='src'; pytest tests\test_persona_source_intake_responsive_hardening.py tests\test_static_persona_source_intake_manifest.py tests\test_persona_source_intake_review_linkage.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_state_switching.py -q -o cache_dir=artifacts\t445_pytest_cache --basetemp=artifacts\t445_pytest_basetemp
```

```powershell
git diff --check
```

## Reviewer Type

Responsive CSS review for source intake manifest cards, Review Workspace
source cards, long-id wrapping, mobile layout stability, and absence of action
controls.
