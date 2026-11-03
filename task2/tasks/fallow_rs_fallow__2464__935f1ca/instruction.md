# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
`fallow init --hooks` Lefthook job skips project-local binary

## Description

Fallow 3.20.0's official Lefthook integration can silently skip a project-local Fallow installation during a real Git commit.

The generated job starts with:

```sh
command -v fallow >/dev/null 2>&1 || exit 0
```

A normal installed Lefthook Git hook preserves the caller's environment and does not add `node_modules/.bin` to `PATH`. In a pnpm project where Fallow is pinned locally (and not installed globally), `command -v fallow` therefore fails and the generated job exits successfully without auditing anything.

## Steps to Reproduce

1. In a pnpm repository, install Fallow 3.20.0 and Lefthook 2.1.12 locally.
2. Run `pnpm exec fallow init --hooks` and install the generated Lefthook hook.
3. Confirm that plain `command -v fallow` exits 1 while `pnpm exec fallow --version` works.
4. Stage a newly introduced finding that `fallow audit --base HEAD~1` rejects, such as an unused exported TypeScript symbol.
5. Commit through the real installed Git hook with `git commit`.

## Expected Behavior

The generated Lefthook job invokes the project's pinned Fallow binary. The audit runs and rejects a commit that introduces a finding.

## Actual Behavior

The real Git commit succeeds. Lefthook reports the Fallow job as successful in about 0.01s because the `command -v fallow` guard exits before running the audit.

On the resulting commit, invoking the same pinned binary directly proves the finding is real:

```sh
node_modules/.bin/fallow audit --base HEAD~1 --format json --quiet
```

This exits 1 with `verdict=fail`, `dead_code_introduced=1`, and the introduced unused export.

A controlled comparison also shows why `pnpm exec lefthook run pre-commit` is not representative: pnpm modifies `PATH`, so that invocation finds `node_modules/.bin/fallow` and runs the audit. The real Git hook does not.

## Environment

- Fallow: 3.20.0
- Lefthook: 2.1.12
- pnpm: 12.1.0
- OS: macOS

## Suggested Fix

Generate a Lefthook command that reliably invokes the repository's pinned Fallow binary in the real Git-hook environment, while preserving supported installation modes. Please add an execution-level regression test that runs the generated Lefthook job with Fallow available only as a project-local dependency; the current string assertions for `command -v fallow` do not exercise this failure mode.

## Additional Context

The relevant generator and string-only tests are in `crates/cli/src/init.rs`. This was discovered while adopting the documented `fallow init --hooks` flow in an existing Lefthook repository.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `935f1ca88e7d0925c75bcb159df915d6e55db84c`.  There
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
{"case_id": "fallow_rs_fallow__2464__935f1ca",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
