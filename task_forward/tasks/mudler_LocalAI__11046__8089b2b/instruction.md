# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Docs: reverse-proxy guide should cover upstream timeouts (OpenResty/nginx 504 on long vision/Responses)

<!-- Thanks for LocalAI. This is primarily a documentation / reverse-proxy ops gap that repeatedly surfaces as a hard 504 to API clients. -->

**LocalAI version:**
Observed against a self-hosted LocalAI deployment exposing OpenAI-compatible `/v1` (including Responses). Edge returns `server: openresty`. Client is .NET OpenAI SDK / Microsoft.Extensions.AI calling non-streaming Responses with multimodal (vision) content.

**Environment, CPU architecture, OS, and Version:**
- Client OS: macOS (Apple Silicon)
- LocalAI is **not** on the client machine; it is reached at a public HTTPS hostname terminated by **OpenResty/nginx**
- Workload: multi-page PDF vision OCR via `/v1` Responses (image/jpeg page renders, ~60–70KB+ per page, non-streaming)
- Model slot example: large multimodal/chat model (e.g. gemma-class vision-capable slot)

**Describe the bug**
Long-running **non-streaming** multimodal / Responses requests fail with:

```text
ClientResultException: Service request failed.
Status: 504 (Gateway Time-out)
```

The HTML body is a classic reverse-proxy gateway timeout page (`504 Gateway Time-out`), not a structured LocalAI/OpenAI error.

This is easy to mis-attribute to LocalAI itself (or to WebSocket/SSE disconnects). In practice:

1. LocalAI is still generating (or would finish) on the backend.
2. The **edge reverse proxy** closes the upstream wait first (`proxy_read_timeout` / equivalent).
3. Clients see a hard 504 and abort the whole multi-page job.

LocalAI's reverse-proxy docs currently cover TLS headers (`X-Forwarded-Proto/Host/Prefix`) but **do not mention proxy read/send timeouts**, body size, or buffering guidance for long inference:

- https://localai.io/advanced/reverse-proxy-tls/
- Source: `docs/content/advanced/reverse-proxy-tls.md`

That doc gap makes 504s a recurring footgun for anyone putting LocalAI behind nginx/OpenResty/NPM/Caddy/Traefik for HTTPS.

Related historical report (closed stale, different primary title, same 504 pattern behind nginx domain vs direct IP):

- https://github.com/mudler/LocalAI/issues/3608#issuecomment-2363988006 — `504 Gateway Time-out` on `POST .../v1/completions` when LocalAI is behind Nginx Proxy Manager; works via IP; backend eventually produces a response.

**To Reproduce**
1. Run LocalAI behind OpenResty/nginx (or Nginx Proxy Manager) with default proxy timeouts (often ~60s).
2. Point an OpenAI-compatible client at the **HTTPS reverse-proxy URL** (not the direct LocalAI port).
3. Issue a **non-streaming** multimodal request that takes longer than the proxy read timeout, e.g.:
   - Responses/chat completion with a full page-scan JPEG
   - Large prompt + vision model on GPU/CPU that needs multiple minutes
4. Observe client `504 Gateway Time-out` while LocalAI may still be working if hit directly on the internal port.

Minimal client symptom (C# OpenAI / MEAI style):

```text
Service request failed. Status: 504 (Gateway Time-out)
```

**Expected behavior**
1. **Docs:** Reverse-proxy guide should explicitly warn that default nginx/OpenResty `proxy_read_timeout` (often 60s) is far too low for local LLM inference, especially vision / non-streaming Responses, and should show recommended timeout / body / buffering settings.
2. **Ops clarity:** Distinguish:
   - edge 504 (proxy gave up waiting)
   - LocalAI busy-watchdog killing long jobs (`LOCALAI_WATCHDOG_BUSY` / `LOCALAI_WATCHDOG_BUSY_TIMEOUT`, default busy timeout 5m if enabled)
   - true backend failure
3. Optionally: health/metrics or error body that makes “upstream still running / proxy timeout” obvious (nice-to-have; docs alone would already help a lot).

**Logs**
Client-side (document ingestion OCR path):

```text
PDF OCR page N send (... bytes JPEG ...)
ClientResultException: Service request failed. Status: 504 (Gateway Time-out)
```

Edge headers from the public host:

```http
HTTP/2 405
server: openresty
```

(OpenResty confirmed in front of `/v1`.)

Direct internal LocalAI often continues / succeeds for the same class of request when the proxy is bypassed (same pattern as #3608).

**Workarounds that work (please consider documenting)**

### 1. Raise reverse-proxy upstream timeouts (primary fix)

OpenResty/nginx `location` proxying to LocalAI:

```nginx
proxy_http_version 1.1;
proxy_set_header Host $host;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-Host $host;
proxy_set_header Connection "";

# Critical for long non-streaming chat/responses/vision
proxy_connect_timeout 60s;
proxy_send_timeout    60m;
proxy_read_timeout    60m;

# Multimodal payloads
client_max_body_size 50m;
proxy_request_buffering off;  # optional
proxy_buffering off;          # optional; helpful for long/streamed responses
```

Equivalent knobs exist in NPM / Caddy / Traefik / HAProxy — the important part is **upstream response wait**, not only TLS headers.

### 2. Bypass public edge for bulk jobs
Point long OCR/batch clients at the internal LocalAI URL (`http://host:8080/v1`) while keeping the public reverse proxy for interactive/browser use.

### 3. LocalAI busy watchdog
If busy watchdog is enabled, ensure `LOCALAI_WATCHDOG_BUSY_TIMEOUT` is **greater than worst-case single request time**, or disable busy watchdog for bulk vision jobs. Default busy timeout is `5m` per runtime settings docs — multi-minute vision pages can look “stuck busy”.

### 4. Client resilience (does not fix root cause)
- Retry 504/502/408 with smaller image long-edge
- Fail open per page for batch OCR
- Do not treat Realtime WebSocket cancels as the PDF/Responses failure mode (different path)

**Additional context**

Why this is worth a first-class docs note:

1. LocalAI intentionally documents reverse-proxy TLS header setup, but omits the timeout settings every production HTTPS deploy needs for local inference latency.
2. 504 HTML from OpenResty/nginx is opaque to OpenAI SDKs → operators waste time debugging “LocalAI Responses/WebSocket” when the edge simply timed out.
3. Vision + non-streaming Responses is an increasingly common path (document OCR, screenshots, agents) and routinely exceeds 60s.
4. LocalAI’s own HTTP client comments note avoiding global response timeouts for long-lived bodies; the edge proxy defaults fight that design unless configured.

Happy to turn the nginx snippet above into a PR against `docs/content/advanced/reverse-proxy-tls.md` (and/or advanced-usage) if maintainers want that shape.

**Suggested doc addition (sketch)**

Under reverse-proxy TLS / nginx section, add something like:

> Long-running inference (especially multimodal and non-streaming Responses) often exceeds default reverse-proxy read timeouts (nginx/OpenResty commonly default to 60s), which surfaces to clients as **504 Gateway Time-out** even while LocalAI is still generating. Raise `proxy_read_timeout` / `proxy_send_timeout` (or your proxy’s equivalent) to cover worst-case generation time, increase body size limits for image payloads, and prefer hitting LocalAI directly on the private network for bulk jobs.

Thanks!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8089b2bf0998428975da076d06faab592fd415e6`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__11046__8089b2b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
