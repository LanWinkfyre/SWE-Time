# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
audit hangs to CI timeout on GitHub Actions runners, only on fallow >=3.4.2 (never reproduces locally)

## Summary

`fallow audit` hangs to timeout on GitHub Actions (`ubuntu-22.04`) runners on every version `>=3.4.2`, but never hangs locally in any repro attempted. Bisected across all published 3.x releases: `3.3.0` is the last good version, `3.4.2` is the first bad one (no `3.4.0`/`3.4.1` were published).

## Environment

- CI: GitHub Actions, `runs-on: ubuntu-22.04` (GitHub-hosted runner)
- Checkout: `actions/checkout@v6`, `fetch-depth: 0`, `sparse-checkout` set to a subdirectory of a large monorepo
- Package manager: bun 1.3.14 (`bun install --ignore-scripts --frozen-lockfile`)
- `fallow` installed as a devDependency via npm registry (`fallow` + `@fallow-cli/*` optional native binaries)
- Invocation: `fallow audit --base $(git merge-base origin/dev HEAD) --format json --quiet`, env `FALLOW_UPDATE_CHECK=off`, `FALLOW_TELEMETRY_DISABLED=1`, `DO_NOT_TRACK=1`

## Symptom

The CI step times out (tested at both 8 and 15 minutes) with `fallow` and (inconsistently, across different runs) a `git` or `git-remote-https` subprocess left running as orphans at kill time. Output is a single WARN line ~4-5s in, then nothing — no further stdout/stderr until the timeout kills it.

Locally, the same command against the same repo/branch/checkout shape completes in 5-25s every time, including:
- A plain run against the full local clone
- A local clone replicating CI's exact checkout (`git sparse-checkout init --cone` + `set <path>`, same `fetch-depth: 0`)
- A genuine fresh `git clone` over the network (not from a local/already-packed object store)

## Bisection

Tested real CI runs across published 3.x versions via binary search:

| Version | Result |
|---|---|
| 3.0.0 | ✅ pass |
| 3.3.0 | ✅ pass (fallow-audit step: ~22s) |
| 3.4.2 | ❌ hangs to timeout |
| 3.5.0 | ❌ hangs to timeout |
| 3.6.0 | ❌ hangs to timeout |
| 3.11.0 | ❌ hangs to timeout |
| 3.25.0 (latest at time of testing) | ❌ hangs to timeout |

`3.4.2`'s release notes mention a git worktree-backed base-snapshot cache added to `audit`. That's the most concrete lead we have, but we have not been able to confirm the actual mechanism.

## What we ruled out

- **Timeout length**: bumped 8min → 15min, still hung (15m44s)
- **Workload size**: `--no-css` cut local runtime but did not change the CI hang
- **Concurrency**: isolated fallow into its own CI step (not backgrounded alongside other lint checks) — still hung alone
- **Verbosity**: dropped `--quiet` — no extra output surfaced; fallow's progress UI appears to be a TTY-only spinner, invisible in CI's log capture either way
- **Git credential prompt**: set `GIT_TERMINAL_PROMPT=0` and `GIT_ASKPASS=/bin/false` to rule out a blocked credential prompt from an internal git subprocess call — did not help
- **Memory**: measured local peak RSS at ~828MB (far below patterns seen in #1843), so this doesn't look like the same OOM-silent-hang issue

We've worked around this for now by pinning to `3.3.0`, but would appreciate any pointers on what changed in `audit`'s git-worktree/base-snapshot caching in `3.4.2` that could behave differently under a GitHub Actions runner specifically vs. a local/dev machine (sandboxing, filesystem, or network differences affecting the new git subprocess calls, maybe?). Happy to run a debug build or `RUST_LOG=debug` against a scratch repo if that'd help narrow it down.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bb3893aa62cc51a0be60037ea7ab5ccf9ade3d5a`.  There
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
{"case_id": "fallow_rs_fallow__2615__bb3893a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
