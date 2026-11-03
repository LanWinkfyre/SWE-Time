# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Agent gate (hooks --target agent) runs bare `fallow audit` → base auto-detects to stale local `main`, with no config/env/flag escape hatch (twin of #242)

### What happened?

The **agent gate** (`fallow hooks install --target agent`, the Claude Code / Codex `fallow-gate.sh`) runs **bare `fallow audit`**, whose base **auto-detects to the local default-branch ref** (`main`). On long-lived local checkouts — e.g. teams that work entirely in `git worktree`s cut from `origin/main` and never run `git checkout main && git pull` — the local `main` ref goes stale. The audit then diffs every branch against an ancient base, surfaces the whole already-merged delta as "changed", finds inherited debt in those files, and returns `verdict: fail`, blocking **every** commit/push (even a one-line change on a branch freshly cut from `origin/main`).

This is the agent-gate twin of #242, which you fixed for the **git** pre-commit hook (resolve `@{upstream}` / merge-base at commit time, v2.58). The agent gate never got that treatment and still relies on `fallow audit`'s auto-detect.

Crucially, there is **no escape hatch** for the agent gate:

- The generated `fallow-gate.sh` runs `fallow audit --format json --quiet --explain` with no base, and `fallow hooks install --target agent --dry-run` shows the script is identical with or without `--changed-since`/`--base` (the flag is ignored for the agent target).
- The `fallow audit` **binary ignores `FALLOW_CHANGED_SINCE`** (it appears to be GitLab-CI-template only). Verified below.
- `AuditConfig` exposes no base/changed-since key.

So the only way to fix it downstream is to wrap or replace the generated gate, which `fallow setup-hooks` / `fallow hooks install` then regenerates over.

### Evidence

`fallow audit --format json` reports the base it resolved in `base_ref`:

```
$ fallow audit --format json --quiet | jq .base_ref
"main"                      # local main ref — stale on worktree checkouts

$ fallow audit --base origin/main --format json --quiet | jq .base_ref
"origin/main"               # correct
```

`FALLOW_CHANGED_SINCE` is ignored by the binary (env value has no effect; only the flag changes the verdict):

```
$ FALLOW_CHANGED_SINCE=<stale-sha> fallow audit --format json --quiet | jq .verdict
"pass"                      # env ignored
$ fallow audit --base <stale-sha> --format json --quiet | jq .verdict
"fail"                      # flag honored
```

### Expected behavior

Any one of:

1. **Agent gate resolves the base like the git hook (#242)** — `git merge-base @{upstream} HEAD` with a configurable remote-tracking fallback (e.g. `origin/<default>`), baked into the generated `fallow-gate.sh`; or
2. **`fallow init`/`hooks install --target agent` honors `--changed-since`/`--base`** and bakes it into the generated agent gate (today it's silently ignored for the agent target); or
3. **`fallow audit` honors a config key / env var for the base** (e.g. make `FALLOW_CHANGED_SINCE` apply to the binary, or add `[audit] base`), so the gate can be pinned without editing the generated script.

Option 1 matches what you already shipped for the git hook and would make the agent gate correct out of the box.

### Reproduction

```bash
# A repo whose local `main` lags origin/main (simulating a long-lived worktree checkout)
git update-ref refs/heads/main <old-sha>     # local main now stale
fallow hooks install --target agent
# bare audit auto-detects local main -> diffs against the stale base -> verdict: fail
fallow audit --format json --quiet | jq '{base_ref, verdict}'
# vs the correct base:
fallow audit --base origin/main --format json --quiet | jq '{base_ref, verdict}'
```

### Fallow version

2.86.0

### Operating system

macOS

### Configuration

No config required — the agent gate runs bare `fallow audit` regardless of `.fallowrc`.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `47a0e4cfd291e8203480fba8ae1dc6edda00f906`.  There
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
{"case_id": "fallow_rs_fallow__1168__47a0e4c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
