# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[NetBSD] processes which are exiting are not recognized as zombies

On NetBSD a process which is exiting, but has not become a zombie yet, is misreported in two ways:

- any `Process` method which internally gets `ESRCH` raises `NoSuchProcess` instead of `ZombieProcess`, even though the PID is still there
- `status()` returns `"sleeping"` or `"?"`

We look at `kinfo_proc2.p_stat`, which holds the *LWP* status. The process status is in `p_realstat`. The two sets of values overlap: `SDYING` (process, 3) has the same value as `LSSLEEP` (LWP, 3), so a dying process looks like it's sleeping.

A process exits by going `SDYING` -> `SDEAD` -> `SZOMB`, and only the last one happens to match the LWP value for zombie (5). That's why this went unnoticed: a zombie you create on purpose and inspect later is fine, but a process caught while it's exiting is not. It shows up as random CI failures under parallel testing:

```
=================================== FAILURES ===================================
________________________ TestFetchAllProcesses.test_all ________________________
[gw2] netbsd10 -- Python 3.11.15 /usr/pkg/bin/python3
psutil/_psbsd.py:436: in wrapper
    return fun(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
psutil/_psbsd.py:491: in exe
    return _psutil.proc_exe(self.pid)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ProcessLookupError: [Errno 3] No such process (originated from sysctl(KERN_PROC_PATHNAME))

The above exception was the direct cause of the following exception:
tests/test_process_all.py:139: in proc_info
    ret = fun()
          ^^^^^
psutil/__init__.py:383: in wrapper
    return method(self, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
psutil/__init__.py:874: in exe
    exe = self._proc.exe()
          ^^^^^^^^^^^^^^^^
psutil/_psbsd.py:440: in wrapper
    raise NoSuchProcess(pid, name) from err
E   psutil.NoSuchProcess: process no longer exists (pid=497, name='python3')

During handling of the above exception, another exception occurred:
tests/test_process_all.py:174: in test_all
    for info in self.iter_proc_info():
                ^^^^^^^^^^^^^^^^^^^^^
tests/test_process_all.py:168: in iter_proc_info
    ls = [proc_info(pid) for pid in psutil.pids()]
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_process_all.py:168: in <listcomp>
    ls = [proc_info(pid) for pid in psutil.pids()]
          ^^^^^^^^^^^^^^
tests/test_process_all.py:141: in proc_info
    check_exception(exc, proc, name, ppid)
tests/test_process_all.py:98: in check_exception
    tcase.assert_proc_gone(proc)
tests/__init__.py:1025: in assert_proc_gone
    self.assert_pid_gone(proc.pid)
tests/__init__.py:1018: in assert_pid_gone
    raise AssertionError(f"did not raise NoSuchProcess ({proc})")
E   AssertionError: did not raise NoSuchProcess (psutil.Process(pid=497, name='python3', status='zombie'))
```

While fixing this, I also noticed that `STATUS_SUSPENDED` is domented as being "NetBSD only", but it's never returned (so `status()` return `"?"`).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `774efdf4860986bd5c1b876e4d643b8c0bd6d6eb`.  There
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
{"case_id": "giampaolo_psutil__2907__774efdf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
