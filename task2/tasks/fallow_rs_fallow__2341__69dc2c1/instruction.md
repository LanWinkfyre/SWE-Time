# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused_dependency_overrides: false positives in bun repos — bun.lock is not consulted (same bug as #371, for bun)

### What happened?

In a bun workspace, every `overrides` entry whose target is a transitive-only dependency is reported as `unused_dependency_overrides`, even though the target is resolved in `bun.lock`. This is #371 (fixed for pnpm in v2.74.0) reproduced for bun.

The cause looks structural rather than incidental. In `crates/core/src/analyze/unused_overrides.rs`, `collect_lockfile_packages` reads only `pnpm-lock.yaml` and `package-lock.json`, and the module doc states "yarn `resolutions` and bun overrides are out of scope."

But bun declares overrides using the **same top-level `overrides` key as npm**, so the npm parser added in v3.11.0 (#2069) picks bun's overrides up regardless of that stated scope. Since no recognised lockfile is present, the resolved set degrades to empty and the analysis falls back to declarations only — so every transitive-only override is flagged.

Net effect: bun overrides are out of scope for lockfile *resolution*, but in scope for *reporting*.

### Reproduction

`package.json`:

```json
{
  "packageManager": "bun@1.3.14",
  "devDependencies": { "happy-dom": "^20.10.6" },
  "overrides": { "ws": "^8.21.0" }
}
```

`bun install` resolves `ws` to 8.21.0 in `bun.lock` as a transitive dependency of `happy-dom`; `ws` is declared in no dependency section.

`fallow check` reports `ws` under `unused_dependency_overrides`, with the hint "may target a transitive dependency; pnpm install --frozen-lockfile is the ground truth".

Observed on a repo with 19 overrides, 14 of them transitive-only: exactly those 14 are flagged, and the flagged set equals `overrides − (dependencies ∪ devDependencies)` precisely. All 14 targets resolve in `bun.lock`, 11 of them pinned to exactly the forced version — they are CVE-fix pins, so acting on the finding would be a security downgrade.

### Expected behavior

The same resolution as #371: flag an override only when its target appears in no workspace `package.json` **and** no lockfile. Either of:

1. Add `bun.lock` (plus the legacy binary `bun.lockb`) to `collect_lockfile_packages`; or
2. Honour the documented scope — skip npm-style override analysis when the only lockfile present is bun's, or when `packageManager` is `bun@*`.

(1) seems preferable: the overrides are real and worth analysing, and only the resolution step is missing.

Separately, the hint text `pnpm install --frozen-lockfile is the ground truth` names pnpm in a repo that has no pnpm, which is misleading on its own.

### Fallow version

Reproduced on 3.15.0. The same code path is present at `v3.17.0` and on `main` (unchanged).

### Operating system

macOS (arm64)

---
_Drafted by Claude Code._
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `69dc2c13221ee32b578617d659352c5218191888`.  There
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
{"case_id": "fallow_rs_fallow__2341__69dc2c1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
