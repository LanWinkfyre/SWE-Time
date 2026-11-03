# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[linux] "No such file or directory: '/proc/xxxxxxx/cwd'" with `psutil.process_iter`

## Summary

* OS: Ubuntu 22.04.5 LTS
* Architecture: x86_64
* Psutil version: 7.0.0
* Python version: 3.11.10
* Type: core

## Description
Issue very similar to https://github.com/giampaolo/psutil/issues/2418

When using `psutil.process_iter`, a `FileNotFoundError` can be raised when `/proc/xxxxxxx/cwd` is not found. 
Similarly to the issue 2418, this could be a race condition when `/proc/xxxxxxx/cwd` was deleted but `/proc/xxxxxxx` still exists. 

This one is hard to reproduce, this happens very rarely.
Stack trace exemple:
```
  File "/home/ubuntu/data/spindata/spindata/Utilities/misc_tools.py", line 878, in get_current_process
    return [p for p in psutil.process_iter(attrs=["pid", "cwd", "cmdline"]) if p.info["pid"] == os.getpid()][0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/data/spindata/spindata/Utilities/misc_tools.py", line 878, in <listcomp>
    return [p for p in psutil.process_iter(attrs=["pid", "cwd", "cmdline"]) if p.info["pid"] == os.getpid()][0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/.cache/pypoetry/virtualenvs/spindata-2prIfHBO-py3.11/lib/python3.11/site-packages/psutil/__init__.py", line 1527, in process_iter
    proc.info = proc.as_dict(attrs=attrs, ad_value=ad_value)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/.cache/pypoetry/virtualenvs/spindata-2prIfHBO-py3.11/lib/python3.11/site-packages/psutil/__init__.py", line 573, in as_dict
    ret = meth()
          ^^^^^^
  File "/home/ubuntu/.cache/pypoetry/virtualenvs/spindata-2prIfHBO-py3.11/lib/python3.11/site-packages/psutil/__init__.py", line 777, in cwd
    return self._proc.cwd()
           ^^^^^^^^^^^^^^^^
  File "/home/ubuntu/.cache/pypoetry/virtualenvs/spindata-2prIfHBO-py3.11/lib/python3.11/site-packages/psutil/_pslinux.py", line 1646, in wrapper
    return fun(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/.cache/pypoetry/virtualenvs/spindata-2prIfHBO-py3.11/lib/python3.11/site-packages/psutil/_pslinux.py", line 2057, in cwd
    return readlink(f"{self._procfs_path}/{self.pid}/cwd")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ubuntu/.cache/pypoetry/virtualenvs/spindata-2prIfHBO-py3.11/lib/python3.11/site-packages/psutil/_pslinux.py", line 202, in readlink
    path = os.readlink(path)
           ^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/proc/295094/cwd'
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `74b707fc735b64ea159e118e26acc2ecfb78a719`.  There
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
{"case_id": "giampaolo_psutil__2514__74b707f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
