# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Web UI fonts and lazy-loaded scripts ignore X-Forwarded-Prefix

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
<!-- Container Image or LocalAI tag/commit -->

LocalAI v4.7.1 (b224c96db6f4b87306a33a808650bfce63b12588)

Docker image:
localai/localai@sha256:66c8824a4bd85f24c55c14b916ecac14550c684d64c7b8fcb5000952d665c30a

**Environment, CPU architecture, OS, and Version:**
<!-- Provide the output from "uname -a", HW specs, if it's a VM  -->

Debian GNU/Linux 13 (trixie) x86_64

Linux internal-host 6.12.94+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.94-1 (2026-06-20) x86_64 GNU/Linux

**Describe the bug**
<!-- A clear and concise description of what the bug is. -->

I am serving the LocalAI Web UI through nginx under `/llm/`.

nginx preserves the `/llm/` path when proxying to LocalAI and sends:

```http
X-Forwarded-Prefix: /llm/
```

Resources referenced directly by the initial HTML are correctly prefixed. However, some font files and lazy-loaded JavaScript chunks are later requested from the origin root.

The resulting 404s cause UI icons to appear as missing-glyph “tofu” characters and may prevent parts of the management UI from loading correctly.

A secondary cache-busted favicon request also returns 404, although that has no visible impact because the initial favicon loads successfully.

*Reverse proxy configuration*

The relevant nginx configuration is:

```nginx
location = /llm {
    return 302 llm/;
}

location /llm/ {
    proxy_pass http://internal-host.local:47080;

    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host:$server_port;
    proxy_set_header X-Forwarded-Prefix /llm/;
}
```

Because `proxy_pass` has no URI component, nginx forwards `/llm/...` upstream without stripping the prefix.

The public hostname is intentionally replaced with `my.redacted.domain` because the instance is not intended for public discovery or third-party testing.

**To Reproduce**
<!-- Steps to reproduce the behavior, including the LocalAI command used, if any -->

1. Run the LocalAI version and container image listed above.
2. Proxy LocalAI through nginx under `/llm/` using the configuration above.
3. Open `/llm/app`.
4. Open the browser Network panel.
5. Navigate through the management UI to trigger lazy-loaded components.
6. Observe 404 responses for root-level JavaScript and font resources under `/assets/...`.

**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->

When `X-Forwarded-Prefix: /llm/` is supplied, all same-origin Web UI resources should remain under `/llm/`, including resources loaded later from compiled JavaScript or CSS.

**Actual behavior**

The initial HTML is prefix-aware, but some URLs embedded in compiled assets or generated at runtime bypass `/llm/` and return 404.

The JavaScript and font failures have visible usability impact. The favicon failure appears to be a related but low-impact symptom.
**Logs**
<!-- If applicable, add logs while running LocalAI in debug mode (`--debug` or `DEBUG=true`) to help explain your problem.  -->

**Additional context**
<!-- Add any other context about the problem here. -->

*Evidence*

The initial HTML contains correctly prefixed URLs:

```html
<base href="https://my.redacted.domain:443/llm/" />
<link rel="icon" type="image/svg+xml" href="/llm/favicon.svg" />
<script type="module" crossorigin src="/llm/assets/index-CUPsCTJ1.js"></script>
<link rel="modulepreload" crossorigin href="/llm/assets/chunk-Cyuzqnbw.js">
<link rel="modulepreload" crossorigin href="/llm/assets/jsx-runtime-xIJTzhZo.js">
<link rel="modulepreload" crossorigin href="/llm/assets/api-CbRzmvjD.js">
<link rel="stylesheet" crossorigin href="/llm/assets/index-B5EK2jBS.css">
```

These initial resources load successfully.

The loaded JavaScript subsequently requests additional chunks from paths such as:

```text
/assets/<chunk>.js
```

rather than:

```text
/llm/assets/<chunk>.js
```

Font resources are similarly requested from paths such as:

```text
/assets/<font>.woff2
```

rather than:

```text
/llm/assets/<font>.woff2
```

The root-level requests return 404. Missing font resources cause icons in the management UI to render as tofu characters.

There is also a lower-impact request after startup:

```text
/favicon.svg?v=<timestamp>
```

It returns 404 because it omits `/llm/`. The favicon remains visible because the initial `/llm/favicon.svg` request succeeded.

*Related prior work and likely cause*

This appears related to #9145 and its fix in #9614.

The existing handling correctly prefixes references in the initial HTML, but the observed behavior suggests it does not cover:

* lazy-chunk URLs embedded in compiled JavaScript;
* font URLs embedded in compiled CSS;
* root-absolute URLs generated later by frontend JavaScript.

The frontend should consistently resolve runtime and compiled asset URLs against the configured base path rather than the origin root.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `40d35c0385df6015f839a89e4729b931be716db2`.  There
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
{"case_id": "mudler_LocalAI__10889__40d35c0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
