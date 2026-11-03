# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
vscode: back off and bound memory when analysis fails repeatedly

## Problem

In #1086 the reporter described the VS Code extension analyzing, failing, and then continuously restarting analysis (including after a full VS Code restart), each attempt consuming memory again. When analysis on a project fails or exhausts memory, the extension should not keep re-attempting the same work in a tight loop, which compounds the resource pressure rather than recovering.

The extension has retry and client-restart machinery (`commands.ts` retry outcomes, `client.ts` `restartClient`) but no backoff that gives up after repeated failures on the same workspace, and the spawned analysis process has no memory ceiling.

The default per-file size skip that shipped for #1086 reduces the chance that a single large file triggers this, but the resilience gap (a failing analysis that re-runs indefinitely) is worth closing on its own.

## Proposed direction

- Crash/failure backoff: after N consecutive analysis failures for the same workspace, stop auto-re-running and surface a clear, dismissable message with a manual "retry" affordance, instead of looping.
- Process memory ceiling on the spawned analysis so an out-of-memory run fails fast with an actionable error rather than taking the editor down with it.
- Make sure a transient retry path cannot re-enter immediately on the same input that just failed.

## Acceptance

- A workspace whose analysis fails repeatedly stops auto-retrying after a bounded number of attempts and shows a clear message.
- An analysis run cannot grow unbounded; it fails with a diagnostic the user can act on.
- Normal (successful) analysis and the existing reveal/latch retry behavior are unchanged.

Size: M. Hardening follow-up to #1086.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `70d5167074917d27e02531e8a669463bb52784c5`.  There
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
{"case_id": "fallow_rs_fallow__1105__70d5167",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
