# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[OS] Dict leak in `psutil_disk_io_counters()` on `kstat_read()` failure

I found a possible reference leak in the SunOS `psutil_disk_io_counters()`. `py_retdict` is created up front, but the `kstat_read()` failure path returns without releasing it.

File: `psutil/arch/sunos/disk.c`

Function: `psutil_disk_io_counters`

Relevant code:

```c
PyObject *py_retdict = PyDict_New();
...
if (kstat_read(kc, ksp, &kio) == -1) {
    kstat_close(kc);
    return psutil_oserror();
}
```

`PyDict_New()` returns a new reference. When `kstat_read()` fails, the function
closes `kc` and returns immediately, bypassing the `error:` label that would
release the dict:

```c
error:
    Py_XDECREF(py_disk_info);
    Py_DECREF(py_retdict);
    if (kc != NULL)
        kstat_close(kc);
    return NULL;
```

So `py_retdict` is leaked on every `kstat_read()` failure.

Suggested fix: replace the direct `return psutil_oserror();` with `goto error`
(the label already closes `kc`), so the owned dict is released on that path.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `567645ca8ccc8da5f7be423cc050cb5d6dc583ca`.  There
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
{"case_id": "giampaolo_psutil__2858__567645c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
