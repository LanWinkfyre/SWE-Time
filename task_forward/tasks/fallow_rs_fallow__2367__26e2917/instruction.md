# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Parse package.json resolutions as an override source for bun repos

The dependency-override analyzer reads only the top-level `overrides` object and `pnpm.overrides` (plus `pnpm-workspace.yaml` overrides). bun honours Yarn-style `resolutions` in `package.json` as an alias for `overrides`, so a bun repository that pins transitive versions under `resolutions` is never analyzed: no `unused-dependency-overrides` or `misconfigured-dependency-overrides` findings with any lockfile, and since #2362 no `bun-lockb-override-resolution-skipped` diagnostic either, because no override state is gathered and the skip point is never reached.

## Reproduction

1. `package.json` with `"packageManager": "bun@1.3.2"`, `"dependencies": { "ws": "^8.21.0" }`, `"resolutions": { "ws": "^8.21.0", "left-pad": "^1.3.0" }` and a `bun.lockb` next to it: `fallow dead-code --format json --quiet` has no `workspace_diagnostics`, no override findings, and no stderr warning.
2. Same manifest with `"resolutions": { "left-pad": "^1.3.0" }` and a text `bun.lock` whose `packages` contain only `ws`: expected `left-pad` as an unused override with the bun hint; actual: no findings.

## Scope suggestion

- Parse `resolutions` through the existing npm override parser when the repository is bun (`packageManager` field or a bun lockfile present).
- For yarn repositories keep the current stance (yarn `resolutions` out of scope) or treat them the same way with a yarn hint; decide and document.
- Update the module docs in `crates/core/src/analyze/unused_overrides.rs`, which state that yarn `resolutions` is out of scope.
- Extend the `bun.lockb` skip diagnostic so a resolutions-only manifest next to a `bun.lockb` also reports it.

Surfaced while reviewing #2362 (the fix for #2358).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `26e291720b30f1877fdce41ec6ce01ef9e1e43c7`.  There
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
{"case_id": "fallow_rs_fallow__2367__26e2917",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
