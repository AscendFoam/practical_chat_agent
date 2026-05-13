# Agent Working Agreement

This repository follows the AI coding workflow in `docs/reference/AI_coding_workflow.md`.

## Roles

- Captain maintains project state, task packages, handoff, risks, and review integration.
- Worker completes exactly one assigned task package and does not self-assign the next task.
- Reviewer performs read-only review and reports `PASS`, `PASS_WITH_WARNINGS`, or `BLOCK`.

## Hard Rules

1. Repository files are the project state; chat sessions are temporary.
2. Only one Current Unique Task is active at a time.
3. Worker must stay within the task package `Allowed files`.
4. Do not write mocks, stubs, or future plans as completed facts.
5. Outbound messaging must remain human-approved unless a task explicitly changes policy and passes review.
6. WeChatBot/iLink SDK work starts outside this repository until Gate 0 passes.
7. Do not vendor unofficial WeChat SDK code into this repository during Sprint 0.
8. Do not revert unrelated changes in a dirty worktree.

## Current Entry Point

Read `docs/04_task_board.md`, then use the task file referenced by `Current Unique Task`.

