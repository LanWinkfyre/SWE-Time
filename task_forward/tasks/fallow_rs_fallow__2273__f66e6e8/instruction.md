# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
GitHub Action: install.sh hangs indefinitely in the verifyInstalled() node heredoc on a self-hosted macOS runner

## Summary

On a self-hosted macOS ARM64 runner, `fallow-rs/fallow@v3.10.0`'s **Install fallow** step hangs after `npm install` succeeds and never returns. Every PR in the repository was blocked for a day: the job hit its `timeout-minutes` and reported only `The operation was canceled`.

`bash -x` on the action's own `action/scripts/install.sh`, run inside the same job, pins it to one command:

```
trace: + npm install -g --ignore-scripts fallow@3.10.0
trace: changed 6 packages in 1s
trace: + script_dir=/…/_actions/fallow-rs/fallow/2881013…/action/scripts
trace: + action_root=/…/_actions/fallow-rs/fallow/2881013…
trace: + verify_script=/…/npm/fallow/scripts/verify-binary.js
trace: ++ npm root -g
trace: + global_root=/…/_temp/npm-fallow/lib/node_modules
trace: + global_fallow_root=/…/_temp/npm-fallow/lib/node_modules/fallow
trace: ++ node -p 'require('\''/…/package.json'\'').version'
trace: + installed_fallow_version=3.10.0
trace: + ACTION_VERIFY_SCRIPT=/…/npm/fallow/scripts/verify-binary.js
trace: + FALLOW_VERIFY_RESOLVE_FROM=/…/_temp/npm-fallow/lib/node_modules/fallow
trace: + node
```

The trace stops at `+ node`, which is the heredoc at `action/scripts/install.sh:126` calling `verifyInstalled()`, and the script then consumes the entire 150s bound I gave it. In real runs it consumed 9.5 minutes before the job timeout killed it.

## Environment

- self-hosted, macOS 15 / Darwin arm64, ephemeral runner (one job per lifecycle), runner 2.336.0
- node 22.23.x, npm from the same distribution
- action pinned to `28810138faa8fdbc830b8d585d0c15d65c39c3fd` (v3.10.0), `version: "3.10.0"`
- `command: audit`, `format: pr-comment-github`, `review-comments: true`, `comment: true`

## What does not reproduce it

Every command in that step, run from a shell on the same host, is fast. A probe step in the same job, same runner, same environment:

```
probe node-version rc=0 1s
probe npm-version rc=0 0s
probe npm-root-g rc=0 0s
probe npm-install-g rc=0 4s        # npm install -g --ignore-scripts fallow@3.10.0
probe fallow-version rc=0 0s
```

And the verifier itself, invoked exactly as `install.sh` invokes it, against a sentinel-less `--ignore-scripts` install:

```
{"ok":true}   # 0-5s, action-bundled verify-binary.js, no .fallow-verified present
{"ok":true}   # 2s under node v20.20.2
{"ok":true}   # 5s under node v22.22.2
fallow 3.10.0 … verified: yes   # 11s, `fallow --version` on the unverified install
```

So it is not the download, not the install, not the signature check as such, and not the CLI's lazy verify. Also ruled out: npm global-prefix contention between concurrent jobs (giving each job its own `npm_config_prefix` under `RUNNER_TEMP` changed nothing), and repository size (`fallow audit --gate new-only` on this repo takes 10-30s from the CLI).

The only difference I have not been able to eliminate is that in the failing case `node` is reading its program from the heredoc on **stdin**, inside an Actions step, rather than via `-e`.

## Suggested handling

Whatever the cause, the step is unbounded, so a hang there costs the whole job with no attribution. A timeout around the verification (the GitHub-API digest fallback already carries `DIGEST_TIMEOUT_MS = 10000`) would turn this into a diagnosable error. Passing the verifier program as a file or `-e` argument rather than on stdin would also be worth trying, if that is the trigger.

Happy to run further probes on this host: the runner is reproducible, it hangs on every run.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f66e6e8d30cdeedaec9f07c740a4584a00442269`.  There
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
{"case_id": "fallow_rs_fallow__2273__f66e6e8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
