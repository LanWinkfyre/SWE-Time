# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[FreeBSD / OpenBSD] false "PID has been reused" NoSuchProcess on system clock updates

`Process._get_ident()` identifies a process uniquely as `(pid, create_time())` in order to detect PID reuse. On FreeBSD and OpenBSD this breaks in case of system clock updates (e.g. via NTP) because `create_time()` will return a different time, even if PID/process is the same (this is done in `Process.__eq__`).

The same problem was fixed on Linux (#2527, #2544), NetBSD (#2579) and macOS (#2582) by using a monotonic start time for the identity. But FreeBSD and OpenBSD were left out because their kernels don't provide monotonic times.

Failures related to this observed on CI:

```
tests/test_system.py:222: in test_deprecated_prefetch_empty_attrs
    p = next(psutil.process_iter(attrs=[]))
E   StopIteration
```

...and:

```
=================================== FAILURES ===================================
________________________ TestFetchAllProcesses.test_all ________________________
[gw3] openbsd7 -- Python 3.13.13 /usr/local/bin/python3
tests/test_process_all.py:150: in test_all
    return pytest.fail(''.join(failures))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   Failed:     
E       ======================================================================
E       FAIL: name=test_ppid, pid=60997, ret=1
E       
E       ----------------------------------------------------------------------
E       Traceback (most recent call last):
E         File "/home/runner/work/psutil/psutil/tests/test_process_all.py", line 99, in proc_info
E           ret = fun()
E         File "/home/runner/work/psutil/psutil/psutil/__init__.py", line 383, in wrapper
E           return method(self, *args, **kwargs)
E         File "/home/runner/work/psutil/psutil/psutil/_common.py", line 262, in wrapper
E           raise err from None
E         File "/home/runner/work/psutil/psutil/psutil/_common.py", line 260, in wrapper
E           return fun(self)
E         File "/home/runner/work/psutil/psutil/psutil/__init__.py", line 791, in ppid
E           self._raise_if_pid_reused()
E           ~~~~~~~~~~~~~~~~~~~~~~~~~^^
E         File "/home/runner/work/psutil/psutil/psutil/__init__.py", line 571, in _raise_if_pid_reused
E           raise NoSuchProcess(self.pid, self._name, msg=msg)
E       psutil.NoSuchProcess: process no longer exists and its PID has been reused (pid=1, name='init')
```

The fix is to just not provide the PID reuse check on these platforms and be done with it.

This is what already partially happens on Windows. `create_time()` there is a fixed value recorded at process creation (so it's stable across clock updates and usable for identity), but in case of `AccessDenied` we only use the PID for process identity, which de facto means the PID reuse check is disabled.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `522873f0806cdc0b707b4489193274fe4cb3cfba`.  There
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
{"case_id": "giampaolo_psutil__2888__522873f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
