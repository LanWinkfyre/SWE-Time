# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
False `NoSuchProcess("PID has been reused")` when process identity can't be determined

Process identity is determined via `(pid, create_time)`, and is checked before terminate(), send_signal(), etc. Problem: sometimes create time is legitimately unknown. On Windows fast `create_time()` method, which raises `AccessDenied` for most elevated processes, and `Process.__init__` then stores `(pid, None)`. Same thing for zombies: `__init__` swallows `ZombieProcess` and keeps `(pid, None)`, and on NetBSD / OpenBSD a zombie that can be queried reports create time 0 (#2287, #2593).

When one side of the comparison has a real create time and the other has None / 0, the two idents differ, and psutil concludes the PID was reused by a new process. It wasn't: we simply couldn't fetch the identity the second time. Net effect, e.g. on Windows: `terminate()` on a process that meanwhile became inaccessible raises `NoSuchProcess("PID has been reused")` even though the process is still there.

I caught on NetBSD CI, where terminate() claimed pid 484 was reused while teardown proved the pid still existed 15 seconds later (it had become a zombie):

```
tests/test_process.py:1624: in test_wait_non_children
    child.terminate()
psutil/__init__.py:571: in _raise_if_pid_reused
    raise NoSuchProcess(self.pid, self._name, msg=msg)
E   psutil.NoSuchProcess: process no longer exists and its PID has been reused (pid=484)
...
E   psutil.TimeoutExpired: timeout after 15 seconds (pid=484)
E   AssertionError: 484   # pid_exists(484) still True
```

The fix: a null create time on either side is not proof of reuse; only flag reuse when both idents are known and differ.


Note this is really the completion of #2287: back then a zombie's null ctime silently broke `is_running()`, which returned `False` for a process that was still there. The PID-reuse detection added later in 3d21a43a turned that same condition into a raised `NoSuchProcess("PID has been reused")` on the `terminate()` / `send_signal()` / `kill()` path.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `16fc07e5e232188db4d6904afbb03b321ae130ef`.  There
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
{"case_id": "giampaolo_psutil__2895__16fc07e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
