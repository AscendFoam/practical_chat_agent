# Task T203: Optional Mem0 Adapter Spike

## Task ID

T203

## Goal

Run a contained spike to evaluate whether Mem0 can be used as an adapter without violating review-first memory semantics.

## Forbidden Scope

- Do not merge Mem0 into main runtime by default.
- Do not allow automatic extraction/write-back.
- Do not index private raw chat history.
- Do not remove local retriever.

## Allowed Files

- `docs/review/T203_mem0_spike_review.md`
- `docs/07_handoff.md`

## Reviewer Type

milestone
