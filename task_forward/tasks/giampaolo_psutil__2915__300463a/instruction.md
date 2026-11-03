# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
Stop publishing free-threaded 3.13 (cp313t) wheels

Free-threaded wheels account for about 0.21% of psutil downloads, and Python 3.13t represents only a subset of those. Monthly downloads:

```
$ python3 scripts/internal/print_downloads.py -a
...
Wheel types                           Downloads        %
--------------------------------------------------------
wheel (abi3)                        222,384,688    96.95
sdist (built from source)             4,932,222     2.15
wheel (version specific)              1,582,346     0.69
wheel (free-threaded)                   483,840     0.21
```     

Free-thread support in `3.13t` is experimental (https://peps.python.org/pep-0779/) and overall discouraged. Slower performance (40% on single thread), it misses safety fixes, etc.

In addition, we don't really have a choice either: manylinux stopped building 3.13 free-threaded images  (https://github.com/pypa/manylinux/issues/1882) and cibuildwheel 4.0 removed them (https://github.com/pypa/cibuildwheel/pull/2684. Keeping the wheels means staying on cibuildwheel 3.x.

So let's just provide `3.14t` (and soon universaal `3.15`) and be done with it.

Users who are on free-thread 3.13 will either pick up psutil 7.2.2 or 8+ installed from sources.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `300463a1cac0fa7269caf13df17e0d8159f37ff0`.  There
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
{"case_id": "giampaolo_psutil__2915__300463a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
