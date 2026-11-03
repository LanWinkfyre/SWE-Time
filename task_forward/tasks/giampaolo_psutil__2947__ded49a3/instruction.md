# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
Introduce C-level critical warning messages


There are circumstances in C where something is clearly "off" but not "off" enough to justify raising an exception, e.g. when we return incomplete results after a sanity check on kernel data failed. In these cases we signal the event via `psutil_debug()`, which prints a message to stderr, but only if psutil is in debug mode (`PSUTIL_DEBUG=1` env var), which is almost never enabled. So in practice these events go unnoticed.

Proposal: add a new `psutil_warn()` C helper that emits an actual `RuntimeWarning`, so it reaches the Python layer, and use it in the (rare) places where it's justified. The warning message includes the C file + line number where it originated from.

Some practical notes on how warnings behave:

- With Python's default filters the same warning is printed only once per process, per calling location. Repeated calls from the same place stay silent after the first one.
- It can be silenced with the standard machinery: `warnings.filterwarnings("ignore", category=RuntimeWarning)`, `python -W ignore::RuntimeWarning`, or the `PYTHONWARNINGS` env var.
- With `-W error` (warnings turned into exceptions, common in test suites) the exception is discarded: psutil functions never fail because of these warnings.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ded49a3a720c8501bcf0d32ca4a31e09007cfd19`.  There
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
{"case_id": "giampaolo_psutil__2947__ded49a3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
