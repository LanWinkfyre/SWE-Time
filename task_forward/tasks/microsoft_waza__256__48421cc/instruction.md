# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
chore: upgrade copilot-sdk/go from v0.1.32 to v1.0.0-beta.4 (fixes Windows conpty.node)

## Summary

Upgrade `copilot-sdk/go` from v0.1.32 to v1.0.0-beta.4 and regenerate the embedded CLI binaries from v1.0.2 to v1.0.46.

## Motivation

The current pinned SDK (v0.1.32) embeds Copilot CLI v1.0.2, which has two critical issues:

1. **Missing conpty.node native module on Windows** — the embedded CLI binary ships without platform-specific native modules, causing all PowerShell/terminal tool executions to fail with `Cannot find module conpty.node`. This breaks any eval task that needs to run shell commands.

2. **Stale CLI binary vs SDK API** — the embedded CLI v1.0.2 was bundled when the SDK was first packaged but never re-generated as the SDK evolved. The `go tool bundler` (from `copilot-sdk/go/cmd/bundler`) auto-detects the correct CLI version from go.mod and should be re-run whenever the SDK version changes.

## SDK version to CLI version mapping

| SDK Version | Embedded CLI | conpty.node | Status |
|---|---|---|---|
| v0.1.32 (current) | v1.0.2 | Missing | Broken on Windows |
| v0.2.2 | v1.0.21 | Present | Works |
| v0.3.0 | v1.0.36 | Present | Works |
| **v1.0.0-beta.4** | **v1.0.46** | Present | **Works** |

## API changes addressed

- SessionEvent.Type: field to method (Type())
- SessionEvent.Data: flat struct to typed SessionEventData interface (requires type switches)
- Event constants: copilot.XXX to copilot.SessionEventTypeXXX
- copilot.Result to copilot.ToolExecutionCompleteResult
- MCPServerConfig: map[string]any type alias to interface (MCPStdioServerConfig, MCPHTTPServerConfig)

## Testing

- Built and verified on Windows 11 (amd64)
- Eval tasks with PowerShell tool calls work (no conpty.node errors)
- Prompt grader (haiku judge) grades correctly with the new SDK
- All 6 platform binaries regenerated via go tool bundler
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `48421cc86adbeee1370ceab8382c5ff519efdd4d`.  There
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
{"case_id": "microsoft_waza__256__48421cc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
