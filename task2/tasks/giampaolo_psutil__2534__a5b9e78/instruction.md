# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
Kill Process Tree docs should provide hint about os.killpg

## Summary

* OS: Linux
* Type: doc

## Description

The https://psutil.readthedocs.io/en/latest/index.html#kill-process-tree docs should provide a hint that there is a simpler way to kill a subprocess tree that is often good enough and does not require psutil, namely creating a built-in `subprocess.Popen` object with `process_group=0` and then using the built-in `os.killpg()`.

Less experienced Python users at several firms I've worked at are finding incomplete advice on the internet (such as the top answer on https://stackoverflow.com/questions/6549669/how-to-kill-process-and-child-processes-from-python), then taking a dependency on psutil and (if they're at least a little more thorough) copy/pasting the `kill_proc_tree()` implementation out of the psutil docs (rather than the worse code on Stackoverflow), when instead they should just be using `os.killpg()`.

I can submit a PR with a small docs update if you agree.

Thanks for the great work on psutil.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a5b9e78927245781b71e7e065a515ebd06fe4908`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "giampaolo_psutil__2534__a5b9e78",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
