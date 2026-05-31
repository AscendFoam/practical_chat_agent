# Web Demo Friendly Labels And Accessibility Plan

Task: T352 Friendly Labels And Accessibility Contract
Status: worker draft for review

## Target Audiences

The M24 static web demo is still for internal reviewers:

- product reviewers checking companion UX coherence;
- safety reviewers checking blocked states and boundaries;
- frontend reviewers checking layout and interaction quality;
- research reviewers checking whether a supervised walkthrough is legible;
- engineering reviewers checking state-contract consistency.

It is not yet written for public users, external study participants, app-store
reviewers, or production support teams.

## Label Tone Principles

Friendly labels should be:

- short enough for compact panels and mobile;
- direct about what is blocked or disabled;
- plain English before technical detail;
- consistent across tabs, scenarios, tags, and notices;
- clear that synthetic content is AI-generated;
- clear that imagined content is not real-world activity;
- clear that proactive behavior cannot send messages;
- clear that voice/avatar are off, locked, and research-only.

Friendly labels must not:

- make real-person recreation sound allowed;
- soften crisis/dependency blocked states into normal chat;
- imply voice, avatar, microphone, camera, ASR, TTS, Live2D, or media runtime;
- imply automatic outreach, scheduling, or platform delivery;
- hide AI-generated/synthetic identity;
- claim validation, compliance, or launch readiness.

## Technical-To-Friendly Label Mapping

| Technical value | Friendly visible label | Notes |
| --- | --- | --- |
| `chat_review` | Chat review | Safe default review state. |
| `chat_blocked` | Chat blocked for review | Use with crisis/dependency reasons. |
| `persona_blocked` | Persona request blocked | Pair with specific reason. |
| `candidate` | Candidate persona | Shows draft status, not a real person. |
| `fictional_ai_persona` | Fictional AI persona | Preserve synthetic boundary. |
| `real_person_clone_blocked` | Real-person recreation is blocked | Do not shorten to "clone blocked" only. |
| `crisis_safety_review_required` | Crisis safety review required | Do not present as clinical support. |
| `proactive_enabled_review` | Proactive settings review | Pair with no-send status. |
| `proactive_blocked` | Proactive outreach blocked | Pair with reason. |
| `proactive_outreach_blocked` | Proactive outreach is blocked | Avoid "message ready" language. |
| `outreach_allowed: false` | No messages can be sent | Must remain visible in Proactive scenario. |
| `evidence_backed` | Evidence-backed | For factual memory only. |
| `imagined` | Imagined | For fictional continuity only. |
| `imagined_ai_generated_content` | Imagined AI-generated content | Life stream label. |
| `not_real_world_activity` | Not real-world activity | Must remain visible for life stream. |
| `ai_generated` | AI-generated | Can appear as compact tag. |
| `synthetic_content` | Synthetic content | Can appear as compact tag. |
| `review_required` | Needs review | Do not imply completion. |
| `disabled` | Off | Voice state only. |
| `blocked` | Blocked | Pair with reason. |
| `voice_enabled: false` | Voice is off | Must remain visible in Voice / Avatar. |
| `avatar_enabled: false` | Avatar is off | Must remain visible if avatar row is added. |
| `locked_research_only` | Locked for research review | Voice/avatar future scope. |
| `avatar_runtime_not_implemented` | Avatar runtime is not implemented | Technical but clearer. |
| `real_person_likeness_blocked` | Real-person likeness is blocked | Must remain explicit. |
| `visual_capture_blocked` | Visual capture is blocked | Blocks camera/face capture expectation. |

## Scenario-Specific Copy Improvements

| Scenario | Current risk | Friendly copy direction |
| --- | --- | --- |
| Safe review | Technical memory metadata can look raw. | Use "Evidence-backed" and "Imagined" labels beside memory cards. |
| Blocked persona | `real_person_clone_blocked` is understandable but technical. | Show "Real-person recreation is blocked" in the notice. |
| Crisis chat | Crisis reason is terse. | Show "Crisis safety review required" and avoid advice-like wording. |
| Dependency | `outreach allowed: false` is clear but awkward. | Show "No messages can be sent" in the proactive summary. |
| Life review | Life stream could look like real activity. | Keep "Imagined" and "Not real-world activity" near the content. |
| Controls | Consent scopes are raw implementation labels. | Show "Memory", "Proactive review", "AIGC export/share review", and "Voice/avatar review". |
| Voice / Avatar | Technical locked state is long. | Show "Voice is off" and "Avatar locked for research review". |

## Accessibility Priorities

The static UI should support:

- persistent visible AI identity disclosure;
- semantic top-level tabs;
- semantic tab panels;
- active scenario state exposed beyond color;
- native button activation for Enter and Space;
- visible focus state on every interactive element;
- accessible names matching visible labels;
- no color-only status communication;
- readable contrast for warning and danger notices;
- labels that wrap without horizontal page scrolling;
- stable panel layout when active labels change.

## Keyboard Interaction Expectations

Minimum T353 behavior:

- `Tab` reaches every top-level tab and every scenario button.
- `Enter` and `Space` activate top-level tabs because controls remain native
  buttons.
- `Enter` and `Space` activate scenario controls because controls remain native
  buttons.
- Active top-level tab updates `aria-selected`.
- Inactive top-level tabs update `aria-selected=false`.
- Active panel is associated with the active tab through `aria-controls` and
  `aria-labelledby`.
- Inactive panels use `hidden` or an equivalent accessible hidden state.
- Active scenario button updates `aria-pressed=true`.
- Inactive scenario buttons update `aria-pressed=false`.

Arrow-key tab navigation can remain a later enhancement if T353 records it as a
residual risk.

## Responsive Layout Expectations

T353 should preserve or improve:

- no horizontal page overflow at representative desktop and mobile widths;
- wrapping top tabs;
- wrapping scenario buttons;
- single-column scenario controls below the mobile breakpoint;
- labels and notices that wrap long words safely;
- panel headers that do not overlap tags;
- readable status strip on mobile.

## Explicit Non-Goals

T352 does not implement:

- HTML, CSS, or JavaScript changes;
- browser QA;
- screen-reader validation;
- public user copy;
- external user research;
- production accessibility certification;
- private chat ingestion;
- model-provider calls;
- automatic outreach;
- platform delivery;
- voice/avatar runtime;
- generated media;
- launch or compliance readiness.

