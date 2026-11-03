# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
`psutil.users()` is not thread-safe

Related to https://github.com/giampaolo/psutil/issues/2565. See file:
https://github.com/giampaolo/psutil/blob/01111d78/psutil/arch/linux/users.c
In here we use `setutent()` and `endutent()` syscalls, which appear to be "global", and hence not thread safe.

I'm not sure how to properly handle this because I'm confused by the existence of the 2 thread models: the "normal" thread-model, for which we could use `PyThread_acquire_lock` / `PyThread_release_lock` or `Py_BEGIN_ALLOW_THREADS` / `Py_END_ALLOW_THREADS` (are they the same?). And now there is the "free-thread python mode" which looks like a different beast. E.g. also in free-thread-python I'd be tempted to use a lock, but it should be defined as a global, so I'm not sure if we'd incur in the same scenario described in https://github.com/giampaolo/psutil/issues/2565.  Perhaps @colesbury has some advice?
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e7d619f82cc971a2184c4d498488de87b3d4a91e`.  There
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
{"case_id": "giampaolo_psutil__2614__e7d619f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
