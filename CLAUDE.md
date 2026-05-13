# Claude Reviewer Notes

Use this file with `AGENTS.md` and `docs/reference/AI_coding_workflow.md` when acting as reviewer.

## Review Posture

Default to read-only review. Check whether the worker completed the exact task package without exceeding scope.

Focus on:

- real implementation versus mock/stub/future wording
- missing verification
- unsafe WeChat or outbound-message behavior
- broken existing Telegram, Feishu, desktop, meeting, memory, or delivery flows
- docs that claim unverified work is done

## Verdicts

- `PASS`: task complete, no blocking issue.
- `PASS_WITH_WARNINGS`: task can move forward, but warnings must be classified by Captain as accepted, deferred, or rejected.
- `BLOCK`: task cannot be accepted without a targeted fix.

For high-risk tasks, use adversarial review: data pipeline, policy, delivery, migrations, or milestone gates.

