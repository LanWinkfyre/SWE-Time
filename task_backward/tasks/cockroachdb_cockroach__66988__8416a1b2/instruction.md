# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
bazel,build:  breaks local test build opaquely

**Describe the problem**

Running local tests through bazel is currently broken on master. Try `dev test pkg/kv/kvserver/batcheval -f=TestDBAddSSTable` (or it's expanded form: `bazel test //pkg/kv/kvserver/batcheval:batcheval_test --test_filter=TestDBAddSSTable`).

**To Reproduce**

I bisected the failure using the following:




**Expected behavior**

We should be able to run these tests locally through bazel. Would've helped with the iteration time for @erikgrinaker over at #66910. +cc @rickystewart for triage.

Epic CRDB-8036
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `858fc125ebb5585120a42fd415058b8f9db76df3` and the full history behind it is present.
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
