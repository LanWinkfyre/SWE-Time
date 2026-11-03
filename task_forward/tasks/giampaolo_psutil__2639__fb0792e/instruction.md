# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[AIX] pip install psutil `v7.1.0` fails due to missing `_psutil_posix.h`

## Summary

- OS: AIX 7.3
- Architecture: PowerPC
- Psutil version: v7.1.0
- Python version: 3.9.23
- Type: installation

## Description

```
      copying psutil/tests/test_linux.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_memleaks.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_misc.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_osx.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_posix.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_process.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_process_all.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_scripts.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_sudo.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_sunos.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_system.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_testutils.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_unicode.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      copying psutil/tests/test_windows.py -> build/lib.aix-7302-2345-64-cpython-39/psutil/tests
      running build_ext
      building 'psutil._psutil_aix' extension
      creating build/temp.aix-7302-2345-64-cpython-39/psutil
      creating build/temp.aix-7302-2345-64-cpython-39/psutil/arch/aix
      creating build/temp.aix-7302-2345-64-cpython-39/psutil/arch/all
      creating build/temp.aix-7302-2345-64-cpython-39/psutil/arch/posix
      gcc -maix64 -fPIC -pthread -O2 -Wno-unused-result -Wsign-compare -DNDEBUG -g -O2 -Wall -I/opt/freeware/include -I/usr/include -DAIX_GENUINE_CPLUSCPLUS -D_ALL_SOURCE -D_LINUX_SOURCE_COMPAT -I/opt/freeware/include -I/usr/include -DAIX_GENUINE_CPLUSCPLUS -D_ALL_SOURCE -D_LINUX_SOURCE_COMPAT -DPSUTIL_POSIX=1 -DPSUTIL_SIZEOF_PID_T=4 -DPSUTIL_VERSION=710 -DPSUTIL_AIX=1 -I/opt/freeware/include/python3.9 -c psutil/_psutil_aix.c -o build/temp.aix-7302-2345-64-cpython-39/psutil/_psutil_aix.o
      psutil/_psutil_aix.c:54:10: fatal error: _psutil_posix.h: No such file or directory
         54 | #include "_psutil_posix.h"
            |          ^~~~~~~~~~~~~~~~~
      compilation terminated.
      error: command '/opt/freeware/bin/gcc' failed with exit code 1
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for psutil
Successfully built rsmate
Failed to build psutil
error: failed-wheel-build-for-install
Ã Failed to build installable wheels for some pyproject.toml based projects
â°â> psutil
script returned exit code 1
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `fb0792eb48465438708575f96d7ec997240a98cf`.  There
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
{"case_id": "giampaolo_psutil__2639__fb0792e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
