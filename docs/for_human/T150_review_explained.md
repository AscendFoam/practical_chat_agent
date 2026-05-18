# T150 Review Explained: ReplyPlanner Regression Tests

## 1. What This Task Is About (In Plain Language)

Imagine you've built a system that suggests draft replies to messages from your contacts — like a smart assistant that helps you figure out what to say back. Before T150, this "reply planner" had been built and tested manually, but there were **no automated tests committed to the codebase**. That meant:

- If someone accidentally broke the planner, no alarm would go off.
- If a code change accidentally leaked private message content into the planner's output, nobody would know until a manual check.
- If the contact-matching logic broke, there was no safety net.

T150 is about building that safety net: writing **49 automated tests** that run the planner with fake (synthetic) data and verify it behaves correctly. Think of it like installing smoke detectors in a building — the building was already built, but now it has automated alarms.

## 2. Implementation Details

### Goal

Create committed, deterministic regression tests that guard M3 Conditional obligations for the ReplyPlanner and policy layer. No implementation changes — only tests and test infrastructure.

### What Changed

| File | Change |
|------|--------|
| `tests/__init__.py` | New empty file to make `tests/` a Python package |
| `tests/helpers.py` | New file with 5 helper functions to construct synthetic test objects (events, memories, skill briefs, memory briefs, chat contexts) |
| `tests/conftest.py` | New file with 7 pytest fixtures covering different scenarios (friend, colleague, thin context, sensitive, false-positive probe, false-negative probe, privacy probe) |
| `tests/test_reply_planner.py` | New file with 49 tests across 11 test classes |
| `pyproject.toml` | Added pytest configuration (`pythonpath` and `testpaths`) |
| `docs/07_handoff.md` | Added T150 implementation record (section 44) |
| `docs/08_risks_and_open_questions.md` | Updated risk states and closed Q125-Q129 |

### How the Tests Work

The tests follow a clear pattern:

1. **Construct synthetic input** — A fake `ChatContext` is built using the helpers. This context contains synthetic messages like `"hey, how have you been?"`, fake contact IDs like `"contact_friend"`, and synthetic approved-store records.

2. **Call the real planner** — `ReplyPlanner().generate(context=...)` runs the actual production code. No mocks, no stubs, no fake outputs.

3. **Assert the output** — The test checks that:
   - The plan has exactly 3 candidates (not 0, not 5)
   - Each candidate has required fields (draft text, rationale, supporting refs, boundary reminders)
   - Private input text does NOT appear in the output (privacy leakage guard)
   - Contact IDs are correctly aligned
   - Ranking is unique and stable (1, 2, 3)
   - Thin context produces lower confidence and risk flags
   - Sensitive context produces boundary warnings and conservative wording

### Key Test Scenarios

- **Baseline friend/colleague**: Happy path — planner works normally with full context.
- **Thin context**: No approved store available — planner falls back conservatively.
- **Sensitive/boundary**: Emotional topic with explicit "give space" cues — planner shifts to cautious wording.
- **False-positive probe**: The word "money" appears in a normal work budgeting message. The test verifies the planner does NOT over-react by flagging it as boundary-sensitive.
- **False-negative probe**: A subtle pressure message ("you should really call me sometime soon") that keyword detection misses. The test documents this as a known limitation rather than pretending it works.
- **Privacy leakage**: Unique text markers are planted in the input. The test verifies none of them appear in the output JSON.
- **Contact mismatch**: The store says "contact A" but the routing says "contact B" — planner must reject with an error.
- **Non-approved ID isolation**: Candidate/rejected/frozen record IDs are injected into the input — the test verifies they don't leak into the output.

### Significance for Future Development

These tests serve as a **regression safety net** for all future work on the reply planner. When someone (human or AI) modifies the planner, policy engine, or context assembly code in the future, these 49 tests will immediately catch:

- Structural regressions (wrong number of candidates, missing fields)
- Privacy regressions (private text appearing in output)
- Contact alignment regressions (wrong contact routing)
- Ranking regressions (duplicate or unstable ranking)

This is critical because T151 (policy fixture suite), T152 (feedback CLI regression tests), and eventually M5-M8 will all build on the same planner infrastructure. Without T150, any of those changes could silently break safety properties.

### What's Still Not Covered

T150 tests the **contract wiring and safety surface** — does the planner produce structurally correct, privacy-safe output? It does NOT test:

- **Naturalness**: Whether the suggested replies actually sound good (that's a human judgment, not automatable)
- **Relationship quality**: Whether the planner adapts well to different relationship types
- **Policy engine internals**: Whether individual policy rules work in isolation (tested indirectly, not directly)
- **Feedback CLI**: T152 will cover that separately

## 3. Why the Review Result Is PASS_WITH_WARNINGS

### Why PASS (not BLOCK)

The task fully meets its goal:

- All 11 required coverage areas have committed tests.
- All tests are deterministic — no LLM calls, no network, no randomness.
- All fixtures are synthetic — no real names, no real messages, no private paths.
- The minimum acceptance bar is met: separate regression-guard tests for structure, privacy, contact alignment, and ranking.
- Tests actually call the real production code (not mocked), so they genuinely guard against regressions.
- No implementation files were modified — planner behavior is unchanged.
- Documentation is honest about what was accomplished and what remains open.

### Why WITH_WARNINGS (not plain PASS)

Six non-blocking issues were noted:

1. **Not-configured-path tests reuse the thin-context fixture** — they're not testing a truly distinct scenario, but the assertions are still different and valid.
2. **No direct policy engine unit tests** — the policy engine is only tested through the planner. If a policy change doesn't affect planner output, it could regress silently. T151 can address this.
3. **Colleague tone assertion depends on exact wording** — if the summary text changes slightly, the test breaks. This is acceptable for a regression guard but fragile.
4. **False-negative tests assert absence rather than documenting the gap with a marker** — if a future improvement closes the gap, the tests break (which is actually good).
5. **Helper functions aren't independently tested** — they're simple constructors, so the risk is very low.
6. **`notes_on_candidate_differences` field is never asserted** — a minor coverage gap for an informational field.

None of these are serious enough to block. They are honest limitations that T151 can address if needed. The core deliverable — 49 committed deterministic tests guarding M3 safety properties — is solid.
