# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[Windows] Alternate NT drive paths not handled in `convert_dos_path`

## Summary

* OS: Windows 11
* Architecture: 64-bit
* Psutil version: 6.1.1
* Python version: 3.13.1
* Type: core

## Description

`convert_dos_path` does not currently handle UNC paths or paths of the form `\??\X:` (as returned by Wine).
This results in the `psutil/tests/test_process.py::TestProcess::test_exe` test failing in the following cases:
* Python is run from a network share; or
* The tests are performed under Wine on a drive other than the one Python is installed on.

In the tests below, TestProcessPath is compiled from https://gist.github.com/klightspeed/cbb6b9957c521517673798bff4e15663

### Case 1: Python is run from a network share:
```
D:\venv\psutil\psutil>net use Z: \\localhost\c$
The command completed successfully.


D:\venv\psutil\psutil>set PATH=Z:\Program Files\Python313\Scripts\;Z:\Program Files\Python313\;%PATH%

D:\venv\psutil\psutil>python -m pytest -v -s --tb=short psutil/tests/test_process.py::TestProcess::test_exe
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0 -- Z:\Program Files\Python313\python.exe
cachedir: .pytest_cache
rootdir: D:\venv\psutil\psutil
configfile: pyproject.toml
plugins: xdist-3.6.1
collected 1 item

psutil/tests/test_process.py::TestProcess::test_exe FAILED

================================== FAILURES ===================================
____________________________ TestProcess.test_exe _____________________________
psutil\tests\test_process.py:741: in test_exe
    out = sh([exe, "-c", "import os; print('hey')"])
psutil\tests\__init__.py:335: in wrapper
    return fun(*args, **kwargs)
psutil\tests\__init__.py:498: in sh
    p = subprocess.Popen(cmd, **kwds)
Z:\Program Files\Python313\Lib\subprocess.py:1036: in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
Z:\Program Files\Python313\Lib\subprocess.py:1548: in _execute_child
    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,
E   FileNotFoundError: [WinError 2] The system cannot find the file specified
=========================== short test summary info ===========================
FAILED psutil/tests/test_process.py::TestProcess::test_exe - FileNotFoundError: [WinError 2] The system cannot find the file specified
============================== 1 failed in 2.24s ==============================

D:\venv\psutil\psutil>python -c "import os; import psutil; p = psutil.Process(os.getpid()); print(p.exe())"
\localhost\c$\Program Files\Python313\python.exe

D:\venv\psutil\psutil>net use Y: \\localhost\d$
The command completed successfully.


D:\venv\psutil\psutil>Y:\venv\TestProcessPath.exe
NtQuerySystemInformation(SystemProcessIdInformation) -> PID = 33004, Status = 00000000, ImageName = \Device\Mup\localhost\d$\venv\TestProcessPath.exe
QueryFullProcessImageNameW -> hProcess = FFFFFFFFFFFFFFFF, Success = 1, ImageName = \\localhost\d$\venv\TestProcessPath.exe

```

### Case 2: tests are run under Wine on a different drive to that Python is installed from:
```
Z:\home\klightspeed\wine-psutil\psutil>python -m pytest -v -s --tb=short psutil/tests/test_process.py::TestProcess::test_exe
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-8.3.4, pluggy-1.5.0 -- C:\Program Files\Python311-32\python.exe
cachedir: .pytest_cache
rootdir: Z:\home\klightspeed\wine-psutil\psutil
configfile: pyproject.toml
plugins: xdist-3.6.1
collected 1 item

psutil/tests/test_process.py::TestProcess::test_exe FAILED

================================== FAILURES ===================================
____________________________ TestProcess.test_exe _____________________________
C:\wine-psutil\psutil\psutil\tests\test_process.py:741: in test_exe
    out = sh([exe, "-c", "import os; print('hey')"])
psutil\tests\__init__.py:335: in wrapper
    return fun(*args, **kwargs)
psutil\tests\__init__.py:498: in sh
    p = subprocess.Popen(cmd, **kwds)
C:\Program Files\Python311-32\Lib\subprocess.py:1026: in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
C:\Program Files\Python311-32\Lib\subprocess.py:1538: in _execute_child
    hp, ht, pid, tid = _winapi.CreateProcess(executable, args,
E   FileNotFoundError: [WinError 2] File not found
=========================== short test summary info ===========================
FAILED psutil/tests/test_process.py::TestProcess::test_exe - FileNotFoundError: [WinError 2] File not found
============================== 1 failed in 0.45s ==============================

Z:\home\klightspeed\wine-psutil\psutil>python -c "import os; import psutil; p = psutil.Process(os.getpid()); print(p.exe())"
\Program Files\Python311-32\python.exe

Z:\home\klightspeed\wine-psutil\psutil>..\TestProcessPath\TestProcessPath.exe
NtQuerySystemInformation(SystemProcessIdInformation) -> PID = 312, Status = 00000000, ImageName = \??\Z:\home\klightspeed\wine-psutil\TestProcessPath\TestProcessPath.exe
QueryFullProcessImageNameW -> hProcess = ffffffff, Success = 1, ImageName = Z:\home\klightspeed\wine-psutil\TestProcessPath\
TestProcessPath.exe

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d461f4c0f0aad1a039c7d8bb724a4c7288ef2f39`.  There
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
{"case_id": "giampaolo_psutil__2494__d461f4c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
