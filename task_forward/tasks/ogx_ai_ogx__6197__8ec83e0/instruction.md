# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
ci: TypeScript streaming integration tests fail with "Premature close" on Node.js 22.23.0

### System Info

GitHub CI environment.

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

The TypeScript client streaming integration tests (streaming basic response: earth and streaming basic response: saturn) began failing consistently on 2026-06-25 with `Premature close` errors. The failures affect all PRs and main branch runs. Non-streaming tests continue to pass.

Root Cause
Node.js 22.23.0 was released between June 23-24 and includes a security fix for `CVE-2026-48931` (response queue poisoning in http.Agent). This fix changes keep-alive socket reuse behavior in a way that exposes a latent bug in `node-fetch v2` (the library used by `ogx-client-typescript` for HTTP requests).

Specifically, node-fetch v2's malformed chunked response detector fires false-positive ERR_STREAM_PREMATURE_CLOSE errors on reused pooled sockets when the response uses Transfer-Encoding: chunked (as SSE/streaming responses do).

Evidence:
  - Last passing run (June 23, 17:11 UTC): Node.js v22.22.3 - all 4 TypeScript tests pass
  - First failing run (June 25, 00:30 UTC): Node.js v22.23.0 - streaming tests fail, same commit `63b14e03`

Upstream References
  - nodejs/node#63989 — bug report against Node.js 22.23.0
  - nodejs/node#64004 — fix: "http: avoid stream listeners on idle agent sockets"
  - node-fetch/node-fetch#1767 — underlying node-fetch v2 bug

### Error logs

```
Installing ogx-client from: /home/runner/work/ogx/ogx/.ts-client-checkout
Verifying ogx-client installation...
✅ ogx-client successfully installed
ogx-typescript-integration-tests@0.0.1 /home/runner/work/ogx/ogx/tests/integration/client-typescript
└── ogx-client@1.1.0-alpha.6 -> ./../../../.ts-client-checkout

Running TypeScript tests for suite responses (setup gpt)

> ogx-typescript-integration-tests@0.0.1 test
> node run-tests.js

Running TypeScript tests for suite responses (setup gpt): __tests__/responses.test.ts
  console.log
    
    === Integration Test Configuration ===

      at Object.<anonymous> (setup.ts:44:11)

  console.log
    Base URL: http://localhost:8321

      at Object.<anonymous> (setup.ts:45:11)

  console.log
    Setup: gpt

      at Object.<anonymous> (setup.ts:46:11)

  console.log
    Text Model: openai/gpt-4o

      at Object.<anonymous> (setup.ts:47:11)

  console.log
    Embedding Model: openai/text-embedding-3-small

      at Object.<anonymous> (setup.ts:50:11)

  console.log
    =====================================

      at Object.<anonymous> (setup.ts:55:11)

FAIL __tests__/responses.test.ts
  Responses API - Basic
    ✓ non-streaming basic response: earth (117 ms)
    ✓ non-streaming basic response: saturn (73 ms)
    ✕ streaming basic response: earth (39 ms)
    ✕ streaming basic response: saturn (27 ms)

  ● Responses API - Basic › streaming basic response: earth

    Premature close

      at IncomingMessage.<anonymous> (../../../.ts-client-checkout/node_modules/node-fetch/lib/index.js:1748:18)

  ● Responses API - Basic › streaming basic response: saturn

    Premature close

      at IncomingMessage.<anonymous> (../../../.ts-client-checkout/node_modules/node-fetch/lib/index.js:1748:18)

Test Suites: 1 failed, 1 total
Tests:       2 failed, 2 passed, 4 total
Snapshots:   0 total
Time:        2.245 s
Ran all test suites matching /__tests__\/responses.test.ts/i.
Stopping OGX Server...
Killing OGX Server processes: 2776
2776
OGX Server stopped
Error: Process completed with exit code 1.
```

### Expected behavior

Workflows complete as expected for the open PRs that are currently failing these checks, like:
- #5603
- #6034
- #6191

Example of job runs that should be completing but currently aren't:
https://github.com/ogx-ai/ogx/actions/runs/28260842034/job/83735615820?pr=5603
https://github.com/ogx-ai/ogx/actions/runs/28208536507/job/83564556649?pr=6191
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8ec83e076d02371a5568d31b0b484482978e3f3d`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "ogx_ai_ogx__6197__8ec83e0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
