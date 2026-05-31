# Local Web Demo Server Contract

Task: T351 Local Demo Server
Status: worker draft for review

## Scope

`TextFirstWebDemoLocalServer` exposes dependency-free local preview routes for
the text-first web demo. It serves only synthetic adapter-backed demo state and
existing local static assets.

Implemented file:

- `src/practical_chat_agent/ui/text_first_web_demo_local_server.py`

Implemented objects:

- `LocalDemoResponse`
- `TextFirstWebDemoLocalServer`
- `build_http_server(...)`

## Routes

| Route | Status | Content type | Source |
| --- | --- | --- | --- |
| `/` | `200` | `text/html; charset=utf-8` | `TextFirstWebDemoStaticShell.render_embedded_html(...)` |
| `/text_first_web_demo.html` | `200` | `text/html; charset=utf-8` | Same as `/`. |
| `/demo-state.json` | `200` | `application/json; charset=utf-8` | `TextFirstWebDemoStaticShell.build_demo_payload_json(...)` |
| `/text_first_web_demo.css` | `200` | `text/css; charset=utf-8` | Existing local CSS asset. |
| `/text_first_web_demo.js` | `200` | `application/javascript; charset=utf-8` | Existing local JS asset. |
| Unknown path | `404` | `text/plain; charset=utf-8` | Not found response. |
| Path traversal | `403` | `text/plain; charset=utf-8` | Rejected before asset lookup. |

All responses include `Cache-Control: no-store`.

## Synthetic State Source

The root HTML and `/demo-state.json` route use:

```text
TextFirstWebDemoAdapter.build_synthetic_demo_state(...)
```

through `TextFirstWebDemoStaticShell`.

The state remains:

- `schema_version=text_first_web_demo_state_v1`;
- synthetic;
- `review_required=true`;
- AI-generated/synthetic labeled;
- voice disabled/not enabled;
- avatar locked/not enabled;
- proactive non-sending.

## Local-Only Behavior

The helper is designed so tests can validate route responses without keeping a
server process alive.

`build_http_server(...)` creates a standard-library `ThreadingHTTPServer` bound
by default to:

```text
127.0.0.1:8767
```

Callers remain responsible for starting and stopping that server in local
review tooling. T351 does not add a CLI command, background service, production
server, public network binding, tunnel, auth flow, token, or platform endpoint.

## Security And Boundary Behavior

The router rejects:

- decoded `..` path segments;
- decoded `.` path segments;
- backslash paths;
- unknown files.

The router serves only named static assets. It does not expose arbitrary file
serving rooted at the repository.

## No-Runtime Boundaries

Responses must not contain:

- raw private chat text;
- private transcripts;
- provider credentials;
- generated audio or video paths;
- voice samples;
- audio bytes;
- microphone or camera prompts;
- platform delivery fields;
- send queues;
- schedules;
- webhooks;
- runtime voice enablement;
- runtime avatar enablement.

The helper must not call model providers, read private chat logs, generate
media, capture input devices, send messages, schedule messages, mutate
persistent state, or integrate with platforms.

## Verification

Expected minimum verification:

```powershell
$env:PYTHONPATH='src'
python -m py_compile src\practical_chat_agent\ui\text_first_web_demo_local_server.py
```

```powershell
$env:PYTHONPATH='src'
pytest tests\test_text_first_web_demo_local_server.py tests\test_text_first_web_demo_static.py tests\test_text_first_web_demo_adapter.py -q
```

```powershell
git diff --check
```

Browser verification is deferred to a later M24 task because T351 only adds a
testable local route helper.

