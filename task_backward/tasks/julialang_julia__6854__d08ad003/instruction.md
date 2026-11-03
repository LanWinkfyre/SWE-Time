# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Failure in test/sparse.jl when all tests run in serial

The failing line is https://github.com/JuliaLang/julia/blob/master/test/sparse.jl#L204 - when you run the test suite in serial (`make testall1`), the RNG just happens to pick a sparse matrix with 16 nonzero entries for `sprb45 = sprandbool(4, 5, 0.5)`. 



 Someone could probably go and calculate the probability of that ... for now, relaxing that test would make sense to me.

```
[tkelman@static-host julia]$ make testall1
    JULIA test/all
     * linalg1
     * linalg2
     * linalg3
     * core
     * keywordargs
     * numbers
     * strings
     * collections
     * hashing
     * remote
     * iobuffer
     * arrayops
     * simdloop
     * blas
     * fft
     * dsp
     * sparse
exception on 1: ERROR: test failed: sum(sprb45)[1] - 10 <= 5
 in error at error.jl:21
 in default_handler at test.jl:19
 in do_test at test.jl:39
 in runtests at /home/tkelman/Julia/julia/test/testdefs.jl:5
 in anonymous at multi.jl:652
 in run_work_thunk at multi.jl:613
 in remotecall_fetch at multi.jl:686
 in remotecall_fetch at multi.jl:701
 in anonymous at task.jl:1350
while loading sparse.jl, in expression starting on line 204
ERROR: test failed: sum(sprb45)[1] - 10 <= 5
 in error at error.jl:21
 in default_handler at test.jl:19
 in do_test at test.jl:39
 in runtests at /home/tkelman/Julia/julia/test/testdefs.jl:5
 in anonymous at multi.jl:652
 in run_work_thunk at multi.jl:613
 in remotecall_fetch at multi.jl:686
 in remotecall_fetch at multi.jl:701
 in anonymous at task.jl:1350
while loading sparse.jl, in expression starting on line 204
while loading /home/tkelman/Julia/julia/test/runtests.jl, in expression starting on line 35

make[1]: *** [all] Error 1
make: *** [testall1] Error 2
```
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `0fb601aa3075f488ae5e468ae0a5267717188164` and the full history behind it is present.
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
