# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Numpy master segfaults in Scipy testsuite


Observed on travis, and repro locally. Crashes at
```
$ gdb --args python runtests.py -g -t scipy/signal/tests/test_spectral.py:TestSTFT.test_permute_axes
Program received signal SIGSEGV, Segmentation fault.
0x00007fffedea4671 in PyArray_Transpose (ap=0x7fffd9244cb0, permute=0x7fffffff9b30) at numpy/core/src/multiarray/shape.c:711
711	            if (reverse_permutation[axis] != -1) {
(gdb) bt
#0  0x00007fffedea4671 in PyArray_Transpose (ap=0x7fffd9244cb0, permute=0x7fffffff9b30) at numpy/core/src/multiarray/shape.c:711
#1  0x00007fffede6b5db in array_transpose (self=0x7fffd9244cb0, args=0x7fffd97a0610) at numpy/core/src/multiarray/methods.c:1956
#2  0x00007ffff7adb7a1 in PyEval_EvalFrameEx () from /lib64/libpython2.7.so.1.0
...
```
Result from git bisect:
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `f24da28e7bef4befa51354fff864bb7b5b3e07f9` and the full history behind it is present.
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
