# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Bug] Redact environment-derived fatal diagnostics at process boundaries

## Summary

Three standalone process entry points print caught error messages directly to stderr. Environment-controlled values can reach those messages, which can expose credentials or other sensitive values in image-build and CI logs.

CodeQL reports the same `js/clear-text-logging` flow in alerts 2025, 2026, and 2027.

## Reproduction

Tested on current `main` commit `475a20e00db5984d026b70d0a01654a2822b6a7a`.

- A messaging plan with an environment-supplied invalid render target prints that target verbatim from `messaging-build-applier.mts`.
- An environment-supplied audit report path that escapes the repository root prints that path verbatim from `audit-reviewed-npm-graph.mts`.
- The OpenClaw npm remediation entry point prints raw child-process output from an inherited environment through its caught error.

The first two reproductions emitted a credential-shaped canary unchanged. The third path is the equivalent CodeQL-traced child-process boundary.

## Expected behavior

Each entry point must return its existing nonzero status and print only a fixed, operation-specific failure message. Raw caught errors, environment values, command output, paths, and credentials must not cross the process boundary.

## Acceptance criteria

- Preserve exit status 2 for messaging build failures and exit status 1 for both npm tooling failures.
- Replace raw caught-error output with fixed operation-specific diagnostics at all three reported sinks.
- Add real-process regressions that inject credential-shaped canaries and prove stdout and stderr omit them.
- Keep successful output and internal error propagation unchanged.
- Close CodeQL alerts 2025, 2026, and 2027 without query suppression.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `475a20e00db5984d026b70d0a01654a2822b6a7a`.  There
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
{"case_id": "NVIDIA_NemoClaw__11673__475a20e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
