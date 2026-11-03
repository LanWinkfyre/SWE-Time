# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
New warning in the main (-Warray-bounds)

# Bug report

### Bug description:

```
$ cc --version
cc (Debian 12.2.0-14) 12.2.0
Copyright (C) 2022 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ ./configure -q && make -s
In file included from ./Include/internal/pycore_dict.h:11,
                 from Objects/typeobject.c:7:
In function ‘Py_DECREF_MORTAL’,
    inlined from ‘PyStackRef_XCLOSE’ at ./Include/internal/pycore_stackref.h:577:9,
    inlined from ‘_PyThreadState_PopCStackRef’ at ./Include/internal/pycore_stackref.h:662:5,
    inlined from ‘vectorcall_maybe.constprop’ at Objects/typeobject.c:2956:9:
./Include/internal/pycore_object.h:481:8: warning: array subscript 0 is outside array bounds of ‘PyObject[0]’ {aka ‘struct _object[]’} [-Warray-bounds]
  481 |     if (--op->ob_refcnt == 0) {
      |        ^
Written build/lib.linux-x86_64-3.14/_sysconfigdata__linux_x86_64-linux-gnu.py
Written build/lib.linux-x86_64-3.14/_sysconfig_vars__linux_x86_64-linux-gnu.json
Checked 112 modules (34 built-in, 77 shared, 1 n/a on linux-x86_64, 0 disabled, 0 missing, 0 failed on import)
```


### CPython versions tested on:

CPython main branch

### Operating systems tested on:

_No response_

  I would appreciate a workaround, but if it's not actual for gcc 14 - probably this not worth it.

It seems, there are no warnings on gcc-10: https://github.com/python/cpython/actions/runs/14139921809/job/39619432128
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `af2afd7c224389856e118d3f544c9621a016599f` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
