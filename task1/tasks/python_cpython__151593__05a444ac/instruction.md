# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
test_abc hangs on TSan Parallel Test on Free Threading

# Bug report

Job: https://github.com/python/cpython/actions/runs/27618576478/job/81660859608?pr=151486

Python built with `./configure --config-cache --with-thread-sanitizer --with-pydebug --disable-gil`.

Test logs:

```
Run ./python -m test --tsan-parallel --parallel-threads=4 -j4 -W
Using random seed: 2157163694
0:00:00 load avg: 2.93 mem: 274.0 MiB Run 2 tests in parallel using 2 worker processes
0:00:12 load avg: 3.10 mem: 591.6 MiB [1/2] test_hashlib passed
0:00:42 load avg: 1.88 mem: 591.6 MiB running (1): test_abc (42.3 sec)
0:01:13 load avg: 1.14 mem: 591.7 MiB running (1): test_abc (1 min 12 sec)
0:01:43 load avg: 0.69 mem: 591.7 MiB running (1): test_abc (1 min 42 sec)
0:02:13 load avg: 0.42 mem: 591.7 MiB running (1): test_abc (2 min 13 sec)
...
0:35:59 load avg: 0.03 mem: 533.8 MiB running (1): test_abc (35 min 59 sec)
0:36:29 load avg: 0.02 mem: 533.8 MiB running (1): test_abc (36 min 29 sec)
0:37:00 load avg: 0.01 mem: 533.8 MiB running (1): test_abc (36 min 59 sec)
Error: The operation was canceled.
```

<!-- gh-linked-prs -->
### Linked PRs
* gh-151594
* gh-151597
* gh-151598
* gh-152133
* gh-152173
* gh-152200
* gh-152232
<!-- /gh-linked-prs -->






That's why I cannot reproduce it on the 3.15 branch.
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `a064b323f4350305e7486c7b1090cf12b19e7738` and the full history behind it is present.
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
