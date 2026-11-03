# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
fallow audit's persistent worktree cache clutters git worktree list and IDE repo views

`fallow audit` creates a persistent, reusable base-snapshot cache under `/tmp/fallow-audit-base-cache-<hash>-<hash>` (kept up to `FALLOW_AUDIT_CACHE_MAX_AGE_DAYS`, default 30). Because this is implemented via real `git worktree add` against the project's repo, every one of these entries is registered permanently in `.git/worktrees` — and shows up in `git worktree list` — until GC reclaims it.

The problem isn't really cosmetic/VSCode-specific: by using `git worktree add`, this internal cache leaks into git's *shared* worktree registry, so any git-worktree-aware tool (VSCode's Git extension, GitLens, JetBrains, plain `git worktree list` in scripts) treats each cache entry as a first-class worktree of the repo. Since `fallow audit` runs frequently (pre-commit hooks, agent workflows, CI-adjacent local checks), this fills the worktree list with a dozen-plus stale, unnamed, detached-HEAD entries that have nothing to do with the developer's actual feature worktrees.

There's no good way to filter these out downstream: IDEs generally only support all-or-nothing worktree detection or exact-path ignore lists (not glob patterns), and the cache directory name changes on every run, so an ignore list can never keep up.

## Example

On a repo with normal day-to-day `fallow audit` usage (pre-commit hook + occasional manual runs), `git worktree list` accumulates entries like this over a couple weeks:

```
$ git worktree list
/home/me/project                                               1edd898 [main]
/home/me/project/.worktrees/some-feature-branch                4b98bc6 [some-feature-branch]
/tmp/fallow-audit-base-cache-4d66d757c3850985-0bf1329de3abd190  0bf1329 (detached HEAD)
/tmp/fallow-audit-base-cache-4d66d757c3850985-1200c6c1513461c7  1200c6c (detached HEAD)
/tmp/fallow-audit-base-cache-4d66d757c3850985-2f95530e5005385c  2f95530 (detached HEAD)
/tmp/fallow-audit-base-cache-4d66d757c3850985-3c7631e7ab5ddc03  3c7631e (detached HEAD)
/tmp/fallow-audit-base-cache-4d66d757c3850985-7dca4c8b21658583  7dca4c8 (detached HEAD)
/tmp/fallow-audit-base-cache-4d66d757c3850985-a6a0e735992b3ac5  a6a0e73 (detached HEAD)
/tmp/fallow-audit-base-cache-4d66d757c3850985-a9ad74924ab9fab5  a9ad749 (detached HEAD)
/tmp/fallow-audit-base-cache-4d66d757c3850985-b275bb7875e7a486  b275bb7 (detached HEAD)
/tmp/fallow-audit-base-cache-4d66d757c3850985-b475a0c749c2c302  b475a0c (detached HEAD)
/tmp/fallow-audit-base-cache-feeb4ba84a6fd0e9-12b8896e804c926c  12b8896 (detached HEAD)
/tmp/fallow-audit-base-cache-feeb4ba84a6fd0e9-80f2fcf23c8b865b  80f2fcf (detached HEAD)
/tmp/fallow-audit-base-cache-feeb4ba84a6fd0e9-be67662faeb8fd7f  be67662 (detached HEAD)
...
```

14 fallow-owned entries alongside 1 real feature worktree — every one of them shows up as its own "repository" in VSCode's Source Control view (via `git.detectWorktrees`), with no distinguishing name beyond a hash, cluttering the UI until the 30-day GC catches up. Note also the two different cache-key prefixes (`4d66d757c3850985`, `feeb4ba84a6fd0e9`) — these appear to be per-base-ref or per-worktree cache buckets, which compounds the count further on repos with multiple active branches/worktrees.

To be clear: I want to *keep* the cache and its reuse benefit — I just don't want fallow's private bookkeeping to be visible as first-class worktrees to every git-worktree-aware tool.

Requests, in order of preference:
1. Stop registering this cache via `git worktree add`, while keeping the same reuse semantics. Since it's a private, fallow-managed snapshot (not something a developer ever needs to `cd` into or see as a "worktree"), storing it as a bare/detached clone or a checkout under a separate `GIT_DIR` (e.g. under `.fallow/cache/`) would give identical caching behavior without adding an entry to the host repo's shared `.git/worktrees` registry. This is the only fix that actually solves the problem, since it removes the entries at the source rather than asking every downstream tool to special-case fallow's naming convention.
2. If `git worktree add` must stay (e.g. to reuse git's own worktree-local object/index machinery), provide a `fallow cache clean` / `fallow gc` command that deregisters (`git worktree remove`) all fallow-owned cache worktrees on demand, so at least clearing the clutter doesn't require hand-rolling a `git worktree list --porcelain | grep ... | git worktree remove` loop.

Workaround in the meantime: periodically running `git worktree list --porcelain | grep fallow-audit-base-cache- | ... | git worktree remove --force` to deregister them (they get recreated on the next `fallow audit`, so this does forfeit the reuse benefit for that next run — which is exactly why request #1 above is the one that actually matters).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bfab9d07e2d6b17041883083a463a8b623acc8f2`.  There
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
{"case_id": "fallow_rs_fallow__1815__bfab9d0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
