# Locate the commit that introduced this regression

A regression was reported against `kubernetes/kubernetes`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
kube-apiserver has test code linked

Code that uses test infrastructure NEEDS to be in separate packages and used only from tests.

```
      --test.bench="": regular expression to select benchmarks to run
      --test.benchmem[=false]: print memory allocations for benchmarks
      --test.benchtime=1s: approximate run time for each benchmark
      --test.blockprofile="": write a goroutine blocking profile to the named file after execution
      --test.blockprofilerate=1: if >= 0, calls runtime.SetBlockProfileRate()
      --test.count=1: run tests and benchmarks `n` times
      --test.coverprofile="": write a coverage profile to the named file after execution
      --test.cpu="": comma-separated list of number of CPUs to use for each test
      --test.cpuprofile="": write a cpu profile to the named file during execution
      --test.memprofile="": write a memory profile to the named file after execution
      --test.memprofilerate=0: if >=0, sets runtime.MemProfileRate
      --test.outputdir="": directory in which to write profiles
      --test.parallel=4: maximum test parallelism
      --test.run="": regular expression to select tests and examples to run
      --test.short[=false]: run smaller test suite to save time
      --test.timeout=0: if positive, sets an aggregate time limit for all tests
      --test.trace="": write an execution trace to the named file after execution
      --test.v[=false]: verbose: print additional output
```




I usually run git bisect with this script

``` bash
#! /bin/bash

godep go build -o kube-apiserver ./cmd/kube-apiserver || exit 255

./kube-apiserver -h 2>&1 | grep -q '\-\-test\.bench' && exit 1 || exit 0
```
```

## What you have

- `/testbed/repo` is a git clone of `kubernetes/kubernetes` truncated just after the regression was
  reported.  `HEAD` is `fd03c2c1d742bba8701fe3e15338ac6302dbb351` and the full history behind it is present.
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
