# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
fix: enable MCP tools for mcp_mocks with the copilot-sdk executor

## Summary
`mcp_mocks` are converted to Copilot SDK stdio server configurations without the Copilot CLI `tools` allowlist. The bundled CLI rejects the mock server with `No tools specified for server "github"`, so MCP tools never reach the evaluated agent.

## Reproduction
1. Create an eval with `config.executor: copilot-sdk` and an inline or fixture-backed `mcp_mocks` entry.
2. Run the evaluation with the bundled Copilot CLI.
3. Observe the CLI log: `No tools specified for server "github"` followed by the server being skipped.

## Expected behavior
Every server generated from `mcp_mocks` should include the Copilot CLI allowlist `tools: ["*"]`, making its declared deterministic tools available to the agent.

## Actual behavior
The mock server process is healthy, but its SDK configuration omits the allowlist; the CLI skips it without Waza surfacing a warning.

## Environment
Reported with Waza 0.38.2 and bundled Copilot CLI 1.0.64-0 on Windows 10 and WSL2 Ubuntu.

## Workaround
Use `config.mcp_servers` directly and add `tools: ["*"]`.

## Proposed fix
Add the allowlist to Waza's mock-to-SDK conversion, cover it with a regression test, and document the behavior.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `51d5ca8aba9738bdb7bca85c623251e40e109d75`.  There
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
{"case_id": "microsoft_waza__440__51d5ca8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
