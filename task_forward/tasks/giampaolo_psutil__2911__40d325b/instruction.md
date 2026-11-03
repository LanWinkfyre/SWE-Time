# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[NetBSD] `environ()` can raise EINVAL on zombie process

Observed on CI:

```
```
=================================== FAILURES ===================================
________________________ TestFetchAllProcesses.test_all ________________________
[gw3] netbsd10 -- Python 3.11.15 /usr/pkg/bin/python3
tests/test_process_all.py:178: in test_all
    for info in self.iter_proc_info():
                ^^^^^^^^^^^^^^^^^^^^^
tests/test_process_all.py:172: in iter_proc_info
    ls = [proc_info(pid) for pid in psutil.pids()]
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_process_all.py:172: in <listcomp>
    ls = [proc_info(pid) for pid in psutil.pids()]
          ^^^^^^^^^^^^^^
tests/test_process_all.py:141: in proc_info
    check_exception(exc, proc, name, ppid)
tests/test_process_all.py:86: in check_exception
    tcase.assert_proc_zombie(proc)
tests/__init__.py:1068: in assert_proc_zombie
    proc.as_dict()
psutil/__init__.py:712: in as_dict
    ret = meth()
          ^^^^^^
psutil/__init__.py:383: in wrapper
    return method(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psutil/__init__.py:1088: in environ
    return self._proc.environ()
           ^^^^^^^^^^^^^^^^^^^^
psutil/_psbsd.py:449: in wrapper
    raise err from None
psutil/_psbsd.py:437: in wrapper
    return fun(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
psutil/_psbsd.py:533: in environ
    return _psutil.proc_environ(self.pid)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   OSError: [Errno 22] Invalid argument (originated from kvm_getenvv(pid=495))
============================= slowest 5 durations ==============================
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `40d325b74fcd340658766ead9a10616df411a4c7`.  There
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
{"case_id": "giampaolo_psutil__2911__40d325b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
