# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[macOS] incorrect zombie process detection logic

Observed on CI:

```________________________ TestFetchAllProcesses.test_all ________________________
[gw0] darwin -- Python 3.8.10 /private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/bin/python
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/_psosx.py:372: in wrapper
 return fun(self, *args, **kwargs)
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/_psosx.py:428: in cmdline
 return cext.proc_cmdline(self.pid)
E   ProcessLookupError: [Errno 3] assume no such process (originated from sysctl(KERN_PROCARGS2) -> EINVAL)

The above exception was the direct cause of the following exception:
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/tests/test_process_all.py:87: in proc_info
 info[fun_name] = fun()
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/__init__.py:749: in cmdline
 return self._proc.cmdline()
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/_psosx.py:376: in wrapper
 raise NoSuchProcess(pid, name) from err
E   psutil.NoSuchProcess: process no longer exists (pid=773, name='sudo')

During handling of the above exception, another exception occurred:
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/tests/test_process_all.py:127: in test_all
 for info in self.iter_proc_info():
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/tests/test_process_all.py:122: in iter_proc_info
 ls = [proc_info(pid) for pid in psutil.pids()]
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/tests/test_process_all.py:122: in <listcomp>
 ls = [proc_info(pid) for pid in psutil.pids()]
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/tests/test_process_all.py:89: in proc_info
 check_exception(exc, proc, name, ppid)
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/tests/test_process_all.py:59: in check_exception
 tcase.assert_proc_gone(proc)
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/tests/__init__.py:1074: in assert_proc_gone
 self.assert_pid_gone(proc.pid)
/private/var/folders/y6/nj790rtn62lfktb1sh__79hc0000gn/T/cibw-run-3rnwugiq/cp38-macosx_arm64/venv-test-arm64/lib/python3.8/site-packages/psutil/tests/__init__.py:1067: in assert_pid_gone
 raise AssertionError("did not raise NoSuchProcess")
E   AssertionError: did not raise NoSuchProcess

```

What happens: 

1) fetching of `cmdline()` results in EINVAL, which is translated to NoSuchProcess
2) still, creating a `Process` instance for that PID succeeds

The C logic appears wrong because already in there we know that the PID exists, and we raise NSP in the hope that the _psosx.py will translate it to ZombieProcess exception, but since the PID is not a zombie that won't happen.
The correct logic at the C level in case of EINVAL should be to raise `AccessDenied` instead.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `047b09c070841e4743eb23d4063b4f19b2397433`.  There
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
{"case_id": "giampaolo_psutil__2650__047b09c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
